# 手上已經有檔案、但不知道是什麼

[nexus-intake 主線](README.md)｜第 1 階段「查證」的分支。

從檔案內容反查，不要從檔名猜：單檔用 `housecarl_nexus_identify`（吃 MD5，無金鑰），
回 mod（id／名稱／作者／status）與 file_details（上游檔名／版本／分類），
**是比檔名可信得多的來源**。整庫批次跑用
`mod-library/db/` 的 **legacy MD5 回溯解析器**（見該目錄的 [`README.md`](../../../mod-library/db/README.md)）。

**坑**：`Light and Shade SE-77993-2-2-....7z` 的檔名寫著 77993，md5 指向的卻是
**82876**（簡中翻譯頁）。任何「用 regex 從檔名撈 id」的做法都要當成猜測看待。

查不到（404）只代表 Nexus 不認得這個 md5——對岸站台來的、或被解壓重打包過的都會 miss，
**不是檔案有問題**。實測 174 個舊命名檔只有 28 個 hit。

MD5 反查是唯讀，不改帳號狀態，不在[硬性紅線](README.md#硬性紅線碰到就停發-needs-user)內。
