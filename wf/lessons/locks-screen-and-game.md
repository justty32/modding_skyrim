# 鎖、螢幕與開遊戲

[lessons 索引](README.md)

## skyrim-no-appmanifest-steam-safe

> Skyrim SE 的 appmanifest 已放回、Play 不觸發更新但 Verify 會重灌；AE CC 內容不是 Steam depot，只能遊戲內 Creations 登入 Bethesda.net 下載（原 type: memory）

2026-09-03 AE 兩輪後的事實（原 08-28 那條「無 appmanifest 所以 Steam 入口作廢」已過時）：

<!-- wf-nav -->
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

2026-10-23 補：無邊框鋪滿螢幕的視窗可能被 KWin 6.7（Wayland，NVIDIA Blackwell 驅動 610.x 已見）當成 direct scanout 候選，present 卡住時主執行緒跟著停，外觀像整個凍結，但 alt+tab／Super／PrintScreen 能讓 KWin 退出 scanout 復活——這不是真死鎖。判準：先問音樂/環境音有沒有持續播放，有就先試多次 alt+tab 而非直接 kill（`agentctl/handoffs/done/2026-10/home-2026-10-09/barter/REPORT-freeze.md`）。確認是真死鎖（alt+tab 救不回）時，關遊戲前先按 CrashLogger v1.24 的 Ctrl+Shift+F12（需 `CrashLogger.ini` 開 Thread Dump Hotkey）留下全執行緒堆疊，不要直接關掉——事後只有 futex_wait 末態快照拿不到卡住瞬間的呼叫鏈，無法定罪（`agentctl/handoffs/done/2026-10/home-2026-10-09/barter/REPORT-hang.md`）。

## agent-driven-nexus-download

> agent 自己從 Nexus 下載檔案的路徑：2026-08-27 起優先用 Claude in Chrome 擴充，退路才是 CDP + 暫存 profile 複本（原 type: memory）

2026-08-22 實測成功：codex 線可以自己完成 Nexus 手動下載，路徑是
**Chrome DevTools Protocol（`--remote-debugging-port`）＋ 使用者 profile 的暫存複本**，
用程式驅動頁面點 `Manual download` → `Slow download`，完全不需要鍵鼠注入。

**2026-08-27 起多一條更短的路**：使用者裝了 Claude in Chrome 擴充（`list_connected_browsers`
看得到本機 Browser），可以直接驅動他現有的 Chrome，不必開 profile 複本也不必開 CDP port。
CDP + profile 複本降為退路（擴充沒連線時用）。**2026-08-27 已用擴充實測成功**
（mod 26440 CHS 主檔，Manual → Slow download 一次過），證據與可重跑序列在
repo 的 `agentctl/logs/nexus-download-via-chrome-extension-2026-08-27.md`。
用擴充時不必取桌面鎖，因為沒有搶螢幕。

**為什麼不是鍵鼠注入**：這台是 Wayland + KDE，`ydotool` 有裝但 `ydotoold` 起不來
（`/dev/uinput` 是 `root:root 660`，要 sudo）。注意 `xdotool` 的限制**沒有**當初以為的那麼死——
2026-08-27 重測：只要有 XWayland 視窗持有焦點，`xdotool` 的鍵盤與**滑鼠**都可用，
詳見 repo 的 `agentctl/docs/resource-locks.md`。但下載仍走瀏覽器驅動，因為那更穩、可驗證。

**profile 要用複本，但只複製三樣**：直接用使用者的 profile 會搶到既有 Chrome 實例（新 flag 被忽略），
或關掉使用者的視窗。複製一份出來既能沿用 Nexus 登入 session，又不干擾使用者。
**2026-08-30 `cx-dl11` 實測：只需要登入 cookie ＋ `Preferences` ＋ `Local State`，複本 6.7 MB 就夠**，
登入狀態帶得過去、不撞 Cloudflare。`cx-dl7`（2026-08-29）整棵複製吃了 **5.9 GB**——
`/tmp` 是 tmpfs（記憶體），那等於白燒 6 GB RAM。**不要整棵複製。**

**light-DOM fallback 別靠 URL 參數認 row**：點 FILES 分頁後 Nexus 會把 URL 裡的 `file_id` 拿掉，
但那一列在 DOM 裡仍正確——要以 DOM 選 row。工具現行行為是 fail-closed（寧可抓不到也不抓錯），
**改工具時不要把這個性質弄丟**。細節在 repo 的
`agentctl/handoffs/done/2026-08-27/cx-dl2/tools/KNOWN-ISSUES.md`。

**manager download 是壞的**：`nxm://` handler 送得到 MO2、`nxmhandler.exe` 回 status 0，
但下載清單不會出現項目。詳見
`~/notes/projects/modding/skyrim/logs/ai-overhaul-1.9.5-nxm-download-attempt-2026-08-21.md`。
官方 manual download 是被允許的，別再繞 handler。

**交接書一定要寫死的紅線**：不准輸入任何憑證、不准解 CAPTCHA、不准接受新條款、
不准點 endorse/track/vote、不准 sudo 或改 group/udev。碰到就發 `NEEDS-USER` 停下來。

**免費驗證**：Nexus 檔案列上的 VirusTotal 連結帶著該檔 hash，可以直接跟下載檔的
SHA-256 比對，等於一次來源驗證。

螢幕是獨佔資源，動之前取 [[aetheria-agent-coexistence]] 提到的遊戲鎖當 screen mutex 並註明用途。
相關：[[driving-other-cli-agents]]、[[trust-gpt-sol-more]]

**2026-09-03 補**：headless CDP 的 Chrome 會自己在背景下載約 4 GB 的 on-device ML 模型（optimization guide），塞爆 /tmp tmpfs 並吃 25 Mbps 頻寬；dl 隊已加啟動旗標擋掉（見 `agentctl/handoffs/home-2026-09-03/dl/` 的 Chrome 啟動參數）。profile 複本放 /tmp 要盯大小，>500 MB 就是有東西在自下載。另：CDP 下載沒有速率上限，Steam 同時在下載時別抓 >500 MB 大檔。

**2026-09-30 使用者重點要求：不准讓他現有 Chrome 的任何帳號被登出（Google 與其他所有網站）。** 寧可下載失敗。
複本改用 `agentctl/tools/nexus_dl/make_profile_copy.sh`（來源唯讀快照、只留 nexusmods.com cookie、殘留自毀），
不再整份 cp Cookies（第二個 Chrome 共用 Google session cookie 可能觸發盜用保護把本尊登出）；
收尾只殺 `--user-data-dir=/tmp/<複本>` 的 Chrome，禁 pkill／killall；擴充路不點登出、不清 cookie、不關使用者分頁。
規則寫在 `wf/workflows/nexus-intake/download-routes.md` 頂部。

2026-10-23 補：CDP profile 複本啟動後在 `/tmp`（tmpfs）會因 OptGuideOnDeviceModel 等元件執行期下載膨脹到約 4.6GB（啟動前複本只 1.7MB），等於白燒記憶體；下次用複本下載，建複本在真實磁碟或啟動時加旗標停用 optimization-guide/screen_ai/WasmTtsEngine，過程定期巡 tmpfs 用量。Nexus「Manual/Slow download」按鈕有時渲染在 shadow DOM 裡，CDP 腳本要同時查 `document` 與 `shadowRoot`、只點可見元素。頁面 load timeout／沒觸發 download start 多半是暫態網路問題，先直接重試不必假設檔案本身有問題。houseCARL 標 manager only 的 Nexus 檔案，agent 用既有慢速下載流程（Xvfb Chrome＋profile 複本）仍可能成功，不要就此放棄。Nexus 頁面版本明顯落後於社群已知相容版（如 AE 支援）時，優先查該 mod 的 GitHub repo 是否有更新 release——housecarl 與既有 CDP 工具只為 Nexus 設計，做不到 GitHub release 下載。
source: agentctl/handoffs/done/2026-09/home-2026-09-01/hfix-2026-09-01/REPORT.md；agentctl/handoffs/done/2026-09/home-2026-09-02/lrdl/REPORT.md:65；agentctl/handoffs/done/2026-09/home-2026-09-02/mco/REPORT.md:34

2026-10-23 補：GitHub release 直連下載（如 xEdit 官方 release 的 BSArch.exe）用 `curl`/`wget` 即可，不撞 Cloudflare、不需要開瀏覽器、不需要取 `desktop.lock`——這條限制只有 Nexus 下載才有，判斷要不要取桌面鎖先看來源是不是 Nexus（`agentctl/handoffs/done/2026-08-31/fixdis-2026-08-31/CX-FD1.md:53-57`）。另：`cdp-download.mjs` 對 >500 MB 檔的逐檔 timeout 要按 bytes 分級（>500MB 給 900 秒、>1GB 給 2400 秒），沿用舊版固定 420 秒會把大檔判失敗（`agentctl/handoffs/done/2026-09/home-2026-09-03/dl/REPORT.md:62`）。

## user-present-screen-is-still-usable

> 2026-08-30 放寬、2026-09-09 /goal 重申：使用者在電腦前時鍵盤滑鼠螢幕歸他，但 agent 可以開遊戲／MO2／瀏覽器，他會 alt+tab 切回去；只有不能暫停的遊戲（如 Helldivers 2）才是禁區（原 type: user）

2026-08-30 使用者原話：

> 我坐在電腦前的時候，**agent 可以用熒幕**，因爲他啓動遊戲後，雖然遊戲會占據熒幕，
> 但我會**立刻 alt+tab 切回我正在做的事情**。除非我是在打 **helldivers 2 這種不能暫停的遊戲**，
> 不然都 OK。

2026-09-09 /goal 重申（同一條，措辭更明確）：

> 我人坐在電腦前，鍵盤滑鼠螢幕歸我，但可以開遊戲, mo2, 瀏覽器。

**Why:** 舊規則是「使用者在電腦前時鍵鼠螢幕全歸他，連鎖都不要拿，最高優先沒有例外」。
那條是為了不打斷他，但**實際上他只要 alt+tab 就回到原本的事**，成本接近零。
真正會被打斷的只有**不能暫停的即時遊戲**。

**How to apply:**
- **預設：使用者在電腦前時，agent 仍可取 `desktop.lock`／`game.lock`、啟動 MO2、Skyrim、Chrome 分頁。**
  不必為此停下來問。
- **仍然不可以做的**：搶焦點回來（送按鍵、`xdotool` 注入到他正在用的視窗）、
  在他明說要用電腦時硬上。**啟動遊戲佔螢幕可以；把他的輸入搶走不行。**
  「鍵盤滑鼠歸他」＝不做鍵鼠注入；瀏覽器走 CDP／claude-in-chrome，不走 xdotool。
- **唯一硬禁區：他正在玩不能暫停的遊戲**（Helldivers 2 這類連線即時遊戲）。
  不確定就問一句，不要自己猜。
- 這條**取代**了 `agentctl/AGENTS.md` 鐵律第 5 條與 `docs/resource-locks.md` 的
  「使用者在電腦前時連鎖都不要拿」。

**我犯的錯**：他說「我洗好澡，人在電腦前了」之後，我立刻把兩條線停在取鎖前，
還跟他說「你先別用鍵鼠」——**方向反了**。他是資源的擁有者，不需要為 agent 讓路；
而 agent 也不必為了他在場就癱瘓。他後來問「他應該可以自己啓動遊戲吧」就是在指出這點。

相關：[[aetheria-agent-coexistence]]（desktop.lock 現在只當我方線間 mutex）、
[[im-dispatcher-codex-implements]]、[[model-tiers-and-headcount]]（09-08／09-09 /goal 的模型路由）。

**2026-09-20 補**：Skyrim 忽略 xdotool 等合成的視窗定向輸入，agent 不搶焦點就操作不了角色；需要「走路」類實機驗收時要嘛使用者自己順手做、要嘛請他給幾分鐘前景。另：領隊曾發生卡鍵（key 沒放開）讓角色自己跑，判「使用者接手」前先看 key-up 後位置是否靜止。

2026-10-23 補：三份獨立記錄各自捕捉到同一類事件——線未送任何鍵鼠，角色卻位移數千單位並持續跑跳離開 cell，代表使用者已接手；即使鎖目錄是空的也不得取鎖開遊戲或部署，必須視為使用者已接手並立刻停止一切改變狀態的操作（`agentctl/handoffs/done/2026-09/home-2026-09-20/calder/REPORT.md:58`）。

## gd-libs-session-coexistence

> 2026-09-18 起同機另有 gd-libs（~/repo/game_dev/gd_libs，Godot 2D 資產管線）Claude session；鍵鼠螢幕使用權以 skyrim session 為尊（原 type: memory）

2026-09-18 使用者裁示：鍵盤／螢幕／滑鼠的使用權「以你（skyrim 頂層 session）為尊」，並已同步告知 gd-libs session。gd-libs 平時走 xvfb＋headless 不佔實體螢幕；要開可見視窗會先傳 session 訊息請求。

**Why:** 兩條線同機並行，遊戲實機驗收要獨佔實體螢幕與 GPU；沒有仲裁者就會互搶。

**How to apply:** 收到 gd-libs 請求時直接裁，不用問使用者。已告知它的協議：`agentctl/.lock/desktop.lock/`（可見視窗）與 `game.lock/`（Skyrim／MO2）mkdir 語意，mkdir 失敗＝有人在用；遊戲隊持鎖期間請它避免長時間 GPU 重負載。它的 session 位址由 cross-session 訊息的 from 欄位取得（會變）。與 [[aetheria-agent-coexistence]] 不同：aetheria 已凍結，gd-libs 是現役。

## launch-skyrim-via-steam

> 2026-08-28 起不再從 Steam 啟動 Skyrim；走開始選單「Skyrim (Modpack-KR)」或 instance/tools/launch-mo2.sh，不經 Steam client（原 type: memory）

**舊規則（2026-08-23～08-28）「測試與遊玩都從 Steam 點 Skyrim→MO2 shim」已作廢。**

2026-08-28 起：從 Steam 點遊戲等同按更新鈕（`AutoUpdateBehavior=1`＝啟動時更新），exe 必須釘在 1.6.1170。
`appmanifest_489830.acf` 已搬出 `steamapps/`（副本在 `~/skyrim_mods/steam-build-backup/`），Steam 不再認得這個 app。
正確啟動：開始選單「Skyrim (Modpack-KR)」或 `instance/tools/launch-mo2.sh`（SteamLinuxRuntime sniper＋Proton 9，完全不經 Steam client），MO2 開起來後使用者自己按 Run。

**2026-09-02 補：** `mo2ctl launch --background-active` 走 `protontricks-launch --appid 489830`，appmanifest 拿掉後會回「Steam app ... could not be found」直接失敗，runtime-qa 文件寫的無人值守路線已死。能用的無人值守路線＝跟 launch-mo2.sh 相同的 sniper＋Proton `waitforexitandrun` 包裝，多帶一個參數 `moshortcut://:SKSE`，MO2 會直接跑 SKSE、不用人按 Run（本機實測 22:43 成功，AgentBridge 30 秒內起來）。這段還沒正規化進 instance/tools／mo2ctl，明天要補。

**Why:** Steam 一更新整個 SKSE 生態全毀且無還原路徑；「驗證檔案完整性」同樣禁止。

**How to apply:** 別再叫使用者從 Steam 開；啟動前確認 `ModOrganizer.ini` 的 `selected_profile=modpack-main`（CRLF 檔）；不要在 SteamLinuxRuntime 容器外直接呼 `proton`；非必要不開 MO2（它一載入就覆寫 profile，見 [[profile-restore-order-and-flags]]）。細節以 `instance/README.md`「啟動方式」為準。

**09-18 補充：** `SkyrimSE.exe` 仍需要 **Steam client 常駐**（`SteamAPI_Init` 失敗＋usvfs 擋掉自拉 steam.exe → 整條鏈靜默退出，log 只有 `[S_API FAIL]`）。「不經 Steam client」只對 MO2 本身成立。安全開法：確認 `appmanifest_489830.acf` 的 `AutoUpdateBehavior=1`／`StateFlags=4`／buildid 未變，`steam -silent` 起來後輪詢守衛 2 分鐘看 StateFlags／buildid 不動；收工關 Steam 或離線。08-31 grow 線與 09-18 dsp-game 第一輪都撞過這面牆。


## lock-lifecycle-ownership-and-broken-states

> 鎖只交領導管理；鎖目錄被殘留檔卡住、或 owner 寫已釋放但目錄還在，都不是正常佔用

2026-08-30 下載線忘記釋放鎖害下輪卡住，改成取得／釋放只收領導層（`agentctl/handoffs/done/2026-08-30/dl-2026-08-30/HANDOFF-cx-dl11.md:17-27`）。09-11 鎖路徑是 0 位元組普通檔，mkdir 回 `Not a directory` 非「已被佔用」（`agentctl/handoffs/done/2026-09/home-2026-09-11/body/REPORT.md:98-100`）。09-18 `game.lock/` 還在，owner 寫「released」仍擋取鎖（`agentctl/handoffs/done/2026-09/home-2026-09-18/recon/REPORT.md:10`）。

**Why:** mkdir 鎖只看目錄存不存在；owner 文字與狀態可能不一致，殘留不會自己清除。

**How to apply:** 多工人共用鎖只讓領導管；取鎖失敗回 `Not a directory` 或 owner 寫已釋放先核實再清除。
