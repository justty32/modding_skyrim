# 分階段任務 P0–P4

> 屬於 [第三方 mod 取得–安裝–驗證流水線](README.md)。

## 四、分階段任務

### P0 — 前置（**2026-08-04 執行完畢，除 0.2 前半受阻**）

git repo 落在 `<MO2 instance>/profiles/`（不是 instance 根目錄——那會把 `mods/` 的 GB 級內容拉進版控範圍，`.gitignore` 出錯的代價太高）。三個 commit：`a636b86` 基線 → `57a7097` 清 stale → `317508d` AgentBridge/QA。

| # | 任務 | 狀態 |
|---|---|---|
| 0.1 | 清掉 `loadorder.txt` 那 3 條 stale CC 條目 | ✅ 已清，plugin 56→53 且 53 個全部 resolve 成功，houseCARL 警告歸零 |
| 0.2 | `housecarl_set_mo2_instance` 指向 MO2 instance | ⛔ **受阻——houseCARL 的 Linux 路徑 bug**：它把 `ModOrganizer.ini` 的 `gamePath` 當字面路徑，沒把 Wine 的 `Z:\` 翻回 Linux，接上 `/Data` 就壞。已記入 `WAIT_USER.md`。**影響有限**：explicit-paths mode 全程可用，只失去 `load_order_status(profile=...)` 的跨 profile 比對 |
| 0.2b | `housecarl_set_tool_path` 補 `papyrus_logs` / `crash_logs` | ✅ 都設好。`papyrus_logs` = prefix 內 `Logs/Script`（有 `Papyrus.0-3.log`）；`crash_logs` = `SKSE/` 本身——CrashLogger 是把 `crash-<時間>.log` **平放在 SKSE 資料夾**，沒有 `Crash Logs` 子目錄。**現存 20 份，最新 2026-08-02**，G5 的 triage 一開始就有真實素材 |
| 0.3 | 開 QA profile | ✅ `profiles/QA`，與 `Default` **只差 AgentBridge 那一行**，其餘檔案 byte-identical。`LocalSaves`/`LocalSettings` 維持 false 與 Default 一致——開它們能得到真正的存檔/ini 隔離，但會讓 `qa_runner` 的 baseline 複製路徑失效，該另外刻意做而不是當副作用 |
| 0.4 | git init + 基線 commit | ✅ `.gitattributes` 設 `* -text`，實測 index 內 CRLF 原樣保留；`.mo2ctl-backups/` 與 `*.bak-*` 排除。12 檔 358 行 |
| 0.5 | AgentBridge 移出正式 profile | ✅ `Default` 停用（109→108 enabled）、`QA` 啟用 |
| 0.3 | 開 QA profile（複製 `Default`），`MO2_PROFILE` 指過去。注意 `mods/` 是 profile 共用的——隔離的是啟用狀態，不是檔案 |
| 0.4 | **git init + commit 現狀為 `main`**（原列 P2.1，2026-08-04 重審上移）。P1 要拿真實第三方 mod 測試，若那時還沒有 `main` 可回滾，第一次紅燈就沒有救援路徑——這是順序錯誤，不是排程偏好 |
| 0.5 | `AgentBridge` 改為 **QA profile 啟用、`Default` 停用**（現況見附錄 G8） |

### P1 — archive + FOMOD 解析層（**優先，整條斷在這裡**）

| # | 任務 | 驗證 |
|---|---|---|
| 1.1 | `.zip` 解壓（stdlib `zipfile`），含 zip-slip 路徑檢查；`.7z`/`.rar` 偵測外部工具或 handoff | 一個無 FOMOD 的第三方 zip 能裝進 MO2 並被引擎載入（`/state?include=plugins`） |
| 1.2 | `fomod/ModuleConfig.xml` 解析：step / group / plugin / 依賴條件 → 可讀摘要 | 對一個真實 FOMOD mod 印出的選項樹與 MO2 GUI 顯示一致 |
| 1.3 | `fomod_choices` 宣告式選項 → materialize 檔案；`fomod/info.xml` → `meta.ini` | 同一份 spec 重跑兩次產出的 mod 資料夾 byte-identical |
| 1.4 | 「手動多資料夾」型（`00 Core` 那種）共用 1.3 的機制 | 一個此型 mod 裝對 |

### P2 — modlist git 治具

| # | 任務 | 驗證 |
|---|---|---|
| 2.1 | 就地 `git init` + `.gitattributes`（`* -text`）+ `.gitignore`（排除 `mods/`、快取、log） | commit 後 `git diff` 對未改動的檔案為空（證明沒被 eol normalize） |
| 2.2 | `manifest.json` schema 與寫入（mod 名 / 來源 / 版本 / sha256 / `fomod_choices`） | 從 manifest 能重放一次安裝，結果與原次一致 |
| 2.3 | `try/` 分支開關收束的治具指令，內建 `require_writable()` 互斥 | 紅燈情境：砍分支 + checkout main → MO2 重啟後 profile 三檔與安裝前 byte-identical |

### P3 — 排序與靜態關卡

| # | 任務 | 驗證 |
|---|---|---|
| 3.1 | 插入式排序：依 mod 頁自述 + conflict tree 決定落點 | 新 mod 的 plugin index 落在預期位置，既有 109 個相對順序不變 |
| 3.2 | 靜態關卡串成一步，出 pass/fail 報告 | 對故意缺 master 的 mod 能紅燈攔下、且不必啟動遊戲 |

### P4 — 端到端

| # | 任務 | 驗證 |
|---|---|---|
| 4.1 | 挑一個真實第三方 zip mod 走完全程，產出 `qa.json`（到達地點 + 穿上裝備） | 報告全綠 + 一則視覺 handoff；`main` 上留下可回滾 commit |
