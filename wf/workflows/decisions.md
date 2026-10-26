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
| 2026-10-26 | houseCARL fork 的 `main` 與 `fix/dialogue-encoding-lint` 一起 fast-forward 到 CJK 名稱修補＋wf 導入（`f0148dc8`），主 checkout 仍在 `fix/dialogue-encoding-lint`；部署 build 跟著換。取代 10-23「刻意停在 `fix/dialogue-encoding-lint`、不動」 | 使用者 2026-10-26 拍板「快轉兩分支＋換 build」；施工見 `agentctl/handoffs/home-2026-10-26/hcdeploy/REPORT.md` | 只 ff、不 merge／force；兩分支分岔時再裁 |
