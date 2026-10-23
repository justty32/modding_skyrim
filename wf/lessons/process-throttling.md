# 行程限流與別線行程的分寸

[lessons 索引](README.md)

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

2026-10-23 補：同理，收線 `kill` tmux session 要逐一指名完整 session 名稱，不要用前綴萬用字元掃描殺——當天有多隊各自用相近前綴（`cx-hp1/2/3` vs `cx-hpa/b/c/d`）會互相誤殺（`agentctl/handoffs/done/2026-09-01/hmpatch-2026-09-01/REPORT.md`）。

## dont-renice-other-sessions

> 2026-10-09 使用者喊停：遊戲卡頓時不准自行 renice／限流別的 session（如 simple_tools/aos-wt）的行程，只回報來源

2026-10-09 使用者玩遊戲回報卡頓，我查到負載來自另一個 Claude session 在 `simple_tools/aos-wt` 跑測試，就自行 renice 它的行程樹；使用者回「你不要調整這個=_=」。

**Why:** 別的 session 的行程是使用者自己的其他工作，優先權由他決定；擅自調整等於替他做取捨。

**How to apply:** 遊戲卡頓時只查證並回報「誰在吃 CPU」（行程樹、所屬 session／repo），由使用者決定要不要停。只有我方派出的線才可以限流或停。這條修正 [[throttle-by-tree-not-by-name]] 的適用範圍：那條只適用於我方行程。
