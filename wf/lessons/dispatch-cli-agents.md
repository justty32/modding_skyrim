# 調度：驅動 codex／tmux 與行程

[lessons 索引](README.md)

## driving-other-cli-agents

> 怎麼從 Claude Code 驅動同機的 pi / codex CLI agent——用 tmux，不是 stdin 注入；以及分工與護欄（原 type: memory）

使用者會把整條工作線外包給同機的其他 CLI agent（2026-08-06 起，例：`pi --provider deepseek --model deepseek-v4-pro`、`codex`），並要 Claude 去驅動它們。

**權威文件在 `~/repo/moddings/skyrim/agentctl/docs/`（2026-08-23 正規化），派線前先讀，不要憑本條目的細節行動**：

- `driving-codex.md` —— 切線、交接書契約、tmux 驅動、監看、收線的完整流程
- `resource-locks.md` —— 桌面 HID 鎖（跨 agent，**Aetheria 優先**）、遊戲鎖、CPU 限流、收工檢查
- `../tools/agent_inbox/PROTOCOL.md` —— 通訊契約與五種 STATUS 語意

**鎖的取得順序**：**先桌面 HID 鎖 `~/shared_agent_locks/desktop.lock`，再遊戲鎖 `agentctl/.lock/game.lock`**。跑 Skyrim 一定佔螢幕，反過來拿會跟 Aetheria 死鎖。遊戲鎖與 inbox 執行期資料的路徑從 repo 位置推導，不放 `~/skyrim_agent_out/`（該目錄 2026-08-22 已刪，指向它的檢查恆真）。

**「找到 process 丟 stdin」做不到**——互動 TUI 的 stdin 是 tty，寫 `/proc/<pid>/fd/0` 是寫到終端裝置（方向反了）；唯一能塞進 tty 輸入佇列的 `ioctl(TIOCSTI)` 被 `dev.tty.legacy_tiocsti=0` 關掉（kernel 6.2 起預設）。

**可行版本是 tmux**：`tmux new-session -d -s <name> -x 200 -y 50 -c <dir> '<agent cmd>'`，用 `send-keys -l '…'` 然後單獨一個 `Enter` 送指令（長交接書寫成檔案、只送路徑），`capture-pane -p -S -60` 讀畫面。使用者可 `attach` 同時插手，而且**他真的會**——看到 pane 裡有他自己打的字就別再代答。headless（`pi -p`、`codex exec`）留給要明確結果的單次任務。

**Why:** 多個 agent 併行時最大的風險不是能力而是撞車與越權。分工乾淨就沒事：各據一個獨立 git repo，母 repo 的 submodule 指標與計畫文件由 Claude 收。

**How to apply:**
- **交接書要寫死護欄**，特別是刪檔：agent 會把移進 `.quarantine/` 的隔離區整個刪掉（ext4 無快照，刪了就沒了）。護欄要寫到「隔離區本身也不准刪，回收前先問」。
- **會動 MO2／檔案系統的 agent 要架看門狗**：`Monitor` 輪詢「非測試用的 mod 資料夾是否消失」「Default profile 是否被改」。注意 `ls` 會給含空格的名字加引號，濾網要考慮。
- codex 表現穩：切 profile 前檢查 CRLF、測試 mod 用獨立命名、自己卸載並還原 active profile。它報「profiles repo 髒了不能裝」時通常是對的，先查 mtime 歸因再下結論。
- 相關：[[delegate-simple-work-to-sonnet]]、[[workspace-layout-and-duties]]

## codex-tmux-operational-notes

> 用 tmux 驅動 codex CLI 的實務細節——送出鍵要分開送、trust prompt、gpt-sol 的行為特性與該寫死的護欄（原 type: feedback）

**送指令要分兩次呼叫**：`tmux send-keys -t <s> -l '<文字>'` 之後的 `C-m`／`Enter` 如果**寫在同一個 Bash 呼叫裡**，codex TUI 常常只把文字放進 composer 而不送出（pane 上看到 `» <你的文字>` 就是還沒送）。要另外發一個 `tmux send-keys -t <s> C-m` 才會真的送出。每次送完務必 capture 確認開頭變成 `›` 且出現 `Working (`。

**啟動時會先問 trust**：`codex` 在新目錄第一次啟動會停在「Do you trust the contents of this directory?」，要送一個 Enter 才會進主畫面。`capture-pane -p -S -30` 在 alt-screen 下抓不到東西，**不要加 `-S`**。

**偵測 idle**：pane 裡有 `Working (` 就是忙碌，消失即該輪結束。用 Monitor 做 busy→idle 邊緣觸發通知，比自己輪詢省很多 token。

**模型與啟動**（2026-09-20）：`codex` 預設模型是 `gpt-6-astra medium`（不是 gpt-sol），要 gpt-sol 得另外確認別名。`codex -m gpt-sol` 回 `The 'gpt-sol' model is not supported when using Codex with a ChatGPT account`（2026-09-08）；交接書寫「gpt-sol」沒問題（是我們的暱稱），但啟動指令別帶 `-m gpt-sol`。

**gpt-sol 的行為特性**（使用者親口提醒 + 實測）：
- 會為了「更保險」跑一大堆與正事無關的驗證測試。**交接書要寫死「驗收就是這四條，一條不多，做完就停」**，實測有效。
- 2026-08-30 使用者心得——指揮 gpt-sol 要經常提醒它專注：「要他專注在真正重要的事情上，無關緊要的小事先別管」，否則它會一直寫測試一直驗證。這是動態手段，跟交接書「寫死驗收條數」（靜態）並列：交接書擋不住的過程漂移，靠 orders／tmux 中途提醒拉回來。逐模型指揮心得表在 agentctl/docs/team-model/speed-and-driving.md。
- subagent 使用者的界線是：**為了推進正事可以開，為了驗證／複查／風險掃描這種周邊小事不准開**。判準寫成「那個 subagent 的產出如果不在驗收清單裡，就不該開它」。
- 護欄遵守度高：叫它「遇到工具錯誤就停下回報」它真的會停——但它把**自己寫錯的 Python 引號**也算成工具錯誤而停工。交接書要區分「工具/環境錯誤 → 停」與「你自己的臨時腳本寫錯 → 自己修」。
- 給精確的預期數字（檔案數、bytes、tree SHA）它會照著對，不會含糊帶過。

**多線分工**：一條 MO2 live tree + profiles git、一條 submodule 原始碼、一條唯讀盤點寫 notes。同一個 git repo 有兩條線要 commit 時，交接書要寫「只准 `git add <明確路徑>`，禁止 `git add -A`，遇到 `.git/index.lock` 等幾秒重試、絕不刪 lock」。

**遊戲是獨佔資源**：MO2／Skyrim 同時只能一條線持有，而且**不能在另一條線正在搬 `overwrite/` 檔案時啟動**（遊戲會寫入 overwrite）。排程要自己當鎖來管。

**orders 檔不是即時剎車**（2026-09-25）：codex 線只在「每完成一步」才讀 `inbox/orders/<線>.md`，追加的「不降版、還原」order 擋不住它最後一步的 commit。要即時攔一條 codex 線，用 `tmux send-keys -t <線> Escape` 中斷再送新指令＋兩次 Enter，或直接 kill session；order 檔只適合「下一步前要看」的補充指示。線沒 push 的話可用 `reset --soft HEAD~1`＋`restore --staged --worktree -- <路徑>`＋刪新檔還原。

**改 `~/.codex/config.toml` 會殺掉所有正在跑的 codex session**（2026-08-20 實測：改一行後兩分鐘內四條線同秒結束，未落檔的在途工作全丟，只有已 commit 的存活）。codex 會監看設定檔並在變更時退出。**要改 codex 設定就先讓所有 session 收工，或接受重開的代價。** 排查時 `journalctl --user | grep 'tmux-spawn.*scope'` 會列出每個 scope 的 wall clock，能用起始時間反推是哪幾條線。

**houseCARL 在本機的已知壞法**：`Mo2InstanceDir` 模式不可用（MO2 的 `gamePath` 是 Wine 路徑 `Z:\home\...`，houseCARL 不做映射，會推出不存在的 `Z:\home\...\Data`）；正解是 explicit paths `HouseCarl__DataDir` / `ModsDir` / `ProfileDir`。`~/.codex/config.toml` 與 `~/.claude.json` 兩邊的 `ProfileDir` 都要指向現役 profile（2026-08-20 起是 `profiles/Modpack-KR`，兩邊都有 `.bak-20260820` 備份）；指著已退役的 profile 時每個 houseCARL 查詢都回 "No active plugins resolved"。`housecarl_bsa_list`（BSArch 走 wine）在這台機器讀 BSA 會 `wineserver: bind: Operation not permitted`，髮型「缺檔」判定要改用 python 直接掃 BSA 位元組，否則會假警報（2026-09-08）。

**任務結束就關掉 session，不要留著等下一批**（2026-08-21 量測後訂的規矩）。每個閒置的 codex session 持有一個 houseCARL MCP 實例，**實測平均 249 MB**；一夜六條線閒置共佔約 2.2 GB，關掉後釋出約 1.8 GB。要用時重開只要 30 秒，而交接書都寫在磁碟上，不依賴 session 記憶——這正是把成果寫成報告與交接書的意義。

資源影響要量了再說，不要沒量就說「影響接近零」。使用者說過「不要操我的電腦」。

**其他坑**：
- `inbox_send.sh` **沒有 `--body-file` 旗標**，正文檔是第 4 個位置參數，寫成旗標會靜默從 stdin 卡住（2026-09-20）。
- 交接書「只看 plugins.txt 帶 `*`」會漏掉隱含載入的 CC 與原版 master（1266 支＝1207 勾選＋59 隱含，2026-09-20）。
- codex sandbox 裡 `python -c` one-liner 的引號在 cmd.exe 下極易被拆壞，自證腳本一律寫成 `.py` 檔再跑（`agentctl/handoffs/done/2026-09-02/lorerim-2026-09-02/team-src/REPORT.md:100-102`）。
- 檢查環境變數是否設定別用 `${VAR:-no}`（已設定時會把值印出），改用 `[ -n "$VAR" ] && echo 有 || echo 無`（`agentctl/handoffs/done/2026-08-27/cx-dl/HANDOFF.md:122`）。
- `notify_watch.sh` 只監看 `inbox/new/`，子線回報其實路由到領導自己的 `mail/`，領導要主動對 `mail/` 跑 `--wait` 輪詢（`agentctl/handoffs/done/2026-08-30/opus-ops-2026-08-30/STATE.md:92`）。
- 互動 shell 的裸 `ls` 是 `eza --icons --git` 別名，大目錄下近似卡死，腳本與需要可靠速度的場合用 `/bin/ls`（`agentctl/handoffs/done/2026-08-30/opus-ops-2026-08-30/STATE.md:88`）。

相關：[[driving-other-cli-agents]]、[[delegate-simple-work-to-sonnet]]

## codex-tmux-enter-must-be-verified

> tmux 送提示詞給 codex 後 Enter 常沒送出（尤其長段中文），送完 5 秒內 capture-pane 看到「Working」才算開工，否則再送一次 Enter（原 type: memory）

2026-09-13：對剛啟動的 codex 送長段中文提示詞＋Enter，畫面看起來正常，字其實卡在輸入框（`›` 後面是提示詞、沒有 Working），白等 9 分鐘；補一次 Enter 就送出。工人在 Working 時追加的訊息也一樣：第一個 Enter 只把字放進 composer（顯示「tab to queue message」），要第二個 Enter 才進佇列。

**Why:** codex TUI 剛起來 15～20 秒內、或 bracketed paste 結束後，第一個 Enter 會被吃掉；畫面沒有錯誤，只看最後幾行很容易誤判已開工。

**How to apply:** 每次 `tmux send-keys ... Enter` 後 `sleep 4; tmux capture-pane -p | tail`，沒看到 `• Working` 或轉圈就再送一次 Enter；把這個檢查寫進等待迴圈的第一輪。
相關：[[codex-tmux-operational-notes]]、[[leads-must-not-end-turn-to-wait]]。

## tmux-working-text-is-not-liveness

> tmux pane 的「Working (Ns)」字樣可能是死 scrollback，判活要看 pane_pid 的子行程樹（原 type: project）

2026-09-01：tmux-resurrect 復原的 pane 會殘留舊 session 的「• Working (2m 20s)」字樣，計時器凍住其實是 codex 早已退出（pane 底部是 shell 提示字元、pane_pid 無子行程）。只盯畫面 hash 判「卡死」會白等。

**Why:** 畫面不動只證明畫面不動；「stuck」與「exited」要靠行程樹分辨。

**How to apply:**
- 判斷 codex/agent 線死活時，tmux capture-pane 之外必查 `pgrep -P <pane_pid>`（無子行程＝已退出）；監看腳本的停滯偵測要同時比對畫面與行程樹。
- 判斷另一條線死活別只憑 SESSION-LOG／line-claims 這類文件說鎖被誰持有，查文件當下可能剛好是空窗期，要 `tmux ls` 加當下鎖檔持有者同一時間點查（2026-10-23，`agentctl/handoffs/done/2026-08-30/modpack-2026-08-30/LEAD-NOTES.md:78-81`）。
- `codex exec` 中途出現大量 ERROR 不代表線已死，線可能繞路（借道其他 MCP）完成任務只是晚交件；判死只能看最終輸出／交付物是否存在（`agentctl/handoffs/done/2026-08-31/slim-modlib-2026-08-31/team-4/REPORT.md:298-308`）。

相關：[[pgrep-self-match-beyond-brackets]]、[[verify-game-alive-via-qa-not-ps]]。

## windows-codex-sandbox-pitfalls

> codex 在 Windows 沙箱一串環境陷阱：假 python3、git mv 做不到、exec 旗標、8.3 短檔名

Windows 的 codex 沙箱（2026-08-31／09-01）：`python3` 是 Store 假 shim，呼叫靜默失敗，`wf-lint.sh` 三項 python3 檢查會靜默跳過卻報綠燈；沙箱 `git mv` 做不到要改 `os.rename`；`codex exec` 另要 `cmd /c "...< NUL"`、非 git 目錄加 `--skip-git-repo-check`、單一可寫根（`agentctl/handoffs/done/2026-08-31/slim-modlib-2026-08-31/SPEC.md`）；`-C` 遇 8.3 短檔名觸發沙箱拒跑（`agentctl/handoffs/history/session-log/2026-08-30-to-09-01.md`）。

**Why:** Windows 的 codex 沙箱跟本機差異大，照搬交接書會假綠燈或拒跑。

**How to apply:** 派 codex 到 Windows 前寫死：呼叫 `python`、搬檔用 `os.rename`、`-C` 用完整長路徑、`exec` 按上述坑改寫。
