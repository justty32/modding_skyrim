# Interior Inspector 1.0 — 單檔瀏覽器版室內 cell 衝突檢查器

← [tool-survey](../README.md)

**結論**：不是遊戲 mod，是一個 639 KB、完全離線的單檔 HTML／JavaScript 工具。它在瀏覽器裡直接讀 MO2 資料夾的 plugin、BSA、NIF、DDS，對「被 mod 改過的每個室內 cell」做 navmesh／門／物件／燈光衝突檢查，有 WebGL 3D 漫遊與「原版 vs 你的 load order」左右對照，還能把修正寫成一顆 ESL 旗標的 ESP 打包下載。原始碼沒有混淆，可以直接讀。我們可以把它當成稽核工具來借用，但它的修正 patch 不能直接進包。

調查日期 2026-11-22。來源檔：`~/Downloads/Interior Inspector 199896 1 2026-11-20T16-00Z izKcFkcwC.zip`（203 KB，內含 `interior-inspector.html` sha256 `202e677e…3a91b`、`Interior Inspector README.txt` sha256 `62502b4c…bde912`）。下文 `html:N` 指解到 `wf/temp/interior-inspector/extract/interior-inspector.html` 的行號，`README:N` 指 README 行號。

## 身分

| 項目 | 值 | 依據 |
|---|---|---|
| 類型 | 外部工具（瀏覽器單頁 app），不進 Data | README:8-9、html 全檔無 `<link>`／外部 script |
| 版本 | 1.0 | README:1 |
| 作者 | 檔內沒寫；自稱是 Terrain Inspector 的室內版 | README:4、html:417 `Skyrim Terrain Seam Inspector — core` |
| Nexus id | 199896（**推論**：取自下載檔名；houseCARL `housecarl_nexus_*` 本場沒掛，**未查證**） | 檔名 |
| 授權 | 檔內沒有授權條款；Nexus 權限頁**未查證** | `grep -i license` 無命中 |
| 建置 | 原本是多個 `.js` 模組由 `build.py` 拼成單檔，各模組也能用 Node `require` | html:3262、html:5304、html:6106 |

## 安全面（靜態審視，沒有執行）

- 全檔唯一的 URL 是 SVG namespace；沒有 `fetch`／XHR／WebSocket／`sendBeacon`／`eval`。
- 讀資料夾用 `showDirectoryPicker({mode:'read'})`（html:6506），只讀；輸出只靠瀏覽器下載（html:7908 zip、html:8441 CSV）。
- 唯一的 `Worker` 是把自家 `buildBVH`／`rayHit`／`holeCompute` 函式轉成 Blob URL 來跑（html:5972）。
- 狀態存在 `localStorage`（修正籃子 `iinsp-basket-v1`，html:8030）和 IndexedDB `terrain-inspector`（記住上次選的資料夾，html:6525）。

## 模組地圖

| 區塊 | 行號 | 負責 |
|---|---|---|
| TSI core（Terrain Inspector 共用核心） | html:417-2480 | 純 JS zlib inflate、plugin header、load order 解析 `resolveLoadOrder`（html:937）、NVNM 解析 `nvnmParse`（html:2098）、navmesh 健康檢查與 ESP 寫入器 `patchWriter`（html:1743） |
| 資產層 | html:2482-3257 | BSA v104/v105＋LZ4（`Archive`，html:2530）、NIF 20.2.0.7 解析 `parseNif`（html:2788；BSTriShape／NiTriShape 等約 35 種 block）、DDS BC1-BC7 |
| II core | html:3259-4344 | 單次掃描 `scanPlugin`（html:3361）、按需讀 cell `loadCell`（html:3563）、原版校準 `calibrate`（html:3845）、規則引擎 `checkCell`（html:3932） |
| 3D 檢視 | html:4346-5297 | WebGL2 freecam、三種打光（`LOOKS`，html:4459）、左右對照、點選物件 |
| 修正 patch 寫入器 IIP | html:5299-5790 | 材質 patch `buildTexturePatch`（html:5365）、navmesh 計畫 `planNavmesh`（html:5520）、zip |
| 破洞偵測 IIH | html:5792-6105 | BVH＋光線：從可走處往外看，原版會撞牆、現在穿到虛空 → 判定為看得到的洞 |
| NPC 走路測試 | html:6107-6216 | 在 navmesh 三角形圖上找路，並檢查身高範圍內的阻擋物 |
| UI | html:6218-8447 | MO2／Wabbajack／Nolvus／Vortex 資料夾辨識、Homes 分頁、修正籃子、CSV |

## 資料流

```mermaid
flowchart LR
  A[選資料夾<br>MO2 / Data] --> B[辨識 mods、profiles、BSA<br>依 modlist 決定贏家檔]
  B --> C[resolveLoadOrder<br>plugins.txt / loadorder.txt]
  C --> D[scanPlugin 每顆 plugin 一次<br>只記 CELL 版本、NAVM、門、base 物件]
  D --> E[calibrate<br>量原版室內的門／navmesh 基準率]
  E --> F[loadCell 按需重讀<br>每個 REFR / NAVM 的各版本]
  F --> G[checkCell 規則]
  G --> H[問題清單 / 2D 平面 / 3D]
  H --> I[修正籃子 → ESL 旗標 ESP + zip]
```

- **記憶體策略**：plugin 整檔讀進來、掃一次後就丟掉，只留下位移（html:3359 註解、`v.off`／`v.end`）。打開 cell 時才用 `readRange` 回頭讀那一段（html:3571）。
- **FormID 正規化**：`resolve()` 把「相對於該檔 master 表」的 FormID 轉成全 load order 唯一的鍵 `名稱索引 × 2^24 + id`（html:3342）。所有比對都在這個空間做。
- **原版校準**：先量原版室內「load door 有門三角形的比例」「navmesh 連結有效率」「重疊 navmesh 的 cell 比例」「每種 base 物件壓在 navmesh 上的比例」，算出門檻（`calEnd`，html:3879-3886：door 至少 85%、link 至少 95%、overlap 不超過 15%）。原版本來就常這樣做的情況（地毯、拱門、梯子）不會被報出來（html:4004）。

## 規則（`checkCell`，html:3932-4244）

| kind | 嚴重度 | 內容 |
|---|---|---|
| `cellDeleted` | 3 | 非原版 plugin 刪掉整個室內 |
| `cellField` | 1-2 | XCLL／LTMP／XCIM／XLCN／XEZN／XOWN／XCMO 等 cell 欄位被後載 plugin 蓋掉（`CELL_FIELDS`，html:3279）；後載者把前者列為 master 時視為刻意，降級 |
| `navDeleted` | 3 | navmesh 被刪除，不是移到地底 |
| `navRival` | 群組 | 多個 mod 改同一張 navmesh；輸家放的物件如果正站在贏家的 navmesh 上就升級（html:3994-4005） |
| `navOverlap`／`navLink`／`navDoorGone`／`noNavmesh` | 2-3 | 重疊、斷鏈、指向消失的門、整個室內沒有 navmesh |
| `doorDest`／`doorOneWay`／`doorMarker` | 1-3 | 門通往不存在的地方、不能雙向往返、落點離門太遠 |
| `refDeleted`／`refRival`／`objOnNav`／`objClash` | 群組 | 物件被刪除而不是 disable、多 mod 搶改同一物件、擋路、兩 mod 疊放 |
| `lightFlicker` | 2 | 同一點超過 4 盞投影燈，或沒有 LLF 時超過 7 盞燈，**而且原版在同一點沒有超標**（html:4206-4238）；LLF 用 `communityshaders.dll`／`lightlimitfix.dll` 是否存在來判斷（html:7002） |

## 修正 patch 怎麼寫

- **Disable**：把贏家的 REFR 逐位元組複製過來，加上 Initially Disabled（0x800），並把 XESP 設成 player＋opposite（html:1791-1840，與 xEdit 手工做法相同），不刪除任何東西。
- **材質**：新的 TXST 加上帶 MODS 替代材質的 STAT 複本，再覆寫 REFR。新 FormID 從 0x800 開始，超過 0xFFF 就提醒分批（html:5678、html:5761）。遇到 VMAD 等無法安全重映射的子記錄就整筆略過並列入報告（html:5373-5380）。
- **Navmesh**：可選要保留哪個 mod 的版本、把被刪的 navmesh 救回並沉到地底，或還原為刪除前的版本。
- TES4 一律帶 ESL 旗標 0x200（html:1778、html:5511-5514）；master 只放真正被引用到的 plugin（html:1744-1748）。

## 已知限制

- 只讀 record：不看腳本，也不看 mesh 內的碰撞（README:256-259）。
- 有在地化的名稱只讀 `strings/<plugin>_english.strings`（html:6964）；沒在地化的字串用 windows-1252 解碼（html:3291），所以 UTF-8 中文的 FULL 會變亂碼（**推論**：只影響顯示的名稱）。
- 3D 打光是逐頂點近似，沒有即時陰影（README:109-110）。
