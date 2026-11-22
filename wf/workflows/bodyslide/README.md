# bodyslide — 隔離建模、驗證與部署

[WORKFLOWS](../../WORKFLOWS.md)｜[INDEX](../../INDEX.md)

把指定 preset 套到指定身體／服裝專案，先在隔離目錄產生可驗證的 NIF／TRI，再交付獨立 output 層。走可重跑的 headless 路線，四支工具串成一條鏈，見 [工具鏈](tools.md)。

**何時用**：重烤身體或服裝、批次 Build、排查 preset 空白／同路徑輸出衝突、評估 BodySlide 自動化。
**何時不用**：找或下載素材 → [nexus-intake](../nexus-intake/README.md)；只改皮膚或指向既有私有 NIF → 先查 ARMA 路徑，不必重烤；只改 NPC 體重或身高 → 查 NPC_ `NAM7`／`NAM6`；修改工具原始碼 → [feature-dev](../feature-dev/README.md)；捏臉、改 NPC 的臉（NAM9／headpart／tint／FaceGen）→ [racemenu](../racemenu/README.md)。

「刷這件／這套衣服」或指定群組增量重刷，先走 [刷衣服](outfits.md)；整範圍重建、換身體、給 NPC 指定身形走 [換身體](body-swap.md)；共用隔離、工具與部署規則沿本頁。

## 內容

| 檔案 | 內容 |
|------|------|
| [tools.md](tools.md) | stage → plan → 沙箱建置 → 驗收的可照抄指令、exit code、暫存保留期 |
| [headless.md](headless.md) | 版本證據、原生 preset、Config、BuildSelection／zap、OSP fallback |
| [outfits.md](outfits.md) | 指定服裝的增量刷新 |
| [body-swap.md](body-swap.md) | 設定檔一行重建全範圍、換身體、使用者自己捏身形、逐 NPC 指定身形（OBody） |
| [fit.md](fit.md) | 自帶專屬身體的 NPC：把私有身體擬合成 preset，讓裝備跟上她的身形 |
| [deploy.md](deploy.md) | 現役贏家查核、最小 manifest、部署後驗證與回退 |
| [evidence.md](evidence.md)、[outfit-evidence.md](outfit-evidence.md) | 2026-11-18 隔離試驗的結論（原件已刪） |

## Done when

`Done when:` 每次開始時填入具體 project／preset 與預期輸出數；交付下列可觀察條件：

- `bodyslide_stage.py` 的來源表存在（exit 0），`bodyslide_outfit_plan.py` 對本輪 project exit 0、`conflicts` 為空；`variant_check_complete=false` 時 REPORT 逐條說明 `uninspected_projects` 與本輪輸出無關。
- 每輪 `bodyslide_sandbox_run.py build` exit 0；`bodyslide_mesh_check.py compare` 對 A／B／B-repeat exit 0。
- REPORT 存在，記錄命令、退出碼與驗證界線；若有部署，另有授權來源、output 層贏家驗證及回退資料（`revert.json`）。

## 流程

### 1. 凍結輸入與授權範圍

先讀 [工具索引](../../../agentctl/docs/tool-index.md)。只做研究／隔離建置時，不改 `instance/`、profile、`mods/`、`overwrite/` 或 Data。使用者已授權的範圍直接續行；未授權部署時，先完成 output 與部署／回退計畫，再呈交具體差異。

先區分隔離能力試驗、現役增量與部署，寫明所需來源保證；盤點後才凍結建置範圍。歷史原件可用於明標非現役的隔離試驗，不冒稱現役 winner。

啟用狀態用 `instance/tools/profile_query.py`（它只回啟用狀態，不解資產贏家）；資產贏家用 `instance/tools/whichmod.py`（寫本機 SQLite 快取，不是 MongoDB；細節與 BSA 限制見 [部署](deploy.md#1-先查現役贏家)）。合併 staging 一律用 `bodyslide_stage.py`，**不要 `cp -r` 疊目錄**：現役樹的 `BodySlide`／`Bodyslide`／`slidersets` 大小寫混雜，手動疊會在 Linux 長出並排的樹，wine 只看得到其中一棵；複製順序不等於優先序時還會吃到舊 OSD。staging 是真複本，不可 hardlink／symlink 回來源；停用資源、`.mohidden`、大小寫、同路徑覆蓋及未處理的封裝資源都在來源表裡明列，不能只複製一個安裝目錄便宣稱等同 MO2 VFS。建置前採集來源／設定及相關 live 目標的集合、hash／不存在基線；事後採樣不能冒稱前後未變。

### 2. 決定 preset、project 與輸出擁有者

以 XML 內的精確名稱確認 preset 和 outfit／project，不能以檔名或 GUI 預設選中項代替。先確認身體家族與專案匹配：**現役是 CBBE 2.0.3**（3BA 只用在 11-18 的能力試驗），全域身體目前由 `Sofia-Body-CBBE` 層決定，見 [部署](deploy.md#1-先查現役贏家)。再明訂 low／high slider 值、未指定 slider 的處置、zap 與 morph 選項；group 只作候選篩選，不等於所有成員都應建置。

依每個 project 的輸出路徑建立映射，同一路徑的不同變體逐一決定唯一勝者（planner 的 `conflicts`／`unselected_variants`）。**每個輸出路徑另查現役實檔贏家，含非 BodySlide 的檔**；贏家不是 BodySlide 產物時，由使用者決定取代或不動。批次模式下同輸出的勝者與 zap 還受 `BuildSelection.xml` 影響，見 [headless](headless.md#buildselection-與-zap)。預期數量由映射算出，不寫死每個 project 必有兩個 NIF 或必有 TRI。

先選一個代表性 project 做 pilot；preset 必須能解析成實際 slider 值，且值與預期一致。只看到 preset 名稱、程式退出 0 或產生同名檔案都不足以通過。

### 3. 沙箱建置

一律經 `bodyslide_sandbox_run.py`，不直接在 shell 跑 `wine BodySlide.exe`：Wine 的 `Z:` 對映整個 `/`，沒有沙箱時隔離只剩 `-t` 一個字串。版本證據、Config 與 preset 細節見 [headless](headless.md)。先通過 pilot 再做選定批次；逐輪看 `result.json`，禁止以批次總退出碼掩蓋單件失敗。

虛擬顯示上的 GUI 自動化與無 GUI runner 分別標示，不混稱；不連進使用者既有 MO2／BodySlide 視窗。舊實測「Wine staging 的 preset 下拉空白」只是該版本／啟動方式的個案，見 [既有 lesson](../../lessons/faces-troubleshooting.md#bodyslide-wine-preset-empty-nam7-weight)；先查搜尋路徑、preset group 適用性與 XML 解析，OSP default 繞法的界線見 [headless](headless.md#fallbackosp-defaults-與幾何哨兵)。

### 4. 隔離驗證

先比對預期／實際相對路徑集合：缺檔與額外檔都要解釋；檔案存在、大小非零只是初檢。以 A／B／B-repeat 驗指定語義，用 `bodyslide_mesh_check.py compare`：A 為中性或已知基準，B 只改一個已知有效的非零 slider；B-repeat 證明可重現。工具能力不足的項目（TRI UV 尾段、材質、skin weights、物理）明列未驗證。失敗保留 log 與隔離現場，修正後開新 label 重建，避免混用舊檔。重驗來源 hash（來源表）、設定與 live output 未被更動。

OBody 動態分配的全域身體／服裝，先逐 slider 核現役 OBody 所需基底與 TRI，區分形狀與接縫校正（見 [刷衣服](outfits.md#2-決定變體與身形路線)），再決定是否烤入非零 preset；私有 NPC 的固定體型及獨立模型路徑另行決策。

### 5. 授權部署與回退

見 [deploy](deploy.md)：現役贏家查核、ASCII 層名、`before` 錨點、`layer_apply` dry-run／`--revert-out`、部署後 winner 重查與 runtime-qa。

## 交接

本輪 manifest、log、驗證與 REPORT 放 private `agentctl` 任務證據目錄；大型 NIF／TRI 留外部磁碟，不進 public 母 repo（他人 mod 的 NIF／TRI 也不得進母 repo）。規模超過 1 KB 的明細依 [data-files](../common/data-files.md) 用 `wf-table/1` 資料檔。暫存保留期與清除條件見 [工具鏈](tools.md#暫存的保留與清除)。

REPORT 分清「來源已讀／headless pilot 已跑／全批次已驗／已部署／實機已驗」，附可續跑命令與未決缺口。等使用者親自做的記 [WAIT_USER](../../../WAIT_USER.md)；跨 session 的 Skyrim 續行點記 [agentctl SESSION](../../../agentctl/SESSION-LOG.md)，母 repo 文件工作才記 [SESSION-LOG](../../../SESSION-LOG.md)。
