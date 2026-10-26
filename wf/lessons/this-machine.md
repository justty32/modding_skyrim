# 本機環境特性（shell、行程、工具差異）

[lessons 索引](README.md)

這台機器（Manjaro／Wayland＋KDE）上，互動 shell 與腳本環境的差異會讓「手測過了」的驗收失真。本檔收這類環境陷阱。

## interactive-grep-is-ugrep

> 家中機互動 shell 的 grep 綁成 ugrep（-x 容忍 CRLF 尾端 \r），腳本裡的 /usr/bin/grep 是 GNU grep 不容忍；手測過的 grep 驗收不可信

2026-09-05 實測：`grep is a shell function`（shell snapshot）→ ugrep 7.8.4；`#!/usr/bin/env bash` 腳本解析到 `/usr/bin/grep` 3.12。MO2 的 `modlist.txt`／`plugins.txt` 全是 CRLF，`grep -Fxq '+Mod Name' modlist.txt` 互動下 rc=0、腳本裡 rc=1。

**Why:** 互動手測與腳本執行走不同的 grep，CRLF 檔案上結果相反；線會以為驗收過了。

**How to apply:** 對 profiles 檔的精確行比對一律 `tr -d '\r' < "$F" | grep -Fxq '...'`（或 `grep -Fxq $'...\r'` 之外再比 LF）；驗收腳本用 `bash -c` 或 `/usr/bin/grep` 複驗，不在互動 shell 手測。交接書可直接寫這條。相關：[[profile-restore-order-and-flags]]、[[pgrep-self-match-beyond-brackets]]。

對 modlist/plugins 單行存在性判斷一律用 `grep -x -F` 整行精確比對，不只是為了 CRLF，也擋掉子字串誤判（2026-10-23；查 "BDI" 會誤中 "BDI Universal Support"、查 "Math" 會誤中 "Math Plugin"）。

## pgrep-self-match-beyond-brackets

> 括號寫法擋不住所有 pgrep 自我匹配；命令列裡的路徑或 heredoc 也會中，要把檢查放進獨立腳本並分兩次呼叫

`pgrep -af '[M]odOrganizer'` 的括號寫法只擋得住「pattern 本身」被匹配。如果同一條命令列的其他地方出現目標字串（MO2 完整路徑、heredoc 內容、MCP 設定 JSON），父 shell 的 cmdline 仍會被 `pgrep -f` 掃到，於是誤判「程式正在執行」（2026-08-21）。

**Why:** Bash 工具是用 `zsh -c '<整段命令>'` 執行的，整段命令（含 heredoc 內文）都在那個行程的 cmdline 裡；`pgrep -f` 掃的就是 cmdline。

**How to apply:** 檢查 Windows 程式是否在跑，用 `ps -eo comm= | grep -qx 'ModOrganizer.ex'`（comm 只有執行檔名、截斷 15 字元、不含參數，不會自我匹配）。`pgrep -x` 對超過 15 字元的名稱會直接報錯，不要用。若一定要用 `pgrep -f`，把檢查寫進獨立 `.sh`，並且**建立腳本與執行腳本分成兩次 Bash 呼叫**——同一次呼叫裡 heredoc 內容還在父 shell 的 cmdline 上。

相關：[[throttle-by-tree-not-by-name]]、[[driving-other-cli-agents]]

## ls-is-eza-alias-use-bin-ls

> 這台機器互動 shell 的 `ls` 是 `eza --icons --git` 別名，對大目錄極慢且非 tty 環境輸出為空

互動殼下 `ls` 是 eza 別名，對大 repo 可能卡超過 120 秒；非 tty（腳本／子代理）環境下輸出直接是空的，容易誤判「目錄是空的」（2026-09-25、2026-10-17 多線踩到，`agentctl/handoffs/home-2026-10-17/structure-review/REPORT.md`）。

**Why:** 跟 [[interactive-grep-is-ugrep]] 同屬本機別名陷阱：手測看起來正常，腳本/子代理跑起來行為完全不同。

**How to apply:** 腳本與子代理指令一律用 `/usr/bin/ls` 或 `find`，不要依賴互動殼的 `ls` 別名。
