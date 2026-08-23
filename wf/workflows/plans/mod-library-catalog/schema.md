# schema 草案

> 屬於 [mod 下載庫建檔與清理（MongoDB）](README.md)。

## 三、schema 草案

沿用 RimWorld 的欄位風格（`_id` 小寫化主鍵、`_raw_extra` 收未對應資料、養成欄位可為 null 表「未調查」）。

### `skyrim.archives`（一壓縮檔一筆）

| 欄位 | 型別 | 類別 | 說明 |
|---|---|---|---|
| `_id` | string | 磁碟 | 檔案 sha256 |
| `paths` | string[] | 磁碟 | 所有出現位置（>1 即 L1 重複） |
| `filename` | string | 磁碟 | 主要檔名 |
| `size` | int | 磁碟 | bytes |
| `format` | enum | 磁碟 | `zip`\|`7z`\|`rar` |
| `mtime` | float | 磁碟 | |
| `nexus_mod_id` | int\|null | 磁碟 | 從檔名解析 |
| `version_parsed` | string\|null | 磁碟 | 從檔名解析 |
| `naming_pattern` | enum | 磁碟 | `nexus_classic`\|`nexus_app`\|`legacy`\|`manual` |
| `has_fomod` / `has_skse_dll` / `has_bsa` / `has_esp` | bool | 磁碟 | 由目錄表判定 |
| `plugin_names` | string[] | 磁碟 | 內含 esp/esm/esl |
| `dll_names` | string[] | 磁碟 | |
| `top_level_shape` | enum | 磁碟 | `data_wrapped`\|`numbered_folders`\|`bare_data`\|`other` |
| `is_translation` | bool | 磁碟 | 檔名標記 + 內容判定 |
| `dll_compat` | object[]\|null | 養成 | 每個 dll：`{name, plugin_name, version, addr_lib: bool, locked_runtimes: []}` |
| `runtime_ok_1_6_1170` | bool\|null | 養成 | L3 的判準欄位；null=未檢查 |
| `nexus_status` | enum\|null | 養成 | `live`\|`hidden`\|`gone`\|`unknown` |
| `nexus_name` / `nexus_latest_version` / `nexus_requirements` | | 養成 | 由 `housecarl_nexus_mod` 補 |
| `never_delete` | bool | 養成 | D5 的保險栓 |
| `cleanup_tier` | enum\|null | 養成 | `L1`\|`L2`\|`L3`\|`L4`\|`keep` |
| `cleanup_decision` | enum\|null | 養成 | `pending`\|`approved`\|`rejected` |
| `quarantined_at` / `quarantine_reason` / `original_path` | | 養成 | D5 的移動記錄 |
| `translates_mod_id` | int\|null | 養成 | 漢化包指向的本體（附錄 B） |
| `installed_as` | string\|null | 養成 | 對應到 MO2 `mods/` 的哪個資料夾 |
| `_raw_extra` | object\|null | | |

### `skyrim.mods`（一 Nexus mod 一筆，聚合）

`_id` = `nexus_mod_id`（無法解析者用 `legacy:<正規化檔名>`）。欄位：`name`、`archive_ids[]`、`versions[]`、`latest_local_version`、`nexus_latest_version`、`is_installed`、`installed_version`、`grouping`（`nexus_id`\|`filename_heuristic`）、`translation_archive_ids[]`、`category`、`summary_zh`、`user_note`。

索引：`archives` 的 `nexus_mod_id` / `cleanup_tier` / `is_translation` / `runtime_ok_1_6_1170` / `never_delete`，`filename` 文字索引；`mods` 的 `is_installed` / `grouping`。
