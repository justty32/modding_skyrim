# 2. NPC 下令機制 (NPC Command/Control)

[返回入口](../intelEngine-gameplugin-analysis.md)

## 2. NPC 下令機制 (NPC Command/Control)

### 2.1 SkyrimNet YAML Actions → Papyrus Functions

IntelEngine 註冊為 SkyrimNet 的 custom category actions。檔案在 `SKSE/Plugins/SkyrimNet/config/actions/`：

2.1 SkyrimNet YAML Actions → Papyrus Functions的記錄已抽到 [npc-commands-action-function-mapping.json](npc-commands-action-function-mapping.json)（10 列）。

Action YAML：保留原表「Action YAML」欄內容。

Papyrus Function：保留原表「Papyrus Function」欄內容。

用途：保留原表「用途」欄內容。

統計：共 10 筆記錄、3 欄。

加上三個 category YAML（`cat_travel.yaml`, `cat_scheduling.yaml`, `cat_communication.yaml`）實現兩段式 drill-down。

### 2.2 Slot 管理系統（5 個 concurrent slots）

IntelEngine 使用 5 個 ReferenceAlias slots 管理同時進行的 NPC 任務（`Core.psc`）。這是整個系統的核心基礎設施：

- `AllocateSlot()`: 分配 slot，寫入 Papyrus arrays + StorageUtil + C++ SlotTracker
- `ClearSlot()`: 清理 slot，寫入 task history，清除所有 package/linked ref/StorageUtil data。支援 `intelPackagesOnly` 模式（保留 SkyrimNet/NFF 的 follow packages）
- Slot states: 0=empty, 1=traveling, 2=at_destination, 3=returning, 5=search_wait, 8=at_target
- 每次 slot 狀態變更都**三寫**：Papyrus array + StorageUtil + C++ SlotTracker（供 SkyrimNet decorators 查詢）

### 2.3 時間排程系統（Schedule System）

`IntelEngine_Schedule.psc` 是 IntelEngine 最獨特的子系統。它支援**未來時間表達式**的解析與排程：

**時間條件解析**（C++ `ParseTimeCondition`）：接受自然語言時間（"at dawn", "at sunset", "tomorrow morning", "in three hours"），轉換為精確的遊戲內時間。

**排程類型**：
- **Meeting**: NPC 在指定時間前出發（計算距離基礎的 departure buffer），走到目的地，等待玩家。支援 lateness detection、grace period、timeout。
- **Scheduled Fetch**: 在指定時間出發去找人
- **Scheduled Delivery**: 在指定時間出發去傳話（可選 meeting invite）

**Dispatch 機制**：
- `RegisterForSingleUpdateGameTime()` 遊戲時間定時器（主要）
- `RegisterForSingleUpdate(15.0)` 實時定時器（備援，處理 < 1 game hour 的短期排程）
- `CheckAndDispatchPendingTasks()`: 檢查所有 pending schedule，到期就 dispatch

**Departure Buffer**：NPC 不是在 meeting time 才出發，而是計算距離（`CalculateDeadlineFromDistance`），提前足夠時間出發。上限為 meeting time 的 75%（防止過早出發）。

### 2.4 實體導航系統（Travel System）

`IntelEngine_Travel.psc` 是物理移動的執行層：

**目的地解析**（`ResolveDestination`）：
- Named locations: "The Bannered Mare", "Dragonsreach"
- Semantic locations: "upstairs", "outside", "the back room"
- Fuzzy matching: "whiterun"

全部委託 C++ `ResolveAnyDestination()`，回傳 ObjectReference marker。

**移動速度**：0=walk, 1=jog, 2=run。各有對應的 AI Package（`TravelPackage_Walk/Jog/Run`）。

**到場偵測**：
- C++ `ProximityMonitor`：每 150ms 檢查一次距離，到場即觸發 callback（消滅 3 秒 Papyrus poll 的延遲）
- Door teleportation：自動通過 loading door（如 "outside" 語意目的地）
- Floor Z-height check：防止 NPC 站在樓下被判定為「已到達」樓上目標
- Same-cell interior check：off-screen NPC 在同一 interior cell 視為到達

**卡點恢復**（四層漸進）：
1. **Soft Stuck**：隨機位移 + 重新套用 travel package + PathToReference
2. **Waypoint Navigation**：找中途地點標記重新導向
3. **Multi-angle Leapfrog**：200→500→1000→2000 單位跳躍，±30° 旋轉角度
4. **Teleport**：最終手段

### 2.5 逗留系統（Linger System）

NPC 到達後不立刻消失，而是：
1. **Approach phase**: 走向玩家（walk speed）
2. **Sandbox phase**: 在玩家 200 單位內自由活動（`SandboxNearPlayerPackage`）
3. **Release**: 玩家走開 `LINGER_RELEASE_DISTANCE`（預設 800 單位）後，NPC 自行回家

對 sandbox-only AI 的 NPC（常見於 modded followers），提供 walk-home fallback。

### 2.6 會議系統（Meeting System）

完整的會議生命週期：
1. **Scheduling**: LLM 選擇 `ScheduleMeeting` action → 解析時間、計算 departure buffer、存入 schedule slot
2. **Dispatch**: 排程時間到 → `GoToLocation()` with `isScheduled=true`
3. **Arrival**: NPC 到達目的地，等待玩家
4. **Smart Approach**: 玩家接近目的地 2000 單位 → NPC 走向玩家
5. **Player Arrival**: 偵測玩家到場 → 計算 lateness（玩家/NPC 雙方的遲到判定）→ 敘事旁白
6. **Linger**: 玩家在場時 NPC 逗留附近
7. **Completion**: 玩家離開 → 會議結束，NPC 自行離開

---

