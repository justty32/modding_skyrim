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
