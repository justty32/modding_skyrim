# 本機驗證證據

[headless 路線](headless.md)｜[入口](README.md)｜[工具鏈](tools.md)

服裝 project 的 CT77 現役／CBBE 對照、實際衣服 shape 與 TRI 驗證見 [服裝證據](outfit-evidence.md)。

**讀法**：2026-11-18 的各節是 3BA（`CBBE 3BBB Body Amazing`）的隔離**能力試驗**，不是現役家族；現役是 CBBE 2.0.3，全域身體由 `Sofia-Body-CBBE` 層決定（見 [部署](deploy.md#1-先查現役贏家)）。11-18 的原件（`/tmp` 下的 probe 目錄與 11-18 的 bodyslide staging 夾）**已刪，結論保留**；要重現就用 [工具鏈](tools.md) 重跑，不找舊路徑。2026-11-21 節是用現役工具鏈對現役家族的實跑。

## 2026-11-21 現役工具鏈端到端（CBBE Body）

stage → plan → 沙箱 runner → `bodyslide_mesh_check.py`，全程在 `~/skyrim_mods/_staging-2026-11-21-bodyslide-fix/run1/`；REPORT 在 private `agentctl/handoffs/home-2026-11-21/bodyslide-fix/`。

- stage 只帶 `ShapeData/CBBE`：480 檔、exit 0；planner 對 `CBBE Body` exit 0、`conflicts=[]`、6 個未選同輸出變體，`variant_check_complete=false`（4 個無關 project 無法檢查）。
- 原生 `-gbuild NativePresetTest -p 'Sentinel A|B' -tri`：A、B、B-repeat、不存在的 preset 四輪 runner 皆 exit 0，各 3 檔（`femalebody_0/1.nif`、`femalebody.tri`）；wine 每輪約 1.3 秒。
- `compare` A／B／B-repeat exit 0：shape `CBBE` 每權重 13,554 頂點（inline count 0），Breasts 0→100 時 4,068 點位移、最大約 2.0934；B↔repeat 全同；TRI 136 morph、尾端 0 bytes。
- 不存在的 preset 對 A：`compare` exit 1（「no vertex changed」），A／B 哨兵不能省。
- safe-fallback 四輪後仍空；modlist.txt sha256 前後一致；沒有殘留 wine／Xvfb 行程。

### BuildSelection 與同輸出（2026-11-21）

同一 run、group 內放 `CBBE Body`＋`CBBE NeverNude`（同輸出 `femalebody`），本機 5.8.2 實測：

| 輪 | tool 根的 `BuildSelection.xml` | 結果 |
|---|---|---|
| bs-none | 無 | 卡住到 120 秒 timeout，log 停在 `Started batch build`，無輸出（推測是看不見的衝突對話框）；runner 對本輪 prefix `wineserver -k` 後收乾淨 |
| bs-choice | `OutputChoice path="meshes\actors\character\character assets\femalebody" choice="CBBE NeverNude"` | 只處理 `CBBE NeverNude`（1 of 1）；輸出有 `CBBE`／`Bra`／`Panty` 三 shape |
| bs-zap | 上一列＋`ZapChoice project="CBBE NeverNude" zap="Remove Bra" choice="true"` | 同上，但 `Bra` shape 消失——zap 依 BuildSelection 套用 |

結論：本機 5.8.2 的 CLI 批次會照 BuildSelection 選同輸出勝者並套 zap；沒有 BuildSelection 時同輸出衝突**不會自動選一件，而是卡死**。所以同輸出一律靠縮小 group 解決，staging 帶進來的 BuildSelection 要照 stage 表逐條核。CLI 建置沒有自己建立 `BuildSelection.xml`（tool 根建置後仍無此檔）。

## 原生 preset：2026-11-18 四輪對照（3BA 能力試驗）

複製官方未修改 `SE 3BBB Amazing.osp`，在 staging 寫精確 group 與 A／B preset，`-gbuild NativePresetTest -p <名稱> -t <隔離路徑>` 執行，沒有 `-tri`。A、B、不存在名稱、B repeat 四輪 exit 0。small／big 的 `Breasts` 同時由 0 改為 100，low／high 各在 18,436 頂點中有 7,709 個改變，最大距離約 2.088543；另兩個 1,905／201 頂點 shape 完全不變。B repeat 與 B 的全部頂點相同。不存在的 `Nonexistent Sentinel` 同樣 exit 0，頂點卻與 A／default 相同。

後續 B＋`-tri` 合測：Config 的 OutputDataPath 改為**已存在且帶結尾反斜線**的私有 safe-fallback，exit 0、產生 low／high NIF 及 5,010,861-byte `femalebody.tri`，NIF 頂點與未加 `-tri` 的 B 相同，safe-fallback 保持空白。當時的 TRI parser 只解 position 段、UV 尾段 30,937 bytes 未解；2026-11-21 的 `bodyslide_mesh_check.py` 已能解完 UV 段。

第一次 fallback 不存在且未帶結尾反斜線時在 OpenGL 初始化後停滯，由本輪精確 PID 終止；根因未隔離。錯 group 的探索輪仍套用 B，因 preset `set` 精確符合 project；不能把 group 當作唯一適用機制。複製的來源 OSP 在建置後仍逐 bytes 等同原版。

## 2026-11-18 固定三輪的獨立覆核

同一 binary 以原生 `-gbuild/-p/-tri/-t` 對 `CBBE 3BBB Body Amazing`、`CT77 Farm Clothes 4` 各跑 A／B／B-repeat；每輪兩 NIF＋一 TRI。身體用歷史官方解包輸入，衣服用現役 loose 子集，不宣稱完整 VFS 或現役 body winner。A／B 僅 Breasts small／big=0／100，其他值按 OSP defaults（連 A 也不是全零基底）。3BA 每權重 7,709／18,436 點改變，FC4 為 522／2,627；位移對 Breasts TRI delta 的最大殘差約 0.000096258／0.000090789。兩 project 各自 B-repeat 三檔路徑及 SHA-256 相同；shape 的 inline count=0 時沿 skin／partition 取頂點。未部署、未實機。來源：`agentctl/handoffs/home-2026-11-18/bodyslide-trial/verify/REPORT.md`。

當時三條實跑都在 bwrap 內：`/` 唯讀、私有 `/tmp`、僅測試目錄可寫、停網路，HOME／WINEPREFIX 在測試夾；Xvfb `-displayfd`、關 GLX（本機預設 GLX 曾觸發 NVIDIA EGL segfault）。這個形狀已收進 `bodyslide_sandbox_run.py`。

## 2026-11-18 OSP defaults 路線

本機 binary SHA-256 為 `3ad463a665d6a735953f177fb87d0f1060ed9cf9c62685a23f681110b98177e2`。取歷史 OSP 的 `bcb1 CBBE 3BBB Body Amazing` 在專用 group `Probe` 跑 `-gbuild Probe -t <隔離路徑> -tri`。只把 OSP `Breasts small` 從 0 改為 100，僅 `_0.nif` 改變（low 7,709／18,436 點位移），`_1.nif`／TRI 不變。把 OutputPath 還原為歷史值時三檔與 2026-11-07 舊輸出逐位元組全等；不同輸出路徑會改變 BODYTRI 字串，所以不能用不同路徑的 NIF hash 推論身材變化。

## 舊個案的驗證界線

2026-11-07 `chronicon-kurone` 的驗證器比對 preset XML 的 small／big 明確值與實際 OSP、輸入／輸出 hash 與 `NiSkinPartition` block hash，但不是直接解析頂點的 A／B 哨兵；同輪 23 個 OBody NPC 排除也不能搬到新任務。場次檔可到期，不作本工作流的必要依賴。
