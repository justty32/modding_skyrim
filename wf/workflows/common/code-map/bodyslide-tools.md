# BodySlide 工具鏈 — 原始碼導航

[CODE_MAP](CODE_MAP.md)｜用法 [bodyslide/tools](../../bodyslide/tools.md)

母 repo `tools/` 下，stdlib only、從參數或環境變數取路徑。每支 `test_<名>.py` 在同目錄，`python -m unittest discover -s tools -p "test_bodyslide*.py"`。

| 檔案 | 職責 |
|---|---|
| `tools/bodyslide_guard.py` | 共用守門：參數或環境變數取 live 根，realpath 雙向比對、ASCII 檢查 |
| `tools/bodyslide_stage.py` | 照 modlist 優先序大小寫不敏感合併各 mod 的 BodySlide 資源成真複本樹＋`wf-table/1` 來源表；容量 gate |
| `tools/bodyslide_outfit_plan.py` | 唯讀預檢 OSP project 的輸出、衝突、未選變體與來源缺項；大小寫變體 fail-closed |
| `tools/bodyslide_sandbox_run.py` | 一輪 headless `-gbuild`：bwrap 唯讀根、唯一可寫 run 目錄、停網路、Xvfb＋私有 prefix；`result.json` |
| `tools/bodyslide_mesh_check.py` | NIF partition 實際頂點、PIRT TRI 解析與 A／B／B-repeat 比對 |

整範圍重建與 OBody（用法見 [換身體](../../bodyslide/body-swap.md)）：

| 檔案 | 職責 |
|---|---|
| `tools/bodyslide_rebuild.py` | 設定檔（`bodyslide-rebuild/1`）驅動 stage→plan→build→verify→layer→obody 一行重建 |
| `tools/bodyslide_select.py` | 寬鬆 OSP 目錄、批次選件（projects／osp_mods／stems／舊層／scope 表）、同輸出裁決、group 與 BuildSelection XML |
| `tools/bodyslide_layer.py` | 批次驗收（路徑集合、抽樣 NIF／TRI／BODYTRI、舊層頂點比對、內嵌身體貼合）、硬連結組層、manifest |
| `tools/bodyslide_fit.py`、`tools/bodyslide_fit_model.py` | 私有身體擬合成 preset（[擬合](../../bodyslide/fit.md)）：OSD／OSP 線性模型、帶界限最小平方、殘差與判定、批次、BODYTRI 改指；測試 `test_bodyslide_fit.py`（含 Aela 正控） |
| `tools/bodyslide_obody_config.py` | OBody NG 覆蓋層：NPC→preset 表轉差量 preset、npcFormID、黑名單與隨機池；schema 子集驗證 |
| `agentctl/tools/bodyslide_scope_scan.py`（private） | 現役 ARMO→ARMA 女性 mesh、VFS 贏家、`.tri`、OSP 對應的 scope 表（rebuild 的 `select.scope` 讀它） |
