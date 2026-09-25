# 架構總覽

[返回入口](../intelEngine-gameplugin-analysis.md)

## 架構總覽

IntelEngine 是 SkyrimNet 的**社群擴充**，專注於讓 NPC 在實體世界中**自主行動**。它基於 SkyrimNet 的 YAML action 系統定義 actions，然後用 Papyrus 腳本執行真正的遊戲內行為（移動、跟隨、傳話、戰鬥）。

最與眾不同的設計：IntelEngine 不是讓 LLM 選一個「action keyword」然後由外部系統解釋，而是**LLM 選擇 action → 對應 Papyrus 函數直接執行**，且 NPC 會**實際在遊戲世界中走路移動**。

```
玩家用自然語言跟 NPC 對話
  → SkyrimNet LLM 選擇 IntelEngine action (YAML: intel_schedulemeeting, intel_travel, ...)
    → SkyrimNet 執行對應 Papyrus function (ScheduleMeeting, GoToLocation, ...)
      → IntelEngine Papyrus:
          ├─→ Slot 管理系統 (5 concurrent slots max)
          ├─→ Package override (Walk/Jog/Run/Stalk/Sandbox)
          ├─→ 路徑搜尋 + 卡點恢復 (soft stuck → waypoint nav → leapfrog → teleport)
          ├─→ 到場偵測 (C++ ProximityMonitor 150ms poll)
          ├─→ 等待/逗留系統 (linger + approach + release)
          └─→ Schedule 系統 (遊戲內時間排程)
```

---

## 1. 世界狀態總結 (World State Summarization)

### 1.1 設計模式：C++ Native + StorageUtil 雙軌

IntelEngine 的世界狀態分散在兩個地方：
- **C++ Native DLL**：提供高效能的索引查詢（location index, NPC home lookup, door teleport targets）、stuck detection（StuckDetector）、off-screen arrival estimation（OffScreenTracker）、proximity monitoring（ProximityMonitor）
- **Papyrus StorageUtil**：持久化每個 NPC 的任務狀態（task type, target, state, speed, deadline, destination marker, etc.）

### 1.2 狀態欄位（StorageUtil on Actor）

每個在任務中的 NPC 會被寫入大量狀態欄位（從 `Core.psc:ClearSlot()` 清理邏輯逆向推導）：

**核心任務狀態**：`Intel_TaskType`, `Intel_Target`, `Intel_Slot`, `Intel_State`, `Intel_Speed`, `Intel_TaskStartTime`, `Intel_WaitHours`, `Intel_WaitForPlayer`, `Intel_WasFollower`

**導航相關**：`Intel_DestMarker`, `Intel_ReturnMarker`, `Intel_CurrentWaypoint`, `Intel_TravelArrivalTime`, `Intel_OffscreenArrival`

**會議相關**：`Intel_IsScheduledMeeting`, `Intel_MeetingTime`, `Intel_MeetingDest`, `Intel_MeetingNpcArrivalTime`, `Intel_MeetingPlayerName`, `Intel_MeetingOutcome`, `Intel_MeetingLateHours`

**逗留/接近**：`Intel_MeetingLingering`, `Intel_MeetingLingerApproaching`, `Intel_TravelLingering`, `Intel_StayAtDest`, `Intel_LingerFarTicks`, `Intel_ApproachStartX/Y`, `Intel_ApproachTick`

**多步驟任務**：`Intel_TargetNPC`, `Intel_Message`, `Intel_DeliveryMeetLocation`, `Intel_InteractCyclesRemaining`

### 1.3 Task History（NPC 記憶）

`Core.SaveTaskToHistory()` (`Core.psc:374-417`)：每次任務結束，寫入滾動的 10 條歷史記錄。包含 task type、target、result、message content、meeting location。預先渲染為 prompt-ready 文字（`Intel_TaskHistoryRendered`）供 SkyrimNet character bio submodule 直接使用。

### 1.4 Fact Injection API（敘事注入）

`Core.InjectFact()` (`Core.psc:1487-1525`)：將敘事性「事實」注入 NPC 的 bio context。Pure FIFO（10 條上限），無時間過期。預渲染為 `Intel_FactsRendered` 供 bio submodule 讀取。

用途例：
- "invited the Dragonborn to dinner but was turned down"
- "was ambushed by the player near Riverwood and barely escaped"

### 1.5 Gossip Injection API（流言傳播）

`Core.InjectGossip()` (`Core.psc:1533-1596`)：雙向記錄——接收者記錄 "heard from X" + 傳播者記錄 "told Y"。各 5 條上限。預渲染為 `Intel_GossipRendered`。

### 1.6 Received Messages

`Core.StoreReceivedMessage()`: 儲存 NPC 收到的訊息內容、發送者名稱、時間戳。讓 NPC "記得" 有人傳話給他們。

### 1.7 Meeting Outcomes

`Core.StoreMeetingOutcome()`: 會議結果（success/player_late/npc_late/player_no_show/npc_late_player_no_show）。持久化到 StorageUtil，供 bio prompt 使用。

---

