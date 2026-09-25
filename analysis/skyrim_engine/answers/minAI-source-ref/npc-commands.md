# 2. NPC 下令相關原始碼

[返回入口](../minAI-source-ref.md)

## 2. NPC 下令相關原始碼

### 2.1 Action Registry（CHIM 端）

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_AIFF.psc` | `RegisterAction()` — 向 CHIM 註冊 action（含 category, cooldown, minBackoff, maxBackoff, backoffWindow, addToAllNPCs, addToPlayer） |
| `Scripts/Source/minai_AIFF.psc` | `StoreAction()` — 儲存外部 mod 的 action（含 prompt, ttl, targetDescription, targetEnum, npcName） |
| `Scripts/Source/minai_AIFF.psc` | `ResetAllActionBackoffs()` — 重置所有 action backoff |

### 2.2 外部 Mod 的 Action API

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_MainQuestController.psc:411-418` | `OnRegisterAction()` — **接收外部 ModEvent 註冊 action**（ExtCmd+actionName prefix；存入 StoreAction） |
| `Scripts/Source/minai_MainQuestController.psc:435-442` | `OnRegisterActionNPC()` — 接收 per-NPC action 註冊 |
| `ModdersGuide.md:1-156` | **完整 Modder API 文件**（MinAI_RegisterEvent, MinAI_RequestResponse, MinAI_RequestResponseDialogue, MinAI_SetContext, MinAI_SetContextNPC, MinAI_RegisterAction, MinAI_RegisterActionNPC 的參數格式與用法） |

### 2.3 Action 控制用 Factions

| 檔案:行號 | 內容 |
|-----------|------|
| `ModdersGuide.md:4-10` | Faction 控制系統（`NoActionsFaction`, `NoSexActionsFaction`, `NoNSFWActionsFaction` — 部分名稱匹配即可，無需硬依賴 MinAI） |

### 2.4 跟隨系統

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_AIFF.psc:68-81` | `InitFollow()` — 載入 `FollowPlayerPackage` + `FollowingPlayerFaction` |
| `Scripts/Source/minai_AIFF.psc` | `CheckIfActorShouldStillFollow()` — cleanup 檢查 |

### 2.5 主要控制器 — 事件路由

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_MainQuestController.psc:62-157` | `Maintenance()` — 初始化所有 15+ 子模組、註冊 ModEvent 監聽、設定 keybinds、檢測安裝的 AI 框架（Mantella/AIFF） |
| `Scripts/Source/minai_MainQuestController.psc:160-165` | `RegisterAction()` — 轉送 action 到 Mantella 或 AIFF |
| `Scripts/Source/minai_MainQuestController.psc:168-184` | `RegisterEvent()` — 轉送事件到 Mantella/AIFF（自動 prefix "info_" 到 event type） |
| `Scripts/Source/minai_MainQuestController.psc:187-200` | `RequestLLMResponse()` — **請求 LLM 回應**（含 cooldown 檢查；冷卻期內降級為 RegisterEvent） |
| `Scripts/Source/minai_MainQuestController.psc:203-237` | `RequestLLMResponseFromActor()` — 請求特定 actor 回應（支援 "player"/"npc"/"both" responseTarget） |
| `Scripts/Source/minai_MainQuestController.psc:240-252` | `RequestLLMResponseNPC()` — NPC→NPC 對話請求（格式: `speaker@target@eventLine`） |

---

