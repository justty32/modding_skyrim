# 三、對 ModForge 的參考價值（可生成 / 需新支援 / 純參考）

← [原文入口](../immersive-interactions.md)

## 三、對 ModForge 的參考價值（可生成 / 需新支援 / 純參考）

### 可生成（ModForge 資料層直接能產）
- **GlobalShort / GlobalVariable 批量**：`AR_*` 那 43 顆設定旗標純資料，ModForge 既有 global 支援即可生成。
- **FormList 批量**：35 個目標分類 FormList 是這個 mod 的「資料驅動」骨架，ModForge 能生成（HasForm 分類是很乾淨的、可被 spec 描述的模式）。
- **MagicEffect + Ingestible（buff 道具）**：`AR_Energized` / 食物 MGEF（PeakValueModifier）——既有 magic/MGEF 支援涵蓋。
- **SoundMarker / SoundDescriptor**：自訂音效記錄可生成。
- **Furniture override（加 keyword）**：4 個 vanilla Lever 的 additive override 只是補 keyword——屬 override-record 模式（參照 `worldspace-override-*` 筆記的 additive-carry 手法）。
- **Quest 殼 + ReferenceAlias（玩家別名）**：空 Quest + alias 容器可生成；**但掛在 alias 上的腳本**屬下一類。

### 需新支援（ModForge 目前缺、值得補的能力）
<!-- wf-nav -->
- **Perk Entry Point「Add Activate Choice」+ 對應的 Perk Fragment**：這是整個 mod 的觸發核心。查 `src/ModForge.Core/Generator.Build.Perks.EntryPoints.cs` 的 `EntryPointTabCount` 表，**沒有 `AddActivateChoice` 也沒有 `SetText`(SetActivateLabel)**——entry-point builder 目前只覆蓋戰鬥/數值類。要生成這類「自訂 Activate 選項 + fragment 派發」的互動 mod，ModForge 需：(1) 支援 AddActivateChoice / SetText entry type（含其 tab-count，呼應 `perk-conditiontabcount-ctd` 筆記：tab-count byte 不對會 load CTD）、(2) 能生成 Perk-fragment 黏合（Perk script + per-effect fragment index），目前 fragment 生成只在 SCEN/quest 路線（見 `scene-playidle-recipe`）。
- **Perk EntryPoint 上的 CTDA conditions（GetIsID/HasKeyword/條件分流）**：AddActivateChoice 之所以能分流，靠每個 effect 帶條件。需確認 ModForge perk builder 能把條件掛到 entry-point effect 層（非 perk 層）。
- **DAR `_conditions.txt` 生成器**：`_CustomConditions/<priority>/_conditions.txt` + `.hkx` 擺放是純文字 + 檔案佈局，ModForge **完全可以新增一個 packaging 步驟生成**（把「global 值 → 動畫資料夾」這個對照表 spec 化）。建議列為 OAR/animation 線的可生成項（OAR 的 `config.json` 更結構化、更該優先）。
- **FNIS list 生成**：`FNIS_..._List.txt`（`ofa`/`o`/`b`/`s`/`+` 語法）同理可由 spec 生成——但 FNIS 已被 Nemesis/Pandora 取代，新支援應瞄準 OAR。

### 純參考（必須靠外部 framework，ModForge 不生成）
- **Dynamic Activation Key (DAK)**：原生 SKSE 外掛，提供長按/短按 Activate 分流。ModForge 不可生成，只能在 spec 標為「外部 master 依賴」。
- **FNIS / Nemesis / Pandora behavior 引擎**：產 `*_Behavior.hkx` 需執行外部工具，非 esp 資料。
- **DAR / OAR runtime**：條件解析在外掛內，ModForge 只能生成它讀的「資料」（見上一類），引擎本身純參考。
- **`.hkx` 動畫檔**：手工製作/外部資產，ModForge 只搬運不生成。
- **SkyUI MCM**：`AR_MCMScript` 依賴 SkyUI；ModForge 可生成 global，但 MCM 面板本身靠 SkyUI framework。

### 與既有 ModForge 筆記的連結
- **`scene-playidle-recipe`**：本 mod 的 `PlayIdle(idleXxx)` / `Debug.SendAnimationEvent` + `OffsetStop` 收尾，和 scene PlayIdle 的「每 phase 一個 idle + 收尾」模式同源；DAR 的 global-選擇器則是 scene 之外的另一條 PlayIdle 變體控制法，可互相參照。
- **`perk-conditiontabcount-ctd`**：若 ModForge 要新增 AddActivateChoice entry-point，務必依此筆記補對 tab-count，否則 load CTD。
- **`dispatcher-magic-trigger`**：本 mod 的「perk fragment → Activate.fXxx() 中央 quest script」是另一種 dispatcher 模式（trigger 進、quest script 集中處理），與既有 dispatcher-psc 派發 Fire() 思路一致——quest-script-as-dispatcher 是可重用的生成樣板。
