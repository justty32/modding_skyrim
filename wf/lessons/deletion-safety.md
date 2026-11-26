# 刪除前的檢查：入站連結與家目錄級刪除

[lessons 索引](README.md)｜ignore 狀態、staging 腳本與重建設定見 [artifact-hygiene-and-ignores](artifact-hygiene-and-ignores.md)

## scan-inbound-links-before-delete

> 刪除前要查的不只是「這檔重不重要」，還有「誰依賴它」——清單產生時就掃活文件的入站連結，正確順序是「刪之前就知道誰會斷」，不是「先刪再發現」。

連結檢查的綠燈蓋的是「磁碟上有」，不是「版控裡有」：歷史 REPORT 連著自己產的截圖／log／work 目錄，這些檔「未追蹤但還在磁碟」時全綠，一刪就紅（2026-10-23）。把歷史區排除出掃描不是解法，那會讓下次大刪除完全無聲。

**How to apply**：產刪除清單的工具要內建入站連結掃描（tracked md 全掃、連結解析到 repo 相對路徑、與候選集取交集），命中的另列 `linked-review.tsv` 不自動列刪；處置二選一：排除該檔，或刪除批次裡同時帶上連結改寫。已斷的連結用 `annotate_dead_links.py` 批次改成不可點擊註記（「原路徑＋移除日期＋不可復原」）。工具：`agentctl/handoffs/home-2026-10-23/tidy/T1/tools/build_candidates.py` 的 `inbound_refs()`，同目錄 `annotate_dead_links.py`。

「已結案但被連結釘住」不是不能刪的理由（2026-10-23 使用者裁示「都可以清掉的」），但要先分辨連過來的是什麼：**純歷史文件**連過來 → 連結改純文字；**open 項**連過來 → 先把它要用的結論吸收進活文件，再刪、連結改純文字（過時即刪，[STRUCTURE](../STRUCTURE.md) local 段）。點名的 open 項要實查狀態，可能早就 `done`。

## home-dir-cleanup-safety

> 家目錄級刪除不可逆（ext4 無快照、quarantine.py 已不能用）；盤點時算的雜湊在執行瞬間要重驗，不能用舊快照直接刪。

判準（2026-10-17 確認沿用）：已解壓且已裝進 MO2 的 `_staging` 可刪；`_dl-*`、含 backup/rollback 字樣的留。做法：逐路徑 dry-run（不用萬用字元）、刪前查 MO2／housecarl-mirror 有無 symlink 指向、大型輸出要逐檔 byte 比對 MO2 內副本才判定可刪（2026-08-06 曾因誤刪永久丟失檔案）。

**Why:** 磁碟級刪除沒有救援路徑；舊雜湊／舊快照在執行當下可能已經不準。

**How to apply:** dry-run 清單＋閘門檢查寫進執行腳本本身、逐路徑不用萬用字元，使用者面板確認後才真刪。來源：`agentctl/handoffs/home-skyrim-cleanup-2026-10-17/REPORT.md`。相關：[[list-scripts-before-deleting-staging]]、[[ignored-is-not-a-deletion-policy]]
