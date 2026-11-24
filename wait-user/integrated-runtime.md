# 整包 UI／中文／任務驗收

## Auri＋現役 VIGILANT 有限解凍整合

內容見 [new-game-followers.md](integrated-runtime/new-game-followers.md)。

## DMK 中文層 smoke 以標準 baseline save 重跑

內容見 [dmk-gameplay.md](integrated-runtime/dmk-gameplay.md)。

## 四個首次生效中文層 → 現在只剩兩個（2026-09-05 核對）

內容見 [localization-checks.md](integrated-runtime/localization-checks.md)。

## 2026-08-20 任務內容批

內容見 [quests-npc-text.md](integrated-runtime/quests-npc-text.md)。

## 四 mod 與 Ambriel 外觀的自然遊玩驗證（2026-11-01 立）

自然遊玩時抽查 Eilgird／Lenora 隨從對話、Paths 實際技能樹，以及原存檔 Ambriel 外觀快取與自然劇情人形／龍變身往返。Paths 技能效果、解鎖條件及自動施展說明請確認換行、右邊不超框、下方不重疊；r4 已部署但尚未實機驗收，見 Paths 斷詞部署紀錄（已刪：`agentctl/handoffs/home-2026-11-01/paths-wrap/REPORT.md`）。兩個新生人形膚色、Paths 空面板中文、Estates 中文 UI 與反射 UI 已驗收；這些不代表上述自然遊玩項已通過。見 部署驗證（已刪：`agentctl/handoffs/home-2026-11-01/wanted/INSTALL-QA.md`）。

## 冬堡學院：Midden01 的 Summerset Isle Assault 通道（2026-11-23）

只有靜態證據：Summerset Isle Assault 在 Midden01 停用原版牆開的通道，被組合補丁蓋回 JK's 版本、JK's 在同座標有自己的牆，等於封回去；它的 navmesh 改動也被組合補丁蓋掉。要實機看傳送門走不走得到（玩家與隨從，有沒有穿牆或擋路）。真的被擋才談修（要動 profile、要使用者同意）。見 [REPORT](../agentctl/handoffs/home-2026-11-23/winterhold-conflicts/REPORT.md)。

## 冬堡學院：Midden 調查書是不是紫色（2026-11-23）

只有靜態證據：Finding Velehk Sain 把 `dunMiddenInvestigationBook` 的模型換成 `BCSSEJournal.nif`，它要的 `JournalAdmonition.dds` 與 `_n.dds` 全機找不到。要實機看 Midden 那本書的貼圖。見 [REPORT](../agentctl/handoffs/home-2026-11-23/winterhold-conflicts/REPORT.md)。

## 冬堡學院：外景冰柱、冰板的貼圖（2026-11-23）

只有靜態證據：Icy Mesh Remaster 要的 `textures/landscape/ENV_I.dds`、`ENV_G.dds` 全機找不到，影響不只學院。要實機看學院外景冰柱、冰板。見 [REPORT](../agentctl/handoffs/home-2026-11-23/winterhold-conflicts/REPORT.md)。

## 冬堡學院：門的造型與貼圖（2026-11-24）

winterhold-apply 已套用（profiles `c714424`，未 push）：停用 JK's College 的 Relighting 補丁，Praedy's 的三支門 nif（ldoor01、ldoor02、animdoor01）改名 `.mohidden`，改由 OCW 的 BSA 供門模型，貼圖仍用 Praedy's 木紋。要實機看學院主門與塔門：應是 OCW 造型（有鋼條）配 Praedy's 木紋，看有沒有紫色或破面；順手看學院內光照有沒有異常。見 [REPORT](../agentctl/handoffs/home-2026-11-24/winterhold-apply/REPORT.md)。
