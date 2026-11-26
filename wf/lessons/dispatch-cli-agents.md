# 調度：驅動 CLI agent／tmux 與多線護欄

[lessons 索引](README.md)

codex 2026-11-24 退役（D20，[decisions](../org/decisions.md)）；現役工人的掛法與選型見 [fsm-gpt 操作單](../../agentctl/aos/fsm-gpt/RUNBOOK.md) 與 [team-model](../../agentctl/docs/team-model.md)。本檔只留不綁 codex 的做法。

## driving-other-cli-agents

> 從 Claude Code 驅動同機的互動式 CLI agent：用 tmux，不是 stdin 注入；鎖的取得順序與護欄

使用者會把整條工作線外包給同機的其他 CLI agent（2026-08-06 起，例：`pi --provider deepseek --model deepseek-v4-pro`），並要 Claude 去驅動它們。

- **「找到 process 丟 stdin」做不到**：互動 TUI 的 stdin 是 tty，寫 `/proc/<pid>/fd/0` 是寫到終端裝置（方向反了）；唯一能塞進 tty 輸入佇列的 `ioctl(TIOCSTI)` 被 `dev.tty.legacy_tiocsti=0` 關掉（kernel 6.2 起預設）。
- **可行版本是 tmux**：`tmux new-session -d -s <name> -x 200 -y 50 -c <dir> '<agent cmd>'`，`send-keys -l '…'` 後單獨一個 `Enter` 送出（長交接書寫成檔案、只送路徑），`capture-pane -p` 讀畫面。使用者可 `attach` 同時插手，而且**他真的會**——pane 裡有他自己打的字就別再代答。要明確結果的單次任務用 headless（如 `pi -p`）。
- **鎖的取得順序**：先桌面 HID 鎖 `~/shared_agent_locks/desktop.lock`，再遊戲鎖 `agentctl/.lock/game.lock`（[resource-locks](../../agentctl/docs/resource-locks.md)）。跑 Skyrim 一定佔螢幕，反過來拿會跟其他持鎖線死鎖。鎖路徑從 repo 位置推導；`~/skyrim_agent_out/` 已不存在，指向它的檢查恆真。

**Why:** 多個 agent 併行時最大的風險是撞車與越權，不是能力。各據一個獨立 git repo，母 repo 的 submodule 指標與計畫文件由 Claude 收。

**How to apply:**
- **交接書寫死刪檔護欄**：agent 會把移進 `.quarantine/` 的隔離區整個刪掉（ext4 無快照）。要寫到「隔離區本身也不准刪，回收前先問」。
- **會動 MO2／檔案系統的 agent 要架看門狗**：`Monitor` 輪詢「非測試用的 mod 資料夾是否消失」「Default profile 是否被改」；`ls` 會給含空格的名字加引號，濾網要考慮。

相關：[[delegate-simple-work-to-sonnet]]、[[workspace-layout-and-duties]]

## codex-tmux-operational-notes

> 派工人的交接書與多線運作的通用護欄：驗收條數寫死、工具錯與自己腳本錯分開、給精確預期數字、一樹一個 commit 者、遊戲獨佔、資源量了再說

- **gpt-sol 會為了「更保險」跑一大堆無關驗證**：交接書寫死「驗收就是這四條，一條不多，做完就停」，實測有效；產出要直接服務固定驗收，不展開無關複查。過程中的漂移靠中途提醒拉回——2026-08-30 使用者心得：「要他專注在真正重要的事情上，無關緊要的小事先別管」。逐模型指揮心得在 [speed-and-driving.md](../../agentctl/docs/team-model/speed-and-driving.md)。
- 叫工人「遇到工具錯誤就停下回報」，它會把**自己寫錯的 Python 引號**也算成工具錯誤而停工：交接書要區分「工具/環境錯誤 → 停」與「你自己的臨時腳本寫錯 → 自己修」。
- 給精確的預期數字（檔案數、bytes、tree SHA），它會照著對，不會含糊帶過。

多線與資源：

- **同一工作樹只指定一條線 commit**；交接書寫「只准 `git add <明確路徑>`，禁止 `git add -A`，遇到 `.git/index.lock` 等幾秒重試、絕不刪 lock」。
- **遊戲是獨佔資源**：MO2／Skyrim 同時只能一條線持有，而且不能在另一條線正在搬 `overwrite/` 檔案時啟動（遊戲會寫入 overwrite）。
- houseCARL 的現役 profile／路徑與 BSA 判定先走 [工具索引](../../agentctl/docs/tool-index.md) 的 mirror／smoke；舊 profile 名不沿用，工具失敗不當缺檔證據。
- **任務結束就關掉 session／工人，不留著等下一批**：閒置行程各持一個 houseCARL MCP 實例（每個數百 MB）；交接書都在磁碟上，重開不依賴 session 記憶。
- 資源影響要量了再說，不要沒量就說「影響接近零」。使用者說過「不要操我的電腦」。

小坑：

- 檢查環境變數是否設定別用 `${VAR:-no}`（已設定時會把值印出），改用 `[ -n "$VAR" ] && echo 有 || echo 無`（`agentctl/handoffs/done/2026-08-27/cx-dl/HANDOFF.md:122`）。
- md 信箱（2026-11-14 起凍結，[FROZEN](../../agentctl/inbox/FROZEN.md)；解凍或讀舊信時才適用）：`inbox_send.sh` 沒有 `--body-file` 旗標，正文檔是第 4 個位置參數，寫成旗標會靜默從 stdin 卡住（2026-09-20）；`notify_watch.sh` 只監看 `inbox/new/`，子線回報路由到領導自己的 `mail/`，領導要主動對 `mail/` 跑 `--wait` 輪詢（`agentctl/handoffs/done/2026-08-30/opus-ops-2026-08-30/STATE.md:92`）。

相關：[[driving-other-cli-agents]]、[[delegate-simple-work-to-sonnet]]

## tmux-working-text-is-not-liveness

> tmux pane 的「Working (Ns)」字樣可能是死 scrollback，判活要看 pane_pid 的子行程樹

2026-09-01：tmux-resurrect 復原的 pane 殘留舊 session 的「• Working (2m 20s)」字樣，計時器凍住，其實 agent 早已退出（pane 底部是 shell 提示字元、pane_pid 無子行程）。

**Why:** 畫面不動只證明畫面不動；「stuck」與「exited」要靠行程樹分辨。

**How to apply:**
- 判 agent 線死活時，capture-pane 之外必查 `pgrep -P <pane_pid>`（無子行程＝已退出）；監看腳本的停滯偵測要同時比對畫面與行程樹。
- 判另一條線死活別只憑 SESSION-LOG／line-claims 這類文件說鎖被誰持有（查的當下可能是空窗期），要 `tmux ls` 加當下鎖檔持有者同一時間點查（2026-10-23，`agentctl/handoffs/done/2026-08-30/modpack-2026-08-30/LEAD-NOTES.md:78-81`）。
- 工人中途出現大量 ERROR 不代表線已死，它可能繞路（借道其他 MCP）完成、只是晚交件；判死只看最終輸出／交付物是否存在（`agentctl/handoffs/done/2026-08-31/slim-modlib-2026-08-31/team-4/REPORT.md:298-308`）。

相關：[[pgrep-self-match-beyond-brackets]]、[[verify-game-alive-via-qa-not-ps]]
