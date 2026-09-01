# 回家第一場執行單（2026-09-01）

順序採「已有可交付產物 → 獨立環境 gate → 單組 archive gate → 現役 winner patch →
4–6 件生態 preflight」。這是本單依剩餘相依與接觸面做的排序：DMK 已有離線 PASS 產物但未部署／
實機驗收，scene-capture-bridge 卡在指定 Windows MinGW 環境，Mihail 則要逐件處理 4–6 組輸入
（`agentctl/handoffs/rtqa-2026-08-31/reports/dmk.md:46`；
`agentctl/handoffs/rtqa-2026-08-31/reports/dmk.md:50`；
`agentctl/handoffs/wu-2026-08-31/CLEANUP.md:43`；`wait-user/home-setup.md:14`）。

## 1. DMK 1.5.0 人工校對版

**前置條件。** 手上要有 exact official ZIP、exact CHS 7z、7z、OpenCC，以及
`mod-library/l10n/tools/build_dmk_cht_layer.py`；兩個 exact archive 的既定 Linux 路徑在
`agentctl/handoffs/rtqa-2026-08-31/HANDOFF-cx-rq1-dmk.md:10`、`:11`、`:12`，builder 的五個必要參數在
`mod-library/l10n/tools/build_dmk_cht_layer.py:168`、`:169`、`:170`、`:171`、`:172`。目前可直接接續的
人工校對成品是 `agentctl/handoffs/rtqa-2026-08-31/dmk-build/DMK-1.5.0-Traditional-Chinese-Human-Reviewed.7z`；
它已離線重建 PASS，inventory 只有 `Data/Viny Mods/DMK/Language.json`
（`agentctl/handoffs/rtqa-2026-08-31/reports/dmk.md:46`；`:50`；`:52`）。

**實際動作。** 先完全關閉 Skyrim／MO2，再照 profile 工作流開 `feat/*`；入口指令是：

```bash
cd /home/lorkhan/repo/moddings/skyrim/instance/profiles
python3 -B tools/profile_workflow.py status
python3 -B tools/profile_workflow.py start feat/<主題>-<日期>
```

`<主題>` 的本次固定名稱 repo 內未記錄，回家現場確認；指令模板與「執行期間不得切 branch」的限制見
`instance/profiles/tools/README.md:17`、`:18`、`:19` 與 `instance/profiles/README.md:33`。用 MO2 安裝上述
人工校對 archive 成獨立層，停用現役 `Directional Movement Keys Traditional Chinese 1.5.0 Machine Private 2026-08-21`，
並讓新層位於 `Directional Movement Keys 1.5.0 Dev 2026-08-21` 之上；現役兩個名稱與優先關係見
`instance/profiles/manifest.json:3063`、`:3080`、`:3089`。`mo2ctl install <archive> --priority
"before:<本體 mod 名>"` 是 repo 記錄的覆蓋層安裝形式，但新層的 `--name` repo 內未記錄，回家現場確認
（`wf/workflows/nexus-intake/README.md:116`；`:121`；`:122`）。從 Steam 點 Skyrim SE、在 MO2 按 Run，
抽查一般設定、相機、PC／手把按鍵、OAR converter 警告，再做移動 smoke
（`wf/workflows/runtime-qa/README.md:24`；`wait-user/home-setup.md:42`；`:43`）。

**通過條件。** `human_reviewed_zh_tw`、66 reviewed、38 override、0 unresolved；不另加數字
（`wait-user/home-setup.md:40`；`:41`）。

**失敗退路。** 任一計數不合即停，不部署該重建物；若部署後 UI／移動異常，停用新層並恢復舊 DMK 本體／
machine CHT 的既定啟用組合，再維持原 `plugins.txt`／`loadorder.txt` 順序
（`agentctl/logs/mcm-helper-dmk-cht-install-2026-08-21.md:36`；`:37`；`:38`；`:39`）。

**預估時間。** 25–45 分鐘（本單估算）；依據是離線重建、token／JSON／archive gate 已經 PASS，剩餘工作集中在
部署與指定 smoke（`agentctl/handoffs/rtqa-2026-08-31/reports/dmk.md:58`；`:59`；`:60`）。

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

## 4. Bandolier NPC 中文 forward patch（已作廢 —— 2026-09-01 使用者裁示 Bandolier 併入 clothes purge）

**本節不執行，前置條件已不存在。**

**前置條件。** 要有現役 Bandolier NPC 八顆 plugins、Classic 本體、CHS seed archive、現役
`modpack-main/plugins.txt`、Python 與 7z；builder 已把這些 Linux 路徑寫死
（`mod-library/l10n/tools/build_bandolier_for_npc_chinese_layer.py:25`；`:26`；`:34`；`:38`；`:41`）。
CHS seed 與本體／NPC plugins 還有 size／SHA-256 pin，來源一變就不應硬跑
（`mod-library/l10n/tools/build_bandolier_for_npc_chinese_layer.py:47`；`:50`；`:54`；`:62`）。

**實際動作。** 在 repo 根執行：

```bash
python3 mod-library/l10n/tools/build_bandolier_for_npc_chinese_layer.py
```

腳本是無參數 entry point（`mod-library/l10n/tools/build_bandolier_for_npc_chinese_layer.py:535`；`:536`），會先核對現役
plugin 啟用集合，異動即 fail closed（`:152`；`:157`；`:159`；`:160`）。完成後用實際 load-order winner 工具核對
83 unique＋23 realistic 兩批，並保存 record 對帳與 plugin gate；該 winner 工具的本案專用命令 repo 內未記錄，
回家現場確認（`modpack-design/archive/content-plan/zh-layer/zh-layer-coverage/unresolved-and-rulings/rulings.md:16`；`:19`）。
注意 builder ledger 的內部 `220 = 220 + 0` 不是本案寫死的 106 winner gate，不能拿來替代
（`mod-library/l10n/mods/BandolierForNPC-Chinese-3.3.0-Dev-2026-08-30/tools/ledger.json:11`；
`wait-user/home-setup.md:24`；`:25`）。

**通過條件。** 106 個目標字串全由 patch 贏得、93 個 NPC 層 ARMO 不再顯示英文，且 NPC 分發與
less-common／realistic variant 都保留；保存 record 對帳與 plugin gate 證據
（`wait-user/home-setup.md:25`；`:26`）。

**失敗退路。** builder 若報 `SOURCE MISMATCH` 或 winner 數不合即停，不改 pin、不部署部分 patch；腳本的
fail-closed 訊息在 `mod-library/l10n/tools/build_bandolier_for_npc_chinese_layer.py:364`。保留現役 NPC 分發與英文狀態，
待 actual archives／plugins 對齊後重做，不能用排序假裝救回中文
（`modpack-design/archive/content-plan/zh-layer/zh-layer-coverage/unresolved-and-rulings/rulings.md:9`；`:11`）。

**預估時間。** 45–75 分鐘（本單估算）；依據是 builder 已存在，但仍需對 106 targets 做現役 winner 對帳
（`wait-user/home-setup.md:23`；`:24`；`:25`）。

## 5. Mihail 自然核心首批 4–6 件 preflight

**前置條件。** 先從自然核心候選 Pigeons、Frogs、House Cats、Ring-necked Pheasants、Crows and Ravens、Swans
凍結本晚 4–6 件；六件的 base／exact 中文版本列在
`agentctl/handoffs/done/2026-08-29/cx-mihail/REPORT.md:92`、`:93`、`:94`、`:95`、`:96`、`:97`。
具體要哪 4–6 件 repo 內尚未記錄，回家現場確認；手上必須同時有每件 base／中文 archives，以及可讀
CELL／worldspace、asset 與 records 的工具環境（`wait-user/home-setup.md:14`；`:15`）。

**實際動作。** 一次只做一件：記錄 base／中文 archive 身分並分開解壓；確認 exact 中文對版；掃
CELL／worldspace placement、asset winner 與 records；再逐一檢查新增 ingredient／food、actor stats／ability／
combat style 對 Apothecary 與現役 EnaiRim 的接觸面。每件都寫出獨立回滾單位與 winner／patch 結論
（`wait-user/home-setup.md:15`；`:16`；`:17`）。本案 xEdit／asset 掃描的具體命令 repo 內未記錄，回家現場確認；
repo 只明確要求施工前對選中子集做 xEdit／asset preflight
（`agentctl/handoffs/done/2026-08-29/cx-mihail/REPORT.md:76`）。不得加入全域 SkyPatcher 分布；它會把 hand-placed
spawns 改成另一個 topology（`wait-user/home-setup.md:16`；
`agentctl/handoffs/done/2026-08-29/cx-mihail/REPORT.md:59`；`:63`）。

**通過條件。** 每件都有可回滾單位、exact 中文對版與明列的 winner／patch 結論，CELL／asset／record 衝突及
Apothecary／Enai 接觸面全數有處置，才能排入施工（`wait-user/home-setup.md:17`；`:18`）。

**失敗退路。** 單件未過即從首批排除，不把它排入施工；若剩餘通過者仍有 4–6 件，可只交付該合格批，少於 4 件則
整批停在 preflight，不用 SkyPatcher 補數（批次範圍與 topology 邊界見 `wait-user/home-setup.md:14`、`:16`、`:18`）。

**預估時間。** 2–4 小時（本單估算）；依據是 4–6 件都要逐件做 placement／asset／record 與兩套 gameplay 語意面，
不能把一件 PASS 外推到其餘候選（`wait-user/home-setup.md:14`；`:15`；`:16`；`:17`）。

## 今晚如果只做得完一件

做 **DMK 1.5.0 人工校對版**。理由是 exact archives 的離線重建已 PASS、成品與 gate 都在 repo，寫死的
66／38／0 也已逐項對上；目前真正剩下的是替換未校對機翻層並做指定 UI／移動 smoke，完成路徑最短且能直接消除
現役 machine translation（`agentctl/handoffs/rtqa-2026-08-31/reports/dmk.md:46`；`:50`；`:60`；`:70`；`:71`；`:72`；
`agentctl/logs/mcm-helper-dmk-cht-install-2026-08-21.md:22`；`:24`；`:25`；`:26`）。
