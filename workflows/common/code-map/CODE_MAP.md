# CODE_MAP — 原始碼導航

本母 repo 主要保存分析與工作流文件；可建置的原始碼位於 `projects/` 的獨立
repo/submodule。修改前先從下表進目標專案，遵守該專案自己的 README、AGENTS 與
CODE_MAP。不存在的根層 source tree 不另造索引。

## 專案入口

| 專案 | 程式碼／文件入口 |
|------|------------------|
| ModForge | [`projects/ModForge/workflows/common/code-map/CODE_MAP.md`](../../../projects/ModForge/workflows/common/code-map/CODE_MAP.md) — generator domain、CLI、schema、tests 的完整分域索引 |
| agent-bridge | [`projects/agent-bridge/README.md`](../../../projects/agent-bridge/README.md) — SKSE HTTP runtime；[`client/README.md`](../../../projects/agent-bridge/client/README.md) — Linux client/MCP；[`QA-SCHEMA.md`](../../../projects/agent-bridge/client/QA-SCHEMA.md) — qa.json contract |
| scene-capture-bridge | [`projects/scene-capture-bridge/README.md`](../../../projects/scene-capture-bridge/README.md) — SKSE runtime；`src/CatalogFile.*` + `tests/CatalogFileTests.cpp` 是不依賴 SKSE 的 ModForge scene-catalog v1 parser/FormKey index/provenance+runtime global-source-order gate/metadata merge；`tests/RunModForgeCatalogContract.cmake` 另以真實 ModForge CLI 串 full/light plugin→catalog exporter bytes→consumer 的 MinGW CTest，`tests/CatalogCompatibilityProbe.cpp` 可把真實 catalog／resolved path list 餵進同一 consumer gate；`Catalog.cpp` 由 `TESDataHandler::files` 取得 full/light 全域 loaded sequence，kDataLoaded 後把合格離線 EditorID/name 補進 Browser |
| godot-worldspace-editor | [`projects/godot-worldspace-editor/README.md`](../../../projects/godot-worldspace-editor/README.md) — `godot/placements_io.gd` 是 placements producer；`tests/test_placements_contract.py` 以 Godot headless 真實 exporter→ModForge CLI→ESP REFR 讀回；`godot/model_fetch.gd` 優先遵守 `MODFORGE_NIF2GLTF_BIN` executable hook 並 fail-closed 管理 `.gltf + .bin` cache，`tests/test_model_fetch_contract.py` 以 synthetic NIF→production converter→Godot `GLTFDocument` 驗 mesh/座標與壞輸出清理重試 |
| model-converter | [`projects/model-converter/README.md`](../../../projects/model-converter/README.md) — `PROTOCOL.md` 定義 nif2gltf/gltf2nif 黑盒 CLI；前者由 Godot ModelFetch live contract 消費，後者由 darksouls-port production batch live contract 消費 |
| skyrim-voicegen | [`projects/skyrim-voicegen/README.md`](../../../projects/skyrim-voicegen/README.md) — `voicegen.py` 是 ModForge TTS 黑盒 producer；`tests/fake_fish_engine.py` 只作 live contract 最末端 fixture，ModForge `VoiceLiveContractTests.cs` 真跨 process 驗完整 args、合法 WAV 與 failure cleanup |
| game-data | [`projects/game-data/README.md`](../../../projects/game-data/README.md) — `extract.sh` 先做全 batch stem collision preflight，再以 sibling staging + paired backup/rollback 原子發布 gamedata/questnodes；`tests/test_extract.py` 用會真寫檔的 fake dotnet 驗 known-good 保留與零半成品 |
| darksouls-port | [`projects/darksouls-port/README.md`](../../../projects/darksouls-port/README.md) — `tools/p1_batch.py` 以同目錄 staging 呼 sibling production gltf2nif，失敗撤下 stale packageable target；`tests/test_model_converter_contract.py` 再用 model-converter production reader 驗 BSTriShape、材質、座標及 bhk hull |
| sofia-patch | [`projects/sofia-patch/README.md`](../../../projects/sofia-patch/README.md) |
| my_skyrim_plugin_1 | [`projects/my_skyrim_plugin_1/README.md`](../../../projects/my_skyrim_plugin_1/README.md) — DaylightDungeon SKSE plugin；`scripts/test_packaging.ps1` 以 synthetic CMake cache/DLL 驗 CI/PowerShell/bash 打包命名與 MO2 layout contract |
| houseCARL（本機、非 submodule） | [`projects/houseCARL/README.md`](../../../projects/houseCARL/README.md)；Linux 適配結論在 [`linux-manjaro-mo2-runbook.md`](../../../analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md) |

## agent-bridge semantic QA 快速圖

| 類別 | 檔案 | 職責 |
|------|------|------|
| Runtime | `projects/agent-bridge/src/GameActions.*`, `MessageBox.*`, `StateActors.*`, `State.*`, `Routes.*` | game-thread actor/dialogue/MessageBox actions、structured state、HTTP contract |
| Linux client | `projects/agent-bridge/client/bridge.py`, `qa_runner.py`, `qa_mcp.py` | HTTP calls、declarative QA steps、MCP semantic tools |
| Tests | `projects/agent-bridge/client/test_bridge.py`, `test_qa_runner.py`, `test_qa_mcp.py` | request shape、retry/validation、MCP routing |
| Docs | `projects/agent-bridge/README.md`, `client/README.md`, `client/QA-SCHEMA.md` | runtime API、client entry、qa.json contract |

新增／刪除原始碼檔案或改變職責時，先更新目標 repo 的 CODE_MAP；目標 repo 沒有
細分 CODE_MAP 時，才維護本頁的快速圖或 README 入口。

## 母 repo 本機工具

| 檔案 | 職責 |
|---|---|
| `scripts/resolve_load_order.py` | 把唯一 `Modpack-KR` 的 enabled `loadorder.txt` 解析成真實 plugin paths；provider precedence 是 shared `overwrite` → `modlist.txt` 最高優先 enabled mod → game `Data`，任何 enabled missing plugin 以非零 exit fail closed |
| `tests/test_resolve_load_order.py` | synthetic MO2 tree 驗 overwrite winner、named-mod priority、implicit master 與 disabled／missing plugin 行為 |
| `scripts/build_vigilant_book_desc_overlay.py` | 以指定版本的 VIGILANT 正體 plugin 同時作結構 seed 與術語來源，只補齊精確 45 筆仍為英文的 `BOOK.DESC`；筆數、record topology 與所有非目標 payload 都 fail closed，並輸出逐筆 ledger |
| `agentctl/tools/agent_inbox/inbox_send.sh` | Codex 工作線以固定 frontmatter／STATUS 契約原子發布完成、阻塞或進度訊息到執行期 inbox |
| `agentctl/tools/agent_inbox/inbox_read.sh` | 無副作用、空 inbox 完全靜默的未讀訊息摘要，供調度者與 `UserPromptSubmit` hook 使用 |
| `agentctl/tools/agent_inbox/notify_watch.sh` | 每 20 秒靜默輪詢新訊息與受監看 tmux session，對新信、消失 session 及兩輪確認的孤兒狀態各通知一次 |
