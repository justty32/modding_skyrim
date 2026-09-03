# 常用離線測試矩陣

[testing](../testing.md)

以下命令都從表中的 repo 根目錄執行。表內通過數是 2026-08-26 的歷史基線；現行命令、環境與
通過數以各 repo README 和本次 exit status 為準，不把舊數量當上限。

欄位：`repo`／`命令`／`本機基線／範圍`。共 19 筆，已抽到 [`offline-matrix.json`](offline-matrix.json)。

## agent-bridge 的 Windows DLL

`agent-bridge` 的 Windows DLL 可在家用 Manjaro 以唯一支援的 clang-cl+xwin 路線驗證，
不部署到 MO2：

```bash
export VCPKG_ROOT="/home/lorkhan/dev/vcpkg"
cmake --fresh --preset build-release-clang-cl-linux
cmake --build build/release-clang-cl-linux
file build/release-clang-cl-linux/AgentBridge.dll
```

本機基線：configure 1s、build 9s，輸出
`PE32+ executable for MS Windows 6.00 (DLL), x86-64, 9 sections`。
前提是 `~/.xwin-cache` 已 splat（`crt/` + `sdk/`，約 630M），缺了會在 configure 期
FATAL_ERROR 並附上重建命令。

`--fresh` **不可省略**：preset 以裸名 `clang-cl` 指定編譯器，CMake 入 cache 時會解析成
絕對路徑，第二次 configure 因兩者不等而中途自毀重跑，此時 compiler probe 已失去 xwin
toolchain 的 include／libpath，必然報「Check for working CXX compiler - broken」。
這是 preset 的結構性問題。

## 不在母 repo 複製命令的 repo

其他 repo 的測試入口以各自 README／工作流為準，不在母 repo 複製容易過期的命令：

- `agent-bridge`：上表只驗 Linux client；SKSE DLL 另依 README 走 Linux clang-cl+xwin cross-build。
- `scene-capture-bridge`：portable CTest、MinGW contract 與 Linux clang-cl+xwin DLL build 的環境不同。
- `my_skyrim_plugin_1`：**沒有 CTest 入口**（`CMakeLists.txt` 沒有 `enable_testing()`／`add_test`，Linux cross-build 目錄也沒有 `CTestTestfile.cmake`），不要拿 build 成功當測試通過。但有可直接跑的離線測試——見上表 `test_quest_prf.sh`。
- `houseCARL`：現行測試閘門、安裝與 explicit-path 設定從
  [`agentctl/docs/housecarl.md`](../../../agentctl/docs/housecarl.md) 進場，再依該 repo README 執行；
  不以這張歷史基線表取代現況。
- `sofia-patch`：內容／文件專案，沒有統一自動化 suite。
