# 技術差異：MCO／ADXP vs BFCO

← [mco-to-bfco-conversion](../mco-to-bfco-conversion.md)

## 1. 技術差異：MCO／ADXP vs BFCO

### 1.1 共用的部分（不變）

| 層 | 元件 | MCO | BFCO | 是否需要改 |
|---|---|---|---|---|
| 0 骨架 | XPMSSE | 需要 | 需要 | 否 |
| 1 behavior 引擎 | Pandora／Nemesis | 需要（[Attack - MCO 前置](https://www.nexusmods.com/skyrimspecialedition/mods/175044)） | 需要 | 否（但兩者**不可同時裝**） |
| 2 資料注入 | [Payload Interpreter](../payload-interpreter.md) | 硬前置 | 硬前置 | 否 |
| 2 位移 | [AMR](../animation-motion-revolution.md) | 硬前置 | 硬前置 | **否——`animmotion`／`animrotation` 註釋與框架無關** |
| 3 動畫選擇 | [OAR](../../oar-replacer-guide.md) | 硬前置 | 硬前置 | 條件本身通常不用改（見 §2.3） |
| 4 NPC AI | [SCAR](../scar.md) | 可選 | 可選（BFCO 另有自帶 AI） | 否 |

證據：BFCO 的 Nexus requirements 與 Attack - MCO 的 requirements 兩邊都列 AMR／OAR／PIE／Pandora-or-Nemesis
（`housecarl_nexus_mod 117052` 與 `175044` 輸出）。

### 1.2 真正不同的四件事

**(a) 動畫檔名 handle（最本質的差異）**

BFCO 的 behavior graph 綁定的是 `BFCO_*` 檔名；MCO 綁 `mco_*`。這是**唯一一定要動的東西**。

| MCO | BFCO |
|---|---|
| `mco_attack1..N.hkx` | `BFCO_Attack1..20.hkx` |
| `mco_powerattack1..N.hkx` | `BFCO_PowerAttack1..20.hkx` |
| `mco_weaponart.hkx` | `BFCO_PowerAttackComb.hkx` |
| `mco_sprintattack.hkx` | `BFCO_SprintAttack.hkx` |
| `mco_sprintpowerattack.hkx` | `BFCO_SprintAttackPower.hkx` |
| `mco_powerattackloop*.hkx` | `BFCO_PowerAttackLoop*.hkx` |
| `mco_powerattackoutro*.hkx` | `BFCO_PowerAttackOutro*.hkx` |

來源：converter 頁的 "What animations will be renamed?"（mod 119926，全版本適用）。
BFCO 側的完整動畫表見 [`raws/BFCO - Attack Behavior Framework (SSE AE VR).txt`](../../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt) 第 40–75 行。
本機 BFCO 3.100.5 出貨的 224 個 `.hkx` 實檔命名（`BFCO_Attack1.hkx`…`BFCO_SwimAttackPower.HKX`，大小寫混用）已核對。

**(b) annotation：BFCO 原生看得懂 MCO 的**

- BFCO 官方頁：`Furthermore, MCO annotations can also work with BFCO.`
  （[`raws/BFCO - ….txt:110`](../../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt)）
- 佐證：BFCO changelog v3.6.0（2026-02-23）`Fix the issue where MCO annotations do not take effect during
  sprinting / directional heavy attacks.`；v3.6.1（2026-02-26）`Fixed the MCO annotations issue agin.`
  ——修的是既有功能，不是新增。
- BFCO v3.100 中文 changelog 更明講：`BFCO_AttackSpeed 会在每一个攻击动画结束时自动重置为 1 …
  MCO_AttackSpeed 保持与 mco 规则相同，只在退出攻击状态时自动重置`——即 BFCO **同時實作兩套變數、兩套重置規則**。

等價對照（converter ≤ 1.1.8 的轉換表，來源同 mod 119926 頁）：

| MCO annotation | BFCO annotation |
|---|---|
| `PIE.@SGVI\|MCO_nextattack\|N` | `BFCO_NextIsAttackN` |
| `PIE.@SGVI\|MCO_nextpowerattack\|N` | `BFCO_NextIsPowerAttackN` |
| `MCO_WinOpen` | `BFCO_NextWinStart` |
| `MCO_PowerWinOpen` | `BFCO_NextPowerWinStart` |
| `MCO_WinClose` / `MCO_PowerWinClose` | `BFCO_DIY_EndLoop` |
| `MCO_Recovery` | `BFCO_DIY_recovery` |
| `PIE.@SGVF\|MCO_AttackSpeed\|x` | `PIE.@SGVF\|BFCO_AttackSpeed\|x` |

**converter v1.2.0（2025-01-01）起這張表不再需要**：changelog v1.2.1 寫 `Dont require hkanno64.exe anymore`，
且頁面把 annotation 轉換段標成 "For converter <= 1.1.8 only"，新流程只剩 `Select Folder` → `Run` → `Filename Changed.mco->bfco.`。
（**推測**：這是因為 BFCO 端已原生解讀 MCO annotation；官方沒有明說「因此」，但兩邊時間線與上述 changelog 一致。）

**(c) attack chain 變數：兩套語意不同的狀態**

BFCO 出貨的 [BDI](../behavior-data-injector.md) 變數（本機 `BFCO_BDI.json` 實檔核對）：

```json
[
  {"projectPath":"Actors","type":"kBool","name":"BFCO_ComboLocked","value":false},
  {"projectPath":"Actors","type":"kInt","name":"BFCO_LastAttack","value":0},
  {"projectPath":"Actors","type":"kInt","name":"BFCO_NextNormal","value":0},
  {"projectPath":"Actors","type":"kInt","name":"BFCO_NextPower","value":0}
]
```

`BFCO_iAttackVariants`（＋ `A`–`E`）**不在** BDI config 裡，它是 **behavior graph 的整數變數**，v3.2 起提供，
v3.100 擴充成六個（[`raws/BFCO - ….txt:182`](../../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt) 與 v3.100 changelog）。
用途是「動畫用 `PIE.@SGVI|BFCO_iAttackVariants|1` 設值 → OAR 用 `CompareValues` 挑下一段動畫資料夾」。

**MCO 沒有這個機制。** MCO 的分支只有 `MCO_nextattack|N`（指定下一段編號）。所以：

- 轉換後**既有連段照舊能跑**（`MCO_nextattack` 直接被 BFCO 吃）。
- **但 BFCO 的變體分支（`BFCO_iAttackVariants` + OAR `CompareValues`）是轉換拿不到的新能力**——
  要用得回頭改 hkx annotation ＋ 新增 OAR 資料夾。這是「轉換」與「重製」的分界線。

**(d) 攻速與 perk 相容性（gameplay 語意，不是檔案問題）**

- MCO **DXP 版**改 behavior 讓攻速由動畫決定 → vanilla／perk／附魔的攻速修飾**失效**，需
  [MCO-DXP and BFCO Attack Speed Fix, mod 160188](https://www.nexusmods.com/skyrimspecialedition/mods/160188)
  或 `Ultimate MCO and BFCO Attack Speed Fix SKSE` 之類的 workaround。
- BFCO 主打**vanilla 攻速 + 方向重擊**，因此宣稱相容所有 perk 大修（Vokrii／Ordinator…）
  ——這正是它對現役 Vokriinator Black 基線的價值。
- ⚠️ **但 BFCO 的 FOMOD 有 `WeapSpeedStyle` 選項**，其中 `B-Only BFCOspeed (MCO like)` 會切回 MCO 式攻速。
  來源：mod 160188 的 requirements 註記（`Only with FOMOD option "WeapSpeedStyle, B-Only BFCOspeed (MCO like)"`）。
  **一套為 MCO 節奏調過 `MCO_AttackSpeed` 的 moveset，轉到 vanilla-speed 的 BFCO 底下手感會變**——
  這是轉換最容易被低估的一項，且**只能靠實機驗**。

---

