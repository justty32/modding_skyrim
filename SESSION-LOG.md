# SESSION-LOG — 進度日誌 hub

只放還沒完成、且 agent 仍能主動推進的活狀態。已完成的實作與調查歷史由對應 plan、
子專案文件與 git history 承接；需要使用者、實機、權限或外部素材的項目只放
[WAIT_USER.md](WAIT_USER.md)。

## 現役工作

截至 **2026-08-21 01:16（Asia/Taipei）**，母 repo 沒有仍在執行中的 agent 工作；今晚
22:00 後的母 repo 變更已收束為 9 筆 commit（交辦同步時原為 8 筆，01:16 另加入
`b64e413`）：

- `a10682d`、`4c6d5ae`：移除已由程式化 runtime 證據完成的 Scene Browser 舊待辦，並把
  `WAIT_USER.md` 的歷史 profile 名稱校正為唯一現役 `Modpack-KR` 的時序說明。
- `2574c9d`、`5a0e727`：校正 houseCARL runbook 的 `Modpack-KR` explicit path，將兩條 fork fix
  收束至 `ff802dd` 並更新 submodule pin；這一批已完成。
- `1938c4c`：將 agent-bridge pin 至 race-resistant HeavyArmor evidence reader `a278a4a`；已完成。
- `64a88a1`：將 scene-capture-bridge pin 至 placement drift 修正 `75308c9`；Armor、Editor commit
  與 save/load 的 runtime regression 已通過。未 commit ghost 的第三人稱攝影機語意仍待使用者
  選擇，列在 `WAIT_USER.md`，不冒充已決定。
- `2932152`、`b64e413`：將 darksouls-port pin 至 ghost-tol 0.02 全量門洞重建及 01:16 runtime
  紀錄。離線重建已完成；本次 Skyrim 未成功啟動，故實走結論仍是 **inconclusive**，不是門洞
  PASS 或 FAIL，後續真人走門保留在 `WAIT_USER.md`。
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
