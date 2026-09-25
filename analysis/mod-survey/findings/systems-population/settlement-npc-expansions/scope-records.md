# settlement-npc-expansions — scope-records

← [調查入口](../settlement-npc-expansions.md)

## Scope / sources

| mod | archive (`~/skyrim_mods/hdd/`) | plugin | size | masters |
|-----|------|------|-----:|------|
| Immersive College NPCs | `Immersive College NPCs-9252-1-1-02-…7z` | `ICNs_ImmersiveCollegeNPCs.esp`（另有 `ICNs_Lite.esp`） | 127 KB | Skyrim/Update/Dawnguard |
| ICMF Immersive College Mini Factions | `ICMF Immersive College Mini Factions AE-2291-3-5-6-…zip` | `ICMF Immersive College Mini Factions.esp` | 727 KB | Skyrim/Update/DG/HF/DB + 多 CC（fish/spellpack/curios/BA-armor/staves/redguard）|
| ETaC Immersive Orc Strongholds | `ETaC - Immersive Orc Strongholds SE-Cht.7z`（中文化） | `Immersive Orc Strongholds.esp` | 651 KB | Skyrim/Update/DG/HF/DB + `ETaC - RESOURCES.esm` |

抽取：`7z x` → `~/skyrim_mods/unzip/<name>/`，`extract.sh` → `game-data/mods/<name>/`，record tally 用 `dump`，細節 `packagediag`/`cellrefs`/`factdiag`/`reladiag`/`npcdiag`。記憶體鐵律遵守（只走 CLI lazy overlay）。ETaC 為中文化版，inline Name 是 cp1252→utf-8 mojibake（見 memory `chinese-mod-gamedata-mojibake`），不影響機制判讀。

## Classification

- 類型：**single-settlement NPC expansion**（把一個既有聚落從半空變成住滿/可逛）。
- 敘事價值：**低**（ICN/ETaC 純人口無對白；ICMF 有少量 generic 訓練/服務對白 + 三條 errand 小任務，無角色弧線）。
- 系統價值：**高**（對 #22）——「**單點聚落 staffing**」最乾淨的範本：少量 unique base + per-NPC 手刻日程 + 服務 faction。

## Record shape（`dump` tally，未整載）

| record | ICN | ICMF | ETaC Orc |
|--------|----:|-----:|---------:|
| 總 records | 239 | 3999 | 1867 |
| **Npc**（base） | 16 | 70 | 19 |
| **Package** | 101 | 38 | 29 |
| **PlacedNpc**（ACHR） | 26 | 46 | 32 |
| PlacedObject（XMarker/家具/裝飾 REFR） | 87 | 3391 | 1638 |
| **Cell**（多為 vanilla override） | 8 | 65 | 37 |
| **Faction** | 0（全用 vanilla 學院 faction）| 7 | 10（3 新 + 7 vanilla override）|
| Relationship | 0 | 3 | 0 |
| Outfit | 0 | 14 | 0 |
| Quest | 0 | 4 | 0 |
| DialogTopic / DialogBranch | 0 | 46 / 12 | 0 |
| Book / Container | 0 / 0 | 40 / 43 | 1 / 8 |
| Spell / MagicEffect | 0 | 30 / 6 | 0 |
| Worldspace（Tamriel override carry）| 1 | 1 | 1 |

讀法：三者都是 **少量 unique base（16/70/19）+ 約 1:1.5 的 ACHR**（一人一個放置點），**人口工作量集中在 Package**（ICN 16 人配 101 個包 ≈ 每人 6 個時段包）。PlacedObject 的暴量在 ICMF/ETaC 是**翻修聚落佈景**（家具/裝飾/店面）——不只是放人，是「把場地裝潢成有人住的樣子」。ICMF 的 Book/Spell/Container/Outfit 是**店家庫存**（賣的書、卷軸、法術、商品容器 + 店員制服）。

