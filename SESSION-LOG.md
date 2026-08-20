# SESSION-LOG — 進度日誌 hub

只放還沒完成、且 agent 仍能主動推進的活狀態。已完成的實作與調查歷史由對應 plan、
子專案文件與 git history 承接；需要使用者、實機、權限或外部素材的項目只放
[WAIT_USER.md](WAIT_USER.md)。

## 現役工作

截至 **2026-08-21 02:40（Asia/Taipei）**，母 repo 沒有仍在執行中的 agent 工作；Skyrim／MO2
已 teardown、遊戲鎖已釋放。今晚已完成的主要提交與 durable 狀態如下：

- `a10682d`、`4c6d5ae`：移除已由程式化 runtime 證據完成的 Scene Browser 舊待辦，並把
  `WAIT_USER.md` 的歷史 profile 名稱校正為唯一現役 `Modpack-KR` 的時序說明。
- `2574c9d`、`5a0e727`：校正 houseCARL runbook 的 `Modpack-KR` explicit path，將兩條 fork fix
  收束至 `ff802dd` 並更新 submodule pin；這一批已完成。
- `1938c4c`：將 agent-bridge pin 至 race-resistant HeavyArmor evidence reader `a278a4a`；已完成。
- `64a88a1`：將 scene-capture-bridge pin 至 placement drift 修正 `75308c9`；Armor、Editor commit
  與 save/load 的 runtime regression 已通過。未 commit ghost 的第三人稱攝影機語意仍待使用者
  選擇，列在 `WAIT_USER.md`，不冒充已決定。
- `2932152`、`b64e413`、`c7703d2`、`fe64d6f`、`b3dd673`：先完成 darksouls-port
  ghost-tol 0.02 全量門洞重建，再查明 `moshortcut` 被 Steam modal 阻塞的啟動根因；plain MO2
  workaround 解封後已做實體 `W` 時間軸測試。角色 6 秒後停在 `Y=1940.9648`，未達
  `Y<1803.84`，結論為 **FAIL**。`h0001B1A18` 的 planar-thresh 0.15/0.08/0.05/0.02 sweep
  不改 blocker cross-section，所以未提交無效參數變更；下一步是 player-capsule-aware 的局部門洞
  clearance 修法，細節歸檔於 `projects/darksouls-port/p1/P1-INGAME-FINDINGS.md`，不再列為
  `WAIT_USER.md` 的真人實走項目。
- `e9e2680`：新增 exact-version、45-record fail-closed 的 VIGILANT `BOOK.DESC` 私人修正產生器；
  工具已完成，1.8.2 是否升級仍不在本批範圍。

## Durable 狀態入口

- houseCARL fork 維護決策：
  [fork-maintenance-decision.md](analysis/houseCARL/answers/fork-maintenance-decision.md)
- houseCARL Linux/MO2 技術方案：
  [linux-manjaro-mo2-runbook.md](analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md)
- 需使用者或外部環境才能完成的工作：[WAIT_USER.md](WAIT_USER.md)

## 各工作流 session-log

| 工作流 | session-log | open 摘要 |
|--------|-------------|----------|
| feature-dev | [workflows/feature-dev/session-log.md](workflows/feature-dev/session-log.md) | 無 |
| refactor | [workflows/refactor/session-log.md](workflows/refactor/session-log.md) | 無 |
| investigation | [workflows/investigation/session-log.md](workflows/investigation/session-log.md) | 無 |
