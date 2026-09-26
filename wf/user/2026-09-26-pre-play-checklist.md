# 下次開玩前要做的事（2026-09-26 早場彙整）

> 整理線 `checklist` 寫（09:25 定稿，八份報告都已收到，yvanni 線代跑的 RT 實機結果也併進來了）。內容全部來自各線 REPORT 和 `RT-QUEUE.md` 的「RT 結果」，沒有另外推新結論。報告之間有矛盾的地方標「待驗」。

今早處理了八題：Forget Spell 移除 ability（forget）、Apocalypse 譯文移植（apoc2）、Vilja 的 NFF 選項（vilja）、卡西娅的信（cassia）、Katana 召喚失效（katana）、金丘農園招總管和 cell 名（farm）、Yvanni 不見了（yvanni）、Aniya 米凱爾任務卡住（aniya）。
其中七題有解：cassia、katana、yvanni、aniya、forget 照 C／D 段打 console 或走對話就能處理；apoc2 和 farm 的修正層已放在 staging，等你決定裝不裝。vilja 的報告和實機結果**矛盾**，要重看（見 C3、E）。
有 7 項要你裁示（見 A）。另外，MO2 開遊戲後 profile 三檔漂移了，dispatcher 已經派 mo2close 線去還原（見 E）。

---

## A. 要你裁示（裁了我才裝）

- **apoc2 24 欄層**：裝的話，22 個 MGEF 名和 2 個 SPEL 名會從英文殘留換成中文，但大多是隱藏的 `*BodyArtHolder`，玩家幾乎看不到；不裝就維持現狀，沒有任何壞處。〔apoc2〕
- **apoc2 另外 334 欄換不換措辭**：這 334 欄只差譯法，例如「烬火炎矢→余烬之矢」。換的話，周目中途法術名會變，跟 Vokriinator／Ordinator 補丁、還有你記得的名字對不上；不換就維持現役譯法。報告建議不換，要換的話先看 `apoc2/review-both-chinese.json`。〔apoc2〕
- **NFF 繁中 esp 排到簡中上方**：排的話，Export 選項會從誤導人的 `[现在按你自己的意志自由活动，you are free]` 改成 `[從框架中移除]`，TC 層修好的兩個 key 也會生效；不排就維持 09-03 inst5 的安排。實機顯示 Vilja 已經被 NFF 匯入，所以她會看到的正是這句 Export 選項，這項和她直接相關。〔vilja §4.1〕
- **Cassia's Plea Remover 重複目錄**：這個目錄其實是主檔被裝了第二次（逐檔 md5 相同）。停用或改名標成「=主檔重複」都無害；不處理也無害。不必補下載 optional，用 C1 的 console 解就好。〔cassia〕
- **farm A：農舍 cell 名修正層**：裝的話，門口提示和室內地點名會從「Creation Club Cell」改成「金丘農園」；不裝就維持英文。〔farm〕
- **farm B：任何隨從都能當總管**（ESPFE）：裝的話，Vilja 這類自訂語音的隨從也能招成總管，但那句台詞會是無聲字幕；不裝的話只有 9 種原版語音的隨從能招，Vilja、Yvanni、Aniya、Sofia、Lydia 等人永遠看不到選項。〔farm〕
- **aniya 修正層**（ESL）：裝的話，就算米凱爾沒來 forcegreet，你也能自己找他點「米凯尔，求你别再纠缠安妮亚了。」；不裝就用 C6 的一行 `set`，效果一樣。〔aniya〕

## B. 進遊戲前（MO2／設定層）

- 開 MO2 之前，先確認 mo2close 線已經把 profile 還原並收線（見 E）。〔yvanni §5〕
- 裁了裝 apoc2：把 `~/skyrim_mods/_staging-2026-09-26/apoc2/Apocalypse-Magic-of-Skyrim-Simplified-Chinese-FULL-Completion-Combined-Dev-2026-09-26/` 放進 MO2 mods，排在 `Apocalypse-…-Combined-Dev-2026-09-25` **正上方**（第 251 行之上）。plugins.txt 不用動。〔apoc2〕
- 裁了 NFF 順序：把 `Nether's Follower Framework Traditional Chinese 2.8.6b Dev 2026-08-16` 排到 `NFF Simplified Chinese 113822 2.8.6b` 上方。〔vilja §4.1〕
- 裁了裝 farm A：`~/skyrim_mods/_staging-2026-09-26/farm/USCC-FarmingPatch-CellName-ZH-Fix-Dev-2026-09-26/`，優先權要高於 `Unofficial-SCC-Patches-ZH-ALL-2026-09-12`。〔farm〕
- 裁了裝 farm B：`~/skyrim_mods/_staging-2026-09-26/farm/FarmOverseerAnyFollower-Dev-2026-09-26/`，plugin 排在 `ccvsvsse004-beafarmer.esl` 之後。〔farm〕
- 裁了裝 aniya 層：`~/skyrim_mods/_staging-2026-09-26/aniya/Aniya-Favor5-MikaelFallback-2026-09-26/`，plugin 排在 `Aniya Follower.esp` 之後。〔aniya〕
- **NFF MCM 設定**（要進遊戲後，準星對著 Vilja）：System 頁的 `Import Enabled` 切成 No，就能擋掉她的 Import 選項；要全域關掉的話，改關 `Allow Import/Export Dialogue`。這是報告給的做法，保留下來；但實機顯示她已經在 ImportFac 裡，所以標**待驗**（詳見 C3）。〔vilja〕
  - NFF 有個上游 bug：用「Load Settings」讀回設定時，`Allow Import` 會變成 Steward 對話的值。所以關掉之後如果又冒出來，重新關一次就好。〔vilja §4.2〕
- **前綴**：
  - 已經用實機驗證過：ForgottenCity=`A4`、EMCompViljaSkyrim=`D5`、Katana=`BC`、nwsFollowerFramework=`7B`、Aniya Follower=`BB`、Yvanni Follower=`FE3A7`（light）。
  - 還只是推算值：ccvsvsse004-beafarmer=`FE024`（light），用 C5 的第一步驗證。
  - 這些都是 Save229 當下的值，之後改了載入順序（例如 A 裁了新 plugin）就要重新用 `help` 對一次。

## C. 進遊戲後的 console 序列

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

## D. 遊戲內要用對話／MCM 做的事

- **D1 Katana／密格拉重招**：跟她們對話，選 **mod 自己的**跟隨選項，也就是回應是「我紧随在后。」的那條，**不要**選 NFF 的招募。兩人各做一次。報告原本寫要先用 NFF 讓她們離隊，但實機顯示她們目前不在隊上（C2 待驗），所以這一步可能可以省略。做完用 `GetGlobalValue AK69KatanaRecruited` 確認回 1。〔katana〕
- **D2 Vilja**（待驗）：可以用 MCM 關掉 `Import Enabled`，或什麼都不做、選項留著不按。C3 的矛盾釐清之前，**不要按** NFF 的 Import 或 Export 選項。〔vilja〕
- **D3 只是嫌 Active Effects 太雜**：用已經裝好的 Magic Organizer。打開魔法選單 → Active Effects → 選取效果 → 按 Hide 熱鍵。效果還在，只是看不到；要還原就開 F1 選單。〔forget〕
- **D4 金丘農園招總管**（沒裝 farm B 的情況）：帶一位語音合格的隨從，要在跟隨狀態、人在農園戶外，對話就會出現「我的農園需要一位總管。有興趣嗎？」。合格的例如 Uthgerd、Aela、Jordis、Iona、Brelyna、Marcurio、Kurone 系（Lili／Nina／Yumi／Coco）、Kiyomi、Rosalia、Charlotte、2B、Ryoko 等。完整名單在 `~/skyrim_mods/_staging-2026-09-26/farm/followers_eligibility.tsv`。〔farm〕
- **D5 Aniya 米凱爾**：C6 的 `set` 打完之後（或裝了 aniya 層之後），跟米凱爾對話，選「米凯尔，求你别再纠缠安妮亚了。」，然後選**威脅**（你 27 級，≥11 就一定成功）或**說服**（需要口才 ≥30）。**不要選打架**：上游有缺陷，打輸、對方逃跑或中途離開酒館，任務目標都不會完成。之後安妮亞會過來找你說話，任務收尾，好感 +3。〔aniya〕
- **D6 Yvanni**：救回之後跟她說「跟我来。我需要你的帮助。」，NFF 會自動接管（已實測）。確認 NFF 選單裡有她之後，存一個新檔。〔yvanni〕

## E. 未解／下次派線

- **profile 三檔漂移**：MO2 開遊戲後，modlist 自動多了一行 `-AssetTest-LightShaft-Dev-2026-09-25`，plugins／loadorder 也被重排了 5 行。dispatcher 已經派 mo2close 線去還原。開 MO2 前請先確認那條線已經收線。〔yvanni §5〕
- **vilja 需要重派**：實機顯示她已經在 nwsFF_ImportFac 裡，和報告「未匯入」的前提相反。要確認你看到的是哪一條選項（Import 還是 Export、在哪一層子選單），再決定要不要 Export。同時也影響 A 的 NFF 順序那項。
- **katana 待驗**：實機顯示兩人目前都不在隊上，報告推斷的「被 NFF 招募」這個前提沒有被坐實。也沒有查她們在不在 DismissedFollowerFaction，而 mod 自己的跟隨選項要求她們在這個 faction 裡。
- aniya：forcegreet 當初為什麼沒觸發，還沒查明。RT 第 8 步沒跑（要看米凱爾是不是被別的 mod 的場景佔住）。另外，上游「打架輸了任務目標不會完成」的缺陷沒修，要改 script 才能修。
- yvanni：她怎麼死的、怎麼跑到鬼海去的，都沒有定論。
- forget：種族被動用 `removespell` 移不掉的話，要派線做 SkyPatcher `spellsToRemove` 規則層（範本是 Nexus 159131）。
- farm：兩個 staging 層都還沒實機測過。
- RT 的限制：qa bridge 只抓得到 console 輸出的最後一行，所以 `sqv` 和 `help` 這類多行輸出都沒有拿到。各題 alias 有沒有填上，目前都還沒查到。

## 報告

- [forget/REPORT.md](../../agentctl/handoffs/home-2026-09-26/forget/REPORT.md)
- [apoc2/REPORT.md](../../agentctl/handoffs/home-2026-09-26/apoc2/REPORT.md)
- [vilja/REPORT.md](../../agentctl/handoffs/home-2026-09-26/vilja/REPORT.md)
- [cassia/REPORT.md](../../agentctl/handoffs/home-2026-09-26/cassia/REPORT.md)
- [katana/REPORT.md](../../agentctl/handoffs/home-2026-09-26/katana/REPORT.md)
- [farm/REPORT.md](../../agentctl/handoffs/home-2026-09-26/farm/REPORT.md)
- [yvanni/REPORT.md](../../agentctl/handoffs/home-2026-09-26/yvanni/REPORT.md)
- [aniya/REPORT.md](../../agentctl/handoffs/home-2026-09-26/aniya/REPORT.md)
- 實機代跑結果：[RT-QUEUE.md](../../agentctl/handoffs/home-2026-09-26/RT-QUEUE.md)（各段下方的「RT 結果」）
