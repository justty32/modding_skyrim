# 2026-11-02：POTC 研究歸層

範圍限定當日 Paths／POTC 調查與相關入站引用。公開原始碼研究正本在 [mod-survey finding](../../../../../analysis/mod-survey/findings/path-of-the-companions/README.md)，沒有改 skills-survival；私有成品維護放在 mod-library 包外家族入口，歷史執行與驗收證據保留原層。沒有功能、遊戲、資料庫或部署變更。

## 搬移與保留

六個跨 repo 研究檔案保留原檔名，映射見 [moves.tsv](moves.tsv)。因跨 repo 無法單次 git mv，先確認來源 commit 已推送，再 copy、核對公私分拆與保留內容，最後在來源 repo git rm；不是刪除研究。兩份原 REPORT 留作交接／執行紀錄，通用概述與普通裝備機制已由 finding 承接。

CLASSES 依角色政策、ABI／save、Skald 拆成三份語意子檔，原檔保留入口及原標題錨點；四個移出段落逐字保留。16 列 ability-map 逐 byte 一致。私有詳細對帳保留在 agentctl 本輪執行證據，公開報告不複製其內容。

## 固定驗證

獨立 review 已核公開內容可見性、原意與技術限制；當次驗收原話及 31 件歷史原件 hash 不變，兩個 sealed 成品包 diff 為 0。搬移連結工具 dry-run 為 0 變更，六個舊研究檔的活 Markdown 入站為 0；本次 Markdown／資料連結及大清單檢查通過。

全庫 checker 搬前 5810 檔、搬後 5817 檔，兩次均為同七條既存 missing-file links，新增 0；之後新增的整理紀錄另以本次檔案檢查涵蓋。67 個母 repo 文件工具測試通過：沿用相同工具的 LF hook 副本處理 checkout 換行，從母 repo Git context 執行，原工具與 hook 未改。既有無關斷鏈不在本輪擴修範圍。

知識導航由 findings 與技能樹索引進入；狀態導航只指向正本，不再把完整研究留在 handoff。本次跨 repo tidy 完成後清除母 repo SESSION open；未新增 WAIT_USER。
