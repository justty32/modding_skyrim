# 交接書 — codex · A1：Nexus 在架狀態補值治具

上位計畫：`~/repo/moddings/skyrim/workflows/plans/round-2026-08-07-catalog-and-korean.md`
你的角色：**本輪的領導者**。你出治具與判準，deepseek（`pi --provider deepseek`）拿去跑大量迴圈，agy 負責網路採集。**三個 agent 之中只有你有 commit 權。**

## 你的 repo

`~/notes`（獨立 git repo，HEAD `71113be`）。本任務所有程式碼落在 `~/notes/projects/modding/skyrim/tools/`。
**不要碰 `~/repo/moddings/skyrim`**——那是 Claude 在管的母 repo。

## Done when

- [ ] `tools/fetch_nexus_status.py` 存在且 `--dry-run` 可跑
- [ ] 抽驗 SkyUI（mod id 12604）→ `nexus_status="live"`、`nexus_latest_version` 抓到最新 MAIN file 的版本（人工對照 https://www.nexusmods.com/skyrimspecialedition/mods/12604 應為 6.11）
- [ ] 抽驗一個已下架／隱藏的 mod → `nexus_status ∈ {gone, hidden}` 且 `never_delete=true`
- [ ] `--limit 20` 實跑一輪，Mongo 欄位確實寫進去，重跑第二次結果一致（冪等）
- [ ] commit 進 `~/notes`

## 環境

- **API key 在環境變數 `NEXUS_API_KEY`**（96 字元，使用者已寫進 `~/.zshrc`）。**絕對不要把 key 的值寫進任何檔案、log、commit message 或 print 出來。** 讀不到就報錯退出，不要 fallback 去抓 HTML。
- **mongod 是手動啟動的**，不是 systemd 那個：
  ```
  mongod --dbpath ~/data/mongodb --bind_ip 127.0.0.1 --port 27018 --logpath /tmp/mongod-manual.log --fork
  ```
  連線字串走環境變數 `SKYRIM_MONGO_URI`，預設 `mongodb://127.0.0.1:27018`。
  **mongod 沒開時要給明確錯誤 + 上面那行啟動指令，不要 timeout。**
- schema 文件：`~/notes/projects/modding/skyrim/docs/mongodb-schema.md`。**欄位已經佔位好了，你只要填值，不用改 schema。**
- 既有腳本可參考風格：`tools/scan_mod_library.py`、`tools/check_dll_runtime.py`。

## 規格

輸入是 `skyrim.mods` collection 裡 `grouping == "nexus_id"` 的文件（`_id` 是 mod id 的字串形式）。共 1,429 筆 `mods`，其中一部分是 `legacy:` 前綴的**要跳過**。

要填的欄位（`archives` 與 `mods` 都有，以 `mods` 為主，`archives` 由既有的 aggregate 流程帶）：

| 欄位 | 值 |
|---|---|
| `nexus_status` | `live` / `hidden` / `gone` / `unknown` |
| `nexus_name` | Nexus 上的正式名稱 |
| `nexus_latest_version` | 最新版本 |
| `nexus_requirements` | 相依需求 |
| `never_delete` | `nexus_status ∈ {gone, hidden}` 時設 `true` |
| `nexus_checked_at` | ISO 時間戳（供續跑判斷） |

### 狀態判定寫死成表——不留臨場解讀空間

Nexus 的 v1 API 端點是 `GET https://api.nexusmods.com/v1/games/skyrimspecialedition/mods/{id}.json`，header `apikey: <key>`。
**先自己打一發看實際回什麼**，再把下表對應到真實欄位（`status` / `available` 這類），不要照我的猜測寫死：

- 回 200 且該 mod 明確可公開取得 → `live`
- 回 404 → `gone`
- 回 200 但標示為隱藏／未發佈／作者下架 → `hidden`
- 其他（429、5xx、超時、欄位讀不出來）→ `unknown`

**鐵律：`unknown` 不得觸發任何清理判準。** 讀不出意圖一律視為保留——這是既有 `check_dll_runtime.py` 的 `judge()` 已經確立的原則（見 `docs/` 執行紀錄第 2 點），照抄。

`nexus_latest_version` 要取**最新 MAIN file 的版本**，不是 mod 自己的 version header——後者會落後（SkyUI 就是這個情況：header 6.9、最新檔 6.11）。這可能要另外打 `/mods/{id}/files.json`。

### 其他要件

- **可中斷續跑**：`nexus_checked_at` 在 N 天內（預設 7）的跳過。`--force` 可覆蓋。
- **控速**：讀 API 回應的 rate-limit header（`X-RL-Daily-Remaining` / `X-RL-Hourly-Remaining` 之類，以實際回的為準），剩餘量低就自己降速或停。預設請求間隔 ≥1s。429/5xx 走指數退避，連續失敗 N 次就**停下並印出續跑指令**，不要硬打。
- **寫入走 D2 的 `$set` / `$setOnInsert` 分離**（見 schema 文件 D2 節，那是 RimWorld 那次最貴的教訓）。
- `--dry-run`（只印不寫）、`--limit N`（抽驗）。
- 進度與失敗案例寫到 `~/notes/projects/modding/skyrim/logs/nexus-status-<date>.log`。

## 護欄

- **不刪任何檔案、不動 `~/skyrim_mods/` 下的任何東西。** 本任務純粹是查詢 + 寫 Mongo 欄位。
- 任何寫入 Mongo 之前，先用 pymongo dump 一份到 `~/notes/projects/modding/skyrim/backups/`（機器沒有 `mongodump`，照既有做法）。
- **不要 `git add -A`**——deepseek 會在 `/home/lorkhan/skyrim_agent_out/deepseek/`（repo 外）產草稿，但保險起見只 add 你自己改的檔案。
- 做完在 tmux 裡印一行 `A1 DONE` 讓我 capture 得到，然後停下等下一個任務（B1）。

## 完成後

回報：① 你實際打 API 看到的 status 欄位長怎樣（我要更新計畫文件）；② 抽驗兩個 mod 的結果；③ 你估這 1,400 筆跑完要多久、rate limit 會不會是瓶頸。
