# Sofia Follower —— Papyrus 腳本架構 — comments-and-relationships

[返回入口](../sofia-scripts.md)

### B. comment 排程器（Sofia 之所以「會吐槽」的引擎）

<!-- wf-nav -->
- **`SofiaCommentScript.psc`**（掛 `JJSofiaDialogue`，15 prop）—— **comment frequency 排程器**，Sofia「個性」的核心。函式 `OnUpdate / SofiaMakeComment / GetPlayerDialogueTarget / SetCommentFrequency / ReloadScript`。運作：用 `RegisterForSingleUpdate` 週期醒來，依 `SofiaCommentFrequency`（GLOB，MCM 可調 0=關）決定間隔，`SofiaDisableComments` 為總開關；觸發時呼叫 `GetPlayerDialogueTarget`（透過 `JJSofiaGetTargetSpell` 取玩家瞄準對象，見下）→ 啟動 `JJSofiaIdleDialogueScene` 或 `JJSofiaMainQuestDialogueScene` 念一句。同檔還掛 `JJSofiaSetHorseSpell`、`SummonSofiaSpell`、左手法術（`FireboltLeftHand/LightningBoltLeftHand/IceSpikeLeftHand`），並用 `IsInDialogueWithPlayer` 避免插嘴。**這支 + 259 個 TIF 對白池，就是「語音隨從會自言自語」的全部機制——純 timer-poll + scene.Start()，零 SKSE。**

- **`JJSofiaQuestUpdateScript.psc`**（掛 `JJSofiaMainQuestDialogue`，7 函式）—— 另一個 comment 觸發器，專管「劇情情境評論」：`SofiaWitnessDragon`（目睹龍時吐槽）、`SofiaMakeComment`、`GetPlayerDialogueTarget`。對應 record 層 `JJSofiaWitnessDragon` GLOB。

- **`JJSofiaGetTargetScript.psc`**（小，掛 `JJSofiaCastSpell`）+ **`jjsofiagettarget` 機制** —— 透過一個施在玩家身上的 spell 取得「玩家正看著誰/什麼」，供 comment 系統決定要評論誰。這是 Skyrim 沒有原生「取玩家準心目標」API 時的標準 workaround（cast 一個 script effect 法術讀 target）。

- **`JJSofiaQuestLineManager.psc`**（**161 個 property，零自訂函式**）—— 不是邏輯，是個**巨型 property 索引表**：`MQLine1..45`、`CollegeQuestLine1..28`、`CompanionsQuestLine1..20`、`ANightToRememberQuestLine1..8`、各 Daedric quest（BoethiahsCalling / TheBlackStar / TheCursedTribe / IllMetByMoonlight / TheHouseOfHorrors / DiscerningTheTransmundane / TheOnlyCure / ADaedrasBestFriend / TheBreakOfDawn / TheWhisperingDoor / WakingNightmare / TheMindOfMadness / PiecesOfThePast）的逐 stage 引用。它讓 Sofia 的對白條件能用「玩家在 X 主線/支線進行到第 N 步」當觸發——把幾十條 vanilla quest 的 stage 全綁進 property，對白才能「應景」。對照 `JJSofiaVariablesScript` 裡那批 `Accompanied*`（見下）。

### C. 狀態中樞與關係/婚姻/醉酒

<!-- wf-nav -->
- **`JJSofiaVariablesScript.psc`**（掛 `JJSofiaVariables`，**33 個 conditional property，僅 GetState/GotoState 無自訂函式**）—— record 層提到的「變數中樞」。全是布林/數值 property 當持久化旗標：`RelationshipLevel`、`SofiaIsDating`、`SofiaIsMarried`、`IsDrunk`、`IsTalking`、`KillsWitnessed`、`DungeonsWitnessed`、`TimeAccompanied`、`DaysAccompanied`、`NudeBombReady`、`SandboxingEnabled`、`InitiateRomanceDialogue`、`InitiateMarriagePrompt`，以及一整排 `Accompanied<VanillaQuest>`（AccompaniedMainQuest / AccompaniedCompanionsQuest / AccompaniedTheBlackStar / …）。**conditional property 會被對白 condition 直接讀**——這是 Sofia 把「狀態」攤在 Papyrus property 上、讓對白系統零成本查詢的手法，等價於別的 mod 用 StorageUtil 存的東西，但這裡純靠 quest script property 落存檔。

- **`JJSofiaRelationshipScript.psc`**（掛 `JJSofiaRelationship`，3 prop + `UpdateSofiaStats`）—— 好感度/統計累加。`OnUpdateGameTime` 週期跑 `UpdateSofiaStats`，把「Dungeons Cleared / People Killed / Animals Killed / Creatures Killed / Undead Killed / Daedra Killed / Automatons Killed」這些見證統計寫進 quest（字串字面值直接出現在 string table）。配 record 層 `SofiaPlayerLike` GLOB。

- **`SofiaMarriageScript.psc`**（掛 `JJSofiaRelationship`，`UpdateGold/SofiaInvestGold/CancelInvestGold` + `OnLocationChange`）—— 婚後經濟系統。`OnUpdateGameTime` 定期讓已婚 Sofia「找到 gold 分給你」或「花你的 Septims」（字面值「Sofia has found … gold which she shares with you.」/「Sofia has spent … Septims of your gold.」），`OnLocationChange` 配 `LocTypeTown`/`LocTypeCity` keyword 判斷在城鎮才結算。`SofiaInvestGold` 是 vanilla 配偶店鋪投資的仿作。

- **`SofiaDrunkScript.psc`**（掛 `JJSofiaDrunk`，9 prop）—— 醉酒狀態機。`OnInit/OnUpdateGameTime` 排程，property 串起 `SofiaDrinkPackage`/`SofiaDrunkPackage`/`SofiaDrunkStopPackage` 三個走路搖晃 package + `JJSofiaDrunkScene`/`JJSofiaDrunkSceneEnd`/`JJSofiaDrunkGiveDrinkDialogue` 三個 scene/對白。對照 record 層 drunk stage 0–50 與 `JJSofiaDrunkScene`（RepeatConditionsWhileTrue 循環）。

### D. 外觀 / 物品 / 換裝

- **`SofiaOutfitManagement.psc`**（`OnItemAdded/OnItemRemoved/SortOutfitStore`）+ **`SofiaSortOutfit.psc`** + **`SofiaWardrobeScript.psc`**（`OnItemAdded/RedressSofia/OnCombatStateChanged`）—— 換裝/衣櫥系統，監聽 container 物品進出自動分類、戰鬥結束後 `RedressSofia` 補穿。對應 record 層 `SofiaStorage`/`SofiaClothes` container 與 `JJSofiaWardrobe` quest。
- **`SofiaClothingFix.psc`** —— record 層提到的「脫衣 glitch」矯正。
- **`SofiaPlayerGive.psc`** / **`JJSofiaRecieveGold.psc`**（sic）—— 送禮收禮、收金幣（提升好感度），對應 `JJSofiaGiveGift` quest。
- **`SofiaNudeBombScript.psc`**（`OnEffectStart` → 是個 ActiveMagicEffect 腳本）—— record 層 `SofiaNudeBombSpell` 的效果腳本。

