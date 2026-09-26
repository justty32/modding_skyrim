# 鎖、螢幕與開遊戲（2/3）

[lessons 索引](README.md)｜同主題：[locks-screen-and-game](locks-screen-and-game.md)、[locks-screen-and-game-3](locks-screen-and-game-3.md)

## skyrim-no-appmanifest-steam-safe

> Skyrim SE 的 appmanifest 已放回、Play 不觸發更新但 Verify 會重灌；AE CC 內容不是 Steam depot，只能遊戲內 Creations 登入 Bethesda.net 下載（原 type: memory）

2026-09-03 AE 兩輪後的事實（原 08-28 那條「無 appmanifest 所以 Steam 入口作廢」已過時）：

- `steamapps/appmanifest_489830.acf` 已放回，`buildid`＝public（24914197）、`StateFlags 4`、`AutoUpdateBehavior=1`。**Play 不會觸發更新**（唯一問題是會開到 MO2 redirector）；**會重灌本體的是 Verify／`steam://validate`**（實測 37 分鐘、5.27 GB，限速 20000 Kbps）。
- 本體維持 1.6.1170（exe sha `c434208894f0…`），FULL 備份在 `~/skyrim_mods/steam-build-backup/489830-1.6.1170-build24604991-FULL/`，回填流程在 `agentctl/handoffs/home-2026-09-03/ae/REPORT.md`；`post-ae-2026-09-03/` **沒有 BSA**，不能拿來拼 1.7.104。
- **AE（appid 1746860）是「無 depot 的授權旗標 DLC」**：已買、DLC 分頁已勾，但 489830 的 13 個 depot 無一掛 dlcappid，Steam 永遠派不出 CC 檔。70 件 CC 只能由遊戲主選單 Creations 登入 Bethesda.net 下載（需使用者本人帳密）。**09-03 晚使用者已抓到 70/75 件**，但落在啟動時 cwd 的 `data/`，見 [[cc-download-lands-in-cwd-data]]；現存 `~/skyrim_mods/cc-ae-download-2026-09-03/`。runbook 在 `agentctl/handoffs/home-2026-09-03/ae2/CC-RUNBOOK.md`，depot 證據在 `ae2/depot-findings.md`。

**Why:** 三次以「Steam 會派 DLC」為前提的動作（validate、勾選切換）全部無效，浪費了一輪隊；docs 裡「Play＝更新」的句子也曾誤導判斷。
**How to apply:** 想拿 CC 就照 runbook 讓使用者親手登入；不要再叫隊去 Steam 找 depot。維持 1.6.1170 期間仍不按 Verify；Play 可用但沒必要（走 `instance/tools/launch-mo2.sh --skse`）。相關：[[launch-skyrim-via-steam]]。

## verify-game-alive-via-qa-not-ps

> 判斷 Skyrim 是否活著要用 qa_status 或截圖,不要用 ps comm 比對（原 type: feedback）

2026-08-31 事故:遊戲其實一直活在主選單,但 `ps -eo comm=` 比對 `^SkyrimSE.exe` 抓不到(Proton 下行程名不如預期),加上 skse64.log 在主選單停止增長,連續誤判成「靜默退出」,浪費 15 分鐘追假 bug 還重射三次(全被 MO2 單實例卡死)。

**Why:** wine/Proton 行程的 comm 呈現不可靠;SKSE 日誌凍結是主選單常態不是死亡訊號。

**How to apply:** 驗活優先順序:`qa_status`(給 game_pids)> spectacle 截圖(wayland 下 `spectacle -b -f -n -o f.png` 可用,背景任務 PATH 可能缺)> ps。另外 [[launch-skyrim-via-steam]] 的鏈裡 MO2 是單實例:重射前先確認上一條 ModOrganizer.exe 已退出,否則新鏈會靜默排隊。

**2026-09-01 事故補充**：偵測 Helldivers 2（及所有 Proton 遊戲）是否在跑，`ps -eo comm=` 恆為偽陰性——HD2 的 comm 是 `reaper`／`srt-bwrap`／`steam.exe`。正確寫法：`ps -e -o args= | grep -c '[h]elldivers2\.exe'`。這次因此誤判 HD2 未開而放行 Skyrim smoke，搶了使用者畫面。開實機窗口前的「使用者遊戲中？」檢查一律用 args 比對。

**2026-09-05 補**：實測 `ps -eo comm=` 下 MO2 是 `main`、SkyrimSE 是 `Main`（Proton）。任何「MO2／遊戲沒在跑才能寫」的 guard 要用 `ps -eo args= | grep -Ei "ModOrganizer\.exe|SkyrimSE\.exe|skse64_loader\.exe"`；四條 codex 線同一天全寫錯，交接書要把這行寫死。

**2026-09-20 補（lead-fde920 自己被騙一次）**：Proton 下 `ps -eo comm=` 對 SkyrimSE 印 `Main`、MO2 印 `main`，
`grep -i skyrimse` 永遠假陰性。要驗「使用者是不是在玩」用
`ps -eo pid,etimes,args | grep -iE 'SkyrimSE\.exe|ModOrganizer\.exe' | grep -v grep`（看 etimes 判是不是別人開的）。
交接書範本裡「`ps -eo comm=` 必須為空」那句是錯的，別再抄。

## alt-tab-during-loading-deadlocks

> 2026-09-20 載入畫面時 alt+tab 讓遊戲死鎖黑屏；設定已是無邊框＋bAlwaysActive=1 無可調；判死鎖看 CPU 掉到個位數＋全執行緒 futex_wait（原 type: memory）

2026-09-20 19:25 使用者切地圖時 alt+tab → 黑屏永久卡住。不是 mod：Loading Menu 關閉、HUD 重開的那一秒後零 log，所有執行緒 `futex_wait`／`poll`，CPU 從 160% 掉到 2–5%，qa_state 逾時、qa_status 仍活、無 crash log。設定已是 Display Tweaks `Borderless=true`／`Fullscreen=false`、`bAlwaysActive=1`，Proton 9.0-203，沒有開關可調。

**Why:** 引擎把畫面從載入執行緒交回主執行緒的瞬間收到 WM_ACTIVATE，兩邊互搶渲染鎖；Windows 也會、Wine 更容易。

**How to apply:** 使用者報「黑屏卡住」先看 `top -p <pid>` 與 `/proc/<pid>/task/*/wchan`：CPU 個位數＋全 futex＝死鎖，直接 kill，別等、別追 mod；只有在**非載入**時 alt+tab 也卡才值得派線查 SKSE DLL。判準給使用者：畫面在跑時切安全，載入／黑屏轉場時別切。相關：[[verify-game-alive-via-qa-not-ps]]。
