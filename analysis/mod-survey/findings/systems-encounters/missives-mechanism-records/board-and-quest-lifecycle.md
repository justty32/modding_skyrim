# 1. 這個 mod 做什麼 + 怎麼運作

← [原文入口](../missives-mechanism-records.md)

## 1. 這個 mod 做什麼 + 怎麼運作

Missives 在各城鎮放置一塊**公告板（Missive Board）**，板上不定期刷出一疊**告示（missive，BOOK 道具）**。玩家拿走一張 missive → 對應的 **radiant quest 自動啟動**：到隨機地點（leveled）幹活（殺賞金頭目 / 取物 / 採集 / 送信 / 追捕逃犯）→ 回報領賞（金幣 + leveled 物品）。

關鍵架構結論：**這顆 mod 完全沒有用 Story Manager**（`smtree`/`dump` 沒有任何 `StoryManagerEventNode`/`SMEN`/`SMBN`/`SMQN`，quest 全是 `type=Misc`、`event=` 空）。**radiant 行為的本體是「引擎的 quest-alias Find-matching-conditions 填充系統」**，由 CK 裡 quest record 的 alias 定義驅動；Papyrus 只負責「板子上刷 quest」「objective 推進」「結算發獎/清 missive」這些膠水。換句話說 Missives = **一個 Activator 控制器 + 265 顆預先寫死的 radiant quest 模板**，沒有中央 controller quest，沒有 SM 子樹。

record census（`dump`）說明性質：

本表整理「1. 這個 mod 做什麼 + 怎麼運作」的逐項記錄。

已抽到 [board-and-quest-lifecycle-record-census.json](board-and-quest-lifecycle-record-census.json)（12 列）。

欄位「記錄類型」：保留原表的記錄類型。

欄位「數量」：保留原表的數量。

欄位「角色」：保留原表的角色。

統計：12 筆記錄，3 個欄位。


`gamedata` 報 `dialogue_lines=0` 是因為這些 topic 是 player 主動講的領賞句、不是 NPC response 體（diag census 只算後者）。`scnscan` 無 scene。

### 公告板 → missive → radiant 目標 → 回報 的完整鏈

<!-- wf-nav -->
1. **刷 quest（板子控制器）**：`_M_ActivatorBoard` 上的 `_M_ActivatorScript`（extends ObjectReference）`OnTriggerEnter`：玩家走近且距上次刷新超過 `RefreshRate` 天，就對 4 個 tier 各跑一次 `UpdateQuests(chance, FormList)`：遍歷該池每顆 quest，`Utility.RandomInt() < chance` 就 `MissiveQuest.Start()`；若 quest 已在跑但玩家還沒接（`GetStage()==0`）就 `SetStage(110)` 收掉（讓位給新的）。**這就是「板子刷新」的全部**——機率 roll + `Quest.Start()`。
2. **接任務（Start 自動填 alias + 投放 missive）**：`Quest.Start()` 觸發引擎的 alias 填充（見 §2）：Location alias 依 hold 條件挑一個隨機地點，nested Reference alias 在該地點裡找箱子/頭目/物品，並把 missive BOOK（`Alias_Missive`）放進板子容器。玩家把 missive 收進背包 → `_M_AliasMissiveScript.OnContainerChanged` → `SetStage(20)`（任務正式開始、objective 顯示）。
3. **做任務（alias 事件推進 objective）**：各 job-type 的目標達成靠掛在 alias 上的 ReferenceAlias 腳本，而非中央輪詢：
   - **Kill/Retrieve 頭目**：`_M_AliasBossScript.OnDeath` → `SetStage(Stage)`。
   - **取物/送信**：`_M_AliasItemScript` / `_M_AliasDeliveryScript.OnContainerChanged` → 物品進玩家背包就完成 objective、離開就退回。
   - **採集**：quest fragment 用 `Game.GetPlayer().GetItemCount(...)` 對 `ItemTotal`（一個 `Utility.RandomInt(min,max)` 決定的隨機數量）比對。
   - **送信期限**：`_M_AliasPlayerCourier.OnUpdateGameTime`（每 6 遊戲小時）比對 `GameDaysPassed > DeliveryDate`，逾期 `SetStage(103)`（失敗）。
4. **回報領賞**：玩家對 radiant 填出來的 QuestGiver/Steward/Jarl 講該 quest 的 `*RewardTopic` 對話 → quest fragment `CompleteAllObjectives()` + `Player.AddItem(Gold001, GoldReward)` + 採集/送信型再 `AddItem(Reward)`（LVLI）→ `SetStage(110)` → fragment 把 missive 從板子或玩家身上移除、`Stop()`。

比重：**控制器 Papyrus 極輕**（一個 Activator 腳本 roll 機率），**任務膠水 Papyrus 中等**（每 job-type 一個 quest fragment 腳本 + 幾個 alias 事件腳本，都只做 objective/stage/發獎），**radiant variety 100% 靠引擎 alias 填充 + 預先寫死的 265 顆模板**。沒有 SM、沒有 controller quest。

---

