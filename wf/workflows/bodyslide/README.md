# bodyslide — 隔離建模、驗證與部署

[WORKFLOWS](../../WORKFLOWS.md)｜[INDEX](../../INDEX.md)

把指定 preset 套到指定身體／服裝專案，先在隔離目錄產生可驗證的 NIF／TRI，再交付獨立 output 層。優先走可重跑的 headless 路線。

**何時用**：重烤身體或服裝、批次 Build、排查 preset 空白／同路徑輸出衝突、評估 BodySlide 自動化。
**何時不用**：找或下載素材 → [nexus-intake](../nexus-intake/README.md)；只改皮膚或指向既有私有 NIF → 先查 ARMA 路徑，不必重烤；只改 NPC 體重或身高 → 查 NPC_ `NAM7`／`NAM6`；修改工具原始碼 → [feature-dev](../feature-dev/README.md)。

「刷這件／這套衣服」或指定群組增量重刷，先走 [刷衣服](outfits.md)；共用隔離、工具與部署規則沿本頁。

## Done when

`Done when:` 每次開始時填入具體 project／preset 與預期輸出數；交付下列可觀察條件：

- 輸入 manifest 存在，含版本／hash、VFS 來源、精確 project／preset、slider 與同路徑輸出決議。
- 隔離 output 的檔案清單、hash、建置 log 與結構驗證報告存在；預期缺檔、未決衝突及來源意外變更均為 0。
- REPORT 存在，記錄命令、退出碼與驗證界線；若有部署，另有授權來源、output 層贏家驗證及回退資料。

## 流程

### 1. 凍結輸入與授權範圍

先讀 [工具索引](../../../agentctl/docs/tool-index.md)。只做研究／隔離建置時，不改 `instance/`、DB 或 profile。使用者已授權的範圍直接續行；未授權部署時，先完成 output 與部署／回退計畫，再呈交具體差異。

從現役 `modpack-main` 讀取啟用狀態與資源贏家；工具先用 `instance/tools/profile_query.py`、`whichmod.py`，參數依各自 `--help`。收集 BodySlide 執行檔及設定、`SliderSets`／`ShapeData`／`SliderPresets`／`SliderGroups`，並查專案實際引用的 NIF／OSD。不能只複製一個安裝目錄便宣稱等同 MO2 VFS；停用資源、`.mohidden`、大小寫、同路徑覆蓋及未處理的封裝資源都要明列。

在實體磁碟、`mods/` 與遊戲 Data 之外建立本輪 `work/`、`output/`、`evidence/`。以唯讀來源建立獨立合併 staging，記下每個相對路徑的來源、winner 與 hash；會修改的設定／OSP 必須複製，不可透過 hardlink／symlink 寫回來源。保留建置前來源 hash 與設定快照。

### 2. 決定 preset、project 與輸出擁有者

以 XML 內的精確名稱確認 preset 和 outfit／project，不能以檔名或 GUI 預設選中項代替。先確認 CBBE／3BA／其他身體家族與專案匹配，再明訂 low／high slider 值、未指定 slider 的處置、zap 與 morph 選項；group 只作候選篩選，不等於所有成員都應建置。

依每個 project 的輸出路徑／檔名建立映射，將同一路徑的不同變體逐一決定唯一勝者。身體物理變體、服裝轉換、第一／第三人稱及私有 NPC 路徑各自核對；未決衝突不得開始全批次。預期數量由映射算出，不寫死每個 project 必有兩個 NIF 或必有 TRI。

先選一個代表性 project 做 pilot；preset 必須能解析成實際 slider 值，且值與預期一致。只看到 preset 名稱、程式退出 0 或產生同名檔案都不足以通過。

### 3. 選擇可證明的 headless 執行路線

版本、可重現命令與哨兵檢查見 [headless](headless.md)。

先核實**本機版本**的 CLI／runner 介面及來源，將完整 argv、工作目錄、環境、輸入／輸出路徑與 timeout 寫入 evidence。沒有證據的旗標不寫進可執行命令；GUI 的 Batch Build 能力不代表可用同一套 CLI。

優先使用已驗證的無互動建置；若需 Wine／Proton 或虛擬顯示，使用獨立設定與本輪行程，禁止連進使用者既有 MO2／BodySlide 視窗。虛擬顯示上的 GUI 自動化與無 GUI runner 分別標示，不混稱。先通過 pilot 再做選定批次；記錄逐 project 成敗與衝突決議，禁止以批次總退出碼掩蓋單件失敗。

舊實測「Wine staging 的 preset 下拉空白」只是該版本／啟動方式的個案，見 [既有 lesson](../../lessons/faces-troubleshooting.md#bodyslide-wine-preset-empty-nam7-weight)。先查搜尋路徑、preset group 適用性與 XML 解析。若採用把值寫入 OSP default 的繞法，只修改 staging 副本，證明 low／high、zap 與 morph 等價；未覆蓋的語義列為缺口，不把它當通用 preset 支援。

### 4. 隔離驗證

先比對預期／實際相對路徑集合：缺檔與額外檔都要解釋；檔案存在、大小非零只是初檢。再用本機已有的 NIF／TRI 解析工具檢查檔案可讀、shape／頂點與 morph 對應、材質路徑及適用的 low／high 配對；工具能力不足的項目明列未驗證。

用同輸入重建 pilot 到第二個空目錄，比較 hash；若有非決定性，記錄差異位置與原因。另用至少一個非中性 slider 對照預期形狀／頂點差異，避免 preset 未套用卻產出合法原始 mesh。重驗來源 hash、設定與 live output 未被更動。失敗保留 log 與隔離現場，修正後重建該輪，避免混用舊檔。

OBody 動態分配的全域身體／服裝，先核現役 OBody 設定要求的零滑條基底與 TRI，再決定是否烤入非零 preset；私有 NPC 的固定體型及獨立模型路徑另行決策，不能把兩條路徑混成同一全批次。

### 5. 授權部署與回退

部署前交付獨立 output mod 的目錄、hash 清單、來源／參數與覆蓋範圍；沿 [profile-change](../profile-change/README.md) 與 [safe-apply](../safe-apply.md) 施工窗執行。授權、遊戲／MO2 停止、鎖與實體磁碟備份先到位，不直接覆寫來源 mod、Data 或 overwrite。新層／舊層的替換與排序要能在 dry-run 看清楚。

部署後從 profile／VFS 重查每個目標 NIF／TRI 的 winner，不用左欄位置的直覺判優先權；確認私有 ARMA 模型路徑真的指向本輪產物。只改資產不代表 NPC_、ARMO／ARMA、體重、裝備骨架與物理相容性已驗證。再接 [runtime-qa](../runtime-qa/README.md)，分別看裸身、目標服裝及需要的體重／動作；離線通過不能替代遊戲觀察。

回退沿工具的 revert 資料恢復上一輪 output 與 profile；先核對沒有後續別人的修改，不盲目覆寫。回退後重查 winner／hash；備份保留與清理按 safe-apply，不自行刪除。

## 交接

本輪 manifest、log、驗證與 REPORT 放 private `agentctl` 任務證據目錄；大型 NIF／TRI 留外部磁碟，不進 public 母 repo。規模超過 1 KB 的明細依 [data-files](../common/data-files.md) 用 `wf-table/1` 資料檔與 `tabledb.py`，不把整批資產表塞進 Markdown。

REPORT 分清「來源已讀／headless pilot 已跑／全批次已驗／已部署／實機已驗」，附可續跑命令與未決缺口。等使用者親自做的記 [WAIT_USER](../../../WAIT_USER.md)；跨 session 的 Skyrim 續行點記 [agentctl SESSION](../../../agentctl/SESSION-LOG.md)，母 repo 文件工作才記 [SESSION-LOG](../../../SESSION-LOG.md)。
