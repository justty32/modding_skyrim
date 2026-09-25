# tundra-defense — building

← [調查入口](../tundra-defense.md)

## 3. Build system mechanism（核心——放置 + 持久化）

**放置一個建物 = 喝一瓶「Plans: X」Ingestible → 觸發其唯一 MagicEffect "Construct X"（script archetype）→ spawner script `PlaceAtMe` 出對應 Activator → 進入「定位模式」由 `aaaFortMainQuestScript` 即時跟著玩家視線移動，按確認鍵落地。**

### 3.1 建材 = Ingestible（potion），不是 MISC、不是 crafting station

`dump` 證實：每個建物都是一個 **Ingestible**（ALCH）`aaaFort…Plan`，Name 形如 `"Plans: Spike Wall"` / `"Plans: Water Well"` / `"Plans: Barracks"`。tutorial quest（`questdiag 0x002853`）的 log 字面坐實玩家流程：

> "open your inventory under the **FOOD** category and use 'Plans - Water Well'"

→ 「喝」這瓶 potion 觸發它掛的 script-archetype MagicEffect。`dump` 列出全部 113 個 MagicEffect 幾乎都是 `aaaFort…Effect "Construct X"`，archetype=**Script**，各掛一個 spawner script（見下）。計畫書本身存在 `aaaFortPlansContainer "Plans Chest"`（玩家從市集/箱子取得）。

### 3.2 spawner script 家族（掛在 MagicEffect 上，`OnEffectStart` 出物）

`dump` 顯示每個 "Construct X" MGEF 的 `script:` 欄就是下面其一（property 數隨建物異）：

| spawner script (pex) | 出什麼 | 關鍵 property/call (pex-strings) |
|------|------|------|
| `aaaFortObjectSpawnerScript` | 單一 Activator（牆/門/forge/barracks…）| `SpawnRef`(activator) / `SpawnContainerRef` / `SpawnFurnitureRef` / `SpawnDoorRef` / `ActorOnPlace`(actorbase) / `rotateOnSpawn` / `distanceOnSpawn` / `isArcane` / `isMedic`；call **`PlaceAtMe` → `StartPositioning`** |
| `aaaFortMultiObjectSpawner` | 多選一（`activator[]` + `RandomInt`）→ farmhouse/townhouse/naturehouse 隨機外觀 | `SpawnRef`(activator[]) / `Spawn` / `RandomInt`；同樣 `PlaceAtMe`→`StartPositioning` |
| `aaaFortBoundarySpawner` | 邊界/市集/巡邏 marker（`MoveTo`+`Enable` 而非 PlaceAtMe）| `IsMarket` / `setMarket` / `collisionRef` / `DebugMode`；call **`MoveTo`+`Enable`→`StartPositioning`** |
| `aaaFortTrapSpawner` | 陷阱（bear trap）——**直接落在腳下，不進定位模式** | call `PlaceAtMe` → Notification "A trap has been placed at your feet." |

→ 共同骨架：`OnEffectStart` → `Game.GetPlayer()` → `PlaceAtMe(SpawnRef)` 生出 disabled/holding 的 ref → 把該 ref 交給 `aaaFortMainQuestScript`（property `MainQuest`）的定位狀態機。Notification "You are already in object placement mode!" 證明同時只能擺一個（`instantReuse` 旗標控制連續擺放）。

### 3.3 定位模式 = `aaaFortMainQuestScript`（即時 follow + 旋轉/距離 + 確認/取消）

這支是放置控制器（pex-strings 完整）：state 機 `MODE_DISTANCE`/`MODE_ROTATE_X/Y/Z`/`MODE_RESET`/`AXIS_X/Y/Z`，function `StartPositioning` / `UpdateObjectPosition`(`OnUpdate` 每 tick 用 `sin/cos` 把 ref `TranslateTo`/`MoveTo` 到玩家前方 `placeDistance`) / `ChangeRotationAxis` / `ResetObjectPosition` / `ConfirmPlacement` / `CancelPlacement`。輸入靠：

- 4 個自製 **Spell**（`dump`）：`aaaFortInputConfirmSpell "[Construction] Confirm"`（type=**Voice**，配 Shout `aaaFortInputConfirmShout "Confirm Construction"` / Word "Go"）、`…CancelSpell`（Voice）、`…PlusSpell`/`…MinusSpell`（Concentration）——定位時這些 spell 被加到玩家手上，喊 Shout 或施法即送出確認/取消/加減。
- `aaaFortSpellControls`（掛 Plus/Minus effect）OnEffectStart 把 `inputPlus`/`inputMinus` 旗標推給 `aaaFortMainQuestScript`（property `placementManager`）；無建造中時 Notification "You are not building anything right now!"。
- `aaaFortKeyRebinderScript` + `aaaFortPlayerQuestScript.BindKey`/`iGetKeyPressed`：SKSE DXScanCode 重綁主選單熱鍵（預設 `'` apostrophe，見 tutorial log）。

確認後 `ConfirmPlacement` → `Enable` 該 ref、`AddToFaction(FortFaction)`、若 `ActorOnPlace` 非空則 `PlaceActorAtMe`（建物附帶住戶，如 barracks 附守衛）。

### 3.4 持久化跨存檔 = **Enable 後的具名 REFR 留在世界 + quest script counter，不是 token 容器**

放下的建物就是一個被 `Enable` 的**真實 REFR**，永久存在玩家所在 cell（多在 Tamriel/玩家自選地點，非預定 cell）。`aaaFortMainQuestScript` 持有所有計數 property（`CitizenCount`/`GuardCount`/`MinerCount`/`ScavengerCount`/`hasArmory`/`hasMedic`/`hasArcane`/`hasPerch`/`hasGrandEstate`…）+ 各種 RefHolding/marker reference（`WaterWellRef`/`ScavengerCrateRef`/`MinerContainer`/`GuardEquipmentBox`…）。**搬移**走 `aaaFortMoveObjectScript`（OnActivate 潛行 → `MoveDialog` → `StartPositioning` 重新定位）；**拆除**走 `aaaFortBreakdownScript`（OnActivate 潛行 → `BreakdownDialog` 確認 → `Delete` 該 ref）。`aaaFortObjectCloningScript`（掛 ReferenceAlias，`OnHit` + keyword `aaaFortObjectCloningKey`）+ Weapon `aaaFortObjectCloner` 提供「敲一下複製已建物」。

→ **持久化＝「Enable 一個真 REFR + quest-script 上的 counter/RefHolding」**，無 JContainers、無 token-in-chest 序列化。代價：建物散落玩家當時的 cell（不集中在自家 worldspace），靠 boundary marker + travel marker（alias `aaaFortTravelMarker` ForcedRef `0x004404`）界定「我的據點」範圍。

