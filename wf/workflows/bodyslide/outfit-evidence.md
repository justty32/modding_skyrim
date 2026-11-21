# 服裝隔離試刷證據

[刷衣服](outfits.md)｜[共同證據](evidence.md)

## 本機例：Farm Clothes 4 的替換來源

2026-11-18 唯讀調查：`03452E:Skyrim.esm`（`ClothesFarmClothes04`）→ `03452C:Skyrim.esm`（`FarmerTorso04AA`），ARMA winner 是 `Remodeled Armor - Vanilla Replacer.esp`。女性第三人稱模型為 `Clothes\FarmClothes04\robef_1.nif`，第一人稱為同目錄 `1stPersonrobef_1.nif`；`robef_0/1.nif` 的現役 winner 是 CT77 output。

候選 `CT77 Farm Clothes 4` 與 `CBBE Vanilla - Body - Farm Clothes 4` 都輸出 `robef`；前者來源 `CT77FarmClothes.osp`，DataFolder `CT77FarmClothes`、SourceFile `CT77FarmClothes4.nif`。這不是無害的同名 project：用 CBBE output 覆蓋 CT77，可能把現役裝備形制換回另一個來源。必須先決定保留 CT77 還是有意換來源，不能默認選 CBBE 即完成現役衣服刷新。

同時核對兩個候選實際輸出集合；只重建第三人稱 `robef` 不代表第一人稱模型也更新。兩個來源可分別在隔離目錄試刷、比較，沒有授權與來源選擇決議前均不部署。記錄解析的依據為本輪 houseCARL／VFS 唯讀輸出摘要，不把解析結果當作穿模或遊戲外觀驗收。

## 2026-11-18 兩套真實服裝試刷

兩輪配方均複製來源 OSP，保留 root `version="1"` 與選定 SliderSet 的 slider／zap／輸出語義，只縮成單件；用 Clothes A／B 將 Breasts small／big 分別設為 0／100，其他值留原 default。專用 prefix／Xvfb（關 GLX）、原生 `-gbuild ... -p ... -tri -t ...`，各自跑 A、B、B repeat，三輪 exit 0 並完成。這是選定 loose-file staging，不是完整 MO2 VFS。

現役 **CT77 Farm Clothes 4** 的衣服 shape `FC4`，low／high 各在 2,627 頂點中有 522 個改變，最大距離約 2.050293；TRI 的 FC4 有 117 個 position morph，Breasts 的 522 個 delta 非零。來源依賴跨 `CT77FarmClothes`、`CT77Shared`、`SE 3BBB Amazing` 三個 ShapeData 目錄；planner 實跑辨出四個必要 NIF／OSD，缺 CT77Shared 的負例回 `ok=false`，不能只按 SourceFile 所在目錄複製資源。

比較用 **CBBE Vanilla - Body - Farm Clothes 4** 的真實衣服 shape `dress_1`，low／high 各在 2,570 點中有 848 點改變，最大距離約 2.25259；TRI 有 97 個 position morph。驗的是衣服頂點本身，不只內嵌身體有變。

兩套各輸出且僅輸出 `meshes/clothes/farmclothes04/robef_0.nif`、`robef_1.nif`、`robef.tri`，B repeat 三檔相對路徑與 SHA-256 全同。A／B 的 TRI hash 相同且含非零 Breasts morph，與基底值改變但 morph 基底相同一致；不能把「TRI hash 不變」當成 preset 沒作用。

驗證器沿 BSTriShape→BSDismemberSkinInstance→NiSkinPartition 解實際命名 shape 頂點；來源基礎為 `projects/model-converter/nif2gltf/nif_reader.py:_read_header` 與 `_blocks.py:_read_bstrishape`。position morph 索引界內且 scale 有限，尾端 UV section 當時未解碼（2026-11-21 起 `bodyslide_mesh_check.py` 已解）。未驗材質、skin weights、物理／zap 視覺、OBody 策略或遊戲貼合；此非建議部署非零全域基底。

## 重現與邊界

11-18 兩套試刷的原件（`/tmp` 下的 probe 目錄與其 `prepare.py`／`validate.py`／`results.json`）**已刪，結論保留**；當時的 SE 3BBB Amazing ShapeData 是 3BA 能力試驗的依賴，不代表現役身體家族（現役是 CBBE 2.0.3，見 [部署](deploy.md#1-先查現役贏家)）。要重現就用 [工具鏈](tools.md)：`bodyslide_stage.py` 照 modlist 合併、planner 點名 ShapeData、`bodyslide_sandbox_run.py` 跑 A／B／B-repeat、`bodyslide_mesh_check.py compare --tri-check --expect-changed FC4` 驗衣服 shape；後者已解 TRI 的 UV 段。2026-11-21 以新解析器重讀 11-18 留存的 `robef_0.nif` 抽樣：`FC4` 2,627 頂點、4 個 partition、inline count 0，TRI 117 morph、尾端 0 bytes，與上表一致。

當時來源 hash 重查無變、safe-fallback 空、live output／profile／DB 未改。一個失敗原型曾遺漏 OSP root `version="1"`，無輸出且以自身精確 PID 停止；縮寫測試 fixture 也必須保存版本語義。CBBE 只作對照，沒有取代 CT77 現役來源，也未產生第一人稱模型；兩套都尚未部署／實機驗收。另有一份 11-18 的 CT77 output 暫存不在 bwrap 內建置、用大小寫敏感路徑取第一個啟用 mod 當來源，不能直接當部署來源；要用就以工具鏈重建。
