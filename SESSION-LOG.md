# SESSION-LOG — 進度日誌 hub

只放還沒完成、且 agent 仍能主動推進的活狀態。已完成的實作與調查歷史由對應 plan、
子專案文件與 git history 承接；需要使用者、實機、權限或外部素材的項目只放
[WAIT_USER.md](WAIT_USER.md)。

**寫入時機**：① **開始**多步驟工作前就先寫一行 open（不是做完才寫）；② 每次 commit 後更新或刪除該行；
③ 條目格式 `- [工作流] 一句 open 狀態 → 下一步 / 連結`，完成即刪——歷史交給 git log，
「為什麼這樣選」落到 [wf/workflows/decisions.md](wf/workflows/decisions.md)。
某工作流長出自己的 `session-log.md` 時，在本檔加一列導流（見 [STRUCTURE](wf/STRUCTURE.md)）。

## 現役工作

- [tidy] **已完成（2026-09-01 實查全部已 push）**：母 repo ＋15 個 submodule 全部乾淨、ahead/behind 皆 0；
  逐個以 `git rev-list --left-right --count @{u}...HEAD` 及本地 remote-tracking ref 核對（本次未 fetch），母 repo
  記錄的 15 個 gitlink commit 也全部存在對應 `origin/main`。附註：`agentctl` 與 `instance` 仍是 detached HEAD，
  但 HEAD commit 已被 `origin/main` 包含，待日後 checkout 回 `main`。之後若要用 `${instance}` 這類專案變數，在各 repo
  `wf/tools/fmt-vars.local.json` 加，需要新的 `how`（固定子路徑）再升 kernel。規則出處：
  [wf/workflows/tidy/README.md](wf/workflows/tidy/README.md)、[data-files](wf/workflows/common/data-files.md)。
- [tidy] 2026-08-29 調查線留下 7 個裁示已落 [WAIT_USER.md](WAIT_USER.md)（later-decisions 六項、feature-runtime DSPortP2）；等使用者。

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
