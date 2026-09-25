# Sofia Follower v2.51 — packages-and-state

[返回入口](../sofia-follower.md)

### 3. Package（54 個）—— 隨從行為骨架

來源：`:7387`–`7499`+。所有 package 都 `template=` 引用 vanilla package 當骨架，再覆寫資料。按用途分群：

<!-- wf-nav -->
- **跟隨變體**：`SofiaFollowerPackage` `[013192]`、`JJSofiaFollowPackage` `[049FF0]`、`SofiaFollowBeside` `[065568]`、`SofiaFollowSneaking` `[06602E]`、`SofiaFollowIdleWait` `[06602F]`、`SofiaFollowWeaponDrawn` `[066AF5]`、`SofiaFollowerStealthKillPackage` `[030DF4]`（AlwaysSneak+WeaponDrawn）。
- **戰鬥風格覆寫**（一大群 `SofiaCombatOverride*`，各引用不同 CombatStyle，內外景成對）：MagicOnly / MeleeOnly / RangedOnly / DualWeildOnly / 各 Default + Exterior 版，外加 Brawl / CoveringFire / IgnoreCombat。對應 MCM 的戰鬥風格切換（見 `SofiaCombatStyles` FormList `[014C9D]`）。
- **解散 / 待命**：`SofiaDismissedSandbox` `[01169B]`、`SofiaFollowerSandbox` `[04AAB5]`、`SofiaStayAtCurrentLocation` `[038F9C]`、`JJSofiaNPCStandStill` `[03646E]`。
- **坐騎**：`SofiaHorseFollowerPackage` `[010BD0]`、`SofiaHorseSummoned` `[01318E]`、`JJSofiaMountHorse` `[0447B2]`、`JJSofiaDismountHorse` `[044D1B]`、`SofiaHorseFleeCombat` `[043CE9]`。
- **劇情 / force-greet**：`SofiaMeetingSleep` `[0285BC]`（馬廄睡覺）、`SofiaIntroForceGreet` `[02B20C]`（MustComplete，強制搭話）、婚禮系列（`SofiaGoToWeddingPackage`、`CrookedPriestGoToWedding`、`PlayerSofiaWeddingTakePosition`、`SofiaWeddingPriestFG01/02`…）、醉酒（`SofiaDrinkPackage`/`SofiaDrunkPackage`/`SofiaDrunkStop`）、`SofiaCastNudeBombPackage`。

要點：所有 package 都掛在某個 quest（`quest=` 欄）或由 alias 動態套用；戰鬥覆寫透過 FormList + GLOB index 在 runtime 切換，不重建 record。

### 4. GlobalShort/Float（57 個）—— 隨從的 runtime 設定與狀態旗標

來源：`:24`–`80`。GLOB 同時扮演「使用者設定」與「狀態旗標」兩種角色：

<!-- wf-nav -->
- **使用者設定（MCM 寫入）**：`SofiaCatchUpEnabled` / `SofiaCatchUpDistance`(Float) / `SofiaDisableComments` / `SofiaCommentFrequency`(Float) / `SofiaNudeBombEnabled` / `SofiaHorseEnabled` / `SofiaFollowBesideVar` / `SofiaCombatStyleNum` / `SofiaCombatClassIndex` / `SofiaCombatStyleIndex`。
- **狀態旗標**：`SofiaShouldTalk` / `SoifaIsTalking`(sic) / `SofiaIsGivingItem` / `SofiaHorseIsSummoned` / `SofiaIgnoreCombat` / `JJSofiaHasMetPlayer` / `JJSofiaMainQuestStage` / `JJSofiaWitnessDragon` / `SofiaWeddingStoodUp` / `SofiaPlayerLike`（好感度數值）/ `SofiaNPCresponse` / `SofiaIsUpdated`。
- **環境偵測**：`SofiaHasSKSE`、`SofiaModVersion`(Float，版本號)。
- **整排技能鏡像**：`SkillOneHanded` … `SkillSpeech` 共 18 個——把玩家全技能複製進 GLOB（推測供對白/戰鬥風格條件判斷用）。
- **玩家裝備分類**：`JJPlayerOutfitType` / `JJIsCriminalOutfit` / `JJIsHeavyArmour` / `JJIsRevealing` / `JJIsMageOutfit` / `JJIsBadOutfit` / `JJIsGoodOutfit`（配合 `JJPlayerCriminalOutfits` 等 FormList，讓 Sofia 評論玩家穿著）。
- **通用 scratch**：`JJTempBool` / `JJTempInt` / `JJTempFloat` / `JJTempIndex`（Papyrus 沒有好的暫存機制時，用 GLOB 當共享暫存變數）。

### 5. 狀態存儲觀察

**Sofia 幾乎完全靠 GLOB + quest stage + quest script property 存狀態，沒掛 JContainers**：

- 57 個 GLOB 承載所有跨存檔的旗標與設定。
- quest stage 承載線性進度（wedding 0→200、drunk 0→50、main quest stage 透過 `JJSofiaMainQuestStage` GLOB 鏡像）。
- 複雜狀態塞進 quest 上的 script property（`JJSofiaVariablesScript` 19 prop、`SofiaMCMscript` 26 prop、`SofiaFollowerScript` 12 prop）——Papyrus property 本身會進存檔。
- **沒有 per-actor 動態狀態表的需求**：Sofia 是唯一隨從，好感度只需一個 `SofiaPlayerLike` GLOB，不像「每個 NPC 各自好感度」那種會逼出 JFormDB 的場景。這正解釋了她為何不需要 JContainers。

其餘支援 record（簡述）：
<!-- wf-nav -->
- **NPC（9）**：`JJSofiaFollower` `[0012C4]`（race 013746=Nord female、class=SofiaCombatSpellsword、voice=JJSofiaVoiceType、aiData Aggressive/Foolhardy、3 perk）；配角 Voldar / Jarvis / OldMage / MasterThief / CrookedPriest（婚禮主持）/ JJSofQuestGuard / GiftStorage / JJSofiaHorse。
- **Relationship（3）**：`NataliePCRelationship` `[001828]`（parent=JJSofiaFollower child=Player rank=**Ally**，"Natalie" 疑為 Sofia 內部代號）；`SofiaHorseRelationship`、`HorsePlayerRelationShip`（馬↔Sofia/玩家 Ally）。用 RELA record 直接固定隨從對玩家友好。
- **Faction（3）**：`SofiaFollowerFaction` / `SofiaDismissedFaction` / `SofiaBrawlFaction`——隨從狀態用 faction membership 表示。
- **Spell（9）**：`SummonSofiaSpell` `[043CEB]`（玩家用的召喚找人）、`SofiaSummonHorseSpell`、`SofiaNudeBombSpell`、`JJSofiaGetTargetSpell`（取玩家目標）、`SofiaFirebolt/LightningBolt/IceSpikeLeftHand`（左手法術，供戰鬥風格用）。
- **VoiceType（4）**：`JJSofiaVoiceType` `[0022EE]` + Jarvis/CrookedPriest/Colin 配角音。
- **CombatStyle（5）**：`SofiaMeleeOnly/RangedOnly/MagicOnly/DualWeildOnly` + `csVoldar`，配 6 個 Class，組成 MCM 可切換的戰鬥矩陣。
- **Container（3）+ Cell（1）**：`SofiaStorage`/`SofiaClothes`/`SofiaTempStore` 放在自訂內景 cell `JJSofiaStore` `[00E600]`（readme 的 `coc jjsofiastore`），含 1 個自訂 NavigationMesh。
- **StoryManagerQuestNode（1）**：`JJSofiaGuardTrigger` `[07182A]`——唯一一個 SM 觸發（衛兵互動），其餘對話皆靠 force-greet package / scene，非 SM。
- **DialogView（9）**：CK 用的對話視圖容器（QuestMeeting / IntroForceGreet / BardSongs / GiveGift / Wedding / Relationship / Questions / GenericFollower / LeadTheWay），把分散在多 quest 的 branch 聚到一個 CK 編輯視圖。

