# 調度、模型分級與交接書（9/9）

[lessons 索引](README.md)｜同主題：[dispatch-and-agents](dispatch-and-agents.md)、[dispatch-and-agents-2](dispatch-and-agents-2.md)、[dispatch-and-agents-3](dispatch-and-agents-3.md)、[dispatch-and-agents-4](dispatch-and-agents-4.md)、[dispatch-and-agents-5](dispatch-and-agents-5.md)、[dispatch-and-agents-6](dispatch-and-agents-6.md)、[dispatch-and-agents-7](dispatch-and-agents-7.md)、[dispatch-and-agents-8](dispatch-and-agents-8.md)

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
