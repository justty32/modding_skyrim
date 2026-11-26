# 鎖、螢幕與開遊戲

[lessons 索引](README.md)｜螢幕使用權（使用者在場、同機 session）見 [screen-and-user-presence](screen-and-user-presence.md)

## verify-game-alive-via-qa-not-ps

> 判斷 Skyrim 是否活著要用 qa_status 或截圖,不要用 ps comm 比對（2026-08-31）

Proton 下 `ps -eo comm=` 對 SkyrimSE 印 `Main`、MO2 印 `main`，Helldivers 2 是 `reaper`／`srt-bwrap`／`steam.exe`，比對 `^SkyrimSE.exe` 或 `grep -i skyrimse` 恆為假陰性；skse64.log 在主選單停止增長是常態不是死亡訊號。規則正本：[runtime-qa](../workflows/runtime-qa/README.md) §1、§4。

- 驗活優先順序：`qa_status`（給 game_pids）> spectacle 截圖（wayland 下 `spectacle -b -f -n -o f.png`，背景任務 PATH 可能缺）> ps。
- MO2 是單實例：重射前先確認上一條 ModOrganizer.exe 已退出，否則新鏈會靜默排隊。
- 「使用者遊戲中？」檢查一律用 args 比對：Helldivers 2 用 `ps -e -o args= | grep -c '[h]elldivers2\.exe'`；使用者是不是在玩 Skyrim 用 `ps -eo pid,etimes,args | grep -iE 'SkyrimSE\.exe|ModOrganizer\.exe' | grep -v grep`（看 etimes 判是不是別人開的）。
- 「MO2／遊戲沒在跑才能寫」的 guard 用 `ps -eo args= | grep -Ei "ModOrganizer\.exe|SkyrimSE\.exe|skse64_loader\.exe"`，交接書把這行寫死；「`ps -eo comm=` 必須為空」是錯的，別抄。

## alt-tab-during-loading-deadlocks

> 載入畫面時 alt+tab 會讓遊戲死鎖黑屏，沒有設定可調；判死鎖看 CPU 掉到個位數＋全執行緒 futex_wait（2026-09-20）

真死鎖：Loading Menu 關閉、HUD 重開那一秒後零 log，全執行緒 `futex_wait`／`poll`，CPU 掉到 2–5%，qa_state 逾時、qa_status 仍活、無 crash log。不是 mod：引擎把畫面從載入執行緒交回主執行緒時收到 WM_ACTIVATE，互搶渲染鎖。設定已是 Display Tweaks `Borderless=true`／`Fullscreen=false`、`bAlwaysActive=1`，無開關可調。

- 使用者報「黑屏卡住」：先問音樂／環境音是否持續；有就先試多次 alt+tab——無邊框鋪滿的視窗可能被 KWin 6.7（Wayland，NVIDIA 610.x 已見）當 direct scanout，present 卡住像凍結，alt+tab／Super／PrintScreen 能讓它復活，不是真死鎖（2026-10-23，`agentctl/handoffs/done/2026-10/home-2026-10-09/barter/REPORT-freeze.md`）。
- 救不回再看 `top -p <pid>` 與 `/proc/<pid>/task/*/wchan`：CPU 個位數＋全 futex＝死鎖。關遊戲前先按 CrashLogger v1.24 的 Ctrl+Shift+F12（`CrashLogger.ini` 開 Thread Dump Hotkey）留全執行緒堆疊，末態快照無法定罪（`.../barter/REPORT-hang.md`）；別追 mod。
- 只有**非載入**時 alt+tab 也卡才派線查 SKSE DLL。給使用者的判準：畫面在跑時切安全，載入／黑屏轉場時別切。

相關：[[verify-game-alive-via-qa-not-ps]]。

## launch-skyrim-via-steam
<a id="skyrim-no-appmanifest-steam-safe"></a>

> 不從 Steam 啟動 Skyrim、永不按 Verify，走開始選單「Skyrim (Modpack-KR)」或 instance/tools/launch-mo2.sh；但 SkyrimSE.exe 仍要 Steam client 常駐；AE CC 不是 Steam depot（2026-08-28；2026-09-03、09-18 補）

入口、禁令與原因的正本是 [`instance/docs/launch-and-safety.md`](../../instance/docs/launch-and-safety.md)（Play 不觸發更新但只開到 MO2 redirector、Verify 會把本體重灌成 public 版、`--skse` 無人值守直啟、`selected_profile` 是 CRLF 檔、不在 SteamLinuxRuntime 容器外呼 `proton`、非必要不開 MO2、`mo2ctl launch` 委派給 `launch-mo2.sh`）。Steam 一更新整個 SKSE 生態全毀。文件沒寫的：

- `SkyrimSE.exe` 仍需 **Steam client 常駐**（2026-09-18；`SteamAPI_Init` 失敗＋usvfs 擋掉自拉 steam.exe → 整條鏈靜默退出，log 只有 `[S_API FAIL]`）；「不經 Steam client」只對 MO2 本身成立。安全開法：確認 `appmanifest_489830.acf` 的 `AutoUpdateBehavior=1`／`StateFlags=4`／buildid 未變，`steam -silent` 起來後輪詢守衛 2 分鐘看 StateFlags／buildid 不動；收工關 Steam 或離線。啟動前若跳更新：Downloads 暫停 → Go Offline → 再啟動。
- 本體釘在 1.6.1170（exe sha `c434208894f0…`），FULL 備份 `~/skyrim_mods/steam-build-backup/489830-1.6.1170-build24604991-FULL/`，回填流程 `agentctl/handoffs/home-2026-09-03/ae/REPORT.md`；`post-ae-2026-09-03/` **沒有 BSA**，不能拿來拼 1.7.104。Verify 也會還原清理過的原版 master，見 [[vanilla-masters-cleaned-in-data]]。

**AE（appid 1746860）是無 depot 的授權旗標 DLC**：489830 的 13 個 depot 無一掛 dlcappid，Steam 永遠派不出 CC 檔，以「Steam 會派 DLC」為前提的動作（validate、勾選切換）全部無效，不要叫隊去 Steam 找 depot。CC 只能由遊戲主選單 Creations 登入 Bethesda.net 下載，讓使用者本人登入（runbook `agentctl/handoffs/home-2026-09-03/ae2/CC-RUNBOOK.md`，depot 證據 `ae2/depot-findings.md`）。下載落點見 [[cc-download-lands-in-cwd-data]]，現存 `~/skyrim_mods/cc-ae-download-2026-09-03/`。

相關：[[profile-restore-order-and-flags]]（MO2 一載入就覆寫 profile）。

## lock-lifecycle-ownership-and-broken-states

> 鎖只交領導管理；鎖目錄被殘留檔卡住、或 owner 寫已釋放但目錄還在，都不是正常佔用

mkdir 鎖只看目錄存不存在；owner 文字與狀態可能不一致，殘留不會自己清除。

- 多工人共用的鎖只讓領導層取得／釋放（2026-08-30；工人忘記釋放會害下輪卡住，`agentctl/handoffs/done/2026-08-30/dl-2026-08-30/HANDOFF-cx-dl11.md:17-27`）。
- 鎖路徑是 0 位元組普通檔時 mkdir 回 `Not a directory`，不是「已被佔用」（2026-09-11，`agentctl/handoffs/done/2026-09/home-2026-09-11/body/REPORT.md:98-100`）。
- `game.lock/` 目錄還在但 owner 寫「released」仍會擋取鎖（2026-09-18，`agentctl/handoffs/done/2026-09/home-2026-09-18/recon/REPORT.md:10`）。
- 遇到這兩種狀態先核實再清除。

## runtime-proxy-save-protection

> agent 代使用者跑實機時，存檔要能證明沒被動：saves／ini／overwrite 前後雜湊、`setini` 關計時存檔、讀檔走主選單「繼續遊戲」（主控台 `load` 在主選單可能無效，還會開出只能「新存檔」的面板）

2026-11-22 起實機線在使用者的 `modpack-main` 存檔上跑。使用者的存檔是唯一不能重來的東西；計時自動存檔、旅行存檔、誤點存檔面板都會寫新檔或覆蓋。主控台 `load Save342` 在主選單無效，還可能開出只有「新的進度檔」的存檔面板，點下去就存檔（[waituser-runtime REPORT](../../agentctl/handoffs/home-2026-11-22/waituser-runtime/REPORT.md)、[ferry-repro REPORT](../../agentctl/handoffs/home-2026-11-22/ferry-repro/REPORT.md)）。

- 開場前與每場後：`saves/` 逐檔 sha256、三個 ini md5、overwrite 檔案清單、modlist 雜湊各存一份，收線比對（各實機線的 `guard.sh` 在 `~/skyrim_mods/_backups/handoff-data-2026-11-22/` 下）。
- 讀檔後 `setini "fAutosaveEveryXMins:SaveGame" 999`、`bDisableAutoSave 1`，`getini` 回讀確認；`bSaveOnTravel` 等在 1.6.1170 `getini` 查不到，靠 profile 的 `skyrimprefs.ini` 本來就是 0。
- 讀檔走主選單「繼續遊戲」，以金幣數等確認讀對檔；看到存檔面板只有「新的進度檔」就 Esc，不點。
- 規則入口在 [runtime-qa](../workflows/runtime-qa/README.md)。
