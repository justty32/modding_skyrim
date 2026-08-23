# 設計決策 D1–D3

> 屬於 [mod 下載庫建檔與清理（MongoDB）](README.md)。

## 二、已定案的設計決策

### D1：文件單位是「壓縮檔」，`_id` 用 sha256

RimWorld 用 `About.xml` 的 `packageId` 當主鍵，**Skyrim 壓縮檔沒有 manifest**，沒有等價物。

因此：`archives` collection 一檔一筆，`_id` = 檔案 sha256。理由是 sha256 同時解決三件事——身分、**bit-identical 重複自動浮現**（根目錄那 25 個直接落出來）、以及重跑時判斷檔案有沒有變。

第二層 `mods` collection 以 `nexus_mod_id` 聚合，回答「這個 mod 我有幾個版本」。無法解析出 mod id 的（舊式命名）落在 `mod_id: null`，靠檔名 fuzzy 分組並標記 `grouping: "filename_heuristic"`——**明確標記可信度，不假裝解析成功**（RimWorld 教訓 3 的同型問題：衍生數字要能看出可不可信）。

### D2：`$set` / `$setOnInsert` 分離，抄 RimWorld 最貴的那次教訓

RimWorld 的 `extract_mod_metadata.py` 原本 `drop_collection` + `insert_many`，每次重掃把 LLM 分類、中文摘要、爬蟲結果四個「養成」欄位清成 `None`，且沒備份。1,481 筆的重建成本極高。

本計畫從第一版就分兩類欄位：

- **磁碟事實**（路徑、大小、sha256、內容旗標、解析出的 mod id/版本）→ `$set`，重掃覆寫。
- **養成資料**（Nexus 查回的名稱/需求/是否仍在架、人工判定、清理決策、漢化對應、韓文站採集結果、使用者的審核意見）→ `$setOnInsert`，重掃**絕不動**。

### D3：內容旗標靠「列表」而非「解壓」，DLL 才解

1,693 個檔全解會炸掉時間與空間。`7z l` / `unar -l` 只讀目錄表，秒級。從檔名列表就能定出：`has_fomod`、`has_skse_dll`、`has_bsa`、`has_esp`、`plugin_names[]`、`is_translation`（檔名 + 內容雙判）、`top_level_shape`（Data/ 包裹、數字前綴資料夾、裸 Data 內容）。

**只有含 `.dll` 的才實際解出那些 dll**（到暫存區）做 runtime 檢查，用完即刪。
