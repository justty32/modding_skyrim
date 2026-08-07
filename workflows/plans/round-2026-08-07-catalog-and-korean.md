# plan：本輪三 agent 分工——mod 庫收尾 + 韓文站採集

出計畫日期 2026-08-07。上游計畫：[mod-library-catalog.md](mod-library-catalog.md)（本輪做它的 P1.4、P1.5 與附錄 A、附錄 B）。
前一輪的三 agent 並行記錄見 `SESSION-LOG.md` 與 commit `dcd385b`。

**本輪不碰**：`projects/darksouls-port`、`projects/houseCARL`（使用者 2026-08-07 決定先放著）。

## 角色與鐵律

| agent | 角色 | 做什麼 | 不做什麼 |
|---|---|---|---|
| **codex** | 領導 | 出 schema／判準／治具骨架、review deepseek 與 agy 的產出、**唯一有 commit 權** | 不跑大量迴圈（那是 deepseek 的活） |
| **deepseek** | 執行 | 跑 codex 寫好的腳本、大量 API／解析迴圈、填 Mongo 欄位 | **不寫治具、不 commit、不 `git add`** |
| **agy** | 網路搜尋與採集 | 韓文站公開板搜尋、抓截圖／簡介／原始連結、翻譯簡介 | **不做事實判斷、不寫 Mongo、不 commit** |

**index.lock 鐵律**：只有 codex 碰 git。deepseek 寫 MongoDB 與 `~/notes/projects/modding/skyrim/logs/`，agy 寫 `~/skyrim_mods/.candidates/`（非版控）。三者落點互斥。

**幻覺隔離**（agy 專用）：原始連結、截圖檔、頁面 HTML **必須是機器抓下來的原物**，agy 只被允許在「已抓到的原文」上做翻譯與摘要。任何 agy 自己「記得」的 mod 名稱、作者、連結一律不採信——收斂時 codex 以「原始檔案是否存在」為準，不以 agy 的敘述為準。

**驅動方式**：tmux `send-keys` + `capture-pane`（不是 stdin 注入；`dev.tty.legacy_tiocsti=0` 讓後者做不到）。每個 agent 一個獨立 tmux session。

---

## 線 A：mod 庫收尾（codex 領導 → deepseek 執行）

### Done when

- [x] `mods` 裡每筆有真 `nexus_mod_id` 的都有 `nexus_status`（`live`/`hidden`/`gone`/`unknown`）與 `nexus_latest_version`
- [x] `nexus_status ∈ {gone, hidden}` 的一律 `never_delete=true`（D5 保險栓）
- [ ] 清理報告產生器可重跑、兩次結果一致，L2 三條例外有測到
- [x] 每次寫入前自動 pymongo dump（P1.7）
- [x] 漢化包能回答「這個漢化包對應哪個本體、版本差多少」（2026-08-07 A4-review：280 筆中 259 high 寫回 `archives.translates_mod_id`，9 low + 12 none 留人工）

### A1（codex）：Nexus 補值治具

寫 `~/notes/projects/modding/skyrim/tools/fetch_nexus_status.py`。要件：

- 輸入是 `mods` collection 裡 `grouping="nexus_id"` 的 `_id`（≈1,429 筆的子集）
- **可中斷續跑**：已有 `nexus_checked_at` 且在 N 天內的跳過
- **控速**：預設 ≥1s/req + 指數退避；429/5xx 要停而不是硬打
- **狀態判定寫死成表**，不留 deepseek 臨場解讀空間：Nexus v1 API `status="published"` + `available=true` → `live`；404 → `gone`；`available=false` 或 `status` 為 `removed` / `wastebinned` 等下架狀態 → `hidden`；其餘 → `unknown`（**`unknown` 不得觸發任何清理**）
- 最新版另打 `/files.json`，取 `category_name="MAIN"` + `category_id=1` + `is_primary=true` 的最新 MAIN file 版本；mod header 的 `version` 會落後（SkyUI 12604：6.9 vs 6.11）
- `--dry-run` 只印不寫；`--limit N` 供抽驗
- 寫入走 D2 的 `$set`／`$setOnInsert` 分離
- **驗收條件**：抽一個已知下架/隱藏 mod 判成 `gone`/`hidden` 且 `never_delete=true`；抽 SkyUI（12604）判成 `live` 且 `nexus_latest_version="6.11"`

### A2（deepseek）：跑補值

`python3 tools/fetch_nexus_status.py --all`，背景長跑。deepseek 的職責只有三件：跑、看 log、把「腳本掛掉／狀態判不出來」的案例整理成清單交回 codex。**不准自己改腳本**，遇到 bug 回報 codex。

環境：`SKYRIM_MONGO_URI=mongodb://127.0.0.1:27018`，mongod 要先手動起：
`mongod --dbpath ~/data/mongodb --bind_ip 127.0.0.1 --port 27018 --logpath /tmp/mongod-manual.log --fork`

### A3（codex）：清理報告產生器（P1.5）+ 備份（P1.7）

`tools/cleanup_report.py`——四級分類 + L2 三條例外，報告可重跑。任何寫入前先 pymongo dump 到 `backups/`。
L2 這一級**必須等 A2 跑完**才產得出來（判準依賴在架狀態）。

### A4（deepseek）：漢化包盤點（附錄 B 的資料層）

對 `is_translation=true` 的檔案填 `translates_mod_id`，並產出版本差異矩陣。方法：

1. 檔名去掉 `- CHS`/`- CHT`/`(Chinese Translation)`/`漢化` 等標記後，比對 `mods` 的名稱與 id
2. 對不上的，解壓列表看 plugin basename 是否命中某個本體
3. **命中不了就留 `null`**，不要猜

產出 `docs/translation-matrix.md`：一列一個漢化包，欄位是「本體 mod、漢化版本、本體庫內最新版、本體 Nexus 最新版、版本落差」。
**本輪到此為止**——實際 forward 譯文欄位需要 houseCARL，本輪不做。

---

## 線 B：韓文站採集（codex 出治具 → agy 採集 → codex 收斂）

承 [mod-library-catalog.md 附錄 A](mod-library-catalog.md)。

### Done when

- [x] `candidates` collection 存在，schema 有否決狀態欄位（被否決過的不再出現在審閱清單）（2026-08-07 B1：schema + ingest/check/gallery 工具落地）
- [ ] 至少一輪採集落地：截圖 + 翻譯後簡介 + 原始連結 + 連結存活狀態
- [x] 本機 HTML 圖庫可開，使用者能在上面逐筆過目（2026-08-07 B1：`build_gallery.py` 已用暫存 DB fixture 驗證）
- [ ] 地圖 porting 類的候選回饋到 `analysis/port-source-survey/`

### B1（codex）：`candidates` schema + 治具

- schema 加進 `docs/mongodb-schema.md`。關鍵欄位：`_id`（來源 URL 的 hash）、`source_site`、`source_url`、`title_ko`、`title_zh`、`summary_zh`、`category`（人物美化／獨立隨從／武器裝備／地圖 porting／其他）、`screenshots[]`（本機相對路徑）、`link_status`、`link_checked_at`、**`review_state`（`pending`/`approved`/`rejected`）+ `rejected_at`**
- `tools/ingest_candidates.py`：吃 agy 產在 `~/skyrim_mods/.candidates/<batch>/` 的原始檔（每筆一個資料夾：`page.html` + `shots/*.jpg` + `meta.json`）→ upsert 進 Mongo。**已是 `rejected` 的 `_id` 直接跳過**
- `tools/check_links.py`：HEAD 請求填 `link_status` / `link_checked_at`
- `tools/build_gallery.py`：出本機 HTML 圖庫（照本 repo 既有 `html-guide` 工作流形狀）

### B2（agy）：採集

- **範圍**：arca.live 等**公開板**與公開部落格。**需登入／入會審核的站（Naver cafe 類）不做。**
- **主題**：人物美化、獨立隨從、武器裝備、其他遊戲地圖 porting
- **只抓不載**：抓頁面 HTML、截圖、原始連結。**絕不下載 mod 本體**
- **產出格式**固定成 B1 定的資料夾結構，`meta.json` 欄位由 codex 指定
- **翻譯**：只翻已抓下來的 `page.html` 內的原文成繁中，寫進 `meta.json` 的 `title_zh`/`summary_zh`。原文一併留著供對照

### B3（codex）：收斂

跑 `ingest_candidates.py` + `check_links.py` + `build_gallery.py`，把圖庫路徑交給使用者審閱。
地圖 porting 類的候選另外整理一段，回饋到 `analysis/port-source-survey/README.md`。

---

## 使用者已定案（2026-08-07）

1. **Nexus 走 personal API key**：使用者自行生 key，A1 治具寫成吃 `api.nexusmods.com`（回 JSON、有明確 status 欄位、有 rate-limit header 可讀），不猜 HTML。key 從環境變數 `NEXUS_API_KEY` 讀，**不得寫進任何版控檔案**。
   - **A1 寫治具不需要 key，可立刻開工；A2 實跑要等 key 到手。**
2. **那 107 筆 `quarantined_at` 不一致的資料：從 `archives` 移除**。副作用要在 A3 前先做掉：移除前先 pymongo dump，並在 `docs/` 留一份被移除的 sha256 + 原檔名清單（不進 `archives`，但保留稽核痕跡）。做完把 `WAIT_USER.md` 那條刪掉。

## 派工順序

| 階段 | codex | deepseek | agy |
|---|---|---|---|
| T0（現在，不等 key） | **A1** 寫 `fetch_nexus_status.py`（吃 Nexus API） | **A4a** 從 Mongo 拉 `is_translation=true` 清單，做檔名正規化配對，產 TSV 草稿（**不寫回 Mongo**） | **B2-recon** 列出可爬的公開站／板塊清單、各站結構與可行性，**先不正式採集** |
| T1（key 到手 + A1 驗收過） | **B1** `candidates` schema + ingest／link-check／gallery 三支治具 | **A2** 長跑補值 | 待 B1 定下 `meta.json` 欄位 |
| T2 | **A3** 清理報告 + 107 筆移除 + P1.7 備份；**B3** 收斂 | **A4b** 用 codex 的 matcher 正式填 `translates_mod_id`、出版本差異矩陣 | **B2** 正式採集 |

## 風險

- **Nexus 控速**：1,000+ 次請求，打太快會被擋。這是 A1 治具的首要設計約束，不是 A2 的臨場判斷。
- **agy 幻覺**：已由「原物優先」規則隔離（見上）。收斂時以檔案存在與否為準。
- **mongod 是手動啟動的**：腳本在 mongod 沒開時要給明確錯誤與啟動指令，不要 timeout。
- **deepseek 越權改腳本**：派工時要明講「回報不修」，並在 capture-pane 檢查時留意它有沒有動 `tools/`。
