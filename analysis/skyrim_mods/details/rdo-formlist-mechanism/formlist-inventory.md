# RDO 的 FormList 投放機制 — formlist-inventory

[返回入口](../rdo-formlist-mechanism.md)

## 0. 一句話結論

RDO 的「FormList」與大家直覺想的不一樣：**18 個 FormList 裡，真正主導對話投放的不是 `aaa_RDOVoices*`（目標名單），而是一個排除名單 `aaa_RDOPreventedActorsList`**。936 次 `IsInList` 條件**全部**指向這一個 list，且 923 次是 `==0`（守門：不在黑名單才放行）。目標投放（「這句話該給誰」）幾乎全交給 `GetIsVoiceType`（9245 次）逐句直接鎖嗓音；Voices FormList 只在少數需要「一條 condition 涵蓋整組嗓音」時當捷徑用（210 次）。

---

## 1. FormList 全表（18 個，分群）

dump 第 58953–58970 行列出全部 18 個 FormList 的 `[FormID] EditorID`。下表的「成員型別 / 數量」來自離線解碼（dump 不展開成員）：

### A. 排除名單（PreventedActors，3 個）——投放的真正主力

| FormID | EditorID | 成員 | 說明 |
|--------|----------|------|------|
| `[01EE3A]` | `aaa_RDOPreventedActorsList` | **0 項（空）** | 全 936 次 `IsInList` 唯一指向的 list；ESP 出貨時是空的 |
| `[02E153]` | `aaa_RDOPreventedActorsHatePL` | **0 項（空）** | 在 dialogue/quest condition 中**零引用** |
| `[02E154]` | `aaa_RDOPreventedActorsFriend` | **0 項（空）** | 同上，零引用 |

三個排除名單**出貨時全為空**。`aaa_RDOPreventedActorsList` 被 condition 引用 936 次卻沒有靜態成員——這是刻意的「**空容器 + 執行期/補丁填充**」設計（見 §4）。

### B. 目標名單（Voices，10 個）——成員清一色 VoiceType

| FormID | EditorID | 成員型別×數量 |
|--------|----------|----------------|
| `[056995]` | `aaa_RDOVoicesFemaleList` | VoiceType × 18 |
| `[056996]` | `aaa_RDOVoicesMaleList` | VoiceType × 27 |
| `[11767B]` | `aaa_RDOVoicesMarriageAll` | VoiceType × 26 |
| `[11767C]` | `aaa_RDOVoicesFollowerAll` | VoiceType × 43 |
| `[223F67]` | `aaa_RDOVoicesAll` | VoiceType × 54 |
| `[35E1E6]` | `a_RDO_USKPVendorMiscVoices` | VoiceType × 15 |
| `[400398]` | `aaa_RDOVoicesUnique` | VoiceType × 9（具名 NPC 專屬嗓音）|
| `[A1D4C4]` | `a_RDOVoicesFollowerGenericResponses` | VoiceType × 14 |
| `[B8EEBF]` | `_RDO_OriginalVoicesFollowerAll` | VoiceType × 17 |
| `[CD811F]` | `_RDOVoicesFollowerAllPlusUniques` | VoiceType × 52 |

成員證據（`aaa_RDOVoicesFemaleList` 解碼，節選）：

```
-> VoiceType:FemaleCommoner (013ADE:Skyrim.esm)
-> VoiceType:FemaleEvenToned (013ADD:Skyrim.esm)
-> VoiceType:FemaleNord (013AE7:Skyrim.esm)
-> VoiceType:FemaleOrc (013AEB:Skyrim.esm)
-> VoiceType:FemaleSultry (013AE0:Skyrim.esm)
-> VoiceType:DLC2FemaleDarkElfCommoner (0247E5:Dragonborn.esm)   ← 含 DLC 嗓音
```

`aaa_RDOVoicesUnique` 全部是「具名主角」的專屬 VoiceType（不是泛用嗓音）：

```
-> VoiceType:FemaleUniqueKarliah (01B080:Skyrim.esm)
-> VoiceType:MaleUniqueBrynjolf  (01B07E:Skyrim.esm)
-> VoiceType:DLC1SeranaVoice      (002B6F:Dawnguard.esm)
-> VoiceType:DLC2FemaleUniqueFrea (017F80:Dragonborn.esm)
```

**重點：這 10 個全是 VoiceType 的集合，沒有一個裝 Actor / Faction / Race。** 「目標名單」鎖的維度是「嗓音類別」，不是「特定 NPC」。

### C. 其他用途（5 個）——與對話投放無關

| FormID | EditorID | 成員 | 用途 |
|--------|----------|------|------|
| `[A03FB0]` | `a_CustomSpellList` | Spell × 57 | 法術清單（如 `Flames 012FCD`、`Frostbite 02B96B`），供「NPC 是否會某類法術」等判斷 |
| `[03EF8C]` | `_RDOEncOrcHuntersFemale` | Npc × 5（RDO 自製 `_RDOEncOrcHunter0xF`）| 自製遭遇 NPC 群組 |
| `[DC60C0]` | `_RDOLeveledActorsWEAdventurerSS` | Npc × 2（`_WEAdventurerSpellsword*F`）| 自製冒險者 actor |
| `[F14397]` | `_RDOICAOWERoad02Noble` | **Package × 1** | AI Package 容器（非 actor/voice）|
| `[FB12EA]` | `_RDOEncHunters` | Npc × 1（`_RDOEncHunterNordM`）| 自製遭遇 NPC |

C 群是 RDO 自帶的小型遭遇/演出資源，與「大規模對話投放」這個主題無關，列出只為完整。

---

