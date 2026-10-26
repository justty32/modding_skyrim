# schema 草案（**已被取代，不要照這份實作**）

> **2026-08-31 降級。** 這是實作前草案，與現行 schema 已對不上：它列了不存在的
> `has_esp`、不存在的 `manual` naming_pattern、不存在的 `latest_local_version`，
> `nexus_*` 還寫「由 `housecarl_nexus_mod` 補」（實際走 Nexus v1 API，見
> `mod-library/db/fetch_nexus_status.py`）。
> **現行唯一 schema 權威是 `mod-library/db/mongodb-schema.md`。**
> 本檔保留是為了看得到當初的設計意圖，不是為了照著做。

> 屬於 [mod 下載庫建檔與清理（MongoDB）](README.md)。

## 三、schema 草案

沿用 RimWorld 的欄位風格（`_id` 小寫化主鍵、`_raw_extra` 收未對應資料、養成欄位可為 null 表「未調查」）。

### `skyrim.archives`（一壓縮檔一筆）

保留已被取代的 skyrim.archives 草案欄位及設計意圖。

已抽到 [schema-archive-fields.json](schema-archive-fields.json)（25 列）。

欄位：原草案的欄位名稱。

型別：原草案的資料型別。

類別：磁碟或養成分類，未分類者留空。

說明：欄位用途及原備註。

統計：25 筆欄位記錄；磁碟 14 筆、養成 10 筆、未分類 1 筆。

### `skyrim.mods`（一 Nexus mod 一筆，聚合）

`_id` = `nexus_mod_id`（無法解析者用 `legacy:<正規化檔名>`）。欄位：`name`、`archive_ids[]`、`versions[]`、`latest_local_version`、`nexus_latest_version`、`is_installed`、`installed_version`、`grouping`（`nexus_id`\|`filename_heuristic`）、`translation_archive_ids[]`、`category`、`summary_zh`、`user_note`。

索引：`archives` 的 `nexus_mod_id` / `cleanup_tier` / `is_translation` / `runtime_ok_1_6_1170` / `never_delete`，`filename` 文字索引；`mods` 的 `is_installed` / `grouping`。
