# 架構總覽

[返回入口](../skyrimNet-gameplugin-analysis.md)

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

