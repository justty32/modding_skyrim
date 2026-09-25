# 3. 對話改變相關原始碼

[返回入口](../skyrimNet-source-ref.md)

## 3. 對話改變相關原始碼

### 3.1 核心對話 Prompt

| 檔案 | 內容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/prompts/dialogue_response.prompt` | **對話回應主 prompt**（system: 你是 {name} + bio + target info；user: event history + final instructions） |
| `SKSE/Plugins/SkyrimNet/prompts/player_dialogue.prompt` | 玩家對話 prompt |
| `SKSE/Plugins/SkyrimNet/prompts/player_thoughts.prompt` | 玩家思考 prompt |
| `SKSE/Plugins/SkyrimNet/prompts/npc_thoughts.prompt` | NPC 思考 prompt |
| `SKSE/Plugins/SkyrimNet/prompts/native_action_selector.prompt` | **獨立 action selector**（輸入: NPC profile + dialogue history + eligible actions → 輸出: ACTION line） |
| `SKSE/Plugins/SkyrimNet/prompts/native_action_selector_drilldown.prompt` | Category drill-down（第二段 LLM call，cheap model） |

### 3.2 Papyrus API — 對話管理

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/SkyrimNetApi.psc:89-97` | `RegisterDialogue()` / `RegisterDialogueToListener()` — **注入對話到事件流** |
| `Source/Scripts/SkyrimNetApi.psc:99-111` | `PurgeDialogue()` — 清除所有進行中對話 |
| `Source/Scripts/SkyrimNetApi.psc:145-182` | `SendCustomPromptToLLM()` — 自訂 LLM prompt |
| `Source/Scripts/SkyrimNetApi.psc:184-208` | `DirectNarration()` — **Direct Narration**（強制 NPC 回應一個事實） |
| `Source/Scripts/SkyrimNetApi.psc:210-231` | `RegisterPersistentEvent()` — **持久事件**（注入 context 但不觸發對話） |
| `Source/Scripts/SkyrimNetApi.psc:234-248` | `TransformDialogue()` — 玩家對話轉換 |
| `Source/Scripts/SkyrimNetApi.psc:250-265` | `GenerateNPCThought()` — NPC 內心思考 |

### 3.3 Papyrus API — Event Schema 系統

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/SkyrimNetApi.psc:369-425` | `RegisterEventSchema()` / `ValidateEventData()` / `FormatEvent()` — **事件格式註冊**（含 isEphemeral, TTL, interrupt 支援） |

### 3.4 Trigger 系統

| 檔案 | 內容 |
|------|------|
| `docs/modding/WORKFLOW_TRIGGERS.md` | **Trigger 建立 workflow**（YAML 結構、事件類型參考、response type、audience、condition operators） |
| `docs/modding/WORKFLOW_TRIGGERS.md:42-57` | 事件類型完整列表（spell_cast, active_effect, combat, death, equip, quest_stage, location_change, mod_event, crime...） |

### 3.5 MinAI Bridge（向後相容層）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/skynet_MinAIBridge.psc:1-35` | `Maintenance()` — 檢測 MinAI.esp、註冊 MinAI ModEvent 監聽 |
| `Source/Scripts/skynet_MinAIBridge.psc:37-79` | `OnMinAI_SetContext()` → `RegisterShortLivedEvent()` |
| `Source/Scripts/skynet_MinAIBridge.psc:82-101` | `OnMinAI_RegisterEvent()` → `RegisterPersistentEvent()` |
| `Source/Scripts/skynet_MinAIBridge.psc:104-125` | `OnMinAI_RequestResponse()` → `DirectNarration()` |
| `Source/Scripts/skynet_MinAIBridge.psc:128-160` | `OnMinAI_RequestResponseDialogue()` → `RegisterDialogueToListener()` |

### 3.6 World Knowledge API

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/SkyrimNetApi.psc:802-828` | `AddWorldKnowledge()` — **共享世界知識**（含 Inja condition expression, alwaysInject vs semantic） |
