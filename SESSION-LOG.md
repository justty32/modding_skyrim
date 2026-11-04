# SESSION-LOG — 進度日誌 hub

只放還沒完成、且 agent 仍能主動推進的活狀態。已完成的實作與調查歷史由對應 plan、
子專案文件與 git history 承接；需要使用者、實機、權限或外部素材的項目只放
[WAIT_USER.md](WAIT_USER.md)。

**寫入時機**：① **開始**多步驟工作前就先寫一行 open（不是做完才寫）；② 每次 commit 後更新或刪除該行；
③ 條目格式 `- [工作流] 一句 open 狀態 → 下一步 / 連結`，完成即刪——歷史交給 git log，
「為什麼這樣選」落到 [wf/workflows/decisions.md](wf/workflows/decisions.md)。
某工作流長出自己的 `session-log.md` 時，在本檔加一列導流（見 [STRUCTURE](wf/STRUCTURE.md)）。

## 現役工作

- [feature-dev] native-bridge隔離候選：先買61308高階附印→原生法術命中掛狀態→進階AND前置；公司source-only候選已封存／push；normal未開、PE未build、未部署，16:50前停止長行程 → [樣板與當前範圍](wf/workflows/plans/poe-skyrim-mapping/combat-combinators/inscription-sample/README.md)。

- [investigation] 全量提取已安裝天賦來源的戰鬥相關進階／高級效果單位，不設件數上限；涵蓋 nonwinning、disabled、hidden 與依賴，按 PERK entry 記覆蓋及範圍理由；新增啟用／對話／互動選項暫緩，非戰鬥效果排除 → 收工停線、尚未完成；公司未帶昨晚17GB完整checkpoint；今日PoE輸入已獨立封存Git且不等於全集資料恢復，續行與核驗狀態見 [private 交接](agentctl/handoffs/NEXT-SESSION.md)。恢復後完成全集調查與可搜尋過目頁，再請使用者確認新數值。

10-24 登記的兩件 `analysis/` 工作（skyrim_engine API 稽核、
commonlibsee-ng README 漏索引）已於 2026-10-26 做完，見
[apiaudit REPORT](agentctl/handoffs/home-2026-10-26/apiaudit/REPORT.md)。

母 repo 只管本身的整理與開發工作。Skyrim 工作線從
[下次開場入口](agentctl/handoffs/NEXT-SESSION.md)接續；需要使用者親自做的事以
[WAIT_USER.md](WAIT_USER.md)為準。

- [planning] 近衛common＋G1「浪潮鬥士」19真點候選已過目並保存；命名理由「一浪接一浪」。4common A/2H與6sub A/2H分計、前置AND圖連通，runtime=0、不進術師registry。見[人頁](wf/user/2026-11-04-guard-double-beat-sample.md)，本場仍16:25收尾／16:50保存。

- [planning] 重裝D1「守衛者」19真點可攜護援候選已落，common4A2H/sub6A2H，runtime=0；固定圈草案非current，七原start為免費錨點、未實跑新rule購點。見[人頁](wf/user/2026-11-04-heavy-warden-sample.md)；16:10已停加設計，僅保存/交接。

## Durable 狀態入口

- DSP／houseCARL 已完成的離線修復、三條隔離分支與續接位置：
  [2026-10-21 離線成果與收尾](wf/user/2026-10-21-offline-fixes.md)
- 四條線的入口：各線 README；Skyrim 工作線交接主線在 `agentctl/SESSION-LOG.md`
- houseCARL fork 維護決策：
  [fork-maintenance-decision.md](analysis/houseCARL/answers/fork-maintenance-decision.md)
- houseCARL Linux/MO2 技術方案：
  [linux-manjaro-mo2-runbook.md](analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md)
- 需使用者或外部環境才能完成的工作：[WAIT_USER.md](WAIT_USER.md)
