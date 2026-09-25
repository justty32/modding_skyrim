# 1. 世界狀態總結相關原始碼

[返回入口](../intelEngine-source-ref.md)

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

