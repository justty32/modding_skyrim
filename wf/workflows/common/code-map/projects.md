# 專案入口

[原始碼導航](CODE_MAP.md) 的專案入口索引。

<!-- wf-nav -->

| 專案 | 程式碼／文件入口 |
|------|------------------|
| ModForge | [`projects/ModForge/workflows/common/code-map/CODE_MAP.md`](../../../../projects/ModForge/workflows/common/code-map/CODE_MAP.md) — generator domain、CLI、schema、tests 的完整分域索引 |
| agent-bridge | [`projects/agent-bridge/README.md`](../../../../projects/agent-bridge/README.md) — SKSE HTTP runtime；[`client/README.md`](../../../../projects/agent-bridge/client/README.md) — Linux client/MCP；[`QA-SCHEMA.md`](../../../../projects/agent-bridge/client/QA-SCHEMA.md) — qa.json contract |
| scene-capture-bridge | [`projects/scene-capture-bridge/README.md`](../../../../projects/scene-capture-bridge/README.md) — SKSE runtime；`src/CatalogFile.*` + `tests/CatalogFileTests.cpp` 是不依賴 SKSE 的 ModForge scene-catalog v1 parser/FormKey index/provenance+runtime global-source-order gate/metadata merge；`tests/RunModForgeCatalogContract.cmake` 另以真實 ModForge CLI 串 full/light plugin→catalog exporter bytes→consumer 的 MinGW CTest，`tests/CatalogCompatibilityProbe.cpp` 可把真實 catalog／resolved path list 餵進同一 consumer gate；`Catalog.cpp` 由 `TESDataHandler::files` 取得 full/light 全域 loaded sequence，kDataLoaded 後把合格離線 EditorID/name 補進 Browser |
| godot-worldspace-editor | [`projects/godot-worldspace-editor/README.md`](../../../../projects/godot-worldspace-editor/README.md) — `godot/placements_io.gd` 是 placements producer；`tests/test_placements_contract.py` 以 Godot headless 真實 exporter→ModForge CLI→ESP REFR 讀回；`godot/model_fetch.gd` 優先遵守 `MODFORGE_NIF2GLTF_BIN` executable hook 並 fail-closed 管理 `.gltf + .bin` cache，`tests/test_model_fetch_contract.py` 以 synthetic NIF→production converter→Godot `GLTFDocument` 驗 mesh/座標與壞輸出清理重試 |
| model-converter | [`projects/model-converter/README.md`](../../../../projects/model-converter/README.md) — `PROTOCOL.md` 定義 nif2gltf/gltf2nif 黑盒 CLI；前者由 Godot ModelFetch live contract 消費，後者由 darksouls-port production batch live contract 消費 |
| skyrim-voicegen | [`projects/skyrim-voicegen/README.md`](../../../../projects/skyrim-voicegen/README.md) — `voicegen.py` 是 ModForge TTS 黑盒 producer；`tests/fake_fish_engine.py` 只作 live contract 最末端 fixture，ModForge `VoiceLiveContractTests.cs` 真跨 process 驗完整 args、合法 WAV 與 failure cleanup |
| game-data | [`projects/game-data/README.md`](../../../../projects/game-data/README.md) — `extract.sh` 先做全 batch stem collision preflight，再以 sibling staging + paired backup/rollback 原子發布 gamedata/questnodes；`tests/test_extract.py` 用會真寫檔的 fake dotnet 驗 known-good 保留與零半成品 |
| darksouls-port | [`projects/darksouls-port/README.md`](../../../../projects/darksouls-port/README.md) — `tools/p1_batch.py` 以同目錄 staging 呼 sibling production gltf2nif，失敗撤下 stale packageable target；`tests/test_model_converter_contract.py` 再用 model-converter production reader 驗 BSTriShape、材質、座標及 bhk hull |
| sofia-patch | [`projects/sofia-patch/README.md`](../../../../projects/sofia-patch/README.md) |
| my_skyrim_plugin_1 | [`projects/my_skyrim_plugin_1/README.md`](../../../../projects/my_skyrim_plugin_1/README.md) — DaylightDungeon SKSE plugin；打包與離線測試在 `scripts/`，**PowerShell 與 POSIX 各一套、彼此獨立**：`pack.ps1`／`pack.sh` 打包，`test_packaging.ps1`／`test_packaging.sh` 驗打包契約（synthetic CMake cache/DLL、zip 內 MO2 layout、`--output-dir` 防護、CLI exit code），`test_quest_prf.ps1`／`test_quest_prf.sh` 驗 quest PRF primitives（純 stdlib g++，不需 SKSE／CommonLib） |
| houseCARL | [`projects/houseCARL/README.md`](../../../../projects/houseCARL/README.md)；Linux 適配結論在 [`linux-manjaro-mo2-runbook.md`](../../../../analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md) |

