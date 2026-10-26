# decisions — 決策記錄（定了什麼、前提是什麼）

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

留下「定了什麼」：git log 找得回改了什麼，找不回**當時定下的規則與它成立的前提**。只記結論、前提與使用者原文；比較過的方案與 AI 寫的理由不記（[tidy 內容精簡](tidy/content-trim.md)），要查靠 git 歷史。

**何時用**：在兩個以上可行方案裡選一個，且日後可能被問「當初定的是什麼、還成立嗎」。
**何時不用**：只有一條路，或隨時可回頭的小事；需要先查清事實時走 [investigation](investigation/README.md)，結論再落到這裡。

## Done when

- 下表新增一列，且「決定」「前提」兩欄非空。

## 記錄（新的在上）

| 日期 | 決定 | 來源（使用者原文或誰定的）| 前提（變了就重看）|
|------|------|-------------------------|-----------------|
| 2026-10-26 | Tomebound、Spellforge、Dragons Keep **不裝**：modlist 改 `-`，mod 目錄保留（profiles `6784720`） | 使用者 2026-10-26 裁示；施工 `agentctl/handoffs/home-2026-10-26/decide1026/REPORT.md` | 想重裝其中任一件時另開評估線（法術覆寫順序、槽位、中文層） |
| 2026-10-26 | OBody 黑名單收齊所有 Kurone7 私有身體隨從：Aniya、Melana 補進 `OBody-PrivateBody-Blacklist-2026-10-04` | 使用者 2026-10-26 裁示；同上 | 有人換成帶 `.tri`／要 OBody 形變的身體時重看 |
| 2026-10-26 | Varinia 永遠是 Coco 的頭髮、不戴假髮：新層 `Varinia-NoWig-Scripts-Dev-2026-10-26` 只拿掉換裝腳本裡「發假髮／戴假髮」兩類行（換衣服照舊），接受偽裝劇情的假髮失效 | 使用者 2026-10-26 裁示；同上 | Varinia 本體更新（pex 換版）要重做這層 |
| 2026-10-26 | Remiel 兩件怪事（placeatme 複本消失、來源不明的「Done Writing」框）**不追** | 使用者 2026-10-26 裁示；出處 `agentctl/handoffs/home-2026-10-26/remiel/REPORT.md` §6 | 正常遊玩再出現時重看 |
| 2026-10-26 | model-converter `wf-import` 分支等下次 DSPort 重釘 converter pin 時一起 ff 回 main，同批跑 converter contract 測試 | 使用者 2026-10-26 裁示；出處 `agentctl/handoffs/home-2026-10-26/tidyall/squad/REPORT.md` | DSPort 不再釘 converter 時改成單獨併 |
| 2026-10-26 | ESL：現役存檔期間不再轉；新周目開檔前做 T1x＋T2（31 支），T3 交 ESLifier 前先做 Linux PoC | 使用者 2026-10-26 裁示；出處 `agentctl/handoffs/home-2026-10-26/shell-esl/REPORT.md` 選項 C／D | 開新周目即觸發；full 槽逼近 254 時提前重看 |
| 2026-10-26 | houseCARL fork 的 `main` 與 `fix/dialogue-encoding-lint` 一起 fast-forward 到 CJK 名稱修補＋wf 導入（`f0148dc8`），主 checkout 仍在 `fix/dialogue-encoding-lint`；部署 build 跟著換。取代 10-23「刻意停在 `fix/dialogue-encoding-lint`、不動」 | 使用者 2026-10-26 拍板「快轉兩分支＋換 build」；施工見 `agentctl/handoffs/home-2026-10-26/hcdeploy/REPORT.md` | 只 ff、不 merge／force；兩分支分岔時再裁 |
