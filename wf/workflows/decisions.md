# decisions — 決策記錄（定了什麼、前提是什麼）

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

留下「定了什麼」：git log 找得回改了什麼，找不回**當時定下的規則與它成立的前提**。只記結論、前提與使用者原文；比較過的方案與 AI 寫的理由不記（[tidy 內容精簡](tidy/content-trim.md)），要查靠 git 歷史。

**何時用**：在兩個以上可行方案裡選一個，且日後可能被問「當初定的是什麼、還成立嗎」。
**何時不用**：只有一條路，或隨時可回頭的小事；需要先查清事實時走 [investigation](investigation/README.md)，結論再落到這裡。

## Done when

- [decisions.json](decisions.json) 新增一列（放最前），且 `decision`、`premise` 兩欄非空。

## 記錄（新的在上）

已抽到 [decisions.json](decisions.json)（11 列，新的在前），md 不留表的副本。欄位：

- `date`：日期
- `decision`：決定
- `source`：來源（使用者原文或誰定的）
- `premise`：前提（變了就重看）

統計：11 列（2026-11-22 一列、2026-11-05 三列、2026-10-26 七列）；查法見工作流的資料檔說明。
