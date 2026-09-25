# real-estate — mechanism

← [調查入口](../real-estate.md)

## Mechanism（取自 `dump` + `questdiag` + pex `strings`）

### Record shape（`dump` tally，未整載）

Record shape（`dump` tally，未整載）的逐列資料。

已抽到 [real-estate-records.json](real-estate-records.json)（14 列）

record：原表「record」欄。

count：原表「count」欄。

角色：原表「角色」欄。

統計：14 列記錄；3 欄。

### 1. 「可買房產」= 一塊**腳本化 Activator 告示牌 ref**（不是改房子本身）

可買的房子**不靠任何 keyword 標記、不掃描、不改房子記錄**。作者**手工在每棟 vanilla 房子外置入一個 `RE_PropertySign` 的 PlacedObject**，editorId 即房名：`RE_Sign_LeigelfHouse`、`RE_Sign_TheFrozenHearth`、`RE_Sign_GraveConcoctions`…（`dump` 可見 base = `RE_PropertySign` 的告示牌散佈各 cell）。每個 sign ref 掛 `RE_PropertySignScript`，**帶 4 個 per-instance 屬性**（價格 / 地點 / 收益型別覆寫——具體欄位 UNVERIFIED，但 base script 有 `__PriceOverride` 屬性可逐房調價）。

→ **「發現可買房」= 純靜態置放一個帶腳本的 Activator**，零 runtime 掃描。礦場用 `RE_MineSign`、農場用 `RE_FarmSign`（各自的 script 帶 ~46 個屬性）。

### 2. 買 / 賣 = `RE_PropertySignBaseScript` 的 **state machine（`Owned` / `Not owned`）**

`RE_PropertySignScript`（72 屬性，掛在 sign ref）繼承 `RE_PropertySignBaseScript`（基底，含計價/所有權邏輯）。確認到的函式（pex strings）：

- **`OnActivate(player)`** → 跳 message-box；`Buy` / `Sell` 函式切 state（`GotoState`，state 名 `Owned` / `Not owned`，pex 字面值 `Owned` / `Not owned` 確認）。
- 計價：`GetBasePrice` 讀 `RE_HouseBasePrice` / `RE_ShopBasePrice` / `RE_InnBasePrice` GLOB × **`GetLocationMult`**（依房子所在城市讀 `RE_WhiterunMult`/`RE_RiftenMult`/…/`RE_SkyrimMult` GLOB，靠 `Game.GetPlayer().IsInLocation(<XxxLocation>)` 判定城市，pex 見 `WhiterunLocation` 等屬性）× `RE_PriceMult` 全域倍率，並夾在 `RE_MinPrice` 之上。
- **`RE_UsePerks` GLOB 開啟時**：買房前 `Game.GetPlayer().HasPerk(...)` 檢查（house=Haggling / shop=Merchant / inn=Investor / special=Master Trader，見翻譯檔 `RE_UsePerksInfoText`），不足跳 `RE_NeedPerkMsg`。
- 計數：每買一棟把對應 `RE_HousesOwned` / `RE_ShopsOwned` / `RE_InnsOwned` / `RE_SpecialsOwned` GLOB +1。

### 3. **所有權變更 = 用「佔位 Weapon token」+ 引擎 ownership**（巧妙繞道，可借鏡）

`ChangeOwnership`（base script）不直接設玩家所有權，而是操作那組**佔位 Weapon**：`RE_OwnerReplacement` / `RE_LocationReplacement` / `RE_Product1..3Replacement`（全是 0-value、隱形用的 token Form，給腳本當「可替換的 actor/location/product 引用容器」）。base script 帶 `_Owner`(actor[]) / `_Location`(location) / `_PropertyDeed` 屬性，買下時把 sign 綁定的房子/容器所有權改成玩家、產出型別綁到 product token。

保險箱用更直接的 vanilla API：`RE_SafeScript`（掛 `RE_MainSafe` 容器）在 `OnInit` `SetActorOwner(Game.GetPlayer().GetActorBase())`，並 `OnItemRemoved` 重設——這是標準 **XOWN/SetActorOwner** 防盜。`RE_FakeSafeScript`（掛 `RE_MainSafeAct_Safe` Activator）是「假保險箱」門面，啟動轉接到真容器（`Activate`），並用 `RE_SafeKey` Key + `RE_NoKeyMsg` 做上鎖門面。

> ⚠️ **UNVERIFIED**：`ChangeOwnership` 內部到底呼叫 `Reference.SetActorOwner` / `SetFactionOwner` / `Location` API 哪一個——pex strings 只見 token 屬性與 `ChangeOwnership` 函式名，未見明確的 `SetLocationOwner` 字面值（PropertySign base 無此 import；只有 SafeScript 有 `SetActorOwner`）。token-replacement 是「把房子的 OwnerReplacement ref 換成玩家」的間接法，細節需反編譯才能定論。

### 4. 收租 = `RegisterForUpdateGameTime` / `OnUpdateGameTime` 被動 timer

`RE_PropertySignScript` 買下後 `RegisterForUpdateGameTime`（pex 見 `Buy - Registered for update` / `Sell - Unregistered for update`）；到期觸發 `OnUpdateGameTime` → `ChangeIncomeLevel` / 加錢（pex 見 ` Adding Income (GDP = ` / ` Income = ` debug 字面值）。收益 = 買價 × 該類型 `RE_HouseIncomeMult`/`RE_ShopIncomeMult`/`RE_InnIncomeMult` GLOB × `RE_IncomeMult`，週期由 `RE_IncomeRate`（MCM「每 N 天」），可選 `RE_RandomIncome` 在 min/max 間抖動。錢 `AddItem(Gold001)` 進 `RE_MainSafe`。

帳本（master ledger）：玩家用 `RE_LedgersQuill`（`RE_UpdateMLScript`，`OnEquipped`）`UpdateCurrentInstanceGlobal` 把所有權狀態寫回 `RE_IncomeAvailable` 等 GLOB——即「**用一個 quest instance + InstanceGlobal 當總帳**」的 pattern（quest = `RE_Quest`）。

### 5. 租客關係 = 4 個 **PERK** 當 ±rank 修正

`RE_RelationshipPerk_Rival(-1)` / `_Enemy(-3)` / `_Ally(+3)` / `_Friend(+1)`（Name `RE_RP -1/-3/+3/+1`）。`RE_PropertySignScript` 有 `SetRelationshipRank` / `SetTenantsRelationship`，買下店鋪/旅店後可把店員（租客）對玩家的 relationship rank 調整，受 `RE_EnableRelationshipPerks` GLOB gate。

### 6. 礦場敵人替換

`RE_MineSignScript`（46 屬性）帶 `Miner0..Miner19`（20 個礦工 ref 屬性）+ `_Enemy` 屬性 + `EnableMiners` / `Enable` / `Disable` 函式。買下礦場且 MCM `RE_MineReplaceEnemies` 開啟時：`Disable` 原敵人、`Enable` 礦工 ACHR（賣出反向）——即 **enable-parent 式的 ref 開關**，非生怪。

### 7. MCM = **SkyUI `SKI_ConfigBase`**（古典 MCM，非 MCM-Helper）

`RE_MCMScript` extends **`SKI_ConfigBase`**（pex 確認），是手寫腳本式 MCM（`OnPageReset` / `OnConfigOpen` / `AddSliderOptionST` / `AddMenuOptionST` / `OnSelectST`…），**不是** MCM-Helper 的 config.json 宣告式。頁面/選項文字全在 `Interface/translations/RE_RealEstate_ENGLISH.txt`（`$RE_*` key）。含 cheat 頁（`Add Safe Key` / `Set RE_Quest stage`）。設定值寫進那批 `RE_*Mult`/`RE_*BasePrice`/`RE_IncomeRate` GLOB。

### 8. 教學 quest `RE_Quest`（`questdiag 0x0038C0`，已驗）

7 stages（0/10/20/50/55/60/70）+ 6 objectives（買書→開保險箱→買第一棟→用 quill 更新帳本→收租→「打造你的房產帝國」）。type=ThievesGuild、StartUpStage。3 個 alias：`ML`(QuestObject+UsesStoredText, 指 `RE_Ledger`)、`Quill`(指 `RE_LedgersQuill`)、`Main Safe`(ForcedReference 指 Core esp 的容器)。`RE_IntroBook`（`RE_IntroBookScript`, `OnRead` AddItem 帳本+quill 並推進 quest）。另有 `RE_Thief01 "Robbed!"`（保險箱被偷的小事件）與 `RE_Arena01`（UNVERIFIED 用途）。

