# tundra-defense — recruitment-defense

← [調查入口](../tundra-defense.md)

## 4. Recruitment + defense mechanism（募兵 + 守城）

### 4.1 募兵 / 雇工 = 「付 Gold → `PlaceActorAtMe` → `AddToFaction` → `SetPlayerTeammate`」（無對白樹、無 alias fill）

統一配方（pex-strings，散見多支 script）：互動建物（barracks/house/mine/market…）OnActivate → MESG 選單 → `Player.RemoveItem(Gold, cost)` → `PlaceActorAtMe(ActorBase)` → `AddToFaction(aaaFortFollowPlayerFaction)` + `SetPlayerTeammate(true)` + `EvaluatePackage`，並 `++Count`（cap 檢查）：

4.1 募兵 / 雇工 = 「付 Gold → `PlaceActorAtMe` → `AddToFaction` → `SetPlayerTeammate`」（無對白樹、無 alias fill）的逐列資料。

已抽到 [tundra-defense-recruitment.json](tundra-defense-recruitment.json)（7 列）

角色：原表「角色」欄。

script：原表「script」欄。

來源建物 / 機制：原表「來源建物 / 機制」欄。

統計：7 列記錄；3 欄。

→ **募兵全程程序化（PlaceActorAtMe + faction + teammate），零 dialogue INFO、零 quest alias**。守衛/居民死了就 `--Count` 並 `Delete`。

### 4.2 守城 / 波次 = `aaaFortPlayerQuestScript`（玩家自觸發或隨機；`PlaceActorAtMe` at boundary markers）

這支同時是 **UI + raid 引擎**（pex-strings 完整）。Raid 流程：

<!-- wf-nav -->
1. 玩家按熱鍵開 `PlayerMenu "Outpost Menu"` → `RaidMenu`/`RaidMenuB`/`RaidMenuC "Manage Raids"` 選 raid 類型 + 難度（`RaidDifficultyMenu`）。
2. 每種 raid 對應一組 `Raider*` **ActorBase 陣列**（property `ActorBase[]`）：`BanditRaid`/`DraugrRaid`/`DragonRaid`/`NatureRaid`/`GiantRaid`/`NecroRaid`/`VampireRaid`/`WerewolfRaid`/`FalmerRaid`/`RandomRaid`，各含分工 base：`RaiderBanditMelee`/`Ranged`/`Wizard`/`Boss`、`RaiderDraugrMeleeM/F`/`Ranged`/`Wizard`/`Boss`、`RaiderNatureBear`/`Wolf`/`Sabre`/`Troll`/`Spider`/`ChaurusReaper`/`IceWraith`、`RaiderGiantA/B`/`Leader`/`Mammoth`、`RaiderDragon` 等。
3. 生怪：`OnUpdate` 迴圈 `RandomInt(min,max)` 決定數量（受 `difficulty`/`raidHandicap`/`GuardCount` 調整）→ **`PlaceActorAtMe(Raider base)` at `BoundaryMarkerA/B/C/D`**（在玩家先前擺的邊界 marker 處刷怪）→ `AddToFaction(aaaFortRaiderFaction)`（與 FortFaction/守衛敵對）。`CurrentRaiders` 計數，清完 → `EndRaid`/`RaidEnded` + 播 `RaidSound`（`aaaFortRaidSoundEffect` / `sound/fx/.../raid.xwm`）。
4. **隨機襲擊**：`RandomRaidEnabled` + `RandomFrequency`（`RaidFrequencyMenu`：Low/Medium/High Dialog）→ 由 `aaaFortRandomOccurancesQuest`（`aaaFortRandomQuestScript`）按頻率自動觸發 `BanditRaid` 等。`firstRaid` 旗標 + tutorial（objective 70 "Start a Raid"）引導第一波。

→ **守城 = 「Message-menu 選 raid → OnUpdate 計時器 → PlaceActorAtMe 一批 Raider base at boundary markers → AddToFaction 成敵 → 數清歸零」**。**無 Story Manager、無 PlaceAtMe(LeveledNpc) at xmarker quest**——是 quest-script 直接驅動的 spawner（與 [immersive-wenches](../../systems-population/immersive-wenches.md) 的 SM/LL spawn 不同路）。

### 4.3 領地 / 安全 = boundary markers + faction 敵我，無 cell-ownership/XOWN

「我的據點範圍」靠 4 個玩家擺的 `BoundaryMarker*`（`aaaFortBoundarySpawner`，`MoveTo`+`Enable`+`collisionRef`，最小距離由 `aaaFortTooFarBoundary`/`aaaFortTooCloseBoundary` MESG 把關）+ travel marker。安全模型純 **faction 敵我**（FortFaction vs RaiderFaction），守衛是 player teammate。**沒看到 XOWN cell-ownership**（建物多在 vanilla worldspace，不是 owned cell）。

## 5. MCM / config

**沒有 MCM**（無 SkyUI / MCM-Helper / `.json` / `.ini`）。**所有設定走 87 個 MESG 選單**，由 `aaaFortPlayerQuestScript` 用 `Message.Show()` 驅動：`PlayerMenu "Outpost Menu"`（根）→ `Settings/SettingsB/SettingsC/SettingsD` 子選單、`RaidFrequencyMenu`（Low/Med/High）、`RaidDifficultyMenu`、`KillStationaryGuards`(`StationaryGuardPurge`)、`RebindMenu`（重綁熱鍵，SKSE）、各建物的 `ManageDialog`/`BreakdownDialog`/`MoveDialog`。設定值存 **quest script property**（`RaidFrequency`/`raidHandicap`/`DebugMode`/`AdvancedMode`/`hideIdleMarkers`/`DistanceSpeed`/`RotationSpeed`…），**非 GLOB**。

