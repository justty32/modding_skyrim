# Perk entry-point 機制概覽 + Entry-point 種類全表

← [perk-entry-points](perk-entry-points.md)

## 一、Perk entry-point 機制概覽

### 概念：引擎 hook 插槽

Perk 是玩家（或 NPC）身上的「被動增益」載具。一個 Perk record（PERK）可以帶多個 effect，每個 effect 選擇一種「觸發時機」（entry-point）並攔截引擎的計算或動作。引擎在執行對應動作時，會遍歷持有者身上所有 Perk 的 effect、找到匹配的 entry-point，依其 FunctionType 與條件決定是否介入。

```
PERK record
  ├── effect [ability]       → SPEL（常駐能力，始終生效）
  └── effect [entryPoint]    → 選定 EntryType hook
        ├── EntryPoint  = EntryType enum（哪個引擎事件）
        ├── FunctionType（效果的「動作種類」：SetValue / AddActivateChoice / SetText…）
        ├── Rank / Priority
        ├── ButtonLabel（LString，互動型才有意義）
        ├── Flags（PerkScriptFlag：FragmentIndex + RunImmediately/ReplaceDefault）
        ├── PerkConditionTabCount（byte，引擎內建 tab 數，不可為 0）
        └── Conditions（PerkCondition 列表，effect-level CTDA）
              └── PerkCondition { RunOnTabIndex, Conditions[] }
```

### record 層次

- **Perk 層條件**（`perk.Conditions`）：決定 Perk 整體是否對持有者生效（例如 `GetLevel >= 30`）。這是 plain `Condition` list，不是 `PerkCondition`。
- **Effect 層條件**（`effect.Conditions`，型別 `PerkCondition`）：決定「此次事件觸發時，這個 effect 是否出手」（例如「目標是門且 crosshair 在門上」）。`PerkCondition` 多了 `RunOnTabIndex`，對應該 entry-point 內建的語意 tab（不同 tab 的條件 run-on target 不同）。
- **PerkConditionTabCount**：entry-point 固有的 tab 數量，引擎用它分配 per-tab 條件陣列，**必須非 0 且與 vanilla 一致**（見第三節）。

---

## 二、Entry-point 種類全表

資料來源：`perkdiag entrypoints` 實測（Skyrim.esm 2026-06-15） + Mutagen `APerkEntryPointEffect.EntryType` enum + `APerkEntryPointEffect.FunctionType` enum 反射。

### 2-1 EntryType：引擎 hook 點（91 個）

下表精選與 ModForge 生成相關度較高的項目，附 vanilla tab-count（從 `Generator.Build.Perks.EntryPoints.cs` EntryPointTabCount 表讀出，unlisted = 預設 2）。

本表整理「2-1 EntryType：引擎 hook 點（91 個）」的逐項記錄。

已抽到 [perk-entry-points-mechanism-entry-types.json](perk-entry-points-mechanism-entry-types.json)（14 列）。

欄位「ID」：保留原表的ID。

欄位「EntryType 名稱」：保留原表的EntryType 名稱。

欄位「Mutagen 類別」：保留原表的Mutagen 類別。

欄位「典型場景」：保留原表的典型場景。

欄位「tab-count」：保留原表的tab-count。

統計：14 筆記錄，5 個欄位。


完整 91 個 EntryType 見 `perkdiag entrypoints` 輸出或 Mutagen `APerkEntryPointEffect.EntryType` enum。

> 注意：`FilterActivation` (74) 是「啟動攔截」的 hook 點，對應 Mutagen 類別 `PerkEntryPointAddActivateChoice`（FunctionType = `AddActivateChoice`）；`SetActivateLabel` (81) 對應 `PerkEntryPointSetText`（FunctionType = `SetText`）。EntryType 名稱（Skyrim 引擎用語）與 Mutagen 類別名稱不同，容易混淆。

### 2-2 FunctionType：effect 的「動作種類」

`APerkEntryPointEffect.FunctionType` enum（用來決定 Mutagen 序列化的具體類別）：

| FunctionType | Mutagen 類別 | 額外欄位 |
|---|---|---|
| SetValue / AddValue / MultiplyValue | `PerkEntryPointModifyValue` | `Value` (float) + `Modification` |
| AddRangeToValue | `PerkEntryPointAddRangeToValue` | `Value` + `Value2` |
| AddActorValueMult | `PerkEntryPointModifyActorValue` | AV + 修改方式 |
| AbsoluteValue / NegativeAbsoluteValue | `PerkEntryPointAbsoluteValue` | 無 |
| AddLeveledList | `PerkEntryPointAddLeveledItem` | `Item`（LVLI ref） |
| **AddActivateChoice** | `PerkEntryPointAddActivateChoice` | `Spell`（SPEL ref，fragment 派發用） |
| **SelectSpell** | `PerkEntryPointSelectSpell` | `Spell` |
| **SelectText** | `PerkEntryPointSelectText` | 文字字串 |
| **SetText** | `PerkEntryPointSetText` | `Text`（LString） |

---

