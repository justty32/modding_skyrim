# wench-derivatives — variants

← [調查入口](../wench-derivatives.md)

## Scope / sources

| Mod | Archive | Plugin | 規模 | 與 IW 關係 |
|-----|---------|--------|------|-----------|
| **Deadly Wenches SE** | `Deadly Wenches SE-599-1-2-5SE.7z`（554 KB） | `Deadly Wenches.esp` 997 rec | npcs=737 quests=1 magic=7（無 dialogue/loc）| **master 依賴 IW**（refs into IW.esp = 4812）|
| **Buxom Wench Yuriana** | `Buxom Wench Yuriana-598-1-2-2.7z`（277 MB，含 BSA/voice/facegen）| `YurianaWench.esp` 3869 rec | books=51 dialogue=143 quests=17 npcs=117 cell=92 worldspace=7 | **無 IW master**（standalone），但保留 `lalawench_` 同源記錄 |
| **Less Buxom Yuriana Watcher Overhaul** | `…-88082-2-…rar`（2.9 GB）| **無 plugin** | 純 meshes/textures/DAR 動畫/FNIS | Yuriana 的美術替換包，override `yurianawench.esp` 的 facegen，**無敘事價值**（一行帶過）|

抽出：`../game-data/mods/{Deadly Wenches, Buxom Wench Yuriana}/`。CLI lazy overlay，未整載 Skyrim.esm。

---

## A. Deadly Wenches — 「戰鬥變體人口」靠 vanilla Leveled List 注入

### Classification
- 類型：**敵對/中立戰鬥 NPC 分發層（leveled-list injection）**，是 IW 的戰鬥職業 add-on，**硬依賴 IW**（用 IW 的 race/keyword/base effect 組裝戰鬥版 wench）。
- 敘事價值：**無**（純戰鬥 spawn，唯一 quest 是 MCM 控制器）。
- 系統價值：中——示範了**與 IW 截然不同的第二種人口填充機制**。

### Record shape（`dump` 數，未整載）
| 記錄 | 數量 | 角色 |
|------|------|------|
| Npc | 737（全 DW-new）| `DW_Enc<Faction>_<race><n>_<role>` 戰鬥變體（Bandit/Forsworn/Vampire/VigilantOfStendarr × race × melee/2H/magic/archer/tank/assassin/mage）|
| LeveledNpc | 120 = **91 vanilla override** + 29 DW-new | **核心**：override 91 個 vanilla 敵人 LL |
| LeveledItem/Spell | 67 / 35 | 戰利品與技能桶 |
| Mod* (ModAttackDamage/ModSpellMagnitude…) | 58 | 難度縮放 perk 用的 entry-point |
| Outfit 23・Perk 3・Spell 4・Armor 4・MagicEffect 3 | | 戰鬥組裝；6 個 spell/mgef 仍掛 `lalawench_` 前綴 |
| Quest | 1 | `lalawench_DWMCM`（純 MCM）|

### Mechanism（與 IW 對比，這是重點）
**IW = 在 vanilla cell 放 XMarker，執行期 script `PlaceAtMe` 生 wench。**
**DW = 改寫 vanilla 敵人 LeveledNpc，靠引擎既有 spawn 點自動生出戰鬥 wench。** 例（byte 已驗）：

```
[01A321:Skyrim.esm] LeveledNpc LCharBanditMeleeNordF   ← override 進 Skyrim.esm 的 LL
    lvln entry -> 039CF5/03CF5C:Skyrim.esm (原 vanilla 條目保留)
    lvln entry -> DW_WenchSubCharBandit_FemaleNord_melee  ×6 (additive 注入)
```

被改寫的 91 個全是 `LCharBandit* / LCharForsworn* / LCharVampire* / LCharSoldier* / SubCharBandit*`。任何貼這些 LL 的 vanilla 生怪點（土匪營、棄誓者、吸血鬼巢、內戰兵），現在有機率生出 DW 戰鬥 wench。**零 placement、零 package、零 scene** —— 純粹「改 LL 讓 vanilla 系統替你鋪人」。

> 對照：IW 自己也有 34 個 `lalawench_lvl_*` LL，但那是**新 LL** 給自己的 marker 用；DW 是**改 vanilla LL** 寄生 vanilla spawn。兩條路互補——IW 鋪「室內生活人口」，DW 鋪「野外戰鬥人口」。

---

## B. Buxom Wench Yuriana — 不是「單一隨從」，是隨從＋自帶任務/地牢的小型 quest-mod

> ⚠️ 修正 IW finding 的一行注記（「單一語音獨立隨從，與本機制無關」）：Yuriana **規模遠超單一隨從**。它是 standalone（無 IW master）的完整 quest-mod。

### Classification
- 類型：**獨立語音隨從 + 自帶 radiant 內容 + 跨 vanilla 世界的 placement 改造**。
- 敘事價值：**中**（17 quest 多為 generic「captured/enslaved wenches」radiant + 商人/服務對白，無強角色弧，但有 145 條 cloned voice）。

### Record shape
| 記錄 | 數量 | 角色 |
|------|------|------|
| PlacedObject (REFR) | 1648 | 大量靜態佈置（改裝酒館/自家地牢內裝）|
| PlacedNpc (ACHR) | 210 | 靜態放置 wench |
| DialogTopic/Responses | 203 / 208 | 真對白量（IW 才 39）|
| Npc | 117 | Yuriana 本體 + 被擄/服務 wench |
| Cell | 92 = **90 vanilla override** + 2 own | override vanilla 酒館；2 個自家 cell |
| Worldspace | 7（全 Skyrim.esm vanilla 引用）| 內容散佈在 Tamriel/各城/Solstheim，**無自建 worldspace** |
| GlobalShort 85・Package 52・Quest 17・Book 51・NavMesh 4 | | 完整 quest-mod 骨架 |
| voice | 145 `.fuz`（FemaleSultry/Commander/EvenToned/UniqueGhost… 8 voicetype）| 真語音 |

### Yuriana follower NPC（`npcdiag 0x000D70`）
- 自家 Race/Class/CombatStyle，Voice = `013AE0:Skyrim.esm`（FemaleSultry）。
- Flags = `Female, Essential, AutoCalcStats, Unique` + 明確 Class → **正確避開 autocalc-no-class 死 NPC 陷阱**（與 memory `autocalc-without-class-dead-npc` 一致）。
- Factions 含 `0x05C84D CurrentFollowerFaction` + `0x05C84E PotentialFollowerFaction` → **走 vanilla 隨從框架**（非 NFF/AFT，免框架依賴）。
- 47 Perk、本體 2 Package。`lalawench_` 前綴記錄（foodfaction/ghost/Rfaction）證明與 IW 同血緣，但已**自帶一份、不依賴 IW**。

> follower 部分對 #22 = **「standalone 語音隨從」的範本**（vanilla follower faction + Essential+Class+AutoCalc + 自家 race/voicetype + cloned `.fuz`），與 ModForge 已 in-game confirmed 的 voice-gen 管線（memory `voice-gen-interface-future`）完全對得上。其餘 90-cell override + radiant captured-wenches 是 IW 內容層的平行重做，**對 #22 無新機制**。

---

