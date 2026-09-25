# settlement-npc-expansions — modforge-verdict

← [調查入口](../settlement-npc-expansions.md)

## ModForge meaning & gap（對 idea #22）

**已能逐欄生成（這三個 mod 的每一條低階機制都已 landed）：**

| 機制 | landed |
|------|--------|
| NPC base（race/class/voice/outfit/combatStyle/factions/aiData/autocalc+class 配對）| `npcs.md` |
| 逐時段 schedule package（`Schedule` hour/min/dur + LocationTarget radius）+ 10 PACK 模板（含 sandbox/sleep/travel/sittarget/eat）+ alias-target radiant 包 | `npcs.md` |
| ACHR 直接置放 + PlacementSpec 六欄 + **vanilla cell override（additive 帶 vanilla ref）** + XMarker | `world.md` |
| **Vendor faction**（`FactionSpec.Vendor`：Vendor flag + 營業時段 + sellBuyList FormList + MerchantContainer）— `Generator.Build.Vendor.cs` / `examples/vendor_spec.json` | landed |
| **Faction（含 rank）+ Relationship（RELA, parent/child/rank）** — `Spec.Actors.cs` | landed |
| dialogue INFO（含 alias 條件填充）/ 小 errand quest（stage+objective+alias）/ Outfit / Container（店家庫存）| `dialogue-quests.md` / `items-magic.md` |

→ **結論：「住滿並 staff 一個聚落」需要的所有原語 ModForge 全已具備**——base、日程包、cell override additive 置放、Vendor faction、Relationship、店家庫存、服務對白。連 [immersive-wenches](../immersive-wenches.md)/[populated-family](../populated-skyrim-family.md) 反覆指出的同一結論：**缺的不是能力，是「量產便利層」**。

**單一最重要 GAP（直指 #22 roadmap 的「聚落量產 spec section」）：一個把「一個聚落」一句話展開成上述幾百筆記錄的 macro-expansion section。** 本三 mod 把 populated-family 提的 `settlementPopulation:` 設想**補上了「店家結構」這一面**——所以該 section 的參數至少要含：

- `cells:`（要 override / 自家的 cell 清單）+ 每 cell 一組 `markers`（XMarker 自動配對 package LocationTarget）；
- `residents:`（一組 archetype：學生/學者/守衛/匠人/商人…）× count，每個附一份 **`dailySchedule` 模板**（睡/上工/用餐/閒晃 時段）macro-expand 成 unique base + 逐時段 package + ACHR；
- `shops:`（新增**最有價值的一格**）：給 `{ vendorType（法師/鐵匠/旅店/雜貨）, owner, hours, sellBuyList, inventory }` → 自動生 **Vendor FACT + MerchantContainer + 庫存 + 店員 base + 服務對白掛接**，把本三 mod 手刻的「per-NPC Vendor faction」變一鍵。
- 選配 `relationships:`（店員/居民間 RELA）+ `enableParent`/`gate GLOB`（補靜態置放「無狀態」弱點，順手做 MCM 式密度/開店開關）。

[`skillTrees:`](../../../../../projects/ModForge/workflows/feature-dev/landed/world.md)（idea #20 Phase 3 landed）已證明這條 macro-expansion 路在 ModForge 完全可行（`Build()` pass-0 `Expand*` 展開成既有低階記錄、重用全 pass、新碼極少）。本三 mod 就是該 section 要生出來的活樣本：**ICN = 日程 staffing 樣本，ICMF/ETaC = 店家/服務 faction 樣本，三者合起來 = 「一個有人住、有人上班、有店可逛的聚落」的完整參數字典**。

風險（沿用 family finding）：① cell override 數/置放數膨脹快，量產層要給上限與 navmesh-safe 紀律；② 大量 base 要 FaceGen 提醒（ICN/ETaC 都背 facegen）；③ Vendor faction 別忘 MerchantContainer + sellBuyList（漏一個就「店員不開店」）；④ 靜態日程 ≠ 動態狀態。

## Verdict

**可借鏡（高）**。三者 100% 機制已 landed，是 #22「聚落量產 spec section」的**「單點聚落 + 店家結構」面**最直接藍圖——補齊了 [populated-skyrim-family](../populated-skyrim-family.md)（密度面）與 [immersive-wenches](../immersive-wenches.md)（生怪面）沒涵蓋的「**服務商圈 staffing**」。內容本身（generic 訓練對白 + errand）對 #22 無敘事價值，**只借 staffing/shop 配方，不借內容**。與 Sofia patch 無交集（不改 follower topics；但 override 學院/獸人要塞 cell，與任何也改這些 cell 的 mod 需相容 patch）。最小垂直切片建議：1 個異世界聚落 cell + 3 居民（各一份 dailySchedule）+ 1 個 Vendor faction 店家，驗「有人住、會上班、可交易」三件事，再擴。
