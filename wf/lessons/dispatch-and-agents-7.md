# 調度、模型分級與交接書（7/9）

[lessons 索引](README.md)｜同主題：[dispatch-and-agents](dispatch-and-agents.md)、[dispatch-and-agents-2](dispatch-and-agents-2.md)、[dispatch-and-agents-3](dispatch-and-agents-3.md)、[dispatch-and-agents-4](dispatch-and-agents-4.md)、[dispatch-and-agents-5](dispatch-and-agents-5.md)、[dispatch-and-agents-6](dispatch-and-agents-6.md)、[dispatch-and-agents-8](dispatch-and-agents-8.md)、[dispatch-and-agents-9](dispatch-and-agents-9.md)

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
