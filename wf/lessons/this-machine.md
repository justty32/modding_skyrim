# 本機環境特性（shell、行程、限流）

[lessons 索引](README.md)

家中機（Manjaro／Wayland＋KDE）上，互動 shell 與腳本環境的差異會讓「手測過了」的驗收失真；多 agent 共機時，按名字找行程會打到別人。本檔收這類環境陷阱與動別線行程的分寸。

## interactive-grep-is-ugrep

> 家中機互動 shell 的 grep 綁成 ugrep（-x 容忍 CRLF 尾端 \r），腳本裡的 /usr/bin/grep 是 GNU grep 不容忍；手測過的 grep 驗收不可信

2026-09-05：互動 shell 的 `grep` 是 shell function → ugrep；`#!/usr/bin/env bash` 腳本走 `/usr/bin/grep`（GNU）。MO2 的 `modlist.txt`／`plugins.txt` 全是 CRLF，`grep -Fxq '+Mod Name' modlist.txt` 互動下 rc=0、腳本裡 rc=1。

**How to apply:** 對 profiles 檔判斷某行存在，一律 `tr -d '\r' < "$F" | grep -Fxq '...'`（`-x -F` 整行精確比對，也擋子字串誤判：查 "BDI" 會誤中 "BDI Universal Support"）；驗收用 `bash -c` 或 `/usr/bin/grep` 複驗，不在互動 shell 手測。交接書可直接寫這條。相關：[[profile-restore-order-and-flags]]、[[pgrep-self-match-beyond-brackets]]。

## pgrep-self-match-beyond-brackets

> 括號寫法擋不住所有 pgrep 自我匹配；命令列裡的路徑或 heredoc 也會中，要把檢查放進獨立腳本並分兩次呼叫

`pgrep -af '[M]odOrganizer'` 的括號只擋得住 pattern 本身。同一條命令列別處出現目標字串（MO2 完整路徑、heredoc 內容、MCP 設定 JSON），父 shell 的 cmdline 仍會被 `pgrep -f` 掃到，誤判程式在跑（2026-08-21）。Bash 工具用 `zsh -c '<整段命令>'` 執行，整段（含 heredoc）都在 cmdline 上。

**How to apply:** 查 Windows 程式在不在跑用 args 比對（`ps -eo args= | grep -Ei 'ModOrganizer\.exe|SkyrimSE\.exe'`）；Proton 下 comm 是 `main`／`Main`，比對 comm 恆為假陰性，見 [[verify-game-alive-via-qa-not-ps]]。args 比對同樣會掃到自己的命令列，照下句放進獨立腳本。`pgrep -x` 對超過 15 字元的名稱會報錯，不要用。一定要 `pgrep -f` 時，把檢查寫進獨立 `.sh`，**建立腳本與執行腳本分兩次 Bash 呼叫**。

相關：[[throttle-by-tree-not-by-name]]、[[driving-other-cli-agents]]

## wait-loop-cmdline-trips-process-detection

> 背景等待迴圈的命令列若含 `SkyrimSE.exe`／`ModOrganizer` 字樣，會讓按行程命令列判斷的工具（`profile_workflow.py record` 等）誤判遊戲在跑；條件永遠不成立的迴圈還會一直掛著

2026-11-22：`record` 回 `runtime: RUNNING`，命中的是另一個 shell 的等待迴圈（命令列含 `SkyrimSE.exe`），遊戲與 MO2 都沒在跑（[checkpoint-4 REPORT](../../agentctl/handoffs/home-2026-11-22/checkpoint-4/REPORT.md)）；`pgrep -f "ModOrganizer.exe|SkyrimSE.exe"` 也比對到自己（[profiles-main REPORT](../../agentctl/handoffs/home-2026-11-22/profiles-main/REPORT.md)）。與 [[pgrep-self-match-beyond-brackets]] 同源。

**How to apply:** 等待條件不要把行程名寫進自己的命令列——改看鎖檔，或把 args 比對放進獨立腳本（Proton 下 comm 不是執行檔名，見 [[verify-game-alive-via-qa-not-ps]]）；每個等待迴圈設上限（`timeout` 或次數），收線前確認沒有殘留迴圈。工具誤判時先 `ps -eo pid,args | grep -F SkyrimSE` 看命中的是誰。

## ls-is-eza-alias-use-bin-ls

> 這台機器互動 shell 的 `ls` 是 `eza --icons --git` 別名，對大目錄極慢且非 tty 環境輸出為空

互動殼的 `ls` 對大 repo 可能卡超過 120 秒；非 tty（腳本／子代理）下輸出是空的，會誤判「目錄是空的」（2026-09-25，`agentctl/handoffs/home-2026-10-17/structure-review/REPORT.md`）。跟 [[interactive-grep-is-ugrep]] 同屬本機別名陷阱。

**How to apply:** 腳本與子代理指令一律用 `/usr/bin/ls` 或 `find`。

## throttle-by-tree-not-by-name

> 多 agent 共機時,限流/kill 要按行程樹歸屬不能按行程名稱;houseCARL 每個 MCP client 各一份實例

houseCARL MCP 是 stdio MCP server，**每個 client（claude session、Claude Desktop…）各 spawn 一份**，還會洩漏 parent 已是 `systemd --user` 的孤兒（2026-08-21）。按名稱釘 `housecarl-mcp` 會打中全部實例，連別人的 session 一起拖慢；別人的 watchdog 按 `cc1plus`／`ld` 這種通用名稱掃，也會誤傷我的 build。

**規則**：限流／renice／kill 按行程樹歸屬：從自己已知的 pid 往下遞迴（`pgrep -P`）或用 cgroup／systemd scope；不用 `pgrep -f <名字>`／`pkill -f`。判斷 parent 讀 `/proc/<pid>/status` 的 `PPid:`，不解析 `ps` 的 `stat` 欄（comm 含空白或括號會解析錯）。歸屬判斷做不到就**不限流**。

被 systemd 收養的程序（如 `protontricks-launch`）祖先鏈追到 `ppid=1` 就斷，無法判斷發起者；鏈完整也不代表歸屬正確——要知道工作是誰的，直接問對方，不要看 `ps`。

收 tmux session 要逐一指名完整名稱，不用前綴萬用字元——相近前綴（如 `cx-hp1/2/3` vs `cx-hpa/b/c/d`）會互相誤殺（2026-10-23，`agentctl/handoffs/done/2026-09-01/hmpatch-2026-09-01/REPORT.md`）。

適用範圍：只限我方派出的行程，別的 session 見 [[dont-renice-other-sessions]]。

## dont-renice-other-sessions

> 2026-10-09 使用者喊停：遊戲卡頓時不准自行 renice／限流別的 session（如 simple_tools/aos-wt）的行程，只回報來源

2026-10-09 遊戲卡頓，負載來自另一個 Claude session 在 `simple_tools/aos-wt` 跑測試；頂層自行 renice 它的行程樹，使用者回「你不要調整這個=_=」。

**Why:** 別的 session 的行程是使用者自己的其他工作，優先權由他決定。

**How to apply:** 遊戲卡頓時只查證並回報「誰在吃 CPU」（行程樹、所屬 session／repo），由使用者決定要不要停。只有我方派出的線才可以限流或停。
