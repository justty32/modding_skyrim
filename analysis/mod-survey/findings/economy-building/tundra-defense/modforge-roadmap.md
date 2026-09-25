# tundra-defense — modforge-roadmap

← [調查入口](../tundra-defense.md)

## 6. ModForge relevance — idea #22 mapping（逐功能 + 每個「做不到」都 grep `src/ModForge.Core/` 驗證）

逐維對照。**已驗 = 在 `src/ModForge.Core/` 找到對應生成碼**；**GAP = 驗證後確認缺**。

6. ModForge relevance — idea #22 mapping（逐功能 + 每個「做不到」都 grep `src/ModForge.Core/` 驗證）的逐列資料。

已抽到 [tundra-defense-modforge-mapping.json](tundra-defense-modforge-mapping.json)（11 列）

Tundra 機制：原表「Tundra 機制」欄。

ModForge 能否生成：原表「ModForge 能否生成」欄。

證據（grep `src/ModForge.Core/`）：原表「證據（grep `src/ModForge.Core/`）」欄。

統計：11 列記錄；3 欄。

**結論（#22 verdict）**：Tundra 的**所有靜態 record（ALCH/MGEF/ACTI/FACT/LVLN/NPC/PACK/KYWD/BOOK/CONT/SHOU/WOOP/SPEL/MESG-殼）ModForge 今天都能生**，而且 `scriptAttach`（反射式、已驗）能把 Tundra 那 56 支 controller `.pex` 掛回對應 record。**唯二真正的 GAP**：① **MESG 無按鈕/分支選單**（`MessageSpec` 確認缺欄）——Tundra 的 UI 撐在這上面；② **整套執行期玩法（定位模式、raid OnUpdate spawn、募兵程序、跨存檔 counter 持久化）是 irreducibly bespoke Papyrus**——ModForge 永遠不會「生成」這段行為碼，只能「ship 一支寫好的 controller `.pex` 並 attach」。換言之：**ModForge 能完整生出 Tundra 的「骨架與零件」，但「靈魂」（那支 controller）必須是手寫並隨附的 `.pex`**——這跟 `settlements:` 純靜態 staffing 的本質差別就在「有沒有一支常駐 controller」。

## 7. Roadmap implications — `settlements:` Phase-2「build / manage / defend」要什麼

現 [`settlements:`](../../systems-population/settlement-npc-expansions.md) macro（`Spec.Settlement.cs`：residents + DailyRoutine + Vendor）只覆蓋「**住滿**」，**完全沒有 build/manage/defend**。Tundra 給出 Phase-2 要新增的原語清單，逐項標 **generable-today / needs-controller**：

<!-- wf-nav -->
1. **`buildables:`（建材選單系統）** — 每個 entry `{ id, name, model, cost, kind: object|multi|boundary|trap, actorOnPlace? }` macro-expand 成 **Ingestible(plan) + "Construct X" MGEF(script-archetype) + Activator(本體)** 三件套並互掛。
   - **靜態三件套：generable-today**（ALCH+MGEF+ACTI 都已驗能生）。
   - **放置定位行為（喝瓶→follow→rotate→confirm）：needs-controller**——必須隨附一支等同 `aaaFortObjectSpawnerScript`+`aaaFortMainQuestScript` 的 `.pex`，用 `scriptAttach`（已驗）掛上。建議 ModForge **內建一支泛用 placement-controller `.pex`**（如同 dispatcher/MCM-Helper 那樣的隨附 runtime），spec 只填 property。

2. **`defense:` / `siege:`（波次守城）** — `{ waves: [{ type, enemyBases: [...], min, max, boss? }], frequency, difficultyLevels, spawnMarkers }`。
   - **enemy NPC base + LeveledNpc + Raider faction + boundary/spawn marker：generable-today**。
   - **波次觸發 + OnUpdate spawn 計時 + AddToFaction 成敵 + 清場計數：needs-controller**（等同 `aaaFortPlayerQuestScript` raid 段）。可考慮**用 Story Manager + dynamic-spawn quest 半生成**（ModForge 已有 SM + `quest.spawn`，見 memory `dynamic-spawn-debugging`）取代部分 controller，但難度調節/波次節奏仍偏向 controller。

3. **`recruitment:`（募兵/雇工）** — `{ recruits: [{ archetype, cost, fromActivator, faction, teammate, cap }] }`。
   - **募兵程序（付 Gold → PlaceActorAtMe → AddToFaction → SetPlayerTeammate → cap）：needs-controller**（Tundra 全程序化，無對白）。
   - **替代路徑：generable-today** — 若改用 ModForge 既有 **dialogue INFO + SetFactionRank + alias fill**（hire-follower 路，見 memory `hirefollower-paid-gold-bug`）可不靠 controller，但體驗與 Tundra 的「選單即募」不同。

4. **`manageMenu:`（管理 UI）** — Tundra 的命脈。**MESG 按鈕/分支選單是當前最明確的 GAP**：`MessageSpec` 需擴充 `buttons: [...]` + 生成器寫 MESG 的 menu-button 子記錄（`Generator.Build.Messages.cs` 須增能）。**這項是 generable-today 的前置改動**（純 record 擴充，非 controller）——值得先做，因為任何 build/manage mod 都要它。

5. **`territory:`（領地界定）** — boundary markers + travel marker + faction 安全。**generable-today**（marker REFR + faction 已有）；範圍判定（最小距離把關）若要即時則 needs-controller。

**Phase-2 的核心架構抉擇**：Tundra 證明「build/manage/defend」**無法純靠靜態 record macro-expand**——它需要一支**常駐 controller `.pex`**。ModForge 已有「隨附 runtime `.pex` + `scriptAttach` 掛接」的成熟先例（MCM-Helper 的 `ModForgeMCM`、dispatcher psc、storageWrites 的 PapyrusUtil 接法）。**建議**：`settlements:` Phase-2 = 「**內建 1–2 支泛用 controller `.pex`（placement-controller + raid-controller）+ spec 只填 buildables/defense/recruitment 的 property，由生成器把靜態三件套生齊並 `scriptAttach` 掛上 controller**」。最小垂直切片：1 個 `buildable`（喝瓶→定位→落地一面牆）+ 1 個 `recruit`（付錢生一名守衛入隊）+ 1 波 `defense`（按鍵刷 3 個 bandit 在 boundary marker），驗「能蓋、能募、能守」三件事，再擴。先決的純-record 改動：**MESG menu-button 支援**（第 4 項）。

## Verdict

**可借鏡（最高，對 #22 核心）**。Tundra Defense 是 idea #22「build/manage/defend」唯一的完整既有藍圖。機制全部 grounded：建材 = Ingestible(potion) → script-MGEF → spawner `PlaceAtMe` → `aaaFortMainQuestScript` 定位狀態機；募兵 = 程序化 PlaceActorAtMe+faction+teammate；守城 = `aaaFortPlayerQuestScript` 的 Message-menu + OnUpdate spawn `Raider*` base at boundary markers；UI = 87 MESG（無 MCM）；狀態 = quest-script property（0 GLOB）。**ModForge 能生 Tundra 的全部靜態零件，並能 `scriptAttach`（已驗）掛回其 controller `.pex`；兩個真 GAP = MESG 按鈕選單（record 擴充可補）＋整套執行期玩法（irreducibly bespoke Papyrus controller，須隨附 `.pex`）。** 與 Sofia patch 無交集。下載已就緒、可隨時做最小切片實驗。
