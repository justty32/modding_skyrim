# 回家第一場執行單（2026-09-01）

順序採「已有可交付產物 → 獨立環境 gate → 單組 archive gate → 現役 winner patch →
4–6 件生態 preflight」。這是本單依剩餘相依與接觸面做的排序：DMK 已有離線 PASS 產物但未部署／
實機驗收，scene-capture-bridge 卡在指定 Windows MinGW 環境，Mihail 則要逐件處理 4–6 組輸入
（`agentctl/handoffs/rtqa-2026-08-31/reports/dmk.md:46`；
`agentctl/handoffs/rtqa-2026-08-31/reports/dmk.md:50`；
`agentctl/handoffs/wu-2026-08-31/CLEANUP.md:43`；`wait-user/home-setup.md:14`）。

## 1. DMK 1.5.0 人工校對版

內容見 [dmk.md](home-runbook-2026-09-01/dmk.md)。

## 2. scene-capture-bridge 完整離線測試

內容見 [offline-gates.md](home-runbook-2026-09-01/offline-gates.md)。

## 3. SDA 4.3.2 exact 簡中 topology gate

內容見 [offline-gates.md](home-runbook-2026-09-01/offline-gates.md)。

## 4. Bandolier NPC 中文 forward patch（已作廢 —— 2026-09-01 使用者裁示 Bandolier 併入 clothes purge）

內容見 [bandolier.md](home-runbook-2026-09-01/bandolier.md)。

## 5. Mihail 自然核心首批 4–6 件 preflight

內容見 [mihail-priority.md](home-runbook-2026-09-01/mihail-priority.md)。

## 今晚如果只做得完一件

內容見 [mihail-priority.md](home-runbook-2026-09-01/mihail-priority.md)。

