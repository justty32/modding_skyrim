# 3. 對話改變機制 (Dialogue Changes)

[返回入口](../intelEngine-gameplugin-analysis.md)

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
