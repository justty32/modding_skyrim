# cutting-room-floor — restoration-mechanism

← [調查入口](../cutting-room-floor.md)

## Scope / sources

- Archive：`~/skyrim_mods/hdd/Cutting Room Floor-276-3-1-11-1638226201.7z`（4.9 MB；另含 `Cutting Room Floor.bsa`（Papyrus）+ `- Textures.bsa`）
- 解壓：`~/skyrim_mods/unzip/Cutting Room Floor/`
- Plugin：`Cutting Room Floor.esp`，1.3 MB，**4643 records**，masters = Skyrim/Update/Dawnguard/HearthFires/Dragonborn/**USSEP**
- 抽出：`../game-data/mods/Cutting Room Floor/`（books=11 dialogue=161 quests=36 npcs=79 items=14 loc=141 magic=17）
- EditorID 前綴：**新內容一律 `CRF*`**；無前綴的（`ArgiFarseer`/`Hadring`/`OlfinaGrayMane`…）是 **vanilla.esm 裡被砍掉的休眠記錄，CRF override 重新啟用**
- 性質：**內容復原（content restoration）**——按 UESP「Unused NPCs / Unfinished Quests / Unobtainable Items」清單，把 Bethesda 做好卻沒接上的東西接回去

## Classification

- 類型：**vanilla 聚落人口/內容復原**（add living NPCs + 小聚落 + 小任務，非破壞性整合）
- Plugin：是，單一 ESP（Papyrus 在 BSA）
- 敘事價值：**中**——個別 NPC 有 vanilla 級小設定，但無角色弧；機制（怎麼非破壞地把人塞進既有聚落）才是 #22 要學的
- 系統價值：**高**——這是「在**既有**世界裡長出一個有人住的小聚落」最乾淨的官方風範本，正面對應 idea #22 的「異世界裡有人住」

## Record shape（`dump` 數出，未整載）— 新增 vs override 是重點

Record shape（`dump` 數出，未整載）— 新增 vs override 是重點的逐列資料。

已抽到 [cutting-room-floor-records.json](cutting-room-floor-records.json)（11 列）

記錄：原表「記錄」欄。

新增(CRF.esp)：原表「新增(CRF.esp)」欄。

override(masters)：原表「override(masters)」欄。

角色：原表「角色」欄。

統計：11 列記錄；4 欄。

對照 Immersive Wenches：IW 是 415 個 **spawn marker + LeveledNpc**（執行期生怪）；CRF 是 **78 個靜態 ACHR + 33 具名 NPC**（編輯期就擺好的固定居民）。兩種「填人口」路線的極端：CRF = 手擺固定住民，IW = 動態生匿名人群。

## Mechanism pattern（核心，三件事）

### 1. 新聚落 = 「override 幾個 vanilla 外景 cell + 加新 interior + 手擺 ACHR + 每人 faction/日程」

以 **Frost River**（Hjaalmarch 一個 vanilla 殘樁聚落）為完整範例：
<!-- wf-nav -->
- **外景**：`CRFFrostRiverFarmEast/West/SE/SmithCell`（FormID `0x0093xx`，**住在 Skyrim.esm**）——是 vanilla 外景 cell 的 **override**，CRF 給它們指派 EditorID 並 additive 塞進建物 REFR。新 **interior** cell 才是真新增（`Rogen's House 0x1A8B79`、`Meadery 0x031377`、`Henrik's House 0x1A8B7A`）。
- **interior 內裝**＝純 placements：`cellrefs 0x031377` 全是 vanilla static/furniture（`029CB0`、`012FE7`…）＋少數 `CRF` 自家 static，標準佈置，無腳本。
- **居民**＝具名 NPC + 每人手刻日程。`npcdiag` Iddli Iron-Blood（`0x023906`）：vanilla race/class/voice/outfit、`AutoCalcStats`+Class（避開 autocalc-no-class 死 NPC 陷阱）、`Unique`、CrimeFaction=該 hold、加入聚落 faction（`FrostRiverFarmFaction 0x08F17F`）。Packages 直接列在個體上（**不走 template DefaultPackageList**，與 IW 相反）：
  - `CRFFrostRiverFarmEatMorning`（template `EatX`，hour 5 / 60min）
  - `CRFFrostRiverFarmWork`（template，hour 10 / 480min，多個 work-marker LocationTarget）
  - `CRFFrostRiverfarmIndoorSandbox`（fallback，NearEditorLocation radius 2048）
  → 早餐→白天工作（綁工作點）→室內 sandbox→（晚上）睡，一人一套。**最費工、最不可規模化**的部分，跟 IW 的 473 package 同病。
- **聚落 faction 三件套**：`CRFFrostRiverFaction`（鎮民歸屬）、`CRFServicesFrostRiverBlacksmith`（vendor faction，帶 sellBuyList/merchantContainer/vendorLocation/營業 8–20）、house faction（門禁/所有權）。Heljarchen/Stonehills 各複製同一套。

### 2. 非破壞整合＝一排無文字的「ChangeLocation 狀態機」quest（不直接砍 vanilla）

新 quest 11 個裡 **9 個是 `CRFChangeLocation0X` + `CRFInitializer`**，全部**無 log/objective 文字**——它們是 Start-Game-Enabled 的管理 quest，靠 startUpStage fragment 在執行期切換 cell/ref 的啟用狀態，避免硬改 vanilla：
- `CRFInitializer`（`0x0368FD`，flags=17 含 StartGameEnabled，filter `Arthmoor\`）：開局把所有編輯過的 quest/物件初始化到正確狀態。
- `CRFChangeLocation03 "Civil War swap at Frost River"`（`0x02600A`，RunOnce，event=CLOC）：用 3 個 reference alias（`CRFFarmMillImperials`/`...Sons` 帶 `AllowDisabled`/`AllowReserved` flag + LocationAliasReference RefType 過濾）依內戰歸屬 enable/disable 對應的帝國/風暴兵 ACHR。
- 其餘：`CRFChangeLocation01` 戰後解鎖塔門、`02` Vigilant 死亡、`04/05` 依別的 quest 是否完成 enable 物件、`06/07` MG08 後讓 Orthorn 回家、`08` 填 Riften 守衛 alias、`09` Ofrid/Vignar 恩怨 scene。
→ **pattern＝用「條件填充 reference alias + AllowDisabled flag」當開關，而非刪 vanilla record**。這就是「相容、可疊加」的官方做法。

### 3. 小內容＝復活的 vanilla cut quest + 一兩個聚落 radiant

- 25 個 **override quest** 是復活 vanilla 半成品（`MGR01/MGRRogue/MGR12 College`、`C01 Proving Honor`、`DB01Misc Cicero`、`CR03 Pelt Collection`…）——CRF 補完 stage/objective/INFO，不是自己寫故事。
- 唯一純新的聚落 radiant：`FreeformFrostRiver "Supply Line"`（`0x0681D4`）——meadery 主人 Signar（`0x023907`）給「送一箱蜜酒到某酒館」repeatable 任務，帶分支對白（`How's business?`→招募鋪陳→accept），目標城市隨機（Winterhold/Whiterun/Solitude）。**這就是「小聚落 + 一個輕量在地任務 + 在地對白」的最小單元**，正是 #22 想要的密度。
- 只新增 1 個 SM 節點 `CRFNode`，其餘觸發 additive 掛 vanilla SM 根。

