# populated-skyrim-family — modforge-verdict

← [調查入口](../populated-skyrim-family.md)

## ModForge meaning & gap

**已能生成（逐欄對得上，幾乎全中）**：
- NPC base（race/class/voice/outfit/combatStyle/factions/aiData）— landed `npcs.md`。
- 自製 Faction + 跨 faction 敵我 — landed。
- **PACK 10 模板**：sandbox / sleep / **travel** / usemagic / **patrol** / follow / escort / sittarget / activate / eat — 完整覆蓋本系列用到的 sandbox/eat/work/travel/wander/follow-boss/pack。**逐時段排程**（`Schedule` hour/minute/duration + 多 LocationTarget radius）與 alias-target radiant package 都已落地 — landed `npcs.md`。
- **LeveledNpc**（Lands/Hell 的難度撐法）— landed。
- 直接 ACHR 置放 + **PlacementSpec 六欄**（Scale / InitiallyDisabled / **EnableParent** / Lock / Ownership / **Count**）+ vanilla **cell override** + map marker — landed `world.md`。EnableParent/InitiallyDisabled 正好能補本系列缺的「按狀態開關」。
- **npcPatches[]** override vanilla NPC 的 packages（AI Overhaul 式）— landed。

→ **結論：本系列每一條低階機制 ModForge 都已具備。缺的不是能力，是「量產便利層」。**

**GAP（單一最重要、直指 #22）= 一個 macro-expansion 的高階 spec section，把「填滿這個聚落 / 這條路線」一句話展開成上述幾百筆低階記錄。**

`skillTrees:`（idea #20 Phase 3，landed `world.md`）已證明這條路在 ModForge 完全可行：在 `Build()` pass-0 `Expand*` 把高階指令展開成既有低階記錄、重用全部既有 pass、新建記錄碼極少。比照它做兩個對應 #22 的 section：

- `settlementPopulation:`（對 Cities）：給聚落 + 一組 archetype（乞丐/勞工/商人/旅店常客…）+ count + 一份「日程模板」（上工時段/用餐旅店/作息），macro-expand 成 unique base × N + 逐時段 sandbox/eat/work package × N + ACHR 置入指定 cell。
- `wildernessPopulation:` / `roadTravelers:`（對 Lands/Roads — #22 的「有人走的荒野/道路」）：給一份 archetype 字典（wandering merchant / pilgrim / adventurer+horse / refugee / mercenary）+ 路線/區域 + LeveledNpc 撐難度 + travel/wander package，macro-expand 成 base/leveled + 置放 + 路線 package。內建 `enableParent`/`gate GLOB` 旋鈕（補本系列「靜態無狀態」的弱點，也順手提供 MCM 式密度開關）。

這正是 #22 roadmap 列的「**聚落量產 spec section**」缺口——本系列就是該 section 要生出來的東西的活樣本：archetype 清單、排程 sandbox 結構、travel 路線 package、leveled 撐場、cell override 置放，全部已被本調查解析成可直接照抄的 pattern。Dungeons 變體額外示範敵性 `IhatePlayer`/pack-on-boss-death 的荒野怪物填充（#22「探索」面）。

風險（沿用 Civil War finding）：① plugin 體積/置放數爆漲快，量產層要給 count 上限與 navmesh-safe 置放紀律；② 大量 base 要 FaceGen 提醒；③ 靜態密度 ≠ 戰略狀態，別誤當模擬系統。

## Verdict

**可借鏡（高）**。機制 100% 已可生成，缺一個量產便利層；是 idea #22「聚落量產 spec section」最直接的設計藍本與 archetype 字典來源。家族其他成員見 [populated-skyrim-civil-war.md](../populated-skyrim-civil-war.md)（戰士版）與 [immersive-patrols.md](../../content/immersive-patrols.md)（精選巡邏版）。
