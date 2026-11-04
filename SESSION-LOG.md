# SESSION-LOG — 進度日誌 hub

只放還沒完成、且 agent 仍能主動推進的活狀態。已完成的實作與調查歷史由對應 plan、
子專案文件與 git history 承接；需要使用者、實機、權限或外部素材的項目只放
[WAIT_USER.md](WAIT_USER.md)。

**寫入時機**：① **開始**多步驟工作前就先寫一行 open（不是做完才寫）；② 每次 commit 後更新或刪除該行；
③ 條目格式 `- [工作流] 一句 open 狀態 → 下一步 / 連結`，完成即刪——歷史交給 git log，
「為什麼這樣選」落到 [wf/workflows/decisions.md](wf/workflows/decisions.md)。
某工作流長出自己的 `session-log.md` 時，在本檔加一列導流（見 [STRUCTURE](wf/STRUCTURE.md)）。

## 現役工作

- [refactor → tidy] 本輪八職設計工具依職責拆檔後，再整理現役交接與導航；Done when: 240 規則與既有 HTML／SVG 重產不變、必要測試通過、舊狀態不再覆蓋現況、收線提交與推送完成。
- [investigation] 戰鬥進階／高級效果全集調查尚未完成；家中持久17GB checkpoint已找回，45個具名原檔SHA全符，正續universe／scope有界閉合。今日Git PoE輸入不是全集包；[恢復實核](agentctl/handoffs/home-2026-11-04/evening-recovery/research/REPORT.md)與[NEXT](agentctl/handoffs/NEXT-SESSION.md)保留各族未完語義與來源身份。

## Durable 狀態入口

- 八職×三子類24設計樣板已補齊並通過語義／真圖核驗：[過目頁](wf/user/2026-11-04-all-classes.md)；新參數過目在WAIT_USER，沒有新source/runtime施工。
- NativeBridge f510已隔離build matching Windows x64 1.2.4.0，normal未開、未部署；[本輪證據](agentctl/handoffs/home-2026-11-04/evening-recovery/README.md)與[WAIT_USER](WAIT_USER.md)承接實機gate。
- DSP／houseCARL 已完成的離線修復、三條隔離分支與續接位置：
  [2026-10-21 離線成果與收尾](wf/user/2026-10-21-offline-fixes.md)
- 四條線的入口：各線 README；Skyrim 工作線交接主線在 `agentctl/SESSION-LOG.md`
- houseCARL fork 維護決策：
  [fork-maintenance-decision.md](analysis/houseCARL/answers/fork-maintenance-decision.md)
- houseCARL Linux/MO2 技術方案：
  [linux-manjaro-mo2-runbook.md](analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md)
- 需使用者或外部環境才能完成的工作：[WAIT_USER.md](WAIT_USER.md)
