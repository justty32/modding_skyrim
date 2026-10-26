# 鎖、螢幕與開遊戲

[lessons 索引](README.md)

## skyrim-no-appmanifest-steam-safe

> Skyrim SE 的 appmanifest 已放回、Play 不觸發更新但 Verify 會重灌；AE CC 內容不是 Steam depot，只能遊戲內 Creations 登入 Bethesda.net 下載（2026-09-03，原 type: memory）

<!-- wf-nav -->
- `steamapps/appmanifest_489830.acf` 已放回，`buildid`＝public（24914197）、`StateFlags 4`、`AutoUpdateBehavior=1`。**Play 不會觸發更新**（唯一問題是會開到 MO2 redirector）；**會重灌本體的是 Verify／`steam://validate`**（實測 37 分鐘、5.27 GB，限速 20000 Kbps）。
- 本體維持 1.6.1170（exe sha `c434208894f0…`），FULL 備份在 `~/skyrim_mods/steam-build-backup/489830-1.6.1170-build24604991-FULL/`，回填流程在 `agentctl/handoffs/home-2026-09-03/ae/REPORT.md`；`post-ae-2026-09-03/` **沒有 BSA**，不能拿來拼 1.7.104。
- **AE（appid 1746860）是「無 depot 的授權旗標 DLC」**：已買、DLC 分頁已勾，但 489830 的 13 個 depot 無一掛 dlcappid，Steam 永遠派不出 CC 檔。70 件 CC 只能由遊戲主選單 Creations 登入 Bethesda.net 下載（需使用者本人帳密）。已下載的 70/75 件落在啟動時 cwd 的 `data/`，見 [[cc-download-lands-in-cwd-data]]；現存 `~/skyrim_mods/cc-ae-download-2026-09-03/`。runbook 在 `agentctl/handoffs/home-2026-09-03/ae2/CC-RUNBOOK.md`，depot 證據在 `ae2/depot-findings.md`。

**Why:** 以「Steam 會派 DLC」為前提的動作（validate、勾選切換）全部無效。
**How to apply:** 想拿 CC 就照 runbook 讓使用者親手登入；不要叫隊去 Steam 找 depot。維持 1.6.1170 期間不按 Verify；Play 可用但沒必要（走 `instance/tools/launch-mo2.sh --skse`）。相關：[[launch-skyrim-via-steam]]。

## verify-game-alive-via-qa-not-ps

> 判斷 Skyrim 是否活著要用 qa_status 或截圖,不要用 ps comm 比對（2026-08-31，原 type: feedback）

**Why:** wine/Proton 行程的 comm 呈現不可靠：Proton 下 `ps -eo comm=` 對 SkyrimSE 印 `Main`、MO2 印 `main`，Helldivers 2 是 `reaper`／`srt-bwrap`／`steam.exe`，比對 `^SkyrimSE.exe` 或 `grep -i skyrimse` 恆為假陰性；skse64.log 在主選單停止增長是常態不是死亡訊號。

**How to apply:**
- 驗活優先順序：`qa_status`（給 game_pids）> spectacle 截圖（wayland 下 `spectacle -b -f -n -o f.png` 可用，背景任務 PATH 可能缺）> ps。
- [[launch-skyrim-via-steam]] 的鏈裡 MO2 是單實例：重射前先確認上一條 ModOrganizer.exe 已退出，否則新鏈會靜默排隊。
- 開實機窗口前的「使用者遊戲中？」檢查一律用 args 比對：Helldivers 2 用 `ps -e -o args= | grep -c '[h]elldivers2\.exe'`；要驗使用者是不是在玩 Skyrim 用 `ps -eo pid,etimes,args | grep -iE 'SkyrimSE\.exe|ModOrganizer\.exe' | grep -v grep`（看 etimes 判是不是別人開的）。
- 任何「MO2／遊戲沒在跑才能寫」的 guard 用 `ps -eo args= | grep -Ei "ModOrganizer\.exe|SkyrimSE\.exe|skse64_loader\.exe"`，交接書要把這行寫死；「`ps -eo comm=` 必須為空」那句是錯的，別抄。

## alt-tab-during-loading-deadlocks

> 2026-09-20 載入畫面時 alt+tab 讓遊戲死鎖黑屏；設定已是無邊框＋bAlwaysActive=1 無可調；判死鎖看 CPU 掉到個位數＋全執行緒 futex_wait（原 type: memory）

症狀：Loading Menu 關閉、HUD 重開的那一秒後零 log，所有執行緒 `futex_wait`／`poll`，CPU 從 160% 掉到 2–5%，qa_state 逾時、qa_status 仍活、無 crash log。不是 mod。設定已是 Display Tweaks `Borderless=true`／`Fullscreen=false`、`bAlwaysActive=1`，Proton 9.0-203，沒有開關可調。

**Why:** 引擎把畫面從載入執行緒交回主執行緒的瞬間收到 WM_ACTIVATE，兩邊互搶渲染鎖；Windows 也會、Wine 更容易。

**How to apply:** 使用者報「黑屏卡住」先看 `top -p <pid>` 與 `/proc/<pid>/task/*/wchan`：CPU 個位數＋全 futex＝死鎖，直接 kill，別等、別追 mod；只有在**非載入**時 alt+tab 也卡才值得派線查 SKSE DLL。判準給使用者：畫面在跑時切安全，載入／黑屏轉場時別切。相關：[[verify-game-alive-via-qa-not-ps]]。

假死鎖（2026-10-23）：無邊框鋪滿螢幕的視窗可能被 KWin 6.7（Wayland，NVIDIA Blackwell 驅動 610.x 已見）當成 direct scanout 候選，present 卡住時主執行緒跟著停，外觀像整個凍結，但 alt+tab／Super／PrintScreen 能讓 KWin 退出 scanout 復活——這不是真死鎖。判準：先問音樂/環境音有沒有持續播放，有就先試多次 alt+tab 而非直接 kill（`agentctl/handoffs/done/2026-10/home-2026-10-09/barter/REPORT-freeze.md`）。確認是真死鎖（alt+tab 救不回）時，關遊戲前先按 CrashLogger v1.24 的 Ctrl+Shift+F12（需 `CrashLogger.ini` 開 Thread Dump Hotkey）留下全執行緒堆疊，不要直接關掉——只有 futex_wait 末態快照拿不到卡住瞬間的呼叫鏈，無法定罪（`agentctl/handoffs/done/2026-10/home-2026-10-09/barter/REPORT-hang.md`）。

## user-present-screen-is-still-usable

> 2026-08-30 放寬、2026-09-09 /goal 重申：使用者在電腦前時鍵盤滑鼠螢幕歸他，但 agent 可以開遊戲／MO2／瀏覽器，他會 alt+tab 切回去；只有不能暫停的遊戲（如 Helldivers 2）才是禁區（原 type: user）

2026-08-30 使用者原話：

> 我坐在電腦前的時候，**agent 可以用熒幕**，因爲他啓動遊戲後，雖然遊戲會占據熒幕，
> 但我會**立刻 alt+tab 切回我正在做的事情**。除非我是在打 **helldivers 2 這種不能暫停的遊戲**，
> 不然都 OK。

2026-09-09 /goal 重申（同一條，措辭更明確）：

> 我人坐在電腦前，鍵盤滑鼠螢幕歸我，但可以開遊戲, mo2, 瀏覽器。

**Why:** 他只要 alt+tab 就回到原本的事，成本接近零；真正會被打斷的只有**不能暫停的即時遊戲**。他是資源的擁有者，不需要為 agent 讓路；agent 也不必為了他在場就癱瘓（2026-08-30 他說「我洗好澡，人在電腦前了」後，頂層把線停在取鎖前，他問「他應該可以自己啓動遊戲吧」——方向反了）。

**How to apply:**
- **預設：使用者在電腦前時，agent 仍可取 `desktop.lock`／`game.lock`、啟動 MO2、Skyrim、Chrome 分頁。**
  不必為此停下來問，也不要叫他先別用鍵鼠。
- **仍然不可以做的**：搶焦點回來（送按鍵、`xdotool` 注入到他正在用的視窗）、
  在他明說要用電腦時硬上。**啟動遊戲佔螢幕可以；把他的輸入搶走不行。**
  「鍵盤滑鼠歸他」＝不做鍵鼠注入；瀏覽器走 CDP／claude-in-chrome，不走 xdotool。
- **唯一硬禁區：他正在玩不能暫停的遊戲**（Helldivers 2 這類連線即時遊戲）。
  不確定就問一句，不要自己猜。
- 這條**取代**了 `agentctl/AGENTS.md` 鐵律第 5 條與 `docs/resource-locks.md` 的
  「使用者在電腦前時連鎖都不要拿」。
- Skyrim 忽略 xdotool 等合成的視窗定向輸入（2026-09-20），agent 不搶焦點就操作不了角色；需要「走路」類實機驗收時要嘛使用者自己順手做、要嘛請他給幾分鐘前景。判「使用者接手」前先排除卡鍵（key 沒放開讓角色自己跑）：看 key-up 後位置是否靜止。
- 線未送任何鍵鼠，角色卻位移數千單位並持續跑跳離開 cell＝使用者已接手；即使鎖目錄是空的也不得取鎖開遊戲或部署，立刻停止一切改變狀態的操作（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-20/calder/REPORT.md:58`）。

相關：[[aetheria-agent-coexistence]]（desktop.lock 現在只當我方線間 mutex）、
[[im-dispatcher-codex-implements]]、[[model-tiers-and-headcount]]（09-08／09-09 /goal 的模型路由）。

## gd-libs-session-coexistence

> 2026-09-18 起同機另有 gd-libs（~/repo/game_dev/gd_libs，Godot 2D 資產管線）Claude session；鍵鼠螢幕使用權以 skyrim session 為尊（原 type: memory）

2026-09-18 使用者裁示：鍵盤／螢幕／滑鼠的使用權「以你（skyrim 頂層 session）為尊」，並已同步告知 gd-libs session。gd-libs 平時走 xvfb＋headless 不佔實體螢幕；要開可見視窗會先傳 session 訊息請求。

**Why:** 兩條線同機並行，遊戲實機驗收要獨佔實體螢幕與 GPU；沒有仲裁者就會互搶。

**How to apply:** 收到 gd-libs 請求時直接裁，不用問使用者。已告知它的協議：`agentctl/.lock/desktop.lock/`（可見視窗）與 `game.lock/`（Skyrim／MO2）mkdir 語意，mkdir 失敗＝有人在用；遊戲隊持鎖期間請它避免長時間 GPU 重負載。它的 session 位址由 cross-session 訊息的 from 欄位取得（會變）。與 [[aetheria-agent-coexistence]] 不同：aetheria 已凍結，gd-libs 是現役。

## launch-skyrim-via-steam

> 2026-08-28 起不再從 Steam 啟動 Skyrim；走開始選單「Skyrim (Modpack-KR)」或 instance/tools/launch-mo2.sh，不經 Steam client（原 type: memory）

不從 Steam 點遊戲：exe 必須釘在 1.6.1170，`AutoUpdateBehavior=1`；Play／Verify 的實際行為見 [[skyrim-no-appmanifest-steam-safe]]。
正確啟動：開始選單「Skyrim (Modpack-KR)」或 `instance/tools/launch-mo2.sh`（SteamLinuxRuntime sniper＋Proton 9），MO2 開起來後使用者自己按 Run。

- 無人值守：同一套 sniper＋Proton `waitforexitandrun` 包裝多帶 `moshortcut://:SKSE`，MO2 會直接跑 SKSE、不用人按 Run（2026-09-02 實測 AgentBridge 30 秒內起來；即 `launch-mo2.sh --skse`）。
- `mo2ctl launch --background-active` 已壞：它走 `protontricks-launch --appid 489830`，appmanifest 不在時回「Steam app ... could not be found」直接失敗（2026-09-02），runtime-qa 文件寫的那條無人值守路線不能用。
- `SkyrimSE.exe` 仍需要 **Steam client 常駐**（2026-09-18；`SteamAPI_Init` 失敗＋usvfs 擋掉自拉 steam.exe → 整條鏈靜默退出，log 只有 `[S_API FAIL]`）。「不經 Steam client」只對 MO2 本身成立。安全開法：確認 `appmanifest_489830.acf` 的 `AutoUpdateBehavior=1`／`StateFlags=4`／buildid 未變，`steam -silent` 起來後輪詢守衛 2 分鐘看 StateFlags／buildid 不動；收工關 Steam 或離線。

**Why:** Steam 一更新整個 SKSE 生態全毀且無還原路徑；「驗證檔案完整性」同樣禁止。

**How to apply:** 別叫使用者從 Steam 開；啟動前確認 `ModOrganizer.ini` 的 `selected_profile=modpack-main`（CRLF 檔）；不要在 SteamLinuxRuntime 容器外直接呼 `proton`；非必要不開 MO2（它一載入就覆寫 profile，見 [[profile-restore-order-and-flags]]）。細節以 `instance/README.md`「啟動方式」為準。

## lock-lifecycle-ownership-and-broken-states

> 鎖只交領導管理；鎖目錄被殘留檔卡住、或 owner 寫已釋放但目錄還在，都不是正常佔用

- 鎖的取得／釋放只收領導層（2026-08-30 起；工人忘記釋放會害下輪卡住，`agentctl/handoffs/done/2026-08-30/dl-2026-08-30/HANDOFF-cx-dl11.md:17-27`）。
- 鎖路徑是 0 位元組普通檔時，mkdir 回 `Not a directory`，不是「已被佔用」（2026-09-11，`agentctl/handoffs/done/2026-09/home-2026-09-11/body/REPORT.md:98-100`）。
- `game.lock/` 目錄還在但 owner 寫「released」時仍會擋取鎖（2026-09-18，`agentctl/handoffs/done/2026-09/home-2026-09-18/recon/REPORT.md:10`）。

**Why:** mkdir 鎖只看目錄存不存在；owner 文字與狀態可能不一致，殘留不會自己清除。

**How to apply:** 多工人共用鎖只讓領導管；取鎖失敗回 `Not a directory` 或 owner 寫已釋放先核實再清除。
