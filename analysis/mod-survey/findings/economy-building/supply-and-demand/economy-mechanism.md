# supply-and-demand — economy-mechanism

← [調查入口](../supply-and-demand.md)

## 1. Classification（類型）

- **類型**：dynamic economy / 物價系統 mod（**transaction-tracking Papyrus controller**，非靜態 record overhaul）。
- **plugin**：`Supply and Demand.esp`（52 KB，**非 ESL-flagged**；master = `Skyrim.esm`, `Update.esm`），**僅 12 筆 record**。
- **SKSE 依賴**：**SkyUI + SKSE**（MCM 走經典 `SKI_ConfigBase`，見 §3/§5）。**無 SKSE DLL plugin、無 SPID/KID/FLM ini、無 MCM-Helper json、無 PapyrusUtil/JContainers 依賴**（解壓目錄只有 `.esp` + `Scripts/*.pex`，全程已 `find` 確認無 `.dll`/`.ini`/`.json`/`.psc`）。
- **系統價值**：**高**。這是 survey 裡第一個確認的「**真・動態物價引擎**」——它在執行期實際改寫物品的 gold value，跟 Trade & Barter 那種「靜態 conditioned-perk 物價修正」是**根本不同的 lever**，對 ModForge roadmap 的「transaction-tracking controller pattern」缺口是直接證據。

## 2. What it does

把 Skyrim 商人經濟變成**供需驅動**：玩家**大量買進**某物 → 該物市場價**因 demand 上升**；**大量賣出** → 價格**因 supply 下降**；隨遊戲時間流逝，市場價**逐日回歸正常**（"As time passes, market values shift back to normal."）。玩家會收到通知（"The market price of … increased/decreased by … due to demand/supply."、"Supply and Demand begins!"）。pex 字串實證的 feature 點：

- 物品 gold value 被**實際讀寫**（`GetGoldValue` / `SetGoldValue`、`GetValue`，配 `Modifier` / `NewValue`）。
- **30 組值陣列**：`ValuesArray1…ValuesArray30` 與 `OriginalValuesArray1…30`——記住每個追蹤類別的**目前值**與**原始值**，回歸 baseline 用（*inference*：30 個物品分類 bucket）。
- **每日回歸**由 MCM 的 "Daily Extinction Ratio" 控制（GLOB `tc_Global_ExtinctionRatio`）。
- 物價對**地點類型**敏感：`LocTypeSettlement` / `LocSetCave` / `LocSetCaveIce` / `LocSetDwarvenRuin` / `LocSetNordicRuin` / `LocSetMilitaryCamp` / `LocSetMilitaryFort`（pex 內 location keyword 變數，*inference*：不同地點 / 容器歸不同市場）。
- 增減量「Increase the item's value by either a percentage, or increase by 1」、四捨五入分歧（"Split for rounding up on decreases or rounding down on increases"）。

## 3. Mechanism（核心：STATIC vs DYNAMIC — 這是關鍵軸）

**結論：DYNAMIC transaction-tracking Papyrus controller。完全沒有 GMST、沒有 ModBuyPrices/ModSellPrices perk、沒有 VendorValues／merchant-gold record 編輯。** `dump` 出的 12 筆 record 全在下面，沒有任何 perk / GMST / Faction / LVLI override：

實際 record（ModForge `dump` 實看）：

<!-- wf-nav -->
- **GLOB** ×2：`tc_Global_ExtinctionRatio`（Float）、`tc_Global_HideNotifications`（Short）。
- **MGEF** ×3：
  - `tc_MonitorEffect`（archetype=**Script**, ConstantEffect/Self）→ 掛 `tc_PlayerScript`（3 props）。
  - `tc_ApplyingEffect`（archetype=**Script**, Concentration/Aimed）→ 掛 `tc_AttachScript`(1) + `tc_PlayerScript`(2)。
  - `tc_CloakEffect`（archetype=**Cloak**, ConstantEffect/Self, assoc=`tc_ApplyingSpell`）。
- **SPEL** ×4：`tc_CloakSpell`（Ability，效果=CloakEffect）、`tc_MonitorAbility`（Ability，效果=MonitorEffect）、`tc_ApplyingSpell`（Spell，Concentration/Aimed）、（以上三者 equip=`013F44:Skyrim.esm` VoiceEquip）。
- **QUST** ×2：`tc_SupplyDemandMCM`（掛 `tc_SupplyDemandMCM` 3 props，flags=17 = StartGameEnabled+RunOnce 類）、`tc_SupplyDemandQuest`（flags=273）。
- **vanilla override** ×2：`WhiterunBanneredMare` CELL + `WhiterunBanneredMareChestRef`（容器 ref）——*inference*：拿一個 vanilla 商人容器當測試/掛載錨點。

**運作鏈（pex `strings` 實證 + inference）：**

<!-- wf-nav -->
1. **player 掛載**：`tc_CloakSpell`（Ability）→ `tc_CloakEffect`（Cloak archetype）→ cloak 命中目標時 `tc_AttachScript`(內含 `AddSpell` / `GotoState`) 把能力掛上去（"Attaches an ability to the player"）。`tc_PlayerScriptAddSpell` 也有 `CloakAbility` / `mymod_CloakEffectOn` GLOB-gate + `PlayerRef` ReferenceAlias + `OnInit`/`OnUpdate`——*inference*：開局把系統 bootstrap 到 player。
2. **交易偵測 = 真動態核心**：`tc_PlayerScript`（68 KB，最大 script）有 **`OnItemAdded` / `OnItemRemoved`**，配 `akSourceContainer` / `akDestContainer` / `aContainer`——監聽物品在容器/商人/玩家之間移動，即「買/賣」事件。
3. **改價**：偵測到交易 → `GetGoldValue` 讀目前市價，依 `Modifier` 算 `NewValue`，`SetGoldValue` **寫回該物的 base value**（連帶 `HasKeyword`/`GetCurrentLocation`/`GetFactionOwner`/`GetInheritedOwner`/`GetParentCell` 判斷是哪個市場/分類）。`ValuesArray*` 存目前值、`OriginalValuesArray*` 存原始值。
4. **回歸**：`tc_MonitorScript`（`OnUpdate` / `RegisterForSingleUpdate` / `UnregisterForUpdate` / `GetCurrentGameTime`）週期把市價依 `tc_Global_ExtinctionRatio` 往 `OriginalValuesArray*` 拉回。

**Papyrus（共 5 個 controller script，全 hand-authored，無 generated fragment 跡象）**：`tc_PlayerScript`（主控/交易偵測/改價）、`tc_MonitorScript`（時間回歸 OnUpdate）、`tc_AttachScript`（cloak→AddSpell 掛載）、`tc_PlayerScriptAddSpell`（bootstrap）、`tc_SupplyDemandMCM`（MCM）。**這就是 Trade & Barter 那條 finding 推測「動態供需幾乎一定要 script 追蹤交易」的活證據**。

**MCM**：`tc_SupplyDemandMCM.pex` 是經典 **`SKI_ConfigBase`**（`AddSliderOption`/`AddToggleOption`/`OnConfigInit`/`OnPageReset`/`OnOptionSliderAccept`…），**不是 MCM-Helper**。只配 **兩個選項**：① **"Daily Extinction Ratio"** slider → `tc_Global_ExtinctionRatio`；② **"Hide Notifications"** toggle → `tc_Global_HideNotifications`。MCM 寫值 → GLOB → script 讀（典型 MCM→GLOB→runtime 連線）。

## 4. vs Trade & Barter（同一目標，相反的 lever）

兩者都想「讓商人物價更有層次」，但**機制完全相反**：

- **Trade & Barter**：**STATIC**——一堆 conditioned `ModBuyPrices`/`ModSellPrices` **EntryPoint perks**（faction/location/skill/race 為 CTDA gate），唯一 script 是 MCM。價格修正是**規則化、條件式、不隨遊玩改變**；近乎純 record overhaul，可被 ModForge **今天就生成**。
- **Supply and Demand**：**DYNAMIC**——**零 perk、零 GMST**，靠 Papyrus 監聽 `OnItemAdded`/`OnItemRemoved` 後 `SetGoldValue` **改寫物品真實 base value**，再隨時間回歸。價格**隨玩家行為演化**。這是 ModForge **生不出邏輯本體**的東西（見 §5）。

一句話：T&B 改的是「barter 公式的係數」，S&D 改的是「物品本身值多少錢」且會浮動。

