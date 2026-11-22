# SESSION-LOG — 進度日誌 hub

只放還沒完成、且 agent 仍能主動推進的活狀態。已完成的實作與調查歷史由對應 plan、
子專案文件與 git history 承接；需要使用者、實機、權限或外部素材的項目只放
[WAIT_USER.md](WAIT_USER.md)。

**寫入時機**：① **開始**多步驟工作前就先寫一行 open（不是做完才寫）；② 每次 commit 後更新或刪除該行；
③ 條目格式 `- [工作流] 一句 open 狀態 → 下一步 / 連結`，完成即刪——歷史交給 git log，
「為什麼這樣選」落到 [wf/workflows/decisions.md](wf/workflows/decisions.md)。
某工作流長出自己的 `session-log.md` 時，在本檔加一列導流（見 [STRUCTURE](wf/STRUCTURE.md)）。

## 現役工作

- [aos] 第 1、2 期已落地（[aos.md](wf/workflows/aos.md)）；第 3～5 期未做 → 下一場由 skyrim-agent 排
- [aos] 舊記憶夾收尾 3 件（補約 3 條 lessons、MEMORY.md 改指回、刪原檔另問）→ 第 5 期
- [aos] `tmp/aos-skyrim-agent/` 測試暫存夾 → 等使用者說要不要清
- [bodyslide] 女體、男體、OBody n5 已部署，實機待驗 → [11-22 STATE](agentctl/handoffs/home-2026-11-22/STATE.md)
- [racemenu] Muiri 臉層停用中；`face_loop` 校準與示範未完（要開遊戲）；R1、R2、R7 未做 → 同上
- [profiles] 11-22 已本地 commit 未 push，等使用者一句話 → 同上

子專案續行見 [agentctl SESSION](agentctl/SESSION-LOG.md)。

## 暫凍（非現役）

使用者2026-11-05暫時凍結 PoE 星盤，等重新指示，不自動研究／設計／實作／部署／驗收。範圍含本輪星盤 IndependentSkills 1.2.x／NativeBridge 候選、24型設計（刻印／浪潮鬥士／守衛者等）及直接服務星盤的全量戰鬥效果研究；不視為取消或完成，不刪資料、不撤既有部署。未確認獨立用途的研究分支保守暫停；一般戰鬥 mod、共用工具及非PoE工作不因此凍結。 續接證據見 [NEXT](agentctl/handoffs/NEXT-SESSION.md)。
