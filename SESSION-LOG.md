# SESSION-LOG — 進度日誌 hub

只放還沒完成、且 agent 仍能主動推進的活狀態。已完成的實作與調查歷史由對應 plan、
子專案文件與 git history 承接；需要使用者、實機、權限或外部素材的項目只放
[WAIT_USER.md](WAIT_USER.md)。

**寫入時機**：① **開始**多步驟工作前就先寫一行 open（不是做完才寫）；② 每次 commit 後更新或刪除該行；
③ 條目格式 `- [工作流] 一句 open 狀態 → 下一步 / 連結`，完成即刪——歷史交給 git log，
「為什麼這樣選」落到 [wf/workflows/decisions.md](wf/workflows/decisions.md)。
某工作流長出自己的 `session-log.md` 時，在本檔加一列導流（見 [STRUCTURE](wf/STRUCTURE.md)）。

## 現役工作

- [investigation] 11-04 家中恢復核驗進行中：17 repo 已同步；隔離恢復 NativeBridge f510 並核 matching build 環境，同時唯讀核昨晚持久研究備份與最小續行資料 → [本輪入口](agentctl/handoffs/home-2026-11-04/evening-recovery/README.md)。不部署或擴型。

- [feature-dev] NativeBridge f510家中matching Windows x64 1.2.4.0已隔離build，normal未開、未部署，仍待家中live驗證。證據見[本輪build](agentctl/handoffs/home-2026-11-04/evening-recovery/native/REPORT.md)；後續依[WAIT_USER](WAIT_USER.md)的實機gate續行，不自動開runtime或擴型。

- [investigation] 戰鬥進階／高級效果全集調查尚未完成；家中持久17GB checkpoint已找回，45個具名原檔SHA全符，正續universe／scope有界閉合。今日Git PoE輸入不是全集包；[恢復實核](agentctl/handoffs/home-2026-11-04/evening-recovery/research/REPORT.md)與[NEXT](agentctl/handoffs/NEXT-SESSION.md)保留各族未完語義與來源身份。

- [planning] 浪潮鬥士／守衛者後續規則強度、未實作能力與實機可行性仍待裁示／驗證；不得把設計候選當runtime支援。待辦邊界見[浪潮交接](agentctl/handoffs/home-2026-11-04/guard-double-beat/README.md)與[守衛交接](agentctl/handoffs/home-2026-11-04/warden-sample/README.md)，未獲下一步授權不自動續施工。

## Durable 狀態入口

- DSP／houseCARL 已完成的離線修復、三條隔離分支與續接位置：
  [2026-10-21 離線成果與收尾](wf/user/2026-10-21-offline-fixes.md)
- 四條線的入口：各線 README；Skyrim 工作線交接主線在 `agentctl/SESSION-LOG.md`
- houseCARL fork 維護決策：
  [fork-maintenance-decision.md](analysis/houseCARL/answers/fork-maintenance-decision.md)
- houseCARL Linux/MO2 技術方案：
  [linux-manjaro-mo2-runbook.md](analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md)
- 需使用者或外部環境才能完成的工作：[WAIT_USER.md](WAIT_USER.md)
