# IntelEngine-GamePlugin 分析：世界狀態、NPC 指令、對話控制

> 來源: `external/frameworks/IntelEngine-GamePlugin/` (clone from https://github.com/galanx/IntelEngine-GamePlugin)
> 分析日期: 2026-07-30
> 類型: SkyrimNet 社群 plugin（基於 SkyrimNet YAML action API + Papyrus）
> 關注範圍: 世界狀態總結機制、NPC 下令、對話改變

---

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

## 2. NPC 下令機制 (NPC Command/Control)

### 2.1 SkyrimNet YAML Actions → Papyrus Functions

IntelEngine 註冊為 SkyrimNet 的 custom category actions。檔案在 `SKSE/Plugins/SkyrimNet/config/actions/`：

| Action YAML | Papyrus Function | 用途 |
|-------------|-----------------|------|
| `intel_travel.yaml` | `GoToLocation(npc, dest, speed, waitForPlayer)` | NPC 走到指定地點 |
| `intel_changespeed.yaml` | `ChangeTaskSpeed(npc, newSpeed)` | 改變行進速度 |
| `intel_canceltask.yaml` | `CancelCurrentTask(npc)` | 取消當前任務 |
| `intel_schedulemeeting.yaml` | `ScheduleMeeting(npc, dest, timeCondition)` | 排程會議 |
| `intel_schedulefetch.yaml` | `ScheduleFetch(npc, target, timeCondition)` | 排程找人 |
| `intel_scheduledelivery.yaml` | `ScheduleDelivery(npc, target, msg, timeCondition, meetLoc, meetTime)` | 排程傳話 |
| `intel_fetchnpc.yaml` | `FetchNPC(agent, targetName)` | 去把某人找來 |
| `intel_escorttarget.yaml` | `EscortTarget(agent, targetName, destName, shouldWait)` | 護送某人到某地 |
| `intel_delivermessage.yaml` | `DeliverMessage(agent, target, msg, meetLoc, meetTime)` | 傳話給某人 |
| `intel_searchforactor.yaml` | `SearchForActor(agent, targetName)` | 一起找某人 |

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

## 3. 對話改變機制 (Dialogue Changes)

### 3.1 敘事注入（Narration Injection）

IntelEngine 透過 SkyrimNet 的 `DirectNarration` API 注入對話：

```papyrus
SkyrimNetApi.DirectNarration(msgText, akActor, akTarget)
```

使用場景：
- 任務開始/完成時的旁白（NPC 說出他們要去哪裡/在做什麼）
- 卡點時的 stumble narration
- 會議遲到/準時的 greeting
- 玩家接近時的 proximity-based greeting

### 3.2 持久記憶注入

```papyrus
SkyrimNetApi.RegisterPersistentEvent(msgText, akOriginator, akTarget)
SkyrimNetApi.RegisterEvent("intel_task_event", msgText, akOriginator, akTarget)
```

讓 NPC 的 prompt context 包含任務歷史和事件記憶。

### 3.3 Character Bio 注入（Facts + Task History + Gossip）

IntelEngine 將狀態預渲染為 prompt-ready 文字，寫入 StorageUtil：
- `Intel_TaskHistoryRendered` → SkyrimNet character bio submodule 直接讀取
- `Intel_FactsRendered` → 注入 bio 的 "facts" 段落
- `Intel_GossipRendered` → 注入 bio 的 "rumors I've heard" 段落
- `Intel_MeetingOutcome` → 注入 bio 的 "recent meetings" 段落

這些欄位對應 SkyrimNet 的 character bio submodules（`0497_intel_facts.prompt`, `0195_intel_gossip.prompt`, `0199_intel_meeting_outcome.prompt` 等）。

### 3.4 Story Engine（Dungeon Master）

`IntelEngine_StoryEngine.psc` 是 IntelEngine 的自主行為引擎。它用一個 LLM DM prompt，接收候選 NPC pool + 世界 context，決定**誰**行動和**什麼類型**的故事：

九種故事類型（LLM 決定，非隨機）：
| Story Type | 描述 |
|------------|------|
| `seek_player` | NPC 尋找玩家（有事要說） |
| `informant` | NPC 傳遞關於另一 NPC 的八卦 |
| `npc_interaction` | 兩個 NPC 互動 |
| `npc_gossip` | NPC 分享謠言給另一 NPC |
| `road_encounter` | 路上的偶遇 |
| `ambush` | 敵對 NPC 潛行跟蹤 + 攻擊 |
| `stalker` | 迷戀/嫉妒 NPC 秘密跟蹤 |
| `message` | NPC 傳遞口信 |
| `quest` | NPC 請求協助（bounty/救援/物品 retrieval） |

Story Engine 有完整的配置系統：Hold restriction policy（限制 NPC 只能從哪個 hold 來）、danger zone policy、player home policy、per-type enabled toggles 等。

### 3.5 Faction Politics Engine

README 提到但未深入分析的 `IntelEngine_Politics.psc`：
- 9 個可配置 faction
- 每 6 遊戲小時生成政治事件（trade deals, espionage, border skirmishes, assassinations, war declarations, surrenders）
- Player standing 根據行動升降
- Faction wars：士氣、軍隊強度、off-screen battles、player-present battles（5 waves, 22 per side）
- PrismaUI dashboard 顯示 faction 關係、active wars、player standings
- NPC 在對話中感知政治事件

---

## 4. 設計亮點與取捨

### 4.1 世界狀態總結

| 設計 | 優點 | 代價 |
|------|------|------|
| C++ native + StorageUtil 雙軌 | 高效能查詢 + Papyrus 可存取 | 狀態分散，需仔細同步 |
| Task history/facts/gossip 預渲染為 prompt-ready 文字 | SkyrimNet bio submodule 零成本讀取 | 更新時需重新渲染整個字串 |
| FIFO 10-entry rolling history | 簡單、無需時間過期邏輯 | 高活躍 NPC 可能快速覆蓋舊記錄 |
| 雙向 gossip 記錄 | 完整追蹤資訊流 | 儲存空間加倍 |

### 4.2 NPC 下令

| 設計 | 優點 | 代價 |
|------|------|------|
| SkyrimNet YAML action → Papyrus function | 利用 SkyrimNet 的 LLM action selection | 需維護 YAML + Papyrus 兩層 |
| 5-slot concurrent task 系統 | 多 NPC 同時行動 | 嚴格上限，額外任務排隊或拒絕 |
| 時間排程 + departure buffer | 自然感覺（NPC 計算路程提前出發） | 跨 cell distance 計算在 interior 不準 |
| 四層卡點恢復 | 極度 robust | 漸進式 fallback 增加複雜度 |
| C++ ProximityMonitor 150ms | 幾乎即時的到場偵測 | 依賴 C++ 插件 |
| Linger + approach + release | NPC 行為自然、不突兀 | 多階段狀態機，邊界條件多 |

### 4.3 對話系統

| 設計 | 優點 | 代價 |
|------|------|------|
| DirectNarration 注入 | NPC 即時語音回饋 | 佔用 TTS queue |
| 預渲染 bio sections | 零 runtime cost | 更新不是即時的 |
| Story Engine DM prompt | 自主故事生成 | 需額外 LLM call |
| 完整的 meeting outcome 追蹤 | 支援複雜的社交敘事 | 大量 StorageUtil 讀寫 |

---

## 5. 與其他 repos 的比較

| 面向 | IntelEngine | SkyrimNet | Mantella | MinAI |
|------|-------------|-----------|----------|-------|
| NPC 移動 | **真實走路（AI Package）+ 卡點恢復** | 無（僅 lookAt + follow） | 無（靠 Papyrus package 指令） | 無（靠 CHIM） |
| 時間排程 | **遊戲內時間排程系統** | 無 | 無 | 無 |
| 會議系統 | **完整生命週期（lateness/l linger/release）** | 無 | 無 | 無 |
| 自主行為 | Story Engine（LLM DM） | GameMaster agent | Radiant conversations | 無 |
| Action 系統 | SkyrimNet YAML → Papyrus | YAML/Papyrus/Native C++ | JSON → OpenAI function calling | CHIM action registry |
| 世界狀態 | StorageUtil + C++ native | C++ 直讀記憶體 | HTTP JSON | SetActorVariable() |
