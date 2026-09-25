# 一、這個 mod 做什麼 + 怎麼運作

← [原文入口](../immersive-interactions.md)

## 一、這個 mod 做什麼 + 怎麼運作

Immersive Interactions（內部 EditorID 前綴 `AR_`，原名 "Animations Reborn"）讓玩家**啟動（Activate）世界物件時播放情境動畫**：開門、撿地上物、開鎖、搜屍、開箱、祈禱、向衛兵/小孩/將領/Jarl 敬禮、摸狗、擠牛奶、解謎機關（拉桿/按鈕/柱子/鏈條）、撿柴、滅火、讀書讀信、用毒咳嗽、坐下等待等。

**機制總結（重點）：完全沒有 SKSE .dll，純資料 + Papyrus + 動畫框架。** 不是 hardcoded 在原生外掛裡，而是三層協作：

<!-- wf-nav -->
1. **觸發層 = Perk Entry Point「Add Activate Choice」**。一顆 `AR_AnimPerk` (Perk 0x000802，OnInit/OnPlayerLoadGame 時 `AddPerk` 給玩家)，掛 **33 個 entry-point effect**：29 個 `PerkEntryPointAddActivateChoice` + 4 個 `PerkEntryPointSetText`(SetActivateLabel)。每個 AddActivateChoice 帶 **conditions**（用 `GetIsID` / keyword / FormList 判斷 crosshair 目標是門/箱/屍/狗/衛兵…）＋一段 **perk fragment**（`AnimimationsReborn_Fragments.psc`，Extends Perk）。fragment 只做一件事：呼叫 quest script 對應函式，例如 `Activate.fOpen(akActor, akTargetRef)`、`Activate.fpetdog(...)`、`Activate.fpuzzle(...)`。
   - 注意 master 列含 **`Dynamic Activation Key.esp`（DAK）**。DAK（自身是 SKSE 外掛）提供「長按 Activate 走 perk choice、短按走原版」的分流；本 mod 把它當依賴，而非自帶 dll。`OnControlUp` 裡也用 `RegisterForControl("Activate")` + `HoldTime` 自己判長按（撿柴/滅火/喝蜜酒那條走 `FindClosestReferenceOfAnyTypeInList` 找附近 static）。

2. **邏輯層 = `AR_QuestScript.psc`（Extends Quest）**。所有 `fXxx()` 函式的家。流程模式高度一致：`IsPlayerIn3rd()`(強制第三人稱+鎖控制) → 設動畫選擇器 global → `PlayIdle`/`SendAnimationEvent` 播動畫 → `utility.wait` → `akTargetRef.Activate(akActor)` 真正執行原版啟動 → 收尾 `Returnto1st()`。用 `bool busy` 當互斥鎖、`bisDoingFavor` 防跟隨者 favor 衝突。目標分類**全靠 FormList.HasForm()**（`Interact_Levers`/`Interact_Buttons`/`Interact_Pillars`/`Interact_Chains`/`Interact_Bars`/`Interact_Puzzle`…各一個 FormList）。
   - `AR_Ref_AliasScript.psc`（Extends ReferenceAlias，掛玩家別名）跑被動 event：`OnObjectEquipped`（吃食材咳嗽、讀書動畫）、`OnItemRemoved`（用毒）、`OnControlDown`（按 Wait 改坐姿+調 timescale）。

3. **動畫選擇層 = FNIS + DAR（Dynamic Animation Replacer）**。動畫本身用 **FNIS** 註冊自訂 idle/offset anim（`FNIS_ImmersiveInteractions_List.txt`：`ofa`/`o`/`b`/`s`/`+` 行定義 `AO_OpenDoor`/`AO_PickUp`/`AO_IdleLockPick`/`AO_IdleTake`…動畫事件名 + .hkx）。而「同一個動作要播哪一種變體」靠 **DAR**：7 個 `_CustomConditions/19931..19937` 資料夾，每個一個 `_conditions.txt`，條件就是
   ```
   ValueEqualTo("ImmersiveInteractions.esp"|0x0000AA13, N)
   ```
   亦即讀 GlobalShort **`AR_DogUp` (0x0000AA13)** 的整數值（1..7）。Papyrus 在播動畫**前**用 `AR_DogUp.SetValue(N)`、播完 `SetValue(0)`，DAR 即時換上該層資料夾裡的 `.hkx`（不同高度/姿勢的撿取、不同搜尋動畫等）。**Global 變數當 DAR 的執行期選擇器**就是這個 mod 的核心巧思。

一句話：**Perk-AddActivateChoice（條件分流）→ perk fragment → Quest script（鎖+播動畫+延後 Activate）→ Global 寫值 → DAR 依 Global 換 FNIS 動畫變體。** 完全資料/腳本驅動，零原生程式碼（DAK/FNIS/DAR 是外部依賴）。

## 二、關鍵檔案與模式

本表整理「二、關鍵檔案與模式」的逐項記錄。

已抽到 [interaction-mechanism-and-files-key-files.json](interaction-mechanism-and-files-key-files.json)（8 列）。

欄位「檔案」：保留原表的檔案。

欄位「角色」：保留原表的角色。

統計：8 筆記錄，2 個欄位。


**用到的動畫事件名（FNIS / SendAnimationEvent）**：`AO_OpenDoor`、`AO_PickUp`、`AO_PickupLow`、`AO_IdleLockPick`、`AO_IdleTake`、`AO_IdleKnock`、`AO_Kneel(Enter/Exit)`、`AO_Cut`、`AO_Tan`、`AO_NoteStart/During/Exit`、加上大量原版 idle（`idlepickup_ground`、`idlegreybeardwordteach`、`idleSearchingChest/Table`、`idlewave`、`idlesalute`…）以 `PlayIdle(Idle property)` 播放。
**用到的 keyword**：`VendorItemIngredient`、`VendorItemPoison`、`VendorItemSpellTome`、`Armor*`/`Clothing*`（armor 換裝動畫分類）。

