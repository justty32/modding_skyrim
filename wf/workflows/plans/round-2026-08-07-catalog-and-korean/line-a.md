# 線 A：mod 庫收尾

> 屬於 [本輪三 agent 分工——mod 庫收尾 + 韓文站採集](README.md)。

## 線 A：mod 庫收尾（codex 領導 → deepseek 執行）

### Done when

- [x] `mods` 裡每筆有真 `nexus_mod_id` 的都有 `nexus_status`（`live`/`hidden`/`gone`/`unknown`）與 `nexus_latest_version`
- [x] `nexus_status ∈ {gone, hidden}` 的一律 `never_delete=true`（D5 保險栓）
- [x] 清理報告產生器可重跑、兩次結果一致，L2 三條例外有測到（2026-08-11 重驗：`--self-test` 13/13 PASS；實庫唯讀 `--verify` 6/6 PASS）
- [x] 每次寫入前自動 pymongo dump（P1.7）
- [x] 漢化包能回答「這個漢化包對應哪個本體、版本差多少」（2026-08-07 A4-review：280 筆中 259 high 寫回 `archives.translates_mod_id`，9 low + 12 none 留人工）

### A1（codex）：Nexus 補值治具

寫 Nexus 狀態富化工具（當時落點是 `~/notes/projects/modding/skyrim/tools/`，2026-08-23 統整後在 `mod-library/db/`）。要件：

- 輸入是 `mods` collection 裡 `grouping="nexus_id"` 的 `_id`（≈1,429 筆的子集）
- **可中斷續跑**：已有 `nexus_checked_at` 且在 N 天內的跳過
- **控速**：預設 ≥1s/req + 指數退避；429/5xx 要停而不是硬打
- **狀態判定寫死成表**，不留 deepseek 臨場解讀空間：Nexus v1 API `status="published"` + `available=true` → `live`；404 → `gone`；`available=false` 或 `status` 為 `removed` / `wastebinned` 等下架狀態 → `hidden`；其餘 → `unknown`（**`unknown` 不得觸發任何清理**）
- 最新版另打 `/files.json`，取 `category_name="MAIN"` + `category_id=1` + `is_primary=true` 的最新 MAIN file 版本；mod header 的 `version` 會落後（SkyUI 12604：6.9 vs 6.11）
- `--dry-run` 只印不寫；`--limit N` 供抽驗
- 寫入走 D2 的 `$set`／`$setOnInsert` 分離
- **驗收條件**：抽一個已知下架/隱藏 mod 判成 `gone`/`hidden` 且 `never_delete=true`；抽 SkyUI（12604）判成 `live` 且 `nexus_latest_version="6.11"`

### A2（deepseek）：跑補值

以 `--all` 背景長跑。deepseek 的職責只有三件：跑、看 log、把「腳本掛掉／狀態判不出來」的案例整理成清單交回 codex。**不准自己改腳本**，遇到 bug 回報 codex。

環境：`SKYRIM_MONGO_URI=mongodb://127.0.0.1:27018`，mongod 要先手動起：
`mongod --dbpath ~/data/mongodb --bind_ip 127.0.0.1 --port 27018 --logpath /tmp/mongod-manual.log --fork`

### A3（codex）：清理報告產生器（P1.5）+ 備份（P1.7）

清理分級工具——四級分類 + L2 三條例外，報告可重跑。任何寫入前先 pymongo dump 到 `backups/`。
L2 這一級**必須等 A2 跑完**才產得出來（判準依賴在架狀態）。

### A4（deepseek）：漢化包盤點（附錄 B 的資料層）

對 `is_translation=true` 的檔案填 `translates_mod_id`，並產出版本差異矩陣。方法：

1. 檔名去掉 `- CHS`/`- CHT`/`(Chinese Translation)`/`漢化` 等標記後，比對 `mods` 的名稱與 id
2. 對不上的，解壓列表看 plugin basename 是否命中某個本體
3. **命中不了就留 `null`**，不要猜

產出 `docs/translation-matrix.md`：一列一個漢化包，欄位是「本體 mod、漢化版本、本體庫內最新版、本體 Nexus 最新版、版本落差」。
**本輪到此為止**——實際 forward 譯文欄位需要 houseCARL，本輪不做。

---
