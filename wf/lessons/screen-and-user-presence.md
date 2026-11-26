# 螢幕使用權：使用者在場與同機 session

[lessons 索引](README.md)｜鎖與開遊戲見 [locks-screen-and-game](locks-screen-and-game.md)

## user-present-screen-is-still-usable

> 使用者在電腦前時鍵盤滑鼠螢幕歸他，但 agent 可以開遊戲／MO2／瀏覽器，他會 alt+tab 切回去；只有不能暫停的遊戲（如 Helldivers 2）才是禁區（2026-08-30，2026-09-09 /goal 重申）

2026-08-30 使用者原話：

> 我坐在電腦前的時候，**agent 可以用熒幕**，因爲他啓動遊戲後，雖然遊戲會占據熒幕，
> 但我會**立刻 alt+tab 切回我正在做的事情**。除非我是在打 **helldivers 2 這種不能暫停的遊戲**，
> 不然都 OK。

2026-09-09 /goal 重申：

> 我人坐在電腦前，鍵盤滑鼠螢幕歸我，但可以開遊戲, mo2, 瀏覽器。

可做／不可做的表與硬禁區已整份寫進 [`agentctl/docs/resource-locks.md`](../../agentctl/docs/resource-locks.md)〈使用者在電腦前時可以做什麼〉，照那裡做：取鎖、開 MO2／Skyrim／Chrome 分頁不必先問；不搶焦點、不注入鍵鼠（瀏覽器走 CDP／claude-in-chrome）；他在玩不能暫停的遊戲是唯一硬禁區，不確定就問。他說「我洗好澡，人在電腦前了」時照常開線——他問過「他應該可以自己啓動遊戲吧」。

文件沒寫的兩條：

- Skyrim 忽略 xdotool 等合成的視窗定向輸入（2026-09-20），agent 不搶焦點就操作不了角色；「走路」類實機驗收要嘛使用者順手做、要嘛請他給幾分鐘前景。判「使用者接手」前先排除卡鍵：看 key-up 後位置是否靜止。
- 線未送任何鍵鼠，角色卻位移數千單位並持續跑跳離開 cell＝使用者已接手；即使鎖目錄是空的也不得取鎖開遊戲或部署，立刻停止一切改變狀態的操作（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-20/calder/REPORT.md:58`）。

desktop.lock 現在只當我方線間 mutex。相關：[[im-dispatcher-codex-implements]]、[[model-tiers-and-headcount]]（09-08／09-09 /goal 的模型路由）。

## gd-libs-session-coexistence

> 同機另有 gd-libs（~/repo/game_dev/gd_libs，Godot 2D 資產管線）Claude session；鍵鼠螢幕使用權以 skyrim session 為尊（2026-09-18）

2026-09-18 使用者裁示：鍵盤／螢幕／滑鼠的使用權「以你（skyrim 頂層 session）為尊」，已同步告知 gd-libs session。gd-libs 平時走 xvfb＋headless；要開可見視窗會先傳 session 訊息請求。

收到 gd-libs 請求時直接裁，不用問使用者。告知它的協議：`agentctl/.lock/desktop.lock/`（可見視窗）與 `game.lock/`（Skyrim／MO2）mkdir 語意，mkdir 失敗＝有人在用；遊戲隊持鎖期間請它避免長時間 GPU 重負載。它的 session 位址取 cross-session 訊息的 from 欄位（會變）。與 aetheria 不同：aetheria 已凍結，gd-libs 是現役。
