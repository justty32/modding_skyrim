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
| 2026-10-23 | `projects/houseCARL` **刻意停在分支 `fix/dialogue-encoding-lint`**（使用者原話「不管，就我們自己留着就好」）。這不是待辦，巡檢不要再把它列成異常 | 使用者 2026-10-23 裁示；T3 的 6a（本地 main FF 到 fork/main）、6b（刪同點分支名）、6c（linux-record-names 併 fork/main）全部不做 | 若 houseCARL 要升版或 fork/main 大幅前進，再回頭看 `agentctl/handoffs/home-2026-10-23/tidy/T3/REPORT.md` 的方案比較 |
