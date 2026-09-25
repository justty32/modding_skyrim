# 轉換步驟與來源

← [mco-to-bfco-conversion](../mco-to-bfco-conversion.md)

## 2. 轉換實際要動什麼（可執行步驟骨架）

### 2.0 前提檢查

1. BFCO ≥ 3.3（`mco_powerattackloop/outro` 才有對應 handle）。現役 3.100.5 ✅。
2. **MCO 與 BFCO 不可共存**（BFCO 頁 Incompatible with 明列 `Skysa/ABR/MCO`，
   [`raws/BFCO - ….txt:259`](../../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt)）。轉換是**單向遷移**，不是相容層。
3. 原 moveset 若是 DAR-only，確認 OAR 已裝（OAR 原生讀 `DynamicAnimationReplacer\_CustomConditions\<priority>\`
   並轉成 "Legacy" replacer-mod，見 [`oar-replacer-guide-overview-planning-folders.md:74`](../../oar-replacer-guide-overview-planning-folders.md)）。

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
  與 attack framework 無關——見 [movesets-examples.md](../movesets-examples.md) 的實檔拆解。
- OAR 是**按被替換動畫的檔案路徑**做替換，所以檔名一改，OAR 自動就替換到 `BFCO_*` handle 上。
  本機 BFCO 3.100.5 自己出貨的 16 個 OAR submod（`OpenAnimationReplacer/BFCO/1hm-sword-base/` 等）
  裡放的正是 `BFCO_*.hkx`，證實這條路徑。
- **要改的例外**：
  - 條件裡出現 `MCO_*` graph variable 的 `CompareValues`（少見，但存在）；
  - 想升級成 BFCO 變體分支（新增資料夾 + `BFCO_iAttackVariants` 條件，語法見 [bfco.md](../bfco.md)）。

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

## 7. 來源

<!-- wf-nav -->
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
- 本 repo：[`raws/BFCO - Attack Behavior Framework (SSE AE VR).txt`](../../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt)、
  [`bfco.md`](../bfco.md)、[`scar.md`](../scar.md)、[`movesets-examples.md`](../movesets-examples.md)、
  [`payload-interpreter.md`](../payload-interpreter.md)、[`behavior-data-injector.md`](../behavior-data-injector.md)、
  [`animation-motion-revolution.md`](../animation-motion-revolution.md)、[`../pandora.md`](../../pandora.md)、
  [`../oar-replacer-guide-overview-planning-folders.md`](../../oar-replacer-guide-overview-planning-folders.md)。
- 本機（唯讀）：`~/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles/modpack-main/modlist.txt`、
  `.../mods/BFCO - Attack Behavior Framework 3.100.5/`、`.../mods/Pandora Output/{Engine.log,Pandora_Engine/ActiveMods.json}`。
