# IntelEngine-GamePlugin — 原始碼出處索引

> 路徑根: `external/frameworks/IntelEngine-GamePlugin/`
> 注意: IntelEngine 是 SkyrimNet 社群 plugin，基於 SkyrimNet YAML action API + Papyrus 腳本。核心導航/目的地解析/stuck detection 等效能敏感邏輯在 C++ native DLL（原始碼不在此 repo）。

---

## 1. 世界狀態總結相關原始碼

### 1.1 Task History（NPC 任務記憶）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:374-417` | `SaveTaskToHistory()` — **任務完成後寫入滾動歷史**（taskType, target, result, msgContent, meetLocation → 10 條 FIFO；預渲染為 `Intel_TaskHistoryRendered` 供 SkyrimNet bio submodule 讀取） |

### 1.2 Fact Injection API（敘事注入）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:1487-1525` | `InjectFact()` — **注入敘事事實到 NPC bio**（10 條 FIFO cap；預渲染為 `Intel_FactsRendered`；同時註冊到 global registry 便於 Maintenance sweep） |
| `Source/Scripts/IntelEngine_Core.psc:1598-1635` | `CleanExpiredFacts()` / `CleanExpiredFactsGlobal()` — 事實清理 |

### 1.3 Gossip Injection API（流言傳播）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:1533-1596` | `InjectGossip()` — **雙向流言記錄**（接收者: heard from X；傳播者: told Y；各 5 條 FIFO cap；預渲染為 `Intel_GossipRendered`） |

### 1.4 Message Persistence API

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:423-443` | `StoreReceivedMessage()` — **儲存 NPC 收到的訊息**（sender name, msgContent, game time → StorageUtil） |

### 1.5 Meeting Outcome API

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:448-478` | `StoreMeetingOutcome()` / `ClearMeetingOutcome()` — **會議結果持久化**（outcome: success/player_late/npc_late/player_no_show/npc_late_player_no_show；dest, time；寫入 StorageUtil 供 bio prompt 使用） |

### 1.6 Narration & Event API（向 SkyrimNet 發送敘事）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:1460-1464` | `SendTaskNarration()` → `SkyrimNetApi.DirectNarration()` — **NPC 語音敘事** |
| `Source/Scripts/IntelEngine_Core.psc:1466-1470` | `SendPersistentMemory()` → `SkyrimNetApi.RegisterPersistentEvent()` — **持久記憶注入** |
| `Source/Scripts/IntelEngine_Core.psc:1473-1478` | `SendTransientEvent()` → `SkyrimNetApi.RegisterEvent()` — **暫時事件注入** |

### 1.7 Slot State Tracking（任務槽位狀態）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:144-165` | 狀態陣列宣告 — `SlotStates[]`, `SlotTaskTypes[]`, `SlotTargetNames[]`, `SlotDeadlines[]`, `SlotSpeeds[]` |
| `Source/Scripts/IntelEngine_Core.psc:582-608` | `AllocateSlot()` — **分配 slot**（Papyrus arrays + StorageUtil + C++ SlotTracker 三寫） |
| `Source/Scripts/IntelEngine_Core.psc:611-777` | `ClearSlot()` — **清理 slot**（~50 行程式碼清除所有 StorageUtil keys + packages + linked refs + faction；支援 `intelPackagesOnly` 模式） |
| `Source/Scripts/IntelEngine_Core.psc:849-917` | `SetSlotState()` / `SetSlotSpeed()` / `SetSlotDeadline()` / `MarkSlotProcessing()` — **三寫同步**（Papyrus + StorageUtil + C++ SlotTracker） |
| `Source/Scripts/IntelEngine_Core.psc:1356-1435` | `RecoverActiveTasks()` / `SyncSlotTrackerFromArrays()` — **遊戲載入時的任務恢復**（co-save path 或 StorageUtil legacy path） |

### 1.8 MCM Settings（StorageUtil-backed）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:1648-1651` | GlobalVariable/StorageUtil 雙軌設定存儲 |
| `Source/Scripts/IntelEngine_Core.psc:1680-1779` | Convenience accessors（`IsDebugMode()`, `IsStoryEngineEnabled()`, `GetMaxConcurrentTasks()`, `GetDefaultWaitHours()`, unified setters for MCM+Dashboard） |

---

## 2. NPC 下令相關原始碼

### 2.1 SkyrimNet YAML Action 定義

| 檔案 | 内容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/config/actions/cat_travel.yaml` | Travel category |
| `SKSE/Plugins/SkyrimNet/config/actions/cat_scheduling.yaml` | Scheduling category |
| `SKSE/Plugins/SkyrimNet/config/actions/cat_communication.yaml` | Communication category |
| `SKSE/Plugins/SkyrimNet/config/actions/intel_travel.yaml` | `GoToLocation` action |
| `SKSE/Plugins/SkyrimNet/config/actions/intel_changespeed.yaml` | `ChangeTaskSpeed` action |
| `SKSE/Plugins/SkyrimNet/config/actions/intel_canceltask.yaml` | `CancelCurrentTask` action |
| `SKSE/Plugins/SkyrimNet/config/actions/intel_schedulemeeting.yaml` | `ScheduleMeeting` action（時間條件: "at dawn", "in 3 hours"） |
| `SKSE/Plugins/SkyrimNet/config/actions/intel_schedulefetch.yaml` | `ScheduleFetch` action |
| `SKSE/Plugins/SkyrimNet/config/actions/intel_scheduledelivery.yaml` | `ScheduleDelivery` action（可選 meeting invite） |
| `SKSE/Plugins/SkyrimNet/config/actions/intel_fetchnpc.yaml` | `FetchNPC` action |
| `SKSE/Plugins/SkyrimNet/config/actions/intel_escorttarget.yaml` | `EscortTarget` action |
| `SKSE/Plugins/SkyrimNet/config/actions/intel_delivermessage.yaml` | `DeliverMessage` action |
| `SKSE/Plugins/SkyrimNet/config/actions/intel_searchforactor.yaml` | `SearchForActor` action |
| `SKSE/Plugins/SkyrimNet/config/actions/intel_report_player_conduct.yaml` | `ReportPlayerConduct` action |

### 2.2 Task Control（取消/變速）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:783-805` | `CancelCurrentTask()` — **取消 NPC 當前任務**（被 player linger proximity 阻擋；寫入 "cancelled" result） |
| `Source/Scripts/IntelEngine_Core.psc:807-839` | `ChangeTaskSpeed()` — **變更移動速度**（0=walk, 1=jog, 2=run；swap travel package + EvaluatePackage） |

### 2.3 時間排程系統（Schedule）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Schedule.psc:1-59` | Constants — `HOUR_DAWN=5`, `HOUR_SUNRISE=6`, `HOUR_SUNSET=19` 等；`DEPARTURE_BUFFER_HOURS=2.0` |
| `Source/Scripts/IntelEngine_Schedule.psc:121-187` | `ScheduleMeeting()` — **排程會議**（時間解析 → 距離基礎 departure buffer → departure hour cap → 通知玩家；取消既有 active meeting） |
| `Source/Scripts/IntelEngine_Schedule.psc:193-220` | `ScheduleFetch()` — 排程找人 |
| `Source/Scripts/IntelEngine_Schedule.psc:222-259` | `ScheduleDelivery()` — 排程傳話（可選 meeting location + time → 收件人也會被排程前往） |
| `Source/Scripts/IntelEngine_Schedule.psc:272-333` | `PrepareScheduleSlot()` — **共享排程腳手架**（時間解析、per-action confirmation prompt、override existing、allocate slot、persist 所有欄位到 StorageUtil） |
| `Source/Scripts/IntelEngine_Schedule.psc:514-539` | `OnUpdateGameTime()` / `OnUpdate()` — 雙定時器（game-time + real-time fallback） |
| `Source/Scripts/IntelEngine_Schedule.psc:541-627` | `ExecuteScheduledTask()` — **執行排程任務**（讀取陣列 → 清除既有任務 → 標記 dispatched → travel/fetch/deliver dispatch） |
| `Source/Scripts/IntelEngine_Schedule.psc:721-738` | `CheckAndDispatchPendingTasks()` — 檢查並 dispatch 到期任務 |
| `Source/Scripts/IntelEngine_Schedule.psc:740-787` | `RegisterForNextDispatch()` — **智能排程間隔**（計算最快將到期的任務；< 1 game hour → real-time 15s poll；>= 1 game hour → game-time timer） |

### 2.4 實體導航系統（Travel）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Travel.psc:64-77` | `EnsureMonitoringAlive()` — 監控 heartbeat（Schedule 的 game-time loop 呼叫，防 Papyrus VM stack dump 殺掉 update callback） |
| `Source/Scripts/IntelEngine_Travel.psc:79-97` | `RestartMonitoring()` — 遊戲載入後重新啟動監控 |
| `Source/Scripts/IntelEngine_Travel.psc:99-146` | `RecoverTravelPackage()` — 載入後恢復 travel package（linked ref + package override + stuck tracking） |
| `Source/Scripts/IntelEngine_Travel.psc:152-293` | `GoToLocation()` — **主要 API：送 NPC 去目的地**（validate → duplicate guard → confirmation prompt → destination resolve → slot allocate → package apply → stuck tracking → off-screen tracking → proximity monitor arm） |
| `Source/Scripts/IntelEngine_Travel.psc:301-312` | `ResolveDestination()` → C++ `ResolveAnyDestination()` — 目的地解析（named/semantic/fuzzy） |
| `Source/Scripts/IntelEngine_Travel.psc:318-341` | `OnUpdate()` — 監控循環（先註冊下次 update 再處理；防 crash 中斷循環） |
| `Source/Scripts/IntelEngine_Travel.psc:343-411` | `CheckTravelSlot()` — **單一 slot 的狀態檢查**（超時檢查 → 出發檢查 → 到場檢查 → 等待檢查） |
| `Source/Scripts/IntelEngine_Travel.psc:413-504` | `CheckForArrival()` — **到場偵測**（3D loaded: distance check + door teleport + floor Z verification；off-screen: same-cell interior check → HandleOffScreenTravel） |
| `Source/Scripts/IntelEngine_Travel.psc:527-551` | `OnProximityArrived()` — **C++ ProximityMonitor 150ms callback**（取代 3 秒 Papyrus poll） |
| `Source/Scripts/IntelEngine_Travel.psc:553-695` | `OnArrival()` — **到場處理**（assassination 分支、meeting 分支、regular travel 分支；sandbox 套用、deadline 計算、door redirection、player proximity 檢查） |
| `Source/Scripts/IntelEngine_Travel.psc:697-823` | `CheckWaiting()` — **等待階段**（linger phase: ProcessLingerProximity → CompleteMeeting；travel linger phase；player proximity → OnPlayerArrived；smart approach；deadline → OnWaitTimeout） |
| `Source/Scripts/IntelEngine_Travel.psc:825-921` | `OnPlayerArrived()` — **玩家到達處理**（會議模式: 精細的 lateness detection for both parties；五段 outcome → narration；StartMeetingLinger。普通旅行: 等待時間 narration + StartTravelLinger/StartStayAtDestLinger） |
| `Source/Scripts/IntelEngine_Travel.psc:923-976` | `OnWaitTimeout()` — **等待超時**（會議: 辨別 NPC late/timeout/player_no_show 三種情況；普通: NPC 離開通知） |

### 2.5 卡點恢復系統（Stuck Detection & Recovery）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Travel.psc:982-1011` | `CheckIfStuck()` — **卡點偵測 dispatcher**（跳過 dialogue/combat 中的 NPC；C++ CheckStuckStatus；status 0=正常, 1=soft recovery, 3=escalate） |
| `Source/Scripts/IntelEngine_Travel.psc:1013-1024` | `HandleSoftStuckRecovery()` — 軟卡點恢復（nudge + re-pathfind；第一次觸發時 narration） |
| `Source/Scripts/IntelEngine_Travel.psc:1026-1106` | `HandleLeapfrogRecovery()` — **漸進式卡點恢復**（Layer B: waypoint nav；Layer C: multi-angle leapfrog 200→500→1000→2000 單位，±30° 旋轉角度） |
| `Source/Scripts/IntelEngine_Core.psc:1238-1259` | `SoftStuckRecovery()` — 共享的軟卡點恢復（nudge + travel package + PathToReference） |
| `Source/Scripts/IntelEngine_Core.psc:1835-1877` | `TryWaypointNavigation()` — 中途地點導航（找最近的 BGSLocation marker → redirect travel；重複卡住 → teleport to waypoint） |
| `Source/Scripts/IntelEngine_Core.psc:1879-1899` | `CheckWaypointArrival()` — 檢查是否到達中途點 |

### 2.6 會議系統（Meeting-specific Logic）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Travel.psc:1116-1173` | Meeting departure detection + failure handling（off-screen teleport / on-screen narrate failure） |
| `Source/Scripts/IntelEngine_Travel.psc:1184-1262` | Smart approach（NPC 走向接近目的地的玩家，stuck recovery） |
| `Source/Scripts/IntelEngine_Travel.psc:1342-1367` | `StartMeetingLinger()` — 會議逗留開始（Phase 1: walk toward player；Phase 2: sandbox at 200 units） |
| `Source/Scripts/IntelEngine_Travel.psc:1369-1385` | `CompleteMeeting()` — 會議結束（narration + slot cleanup + follower restore） |

### 2.7 逗留系統（Linger System）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:925-994` | `ShouldReleaseLinger()` + `ReleaseLinger()` — **共享逗留釋放邏輯**（distance check: > LINGER_RELEASE_DISTANCE 或跨 cell；sandbox-only AI NPC 的 walk-home fallback） |
| `Source/Scripts/IntelEngine_Travel.psc:1290-1349` | `ProcessLingerProximity()` — 共享的 approach/sandbox/release 狀態機 |
| `Source/Scripts/IntelEngine_Travel.psc:1391-1449` | `StartTravelLinger()` / `StartStayAtDestLinger()` / `CompleteTravelLinger()` / `IsStayAtDestination()` — 不同類型的逗留 |

### 2.8 Package & Linked Ref 管理

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:1033-1064` | `DismissFollowerForTask()` — **任務前清除所有 package override**（含 SkyrimNet follow/TalkToPlayer；記錄 wasFollower 以便恢復） |
| `Source/Scripts/IntelEngine_Core.psc:1261-1292` | `RemoveAllPackages()` / `RemoveIntelPackages()` — 選擇性清除 package overrides |
| `Source/Scripts/IntelEngine_Core.psc:1295-1308` | `ClearLinkedRefs()` — 清除所有 linked ref keywords |

### 2.9 Task Confirmation（MCM 確認提示）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:1066-1147` | `ShowTaskConfirmation()` / `ShowTaskConfirmationForAction()` — **Per-action 確認提示**（mode: 0=disabled, 1=followers only, 2=everyone；per-action follower skip toggle） |

### 2.10 Off-Screen Travel Tracking

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:1167-1179` | `InitOffScreenTracking()` — **離屏移動估算**（`CalculateDeadlineFromDistance` → 預估到達時間 → C++ tracker） |
| `Source/Scripts/IntelEngine_Core.psc:1223-1236` | `HandleOffScreenTravel()` — 檢查離屏 NPC 是否該傳送到達 |

### 2.11 Navigation Helpers

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:1160-1165` | `InitializeDepartureTracking()` — 出發偵測（C++ DepartureDetector） |
| `Source/Scripts/IntelEngine_Core.psc:1331-1349` | `CheckDepartureProgress()` — **出發進度檢查**（status: 0=too_early, 1=departed, 2=soft_recovery, 3=escalate） |
| `Source/Scripts/IntelEngine_Core.psc:1310-1318` | `TeleportBehindPlayer()` — NPC 傳送到玩家背後（C++ `GetOffsetBehind`） |
| `Source/Scripts/IntelEngine_Core.psc:1181-1221` | `UnlockHomeForTask()` / `EnsureBuildingAccess()` — **反 trespass 系統**（unlock NPC 的家門讓 agent 可進入） |

---

## 3. 對話改變相關原始碼

### 3.1 敘事旁白（Narration）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:1460-1464` | `SendTaskNarration()` → `SkyrimNetApi.DirectNarration(msgText, akActor, akTarget)` |
| `Source/Scripts/IntelEngine_Core.psc:1637-1640` | `NotifyPlayer()` → `Debug.Notification()` |

### 3.2 Story Engine（Dungeon Master — 自主行為）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_StoryEngine.psc:1-19` | Story types 定義 — 9 種（seek_player, informant, npc_interaction, npc_gossip, road_encounter, ambush, stalker, message, quest） |
| `Source/Scripts/IntelEngine_StoryEngine.psc:29-44` | Dispatch state + constants（ENCOUNTER_PROXIMITY, SNEAK_APPROACH_DISTANCE, AMBUSH_CONFRONT_DISTANCE 等） |
| `Source/Scripts/IntelEngine_StoryEngine.psc:45-100` | MCM 設定（MaxTravelDays, LongAbsenceDays, DangerZonePolicy, PlayerHomePolicy, per-type toggles, per-type hold restriction policies, per-action confirmation, per-action follower skip） |

### 3.3 Faction Politics Engine

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Politics.psc` | Faction 政治系統（9 faction, 6 遊戲小時政治事件、faction wars、player standing） |
| `SKSE/Plugins/SkyrimNet/config/plugins/IntelEngine/factions.sample.yaml` | Faction 設定 sample |
| `SKSE/Plugins/SkyrimNet/config/plugins/IntelEngine/manifest.yaml` | Plugin manifest |

### 3.4 Battle Engine

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Battle.psc` | 戰鬥系統（ambush attack sequence、faction war battles、5 waves, 22 per side） |

### 3.5 NPC Tasks（多步驟任務）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_NPCTasks.psc` | `FetchNPC()`, `DeliverMessage()`, `EscortTarget()`, `SearchForActor()` — **多步驟 NPC 任務**（travel → find target → interact → return） |

### 3.6 Dashboard State & Events

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:1918-2029` | `RegisterDashboardEvents()` + event handlers — **PrismaUI Dashboard 整合**（Dashboard opened/refresh/cancel task/cancel quest/cancel schedule/toggle story/settings/remove packages/dispatch story/social/politics/execute action/auto bio update） |
| `Source/Scripts/IntelEngine_Core.psc:2029+` | Dashboard state push methods |

### 3.7 MCM 介面

| 檔案 | 內容 |
|------|------|
| `Source/Scripts/IntelEngine_MCM.psc` | MCM 設定頁面 |
| `Interface/MCMHelper/IntelEngine/config.json` | MCM Helper 設定 |

### 3.8 Plugin 設定

| 檔案 | 內容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/config/plugins/IntelEngine/manifest.yaml` | SkyrimNet plugin manifest |
| `SKSE/Plugins/SkyrimNet/config/plugins/IntelEngine/settings.sample.yaml` | Settings sample |
| `SKSE/Plugins/SkyrimNet/config/plugins/IntelEngine/factions.sample.yaml` | Faction 設定 sample |
