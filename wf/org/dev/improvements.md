開發部門 `dev` 的改進紀錄：一行一項，看到什麼 → 提案 → 狀態。

# 改進紀錄：`dev`

回 [卡](README.md)。規矩見 [sites](../sites.md)「公司場的空檔拿來改進」（使用者 2026-11-25，D36）。

- **看到**：`autocrlf=true` 的 checkout 把 `.sh` 寫成 CRLF、在 WSL 跑不起來；之前在母 repo、agentctl、modpack-design、model-converter 各修過一次，11-25 公司場又因此紅了 game-data、plugin1、instance → **提案**：每個有 `.sh` 的 repo 都補 `*.sh text eol=lf` → **狀態**：`main` 2026-11-25 代做，12 個 repo 已補、審查通過；回家驗，經過見 11-25 STATE。
- **看到**：審查代班指出 ModForge `skylink-call.py`、agent-bridge `qa_mcp.py`／`mo2ctl.py`／`qa_runner.py` 是直接執行的 `.py`，在 CRLF 工作樹 shebang 會壞 → **提案**：替有 shebang 的 `.py` 補 LF 規則 → **狀態**：提案，都要遊戲或 MO2 才用得到，還沒做。
