# 下次開玩前要做的事（2026-09-26 早場彙整）

> 整理線 `checklist` 寫（09:25 定稿，八份報告都已收到，yvanni 線代跑的 RT 實機結果也併進來了）。內容全部來自各線 REPORT 和 `RT-QUEUE.md` 的「RT 結果」，沒有另外推新結論。報告之間有矛盾的地方標「待驗」。

今早處理了八題：Forget Spell 移除 ability（forget）、Apocalypse 譯文移植（apoc2）、Vilja 的 NFF 選項（vilja）、卡西娅的信（cassia）、Katana 召喚失效（katana）、金丘農園招總管和 cell 名（farm）、Yvanni 不見了（yvanni）、Aniya 米凱爾任務卡住（aniya）。
其中七題有解：cassia、katana、yvanni、aniya、forget 照 C／D 段打 console 或走對話就能處理；apoc2 和 farm 的修正層已放在 staging，等你決定裝不裝。vilja 的報告和實機結果**矛盾**，要重看（見 C3、E）。
有 7 項要你裁示（見 A）。另外，MO2 開遊戲後 profile 三檔漂移了，dispatcher 已經派 mo2close 線去還原（見 E）。

---

## A. 要你裁示（裁了我才裝）

<!-- wf-nav -->
- **apoc2 24 欄層**：裝的話，22 個 MGEF 名和 2 個 SPEL 名會從英文殘留換成中文，但大多是隱藏的 `*BodyArtHolder`，玩家幾乎看不到；不裝就維持現狀，沒有任何壞處。〔apoc2〕
- **apoc2 另外 334 欄換不換措辭**：這 334 欄只差譯法，例如「烬火炎矢→余烬之矢」。換的話，周目中途法術名會變，跟 Vokriinator／Ordinator 補丁、還有你記得的名字對不上；不換就維持現役譯法。報告建議不換，要換的話先看 `apoc2/review-both-chinese.json`。〔apoc2〕
- **NFF 繁中 esp 排到簡中上方**：排的話，Export 選項會從誤導人的 `[现在按你自己的意志自由活动，you are free]` 改成 `[從框架中移除]`，TC 層修好的兩個 key 也會生效；不排就維持 09-03 inst5 的安排。實機顯示 Vilja 已經被 NFF 匯入，所以她會看到的正是這句 Export 選項，這項和她直接相關。〔vilja §4.1〕
- **Cassia's Plea Remover 重複目錄**：這個目錄其實是主檔被裝了第二次（逐檔 md5 相同）。停用或改名標成「=主檔重複」都無害；不處理也無害。不必補下載 optional，用 C1 的 console 解就好。〔cassia〕
- **farm A：農舍 cell 名修正層**：裝的話，門口提示和室內地點名會從「Creation Club Cell」改成「金丘農園」；不裝就維持英文。〔farm〕
- **farm B：任何隨從都能當總管**（ESPFE）：裝的話，Vilja 這類自訂語音的隨從也能招成總管，但那句台詞會是無聲字幕；不裝的話只有 9 種原版語音的隨從能招，Vilja、Yvanni、Aniya、Sofia、Lydia 等人永遠看不到選項。〔farm〕
- **aniya 修正層**（ESL）：裝的話，就算米凱爾沒來 forcegreet，你也能自己找他點「米凯尔，求你别再纠缠安妮亚了。」；不裝就用 C6 的一行 `set`，效果一樣。〔aniya〕

## B. 進遊戲前（MO2／設定層）

<!-- wf-nav -->
- 開 MO2 之前，先確認 mo2close 線已經把 profile 還原並收線（見 E）。〔yvanni §5〕
- 裁了裝 apoc2：把 `~/skyrim_mods/_staging-2026-09-26/apoc2/Apocalypse-Magic-of-Skyrim-Simplified-Chinese-FULL-Completion-Combined-Dev-2026-09-26/` 放進 MO2 mods，排在 `Apocalypse-…-Combined-Dev-2026-09-25` **正上方**（第 251 行之上）。plugins.txt 不用動。〔apoc2〕
- 裁了 NFF 順序：把 `Nether's Follower Framework Traditional Chinese 2.8.6b Dev 2026-08-16` 排到 `NFF Simplified Chinese 113822 2.8.6b` 上方。〔vilja §4.1〕
- 裁了裝 farm A：`~/skyrim_mods/_staging-2026-09-26/farm/USCC-FarmingPatch-CellName-ZH-Fix-Dev-2026-09-26/`，優先權要高於 `Unofficial-SCC-Patches-ZH-ALL-2026-09-12`。〔farm〕
- 裁了裝 farm B：`~/skyrim_mods/_staging-2026-09-26/farm/FarmOverseerAnyFollower-Dev-2026-09-26/`，plugin 排在 `ccvsvsse004-beafarmer.esl` 之後。〔farm〕
- 裁了裝 aniya 層：`~/skyrim_mods/_staging-2026-09-26/aniya/Aniya-Favor5-MikaelFallback-2026-09-26/`，plugin 排在 `Aniya Follower.esp` 之後。〔aniya〕
- **NFF MCM 設定**（要進遊戲後，準星對著 Vilja）：System 頁的 `Import Enabled` 切成 No，就能擋掉她的 Import 選項；要全域關掉的話，改關 `Allow Import/Export Dialogue`。這是報告給的做法，保留下來；但實機顯示她已經在 ImportFac 裡，所以標**待驗**（詳見 C3）。〔vilja〕
  - NFF 有個上游 bug：用「Load Settings」讀回設定時，`Allow Import` 會變成 Steward 對話的值。所以關掉之後如果又冒出來，重新關一次就好。〔vilja §4.2〕
- **前綴**：
  - **2026-10-08 newsave build 後重算（新檔用這組）**：EMCompViljaSkyrim=`BB`、Katana=`A4`、nwsFollowerFramework=`6B`、Aniya Follower=`A3`、Yvanni Follower=`FE3C2`（light）、ccvsvsse004-beafarmer=`FE024`（light）、FDE Lydia=`FE360`（light）。ForgottenCity 已移除，C1 不再適用。這組是用 profiles `2cdbf1a` 的 loadorder 推算（`resolve_load_order.py`＋esplib `LoadOrder`），**還沒實機驗證**，進遊戲用 `help <名字>` 對一次。C 段指令裡的前綴仍是下面 Save229 的舊值，用在新檔時把前兩碼（light 是前五碼）換成這組。
  - Save229 當下（09-26，已過期）：實機驗證過 ForgottenCity=`A4`、EMCompViljaSkyrim=`D5`、Katana=`BC`、nwsFollowerFramework=`7B`、Aniya Follower=`BB`、Yvanni Follower=`FE3A7`（light）；推算 ccvsvsse004-beafarmer=`FE024`（light）。
  - 之後再改載入順序（裝／拔 plugin）就要重新用 `help` 對一次。

## C. 進遊戲後的 console 序列

讀 Save229。**只要步驟會改存檔，做完一律另存新檔，不要覆蓋 Save229。** 全文已拆到 [C-console.md](2026-09-26-pre-play-checklist/C-console.md)。各小節：

- C1. 卡西娅的信（兩封「卡西娅的请求」丟不掉）〔cassia〕
- C2. Katana／密格拉召喚沒反應〔katana〕
- C3. Vilja 的 NFF 選項〔vilja〕— **待驗，報告和實機矛盾**
- C4. 移除某個 ability〔forget〕
- C5. 金丘農園招總管〔farm〕
- C6. Aniya「說服米凱爾別再糾纏安妮亞」卡住〔aniya〕
- C7. Yvanni 不見了〔yvanni〕

## D. 遊戲內要用對話／MCM 做的事

對話與 MCM 步驟（D1 起）全文已拆到 [D-ingame.md](2026-09-26-pre-play-checklist/D-ingame.md)。

- D1 Katana／密格拉重招
- D2 Vilja
- D3 只是嫌 Active Effects 太雜
- D4 金丘農園招總管
- D5 Aniya 米凱爾
- D6 Yvanni

## E. 未解／下次派線

未解項與下次派線全文已拆到 [E-open.md](2026-09-26-pre-play-checklist/E-open.md)。

- profile 三檔漂移
- vilja 需要重派
- katana 待驗

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
