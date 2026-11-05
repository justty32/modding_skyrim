# 整包 UI／中文／任務驗收

## GO19 新內容要不要改用新周目正式驗收

內容見 [new-game-followers.md](integrated-runtime/new-game-followers.md)。

## Auri＋現役 VIGILANT 有限解凍整合

內容見 [new-game-followers.md](integrated-runtime/new-game-followers.md)。

## DMK 中文層 smoke 以標準 baseline save 重跑

內容見 [dmk-gameplay.md](integrated-runtime/dmk-gameplay.md)。

## Modpack-KR Batch 6 final gameplay

內容見 [dmk-gameplay.md](integrated-runtime/dmk-gameplay.md)。

## 四個首次生效中文層 → 現在只剩兩個（2026-09-05 核對）

內容見 [localization-checks.md](integrated-runtime/localization-checks.md)。

## RDO 中文層（62500／76474 已落地，待進遊戲抽查）

內容見 [localization-checks.md](integrated-runtime/localization-checks.md)。

## VIGILANT 1.8.2 正體中文

內容見 [quests-npc-text.md](integrated-runtime/quests-npc-text.md)。

## 2026-08-20 任務內容批

內容見 [quests-npc-text.md](integrated-runtime/quests-npc-text.md)。

## JhNPCBeautyDev 蓋掉 NPC 中文名（2026-08-28 發現，待裁示）

內容見 [quests-npc-text.md](integrated-runtime/quests-npc-text.md)。

## cow 中文層人眼抽查（2026-10-26 立）

cow 學院中文層（profiles `93261f4`）已部署、煙霧通過，剩人眼：在學院裡看有沒有方框字、截斷。

1. 成就大厅／智慧大厅／面容之殿門口的「指南」牌：樓層分「楼上／一楼／地下层」，房間名照 Alias 帶出。
2. 首席法師房間水晶球選單：六鈕依序「植物园／议会厅／温泉／办公室／档案室／无」；選「档案室」應真的變成檔案室布置。
3. 《泰姆瑞尔智识：修订版》翻到第 7 頁以後（原本是英文）。

內容取自 [`agentctl/handoffs/home-2026-10-26/cowzh/REPORT.md`](../agentctl/handoffs/home-2026-10-26/cowzh/REPORT.md)「給使用者的人眼抽查」。

## 四 mod 與 Ambriel 外觀的自然遊玩驗證（2026-11-01 立）

自然遊玩時抽查 Eilgird／Lenora 隨從對話、Paths 實際技能樹，以及原存檔 Ambriel 外觀快取與自然劇情人形／龍變身往返。Paths 技能效果、解鎖條件及自動施展說明請確認換行、右邊不超框、下方不重疊；r4 已部署但尚未實機驗收，見 [Paths 斷詞部署紀錄](../agentctl/handoffs/home-2026-11-01/paths-wrap/REPORT.md)。兩個新生人形膚色、Paths 空面板中文、Estates 中文 UI 與反射 UI 已驗收；這些不代表上述自然遊玩項已通過。見 [部署驗證](../agentctl/handoffs/home-2026-11-01/wanted/INSTALL-QA.md)。

## 青蛙相關 crash 自然戰鬥復發觀察（2026-11-01 立）

自然遊玩遭遇青蛙戰鬥時，留意是否再發生 crash。青蛙模型 Trial 層已部署，室內短窗模型載入通過，但尚未證明戰鬥中的 crash 已解決；見 [部署紀錄](../agentctl/handoffs/home-2026-11-01/varinia-native-crash/DEPLOY.md)。
