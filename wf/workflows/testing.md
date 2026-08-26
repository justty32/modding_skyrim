# testing — 測試入口

把本專案所有常用驗證指令放這裡。agent 能跑的測試應自己跑；不能跑的記到 [../WAIT_USER.md](../../WAIT_USER.md)。

開始前寫 `Done when: <指定測試/驗證命令跑完，結果已回報>`。

## 母 repo 驗證

母 repo 主要是 Markdown、索引與 submodule gitlink，另有一個 Python stdlib 文件驗證器；
沒有統一 build。改文件時至少跑：

```bash
python -m unittest discover -s tools -p "test_*.py" -v
python tools/check_markdown_links.py
git diff --check
git status --short --branch
git submodule status
```

GitHub 的 `Documentation checks` 跑同一組 unittest，link checker 則加 `--skip-symlinks`。

`git submodule status` 行首空白代表 checkout 與母 repo gitlink 一致；`+` 代表不一致，`-` 代表
尚未初始化。fresh clone 或母 repo gitlink 更新後再跑：

```bash
git submodule update --init --recursive
```

## 常用離線測試

以下命令都從表中的 repo 根目錄執行。表格文字不是同一天寫出的，逐列如下：
`ModForge`、`agent-bridge`（Linux client 一列）、`darksouls-port`、
`my_skyrim_plugin_1`（兩列）與 `scene-capture-bridge` 的**命令欄**是 **2026-08-26**
實測後改寫的（見
[`offline-test-matrix-2026-08-26`](../../agentctl/logs/offline-test-matrix-2026-08-26.md)）；
`game-data`、`skyrim-voicegen`、`model-converter`、`godot-worldspace-editor`（兩列）與
`scene-capture-bridge` 的**通過數量**沿用 2026-08-12 的原始基線——這幾個 submodule 的
gitlink 自 2026-08-12 起未再變動、程式碼沒改，數字本來就不會變。2026-08-26 稍晚已把這
六列實際重跑一遍逐格核對（同一份記錄新增的「測試矩陣查證·第二輪」章節），結果與
2026-08-12 的舊值完全一致，不是照抄舊文件。下面 `agent-bridge` 的 Windows DLL
clang-cl+xwin 段落也是 **2026-08-26** 由另一條線複驗、本線套用文字更正
（`VCPKG_ROOT` 路徑寫錯、`--fresh` 保留理由換了）。之後新增測試時以 exit status
為準，不要把舊數量當上限。

| repo | 命令 | 本機基線／範圍 |
|---|---|---|
| `ModForge` | `./scripts/test-offline.sh` | 1190 pass；排除 `RequiresSkyrim` |
| `agent-bridge` | `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s client -p 'test*.py' -v` | 88 pass；stdlib-only Linux client、無需 MO2/遊戲 |
| `game-data` | `python -m unittest discover -s tests -v` | 12 pass；fake dotnet，無需遊戲資料 |
| `skyrim-voicegen` | `python -m unittest discover -s tests -v` | 6 pass；不載 TTS 模型 |
| `model-converter` | `.venv/bin/python -m pytest` | 68 pass；若無 POSIX venv，依該 repo README 建環境 |
| `model-converter` (Windows) | `.venv\Scripts\python.exe -m pytest` | 68 pass；Windows 等價命令 |
| `darksouls-port` | `PYTHONDONTWRITEBYTECODE=1 ./venv/bin/python -m unittest discover -s tests -p "test_*.py" -v` | 35 pass；**測試在 `tests/` 不是 `tools/`，且必須用 repo 自帶的 `venv/`**——系統 Python 缺 numpy，會變成 2 error / 19 skip |
| `scene-capture-bridge` | `ctest --test-dir build/tests-native --output-on-failure` | 2 pass（Linux native）。`build/portable-tests-mingw` 是 **Windows MinGW** 的目錄，這台機器上不存在；完整 x64 triplet 尚缺 |
| `my_skyrim_plugin_1` | `./scripts/test_quest_prf.sh` | 25 pass；quest PRF primitives，純 stdlib g++，不需 SKSE／CommonLib／Windows。Windows 對等物是 `scripts/test_quest_prf.ps1` |
| `my_skyrim_plugin_1` | `./scripts/test_packaging.sh` | 10 pass；`pack.sh` 的打包契約（zip 內路徑佈局、`--output-dir` 防護、CLI exit code）。Windows 對等物 `test_packaging.ps1` 測的是 `pack.ps1`，兩支打包腳本各自獨立 |
| `godot-worldspace-editor` | `python tests/test_placements_contract.py` | source gate 必跑；缺 Godot 時 runtime 明示 skip |
| `godot-worldspace-editor` | `python tests/test_model_fetch_contract.py` | model-converter→Godot live contract；缺 Godot時 skip |

`agent-bridge` 的 Windows DLL 可在家用 Manjaro 以唯一支援的 clang-cl+xwin 路線驗證，
不部署到 MO2：

```bash
export VCPKG_ROOT="/home/lorkhan/dev/vcpkg"
cmake --fresh --preset build-release-clang-cl-linux
cmake --build build/release-clang-cl-linux
file build/release-clang-cl-linux/AgentBridge.dll
```

2026-08-26 複驗：configure 1s、build 9s，輸出
`PE32+ executable for MS Windows 6.00 (DLL), x86-64, 9 sections`。
前提是 `~/.xwin-cache` 已 splat（`crt/` + `sdk/`，約 630M），缺了會在 configure 期
FATAL_ERROR 並附上重建命令。

`--fresh` **不可省略**：preset 以裸名 `clang-cl` 指定編譯器，CMake 入 cache 時會解析成
絕對路徑，第二次 configure 因兩者不等而中途自毀重跑，此時 compiler probe 已失去 xwin
toolchain 的 include／libpath，必然報「Check for working CXX compiler - broken」。
這是 preset 的結構性問題，與任何一次目錄搬遷無關——舊文件說 `--fresh` 是為了清
2026-08-02 搬離 `ModForge/sub_projs` 前留下的絕對路徑 cache，這個理由已經過期：
2026-08-26 複驗現有 cache 對 `ModForge|sub_projs` 命中 0 筆，`--fresh` 仍然必留，只是
理由換了。

其他 repo 的測試入口以各自 README／工作流為準，不在母 repo 複製容易過期的命令：

- `agent-bridge`：上表只驗 Linux client；SKSE DLL 另依 README 走 Linux clang-cl+xwin cross-build。
- `scene-capture-bridge`：portable CTest、MinGW contract 與 Linux clang-cl+xwin DLL build 的環境不同。
- `my_skyrim_plugin_1`：**沒有 CTest 入口**（`CMakeLists.txt` 沒有 `enable_testing()`／`add_test`，Linux cross-build 目錄也沒有 `CTestTestfile.cmake`），不要拿 build 成功當測試通過。但有可直接跑的離線測試——見上表 `test_quest_prf.sh`。
- `houseCARL`：只維護自有 fork、不追 upstream；建置與 HTTP explicit-path 驗證見
  [`analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md`](../../analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md)。
- `sofia-patch`：內容／文件專案，沒有統一自動化 suite。

## 測試分類

- `fast`：目標 repo 自己的 unit/source-gate；每次小改都跑。
- `contract`：跨 sibling repo 的真實 CLI/process boundary；改 producer、consumer 或 protocol 時跑。
- `full`：目標 repo README 指定的完整離線 suite；commit 前或大改後跑。
- `external`：需要 Skyrim、MO2、Godot GUI、遊戲素材、模型、帳號或人工感官驗收；不能由
  agent 代跑的項目記到 [../WAIT_USER.md](../../WAIT_USER.md)。

## 已知環境條件

- 這台未安裝 Godot；兩個 Godot contract 的 source gate 會通過，runtime class 會明示 skip。
- `darksouls-port` 用 repo 自帶的 `venv/` 是 35/35 全過（2026-08-26 實測）。用系統 Python 會變成
  2 error / 19 skip（缺 numpy）——**那不是 repo 壞了，是跑錯直譯器**。
- ModForge 離線 suite 目前會輸出既有 nullable/xUnit analyzer warnings，但 1190 項全過。

## 何時不用

- 只是查測試指令，直接讀本檔回答。
- 測試是 feature/refactor 的一部分，不需要另開測試工作流；在原工作流內執行即可。

## 綠燈不等於有檢查

**一道檢查通過，可能是因為它根本沒在檢查。** 這不是假設，2026-08-23 一天抓到四個：

| 檢查 | 為什麼恆真 |
|---|---|
| `check_profiles.py`（歷史） | 2026-08-23 之前只看 profile 目錄，**不看 `ModOrganizer.ini`**。ini 曾停在 codex 線留下的 `PandoraRuntimeDefer-20260822`（一個不存在的 profile），每次都 PASS。已於 2026-08-23 的 `instance/profiles` commit `241522d`（`feat(tools): validate selected_profile against the canonical name`）修正，新增 `selected_profile_errors()` 讀 `ModOrganizer.ini` 的 `selected_profile=`，與宣告的 `CANONICAL_PROFILE` 不符就擋下 |
| teardown 的「遊戲鎖已釋放」 | 鎖的路徑指向已被刪除的 `~/skyrim_agent_out/_lock/`——**檢查一個不可能存在的東西，永遠會過** |
| `check_markdown_links.py`（歷史） | `git ls-files` 到 gitlink 就停，四條線的 87 個壞連結它從來沒看到；後續也發現只驗檔案存在、沒有驗 `#anchor`。**兩者都已修（gitlink；anchor 於 `26dd4f7`）。2026-08-26 以突變測試複驗：實作是真的會變紅，但測試本身有四個空隙（標題內 inline link、anchor 側 fenced code、closed ATX 尾綴、一行死碼），已於 `76df55f` 補齊，13/13 突變體全殺。** |
| 自製的 CJK 偵測 | `b.decode('utf-8', errors='ignore')` **永遠不拋錯**，所以「依序試多種編碼、成功就 break」的迴圈第一輪就結束，根本沒試過 cp936 |

### 規則：新增或修改一道檢查時，要證明它能變紅

```sh
# 餵一個「應該被擋」的輸入，確認 exit != 0
SKYRIM_MO2_INSTANCE="$fake" python3 tools/check_profiles.py; echo $?   # 應為 1
# 再餵正確的，確認 exit == 0
```

沒做過這個雙向驗證的檢查，不要拿它的綠燈當證據。

### 兩個相關的推論

- **檢查器的涵蓋範圍要跟著結構走。** 拆出 submodule、搬走目錄之後，
  要回頭確認檢查器還看得到那些地方。
- **靜態全過不等於畫面上是對的。** 方框、mojibake、截斷、手感只有人眼看得出來；
  這類項目記到 [WAIT_USER.md](../../WAIT_USER.md)，不要自己宣稱通過。
