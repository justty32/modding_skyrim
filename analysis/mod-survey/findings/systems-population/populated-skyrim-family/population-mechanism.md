# populated-skyrim-family — population-mechanism

← [調查入口](../populated-skyrim-family.md)

## Scope / sources

| 變體 | archive (`~/skyrim_mods/hdd/`) | plugin |
|------|------|--------|
| Cities/Towns/Villages | `Populated Cities Towns Villages SE BSA-2005-…7z` | `Populated Cities Towns Villages Legendary.esp` (2.1 MB) |
| Lands/Roads/Paths | `Populated Lands Roads Paths Legendary loose files-1840-…7z` | `Populated Lands Roads Paths.esp` (0.7 MB) |
| Dungeons/Caves/Ruins | `Populated Dungeons Caves Ruins Legendary Edition-2820-1-0.7z` | `Populated Dungns Caves Ruins Legendary.esp` (0.28 MB) |
| Hell Edition（極限版＝四者聯集＋更多） | `Populated Skyrim Hell Edition-5017-…7z` | `Populated Skyrim Legendary.esp` (2.8 MB) |

抽取：`7z x` → `~/skyrim_mods/unzip/`，`extract.sh` → `../../../projects/game-data/mods/<name>/`，record 概覽用 `dump`，package 用 `packagediag`。記憶體鐵律遵守（只走 CLI lazy overlay）。

## Classification

- Type：world population / 純置放 NPC（無任務、無對白演出）。
- 敘事價值：**無~低**。沒有 quest / scene / 有意義對白（Hell 的少數 DialogTopic 只是「雇傭兵/商人雇用」交易選項，沿用 vanilla hireling 框架）。
- 系統價值：**高**（對 #22）。這是「把世界填滿活人」的密度基準與 archetype 字典。

## Key records & scale（record-type tally，`dump`）

| record | Cities | Lands/Roads | Dungeons | Hell |
|--------|-------:|------:|------:|-----:|
| 總 records | 6755 | 1743 | 1464 | 8350 |
| **Npc**（base） | 1115 | 943 | 90 | **3171** |
| **PlacedNpc**（ACHR） | 190 | 146 | 549 | **1863** |
| PlacedObject（REFR/marker/idle） | 3910 | 125 | 604 | 1518 |
| **Package** | 1190 | 161 | 66 | 649 |
| LeveledNpc | 62 | 138 | — | 267 |
| Cell（多為 override vanilla） | 164 | 88 | 104 | 558 |
| Faction | 25 | 24 | 3 | 56 |
| NavigationMesh | 29 | — | — | — |
| masters | Skyrim+Update | Skyrim+Update | Skyrim+Update | +Dawnguard+HearthFires+Dragonborn |

讀法：Cities = **1 unique base : 1 ACHR**，但 **package 數 ≈ base 數**（每個市民有專屬排程 package）。Dungeons 反過來 = 90 base : 549 ACHR（少量共用敵性 base 大量置放）。Hell = 把前三者疊起來再加 bandit/militia/prisoner。

## Mechanism pattern（四變體的差異就是機制的差異）

共同骨架（與 Civil War / Immersive Patrols 同源，無 controller）：
**自製 NPC base（race/class/voice/outfit/combatStyle/factions 全指 vanilla FormID）→ 指派 package → 直接 ACHR 置入 vanilla cell（cell override）→ 靠 faction 敵我與 package AI 產生 emergent 行為**。EditorID 前綴 `ssss`/`oooo`/`iiii`/`eeee`/`rrrr`/`kkkk`/`llll` 分群。Cities 還自帶 29 個 NavigationMesh override（置放紀律 = 不踩壞尋路）。

四變體各自的「人口機制」：

Mechanism pattern（四變體的差異就是機制的差異）的逐列資料。

已抽到 [populated-skyrim-family-variants.json](populated-skyrim-family-variants.json)（4 列）

變體：原表「變體」欄。

base 策略：原表「base 策略」欄。

package 類型：原表「package 類型」欄。

faction / 敵我：原表「faction / 敵我」欄。

場景：原表「場景」欄。

統計：4 列記錄；5 欄。

**效能/相容手法**（如何不 CTD / 不卡）：① 純 record，無 runtime spawn 腳本（負載可預期）；② Hell 變體含 **`PopLandsMCM` quest**（flags=273 Start-Game-Enabled、PlayerRef ForcedReference alias）＝ MCM 設定選單，讓玩家**開關各城/各類人口、調密度**（這是這系列出名的「可調人口」核心）；③ Cities 重置 navmesh 避免尋路崩；④ 大量 base 必附 FaceGen（archive 帶 mesh/texture）。注意：與 Civil War / Immersive Patrols 一樣，**靜態置放無法隨劇情狀態改變**——密度給得起，戰略狀態給不起。

對照家族其他成員：本系列比 Civil War 變體**範圍更廣**（不只戰士、含全民生 archetype + 排程 sandbox），但機制同源；比 Immersive Patrols **更暴力、更不講究**（IP 是精選路線交叉，本系列是地毯式填滿）。

