# 調度：驅動 codex／tmux 與行程

[lessons 索引](README.md)

## driving-other-cli-agents

> 怎麼從 Claude Code 驅動同機的 pi / codex CLI agent——用 tmux，不是 stdin 注入；以及分工與護欄（原 type: memory）

使用者會把整條工作線外包給同機的其他 CLI agent（2026-08-06 首次：`pi --provider deepseek --model deepseek-v4-pro` 接 mod 庫、`codex` 接第三方 mod 流水線），並要 Claude 去驅動它們。

**「找到 process 丟 stdin」做不到**——互動 TUI 的 stdin 是 tty，寫 `/proc/<pid>/fd/0` 是寫到終端裝置（方向反了）；唯一能塞進 tty 輸入佇列的 `ioctl(TIOCSTI)` 被 `dev.tty.legacy_tiocsti=0` 關掉（kernel 6.2 起預設）。

**可行版本是 tmux**：`tmux new-session -d -s <name> -x 200 -y 50 -c <dir> '<agent cmd>'`，用 `send-keys -l '…'` 然後單獨一個 `Enter` 送指令（長交接書寫成檔案、只送路徑），`capture-pane -p -S -60` 讀畫面。使用者可 `attach` 同時插手，而且**他真的會**——看到 pane 裡有他自己打的字就別再代答。headless（`pi -p`、`codex exec`）留給要明確結果的單次任務。

**Why:** 三個 agent 併行時最大的風險不是能力而是撞車與越權。實測分工乾淨就沒事：各據一個獨立 git repo（Claude 在 `projects/darksouls-port`、codex 在 `projects/agent-bridge`、pi 在 `~/notes`），母 repo 的 submodule 指標與計畫文件由 Claude 收。

**How to apply:**
- **交接書要寫死護欄**，特別是刪檔：pi 那次照著把檔案移進 `.quarantine/`，**但接著把整個隔離區刪掉**，107 筆沒經 restore 就永久消失（ext4 無快照）。實質損失為零純屬運氣好。護欄要寫到「隔離區本身也不准刪，回收前先問」。
- **會動 MO2／檔案系統的 agent 要架看門狗**：`Monitor` 輪詢「非測試用的 mod 資料夾是否消失」「Default profile 是否被改」。注意 `ls` 會給含空格的名字加引號，濾網要考慮。
- codex 表現穩：切 profile 前檢查 CRLF、測試 mod 用獨立命名、自己卸載並還原 active profile。它報「profiles repo 髒了不能裝」時**是對的**，先查 mtime 歸因再下結論。
- 相關：[[delegate-simple-work-to-sonnet]]、[[workspace-layout-and-duties]]

**2026-08-23：這套已經正規化成文件，不要再只靠記憶。**
權威在 `~/repo/moddings/skyrim/agentctl/docs/`：

- `driving-codex.md` —— 切線、交接書契約、tmux 驅動、監看、收線的完整流程
- `resource-locks.md` —— 桌面 HID 鎖（跨 agent，**Aetheria 優先**）、遊戲鎖、CPU 限流、收工檢查
- `../tools/agent_inbox/PROTOCOL.md` —— 通訊契約與五種 STATUS 語意

**鎖的取得順序**（先前從沒寫下來過）：**先桌面 HID 鎖 `~/shared_agent_locks/desktop.lock`，
再遊戲鎖 `agentctl/.lock/game.lock`**。跑 Skyrim 一定佔螢幕，反過來拿會跟 Aetheria 死鎖。

**兩個曾經失效的路徑已修**：遊戲鎖原本在 `~/skyrim_agent_out/_lock/`、inbox 執行期資料原本在
`~/skyrim_agent_out/_inbox/`，該目錄 2026-08-22 隨 agent 線封存被刪，
於是「遊戲鎖已釋放」的檢查一直在檢查不存在的路徑（恆真），inbox 送收也兩端落空。
現在都改成從 repo 位置推導。

派線前先讀那兩份文件，不要憑本記憶條目的舊細節行動。

## codex-tmux-operational-notes

> 用 tmux 驅動 codex CLI 的實務細節——送出鍵要分開送、trust prompt、gpt-sol 的行為特性與該寫死的護欄（原 type: feedback）

2026-08-20 夜間一次開三條 codex 線（gpt-5.6-sol）跑 Skyrim modding 工作，累積的操作細節。

**送指令要分兩次呼叫**：`tmux send-keys -t <s> -l '<文字>'` 之後的 `C-m`／`Enter` 如果**寫在同一個
Bash 呼叫裡**，codex TUI 常常只把文字放進 composer 而不送出（pane 上看到 `» <你的文字>` 就是還沒送）。
要另外發一個 `tmux send-keys -t <s> C-m` 才會真的送出。每次送完務必 capture 確認開頭變成 `›` 且出現
`Working (`。

**啟動時會先問 trust**：`codex` 在新目錄第一次啟動會停在「Do you trust the contents of this
directory?」，要送一個 Enter 才會進主畫面。`capture-pane -p -S -30` 在 alt-screen 下抓不到東西，
**不要加 `-S`**。

**偵測 idle**：pane 裡有 `Working (` 就是忙碌，消失即該輪結束。用 Monitor 做 busy→idle 邊緣觸發
通知，比自己輪詢省很多 token。

**gpt-sol 的行為特性**（使用者親口提醒 + 實測）：
- 會為了「更保險」跑一大堆與正事無關的驗證測試。**交接書要寫死「驗收就是這四條，一條不多，
  做完就停」**，實測有效。
- subagent 使用者的界線是：**為了推進正事可以開，為了驗證／複查／風險掃描這種周邊小事不准開**。
  判準寫成「那個 subagent 的產出如果不在驗收清單裡，就不該開它」。
- 護欄遵守度高：叫它「遇到工具錯誤就停下回報」它真的會停——但它把**自己寫錯的 Python 引號**
  也算成工具錯誤而停工。交接書要區分「工具/環境錯誤 → 停」與「你自己的臨時腳本寫錯 → 自己修」。
- 給精確的預期數字（檔案數、bytes、tree SHA）它會照著對，不會含糊帶過。

**多線分工**：一條 MO2 live tree + profiles git、一條 submodule 原始碼、一條唯讀盤點寫 notes。
同一個 git repo 有兩條線要 commit 時，交接書要寫「只准 `git add <明確路徑>`，禁止 `git add -A`，
遇到 `.git/index.lock` 等幾秒重試、絕不刪 lock」。

**遊戲是獨佔資源**：MO2／Skyrim 同時只能一條線持有，而且**不能在另一條線正在搬 `overwrite/`
檔案時啟動**（遊戲會寫入 overwrite）。排程要自己當鎖來管。

**改 `~/.codex/config.toml` 會殺掉所有正在跑的 codex session**（2026-08-20 實測）：22:57:39 用
`sed -i` 改了一行 `HouseCarl__ProfileDir`，22:59:09–10 四個 `tmux-spawn-*.scope` 在同一秒內全部結束，
四條 codex 線同時死光，在途工作（未落檔的交接書、未寫出的腳本）全部丟失；只有已經 commit 的存活。
codex 顯然會監看設定檔並在變更時退出。**要改 codex 設定就先讓所有 session 收工，或接受重開的代價。**
排查時 `journalctl --user | grep 'tmux-spawn.*scope'` 會列出每個 scope 的 wall clock，能用起始時間反推
是哪幾條線。

**houseCARL 在本機的已知壞法**：`Mo2InstanceDir` 模式不可用（MO2 的 `gamePath` 是 Wine 路徑
`Z:\home\...`，houseCARL 不做映射，會推出不存在的 `Z:\home\...\Data`）；正解是 explicit paths
`HouseCarl__DataDir` / `ModsDir` / `ProfileDir`。2026-08-20 單 profile 遷移後，`~/.codex/config.toml`
與 `~/.claude.json` 兩邊的 `ProfileDir` 都還指著已退役的 `profiles/Default`，導致每個 houseCARL 查詢
都回 "No active plugins resolved"。已改成 `profiles/Modpack-KR`（兩邊都有 `.bak-20260820` 備份）。

**任務結束就關掉 session,不要留著等下一批**(2026-08-21 量測後訂的規矩)。每個閒置的 codex
session 持有一個 houseCARL MCP 實例,**實測平均 249 MB**。昨夜開六條線、任務結束後只確認成果
有沒有推上去卻沒收拾 session,結果 codex-b/codex-f 從凌晨閒置到早上;連同其他閒置線共佔
**2,237 MB**,關掉後降到 475 MB,**釋出約 1.8 GB**。

要用時重開只要 30 秒,而交接書都寫在磁碟上(`~/skyrim_agent_out/<線名>/`),不依賴 session 記憶——
這正是把成果寫成報告與交接書的意義。

**附帶教訓**:我一度用「影響接近零」把 MCP 實例洩漏帶過去,那是**沒量就下的結論**。
使用者說過「不要操我的電腦」,這種事該量了再說。

相關：[[driving-other-cli-agents]]、[[delegate-simple-work-to-sonnet]]

**2026-08-30 使用者心得——指揮 gpt-sol 要經常提醒它專注**：「要他專注在真正重要的事情上，無關緊要的小事先別管」，否則它會一直寫測試一直驗證。這是動態手段，跟交接書「寫死驗收條數」（靜態）並列：交接書擋不住的過程漂移，靠 orders／tmux 中途提醒拉回來。各模型有各自的指揮方式，已進 agentctl/docs/team-model/speed-and-driving.md 的逐模型指揮心得表（2026-08-30）。

**2026-09-08 模型別名壞了**：`codex -m gpt-sol` 現在回 `The 'gpt-sol' model is not supported when using Codex with a ChatGPT account`；config 裡的真名是 `gpt-5.6-sol`，直接跑 `codex` 用預設模型即可。交接書寫「gpt-sol」沒問題（是我們的暱稱），但啟動指令別帶 `-m gpt-sol`。另：`housecarl_bsa_list`（BSArch 走 wine）在這台機器讀 BSA 會 `wineserver: bind: Operation not permitted`，髮型「缺檔」判定要改用 python 直接掃 BSA 位元組，否則會假警報。

**2026-09-20 補**：`codex` 預設模型實際是 `gpt-6-astra medium`（不是 gpt-sol），要 gpt-sol 得另外確認別名；
`inbox_send.sh` **沒有 `--body-file` 旗標**，正文檔是第 4 個位置參數，寫成旗標會靜默從 stdin 卡住（lead-fde920 抓到）。
交接書「只看 plugins.txt 帶 `*`」會漏掉隱含載入的 CC 與原版 master（1266 支＝1207 勾選＋59 隱含）。

**2026-09-25 orders 檔不是即時剎車**：cx-wu-kern 在我把「不降版、還原」的 order 追加到 `inbox/orders/cx-wu-kern.md` 三分鐘後照樣 commit 了降版（它只在「每完成一步」才讀 order，最後一步 commit 前沒再讀）。要即時攔一條 codex 線，用 `tmux send-keys -t <線> Escape` 中斷再送新指令＋兩次 Enter，或直接 kill session；order 檔只適合「下一步前要看」的補充指示。事後靠三個 repo 都沒 push，用 `reset --soft HEAD~1`＋`restore --staged --worktree -- wf AGENTS.md`＋刪新檔還原。

## codex-tmux-enter-must-be-verified

> tmux 送提示詞給 codex 後 Enter 常沒送出（尤其長段中文），送完 5 秒內 capture-pane 看到「Working」才算開工，否則再送一次 Enter（原 type: memory）

2026-09-13 dsp9：對兩個剛啟動的 codex 送長段中文提示詞＋Enter，畫面看起來正常，
9 分鐘後回來才發現字還卡在輸入框（`›` 後面是提示詞、沒有 Working），白等 9 分鐘，
使用者 20:00 的硬時限被吃掉四分之一。補一次 Enter 就送出。工人在 Working 時追加的訊息
也一樣：第一個 Enter 只把字放進 composer（顯示「tab to queue message」），要第二個 Enter 才進佇列。

**Why:** codex TUI 剛起來 15～20 秒內、或 bracketed paste 結束後，第一個 Enter 會被吃掉；
畫面沒有錯誤，只看最後幾行很容易誤判已開工。

**How to apply:** 每次 `tmux send-keys ... Enter` 後 `sleep 4; tmux capture-pane -p | tail`，
沒看到 `• Working` 或轉圈就再送一次 Enter；把這個檢查寫進等待迴圈的第一輪。
相關：[[codex-tmux-operational-notes]]、[[leads-must-not-end-turn-to-wait]]。

## tmux-working-text-is-not-liveness

> tmux pane 的「Working (Ns)」字樣可能是死 scrollback，判活要看 pane_pid 的子行程樹（原 type: project）

2026-09-01 hwrap 查證：tmux-resurrect 復原的 pane 會殘留舊 session 的「• Working (2m 20s)」字樣，計時器凍住其實是 codex 早已退出（pane 底部是 shell 提示字元、pane_pid 無子行程）。只盯畫面 hash 判「卡死」白等了一小時。

**Why:** 畫面不動只證明畫面不動；「stuck」與「exited」要靠行程樹分辨。

**How to apply:** 判斷 codex/agent 線死活時，tmux capture-pane 之外必查 `pgrep -P <pane_pid>`（無子行程＝已退出）；監看腳本的停滯偵測要同時比對畫面與行程樹。相關：[[pgrep-self-match-beyond-brackets]]、[[verify-game-alive-via-qa-not-ps]]。

## throttle-by-tree-not-by-name

> 多 agent 共機時,限流/kill 要按行程樹歸屬不能按行程名稱;houseCARL 每個 MCP client 各一份實例（原 type: reference）

2026-08-21 與 aetheria agent 協調 CPU 時查證出來的。

**houseCARL MCP 不是共用常駐服務**——它是 stdio MCP server，**每個 client 各 spawn 一份**。
實測同時有 10 個 `housecarl-mcp` 實例：我的 claude session 一份、六個 codex session 各一份、
Claude Desktop 底下一份，外加一個 parent 已是 `systemd --user` 的**孤兒**（實例會洩漏）。

**因此**：aetheria agent 昨夜想壓自己那條線的 CPU，把「`housecarl-mcp` 連同子行程」釘到 2 核，
結果**打中了全部 10 個實例**，包括我六個 codex session 各自的那份，害它關閉時卡十分鐘。

**規則**：多 agent 共用一台機器時，限流／renice／kill **要按行程樹歸屬，不要按行程名稱**。
從自己已知的 pid 往下遞迴（`pgrep -P`）或用 cgroup／systemd scope；
`pgrep -f <名字>`／`pkill -f` 會掃到別的 agent 同名的實例。
同理，別人的 watchdog 若按 `cc1plus`／`ld` 這種通用名稱掃，也會誤傷我的 build。

**相關陷阱**：`protontricks-launch` 這類程序會被 systemd 收養、parent 變成 `systemd --user`，
祖先鏈追到 `ppid=1` 就斷，**無法判斷發起者**。反過來，鏈完整也不代表歸屬正確——
要判斷工作歸屬，直接寄信問對方，不要看 `ps`。

**實作細節**：判斷 parent 要讀 `/proc/<pid>/status` 的 `PPid:`，**不要解析 `ps` 的 `stat` 欄位**
——comm 含空白或括號時會解析錯誤（aetheria agent 2026-08-21 提供）。
歸屬判斷做不到時就**不要做限流**，寧可不限也不要在歸屬失效時亂打。

**最終定案的分配**（2026-08-21）：aetheria CPU 35%（上限 6 核）／skyrim CPU 45%／
GPU 與桌面 HID（螢幕鍵鼠）**全歸 skyrim**——對方 Godot 一律 headless、看圖用匯出 PNG，
完全不需要桌面，因此**要開 Skyrim 不必先寄信詢問**。

相關：[[aetheria-agent-coexistence]]

## dont-renice-other-sessions

> 2026-10-09 使用者喊停：遊戲卡頓時不准自行 renice／限流別的 session（如 simple_tools/aos-wt）的行程，只回報來源

2026-10-09 使用者玩遊戲回報卡頓，我查到負載來自另一個 Claude session 在 `simple_tools/aos-wt` 跑測試，就自行 renice 它的行程樹；使用者回「你不要調整這個=_=」。

**Why:** 別的 session 的行程是使用者自己的其他工作，優先權由他決定；擅自調整等於替他做取捨。

**How to apply:** 遊戲卡頓時只查證並回報「誰在吃 CPU」（行程樹、所屬 session／repo），由使用者決定要不要停。只有我方派出的線才可以限流或停。這條修正 [[throttle-by-tree-not-by-name]] 的適用範圍：那條只適用於我方行程。
