# 1. 這個 mod 做什麼

← [原文入口](../spellforge.md)

## 1. 這個 mod 做什麼

Spellforge 是一個**法術鍛造工作站**：玩家召喚 / 找到一座「Spellforge」鐵砧，把材料（轉成 *Resin* 的鍊金素材 + 紙 + 墨水）投進去，選一組條件，工作站就把對應的法術**教給玩家**（`AddSpell`），或產出捲軸 / 法杖。它也能逆向——把已會的法術「回收」(recycle) 換回材料。

關鍵在於：**它本身幾乎不含任何「可施放的法術」內容**。鍛造出來的法術全部是**別人寫好的**——vanilla 或一卡車法術 mod（Apocalypse、Odin、Mysticism、Triumvirate、Forgotten Magic、Colorful Magic…）。Spellforge 只是一個**目錄 + 取得機制**疊在這些既有法術之上。

## 2. 怎麼運作（鍛造機制）

**結論：100% 預製 SPEL 池（pre-authored pool），零 runtime MGEF 組裝。** 沒有「把火 effect + 範圍 effect 拼成新法術」這回事；玩家只是用條件**篩選並取得一個早就存在的 SPEL 記錄**。

### 2a. 兩層 esp 架構

| esp | 角色 | record 普查（用 ModForge `dump`） |
|-----|------|-----------------------------------|
| `Spellforge.esp`（122 KB） | **機器本體**：UI、狀態、FX、材料邏輯 | 80 Message、43 PlacedObject、33 FormList、30 Activator、27 GlobalShort、21 MiscItem、10 Explosion、**8 Spell、8 MagicEffect**、3 Projectile、3 Hazard、2 Quest、2 Book |
| `Spellforge - Library - *.esp`（每個法術 mod 一個，5–22 KB） | **純索引 metadata**：把該 mod 的既有法術分類進 FormList。**不含任何新 SPEL/MGEF** | 例如 `AE Spells`：32 FormList + 1 Quest + 1 Message，**零 Spell** |

核心 esp 的 8 個 SPEL / 8 個 MGEF **全是工作站機械**，不是目錄法術：`SFM_ConjureForge`（`Script` archetype，召喚鐵砧）、`SFM_ForgeEnkindle`（點火）、`SFM_ForgeHeatingHazardSpell`（Hazard：靠太近燙傷，`ValueModifier`/Health/`ResistFire`/Touch）、`SFM_ForgeVortex*`（吸入特效）、`SFM_SpellCreationFX`。沒有一個是給玩家施放的內容法術。

### 2b. 法術目錄 = 平行 FormList 的「座標系」

每個 library esp 為它的法術，沿幾條正交軸建**平行 FormList**（patch lists），library quest 上的 `sfm_librarytransferscript` 在載入時把它們 merge 進核心 esp 的 base lists：

- **Delivery**：`DeliveryAimed` / `DeliveryLocation` / `DeliverySelf`
- **Level**（複雜度）：`Level0Novice` … `Level4Master`
- **Method**：`MethodConcentration` / `MethodFireForget`
- **Principle**（「做什麼」分類）：`Principle00` … `Principle19`（20 個語意 bucket：傷害火、召喚、護盾…）

一個法術由它在這些平行清單裡的**索引位置**辨識（同一 index 跨清單對齊）。`sfm_spellstorage` 警告 *"Missing level/method/delivery flist for spell at index N"* 證明這是 index-aligned 的平行陣列，不是 keyword 標記。

### 2c. 鍛造一次的流程（`sfm_forgescript`，33 KB，核心）

<!-- wf-nav -->
1. 玩家在工作站選條件，組成一個 **"definition"**：`compose_flag_school` + `compose_flag_principle` + `compose_flag_level` + `compose_flag_method` + `compose_flag_delivery`。
2. `find_all_spells_for_definition` / `get_all_indices_for_definition`：**交集**那幾條平行 FormList，找出符合 definition 的所有預製 SPEL。
3. 技能 / 任務 gate：`get_school_skill_level` 對 `get_desired_skill_level`（MCM `RequireMagicSkill`、`RequireMasterQuest`、`_SchoolLock` / `_SchoolPrincipleLock`）。
4. 收費 + 扣料：`ApplyCostMultipliers`，magicka 花費 = `MagickaCostPerComplexity × complexity`（complexity = level tier），材料 = `Resin`（`ConvertIngredientsToResin` / `ClaimResin`）+ `paper_cost` + `ink_cost`（`Inkwell01`）。全部走 Global + MCM 滑桿可調。
5. 交付：`Game.GetPlayer().AddSpell(theSpell)`（法杖 / 捲軸則產 item）。`AddSpellExclusion` 處理互斥組。
6. **回收**（`sfm_spellrecyclescript`）：`GetEquippedSpell` → `RemoveSpell` + `RemoveAndConvert` 退回部分材料。

### 2d. SKSE / Papyrus / MCM 比重

- **SKSE DLL：0%**。完全沒有 native plugin。
- **Papyrus：100% 的邏輯**。14 個 `.pex`（藏在 BSA，根目錄那兩個只是 stub）：`sfm_forgescript`(33K, 主控)、`sfm_spellstorage`(14K, 目錄存取)、`sfm_mcmconfigscript`(13K)、`sfm_configbookscript`(13K, 用一本「設定書」當 UI)、`sfm_spellrecyclescript`、`sfm_librarycontainerscript` / `sfm_librarytransferscript`(library merge)、`sfm_principleselectorscript`、`sfm_deliveryselectorscript`、`sfm_playertrackingscript`、`sfm_castspell`、`sfm_setglobalonload`。
- **MCM**：有 SkyUI MCM（`sfm_mcmconfigscript`，`AddToggleOptionST` / `AddSliderOptionST`），但**也有一條無 SkyUI 的退路**——`SFM_ConfigBook`「Spellforge Manual」用 80 個 Message-box 串成選單。UI 完全靠 vanilla engine 的 Message / Activator / Book，**不需要任何外部 UI 資產**。

