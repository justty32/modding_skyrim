# jks-skyrim-setdressing — setdressing-mechanism

← [調查入口](../jks-skyrim-setdressing.md)

## Scope / sources

| | archive (`~/skyrim_mods/hdd/`) | plugin |
|------|------|------|
| **本檔主角：all-in-one（EN）** | `JK's Skyrim all in one-6289-1-7-1614998676.zip`（3.2 MB esp + 11 MB BSA mesh/texture） | `JKs Skyrim.esp` (3.2 MB) |
| 模組化（per-city / per-interior，~30 個） | `JK's Whiterun…` `JK's Riverwood…` `JK's Dragonsreach…` `JK's The Bannered Mare…` `JK's Belethor's General Goods…` … | 各自一個小 esp，**同一置放 pattern、同一 `XJK*` 命名**，差別只在範圍切片（一城或一店一檔）；玩家照需求挑裝，all-in-one = 全部聯集 |

抽取：`7z x` → `~/skyrim_mods/unzip/JKs-Skyrim-AIO/`，記錄概覽用 `dump`，新內裝用 `cellrefs`。記憶體鐵律遵守（只走 CLI lazy overlay）。

## Classification

- **Type**：world set-dressing / 純靜態置放（mass STAT placement via vanilla cell override）。
- **敘事價值：無**。零 quest、零 scene、零有意義對白；39 個新 NPC 全是為新增的幾間商店補的店主（`XJKsDawnstarGeneralvendor "Balgus"`…），53 個 package 也只是這些店主的 sandbox/vendor 排程。**它不講故事，它佈置舞台。**
- **系統價值：高**（對 #22）。這是「**靠置放量讓空間顯得被使用**」的密度基準與 placement-volume 活樣本。

## Key records & scale（record-type tally，`dump`）

5 masters：Skyrim + Update + Dawnguard + HearthFires + Dragonborn。21325 records，壓倒性是置放：

| record | count | 說明 |
|--------|------:|------|
| **PlacedObject (REFR)** | **18550** | 全部精華都在這裡——雜物/家具/招牌/植栽的靜態置放 |
| Static (base) | 293 | 少量自製 STAT base（多為走道/招牌等，textureSet 改皮）|
| **Cell** | **182**（170 Skyrim + 12 Dragonborn）vanilla **override** ＋ **12 新內裝**（`XJK*`）| 置放的載體 |
| **NavigationMesh** | **140**（138 Skyrim + 2 Dragonborn）override | 置放紀律：改完佈景**重做尋路**避免卡 NPC |
| Worldspace | 7 override | Tamriel + Solstheim + 5 座牆內城（Whiterun/Windhelm/Riften/Markarth/Solitude World）|
| PlacedNpc (ACHR) | 109（96 新 + 13 vanilla override）| 新店主置入 |
| Npc (base) | **39** | 只有新店主，全新建（指 vanilla race/voice/outfit）|
| Package | 53 | 店主排程 |
| Container/Faction/Outfit/Key… | 數十 | 配合新商店的零碎支援（vendor faction + merchant chest）|

對比 [Populated Cities](../populated-skyrim-family.md)：那邊 1115 Npc / 190 ACHR / 1190 Package（**人**為主）；JK's 是 18550 REFR / 39 Npc（**物**為主）。數字直接證明 set-dressing vs population 的分工。

## Mechanism pattern（單一手法，重複一萬八千次）

**核心 = 加性 vanilla cell override（additive cell override）**：拿一個 vanilla exterior/interior cell，**原樣帶回它既有的 vanilla refs，再追加自己的數百筆新 REFR**。實測 145 個 exterior override 中 **119 個 total > new**（帶回 vanilla refs 後加料），平均**每個 vanilla override 新增 106 筆**置放：

| cell（override） | new refs | total refs |
|------|------:|------:|
| `WindhelmOrigin` 0x03837E | 631 | 689 |
| `RiftenOrigin` 0x042247 | 594 | 637 |
| `DragonBridgeExterior01` 0x009328 | 431 | 456 |
| `RoriksteadExterior03` 0x009597 | 400 | 452 |
| `FalkreathExterior01` 0x009C80 | 353 | 389 |
| `SolitudeArch` 0x037EE7 | 334 | 393 |
| `MarkarthOrigin` 0x020EE7 | 310 | 332 |
| `XJKDawnstarShipInterior` 0x0021D8（新內裝）| 755 | 755 |

每筆 REFR = `base FormID（幾乎全指 vanilla STAT）+ position + rotation + scale`，無腳本、無 enable-parent gate、無條件——**純資料**。同一把 vanilla 雜物 base 被海量複用（如某 base 出現 744 次、另一個 665 次），靠位置/旋轉/縮放變化營造多樣。

新增 12 間商店是「from-scratch 內裝」：新 interior cell 從零塞滿 300-750 筆 REFR + 一個店主 NPC + vendor faction + merchant container（沿用 vanilla 雇傭/商店框架，無新機制）。

**為什麼不 CTD / 不卡**：① 純 record，零 runtime spawn，負載可預期；② **140 個 navmesh override** 把改過佈景的地面尋路一起重做（這是 set-dressing mod 不踩壞 AI 的代價，也是衝突大戶）；③ 自製 base 與紋理隨 BSA 出貨。

**衝突 profile（需相容的點）**：因為是 vanilla cell + worldspace + navmesh 的 override，**任何動到同一城市外觀/尋路的 mod 都會撞**（這正是社群有海量 JK's compatibility patch 的原因，hdd/ 內就有 `CFTO - JK's Skyrim Patch`、各種 -patch）。**靜態置放最大弱點**：給得起密度，給不起狀態——佈景無法隨劇情/陣營/季節改變（與 BOS 的 runtime 換物互補：BOS 才能做「戰後變廢墟」這種狀態化佈景）。

