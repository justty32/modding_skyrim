# 2. 關鍵 record 與模式（重點：radiant quest 的可生成結構）

← [原文入口](../missives-mechanism-records.md)

## 2. 關鍵 record 與模式（重點：radiant quest 的可生成結構）

### 2a. quest 模板的笛卡兒積 + tiered FormList 池

EditorID 本身就是生成表：`_M_Quest<Hold><JobFamily><Variant><Tier>`，例如 `_M_QuestWhiterunKillBandit`、`_M_QuestRiftGatherOreVeryHigh`、`_M_QuestEastmarchCourierLetterHigh`。

- **9 holds**：Whiterun / Eastmarch / Falkreath / Haafingar / Hjaalmarch / Pale / Reach / Rift / Winterhold（各約 29–30 顆）。
- **job families**：Kill（Bandit/Animal/Dragon/Giant/Forsworn）、Retrieve（Wilderness/Ruins/Hideout）、Gather（Ingr/Ore/SoulGem/Inn 各 Low/Med/High[/VeryHigh]）、Courier（Letter/Weapon/Potion 各 Low/Med/High）、Track（Thief/Vampire/Fugitive）。
- **4 個難度 tier**：`_M_ListQuests<Hold><Tier>`（Low/Med/High/VeryHigh）＝ FormList 池。板子用 4 個 `QuestChance*` global 控各 tier 出現率。

**每塊板子（每個 hold）綁該 hold 的 4 個 FormList**；同一顆 quest「下次再接」靠 `Start()` 重填 alias，所以模板可重複使用。

### 2b. quest 模板的內部骨架（`questdiag`）

所有模板共用同一套 stage：`0=StartUpStage / 20=接取 / (30,40=取物/送達) / 100=Complete / 105=Fail / 110=ShutDown`。objective display text 大量用 alias token：

```
Kill:     obj20 "Kill the Leader of <Alias=Dungeon>"  obj40/41 "Collect bounty from <Alias=Steward>/<Alias=Jarl>"
Retrieve: obj20 "Retrieve <Alias=Item>"               obj40 "Return <Alias=Item>"
Gather:   obj20 "Gather <Alias=Item> (<Global=Count>/<Global=Total>)"  obj40 "Bring ... to <Alias=QuestGiver>"
Courier:  obj20 "Collect <Alias=Item>" obj30 "Recover <Alias=Item>" obj40 "Deliver ... by <Global.Day=Time>"
Track:    obj10 "Find the Thief in <Alias=OtherHold> and Retrieve <Alias=Item>"
```

注意 obj40/41 的雙軌（有 Steward 走 40、沒有走 41 領 Jarl）＝靠 quest fragment `if(Alias_Steward.GetRef())` 分流。Gather 的數量顯示靠 `<Global=...Count>/<Global=...Total>` 兩個計數 global 即時更新。

### 2c. alias fill 模式（這是 radiant variety 的真正引擎）

從各 quest 腳本的 alias property 宣告，可逆推出每顆模板的 alias 套組（fill 模式存在 quest record 的 alias 定義裡，由 `Quest.Start()` 時引擎執行）：

<!-- wf-nav -->
- **`LocationAlias Alias_Hold`**：用 keyword 條件（hold location type）挑中**這個 hold**——這就是「Whiterun 板子只給 Whiterun 任務」的根。
- **`LocationAlias Alias_Dungeon` / `Alias_Inn` / `Alias_Destination` / `Alias_City`**：在 `Hold`（或排除 forbidden）範圍內**Find matching location**（依 location-type keyword：dungeon / inn / city…）隨機挑一個合法地點＝目標地點的隨機化。
- **nested `ReferenceAlias`（Find in alias）**：在已填好的 `Dungeon` 裡找 ——
  - `Alias_Steward`/`Alias_Jarl`/`Alias_QuestGiver`/`Alias_recipient`＝在城鎮 location 裡找特定 ref / unique actor（領賞對象）；
  - `Alias_chest`/`Alias_Item`＝在 dungeon 裡找一個容器，再把 LVLI 目標物投進去（取物型）；
  - `Alias_target`/`Alias_Thief`＝Create Reference to a LeveledNpc（`_M_LCharThief` 等）或 Find boss ref（殺/追捕型）。
- **`_M_ListLocationsForbidden` / `_M_ListPeopleForbidden`**：alias 條件的排除清單，避免挑到不該用的地點/人。
- **追捕型的跨 hold**：`Alias_OtherHold` 另填一個**不同**的 hold，逃犯 NPC（LVLN）由 Papyrus `Enable()` + 投物到該 hold 的 inn marker（`Alias_Inn1/2`、`Alias_InnMarker1/2`），追到殺掉取回失物。

**結論：variety = (a) 模板把 job-type 寫死，(b) Location alias 用 keyword/forbidden-list 隨機挑地點，(c) nested Reference alias 在那地點裡 Find/Create 出箱子・頭目・領賞人・LVLN 目標。** 完全是引擎原生 radiant 機制，跑時零 Papyrus 介入填充。

### 2d. 物品與獎勵的 LVLI 雙用

- **目標物品**＝`_M_LItemItem*`（Ingr/Ore/SoulGem/Inn/Jewelry/Heirloom/Armor/BookSkills/Potion…）：填進 dungeon 箱子或當採集目標，由 tier 決定稀有度。
- **獎勵**＝`_M_LItemReward*`：結算時 `AddItem(Reward)`。金幣另由 `GoldReward` global 給。
- **動態命名**：`Message` record（如 `_M_MessageItemRetrieve "<Alias.ShortName=QuestGiver>'s <BaseName>"`）把通用 LVLI 物品改寫成「某人的傳家寶」這種具體名，增強敘事而不需做獨立 record。

### 2e. missive BOOK 與板子 Container/Activator

- **Book**（`_M_Missive*`）＝告示，標題 `"Missive: Kill the Leader of <Alias=Dungeon>"` 用 alias token 代入；填進 `_M_MissiveBoard`（Container）。
- **Activator + Container 分工**：`_M_ActivatorBoard`（隱形 trigger box，掛刷新腳本）+ `_M_MissiveBoard`（玩家能開的容器，裝 missive）。刷新時 `BlockActivation(true/false)` 鎖住容器避免並發。
- **領賞對話**：每顆 quest 一條 `_M_Quest...RewardTopic`（DialogTopic，player line），條件綁該 quest 在跑 + objective 狀態，講給 radiant 填出的領賞 alias。

---

