# SESSION-LOG — 進度日誌 hub

只放還沒完成、且 agent 仍能主動推進的活狀態。已完成的實作與調查歷史由對應 plan、
子專案文件與 git history 承接；需要使用者、實機、權限或外部素材的項目只放
[WAIT_USER.md](WAIT_USER.md)。

## 現役工作

截至 **2026-08-23（Asia/Taipei）**，母 repo 沒有仍在執行中的 agent 工作，也沒有 codex 線在跑；
Skyrim／MO2 已關閉，兩個資源鎖都未持有。

**2026-08-23 的主線是工作區統整**（[consolidation-2026-08-23](workflows/plans/consolidation-2026-08-23.md)）。
日常工作現在分成四條獨立的線，各自是 private submodule：

| 線 | 管什麼 |
|---|---|
| [`instance/`](instance/) | 本機部署狀態：MO2 instance、現役 profile `modpack-main`、load order、profile 稽核 |
| [`mod-library/`](mod-library/) | mod 庫：MongoDB 索引、自製繁中翻譯層、自製插件與修正 esp |
| [`modpack-design/`](modpack-design/) | 整合包設計：六階段整包計畫、技術債、選型調查 |
| [`agentctl/`](agentctl/) | AI 操控總控：工作流、agent 交接、QA harness、執行證據 |

各線自己的續行點在 [`agentctl/SESSION-LOG.md`](agentctl/SESSION-LOG.md)——那是 Skyrim 工作線的交接主線。
**本檔只管母 repo。**

## 2026-08-23 已收束

- **工作區統整**：`~/notes/projects/modding/skyrim` 的 1047 檔依性質分流到四條線，
  逐檔比對驗證；實機截圖與 MongoDB 快照刻意留在 repo 外。順帶修掉一個曝險——
  `dist/mods/` 的 34 個翻譯層內含他人 mod 的完整原始 ESP，一直躺在這個 public repo 裡。
- **MO2 profile 改名**：`Modpack-KR` → `main` → `modpack-main`（前綴是為了不跟分支名撞）。
  走完 `feat → release → main`；`check_profiles.py` 新增 `selected_profile` 比對，
  補上一道從來沒有的閘門。
- **中文層排序失效**：四個覆蓋層裝在本體下方而完全失效（11 個檔被英文本體贏走），已上移並晉升。
  常駐稽核 `mod-library/l10n/tools/audit_layer_priority.py`。
- **agent 協作協議正規化**：`agentctl/docs/driving-codex.md` 與 `resource-locks.md`；
  修好兩個指向已刪除 `~/skyrim_agent_out` 的死路徑（遊戲鎖與 inbox）。
- **連結檢查涵蓋四條線**：`git ls-files` 到 gitlink 就停，四條線的 87 個壞連結沒人在看。
  全數修復，檢查器改為連 submodule 一起掃（427 檔 → 789 檔）。
- **Downloads 歸檔**：113 個 Skyrim mod 壓縮檔逐一開檔判斷，61 個新的入 `~/skyrim_mods/hdd/`。

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
| feature-dev | [workflows/feature-dev/session-log.md](workflows/feature-dev/session-log.md) | 無 |
| refactor | [workflows/refactor/session-log.md](workflows/refactor/session-log.md) | 無 |
| investigation | [workflows/investigation/session-log.md](workflows/investigation/session-log.md) | 無 |
