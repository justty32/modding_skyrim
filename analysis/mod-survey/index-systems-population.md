# 系統／機制型 · 戰役、巡邏與聚落人口

← [mod-survey](README.md)｜[survey index](index.md)

逐 mod 機制拆解 + 對 ModForge 的「可生成 / 需新支援 / 純參考」標記。共通缺口已彙整進 [roadmap](../../projects/ModForge/workflows/roadmap/README.md)「mod-survey 浮現的 record/生成缺口」。

<!-- wf-nav -->

| Mod | Finding | 機制重點 | ModForge 缺口 |
| --- | --- | --- | --- |
| Civil War Overhaul Redux | [findings/civil-war-overhaul-redux.md](findings/civil-war-overhaul-redux.md) | `Civil War Overhaul.esp` | 高（M&B / 戰略戰役參考） | campaign GLOB state machine；fixed attacker/defender aliases；ticket-based reinforcement controller；fort/city siege phase triggers |
| WARZONES - Civil Unrest | [findings/warzones-civil-unrest.md](findings/warzones-civil-unrest.md) | `WARZONES - SSE - Civil Unrest.esp` | 高（M&B ambient warzone） | marker/activator-driven encounter sites；spawnometer activators；global/MCM toggles；leveled spawn pools |
| Populated Skyrim Civil War | [findings/populated-skyrim-civil-war.md](findings/populated-skyrim-civil-war.md) | `Populated Skyrim Civil War.esp` | 中（world population） | 430 NPC bases + placed civil-war actors；no quest/dialogue controller；static battlefield density baseline |
| OBIS SE Patrols Addon | [findings/obis-patrols-addon.md](findings/obis-patrols-addon.md) | `OBIS SE Patrols Addon.esp` | 高（route spawn pattern） | 100-alias patrol quest；CreateReferenceToObject from leveled lists；ALPS package override per route；book/MCM globals |
| Populated Skyrim family (Steelfeathers: Cities/Lands/Dungeons/Hell) | [findings/populated-skyrim-family.md](findings/populated-skyrim-family.md) | `Populated Cities Towns Villages Legendary.esp` / `Populated Lands Roads Paths.esp` / `Populated Dungns Caves Ruins Legendary.esp` / `Populated Skyrim Legendary.esp`(Hell) | 無（人口 pattern 極高） | 純靜態置放人口（base+package+cell override，無 controller），#22 聚落量產 spec section 的活藍本——機制全已可生成，缺 macro-expansion 便利層 |
| Immersive Citizens - AI Overhaul | [findings/immersive-citizens-ai-overhaul.md](findings/immersive-citizens-ai-overhaul.md) | `Immersive Citizens - AI Overhaul.esp` | 低（系統 pattern 極高） | alias-ALPS 分派 quest 替既有 NPC 掛整疊 bespoke 日程包（不碰 NPC 記錄）+ Flee-template 防禦/逃跑 AI；#22 直接借鏡日程配方、需補 `flee` PACK 模板 |
| Immersive Wenches SE | [findings/immersive-wenches.md](findings/immersive-wenches.md) | `Immersive Wenches.esp` | 中 | cell-override XMarker + LeveledNpc 腳本生怪 + per-inn 時段 package + SM 觸發的環境 scene；#22 活人口最完整藍圖，~80% 已 landed，缺「人口填充 generator」便利層 |
| Populated Skyrim prison cells | [findings/populated-prison-cells.md](findings/populated-prison-cells.md) | `Populated Skyrim Prisons Cells.esp` | 無 | 家族同骨架，但置放走 carrier→LeveledNpc 兩層抽卡（牢房隨機囚犯）；單一 sandbox package、敵視玩家 faction；無新 gap，收束 Populated 全家桶 |
| Cutting Room Floor | [findings/cutting-room-floor.md](findings/cutting-room-floor.md) | `Cutting Room Floor.esp` | 中 | vanilla 聚落人口復原：override 幾個 vanilla cell + 新 interior + 手擺具名住民（faction 三件套 + per-NPC 日程）+ 無文字 ChangeLocation 狀態機做非破壞整合；#22「固定住民聚落」最乾淨骨架，缺 settlement generator 便利層 |
| Settlement NPC expansions (Immersive College NPCs / ICMF / ETaC Orc Strongholds) | [findings/settlement-npc-expansions.md](findings/settlement-npc-expansions.md) | `ICNs_ImmersiveCollegeNPCs.esp` / `ICMF Immersive College Mini Factions.esp` / `Immersive Orc Strongholds.esp` | 低（staffing/shop pattern 極高） | 單點聚落「住滿＋擺出店家」配方：unique base + 逐時段 package + additive cell override + **per-NPC Vendor faction（非 rank 公會，是迷你商圈）**；補 #22 聚落量產 section 的店家/服務面，機制全已 landed |
| Wench derivatives (Deadly Wenches / Buxom Yuriana) | [findings/wench-derivatives.md](findings/wench-derivatives.md) | `Deadly Wenches.esp`(依賴 IW) / `YurianaWench.esp`(standalone) | 無 / 中 | DW=override vanilla 敵人 LeveledNpc 注入野外戰鬥人口（異世界不適用，倒出輕量 `leveledListInject[]` 念頭）；Yuriana=standalone 語音隨從範本（90-cell-override 小 quest-mod，非單一隨從）|
| JK's Skyrim (set-dressing) | [findings/jks-skyrim-setdressing.md](findings/jks-skyrim-setdressing.md) | `JKs Skyrim.esp` | 無 | 18550 靜態 REFR、零任務的 mass cell-override 佈景：placement-volume 範本，cellrefs 欄位 1:1 對齊 Godot 編輯器 placements.json，天然 authoring 工具＝Godot worldspace editor |
