# SESSION-LOG — 進度日誌 hub

只放還沒完成、且 agent 仍能主動推進的活狀態。已完成的實作與調查歷史由對應 plan、
子專案文件與 git history 承接；需要使用者、實機、權限或外部素材的項目只放
[WAIT_USER.md](WAIT_USER.md)。

**寫入時機**：① **開始**多步驟工作前就先寫一行 open（不是做完才寫）；② 每次 commit 後更新或刪除該行；
③ 條目格式 `- [工作流] 一句 open 狀態 → 下一步 / 連結`，完成即刪——歷史交給 git log，
「為什麼這樣選」落到 [wf/workflows/decisions.md](wf/workflows/decisions.md)。
某工作流長出自己的 `session-log.md` 時，在本檔加一列導流（見 [STRUCTURE](wf/STRUCTURE.md)）。

## 現役工作

目前沒有已授權主動續行的工作。

## 暫凍（非現役）

使用者2026-11-05暫時凍結 PoE 星盤，等重新指示，不自動研究／設計／實作／部署／驗收。範圍含本輪星盤 IndependentSkills 1.2.x／NativeBridge 候選、24型設計（刻印／浪潮鬥士／守衛者等）及直接服務星盤的全量戰鬥效果研究；不視為取消或完成，不刪資料、不撤既有部署。未確認獨立用途的研究分支保守暫停；一般戰鬥 mod、共用工具及非PoE工作不因此凍結。 續接證據見 [NEXT](agentctl/handoffs/NEXT-SESSION.md)。
