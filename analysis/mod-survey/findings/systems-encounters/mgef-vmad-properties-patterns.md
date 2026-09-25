# ActiveEffect property 表 + 設計模式 + 評估

← [mgef-vmad](mgef-vmad.md)

## 三、ActiveEffect 內建 property 表

這些是 `ActiveMagicEffect` 提供給子腳本的「隱性 property」，不需要在 VMAD 的 `Properties[]` 中宣告——由引擎在 effect 開始時自動注入：

| Property 名 | 型別 | 說明 |
|---|---|---|
| `Self` | `ActiveMagicEffect` | 指向自身（此 effect 實例） |
| `GetCasterActor()` | method → `Actor` | 施法者（注：是 method，非 property） |
| `GetTargetActor()` | method → `Actor` | 目標（注：是 method，非 property） |

`OnEffectStart(Actor akTarget, Actor akCaster)` 直接把 caster/target 以參數傳入，所以一般不需要 property binding；caster/target 只有在 `OnEffectStart` 以外的地方（如腳本的其他 function）需要透過 `GetCasterActor()` 取得。

從 Arrowblock 的 `Blocking.psc` 可見，5 個 property 全是手動宣告並在 VMAD 中綁定的業務型 property（存放 FX spell ref、sound ref 等），並非引擎自動注入。**使用者需要自己在 spec `properties[]` 裡宣告並在 VMAD 中綁定所有業務 property**——引擎只自動提供 caster/target 事件參數與 `Self`。

典型業務 property 範例（來自 Arrowblock `Blocking.psc`）：

```papyrus
Spell Property BlockingmodFX Auto    ; → SPEL ref，施放 FX
Sound Property BlockHitSound Auto    ; → SNDR ref，播音效
Float Property StaminaCost Auto      ; → float 常數
Actor Property pPlayer Auto          ; → 玩家 ref（by unique actor）
```

---

## 四、設計模式：Script MGEF 的常見 pattern

### Pattern A：SPEL + Ability MGEF + Script（常駐被動反應）

```
SPEL (type=Ability, castType=ConstantEffect, targetType=Self)
  effect → MGEF (archetype=Script, castType=ConstantEffect, targetType=Self)
              VMAD → MyScript (extends ActiveMagicEffect)
                        OnHit / OnEffectStart / ...
```

用途：把腳本常駐掛在 actor 上，攔截戰鬥事件。PERK 的 `effect[ability]` 給 SPEL，SPEL 帶 MGEF，MGEF 帶腳本。Arrowblock 的 `Blocking.psc` 是此模式的教科書範例。

### Pattern B：OnEffectStart Gate 模式

```papyrus
Event OnEffectStart(Actor akTarget, Actor akCaster)
    ; 一次性初始化 + 條件檢查 gate
    If akTarget.HasKeyword(MyKeyword) && akCaster != akTarget
        ; 觸發主邏輯
    EndIf
EndEvent
```

OnEffectStart 用於 FireAndForget 型效果的「一次性觸發」；OnEffectFinish 用於清理。Gate 條件判斷通常在 OnEffectStart 內做，避免在非目標情況下執行開銷大的邏輯。

### Pattern C：三層載具鏈（PERK → SPEL → MGEF → Script）

```
PERK
  effect[ability] → SPEL (Ability/ConstantEffect/Self)
                      effect → MGEF (Script/ConstantEffect/Self)
                                  VMAD → Script
  effect[entryPoint] → ... （純 record 層引擎邏輯，與 Script 並行）
```

此三層鏈讓 PERK 同時驅動「引擎層行為」（entry-point 改數值）與「腳本層行為」（Papyrus 事件），兩者共同演一個效果。Arrowblock 正是此模式：entry-point `ModIncomingDamage Set 0` 歸零傷害，Script MGEF 的 `ClearExtraArrows()` 拔箭。

---

## 五、對 ModForge 的評估

本表整理「五、對 ModForge 的評估」的逐項記錄。

已抽到 [mgef-vmad-properties-patterns-modforge-capabilities.json](mgef-vmad-properties-patterns-modforge-capabilities.json)（6 列）。

欄位「能力」：保留原表的能力。

欄位「狀態」：保留原表的狀態。

欄位「根據」：保留原表的根據。

統計：6 筆記錄，3 個欄位。


**總結**：MGEF VMAD 在 ModForge 屬於「可生成但需繞路」的 partial 狀態。通用 `scripts[]` 頂層 attach 已能把腳本掛到 MGEF，技術上不缺功能；真正缺的是 spec 的 `magicEffects[i].scripts[]` inline 欄位（讓 MGEF 的腳本宣告貼近 record 本身，更自然），以及對應的文件說明。
