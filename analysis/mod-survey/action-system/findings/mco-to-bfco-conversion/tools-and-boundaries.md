# 現成工具與轉換邊界

← [mco-to-bfco-conversion](../mco-to-bfco-conversion.md)

## 3. 現成工具與社群做法

### 3.1 官方／半官方支援

| 事實 | 版本／時間 | 來源 |
|---|---|---|
| BFCO 頁直接推薦 converter：`people can easily convert the MCO hkx to BFCO by using MCO To BFCO Converter` | 現行頁 | [`raws/BFCO - ….txt:259`](../../raws/BFCO%20-%20Attack%20Behavior%20Framework%20%28SSE%20AE%20VR%29.txt) |
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

<!-- wf-nav -->
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

逐項記錄轉換的邊界、判定與依據。

已抽到 [tools-and-boundaries-conversion-boundaries.json](tools-and-boundaries-conversion-boundaries.json)（10 列）。

#：原表識別碼。

邊界：需注意的轉換條件。

判定：原調查判定。

依據：判定的證據與限制。

統計：10 筆記錄，4 欄。


### 4.1 授權：已逐字查證（2026-08-27）

> 查證方式與逐字原文在 [`agentctl/logs/nexus-permissions-mco-movesets-2026-08-27.md`](../../../../../agentctl/logs/nexus-permissions-mco-movesets-2026-08-27.md)
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

