# plan：mod 下載庫建檔與清理（MongoDB）

出計畫日期 2026-08-04。姊妹計畫：`wf/workflows/plans/third-party-mod-pipeline/README.md`（流水線；本計畫產出的目錄是它的資料來源）。前例：`~/notes/projects/modding/rimworld/`（RimWorld 那套 MongoDB 建檔，schema 與教訓整套可搬）。

## 目標

把 `~/skyrim_mods/` 這個 97GB、1,693 個壓縮檔、零索引的下載庫變成一份可查詢的目錄，並在此基礎上安全地清掉**確定沒用**的東西。

**實跑後的定位修正（2026-08-04）**：本計畫**不是空間回收任務**。實測 1,659 個壓縮檔共 85.7 GiB，清理上限是 L1 0.47 GiB + L2 4.76 GiB ≈ **5.2 GiB（6%）**。真正的價值在三件事：知道自己有什麼、揪出 176 個含 SKSE dll 的包裡哪些鎖在別的 runtime（這才是「認定 1.6.1170 為主力」對應的清理）、以及把 286 個漢化包連回它們的本體。空間只是副產品，而且是小的。

**這份目錄是三件事的共同脊椎**：本計畫（庫存與清理）、韓文站採集（附錄 A）、漢化管理（附錄 B）。流水線的 G7「對照已裝」也從這裡查。

## Done when

- [x] **（2026-08-04）** `~/skyrim_mods/` 全部壓縮檔進 MongoDB，每筆有 sha256、來源解析、內容旗標。實際 1,692 個檔 → 去重後 **1,659 筆**、85.7 GiB；檔名解析 99.0%；0 個 listing 失敗；耗時 1 分 46 秒。
- [x] **（2026-08-04）** SKSE DLL 的 runtime 相容性可查。186 個含 dll 的壓縮檔全查完：151 相容 / 9 不相容 / 26 無法判定 / 0 失敗。PE 解析器已對 houseCARL 的已裝層讀值校驗通過。
- [x] **（2026-08-07 落地；2026-08-11 重驗）** 清理報告已分 L1–L4 + keep，每級有明確判準與例外；清理分級工具的 `--self-test` 13/13 PASS，實庫唯讀 `--verify` 6/6 PASS 且兩次分類一致。
- [x] **（2026-08-04，L3 部分）** 候選移入隔離區而非刪除，且 restore 往返實測可用。L1/L2 尚未執行。
- [x] **（2026-08-07）** `mongosh` 已能回答版本、已裝版本差異、漢化本體對應與 Nexus 消失／隱藏狀態；P1.4 在架狀態與 A4 `translates_mod_id` 補值均已完成。

**不包含**：直接 `rm`（見 D5）、`unzip/` 內已解壓素材的去重（先只做壓縮檔層）、`mine/`（自製物，不清理，只建檔）、韓文站採集與漢化實作（附錄 A/B，各自另開計畫）。

## 一、環境事實（2026-08-04 實查）

| 項目 | 事實 |
|---|---|
| 庫總量 | 97GB、28,469 檔 |
| `hdd/` | **83GB / 1,441 壓縮檔** — 主體，疑似舊硬碟搬來的完整下載史 |
| `unzip/` | 11GB / **49 個已解壓資料夾**（僅約 3% 的壓縮檔被解壓；數量與 MO2 啟用條目相近，推測是現役子集） |
| `aa/` | 1.1GB / 11 檔 — 新版 Nexus App 命名（帶 ISO 時間戳），下載工具換過的痕跡 |
| `mine/` | 143MB / 58 項 — 自製 `DSPort*` / `ModForge*` / `MF*` / `SofiaVigilantAct*` |
| 根目錄散檔 | 108 檔 / 2.6GB，**其中 25 個（23%）與 `hdd/` 內 bit-identical** |
| 格式分布 | `.7z` 818（53.2GB）· `.zip` 618（14.2GB）· `.rar` 257（25.1GB）。**zip 只佔 36%** |
| 重複規模 | 去版本號後 **100+ 組**同名 mod 出現 2 次以上 |
| 既存索引 | **完全沒有**。唯一命中是 `.mo2-profile-backup-20260710-123409/` 的三個 MO2 txt（不記來源/版本） |
| 解壓工具 | `unar` / `unrar` / `7z`（**支援 rar5**）/ `bsdtar` 全部已裝 |
| MongoDB | `~/data/mongodb`（216MB，RimWorld 那份）。**mongod 目前沒在跑**，手動啟動；系統的 `mongodb.service` 指向空的 `/var/lib/mongodb`，**不要動** |
| pymongo | 4.17.0 |
| 磁碟餘量 | `/` 632GB 可用 — 隔離區與暫存空間充裕 |
| 命名 pattern | 四種：標準 Nexus（`Name-36869-7-3-0-1778353486.7z`）、無 id 舊式、新 Nexus App（`Name 159600 1.2 2026-06-21T15-09Z xxx.rar`）、**衍生標記（`- CHS` / `- CHT` / `(Chinese Translation)` / `- ESPFE`）** |

**已有大量漢化包躺在庫裡**（最後一項）——附錄 B 的起點不是零。

## 四、分階段任務

| # | 任務 | 驗證 |
|---|---|---|
| 1.1 | 掃描器：走 `~/skyrim_mods/`，算 sha256、讀目錄表、解析檔名 → `archives`（upsert，D2 分離） | 1,693 筆全進；`--dry-run` 只印不寫；重跑一次養成欄位不變 |
| 1.2 | `mods` 聚合 + L1 重複偵測 | 根目錄那 25 個 bit-identical 檔正確被認出 |
| 1.3 | DLL runtime 檢查（解 dll → 解析 `SKSEPlugin_Version` → `dll_compat` / `runtime_ok_1_6_1170`） | 抽驗 `SmoothCam`（多 runtime）判為 OK；抽一個純 SE 期插件判為不 OK |
| 1.4 | Nexus 補值：`housecarl_nexus_mod` 查在架狀態與最新版 → `nexus_status` / `never_delete` | 抽驗一個已下架 mod 正確標成 `gone` 且 `never_delete` |
| 1.5 | 清理報告產生器（四級分類 + L2 三條例外） | 報告可重跑且結果一致；例外規則有測到 |
| 1.6 | 隔離器（移動 + 回寫 Mongo，非刪除） | 移動後可用記錄完整還原；`--dry-run` 先出清單 |
| 1.7 | 備份：pymongo dump 到 json（機器無 `mongodump`，同 RimWorld） | 任何清理動作前自動先 dump |

執行順序上 1.1–1.2 先跑（純磁碟、快），1.3–1.4 是慢的養成階段（解壓 + 網路），1.5 之後才碰得到檔案。

## 五、風險

- **不可替代性**（D5 已處理）：最大的一項。任何「先刪了再說」的做法都不可接受。
- **多 runtime 打包導致 L3 誤判**（D4 已處理）：實查已證這在庫裡很常見。
- **sha256 掃 97GB 的時間成本**：一次性可接受，但要能中斷續跑（記 `mtime` + `size` 做快取鍵，未變的不重算）。
- **`unzip/` 與壓縮檔的關係未建立**：49 個已解壓資料夾只有部分能對回壓縮檔。本計畫不處理，但要在目錄裡留欄位，別讓後續無處可放。
- **`mine/` 是自製物**：只建檔不清理。它們的來源是 `projects/` 的產物，重建成本低但歷史意義高。
- **Mongo 成為隱性依賴**（D6 已處理）：流水線不得硬依賴。
- **mongod 是手動啟動的**：腳本要在 mongod 沒開時給明確錯誤與啟動指令，而不是 timeout。

---

## 本計畫的其他部分

| 檔案 | 內容 |
|---|---|
| [`decisions-d1-d3.md`](decisions-d1-d3.md) | 設計決策 D1–D3 |
| [`decisions-d4-d7.md`](decisions-d4-d7.md) | 設計決策 D4–D7 |
| [`schema.md`](schema.md) | schema 草案 |
| [`execution-log.md`](execution-log.md) | 執行紀錄 |
| [`appendices.md`](appendices.md) | 附錄 A 韓文站採集／附錄 B 漢化管理 |
