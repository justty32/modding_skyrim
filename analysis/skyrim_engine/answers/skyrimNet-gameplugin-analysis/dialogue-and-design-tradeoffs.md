# 3. 對話改變機制 (Dialogue Changes)

[返回入口](../skyrimNet-gameplugin-analysis.md)

## 3. 對話改變機制 (Dialogue Changes)

### 3.1 Dialogue Response Pipeline

`dialogue_response.prompt` 是核心對話 prompt，結構極簡：

```
[system] 你是 {name}, 一個 {gender} {race}。你正在對 {target} 說話。
  + 完整 character bio (經由 render_subcomponent("system_head", "full"))
[user]
  + 場景資訊 + 附近人物 + 最近事件 (經由 render_template("event_history"))
  + 使用者最終指令 (user_final_instructions submodules)
  + 可選: 嵌入 action 指令
```

關鍵設計：**NPC 的 identity 是透過 character bio submodules 拼裝的**，而非寫死在 prompt 中。

### 3.2 對話注入 API

從 `SkyrimNetApi.psc`：

```papyrus
; 一般廣播對話
RegisterDialogue(speaker, dialogue)
RegisterDialogueByUUID(speakerUuid, dialogue)

; 指定聽者的對話
RegisterDialogueToListener(speaker, listener, dialogue)

; 直接旁白（Direct Narration）— 強制 NPC 回應一個「事實」
DirectNarration(content, originatorActor, targetActor)
; 特例: content="" 時只建立短期事件，不持久化

; 持久事件（不觸發對話反應）
RegisterPersistentEvent(content, originatorActor, targetActor)

; 玩家對話轉換（透過 LLM 轉成 in-character 對話）
TransformDialogue(dialogueText)

; NPC 內心想法（不發聲、不讓其他 NPC 聽到）
GenerateNPCThought(npcActor, promptHint)

; 清除所有進行中的對話
PurgeDialogue(deferToCurrentFinished)
```

### 3.3 對話中斷控制

`0750_embedded_actions.prompt` 描述了關鍵的行為：**對話先輸出，action 行在後**。這讓 TTS 可以先開始播放對話文字，同時 C++ 端解析 action 行。

### 3.4 說話對象設定

`skynet_MainController.psc:91-114`:
```papyrus
SetActorDialogueTarget(akActor, akTarget)
  → SetLookAt(akTarget)
  → SetLinkedRef(akActor, akTarget, keywordDialogueTarget)
  → RegisterPackage(akActor, "TalkToPlayer"/"TalkToNPC", ...)
  → EvaluatePackage()
```

### 3.5 Trigger 系統（事件→ 對話/旁白）

`WORKFLOW_TRIGGERS.md` 描述了 trigger YAML 系統，讓遊戲事件自動產生對話/旁白/思考：

觸發類型：
| Response Type | 效果 |
|---------------|------|
| `player_thought` | 玩家內心思考 |
| `player_dialogue` | 玩家說出對話 |
| `direct_narration` | 旁白，附近 NPC 會感知並反應 |
| `persistent_generic` | 背景事件，不觸發 NPC 對話 |
| `diary_entry` | 為 NPC 生成日記 |
| `dynamic_bio_update` | 更新 NPC 的 character bio |

可監聽的事件類型涵蓋整個遊戲：spell_cast, active_effect, hit, combat, death, activation, equip, sleep, book_read, quest_stage, location_change, container_changed, animation_event, mod_event, crime, dragon_soul, dialogue

### 3.6 MinAI Bridge（向後相容）

`skynet_MinAIBridge.psc` 提供與 MinAI 生態的相容層，監聽四個 ModEvent：
- `MinAI_SetContext` → `RegisterShortLivedEvent` (有時效的場景上下文)
- `MinAI_RegisterEvent` → `RegisterPersistentEvent` (持久事件)
- `MinAI_RequestResponse` → `DirectNarration` (請求 NPC 回應)
- `MinAI_RequestResponseDialogue` → `RegisterDialogueToListener` (指定說話者和聽者)

---

## 4. 設計亮點與取捨

### 4.1 世界狀態總結的設計選擇

| 設計 | 優點 | 代價 |
|------|------|------|
| C++ 直接讀記憶體，不走序列化 | 零延遲、最新狀態 | 強依賴 Address Library、版本耦合 |
| Inja 模板引擎（非 Jinja2） | 輕量、C++ 內嵌 | 語法受限（無 macro、無複雜 filter） |
| Character bio 用 submodule 拼裝 | 極度模組化、modder 友善 | 組合順序靠檔名數字，隱式依賴 |
| 時間用相對描述而非絕對數值 | LLM 友善 | 精度損失 |
| Furniture-based 行為推論 | 不用 hook 每個 animation | 粗糙、依賴家具命名慣例 |

### 4.2 Action 系統的設計選擇

| 設計 | 優點 | 代價 |
|------|------|------|
| 雙路徑（嵌入 vs 獨立 selector） | 靈活 | 兩套 prompt 需分別維護 |
| Category drill-down（兩段式選擇） | 省 token（cheap model 做第二步） | 增加延遲 |
| Eligibility 預熱 | 減少 LLM 等待 | 需持續計算 |
| YAML 定義 action + Papyrus 執行 | Modder 不需寫 C++ | 受限於 Papyrus 的能力邊界 |

### 4.3 對話系統的設計選擇

| 設計 | 優點 | 代價 |
|------|------|------|
| Character bio 驅動 identity | NPC 個性可熱更新 | Bio 品質決定對話品質 |
| 三個 render mode（full/thoughts/target） | 同一個 bio 服務多種場景 | 模板撰寫需注意條件分支 |
| 對話文字先出、action 後解析 | 降低感知延遲 | Parsing 耦合 |

---

## 5. 與其他 repos 的關係

- **MinAI** (`MinLL/MinAI`): SkyrimNet 透過 `skynet_MinAIBridge.psc` 提供向後相容層，監聽 MinAI 的 ModEvent 並轉送
- **Mantella** (`art-from-the-machine/Mantella`): 完全不同的架構（外部 Python 程序），SkyrimNet 在 README 中明確定位為 "no Python launcher, no WSL" 的替代方案
- **IntelEngine** (`galanx/IntelEngine-GamePlugin`): SkyrimNet 的社群 plugin，基於其 action API 建構的 NPC 自主行為層
