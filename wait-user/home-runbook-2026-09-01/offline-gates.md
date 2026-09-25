## 2. scene-capture-bridge 完整離線測試

**前置條件。** 必須是能跑 Windows MinGW `x64-mingw-static` vcpkg build 的環境；Linux native 2/2 不能冒充此 gate
（`agentctl/handoffs/wu-2026-08-31/CLEANUP.md:43`）。該環境需有 CMake、MinGW、vcpkg，且
`tests/vcpkg.json` 只要求 `nlohmann-json`（`projects/scene-capture-bridge/BUILD.md:26`；`:27`；
`projects/scene-capture-bridge/BUILD.md:43`；`:44`）。

**實際動作。** 在 Windows PowerShell、`projects/scene-capture-bridge` 根目錄照 repo 原指令執行：

```powershell
$env:PATH='C:\dev\mingw64\bin;' + $env:PATH
$env:VCPKG_ROOT='C:\dev\vcpkg'
cmake -S tests -B build/portable-tests-mingw -G 'MinGW Makefiles' `
  -DCMAKE_MAKE_PROGRAM=C:/dev/mingw64/bin/mingw32-make.exe `
  -DCMAKE_CXX_COMPILER=C:/dev/mingw64/bin/g++.exe `
  -DCMAKE_TOOLCHAIN_FILE=C:/dev/vcpkg/scripts/buildsystems/vcpkg.cmake `
  -DVCPKG_TARGET_TRIPLET=x64-mingw-static `
  -DVCPKG_HOST_TRIPLET=x64-mingw-static
cmake --build build/portable-tests-mingw --parallel
ctest --test-dir build/portable-tests-mingw --output-on-failure
```

來源逐行在 `projects/scene-capture-bridge/BUILD.md:30` 至 `:40`；若本機工具不在 `C:\dev`，替代路徑 repo 內未記錄，
回家現場確認，不自行假裝已有該環境。

**通過條件。** 完整 `x64-mingw-static` nlohmann-json triplet 的 configure／build 完成，且該環境下 CTest 2/2 PASS；
既有 portable 2/2 不替代這次缺口（`wait-user/home-setup.md:30`；`:31`）。

**失敗退路。** 缺環境或 vcpkg 依賴即停並維持 open；不得改測試掩蓋缺依賴
（`wait-user/home-setup.md:31`）。

**預估時間。** 30–60 分鐘（本單估算，從完整 configure 到 CTest；首次 vcpkg 實耗 repo 內未記錄，回家現場計時），
估算範圍只涵蓋 `BUILD.md` 已列的三段指令（`projects/scene-capture-bridge/BUILD.md:33`；`:39`；`:40`）。

## 3. SDA 4.3.2 exact 簡中 topology gate

**前置條件。** SDA 4.3.2 official archive 與 Nexus `78511` 簡中 `4.3.2v1.2` exact archive；該中文層只有
版本字串 exact，尚未過 binary topology gate（`wait-user/home-setup.md:6`；`:7`；
`agentctl/handoffs/done/2026-08-29/cx-serana/REPORT.md:183`）。另需能列 archive inventory、解壓與做 plugin
semantic binary diff 的工具；本案專用工具名稱／命令 repo 內未記錄，回家現場確認。

**實際動作。** 先對兩包各跑 `7z l '<archive>'` 並保存 inventory，再解到兩個分離暫存目錄；`7z l` 作 archive
真偽 gate 與 `7z x -y -o<dir> <archive>` 的既有用法分別見
`agentctl/handoffs/rtqa-2026-08-31/HANDOFF-cx-rq1-dmk.md:13`、
`mod-library/l10n/tools/build_dmk_cht_layer.py:186`、`:187`。接著核對 plugin basename／masters、archive 內
scripts／assets；對 official plugin 與簡中 plugin 比對 record totals、各型計數、FormID set、GRUP／subrecord topology
及非文字 payload，只有本地化文字 payload 可以不同（`agentctl/handoffs/done/2026-08-29/cx-serana/REPORT.md:222`；
`:223`；`wf/workflows/nexus-intake/README.md:64`；`:66`；`:67`）。證據檔落點 repo 內未記錄，回家現場確認。

**通過條件。** 版本與 master 對版、中文層只改預期文字面、沒有舊版 record／script／asset 回滾；證據落檔後才可進部署
（`wait-user/home-setup.md:8`；`:9`）。

**失敗退路。** 任一非文字差異、master／版本錯配或舊 payload 回滾即停，不部署；不得退回把 4.1.1.3 繁中 ESP 當
4.3.2 runtime 層（`agentctl/handoffs/done/2026-08-29/cx-serana/REPORT.md:184`；
`wf/workflows/nexus-intake/README.md:70`）。

**預估時間。** 45–90 分鐘（本單估算）；依據是兩包 inventory 加一組 plugin／script／asset 與 semantic payload 對帳，
不是重翻 8,000+ 行（`agentctl/handoffs/done/2026-08-29/cx-serana/REPORT.md:183`）。

