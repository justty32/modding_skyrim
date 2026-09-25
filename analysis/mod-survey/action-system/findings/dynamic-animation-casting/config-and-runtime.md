# DAC 功能、設定格式與執行依賴

← [dynamic-animation-casting](../dynamic-animation-casting.md)

## 是什麼（What it does）

- 一個 SKSE plugin，hook 動畫事件系統。當任一 actor（玩家或 NPC）播放到設定中指定的 **animation event**（如 `HitFrame`、`BeginCastLeft`、`MRh_SpellFire_Event`…），DAC 就在該 actor 身上**釋放一組 spell**。
- 等於把「揮刀的那一幀」「開始唸咒的那一幀」變成 spell 觸發點——招式特效、反擊光環、近戰附魔射彈、weapon-art 全靠它。是 BFCO/SCAR 那條「動畫驅動戰鬥」鏈裡負責「動畫 → 施法」的一支（PIE 負責「動畫 → 設 graph var」，DAC 負責「動畫 → 放 spell」）。
- 對 mod 用戶：裝 DLL 即可，零操作；對 modder：寫一個 `.toml` config 就能擴。**這正是 ModForge 主場——可生成的純文字 config。**

## Config schema（核心交付，**實檔驗證 NG Plus 73293 v3.2.4**）

出貨在：`SKSE/plugins/_DynamicAnimationCasting/*.toml`（資料夾下所有 `.toml` 都會被讀；檔名隨意，慣例 `<Mod>.toml`）。**格式是 TOML，不是 JSON**——每筆綁定是一個 `[[event]]` array entry。隨附 `AnimEvents.txt`（約 1300 個合法 animation event 名清單，給作者查 `AnimationEvent` 該填什麼）。

FormID 一律走 **DAR/OAR 風格字串** `"Plugin.esp|0xFormID"`（NG Plus 官方 template 明寫「same as DAR format」；玩家 = `"Skyrim.esm|20"`）。

### 必填
- `AnimationEvent` = `<String>` — 要在哪個動畫事件上觸發（查 `AnimEvents.txt`）。

### Spell（要放什麼）
- `SpellFormIDs` = `<Array[Form ID | 特殊符號]>` — 要釋放的 spell 清單。特殊符號（**實檔 template 列出**）：
  - `@FOREHAND` 當前手上裝備的 spell／`@OFFHAND` 另一手／`@POWER` 選定的 power/shout／`@FAVOURITE` 我的最愛裡的一個（由 Papyrus 選）／`@<STRING>` 由 Papyrus `RegisterCustomSpell("STRING", spell)` 註冊的自訂名。
  - 例：`["Skyrim.esm|0x7D997", "@OFFHAND", "@TEST"]`。
- Spell 過濾旗標：`CastOnlyFirstSpell` / `CastOnlyKnownSpell`（actor 不會就不放）/ `IgnoreConcentrationSpell` / `IgnoreBoundWeaponSpell`（皆 `<Boolean>`）。

### 條件（全部 AND；不用的就省略）
`HasActorFormID` / `HasRaceFormID` / `HasEffectFormID`（有此 active effect 時）/ `HasKeywordFormID` / `HasPerkFormID` / `IsEquippedRightFormID` / `IsEquippedLeftFormID` 皆 `<Form ID>`（`0`/`-1` = 忽略）；`HasWeaponType` = `<Enum>`（`"HandToHandMelee" "OneHandSword" "OneHandDagger" "OneHandAxe" "OneHandMace" "TwoHandSword" "TwoHandAxe" "Bow" "Staff" "Crossbow" "Spell" "Shield" "Torch"`）；`HasWeaponKeyword` / `HasWeaponEnchantEffect` = `<Form ID>`；`IsOnMount` / `IsSneaking` / `IsRunning` = `<Boolean>`；`Chance` = `<Float 0–1>`（亂數沒過就不放）；`Cooldown` = `<Float 秒>`；`ExclusiveGroup` = `<String>`（同 group 在同一 event 只觸發一筆，防同一施法重複觸發）。

### Properties（消耗與強度，皆 `<Float>`，**整筆只扣一次、非每 spell**）
`HealthCost` / `StaminaCost` / `MagickaCost` / `CastMagickaCostFactor`（預設 1.0）/ `EnchantmentCost`（WIP）/ `EnchantmentCostFactor`（WIP）/ `Effectiveness` / `Magnitude`（似乎只對 Restoration 生效）/ `WeaponEnchantMagnitudeFactor`（同前）；`DualCasting` = `<Boolean>`（強制雙手施法加成）。

### 實例（NG Plus 官方 template 內的範例，**逐字引自檔案**）
```toml
# Instant cast spells (no charge time) when sneaking
[[event]]
AnimationEvent = "BeginCastLeft"
HasActorFormID = "Skyrim.esm|20"
SpellFormIDs = ["@FOREHAND"]
HasWeaponType = "Spell"
IsSneaking = true
```

### Papyrus API（隨附 `DynamicAnimationCasting.psc`，3 個 global native）
```papyrus
bool function RegisterCustomSpell(string name, Spell spell) global native  ; → @NAME
bool function SelectFavouriteSpell(int index) global native                ; → @FAVOURITE
int  function NextFavouriteSpell(int delta) global native
```
即：config 只能寫死 FormID 或 `@FOREHAND`/`@OFFHAND`/`@POWER`/`@FAVOURITE`；要動態指定任意 spell，得在 config 用 `@MYNAME` 佔位，再由 Papyrus 在 runtime `RegisterCustomSpell("MYNAME", someSpell)` 綁上去。

## 機制 / 依賴（Mechanism / deps）

- **出貨內容（NG Plus 實檔驗證）**：`SKSE/plugins/loki_DynamicAnimationCasting.dll`（+ `.pdb`）、`Scripts/DynamicAnimationCasting.pex` + `Source/Scripts/*.psc`、`_DynamicAnimationCasting/template.toml`（含完整欄位註解）+ `AnimEvents.txt`。**無 esp/esm、無 MCM、無 Nemesis patch**——純 DLL + config 表 + 薄 Papyrus API。
- **驅動方式**：純 **config-file driven**（讀 `.toml`），不是 hkx 內 annotation。它不需要動畫師在 hkx 裡加註釋——只要動畫**本來就會送出**某個 animation event（vanilla 行為圖天然有 `HitFrame`/`BeginCastLeft`/`attackStart`…，BFCO/MCO 等再補更多），config 把那個 event 名綁到 spell 即可。這點與 PIE（需 hkx annotation）關鍵不同，對 ModForge **更友善**。
- **依賴**：SKSE64 + Address Library。`@FAVOURITE`/`@NAME` 路徑需 DAC 自帶的 `DynamicAnimationCasting.psc` 編譯產物（已附 pex）。**未見** PapyrusUtil/JContainers/SPID 等外部相依。

