# SkyrimNet-GamePlugin — 原始碼出處索引

> 路徑根: `external/frameworks/SkyrimNet-GamePlugin/`
> 注意: C++ native DLL 原始碼不在此 repo，以下指向 repo 內的 Papyrus、prompt 模板、YAML 定義

---

## 1. 世界狀態總結相關原始碼

### 1.1 Prompt 模板引擎 — Scene Context

| 檔案 | 內容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/prompts/components/context/scene_context_full.prompt` | 場景上下文五大區塊結構（Scene Info / Weather / Nearby People / Recent Events / Scene Summary） |
| `SKSE/Plugins/SkyrimNet/prompts/components/context/scene_context.prompt` | 精簡版 scene context |
| `SKSE/Plugins/SkyrimNet/prompts/components/context/scene_context_target_selection.prompt` | 目標選擇專用 context |
| `SKSE/Plugins/SkyrimNet/prompts/components/context/component_npc_state_summary.prompt` | **核心：NPC 行為狀態推論**（~25 種家具關鍵字比對: bed→睡覺, forge→打鐵, shrine→祈禱...） |
| `SKSE/Plugins/SkyrimNet/prompts/components/context/component_recent_events.prompt` | 近期事件摘要 |

### 1.2 Prompt 模板引擎 — 事件歷史

| 檔案 | 內容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/prompts/components/event_history.prompt` | **完整事件歷史**（含時間差標記: "[A while ago]", "[Yesterday]"；時間間隙: "Some time passes...", "The next day..."） |
| `SKSE/Plugins/SkyrimNet/prompts/components/event_history_compact.prompt` | 精簡版（action selector 用） |
| `SKSE/Plugins/SkyrimNet/prompts/components/event_history_verbose.prompt` | 詳細版 |

### 1.3 Prompt 模板引擎 — Character Bio Submodules

| 檔案 | 內容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/0010_header.prompt` | 基本身份 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/0050_physical_activity.prompt` | 身體活動狀態 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/0100_summary.prompt` | 手寫 summary |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/0130_world_knowledge.prompt` | World knowledge 注入 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/0200_background.prompt` | 背景故事 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/0300_personality.prompt` | 性格 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/0310_interject_summary.prompt` | 插話摘要 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/0400_appearance.prompt` | 外觀 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/0410_equipment.prompt` | 裝備 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/0500_skills.prompt` | 技能 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/0600_relationships.prompt` | 關係 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/0610_party_quests.prompt` | 隊伍任務 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/0700_occupation.prompt` | 職業 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/7000_memories_and_progression.prompt` | 記憶與進度 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/7100_memories.prompt` | 記憶（vector recall） |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/character_bio/9990_speech_style.prompt` | 說話風格 |

### 1.4 Prompt 模板引擎 — System Head & Guidelines

| 檔案 | 內容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/prompts/submodules/system_head/0010_instructions.prompt` | 系統指令 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/system_head/0020_format_rules.prompt` | 格式規則 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/system_head/0100_actor_bios.prompt` | Actor bio 聚合 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/system_head/0150_telepathy_awareness.prompt` | Telepathy 感知 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/system_head/0200_scene_context.prompt` | 場景 context 聚合 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/system_head/0250_omnisight.prompt` | OmniSight vision |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/system_head/0400_speech_style_bio.prompt` | 說話風格 bio |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/guidelines/0500_roleplay_guidelines.prompt` | Roleplay 指南 |

### 1.5 Prompt 模板引擎 — User Final Instructions

| 檔案 | 內容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/prompts/submodules/user_final_instructions/0150_environmental_awareness.prompt` | 環境感知指令 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/user_final_instructions/0160_telepathy_reception.prompt` | Telepathy 接收 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/user_final_instructions/0200_combat_status.prompt` | 戰鬥狀態指令 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/user_final_instructions/0500_response_format.prompt` | 回應格式 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/user_final_instructions/0650_audio_tags.prompt` | 音訊標籤 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/user_final_instructions/0700_extra_instructions.prompt` | 額外指令 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/user_final_instructions/0750_embedded_actions.prompt` | **嵌入 actions 格式**（對話文字先出、ACTION 行後解析） |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/user_final_instructions/0800_direct_narration.prompt` | Direct narration 格式 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/user_final_instructions/8000_recent_state_changes.prompt` | 近期狀態變化 |

### 1.6 Decorator 測試（展示所有可用 decorator 的實例）

| 檔案 | 內容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/prompts/submodules/test_decorators/0100_actor_decorators.prompt` | Actor decorators 測試 |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/test_decorators/0200_combat_decorators.prompt` | Combat decorators |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/test_decorators/0300_equipment_decorators.prompt` | Equipment decorators |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/test_decorators/0350_item_decorators.prompt` | Item decorators |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/test_decorators/0400_faction_relationship_decorators.prompt` | Faction/Relationship decorators |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/test_decorators/0500_magic_decorators.prompt` | Magic decorators |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/test_decorators/0600_quest_gamesystem_decorators.prompt` | Quest decorators |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/test_decorators/0700_scene_world_decorators.prompt` | Scene/World decorators |
| `SKSE/Plugins/SkyrimNet/prompts/submodules/test_decorators/0800_omnisight_state_decorators.prompt` | OmniSight decorators |

### 1.7 API 文件

| 檔案 | 內容 |
|------|------|
| `docs/modding/prompts-and-decorators.md` | **Decorator 使用指南**、`decnpc()` 回傳結構、Inja 模板語法、render mode 說明 |
| `docs/modding/WORKFLOW_PROMPTS.md` | Prompt 建立 workflow（含 decorator category 列表、context variables） |
| `docs/modding/prompt-file-syntax.md` | Prompt 檔案語法 |

---

## 2. NPC 下令相關原始碼

### 2.1 Papyrus API — Action 管理

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/SkyrimNetApi.psc:13-15` | `RegisterDecorator()` — 註冊自訂 decorator |
| `Source/Scripts/SkyrimNetApi.psc:21-43` | `RegisterAction()` / `RegisterSubCategory()` / `RegisterTag()` — **Modder action API** |
| `Source/Scripts/SkyrimNetApi.psc:47-56` | `IsActionRegistered()` / `UnregisterAction()` / `ExecuteAction()` |
| `Source/Scripts/SkyrimNetApi.psc:58-62` | `SetActionCooldown()` / `GetRemainingCooldown()` — 冷卻管理 |

### 2.2 Papyrus API — Package 管理

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/SkyrimNetApi.psc:117-144` | `RegisterPackage()` / `UnregisterPackage()` / `ClearAllPackages()` / `ReinforcePackages()` |

### 2.3 Action 定義格式（YAML）

| 檔案 | 內容 |
|------|------|
| `docs/modding/WORKFLOW_ACTIONS.md` | **Action 建立完整 workflow**（YAML 結構、eligibility rule 邏輯、參數 mapping、validation） |
| `docs/modding/WORKFLOW_MOD_INTEGRATION.md` | Mod 整合指南 |

### 2.4 內建 Action 實作（Papyrus 端）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/SkyrimNetInternal.psc:100-118` | `OpenTrade_IsEligible()` + `OpenTrade_Execute()` |
| `Source/Scripts/SkyrimNetInternal.psc:130-143` | `Companion_IsEligible()` + `CompanionInventory()` |
| `Source/Scripts/SkyrimNetInternal.psc:145-165` | `CompanionFollow_IsEligible()` + `CompanionFollow()` |
| `Source/Scripts/SkyrimNetInternal.psc:166-185` | `CompanionWait_IsEligible()` + `CompanionWait()` |
| `Source/Scripts/SkyrimNetInternal.psc:207-261` | `StartFollow_IsEligible()` → `StopFollow_IsEligible()` — 跟隨系統 |
| `Source/Scripts/SkyrimNetInternal.psc:291-316` | `RentRoom_IsEligible()` + `RentRoom_Execute()` |
| `Source/Scripts/SkyrimNetInternal.psc:357-382` | `AlwaysEligible()` / `Follower_IsEligible()` — Tag-based eligibility |
| `Source/Scripts/SkyrimNetInternal.psc:24-38` | `GetDiaryScopeMessage()` — Diary scope 查詢 |

### 2.5 Papyrus — NPC 對話/跟隨對象設定

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/skynet_MainController.psc:91-114` | `SetActorDialogueTarget()` — 設定 NPC 看向誰、套用 `TalkToPlayer`/`TalkToNPC` package |
| `Source/Scripts/skynet_MainController.psc:121-131` | `SetActorFollowing()` / `ClearActorFollowing()` — 跟隨系統 |

### 2.6 GameMaster 自主行為 Prompt

| 檔案 | 內容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/prompts/gamemaster_action_selector.prompt` | **GameMaster action selector**（StartConversation/ContinueConversation, Scene Plan beats, NPC→NPC 優先） |
| `SKSE/Plugins/SkyrimNet/prompts/gamemaster_scene_planner.prompt` | GameMaster 場景規劃 |

---

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
