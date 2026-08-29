# SESSION-LOG — 進度日誌 hub

只放還沒完成、且 agent 仍能主動推進的活狀態。已完成的實作與調查歷史由對應 plan、
子專案文件與 git history 承接；需要使用者、實機、權限或外部素材的項目只放
[WAIT_USER.md](WAIT_USER.md)。

## 現役工作

截至 **2026-08-29 早上（Asia/Taipei）**，母 repo 本身沒有進行中的 agent 工作。Skyrim／MO2 已關閉。
同日使用者外出期間會**遠端驅動 gpt-sol（codex）**在本工作區做上網調查／下載 mod 這類
**不開遊戲、不開 MO2、不寫 `instance/`** 的線；線的認領、鎖與回報一律照
[`agentctl/`](agentctl/README.md)（2026-08-27 起：Fable 頂層決策、Opus 中層管理、codex／sonnet 執行；
先全部調查完再一次施工）。

**2026-08-23 的主線是工作區統整**（[consolidation-2026-08-23](wf/workflows/plans/consolidation-2026-08-23/README.md)）。
日常工作現在分成四條獨立的線，各自是 private submodule：

| 線 | 管什麼 |
|---|---|
| [`instance/`](instance/) | 本機部署狀態：MO2 instance、現役 profile `modpack-main`、load order、profile 稽核 |
| [`mod-library/`](mod-library/) | mod 庫：MongoDB 索引、自製繁中翻譯層、自製插件與修正 esp |
| [`modpack-design/`](modpack-design/) | 整合包設計：Gameplay 遷移批次、技術債、選型調查 |
| [`agentctl/`](agentctl/) | AI 操控總控：工作流、agent 交接、QA harness、執行證據 |

各線自己的續行點在 [`agentctl/SESSION-LOG.md`](agentctl/SESSION-LOG.md)——那是 Skyrim 工作線的交接主線。
**本檔只管母 repo。**

## Durable 狀態入口

- 四條線的入口：各線 README；Skyrim 工作線交接主線在 `agentctl/SESSION-LOG.md`
- houseCARL fork 維護決策：
  [fork-maintenance-decision.md](analysis/houseCARL/answers/fork-maintenance-decision.md)
- houseCARL Linux/MO2 技術方案：
  [linux-manjaro-mo2-runbook.md](analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md)
- 需使用者或外部環境才能完成的工作：[WAIT_USER.md](WAIT_USER.md)

## 各工作流 session-log

| 工作流 | session-log | open 摘要 |
|--------|-------------|----------|
| feature-dev | [workflows/feature-dev/session-log.md](wf/workflows/feature-dev/session-log.md) | 無 |
| refactor | [workflows/refactor/session-log.md](wf/workflows/refactor/session-log.md) | 無 |
| investigation | [workflows/investigation/session-log.md](wf/workflows/investigation/session-log.md) | 無 |
