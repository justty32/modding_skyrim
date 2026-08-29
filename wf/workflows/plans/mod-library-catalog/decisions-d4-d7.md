# 設計決策 D4–D7

> 屬於 [mod 下載庫建檔與清理（MongoDB）](README.md)。

## 二、已定案的設計決策（續）


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

### D7：實作落點（2026-08-23 工作區統整後）

2026-08-04 曾授權本計畫的目錄治具落在 `~/notes/projects/modding/skyrim/{docs,tools,scripts}/`，與 `~/notes/projects/modding/rimworld/` 同構；授權不含部署類筆記 `README.md`、`my-mods.md`、`housecarl.md`、`jackify-manjaro-plan.md`。2026-08-23 統整後，程式與文檔的唯一落點改為 `mod-library/`，`~/notes/projects/modding/skyrim/` 只留不進版控的截圖與 MongoDB 快照，本 repo 只留計畫與設計。
