# SESSION-LOG — 進度日誌 hub

只放還沒完成、且 agent 仍能主動推進的活狀態。已完成的實作與調查歷史由對應 plan、
子專案文件與 git history 承接；需要使用者、實機、權限或外部素材的項目只放
[WAIT_USER.md](WAIT_USER.md)。

**寫入時機**：① **開始**多步驟工作前就先寫一行 open（不是做完才寫）；② 每次 commit 後更新或刪除該行；
③ 條目格式 `- [工作流] 一句 open 狀態 → 下一步 / 連結`，完成即刪——歷史交給 git log，
「為什麼這樣選」落到 [wf/workflows/decisions.md](wf/workflows/decisions.md)。
某工作流長出自己的 `session-log.md` 時，在本檔加一列導流（見 [STRUCTURE](wf/STRUCTURE.md)）。

## 現役工作

- [modpack-planning] 2026-09-03 白天場已收工；續行 [`agentctl/handoffs/NEXT-SESSION.md`](agentctl/handoffs/NEXT-SESSION.md)
- [modpack-planning] 待使用者：AE DLC、新周目、LoreRim／GO19 與清理裁示 → [`WAIT_USER.md`](WAIT_USER.md)

2026-08-23 工作區統整的歷史見
[consolidation-2026-08-23](wf/workflows/plans/consolidation-2026-08-23/README.md)；四條日常主線與職責見
[`README.md`](README.md#四條主線)。Skyrim 工作線交接主線在 [`agentctl/SESSION-LOG.md`](agentctl/SESSION-LOG.md)，
**本檔只管母 repo**。

## Durable 狀態入口

- 四條線的入口：各線 README；Skyrim 工作線交接主線在 `agentctl/SESSION-LOG.md`
- houseCARL fork 維護決策：
  [fork-maintenance-decision.md](analysis/houseCARL/answers/fork-maintenance-decision.md)
- houseCARL Linux/MO2 技術方案：
  [linux-manjaro-mo2-runbook.md](analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md)
- 需使用者或外部環境才能完成的工作：[WAIT_USER.md](WAIT_USER.md)
