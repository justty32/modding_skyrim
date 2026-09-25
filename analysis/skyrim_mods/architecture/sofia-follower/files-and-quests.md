# Sofia Follower v2.51 — files-and-quests

[返回入口](../sofia-follower.md)

## 檔案結構

來源：`~/skyrim_mods/Sofia Follower v.2/`

- `Data/SofiaFollower.esp` —— 主檔，master(s) = `[Skyrim.esm, Update.esm]`（`/tmp/mfdump/sofia.txt:1`），localized=False（字串內嵌、非 .strings 外置）。
- 2 個 BSA（script `.pex`、voice `.fuz`、mesh/texture `.nif/.dds`）——**無工具解包**，本分析聚焦 ESP record 層。
- `Sofia Follower Readme V.2.51.txt` —— 起始流程、summon spell、drunk/relationship 系統線索。

起始劇情（readme）：玩家到 Whiterun 馬廄（horses 那塊，不是建築）→ 喚醒躺在乾草堆的 Sofia → 對話邀請入隊。找不到她可用 summon spell 或 quest journal 的 tracking marker。

record 類型分佈（前段）：DialogResponses 1135 / DialogTopic 239 / DialogBranch 63 / Package 54 / GlobalShort+Float 57 / Quest 30 / Scene 28 / PlacedObject 26 / FormList 15 / Spell 9 / Npc 9 / DialogView 9 / Class 6 / ArmorAddon 6 / CombatStyle 5 / VoiceType 4 / Cell 4 / Worldspace 3 / Relationship 3 / Faction 3 / Container 3 / StoryManagerQuestNode 1 / NavigationMesh 1。

> 命名慣例：作者前綴混用 `JJ`（John Jarvis）與 `Sofia`，readme 也說「Most things related to Sofia will either start with the prefix JJ or have Sofia in the name」。

## record 解剖

### 1. Quest 全表（30 個）—— 「一個隨從用幾十個 quest 各司其職」

來源：`/tmp/mfdump/sofia.txt:7267`–`7386`。把 30 個 quest 按職責分群：

#### A. 主控 / 狀態核心
| Quest | FormID | 掛載 script（屬性數） | 角色 |
|---|---|---|---|
| `JJSofiaFollowerMain` | `[01010A]` | SofiaFollowerScript (12) | 隨從主狀態機，objective[10]「is waiting for you」 |
| `JJSofiaScripts` | `[00AA58]` | SofiaNewVersionScript(16)+SofiaUpdateScript(18)+SofiaCatchUpNewScript(16) | 版本升級 / catch-up 跟隨邏輯總成 |
| `JJSofiaVariables` | `[0557B1]` | JJSofiaVariablesScript (19) | 變數中樞，flags=273（StartGameEnabled），quest script property 存狀態 |
| `JJSofiaRelationship` | `[05373C]` | JJSofiaRelationshipScript(3)+SofiaMarriageScript(5) | 好感度 + 婚姻條件追蹤 |

#### B. 對話容器（每個 quest = 一批 dialogue / scene 的掛載點）
- `JJSofiaDialogue` `[001D8B]`（SofiaCommentScript 14 prop）—— 核心隨從互動分支（trade / part ways / follow / can I talk / storage…，見 DialogBranch 群 `:7548`+）。
- `JJSofiaIdleDialogue` `[007F02]` —— 閒聊；單一 scene topic 掛 **149 個 INFO group**（`:1420`），是全 mod 最大的對白池。
- `JJSofiaMainQuestDialogue` `[020467]`（JJSofiaQuestUpdateScript 7 + JJSofiaQuestLineManager 0）—— Sofia 個人主線劇情。
- `JJSofiaSidequestDialogue` `[034EBF]` —— bounty / 支線。
- `JJSofiaBardSongs` `[02F2D1]` —— 唱歌（多首歌各一個 scene，見下）。

#### C. 互動 comment（對特定 vanilla NPC 吐槽，高度模板化）
8 組，每組「`*Comment` quest（priority=60）+ `*SayComment` scene（flags=BeginOnQuestStart, StopQuestOnEnd）」成對出現：
`JJSofiaNazeemComment` `[03088D]` / `JJSofiaCarlottaComment` `[03BB10]` / `JJSofiaBraithComment` `[03CB44]` / `JJSofiaLarsComment` `[06FCCB]` / `JJSofiaNelkirComment` `[070239]` / `JJSofiaTaarieComment` `[070244]` / `JJSofiaEndarieComment` `[070251]` / `JJSofiaGuardComment` `[070D22]`。

這些 comment quest 用 `alias[2]` 直接 `uniqueActor` 指向 vanilla NPC，例如 `LarsRef -> 013BAF:Skyrim.esm`、`NelkirRef -> 01434D:Skyrim.esm`、`TaarieRef -> 0132AB:Skyrim.esm`、`EndarieRef -> 01326F:Skyrim.esm`（`:7371`–`7380`）。**這是「批次生成的 per-NPC 吐槽」設計模式**——同一結構複製 8 份，只換目標 actor 與對白。

#### D. 系統 / 工具
| Quest | FormID | 用途 |
|---|---|---|
| `JJSofiaMCM` | `[00C55D]` | SofiaMCMscript (26 prop)，SkyUI MCM 設定選單 |
| `JJSofiaGetHasSKSE` | `[00E5FE]` | SofiaHasSKSEscript，偵測有無 SKSE → 設 `SofiaHasSKSE` GLOB |
| `JJSofiaTrackingMarker` | `[043CED]` | flags=281，objective「Sofia Tracking Marker」（可在 journal 切換的找人 marker） |
| `JJSofiaClothingFix` | `[04BAE3]` | 修「脫衣 glitch」的外觀矯正 |
| `JJSofiaWardrobe` | `[061F70]` | 衣櫥/換裝 |
| `JJSofiaBattleCommands` | `[030DF3]` | priority=90，戰鬥指令 |
| `JJSofiaCastSpell` | `[03749E]` | 觸發 Sofia 施法（nude bomb 等） |
| `JJSofiaGiveGift` | `[040C27]` | 送禮（提升好感度） |
| `JJSofiaLeadTheWay` | `[017D1E]` | 帶路到目的地 |

#### E. 劇情 / 演出
- `JJSofiaWeddingCeremony` `[05167F]`（QF script 11 prop，flags=**RunOnce**，priority=100）—— 完整婚禮，stage 0→5→10→20→150(FailQuest「You stood Sofia up」)→200(CompleteQuest「You married Sofia」)，objective「Go To Wedding」（`:7343`–`7358`）。
- `JJSofiaDrunk` `[01A866]`（priority=100）—— 醉酒系統，stage 0–50。readme 提供 console 救援 `stopquest jjsofiadrunk`。
- `JJSofiaQuest` `[0285BD]` —— 起始 meeting quest，stage[0]=**StartUpStage**（馬廄醒來/邀請）。
- `JJJarvisDialogue` `[0343F0]` —— 作者彩蛋角色 Jarvis。

**設計模式歸納**：Sofia 把一個隨從拆成「**一個職責一個 quest**」的微服務式架構——狀態核心、跟隨邏輯、每種互動、每首歌、每個被吐槽的 NPC、每個系統功能各自一個 quest。好處是各功能可獨立 start/stop（readme 的救援指令正是靠這個粒度），壞處是 record 數爆炸（光 comment 就 8×2 個 record）。

