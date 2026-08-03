# SkyrimNet-GamePlugin 分析：世界狀態、NPC 指令、對話控制

> 來源: `external/frameworks/SkyrimNet-GamePlugin/` (clone from https://github.com/MinLL/SkyrimNet-GamePlugin)
> 分析日期: 2026-07-30
> 關注範圍: 世界狀態總結機制、NPC 下令、對話改變（排除 TTS/STT/AI 截圖等）

---

## 架構總覽

SkyrimNet 是一個 **單一 SKSE native DLL**（C++）＋ Papyrus 腳本層的架構。核心 C++ DLL 不含在本 repo（本 repo 只有 Papyrus 原始碼、prompt 模板、UI 資源），但可以從 Papyrus API 和 prompt 模板反向推導出完整設計。

關鍵分層：
```
遊戲引擎記憶體 (C++ 直接讀取)
  └─→ Native DLL (C++): 讀 gamestate、跑 HTTP/WS、embedding、TTS
        ├─→ Prompt Engine (Inja 模板引擎): 將 gamestate 渲染為 LLM prompt
        │     ├─→ Decorators: ~100+ 個 C++/Papyrus 函數，讓模板能查詢遊戲狀態
        │     └─→ Submodules: 模組化 prompt 片段，數字排序控制組合順序
        ├─→ Action System: LLM 選擇 action → Papyrus function 執行
        │     ├─→ YAML-defined actions (modder 定義)
        │     ├─→ Papyrus-registered actions (runtime 註冊)
        │     └─→ Native C++ actions (其他 SKSE plugin 注入)
        ├─→ Event System: 遊戲事件 → trigger YAML → response (narration/thought/dialogue)
        └─→ Dialogue Pipeline: 玩家輸入 → prompt 渲染 → LLM → 解析 response
              ├─→ 對話文字 → TTS 生成
              └─→ 嵌入動作 (embed_actions_in_dialogue) → 執行
```

---

## 1. 世界狀態總結 (World State Summarization)

### 1.1 核心機制：Decorator 函數 + Inja 模板

世界狀態是透過 **decorator functions** 從記憶體即時讀取，然後在 prompt 渲染時注入。**不經過序列化到檔案的中間層**，而是 C++ 端直接讀遊戲記憶體後轉成 JSON 給模板引擎。

### 1.2 關鍵 Decorator: `decnpc(actorUUID)`

`decnpc()` 是單一最核心的 decorator，對一個 actor 回傳完整 state blob（`Source/Scripts/SkyrimNetApi.psc` 無此函數定義證明它是 pure C++ native decorator）：

從 `WORKFLOW_PROMPTS.md:97-135` 可推導其回傳結構：
```
name, race, gender, class, level
health, magicka, stamina
oneHanded, destruction, speech, ... (全技能 0-100)
summary, background, personality, speechStyle  (手寫/生成的 character bio)
subjectivePronoun, objectivePronoun, possessivePronoun, reflexivePronoun
relationshipRank (-4 到 4)
isVirtual, isVirtualPrivate, isDead, isFemale
universalTranslatorSpeechPattern
```

### 1.3 場景上下文 (Scene Context) 的結構

`SKSE/Plugins/SkyrimNet/prompts/components/context/scene_context_full.prompt` 定義場景上下文的五大區塊：

1. **Scene Information** — 當前場景摘要（由 GameMaster/LLM 生成）
2. **Weather** — 天氣描述
3. **Nearby People** — 附近 NPC 清單（距離、在做什麼、跟隨狀態）
4. **Recent Events** — 近期事件（過濾掉 spell/hit/combat 等高頻事件）
5. **Scene Summary / NPC State Summary** — 每個 NPC 的行為狀態

### 1.4 NPC 行為狀態偵測 (`component_npc_state_summary.prompt`)

這是最有趣的檔案之一。它對附近每個 NPC 做 **furniture-based 行為推論**：

```
"bed" / "bedroll" → "NPC 正在睡覺"
"table" / "desk" → "NPC 正坐在桌旁"
"alchemy" / "mortar" → "NPC 正在調製藥水"
"forge" / "anvil" → "NPC 正在打鐵"
"shrine" / "altar" → "NPC 正在祈禱"
"chair" / "stool" → "NPC 正坐著"
"lute" / "drum" / "flute" → "NPC 正在演奏"
...等 ~25 種家具關鍵字比對
```

也處理：跟隨玩家、昏迷狀態、召喚生物、復活不死生物、敵對關係。

### 1.5 事件歷史 (Event History) — 時間感知

`event_history.prompt` 和 `event_history_compact.prompt` 實作了一套精細的**相對時間標記系統**：

```
< 30 分鐘前 → "[A while ago]"
< 1 小時前 → "[About an hour ago]"
< 2 小時前 → "[A few hours ago]"
... 
> 1 週 → "[Over a week ago]"
```

而且事件之間有時間間隙標記（"Some time passes...", "The next day..."），讓 LLM 理解**時間流逝**。

### 1.6 Prompt 組合機制

Character bio 由 ~20 個 submodule 檔案在 `submodules/character_bio/` 下以數字排序組合：

```
0010_header.prompt        — 基本身份
0050_physical_activity.prompt
0100_summary.prompt       — 手寫 summary
0130_world_knowledge.prompt
0200_background.prompt    — 背景故事
0300_personality.prompt   — 性格
0310_interject_summary.prompt
0320_aspirations.prompt
0400_appearance.prompt    — 外觀
0410_equipment.prompt     — 裝備
0500_skills.prompt        — 技能
0600_relationships.prompt — 關係
0610_party_quests.prompt
0700_occupation.prompt    — 職業
7000_memories_and_progression.prompt
7100_memories.prompt      — 記憶（vector recall）
9990_speech_style.prompt  — 說話風格
```

### 1.7 World Knowledge (共享世界知識)

從 `SkyrimNetApi.psc:802-828` 的 `AddWorldKnowledge()`：
- 每個知識條目有 **Inja 條件表達式** 控制哪些 NPC 能看到
- `alwaysInject=true` → 無條件注入 prompt；`false` → 僅語義搜尋時浮現
- 條件例：`is_in_faction(actorUUID, "CompanionsFaction")` / `get_quest_stage("MQ104") >= 13`

### 1.8 Render Mode（視角控制）

同一個 bio submodule 可以根據 `render_mode` 輸出不同版本（`WORKFLOW_PROMPTS.md:416-436`）：

| Render Mode | 視角 | 顯示內容 |
|-------------|------|---------|
| `transform`, `full`, `thoughts` | 第一人稱 | 內心狀態、感受 |
| `target` | 第三人稱 | 僅可觀察的資訊 |
| `short_inline`, `interject_inline` | 精簡 | 最少相關資訊 |

---

## 2. NPC 下令機制 (NPC Command/Control)

### 2.1 三層 Action 系統

Action 是對 NPC 下令的核心機制，有三種註冊方式：

#### Layer 1: YAML-defined actions（最常見）
YAML 檔案定義 action → C++ 端解析 → 透過 `executionFunctionName` 呼叫 Papyrus 腳本的函數。

YAML 結構 (`WORKFLOW_ACTIONS.md:236-268`):
```yaml
name: "ActionName"
description: "描述給 LLM 看，讓 LLM 判斷何時使用"
questEditorId: "QuestEditorID"
scriptName: "ScriptName"
executionFunctionName: "FunctionName"
parameterMapping:
  - type: "speaker"       # 自動填為執行 action 的 NPC
  - type: "dynamic"       # LLM 選擇參數值
    name: "param_name"
    description: "描述給 LLM"
  - type: "static"        # 固定值
    value: "fixed_value"
eligibilityRules:
  - conditions:
      - decoratorName: "is_in_faction"
        arguments: ["currentActor", "FactionEditorID"]
        comparisonOperator: "=="
        expectedValue: true
    logicalOperator: "AND"
    required: true
```

參數映射支援的型別：
| Papyrus Type | Mapping |
|--------------|---------|
| Actor (self) | `speaker` |
| Actor (target) | `dynamic` (LLM 選) |
| Int/Float (fixed) | `static` |
| Int/Float (variable) | `dynamic` |
| Bool/String | `static` 或 `dynamic` |

#### Layer 2: Papyrus-registered actions
透過 `SkyrimNetApi.RegisterAction()` 在 runtime 註冊（`SkyrimNetApi.psc:27-31`）：
```papyrus
SkyrimNetApi.RegisterAction(
    actionName, description,
    eligibilityScriptName, eligibilityFunctionName,
    executionScriptName, executionFunctionName,
    triggeringEventTypesCsv, categoryStr,
    defaultPriority, parameterSchemaJson, customCategory, tags)
```

#### Layer 3: Native C++ actions
其他 SKSE plugin 可以注入 C++ 實作的 actions。

### 2.2 Action 的兩個執行路徑

#### Path A: 嵌入對話（`embed_actions_in_dialogue`）
`0750_embedded_actions.prompt` 讓 LLM 在生成對話的同時輸出 action：
```
NPC 的對話文字
ACTION: ActionName PARAMS: {"param": "value"}
```
C++ 端解析 response，先送對話去 TTS，同時解析並執行 action。

#### Path B: 獨立 Action Selector
`native_action_selector.prompt` 是一個**獨立的 LLM 呼叫**，專門判斷對話後應該執行哪個 action。輸入包含：
- NPC 的完整 character profile
- 對話歷史（compact event history）
- 最近一次交換（玩家說了什麼、NPC 回了什麼）
- 附近 actors 清單（含距離、狀態）
- **Eligible Actions 清單**（已預先過濾/filtered by eligibility + cooldown）

### 2.3 Action 分類系統 (Categories → Drill-down)

Actions 可以分組到 categories 中。當 LLM 選擇一個 category（而非具體 action）時，系統會觸發 **第二次 LLM 呼叫** (`native_action_selector_drilldown.prompt`) 用更便宜的 model 來選具體 action。Category 選擇時必須帶 `intent`：
```json
{"ACTION": "Economy", "PARAMS": {"intent": "sell a health potion to the player for 450 gold"}}
```

### 2.4 Eligibility 預熱 (Pre-warming)

在玩家語音輸入期間，系統**預先計算**每個附近 NPC 對每個 action 的 eligibility，所以當玩家說完話時，LLM 已經知道哪些 actions 是合法選項。

### 2.5 GameMaster 自主行為

`gamemaster_action_selector.prompt` 控制 NPC **在沒有玩家輸入時的自主行為**：

- **StartConversation**: 發起 NPC-to-NPC 對話（優先），或 NPC-to-Player（僅在有直接原因時）
- **ContinueConversation**: 維持進行中的對話
- **Scene Plan**: 預先規劃的場景節奏（scene beats），每個 beat 有 type/description/characters/purpose
- **Continuous Mode**: GM 持續導演場景，不能選 None

### 2.6 Papyrus Package 管理

`SkyrimNetApi.psc:117-145` 提供了 package 管理 API：
```papyrus
RegisterPackage(actor, packageName, priority, flags, isPersistent)
UnregisterPackage(actor, packageName)
ClearAllPackages(actor)
ReinforcePackages(actor)  ; 重新套用所有 SkyrimNet packages
```

這用於讓 NPC 看向說話對象（`TalkToPlayer`/`TalkToNPC` packages）。

### 2.7 Mod 社群 action 生態

README 提到兩個主要社群 plugin：
- **SeverActions**: 71 actions (combat, gold/debt, crafting, crime/arrest system)
- **IntelEngine**: NPC 自主行動、dynamic quest creation、faction politics（這是第四個要分析的 repo）

---

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
