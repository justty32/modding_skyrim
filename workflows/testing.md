# testing — 測試入口

把本專案所有常用驗證指令放這裡。agent 能跑的測試應自己跑；不能跑的記到 [../WAIT_USER.md](../WAIT_USER.md)。

開始前寫 `Done when: <指定測試/驗證命令跑完，結果已回報>`。

## 母 repo 驗證

母 repo 主要是 Markdown、索引與 submodule gitlink，另有一個 Python stdlib 文件驗證器；
沒有統一 build。改文件時至少跑：

```bash
python -m unittest discover -s tests -v
python scripts/check_markdown_links.py
git diff --check
git status --short --branch
git submodule status
```

GitHub 的 `Documentation checks` 跑同一組 unittest，link checker 則加 `--skip-symlinks`：
兩份 `.md` symlink 的 canonical 文件住在 ModForge submodule，而目前 recursive checkout 會先被
三個未發布 gitlink 擋住。本機完整 gate 仍不跳過 symlink；submodule 發布修好後再讓 CI 初始化
ModForge 並移除這個選項。

`git submodule status` 行首空白代表 checkout 與母 repo gitlink 一致；`+` 代表不一致，`-` 代表
尚未初始化。fresh clone 或母 repo gitlink 更新後再跑：

```bash
git submodule update --init --recursive
```

## 常用離線測試

以下命令都從表中的 repo 根目錄執行。數量是 2026-08-12 在家用 Manjaro 的基線；之後新增
測試時以 exit status 為準，不要把舊數量當上限。

| repo | 命令 | 本機基線／範圍 |
|---|---|---|
| `ModForge` | `./scripts/test-offline.sh` | 1123 pass；排除 `RequiresSkyrim` |
| `agent-bridge` | `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s client -p 'test*.py' -v` | 54 pass；stdlib-only Linux client、無需 MO2/遊戲 |
| `game-data` | `python -m unittest discover -s tests -v` | 12 pass；fake dotnet，無需遊戲資料 |
| `skyrim-voicegen` | `python -m unittest discover -s tests -v` | 6 pass；不載 TTS 模型 |
| `model-converter` | `.venv/bin/python -m pytest` | 68 pass；若無 POSIX venv，依該 repo README 建環境 |
| `darksouls-port` | `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v` | 系統 Python 缺 numpy 時會 skip 12 個碰撞單測 |
| `godot-worldspace-editor` | `python tests/test_placements_contract.py` | source gate 必跑；缺 Godot 時 runtime 明示 skip |
| `godot-worldspace-editor` | `python tests/test_model_fetch_contract.py` | model-converter→Godot live contract；缺 Godot時 skip |

`darksouls-port` 若同層 `model-converter/.venv` 已存在，可用它補跑完整 25 項：

```bash
PYTHONDONTWRITEBYTECODE=1 ../model-converter/.venv/bin/python \
  -m unittest discover -s tests -v
```

`agent-bridge` 的 Windows DLL 可在家用 Manjaro 以唯一支援的 clang-cl+xwin 路線驗證，
不部署到 MO2：

```bash
export VCPKG_ROOT="$HOME/vcpkg"
cmake --fresh --preset build-release-clang-cl-linux
cmake --build build/release-clang-cl-linux
file build/release-clang-cl-linux/AgentBridge.dll
```

2026-08-12 基線為 build 成功，輸出 `PE32+` x86-64 DLL。`--fresh` 是為清除 2026-08-02
搬離 `ModForge/sub_projs` 前留下的絕對 source cache；不會修改原始碼或部署遊戲。

其他 repo 的測試入口以各自 README／工作流為準，不在母 repo 複製容易過期的命令：

- `agent-bridge`：上表只驗 Linux client；SKSE DLL 另依 README 走 Linux clang-cl+xwin cross-build。
- `scene-capture-bridge`：portable CTest、MinGW contract 與 Linux clang-cl+xwin DLL build 的環境不同。
- `my_skyrim_plugin_1`：以 README 的 CMake/CTest 與 packaging contract 為準。
- `houseCARL`：母 repo 釘自有 fork 的 `fix/dialogue-encoding-lint`；建置與 HTTP explicit-path 驗證見
  [`analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md`](../analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md)。
- `sofia-patch`：內容／文件專案，沒有統一自動化 suite。

## 測試分類

- `fast`：目標 repo 自己的 unit/source-gate；每次小改都跑。
- `contract`：跨 sibling repo 的真實 CLI/process boundary；改 producer、consumer 或 protocol 時跑。
- `full`：目標 repo README 指定的完整離線 suite；commit 前或大改後跑。
- `external`：需要 Skyrim、MO2、Godot GUI、遊戲素材、模型、帳號或人工感官驗收；不能由
  agent 代跑的項目記到 [../WAIT_USER.md](../WAIT_USER.md)。

## 已知環境條件

- 這台未安裝 Godot；兩個 Godot contract 的 source gate 會通過，runtime class 會明示 skip。
- 系統 Python 沒有 numpy；`darksouls-port` 的 12 個碰撞單測會 skip。使用上面的
  `model-converter/.venv` 命令可跑滿 25/25。
- ModForge 離線 suite 目前會輸出既有 nullable/xUnit analyzer warnings，但 1123 項全過。
- 母 repo `b95ee0d` 指到三個尚未 push 的子模組 commit，recursive update 會失敗；精確 SHA
  與修復步驟見 [../WAIT_USER.md](../WAIT_USER.md)。這是發布狀態，不要誤判成測試 regression，
  也不要把 gitlink 倒退來掩蓋。

## 何時不用

- 只是查測試指令，直接讀本檔回答。
- 測試是 feature/refactor 的一部分，不需要另開測試工作流；在原工作流內執行即可。
