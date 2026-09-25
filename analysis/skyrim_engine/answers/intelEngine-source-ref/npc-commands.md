# 2. NPC 下令相關原始碼

[返回入口](../intelEngine-source-ref.md)

## 2. NPC 下令相關原始碼

### 2.1 SkyrimNet YAML Action 定義

2.1 SkyrimNet YAML Action 定義的記錄已抽到 [npc-commands-yaml-actions.json](npc-commands-yaml-actions.json)（14 列）。

檔案：保留原表「檔案」欄內容。

内容：保留原表「内容」欄內容。

統計：共 14 筆記錄、2 欄。

### 2.2 Task Control（取消/變速）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:783-805` | `CancelCurrentTask()` — **取消 NPC 當前任務**（被 player linger proximity 阻擋；寫入 "cancelled" result） |
| `Source/Scripts/IntelEngine_Core.psc:807-839` | `ChangeTaskSpeed()` — **變更移動速度**（0=walk, 1=jog, 2=run；swap travel package + EvaluatePackage） |

### 2.3 時間排程系統（Schedule）

2.3 時間排程系統（Schedule）的記錄已抽到 [npc-commands-schedule-functions.json](npc-commands-schedule-functions.json)（9 列）。

檔案:行號：保留原表「檔案:行號」欄內容。

內容：保留原表「內容」欄內容。

統計：共 9 筆記錄、2 欄。

### 2.4 實體導航系統（Travel）

2.4 實體導航系統（Travel）的記錄已抽到 [npc-commands-travel-functions.json](npc-commands-travel-functions.json)（13 列）。

檔案:行號：保留原表「檔案:行號」欄內容。

內容：保留原表「內容」欄內容。

統計：共 13 筆記錄、2 欄。

### 2.5 卡點恢復系統（Stuck Detection & Recovery）

2.5 卡點恢復系統（Stuck Detection & Recovery）的記錄已抽到 [npc-commands-stuck-recovery-functions.json](npc-commands-stuck-recovery-functions.json)（6 列）。

檔案:行號：保留原表「檔案:行號」欄內容。

內容：保留原表「內容」欄內容。

統計：共 6 筆記錄、2 欄。

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

