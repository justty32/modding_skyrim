# 鎖、螢幕與開遊戲（1/3）

[lessons 索引](README.md)｜同主題：[locks-screen-and-game-2](locks-screen-and-game-2.md)、[locks-screen-and-game-3](locks-screen-and-game-3.md)

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
