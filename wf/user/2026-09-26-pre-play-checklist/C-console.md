# 下次開玩前要做的事——C. 進遊戲後的 console 序列（2026-09-26）

> 從 [2026-09-26-pre-play-checklist.md](../2026-09-26-pre-play-checklist.md) 拆出（2026-10-10 git-tidy，>8 KB 拆檔），內容未改。


讀 Save229。**只要步驟會改存檔，做完一律另存新檔，不要覆蓋 Save229。**

### C1. 卡西娅的信（兩封「卡西娅的请求」丟不掉）〔cassia〕

實機已經驗證：前綴是 A4，身上有 2 封，`000FCQuest01` 已完成（=1），所以可以安全 stopquest。建議還是再確認一次 `getquestcompleted 000FCQuest01` 回 1；**如果回 0，就不要 stopquest，只做 removeitem**，否則每次換地點都會再收到一封新信。

以下會改存檔：
```
getquestcompleted 000FCQuest01
stopquest 000FCQuestStart
player.removeitem A4036D8C 2
player.getitemcount A4036D8C
```
最後一行應該回 0。確認後另存新檔。stopquest 本身沒有副作用（這個 quest 只有 stage 0，沒有日誌）。不要用 `completequest`。

### C2. Katana／密格拉召喚沒反應〔katana〕

實機已經驗證：兩個 global 都是 0，兩個召喚法術都還在身上。這和報告判斷的原因（SPEL 的 global 條件不成立）對得上。

**待驗**：報告推斷「她們是被 NFF 招募的」，但實機顯示 Save229 當下兩人**都不在隊上**：teammate=0、CurrentFollowerFaction=0、兩個 NFF faction 都是 0、沒有被 disable。所以 D1 裡「先用 NFF 讓她們離隊」這一步可能用不到，直接去找她們對話就好。另外，密格拉的懸賞任務 `AK69MegaraBanditQuest` 還在跑（stage 0）。

正規修法見 **D1**。救急做法（會改存檔；能力立刻能用，但 mod 自己的 Config／Reactions quest 不會啟動，之後被 mod 解雇時會歸零）：
```
set AK69KatanaRecruited to 1
set AK69MegaraRecruited to 1
```
人不見時的救援（會改存檔）：
```
prid BC005902
enable
moveto player
```
密格拉的話，把第一行換成 `prid BC8EBD22`。

選配：D1 重招之後，對她們 `additem 7B1CFC8D 1`（NFF Ignore Token），防止 NFF 再接管。這是從引用關係推出來的，**沒有實測過**。

### C3. Vilja 的 NFF 選項〔vilja〕— **待驗，報告和實機矛盾**

- **報告的結論**：她沒有被 NFF 管，看到的是 Import 入口 `[加入框架（匯入）]`，屬於正常現象。
- **實機結果**（RT，Save229）：
  - `getinfaction 7B016EB1`（nwsFF_ImportFac）回 **1**。按報告自己的判準，這代表她**已經被匯入**了。
  - 她的對話頂層只有 `告訴我你在想什麼。` 和 `晚點再說吧。` 兩條，沒有看到 NFF 選項，子選單沒有展開。
  - 其他幾項都符合預期：teammate=1、FollowerFac=0、NoImport=0、她自己的跟隨 faction=1。
- 按報告寫好的分支：如果她已經被匯入，你看到的應該是 Export 選項 `[现在按你自己的意志自由活动，you are free]`，結論要反過來。報告的做法先保留，但標**待驗**：
  - 用 MCM 關 `Import Enabled`（見 B）。
  - 或用 console 把她加進 nwsFF_NoImport（會改存檔）：
    ```
    prid Viljaref
    addtofaction 7B5C4445 0
    ```
  - 報告 §5 寫的退出順序是「先按 Export，再用 Vilja 自己的對話解散」。要不要這樣做，等重派的線確認之後再決定（見 E）。
- 進遊戲時請順手記下：你當初看到的那條選項的**完整原文**，以及它在哪一層子選單裡。

### C4. 移除某個 ability〔forget〕

Forget Spell 從設計上就不處理 ability，也沒有替代 mod，所以改用 console：
```
help "<能力名稱>" 4
player.removespell <FormID>
```
- 第 1 行：輸出裡要找 **SPEL** 那行的 FormID，不是 MGEF。
- 第 2 行會改存檔。做完存檔再讀檔，確認它真的不見了。
- 要恢復就 `player.addspell <FormID>`。
- 種族被動讀檔後如果又長回來，改走 E 的 SkyPatcher 路線（這種情況沒有實測過）。

### C5. 金丘農園招總管〔farm〕

先驗證（唯讀；FE024 還是推算值）：
```
help ccVSVSSE004 4
getstage FE024EB7
getinfaction 5c84e
```
- 第 2 行應該回 10。
- 第 3 行要先點選隨從再打，應該回 1。這是推論，沒有實機驗證過。
- **不要**用 `setstage FE024EB7 20` 當捷徑：總管欄位會是空的、收益計時器不會啟動，農園會半殘。console 沒有其他捷徑。
- 合格隨從也看不到選項的話，要查存檔裡的 `FarmOwned`／`HasOverseer`。報告沒有讀這兩個值。

### C6. Aniya「說服米凱爾別再糾纏安妮亞」卡住〔aniya〕

實機已經驗證（RT）：`AniyaWhereAreYou` stage=5，所以 quest 級條件都成立；米凱爾活著、在旗幟母馬、沒被 disable；兩個 global 可以用 EditorID 設定。**但 Save229 當下安妮亞不在隊上**（CurrentFollowerFaction rank -2，隊伍是薇莉亞／莱拉／萝赛塔）。這個任務的對話和 forcegreet 都要求她正在跟隨，所以**先把她招進隊伍**。

解法 A（建議，會改存檔）：先帶著跟隨中的安妮亞進白漫的旗幟母馬，再打：
```
set AniyaRomanceIntroFavor5_MikaelHasDialogue to 1
```
接著照 **D5** 做。選單如果沒有出現那條選項，先回報，不要亂 setstage。

解法 B（直接跳過；會改存檔，而且會少掉那段對話和 +3 好感）：
```
setobjectivecompleted BB31A013 7 1
set AniyaRomanceIntroFavor5_MikaelForcegreetGlobalVar to 0
set AniyaRomanceIntroFavor5_ConvincedMikael to 1
set AniyaRomanceIntroFavor5_Running to 0
set AniyaRomanceIntroFavor5_Done to 1
```
要補好感的話：先 `getglobalvalue AniyaRomanceLevel` 看原值，再 `set AniyaRomanceLevel to <原值+3>`。

### C7. Yvanni 不見了〔yvanni〕

她在 Save229 裡**已經死了**，屍體在 DAc0da 的鬼海（`zDcdGhostSea`，cell `DcdKalpicShip02`）。09-25 的 Save221 裡就已經是這樣，資料層沒有任何東西把她藏起來。她不在 NFF 名單裡，是因為她從來沒被 NFF 接管過。

在任何地方都可以救回（會改存檔；yvanni 線已經在不存檔的情況下實測可行）：
```
prid FE3A78D7
moveto player
resurrect
```
接著照 **D6** 做。副作用：`resurrect` 可能會重置她的裝備和背包，服裝可以之後用她的對話「更改服装」重新選。如果不救也沒關係，屍體留著對存檔沒有影響。
