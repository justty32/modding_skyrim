# immersive-wenches — population-mechanism

← [調查入口](../immersive-wenches.md)

## Scope / sources

- Archive: `~/skyrim_mods/hdd/Immersive Wenches SE-595-1-6-0SE.7z`（15 MB；另含 `Immersive Wenches.bsa` 104 MB + Textures.bsa 14 MB，scripts/voice 都在 BSA 內）
- 解壓：`~/skyrim_mods/unzip/Immersive Wenches SE/`
- Plugin：`Immersive Wenches.esp`，1.4 MB，**2919 records**，masters = Skyrim/Update/Dawnguard/Dragonborn
- 抽出：`../game-data/mods/Immersive Wenches/`（books=46 dialogue=39 quests=15 npcs=646 items=36 loc=85 magic=319）
- 全 EditorID 前綴 `lalawench_`（作者 lalafaye）

姊妹/衍生（各一行帶過，不深挖）：
- **Deadly Wenches SE**（599，0.5 MB）：把 wench 變成可戰鬥的敵對/中立戰士，是 IW 的戰鬥職業層（necro/mage/mystic/ranger/2H… 對應 IW 的 122 SPEL/191 MGEF/14 Class/5 CombatStyle）。
- **Buxom Wench Yuriana**（598，277 MB）：單一語音獨立隨從，沿用 wench 美術，與本機制無關。
- 另有 IW/DW 的 CHS 中文修正包（只改 STRINGS/inline，機制相同）。

## Classification

- 類型：**世界人口填充（dynamic tavern/world population）+ 輕量內容層（ambient scene + radiant quest + 隨從/配偶）**
- Plugin：是，單一 ESP（重度依賴 BSA 內 Papyrus）
- 敘事價值：**中**（內容層是 generic radiant + ambient，無角色弧線；機制價值才是重點）
- 系統價值：**高**——這是「把活 NPC 鋪滿 vanilla 酒館」最完整的範本，直接對應 idea #22。

## Record shape（用 `dump` 數出來，未整載）

Record shape（用 `dump` 數出來，未整載）的逐列資料。

已抽到 [immersive-wenches-records.json](immersive-wenches-records.json)（11 列）

記錄：原表「記錄」欄。

數量：原表「數量」欄。

角色：原表「角色」欄。

統計：11 列記錄；3 欄。

## Mechanism pattern（核心，三層）

### 1. 人口填充 = vanilla cell override 放 XMarker → 腳本生 leveled wench

不是 SPID 分發、也不是逐個 ACHR 靜態放置：

- **override 91 個 vanilla inn/聚落/dungeon cell**，每個塞 3–6 個具名 `Static` XMarker（如 `lalawenchXMarker_whiterun_innbannered1..3`）。`cellrefs Bannered Mare(0x01605E)` → 3 個 placed object、**0 placed npc**：酒館本身只放生怪點，wench 是執行期生出來的。
- 生怪來源是 34 個 `lalawench_lvl_*` **LeveledNpc**（按 race / Sultry / 城市 / patron / bodyguard 分桶）。BSA 內的 Papyrus 控制器在 marker 上 `PlaceAtMe` 對應 LL，數量/開關由 27 個 GlobalShort（`morewenches`/`nobottles`/`moretravelers`/`noscenes`/`nojarlhouses`/`novamps`…，皆 MCM 綁定）控制。
- 另有 **"Wench Bottle" ALCH（每 race/職業各一）**：玩家喝下 → 腳本在身邊生一個對應 wench（手動生怪入口，呼應 `nobottles` 開關）。

### 2. 行為 = per-inn × per-時段 × per-role 手作 package

473 個 package 命名極細，例：
`winterhold_innfrozenheart_sandbox_barmaid` / `_nightservice` / `_night_dancedrunk` / `_sleep` / `_alldayservice` / `jarlshouse_sandbox` / `morningpatrol` / `afternoonmarket`，外加 12 個 generic `Followpatrolwench` 跟隨包。
→ 每間酒館手刻一套日程（白天端酒、晚上跳舞/喝酒、夜裡睡覺、清晨巡邏）。**這是工作量最大、最不可規模化的部分**。

wench NPC 本體（`npcdiag` Linda 0xD63）：Template 繼承（`0x0012F0`）、`AutoCalcStats`+Class（避開 autocalc-no-class 死 NPC 陷阱）、role keyword（`lalawench_potentialfollower` + `_magic`）、CombatStyle、若干 ActorEffect。package/faction 走 template 的 DefaultPackageList，不寫在個體上。

### 3. 內容層 = Story-Manager 觸發的 vanilla-style ambient scene + radiant quest

<!-- wf-nav -->
- **4 個 SCEN** 都是標準多 phase（6–9 phase）`Dialog + Package` action 的 scene，host quest 的 reference alias（Server/Patron/Wench/Pervert/Barmaid）以**條件 + `MatchingRefInLoadedArea`** 填充：`HasKeyword <wench>`、`GetIsVoiceType`、`IsInFurnitureState`、`GetInFaction`、`IsInInterior` 等。任何在載入酒館內、符合條件的 wench/patron 會被即時抓進 scene。
- `lalawench_Scene_serving`（0x10AAA9）甚至直接複製 vanilla **World-Interaction** 系統：quest `type=Misc event=ADIA filter=World Interactions\Tavern\`，即 wench 掛上 keyword 後就能參與原版酒館互動。
- scene **觸發靠 Story Manager**：SMBN `IWenches`/`IWenchesalways` → SMQN `RandomWenchesScenes` / `LoneWenchScene`，事件驅動隨機挑 scene quest，**無自訂 dispatcher**。
- radiant 內容：`Captured/Enslaved Wenches`（救/賣/留被擄 wench，用 GlobalShort 當計數器與 stage gate）、`Wench Followers`（persuade 對白招募）、`Spouse`、`HomeWork`、`Misc`（買藥水/付小費/租房對白），都是 generic、可重複觸發的輕內容。

