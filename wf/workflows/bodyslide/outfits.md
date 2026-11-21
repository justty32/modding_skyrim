# 刷衣服 — 指定服裝的增量 BodySlide 建置

[BodySlide 母流程](README.md)｜[headless 命令](headless.md)

**何時用**：「刷這件衣服／這套裝備」「新裝的衣服要套身形」「只重刷某群組」；產物是選定服裝的獨立 output 層。
**何時不用**：沒有適配專案的裝備不能靠 Batch Build 自動轉換；找轉換包走 [nexus-intake](../nexus-intake/README.md)，製作新轉換另立任務。只換身體或私有 NPC 裸身走母流程。

## Done when

`Done when:` 開始時填入一件、一套或精確群組名稱，以及固定 preset／動態 morph 的目標；完成時：

- scope manifest 存在，含裝備記錄到實際模型路徑、對應 project／變體／來源、同輸出決議及本輪預期集合。
- 本輪隔離輸出與驗證報告存在，列出 low／high、morph、缺件及不適用項目；未解釋的路徑差異為 0。
- 增量部署／回退計畫存在；有授權且已部署時，附每個目標 winner／hash 與實機驗收狀態。

## 流程

### 1. 把「這件／這套」變成實際路徑

先按母流程凍結輸入與授權，不把整個 installed group 當作已授權範圍。單件從 ARMO 的精確 FormKey／EDID 或可定位名稱開始；套裝列出實際要穿的各件，含手套／靴／配件；群組則先展開並審核成員，排除不在本輪範圍的裸身及其他裝備。

讀取真實贏家 ARMO → Armature 的 ARMA，查適用性別／種族、第三人稱模型及需要時的第一人稱模型；ARMO world/inventory 模型不要當成穿在身上的模型。NPC outfit 可由 NPC_／OTFT 追到 ARMO，但只刷玩家裝備時不需要 NPC_ gate。透過既有 `whichmod.py`、houseCARL 或唯讀解析工具定位，具體介面先看工具索引／`--help`，不假造子命令。

將目標相對模型路徑與 OSP `OutputPath`／`OutputFile` 比對，確認遊戲真的會載入此 project 的輸出。再記現役 VFS 中模型、OSP、ShapeData、OSD 與 preset 各自的 winner／hash。裝備本體和 BodySlide 轉換包可能不同來源；只看到相同服裝名稱不代表使用同一版。缺少專案或來源不相容時保留缺口，不把另一個名字相似的 project 當作修復。

### 2. 決定變體與身形路線

先在**尚未過濾變體**的合併 staging 跑唯讀 planner，從母 repo 根目錄執行：

```bash
: "${BS_TOOL_DIR:?請設定已合併的隔離 BodySlide 資源目錄}"
python tools/bodyslide_outfit_plan.py --staging "$BS_TOOL_DIR" \
  --project 'CT77 Farm Clothes 4' --tri
```

換成本輪精確 XML 名稱；多件重複 `--project`。工具不修改 staging；exit 0／`ok=true` 只代表其靜態預檢通過。`conflicts` 是**已選 project** 的共同輸出，須先裁決；`unselected_variants` 是尚未選取、會寫同路徑的候選，不能自動當成衝突或預設勝者。若 staging 已縮成單件，此欄空白不能證明其他來源沒有變體。

工具列出必要 NIF／OSD 等 source candidates，處理獨立 OSP v1，僅驗來源存在；不解 MO2／封裝、NIF／OSD 內容、preset/zap、OBody 或 runtime。`conditional_outputs` 的 TRI 是候選，不保證必產生；查看 `limitations`／`uninspected_projects` 後再判定是否需其他工具。

同一件可能有 CBBE／3BA、物理／無物理、袖子／裸露、zap 等變體；依已裝本體、骨架及本輪目標選一個，對每個共同輸出路徑明訂勝者。群組只用來選已審核 project，不解決 variant 衝突。若單件有多個必要 project，依輸出集合一併納入，不以「只刷一件」誤縮成一個 project。

動態 OBody 路線：依現役設定刷明確的零滑條基底與需要的 TRI，核對所有適用 small／big 值；名字叫 Zeroed 不能取代實際值驗證。固定身形路線：用精確 preset 的 low／high；是否產生 TRI 取決於是否仍需 runtime morph，不能把兩條路線無條件混刷。嵌入衣服的身體 shape、裸身及其他同穿部件要採相容基底，避免穿脫時身形跳變。

不能只靠私有目錄判定排除 OBody；只有本輪涉及私有 NPC 時才查其模型指向、排除設定及既存 morph。沒有物理或 zap 的 project，不強加物理／zap 驗收；單一權重專案也不要求虛構 `_0`／`_1` 配對。

### 3. 小範圍試刷與增量

重用 [headless](headless.md) 的私有 staging、未修改 OSP＋原生 `-p`、精確 group、空 output 及 safe-fallback 設定。每個 project 的預期檔案先算清楚，`-tri` 依需要加入。先試一件代表服裝，驗證 preset 存在並作用；本機已驗證同 binary 的通用 A／B 哨兵可重用，但新專案若缺 slider、使用 zap 或特殊 morph，仍需針對該語義補驗。

增量以來源／project／preset／選項及輸出映射的變化為準，不用整個 profile 全刷。把新增、改變、移除或改名的輸出路徑和上輪 manifest 比較，留下本輪預期集合與差異。新建空的本輪 output，避免舊 NIF／TRI 被誤算成成功；部署時不能只覆蓋新增檔而留下已不適用的舊檔。移除舊輸出先備份／提出明確差異，仍走授權與安全套用。

### 4. 驗收與可交付結果

逐 project 保存本輪 log、退出碼、輸入與產物 hash；比對實際／預期路徑集合，再解析適用的 NIF／TRI。核對 shape、材質路徑、skin／骨架、權重配對；有 TRI 才查 BODYTRI 指向、morph shape／頂點索引。內嵌身體、物理骨及 zap 只驗本輪實際包含的項目；解析器只支持 position morph 時列明 UV 等未驗部分，不冒稱完整 TRI 語義通過。

隔離建置通過後才產出獨立 output 層、覆蓋差異與回退清單；沿母流程的 [授權部署與回退](README.md#5-授權部署與回退) 進施工窗。重新解析實際裝備 ARMA 路徑與 VFS winner，確認穿到的是本輪產物，不只看檔案複製成功。

實機依本輪範圍穿／脫單件與整套、必要的 low／high 體重，觀察破洞、穿模、接縫與動作；有物理才看物理、有動態 morph 才驗 morph。只驗一件不得標成全套已驗。失敗先分辨裝備記錄／路徑、winner、來源變體、建置語義或運行時問題，再回退受影響 output；不擅改 ARMO／ARMA 或全域 preset 來掩蓋錯配。

## 交接

沿母流程保存 scope manifest、增量差異、驗證與 REPORT；若未部署，標「隔離服裝建置已驗」，不標已刷入遊戲。待使用者操作或跨 session 的記錄仍走母流程，不在本頁累積 open 清單。

## 本機實例

[Farm Clothes 4 的來源選擇與真實衣服驗證](outfit-evidence.md)含 CT77 現役與 CBBE 對照。
