# RDO 的 Papyrus 腳本：投放靠資料、腳本只補三件小事 — script-inventory-and-throttling

[返回入口](../rdo-scripts.md)

## 0. 一句話結論

RDO 的對話投放**完全不靠 script**——98 個腳本裡沒有任何一支在 runtime 決定「哪句話投給哪個 NPC」。投放是純資料（INFO + condition + 靜態 FormList），script 只負責三件 vanilla 對話框架本來就需要的瑣事：**節流計時、隨從管理、quest fragment 黏合**。BSA 還附帶完整 `.psc` 原始碼，無需反編譯即可全文閱讀，本文所有引用皆來自原始碼。

## 1. 腳本清單與數量

`scripts/source/` 共 **98 個 `.psc`**（與 98 個 `.pex` 一一對應）。對照 architecture 統計的「9765 records / 6650 新 INFO」，腳本佔比極低——平均約 68 句新台詞才攤到 1 支腳本，而那支腳本與「這句話投給誰」毫無關係。

按家族歸併後，98 支可收斂成寥寥幾類：

| 家族 | 數量 | 性質 | 代表檔 |
|---|---:|---|---|
| `RDO_IdleCommentTimer<VT>` | 20 | 每個 VoiceType 一支的**節流計時器** | `rdo_idlecommenttimerfnord.psc` |
| `RDO_NextIdleComment<VT>` | 20 | 上者的 TopicInfo fragment 觸發殼 | `rdo_nextidlecommentfnord.psc` |
| `RDO_Default*`（follow/recruit/dismiss/wait/trade/favor…） | 10 | 共用隨從/好感 TopicInfo fragment | `rdo_defaultfollowme.psc` |
| Gelebor / Isran / Valerica 隨從組（各 7） | 21 | 三名 RDO 自管隨從的完整 follower 框架 | `rdo_geleborfollowerscript.psc` |
| Kaie confront quest 組 | 6 | RDO 原創 Kaie 劇情 quest 的 fragment + alias | `rdo_kaieconfrontquestfragments.psc` |
| FfRiftenGrelka 組 | 5 | 一段 Riften 任務的 fragment + 說服/賄賂/恐嚇 | `rdo_ffriftengrelkaquestfragments.psc` |
| 其餘單支 | 16 | MCM、misc fixes、各式 TIF/SF fragment | 見 §4 |

四個「家族」（71 支）幾乎都是**機械複製**：20+20 個是「每個 VoiceType 各一份的同一支節流器」，21 個是「三名隨從各複製一份同一套 follower 邏輯」。真正獨立的內容腳本只有十來支。

注意命名與 architecture 提到的節點吻合：`a_RDOKaieConfront`（→ `rdo_kaieconfrontquestfragments.psc`）、`a_RDOAssaultActor`（對應 SM `a_RDOAssaultActorNode`）等都能在腳本側找到落點。

## 2. 唯一稱得上「投放輔助」的 script：per-VoiceType 節流

architecture 與 targeting-technique 都猜測 RDO 有「per-voicetype comment 計時節流，推進 `a_RDO_*NextComment` 全域變數」。解包後**完全證實**，而且這是全 mod 唯一與投放沾邊的 script 機制——但它管的是「多久能再講一次」，不是「投給誰」。

機制三件套（以 FemaleNord 嗓音為例）：

1. **計時器本體** `RDO_IdleCommentTimerFNORD extends Quest`（`rdo_idlecommenttimerfnord.psc`）。核心函式 `Commented()`：擲 `Utility.RandomInt(1,7)` 取一個 0.01–0.06 的 `DaysUntilNextAllowed`（約 15 分鐘到 1.5 小時遊戲時間），加上 `GameDaysPassed.GetValue()` 得 `NextAllowed`，寫回 `a_RDO_FNORDNextComment.SetValue(NextAllowed)`。

   ```papyrus
   float NextAllowed = GameDaysPassed.GetValue() + DaysUntilNextAllowed
   a_RDO_FNORDNextComment.SetValue(NextAllowed)
   ```

2. **觸發殼** `RDO_NextIdleCommentFNORD extends Quest Hidden`（`rdo_nextidlecommentfnord.psc`）。一個 CK 自動生成的 quest fragment，整支只做 `kmyquest.Commented()` 一行——掛在某筆評論 INFO 的 quest stage fragment 上，NPC 一旦講了話就推進計時器。

3. **回讀**：condition 端用 `GetGlobalValue`/`ConditionGlobal` 比較 `a_RDO_*NextComment` 與當前 `GameDaysPassed`，「冷卻未到 → 整筆 INFO 失格」。這一步**在資料（condition）裡，不在 script**。

也就是：script 只負責「把下次允許時間寫進全域變數」，至於「這個全域變數讓哪句話冷卻」「冷卻的是哪一群 NPC」，全由 condition + VoiceType 決定。架構文檔行 145 提到的 `a_RDO_FNORDNextComment` / `a_RDO_MDRNKNextComment` 等 20 個 GlobalFloat，正是這 20 支計時器各自的儲存格。

對應的 TopicInfo fragment（如 `rdo_defaultidlecomment.psc`）也只是 `GetOwningQuest().SetStage(30)` 一行——推進 stage 觸發上述計時，同樣不碰投放。

## 3. 沒有「動態維護 aaa_RDOVoices* 名單」這回事

另一個 architecture 的猜測——「把 NPC 動態加進/移出 `aaa_RDOVoices*` FormList」——**解包後證偽**。對全 98 支 script grep `RDOVoices` / `AddForm` / `RemoveAddedForm` 到 voice 名單，**零命中**。`aaa_RDOVoices*`（18 個 FormList）是 CK 裡靜態建好的，runtime 只被 `IsInList` condition 讀取，從不被 script 改寫。

唯一的 runtime FormList 寫入在 `RDO_MCMConfig.RDO_StartupChanges()`（`rdo_mcmconfig.psc:198` 起），且**與 voice 投放無關**：它在 `OnInit()` 一次性把 RDO 自製的 encounter NPC 注入三個 vanilla **LeveledActor** 列表——

```papyrus
WEAdventurerSpellswordSubChar.AddForm(_RDOLeveledActorsWEAdventurerSS.GetAt(0), 1)
LCharHunter.AddForm(_RDOEncHunters.GetAt(0), 1)
LCharOrcMissile.AddForm(_RDOEncOrcHuntersFemale.GetAt(0), 1)
```

目的（原始碼註解寫得很白）是讓「原版有配音卻沒被用到的 VoiceType」（FemaleCommander/FemaleSultry 傭兵、MaleCommonerAccented 獵人、FemaleOrc 獵人）有實際 NPC 去講那些早就錄好的台詞。這是「補 vanilla 漏網的 leveled list」，做完即 `changesDone = True` 不再執行——一次性資料修補，不是投放邏輯。

