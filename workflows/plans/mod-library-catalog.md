# plan：mod 下載庫建檔與清理（MongoDB）

出計畫日期 2026-08-04。姊妹計畫：`workflows/plans/third-party-mod-pipeline.md`（流水線；本計畫產出的目錄是它的資料來源）。前例：`~/notes/projects/modding/rimworld/`（RimWorld 那套 MongoDB 建檔，schema 與教訓整套可搬）。

## 目標

把 `~/skyrim_mods/` 這個 97GB、1,693 個壓縮檔、零索引的下載庫變成一份可查詢的目錄，並在此基礎上安全地清掉**確定沒用**的東西。

**實跑後的定位修正（2026-08-04）**：本計畫**不是空間回收任務**。實測 1,659 個壓縮檔共 85.7 GiB，清理上限是 L1 0.47 GiB + L2 4.76 GiB ≈ **5.2 GiB（6%）**。真正的價值在三件事：知道自己有什麼、揪出 176 個含 SKSE dll 的包裡哪些鎖在別的 runtime（這才是「認定 1.6.1170 為主力」對應的清理）、以及把 286 個漢化包連回它們的本體。空間只是副產品，而且是小的。

**這份目錄是三件事的共同脊椎**：本計畫（庫存與清理）、韓文站採集（附錄 A）、漢化管理（附錄 B）。流水線的 G7「對照已裝」也從這裡查。

## Done when

- [x] **（2026-08-04）** `~/skyrim_mods/` 全部壓縮檔進 MongoDB，每筆有 sha256、來源解析、內容旗標。實際 1,692 個檔 → 去重後 **1,659 筆**、85.7 GiB；檔名解析 99.0%；0 個 listing 失敗；耗時 1 分 46 秒。
- [x] **（2026-08-04）** SKSE DLL 的 runtime 相容性可查。186 個含 dll 的壓縮檔全查完：151 相容 / 9 不相容 / 26 無法判定 / 0 失敗。PE 解析器已對 houseCARL 的已裝層讀值校驗通過。
- [ ] 產出一份清理報告，分級列出候選（見 D4），**每一級都有明確判準與例外規則**，且報告本身可重跑。（L3 已具備；L1 可由 `stats` 產出；**L2 待 P1.4 的在架狀態才能安全判定**）
- [x] **（2026-08-04，L3 部分）** 候選移入隔離區而非刪除，且 restore 往返實測可用。L1/L2 尚未執行。
- [ ] `mongosh` 能回答這幾個問題：某個 mod 我有幾個版本？哪些壓縮檔跟已裝版本不同？哪些是漢化包、對應哪個本體？哪些檔在 Nexus 上已經消失？（前三個已可；**「已消失」待 P1.4**）

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

### D4：清理判準分四級，只有第一級可自動化

| 級 | 判準 | 處置 |
|---|---|---|
| **L1** | **sha256 完全相同**的多份副本 | 保留路徑最淺的一份，其餘進隔離區。**唯一可自動執行的一級** |
| **L2** | 同一 `nexus_mod_id` 的舊版本，且**已有更新版在庫內** | 列報告，逐項需確認。例外見下 |
| **L3** | 含 SKSE dll，且**內含的 dll 沒有任何一個**支援 1.6.1170（既非 Address Library、locked runtime 也不含 1.6.1170），且該壓縮檔**沒有其他有用內容**（無 esp / bsa / 素材） | 列報告，逐項需確認 |
| **L4** | 舊式命名、無法解析來源、無法在 Nexus 上找到對應 | **一律不動**，只標記待人工辨識 |

**L3 實跑結果（2026-08-04）——這一級的目的要改寫**

186 個含 dll 的壓縮檔全部檢查完（0 失敗）：**151 相容、9 不相容、26 無法判定**（query-only / 無 loader-scoped dll，一律保留）。9 個不相容的合計 **0.01 GiB**，其中 6 個同時帶 esp/bsa 內容 → 依 L3 判準不得刪。

**真正可隔離的只有 3 個、共 1.6 MiB**：`JContainers SE 4.2.3`、`PapyrusUtil AE SE 4.4`、`Fuz Ro D'oh 2.3`，全部鎖 1.6.640。

所以 **L3 的價值不是空間，是移除地雷**：這三個正好是目前以 1.6.1170 版本裝著的三個 version-LOCKED 框架的舊副本。庫裡留著鎖 1.6.640 的同名框架，就是姊妹計畫 G4／G7 那個「重裝框架版本→109 個 mod 一起壞」的引信。隔離它們的理由是**風險**，不是容量。

另外 6 個帶 esp/bsa 的（`Honed Metal` 系列、`TK Hitstop AE`、`FISSES`、`RaceMenu 0.4.19.14`）指向一個更有用的結論：**這些 mod 以目前打包的樣子在 1.6.1170 上載不起來**。對它們該問的是「Nexus 上有沒有新版」（一次 `nexus_mod` 查詢），不是「要不要刪」。

**L3 的精確性要求**：多 runtime 打包很常見——實查抽樣中 `SmoothCam` 同時附 AE / AE-Pre629 / SSE 三套 dll，`Base Object Swapper` 附 AE / AE640 / SE 三套。所以**不能看檔名判斷、不能看單一 dll 判斷**，必須是「內含所有 dll 都不相容」才成立。判斷方式：解出 dll，解析 PE export 的 `SKSEPlugin_Version` 結構（houseCARL 的 `skse_inventory` 對已裝 dll 就是這麼做的，**不載入不執行**）。

**L2 的分組鍵修正（2026-08-04 實跑後改，原判準有誤）**

原判準寫「同一 `nexus_mod_id` 的舊版本」——**錯的**。一個 Nexus mod 頁會出多個**不同檔案**（main / optional / patch / 材質變體），每個檔案有自己的版本線。只按 mod_id 分組會把不同檔案當成同一檔的不同版本。實跑抓到的兩個證據：

- `mod 10917` = `Beyond Skyrim - Assets`（632 MiB）+ `Bruma`（2,536 MiB）+ `DLC Integration Patch`（2 MiB）三個**都需要**的檔。天真規則會刪掉 Assets 與 patch，只留 Bruma → mod 直接壞掉。
- `mod 2227` = `Khajiit Will Follow` 本體 + `Khajiit Will Follow Patch - Vigilant`。天真規則會刪掉 Vigilant patch。

**修正**：分組鍵改為 `(nexus_mod_id, normalise_for_grouping(clean_name))`。實測 115 組 → **65 組真·版本堆疊**，避免了 **2.64 GiB 的誤刪**。

**排序鍵必須是檔名裡的 10 位 Nexus timestamp**，不是版本字串、更不是檔案大小：

- 版本字串跨 scheme 不可排序（`0.95.50` vs `0.95.0`、`AE-1-6-640`、`Final`、`beta3`）。
- 大小完全不可靠——`mod 51874` 的舊版 1.7.0 是 493 MiB，新版 1.7.3 只有 472 MiB。按大小留會留到舊的。

**L2 無法全自動（2026-08-04 查證）**：`housecarl_nexus_mod` 只回「最新 MAIN 檔的版本」，**不回逐檔清單**（沒有 file id / MAIN·OPTIONAL·OLD_VERSION 分類）。也就是「這個檔是不是被 Nexus 歸為舊版」問不到。65 組的規模人工逐組審是完全可行的（估 20 分鐘），**不值得為此去擴 houseCARL 的 Nexus client**。報告要附：組內所有檔名、大小、解析版本、Nexus 最新 MAIN 版本。

（附帶收穫：`nexus_mod` 會回報「作者關閉直接下載，只能走 manager/nxm」——這個欄位對姊妹計畫 D5 的下載工作單有用，它決定瀏覽器那條路走不走得通。）

**L2 的三條例外（優先於判準）**：

1. **目前已裝的那一版永不列為候選**，即使它不是最新（對照 MO2 的 `mods/` 與 houseCARL）。
2. **漢化包的版本對應關係要先建立**（附錄 B）。刪掉舊本體可能讓手上唯一版本相符的漢化包失去對象。
3. **Nexus 上已消失的一律保留**（見 D5）。

### D5：不可替代性優先於一切判準 — 不刪，只隔離

97GB 是多年累積。Nexus 上的 mod 會被作者隱藏、下架、刪號；一個現在下載不到的檔刪掉就是永久損失，而**判準完全看不出這件事**。

因此：

- 建檔階段用 Nexus API 查每個 mod **是否仍在架**。查不到 / 已隱藏 → `nexus_status: "gone" | "hidden"` → **標記為 `never_delete: true`，覆蓋所有清理判準**。
- **2026-08-07 實測釘死 Nexus API 欄位**：`GET https://api.nexusmods.com/v1/games/skyrimspecialedition/mods/{id}.json`，header `apikey`。`status="published"` 且 `available=true` → `live`；404 → `gone`；`available=false` 或 `status` 為 `removed` / `wastebinned` 等下架狀態 → `hidden`；其他一律 `unknown`，且 `unknown` 不得觸發清理。
- `nexus_latest_version` 不能取 mod header 的 `version`。SkyUI 12604 實測 header 是 6.9，但最新 MAIN file 是 6.11；必須另打 `/mods/{id}/files.json`，取 `category_name="MAIN"`、`category_id=1`、`is_primary=true` 的最新檔案版本。
- Nexus rate limit 實測 2,000/小時、20,000/天；1,272 個 nexus_id 以 1 秒以上 request interval 可在一小時內跑完，rate limit 不是瓶頸。
- 所有清理動作都是**移入隔離區**（`~/skyrim_mods/.quarantine/<日期>/`，保留原相對路徑），不是 `rm`。移動記錄寫回 Mongo（`quarantined_at`、`quarantine_reason`、`original_path`）。
- 真正的刪除是**另一次獨立的、使用者主動發起的操作**，不在本計畫的 Done when 裡。
- RimWorld 的 `prune` 是 `delete_many` 且無 dry-run 無備份——**這一點不抄**。

### D6：目錄是分析工具，不是部署權威（承 RimWorld 教訓 4）

RimWorld 的 runbook 明文警告：MongoDB 那套適合「篩選查詢」，但**刻意不整合**進組包管道；組包權威永遠是 `layers/` + `profiles/` + `rwbuild.py` 這條獨立管道，不依賴 Mongo。

同構搬到 Skyrim：**load order 的權威是 MO2 profile + git（姊妹計畫 D3），永遠不是 Mongo。** 流水線可以查目錄來加速決策（例如 G7 的依賴 diff），但 **mongod 沒開時流水線必須照樣能跑完**。任何讓流水線硬依賴 Mongo 的設計都是錯的。

### D7：實作落點 = `~/notes/projects/modding/skyrim/`，照 RimWorld 對稱（使用者 2026-08-04 決定）

程式與文檔落 `~/notes/projects/modding/skyrim/{docs,tools,scripts}/`，與 `~/notes/projects/modding/rimworld/` 同構。

**這是對「`~/notes/` 不主動動手」那條慣例的一次明確授權例外**，範圍限於本計畫的目錄治具。其他部署類筆記（`README.md`、`my-mods.md`、`housecarl.md`、`jackify-manjaro-plan.md`）仍不代改。

本 repo 這邊只留計畫與設計（本檔）；程式不進本 repo，避免同一份東西兩個家。

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

## 六、執行紀錄

程式在 `~/notes/projects/modding/skyrim/tools/`：`scan_mod_library.py`（1.1–1.2）、`check_dll_runtime.py`（1.3）、`quarantine.py`（1.6）。schema 文件在同專案 `docs/mongodb-schema.md`。

**2026-08-04 · L3 隔離已執行**

移入 `~/skyrim_mods/.quarantine/2026-08-04/`，共 3 檔 1.61 MiB，理由是移除框架版本地雷（非回收容量）：

| 檔案 | 鎖定 runtime | 庫內保留的相容版 |
|---|---|---|
| `Fuz Ro D'oh-15109-2-3` | 1.6.640 | `Fuz Ro D'oh-15109-2-5` |
| `JContainers SE-16495-4-2-3` | 1.6.640 | `JContainers SE-16495-4-2-9` |
| `PapyrusUtil AE SE-13048-4-4` | 1.6.640 | `PapyrusUtil AE SE-13048-4-6` |

移動前自動 dump 了整份 catalogue（`backups/skyrim-mongo-2026-08-04-222103-pre-quarantine.json`）。**restore 往返已實測**：還原一個 → 確認回到原路徑且 mtime 保留 → 再次隔離 → 狀態一致。沒有驗過 restore 的隔離區只是慢動作刪除，所以這個往返測試是驗收條件而不是加分項。

**實作時撞到、值得記下的兩件事**

1. **`compatibleVersions` 陣列在宣告 AddrLib 的 plugin 裡是垃圾。** 實測 `APoseFix`、`AnimationMotionRevolution` 讀出 16 個一模一樣的 `0x01000000`（解成「1.0.0」，不是任何 Skyrim runtime）——SKSE 在版本獨立位元有設時根本不讀這個陣列，作者自然不初始化它。修法：只在 `addr_lib=false` 時採信該陣列，並過濾掉不在 1.4–1.6 範圍的值。原始值另存 `raw_compatible_versions` 供稽核。
2. **「讀不出意圖」必須判為保留，不能判為不相容。** query-only 的舊 plugin 是在 `SKSEPlugin_Query` 裡動態設定 metadata，靜態讀不到。`judge()` 只在「每個 loader-scoped plugin 都宣告了可用的 runtime 清單、且都不含 1.6.1170」時才回 False。26 個「無法判定」就是這條規則保下來的。

## 附錄 A：韓文站採集工作流（使用者 2026-08-04 提出，待轉 `workflows/roadmap/`）

**需求**：使用者對韓文圈的**人物美化、獨立隨從、武器裝備、其他遊戲地圖 porting** 長期感興趣，想讓 `agy` 多次長時間爬，先抓**截圖與簡介**進一個資料夾供審閱，審過才下載；並要檢查**下載連結是否還有效**。

已定的形狀：

- **這是「發現階段」，接在流水線最前面**，產出 `candidates` collection（不是零散資料夾）。放 Mongo 的關鍵理由是**否決狀態要能持久**——長期多次爬，被否決過的不該再次出現在審閱清單裡。
- 審閱介面用**本機 HTML 圖庫**（截圖 + 翻譯後簡介 + 原始連結 + 連結存活狀態），對應本 repo 既有的 `html-guide` 工作流形狀。
- 執行者是 `agy`（姊妹計畫 D7），主 session 出 schema 與判準、收斂結果。爬取本身外包。
- 連結存活檢查：HEAD 請求，狀態寫 `link_status` + `link_checked_at`。
- **地圖 porting 類與 `projects/darksouls-port` 及 `analysis/port-source-survey/` 直接相關**，採集到的候選應該回饋那份調查。
- 邊界：需登入／入會審核的站（Naver cafe 類）不做；公開板（arca.live、公開部落格）可做。

## 附錄 B：漢化管理（使用者 2026-08-04 提出，待轉 `workflows/roadmap/`）

**需求**：Nexus 下載的東西要順便抓漢化；漢化版本不對要能補強；韓文站抓回來的也要檢查並做漢化。

已定的形狀：

- **起點不是零**：庫裡已有大量 `- CHS` / `- CHT` / `(Chinese Translation)` 檔（實查確認，如 `Honed Metal` 一組六個變體）。本計畫的 `is_translation` / `translates_mod_id` 就是給這件事鋪路的。
- **資料模型陷阱（2026-08-07 A4a）**：漢化包在 Nexus 上常有自己的 mod id，所以 `mods` 裡會出現純漢化包 stub（`archive_ids=[]`、`translation_archive_ids` 非空）。A4a 實掃有 255 個這種 stub。比對本體時必須排除它們，只比對 `archive_ids` 非空的真本體；否則會把漢化包配到另一個漢化包，實例是 `Beyond Skyrim - Bruma SE (CHT)` 被配到 `Beyond Skyrim Bruma - CNS`。
- **A4a 掃出的翻譯衍生標記**（剔除誤收的 `MCM`、`CLEAN`）：`CHINESE`、`CHS`、`CHT`、`CNS`、`Chinese`、`Chinese Localisation`、`Chinese Localisation Based on WOK`、`Chinese Simple`、`Chinese Translation`、`Chinese translation`、`Chinese version`、`Simpifity Chinese`、`Simplified Chinese`、`Simplified Chinese Translation`、`Simplified Chinese translation`、`Traditional Chinese`、`Traditional Chinese Translation`、`Traditional Chinese translation`、`ZH`、`\CHS\`、`\CHT\`、`\chs\`、`\cht\`、`chinese translation`、`chs`、`cht`、`cns`、`simplified Chinese`、`simplified Chinese translation`、`traditional Chinese`、`traditional Chinese translation`、`zh`、`zh_CN`、`汉化`、`汉化补丁`。
- **版本不對的正確解法不是換 esp。** 漢化包通常是整份 plugin 替換——拿 v1.0 的漢化 esp 蓋 v1.2 的本體，等於把 v1.2 的所有改動退回 v1.0。正確做法是**只把譯文欄位（FULL / DESC / 對話）forward 到當前版本的 plugin，輸出成 patch**。houseCARL 的 `forward_record` / `bulk_apply` / `set_field` / `cross_plugin_query` / `batch_record_detail` 正是這組工具，能力已經在手上。
- **最大的技術陷阱是編碼。** Skyrim plugin 的字串或內嵌（非 localized，Windows-1252）或走 `Strings/*.STRINGS`（localized）。中文無法用 Windows-1252 表示，所以漢化包要嘛走 localized strings、要嘛靠 codepage 詮釋的老 hack。**houseCARL 目前就有一條 `fix/dialogue-encoding-lint` 分支掛在 `WAIT_USER.md`**——編碼在自家工具鏈裡已經是活的議題，不是理論風險。動手前先把那條分支的結論確定。
- 非 plugin 的字串也要顧：MCM 的 `Interface/Translate_<name>_<lang>.txt`、SkyUI MCM 的 json、`.pex` 內硬編字串（難）、語音 `.fuz`（`projects/skyrim-voicegen` 是另一條路，屬 TTS 不屬翻譯）。
- 資料模型參考 RimWorld 的 `diy_translates`（`target_package_ids` / `target_details` / `translation_files` / `file_count`），結構可直接對應。
