# CODE_MAP — 原始碼導航

本母 repo 主要保存分析與工作流文件；可建置的原始碼位於 `projects/` 的獨立
repo/submodule。修改前先從下表進目標專案，遵守該專案自己的 README、AGENTS 與
CODE_MAP。不存在的根層 source tree 不另造索引。

## 專案入口

| 專案 | 程式碼／文件入口 |
|------|------------------|
| ModForge | [`projects/ModForge/workflows/common/code-map/CODE_MAP.md`](../../../projects/ModForge/workflows/common/code-map/CODE_MAP.md) — generator domain、CLI、schema、tests 的完整分域索引 |
| agent-bridge | [`projects/agent-bridge/README.md`](../../../projects/agent-bridge/README.md) — SKSE HTTP runtime；[`client/README.md`](../../../projects/agent-bridge/client/README.md) — Linux client/MCP；[`QA-SCHEMA.md`](../../../projects/agent-bridge/client/QA-SCHEMA.md) — qa.json contract |
| scene-capture-bridge | [`projects/scene-capture-bridge/README.md`](../../../projects/scene-capture-bridge/README.md) — SKSE runtime；`src/CatalogFile.*` + `tests/CatalogFileTests.cpp` 是不依賴 SKSE 的 ModForge scene-catalog v1 parser/FormKey index 與 MinGW CTest |
| godot-worldspace-editor | [`projects/godot-worldspace-editor/README.md`](../../../projects/godot-worldspace-editor/README.md) |
| model-converter | [`projects/model-converter/README.md`](../../../projects/model-converter/README.md) |
| skyrim-voicegen | [`projects/skyrim-voicegen/README.md`](../../../projects/skyrim-voicegen/README.md) |
| game-data | [`projects/game-data/README.md`](../../../projects/game-data/README.md) |
| darksouls-port | [`projects/darksouls-port/README.md`](../../../projects/darksouls-port/README.md) |
| sofia-patch | [`projects/sofia-patch/README.md`](../../../projects/sofia-patch/README.md) |
| my_skyrim_plugin_1 | [`projects/my_skyrim_plugin_1/README.md`](../../../projects/my_skyrim_plugin_1/README.md) |
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
