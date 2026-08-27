# MCO／ADXP moveset → BFCO 轉換

← [action-system 中樞](../README.md)｜相關：[BFCO](bfco.md)、[SCAR](scar.md)、[moveset 實例庫](movesets-examples.md)、[Payload Interpreter](payload-interpreter.md)、[OAR 指南](../oar-replacer-guide.md)

> **落點＝五層堆疊的第 4 層（招式框架）內部的框架遷移。** 第 0–3 層（XPMSSE／Pandora／BDI・PIE・AMR／OAR）
> 在 MCO 與 BFCO 底下**完全共用**，所以這不是「換一套動作系統」，而是**同一批 `.hkx` 換一個 attack framework 的 handle**。
>
> **一句話結論**：在現行版本（BFCO ≥ 3.3、converter ≥ 1.2.0）下，**MCO moveset 轉 BFCO 的必要動作只有「批次改檔名」**——
> annotation 不必改寫、OAR 條件不必改、不必重跑 Pandora／Nemesis。有現成工具
> （[MCO to BFCO Converter, mod 119926](https://www.nexusmods.com/skyrimspecialedition/mods/119926)），
> 而且 BFCO 官方頁明載「MCO annotations can also work with BFCO」。
>
> **授權已於 2026-08-27 逐字查證**（§4.1）：三筆爭議 moveset 的 `Conversion permission` 只禁「移植到別的遊戲」，
> **不涵蓋同遊戲內的框架轉換** → **私人本機轉換無障礙、再發布一律不可**。
> 所以剩下的真門檻只有兩個：**attack-speed 手感偏移**（要實機驗）與 **NPC 路／玩家路必須分開規劃**（§4.2）。

---

## 1. 技術差異：MCO／ADXP vs BFCO

### 1.1 共用的部分（不變）

| 層 | 元件 | MCO | BFCO | 是否需要改 |
|---|---|---|---|---|
| 0 骨架 | XPMSSE | 需要 | 需要 | 否 |
| 1 behavior 引擎 | Pandora／Nemesis | 需要（[Attack - MCO 前置](https://www.nexusmods.com/skyrimspecialedition/mods/175044)） | 需要 | 否（但兩者**不可同時裝**） |
| 2 資料注入 | [Payload Interpreter](payload-interpreter.md) | 硬前置 | 硬前置 | 否 |
| 2 位移 | [AMR](animation-motion-revolution.md) | 硬前置 | 硬前置 | **否——`animmotion`／`animrotation` 註釋與框架無關** |
| 3 動畫選擇 | [OAR](../oar-replacer-guide.md) | 硬前置 | 硬前置 | 條件本身通常不用改（見 §2.3） |
| 4 NPC AI | [SCAR](scar.md) | 可選 | 可選（BFCO 另有自帶 AI） | 否 |

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
BFCO 側的完整動畫表見 [`raws/BFCO - Attack Behavior Framework (SSE AE VR).txt`](../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt) 第 40–75 行。
本機 BFCO 3.100.5 出貨的 224 個 `.hkx` 實檔命名（`BFCO_Attack1.hkx`…`BFCO_SwimAttackPower.HKX`，大小寫混用）已核對。

**(b) annotation：BFCO 原生看得懂 MCO 的**

- BFCO 官方頁：`Furthermore, MCO annotations can also work with BFCO.`
  （[`raws/BFCO - ….txt:110`](../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt)）
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

BFCO 出貨的 [BDI](behavior-data-injector.md) 變數（本機 `BFCO_BDI.json` 實檔核對）：

```json
[
  {"projectPath":"Actors","type":"kBool","name":"BFCO_ComboLocked","value":false},
  {"projectPath":"Actors","type":"kInt","name":"BFCO_LastAttack","value":0},
  {"projectPath":"Actors","type":"kInt","name":"BFCO_NextNormal","value":0},
  {"projectPath":"Actors","type":"kInt","name":"BFCO_NextPower","value":0}
]
```

`BFCO_iAttackVariants`（＋ `A`–`E`）**不在** BDI config 裡，它是 **behavior graph 的整數變數**，v3.2 起提供，
v3.100 擴充成六個（[`raws/BFCO - ….txt:182`](../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt) 與 v3.100 changelog）。
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

## 2. 轉換實際要動什麼（可執行步驟骨架）

### 2.0 前提檢查

1. BFCO ≥ 3.3（`mco_powerattackloop/outro` 才有對應 handle）。現役 3.100.5 ✅。
2. **MCO 與 BFCO 不可共存**（BFCO 頁 Incompatible with 明列 `Skysa/ABR/MCO`，
   [`raws/BFCO - ….txt:259`](../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt)）。轉換是**單向遷移**，不是相容層。
3. 原 moveset 若是 DAR-only，確認 OAR 已裝（OAR 原生讀 `DynamicAnimationReplacer\_CustomConditions\<priority>\`
   並轉成 "Legacy" replacer-mod，見 [`oar-replacer-guide-overview-planning-folders.md:74`](../oar-replacer-guide-overview-planning-folders.md)）。

### 2.1 hkx annotation：**不用改寫**（現行版本）

- 現行 converter（≥ 1.2.0）不動 annotation，只改檔名。
- 只有這兩種情況要碰 hkanno64：
  - 想加 BFCO 專屬能力（`BFCO_iAttackVariants`、`BFCO_ChargeStage*`、`BFCO_ForbidRotationStart`、
    `BFCO_UnequipFaster`）；
  - 遇到 BFCO 沒吃到的 MCO 註釋殘留（**目前查不到具體清單，需要實機逐招驗**）。

### 2.2 檔名：唯一必做的一步

工具是 Windows 的 pyinstaller `.exe`（`mco2bfco.exe.DELETEME`，要先改副檔名），作者另有上傳 `source code`（`.py`）。
**本機是 Linux**，所以：

- 走 Proton／wine 跑 `.exe`；或
- 跑作者的 `.py` 原始碼（≥ 1.2.0 已不需要 `hkanno64.exe`）；或
- **直接自己改檔名**——因為 ≥ 1.2.0 的行為就只是遞迴重新命名，等價於：

```sh
# 骨架，未實跑；轉換前務必先備份整包
find <moveset-root> -type f -iname 'mco_*.hkx' | while read -r f; do
  d=$(dirname "$f"); b=$(basename "$f")
  n=$(printf '%s' "$b" \
    | sed -E 's/^[Mm][Cc][Oo]_attack/BFCO_Attack/;             s/^[Mm][Cc][Oo]_powerattackloop/BFCO_PowerAttackLoop/;
              s/^[Mm][Cc][Oo]_powerattackoutro/BFCO_PowerAttackOutro/; s/^[Mm][Cc][Oo]_powerattack/BFCO_PowerAttack/;
              s/^[Mm][Cc][Oo]_weaponart/BFCO_PowerAttackComb/;  s/^[Mm][Cc][Oo]_sprintpowerattack/BFCO_SprintAttackPower/;
              s/^[Mm][Cc][Oo]_sprintattack/BFCO_SprintAttack/')
  [ "$b" != "$n" ] && mv -n "$f" "$d/$n"
done
```

> ⚠️ `sed` 的順序有講究：`powerattackloop`／`powerattackoutro`／`sprintpowerattack` 必須排在
> `powerattack`／`sprintattack` **前面**，否則會被短的規則先吃掉。上面骨架已排好，但**未實跑驗證**。
> 官方工具的 regex 在 v1.1.4／1.1.6／1.1.7／1.2.2 修過四次同類問題（converter changelog），
> 自己刻等於重蹈那些坑——**建議還是走官方工具，自刻只當離線備案**。

### 2.3 OAR config：**通常不用改**

- moveset 的 OAR submod 條件幾乎都是裝備／種族／角色條件（`IsEquippedType`、`IsActorBase`、`IsRace`、`Random`…），
  與 attack framework 無關——見 [movesets-examples.md](movesets-examples.md) 的實檔拆解。
- OAR 是**按被替換動畫的檔案路徑**做替換，所以檔名一改，OAR 自動就替換到 `BFCO_*` handle 上。
  本機 BFCO 3.100.5 自己出貨的 16 個 OAR submod（`OpenAnimationReplacer/BFCO/1hm-sword-base/` 等）
  裡放的正是 `BFCO_*.hkx`，證實這條路徑。
- **要改的例外**：
  - 條件裡出現 `MCO_*` graph variable 的 `CompareValues`（少見，但存在）；
  - 想升級成 BFCO 變體分支（新增資料夾 + `BFCO_iAttackVariants` 條件，語法見 [bfco.md](bfco.md)）。

### 2.4 資料夾／檔案結構：不變

MCO 與 BFCO 的 moveset 都放
`meshes\actors\character\animations\OpenAnimationReplacer\<Mod>\<Submod>\`（或 DAR 的 `_CustomConditions\<N>\`）。
**目錄佈局零改動**，只有裡面的檔名變。

### 2.5 Pandora／Nemesis：**純 moveset 不用重跑**

- moveset 是 runtime 的 OAR 資產，不進 behavior graph → 不觸發重生成。
  同類佐證：mod 160188 的頁面 `This mod is script-free. NO need to rerun Nemesis after installing this.`
- **要重跑的是「換框架」那一步**：移除 MCO／安裝 BFCO 之後必須重跑一次。
- ⚠️ **BFCO 3.100.7（2026-08-23）起 FOMOD 不再附預生 behavior**：
  `Pre-generated behaviors are no longer installed to prevent file overwrites. Running Nemesis & Pandora is now required`
  ——現役停在 3.100.5（仍附預生 behavior），**升到 3.100.7 就變成硬性要重跑 Pandora**。

### 2.6 現役基線的實測狀態（2026-08-27，唯讀核對）

| 項 | 狀態 | 證據 |
|---|---|---|
| BFCO | 已裝 3.100.5 | `modlist.txt:133` |
| Pandora output 是否含 bfco patch | **是** | `Pandora Output/Pandora_Engine/ActiveMods.json` 有 `{"code":"bfco","active":true,"priority":12}`；`Engine.log`：`INFO : Pandora Mod 12 : BFCO - Attack Behavior - v.1.0.0` |
| PIE 的 `evfmgo` patch | 已套 | 同 `ActiveMods.json`，priority 13 |
| MCO／ADXP | **未安裝** | 340 個 mod 資料夾全掃無 |
| SCAR | **未安裝** | 同上；`ActiveMods.json` 無 `scar` |
| 任何 `mco_*.hkx` | **本機零檔** | `find <mods> -iname 'mco_*.hkx'` 無結果 |
| 第三方 moveset | **零套** | OAR/DAR 下有 `.hkx` 的只有 BFCO 本體、Pandora Output、Precision、SIGMA Magic、Glad You're Here |

→ **現在的處境是「有框架、沒內容」**：BFCO 裝好、Pandora 也正確 patch 了，但一套 moveset 都沒有。
所以本題不是「修既有東西」，而是「要不要開始拿 MCO 生態的內容來填 BFCO」。

---

## 3. 現成工具與社群做法

### 3.1 官方／半官方支援

| 事實 | 版本／時間 | 來源 |
|---|---|---|
| BFCO 頁直接推薦 converter：`people can easily convert the MCO hkx to BFCO by using MCO To BFCO Converter` | 現行頁 | [`raws/BFCO - ….txt:259`](../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt) |
| BFCO 原生吃 MCO annotation | 頁面明載；3.6.0／3.6.1 有相關 bugfix | mod 117052 頁 + changelog |
| BFCO 保留 `MCO_AttackSpeed` 的 MCO 語意 | v3.100（2026-04-18） | mod 117052 changelog |
| `mco_powerattackloop/outro` 有對應 handle | BFCO ≥ 3.3 | converter changelog v1.2.1 |

### 3.2 轉換工具

**[MCO to BFCO Converter, mod 119926](https://www.nexusmods.com/skyrimspecialedition/mods/119926)**
（Sukezzzzz，v1.2.2 / 2025-01-02，1,495 endorsements、44,771 downloads）

- 功能：批次改檔名；批次 dump／update annotation；(≤1.1.8) 批次改 annotation。
- 前置：BFCO（軟性）、hkanno64 ≤ 1.1.8（只有舊版需要）。
- 作者自己標註：`Don't install this mod in your MO2. Find a clean place and download this mod.`
  ——它是**離線工具**，不是 mod。且因 pyinstaller 打包會被防毒誤判，作者加了 `.DELETEME` 副檔名並另傳 `.py` 原始碼。
- **反向工具也存在**（品質不明）：`bfco to mco (bat tool)`, mod 160624（0 endorsements、3 downloads）。

### 3.3 社群實務：轉換已是常態

- **雙框架出貨**：[Dragons Dogma 2 Fighter Sword and Shield Moveset - MCO and BFCO, mod 123708](https://www.nexusmods.com/skyrimspecialedition/mods/123708)
  這類「同一批動畫、FOMOD 選框架」的頁已經很普遍。
- **第三方轉換頁（帶授權）**：
  - [BFCO I BDO Guardian Awakening, mod 135503](https://www.nexusmods.com/skyrimspecialedition/mods/135503)
    ——`BFCO conversion of BDO Guardian Awakening by krembrule. **Published with permission.**`
  - [BFCO Dragon Age Staff Moveset, mod 184100](https://www.nexusmods.com/skyrimspecialedition/mods/184100)
    ——只出「轉換層」，把原 MCO mod 列為 **required**，自己不重發原始資產。**這是規避授權問題的標準做法。**
- **大型 NPC 整合**：[Diverse NPC Movesets, mod 141893](https://www.nexusmods.com/skyrimspecialedition/mods/141893)
  （Rei，v3.0.0 / 2026-02-24）把 `Ultimate NPC Attack Variety Guide` 整批從 DAR 轉 OAR，
  FOMOD 裡 `Choose between MCO or BFCO framework`，並宣稱 `All original authors gave explicit permission for this conversion.`
  硬前置：**SCAR**（＋ SCAR AE Support）、OCF、OAR。

### 3.4 查不到的

- **BFCO 官方沒有出「MCO 相容模式」開關**——相容是靠 annotation 層，不是模式切換。
- **查不到任何官方或社群整理的「BFCO 吃不下的 MCO 註釋清單」。** 只查到零星使用者回報
  （例：sprint attack 播得出來但不接普攻的鏈接問題），無法據此下結論，需實機驗。

---

## 4. 轉不了／要小心的邊界條件

| # | 邊界 | 判定 | 依據 |
|---|---|---|---|
| B1 | **授權** | **私人本機轉換：不阻斷**（已查證）；**再發布轉好的檔案：硬阻斷** | 見 §4.1，已由調度者用瀏覽器逐字查證 |
| B2 | **MCO-Updated 專屬招式**（`MCO Left Attack1..10`、`MCO Normal Weapon Art`） | **無對應 handle，轉不了** | [Attack - MCO Updated, mod 181779](https://www.nexusmods.com/skyrimspecialedition/mods/181779) 是加在 MCO 之上的擴充；BFCO 只有 `BFCO_SpecialAttack`／`BFCO_PowerAttackComb` |
| B3 | **DAR-only 舊包** | **可轉**（OAR 讀 DAR legacy），但條件表達力受限 | `oar-replacer-guide-overview-planning-folders.md:74`。DAR 的 `_conditions.txt` DSL **沒有 graph-variable 條件**，要用 `BFCO_iAttackVariants` 分支必須先把條件搬成 OAR JSON |
| B4 | **依賴 SCAR 的 NPC 連段** | **不阻斷，但會降級** | BFCO：`Animation without SCAR-event is managed by bfcoAI, while animation with SCAR-event is still managed by scarAI`（[`raws/BFCO - ….txt:245`](../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt)）。**現役沒裝 SCAR** → SCAR-annotated moveset 由 BFCO 自帶 AI 接管，連段品質較低。⚠️ 2026-08-27 使用者已放行引入 SCAR／SCAR AE Support／OCF，這條不再是選型阻礙，但仍是**新增三個前置**的成本 |
| B5 | **`SCAR_*Dummy.hkx` 標記動畫在沒有 SCAR 時的行為** | **未知，需實機驗**（推測：它替換的是 ready-idle，沒有 SCAR 時可能留下錯誤 idle pose） | [movesets-examples.md](movesets-examples.md) 記錄實檔有 `SCAR_1hmReadyDummy.hkx`；查不到「無 SCAR 時該檔行為」的官方說明 |
| B6 | **root motion／AMR 位移** | **不阻斷** | `animmotion`／`animrotation` 是 AMR 的註釋，兩框架都硬前置 AMR，且註釋與 framework 無關（[animation-motion-revolution.md](animation-motion-revolution.md)）。⚠️ AMR 生效需 behavior 設 `bAllowRotation`／`bAnimationDriven`；BFCO 的攻擊狀態是否全部滿足——**未驗證，推測滿足**（BFCO 自帶動畫本身就依賴位移） |
| B7 | **attack speed 手感偏移** | **不阻斷，但一定要重驗** | §1.2(d)。為 MCO DXP 節奏調過的 moveset，在 vanilla-speed BFCO 下節奏會變 |
| B8 | **moveset 自帶 esp／Nemesis patch**（例：攻速 esp、weapon-keyword esp） | **轉換工具管不到**，要逐件人工判 | converter 只處理 `.hkx` 檔名 |
| B9 | **Troll／Draugr 這類「生物 MCO」包** | **不是 moveset 轉換問題** | 它們是 SPID／AI／race overhaul，動畫只是其中一層；BFCO 的 NPC 連段只涵蓋人形 behavior project |
| B10 | **MCO 與 BFCO 不可共存** | **硬性** | [`raws/BFCO - ….txt:259`](../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt)。不能「留 MCO 當 fallback」 |


### 4.1 授權：已逐字查證（2026-08-27）

> 查證方式與逐字原文在 [`agentctl/logs/nexus-permissions-mco-movesets-2026-08-27.md`](../../../../agentctl/logs/nexus-permissions-mco-movesets-2026-08-27.md)
> （調度者用 Chrome 擴充讀 mod 頁的 `Permissions and credits` 折疊區；houseCARL 與 keyless GraphQL 都沒有這個欄位）。

**94715（Leviathan II Greatsword MCO）／110676（Vanargand II Unarmed MCO）／80085（DD Daggers MCO）三頁四欄逐字相同：**

| 欄 | 原文 |
|---|---|
| Upload | `You are not allowed to upload this file to other sites under any circumstances` |
| Modification | `You must get permission from me before you are allowed to modify my files to improve it` |
| Conversion | `You are not allowed to convert this file to work on other games under any circumstances` |
| Asset use | `You must get permission from me before you are allowed to use any of the assets in this file` |

**判讀（這是判讀，不是原文）**：

- ⚠️ **`Conversion permission` 那條擋不住本案。** 原文限定 `to work on other games`——它講的是**移植到別的遊戲**，
  不是 MCO→BFCO 這種**同一款遊戲內的框架轉換**。任何把這欄當成「不准轉 BFCO」的依據都是誤讀。
- **私人本機轉換：三筆都沒有障礙。** Nexus 這組欄位管的是再發布，不管使用者在自己 load order 裡改檔。
- **再發布轉好的檔案：三筆都禁止。** Upload 欄是 `under any circumstances`，連問都不必問。
  → 若日後真要做，只能走社群慣例：**只發「轉換層」、把原 mod 列 required、不重發原始資產**（mod 184100 的做法）。

### 4.2 ⚠️ NPC 分發 ≠ 玩家 moveset（最容易搞錯的一點）

[Diverse NPC Movesets 141893](https://www.nexusmods.com/skyrimspecialedition/mods/141893) 的
`All original authors gave explicit permission for this conversion.` **已查證屬實**，
FOMOD 也確實 `Choose between MCO or BFCO framework`，catalog 裡有本輪爭議的四筆：

| 候選 | 141893 的位置 |
|---|---|
| Leviathan II Greatsword | priority 20000，Companions & Dawnguard |
| Vanargand II Unarmed | priority 19000，Bretons／Imperials、Wood Elves、High Elves |
| BDO Guardian | priority 29000，Nords & Orcs，War Axe |
| Dragons Dogma Fighter | priority 14000，Bretons／Imperials、High Elves，Sword and Shield |
| **DD Daggers（80085）** | **不在 catalog 裡** |

**但 141893 是按種族／派系把動畫發給 NPC 的分發包，不是玩家 moveset。**
裝了它，**玩家不會多出任何招式**——它的 OAR 條件是種族／派系導向的 NPC 分發。

⇒ **兩條路必須分開規劃，不能混為一談：**

| 路 | 對象 | 做法 | 授權狀態 | 代價 |
|---|---|---|---|---|
| **NPC 路** | NPC／敵人 | 直接裝 141893，FOMOD 選 BFCO framework | ✅ 原作者明示授權，現成品 | 新增硬前置 SCAR(72014) + SCAR AE Support(77285) + OCF(81469)；選配 Knockback SKSE(171277)、SCAR NPC Combo Limitation Patch(162497)。使用者 2026-08-27 已放行 |
| **玩家路** | 玩家角色 | 自己買原 MCO moveset → 批次改檔名（§2.2） | ✅ 私人可；❌ 不得再發布 | 每套要自轉 + 實機驗收（§5.4） |

> 141893 自己的授權是全鎖（不得修改／取用素材／上傳），但那隻管再發布，不影響安裝使用。

---

---

## 5. 成本判定：對現役 stack 值不值得做

### 5.1 成本結構

| 項 | 成本 |
|---|---|
| 工具取得 | 一次性（mod 119926，離線工具，不進 MO2） |
| Linux 執行 | Proton／wine 跑 `.exe`，或跑作者 `.py`，或自刻 rename（§2.2）。**低** |
| 每套 moveset 的機械成本 | **一次批次改檔名**，分鐘級 |
| Pandora 重跑 | **純 moveset 不需要**；只有換框架／升 BFCO 到 3.100.7 才要 |
| OAR config 改寫 | 通常 0 |
| **實機驗收** | **這才是真成本**：每套要驗連段是否接得上、攻速手感、NPC 行為、hitbox（Precision 已在役） |
| 授權判斷 | **本輪三筆已查完**（§4.1）；新增候選才要再看一次 mod 頁 Permissions（需瀏覽器，歸調度者） |

### 5.2 判定

**值得做。** 先分 NPC／玩家兩條路（§4.2），再在每條路裡分 A／B 類：

| | **NPC 路** | **玩家路** |
|---|---|---|
| 主要手段 | 直接裝 [141893](https://www.nexusmods.com/skyrimspecialedition/mods/141893)，FOMOD 選 BFCO framework | 逐套自轉（§2.2） |
| 轉換成本 | **零**（現成品） | 每套分鐘級 |
| 授權 | ✅ 原作者明示授權 | ✅ 私人可、❌ 不得再發布（§4.1） |
| 額外前置 | SCAR + SCAR AE Support + OCF（**使用者 2026-08-27 已放行**） | 無 |
| 真成本 | 實機驗收 + 一批 NPC 行為要看 | 實機驗收（§5.4） |

每條路裡再分：

- **A 類——已有現成 BFCO 版／雙框架版**：直接取，**零轉換成本**，應優先。
  例：mod 135503（BDO Guardian Awakening）、mod 123708（DD2 Fighter）、mod 184100（DA Staff）。
- **B 類——只有 MCO 版、要自己轉**：機械成本低，但**驗收成本與 A 類相同**。
  只有在「那套動畫不可替代」時才值得。例：mod 80085（DD Daggers）。

**仍然不值得做的**：為了單一展示片新增框架依賴。使用者雖已放行 SCAR／OCF，
但那是**為了 141893 這個整包**放行的；不要把它當成「以後任何 mod 要什麼前置都可以加」。

### 5.3 `animation-combat.md` 逐筆影響

> **只讀引用。`modpack-design/` 的寫入權在 `opus-content` 手上。** 下表是本線給出的技術依據與建議，不是判定。

| 行 | 候選 | 現行結論 | 本線技術依據 | 建議 |
|---|---|---|---|---|
| `:56` | **BDO Guardian** | `NO-GO-MCO-ONLY` | **前提不成立**：[BFCO I BDO Guardian Awakening, mod 135503](https://www.nexusmods.com/skyrimspecialedition/mods/135503) 是**帶授權的現成 BFCO 版**（189 endorsements / 41,973 DL）；War Axe 版另收在 Diverse NPC Movesets 的 BFCO 分支（priority 29000） | **重新開放**（改判理由：不再是 MCO-only） |
| `:56` | **DD Fighter** | `NO-GO-MCO-ONLY` | **前提不成立**：[Dragons Dogma 2 Fighter Sword and Shield Moveset - MCO and BFCO, mod 123708](https://www.nexusmods.com/skyrimspecialedition/mods/123708) 官方就出雙框架。⚠️ 若審的是舊的 [mod 77366 `ADXP I MCO Dragons Dogma Fighter`](https://www.nexusmods.com/skyrimspecialedition/mods/77366)，那個仍是 MCO-only，但收在 Diverse NPC Movesets BFCO 分支（14000） | **重新開放**，並先釐清審的是哪一個 mod id |
| `:56` | **DA Staff** | `NO-GO-MCO-ONLY` | **前提不成立**：[BFCO Dragon Age Staff Moveset, mod 184100](https://www.nexusmods.com/skyrimspecialedition/mods/184100)（2026-07-01）是現成 BFCO 轉換層，把原 [mod 94748](https://www.nexusmods.com/skyrimspecialedition/mods/94748) 列 required。⚠️ 它另需 `For Honor Power Attack` 或同類熱鍵 mod——而 BFCO MCM 內建重擊熱鍵，**這條前置是否真的必要需驗** | **重新開放**，但把「額外熱鍵 mod 前置」列為未決 |
| `:56` | **DD Daggers** | `NO-GO-MCO-ONLY` | **只有玩家路，且要自轉**：只有 [mod 80085](https://www.nexusmods.com/skyrimspecialedition/mods/80085)，**查無現成 BFCO 版**，且 **141893 catalog 裡也沒有它**（已查證）。授權已查完：私人轉換可，再發布不可（§4.1） | **降為 DEFER**——不是技術阻斷也不是授權阻斷，是「值不值得為它花一次自轉＋驗收」 |
| `:57` | **Bloodskal Weapon Art** | `NO-GO-MCO/ARTIFACT-OWNER` | 判定的第二個理由（weapon art 與神器 rebalance 越界）**與框架無關**，不因本結論改變。且 BFCO 自帶 DLC2-Bloodskal Event 專用處理（[`raws/BFCO - ….txt`](../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt) 的 `DLC2-Bloodskal Event` 段） | **確定關閉**（MCO 那半的理由失效，但 artifact-owner 那半仍然成立） |
| `:79` | **Leviathan Animations II — Greatsword 四件**（92266／88171／86183／99073 等 vanilla-replacer 家族） | `DEFER-BFCO-CONVERSION/OWNER-HOLD` | 這四件是 **vanilla replacer／locomotion／stance**，**不是 MCO moveset**——本結論**不適用**，它們沒有 `mco_*.hkx` 要改 | **維持 DEFER**（本線無新證據） |
| `:80` | **Leviathan Animations II — Greatsword MCO 94715** | `NO-GO-MCO-ONLY；Attack MCO 硬依賴且作者未授權轉 BFCO` | **兩個前提都已被推翻**：(1) 技術上可轉；(2) **授權已逐字查證**（§4.1）——Verolevi 的 `Conversion permission` 只禁「移植到別的遊戲」，不涵蓋同遊戲內框架轉換，**私人轉換無障礙**（禁的是再發布）。**NPC 路**另有現成品：141893 priority 20000，原作者明示授權 | **重新開放**。NPC 走 141893（現成）、玩家自轉——**兩條要分開寫** |
| `:81` | **Vanargand One Handed 三件** | `NO-GO-LEGACY-VANILLA/BFCO` | 同 `:79`：`legacy vanilla` 那半與框架無關。若其中含 MCO moveset 件，技術上可轉；Verolevi 的授權條款已查（§4.1，私人可） | **維持 NO-GO**，除非 `opus-content` 想連同 `:80` 一起重審 |
| `:82` | **Vanargand Dual Wield** | `NO-GO-LEGACY-VANILLA/BFCO` | 第二理由（dual power stamina／perk 語意偏移）**與框架無關**；且 BFCO 走 vanilla 攻速反而讓 perk 語意問題**變小** | **建議重審第二理由**，但本線無足夠證據翻案 |
| `:83` | **KG Animations 1H／DW＋2H** | `NO-GO-VANILLA-COMBAT/BFCO` | 理由是「全域 1P／3P attack owner」，與 MCO→BFCO 無關 | **確定關閉** |
| `:84` | **Vanargand II Unarmed Pugilism family** | `DEFER-BFCO-MOVESET-HOLD；Attack MCO 件 NO-GO` | 家族拆解：`Pugilism Stance`(109684)／`Non Combat Locomotion`(105376)／`Normal And Power Attacks`(117328) 都**不是 MCO 件**；只有 [`Unarmed MCO Moveset`(110676)](https://www.nexusmods.com/skyrimspecialedition/mods/110676) 是。該件的 MCO-ONLY 前提不成立，**授權亦已查證可私人轉換**（§4.1）。**NPC 路**：141893 priority 19000（現成、授權明確） | **把「Attack MCO 件 NO-GO」改成 DEFER**；`OAR stance 不做半套` 那半維持。NPC／玩家兩條分開寫 |
| `:149` | **Troll — MCO** | `DEFER-SCAR-FRAMEWORK-HOLD` | **不受影響**：它是 Troll AI／race overhaul，SCAR 是獨立決策（見 B9） | **維持 DEFER** |
| `:150` | **Draugr — MCO** | `DEFER-SCAR-FRAMEWORK-HOLD` | 同上 | **維持 DEFER** |
| `:55` | **Spear of Skyrim** | `DEFER-BFCO-WEAPON-CLASS-HOLD` | **不受影響**：[mod 147277](https://www.nexusmods.com/skyrimspecialedition/mods/147277) 已是 `BFCO-OAR-SkyUI Version`，本來就沒有 MCO 轉換問題；hold 的理由是 weapon-record 語意 | **維持 DEFER** |

**小計**：`NO-GO-MCO-ONLY` 四筆（`:56` 的 BDO Guardian／DD Fighter／DA Staff／DD Daggers）中**三筆的事實前提不成立**、
第四筆降為 DEFER；`:80` 的**技術與授權前提都已被推翻**；`:84` 的 MCO 件前提不成立
→ **重新開放 5 筆、降 DEFER 1 筆**；`:57`、`:83` **確定關閉**（理由與本結論無關，不必再掛在 MCO 上）。
**每一筆重新開放的都必須分「NPC 路（141893 現成）」與「玩家路（自轉）」兩條寫**，理由見 §4.2。

### 5.4 實機驗收清單（交給調度者排遊戲鎖，逐條打勾）

> 本線**不取鎖、不啟動遊戲**。以下是可逐條打勾的驗收項；每一項都寫成「看什麼、算過還是算不過」。
> 前置：先確認 `selected_profile=modpack-main`，走 Steam → MO2 shim 啟動。

**V-A 玩家路（裝一套自轉的 moveset 後）**

| # | 驗什麼 | 算過的條件 |
|---|---|---|
| A1 | 普攻連段 | 連按輕擊能連出 2 段以上，且動畫不回到 vanilla 揮砍 |
| A2 | 重擊連段 | 重擊後能接輕擊（`MCO_nextattack` 被 BFCO 吃到的證據） |
| A3 | 衝刺攻擊接續 | 衝刺攻擊播完能接普攻（社群有回報這條會斷） |
| A4 | recovery 脫離 | 攻擊後搖按移動鍵能提前脫離（`MCO_Recovery` → `BFCO_DIY_recovery`） |
| A5 | 攻速手感 | 節奏沒有明顯過快／過慢；若異常，記下 BFCO FOMOD 的 `WeapSpeedStyle` 目前選項 |
| A6 | perk 攻速生效 | 裝備／perk 的攻速修飾**看得出差異**（BFCO 走 vanilla 攻速的賣點） |
| A7 | Precision hitbox | 揮空不掉血、揮中會掉血，無穿模判定 |
| A8 | 位移同步 | 沒有滑步／砍空氣（AMR `animmotion` 有生效） |

**V-B NPC 路（裝 141893 + SCAR + OCF 後）**

| # | 驗什麼 | 算過的條件 |
|---|---|---|
| B1 | NPC 出招 | 對應種族／派系的 NPC 用到新招式，不是 vanilla 揮砍 |
| B2 | NPC 連段 | NPC 打得出 2 段以上連段 |
| B3 | 玩家不受影響 | **玩家自己的招式沒有變**（141893 是 NPC 分發，§4.2） |
| B4 | `SCAR_*Dummy.hkx` | 裝了 SCAR 之後，NPC 的 ready idle 沒有異常姿勢（B5 那條未知項的實測） |
| B5 | 連段不無限 | 沒有被 NPC 連到死（否則要加 SCAR NPC Combo Limitation Patch 162497） |

**V-C 回歸（不論走哪條路都要）**

| # | 驗什麼 | 算過的條件 |
|---|---|---|
| C1 | TK Dodge | 閃避仍可用，且攻擊↔閃避能互相派生 |
| C2 | TDM | 方向移動與方向重擊沒有互卡 |
| C3 | 存檔／讀檔 | 收刀存檔、讀回無 CTD、無卡姿勢 |

> ⚠️ **不要在同一次驗收裡動 Pandora／BFCO 版本／MO2 設定**（使用者 2026-08-27 裁示：Pandora 晚上再說）。
> A1–A8 只需要放進一套 moveset 檔案，不需要重跑 behavior 生成。

---

## 6. 待驗證／需使用者決定

### 已結案（2026-08-27）

| 項 | 結果 |
|---|---|
| ~~授權查證~~ | ✅ **已完成**，見 §4.1 與 [`agentctl/logs/nexus-permissions-mco-movesets-2026-08-27.md`](../../../../agentctl/logs/nexus-permissions-mco-movesets-2026-08-27.md)。結論：私人轉換可，再發布不可；`Conversion permission` 那條**不適用**本案 |
| ~~要不要引入 SCAR／OCF~~ | ✅ **使用者已放行**（SCAR 72014、SCAR AE Support 77285、OCF 81469） |
| ~~141893 授權是否屬實~~ | ✅ **屬實**，但它是 **NPC 分發不是玩家 moveset**（§4.2） |

### 仍待處理

1. **實機驗收（需遊戲鎖，由調度者排程與取鎖，本線不碰）**：清單見 §5.4，共 16 條可逐條打勾。
2. **Pandora／BFCO 版本：目前凍結。** 使用者 2026-08-27 裁示「晚上再說」，現在不得動
   Pandora／BFCO 版本／MO2。升級題本身仍在：BFCO 3.100.5 → 3.100.7 起
   `Running Nemesis & Pandora is now required`，升級後要重跑並重新版本化 output。
3. `mco_powerattackloop/outro` → `BFCO_PowerAttackLoop/Outro` 這組 handle **不在 BFCO 頁的動畫表上**
   （頁上寫的是 `BFCO_PowerAttack_Charge1~3.hkx` 的 DIY Charge 機制）。converter changelog 說 BFCO ≥ 3.3 支援，
   兩邊對不太上，**需要實檔或實機確認**。
4. `SCAR_*Dummy.hkx` 在**無 SCAR** 環境下的行為仍未知（推測會留下錯誤 ready idle）。
   若 NPC 路照計畫裝 SCAR，這條就不會遇到；只有走「不裝 SCAR 卻用 (SCAR) moveset」才需要驗（§5.4 B4）。
5. DA Staff 的轉換層 mod 184100 另列 `For Honor Power Attack` 前置，
   而 BFCO MCM 內建重擊熱鍵——**這條前置是否真的必要，需實機確認**。
6. §2.2 的 Linux rename `sed` 骨架**未實跑**；建議走官方工具，自刻只當離線備案。

## 7. 來源

- Nexus（全部經 houseCARL MCP，無瀏覽器）：
  [BFCO 117052](https://www.nexusmods.com/skyrimspecialedition/mods/117052)、
  [MCO to BFCO Converter 119926](https://www.nexusmods.com/skyrimspecialedition/mods/119926)、
  [Attack - MCO 175044](https://www.nexusmods.com/skyrimspecialedition/mods/175044)、
  [Attack - MCO Updated 181779](https://www.nexusmods.com/skyrimspecialedition/mods/181779)、
  [MCO Universal Support 85491](https://www.nexusmods.com/skyrimspecialedition/mods/85491)、
  [MCO-DXP and BFCO Attack Speed Fix 160188](https://www.nexusmods.com/skyrimspecialedition/mods/160188)、
  [Diverse NPC Movesets 141893](https://www.nexusmods.com/skyrimspecialedition/mods/141893)、
  [BFCO I BDO Guardian Awakening 135503](https://www.nexusmods.com/skyrimspecialedition/mods/135503)、
  [BFCO Dragon Age Staff Moveset 184100](https://www.nexusmods.com/skyrimspecialedition/mods/184100)、
  [DD2 Fighter MCO and BFCO 123708](https://www.nexusmods.com/skyrimspecialedition/mods/123708)、
  [BFCO NG 160505](https://www.nexusmods.com/skyrimspecialedition/mods/160505)。
- 本 repo：[`raws/BFCO - Attack Behavior Framework (SSE AE VR).txt`](../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt)、
  [`bfco.md`](bfco.md)、[`scar.md`](scar.md)、[`movesets-examples.md`](movesets-examples.md)、
  [`payload-interpreter.md`](payload-interpreter.md)、[`behavior-data-injector.md`](behavior-data-injector.md)、
  [`animation-motion-revolution.md`](animation-motion-revolution.md)、[`../pandora.md`](../pandora.md)、
  [`../oar-replacer-guide-overview-planning-folders.md`](../oar-replacer-guide-overview-planning-folders.md)。
- 本機（唯讀）：`~/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles/modpack-main/modlist.txt`、
  `.../mods/BFCO - Attack Behavior Framework 3.100.5/`、`.../mods/Pandora Output/{Engine.log,Pandora_Engine/ActiveMods.json}`。
