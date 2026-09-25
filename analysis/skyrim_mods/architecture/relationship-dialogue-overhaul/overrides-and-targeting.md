# Relationship Dialogue Overhaul (RDO Final, v1187) — overrides-and-targeting

[返回入口](../relationship-dialogue-overhaul.md)

## override 策略

### 1. 海量 condition 投放（mod 的靈魂）

對 dump 全體 condition 跑頻率（`grep -oE 'condition: [A-Za-z]+' … | sort | uniq -c | sort -rn`）：

本表彙整「condition-usage」的原始記錄。已抽到 [overrides-and-targeting-condition-usage.json](overrides-and-targeting-condition-usage.json)（12 列）。

次數：原表「次數」欄值。

condition function：原表「condition function」欄值。

投放用途：原表「投放用途」欄值。

統計：12 列，3 欄。

**分佈的解讀**：前兩名 `GetIsVoiceType`(9245) + `GetInFaction`(7224) 壓倒性領先，直接證明 RDO 的投放單位是**「類」而非「個」**——一句通用台詞用「語音類型 + 陣營」就能覆蓋成百上千個 NPC，無需逐一掛到每個 actor。再疊上 `GetRelationshipRank`(1683) + `GetPlayerTeammate`(2142)，讓同一情境下台詞隨「玩家與你的關係 / 你是不是隨從」分流。最後 `GetRandomPercent`(3112) 在每一束候選台詞上做隨機抽選，避免重複。三層疊起來就是：**用條件把有限的台詞素材，組合投放成「看起來無限」的對話覆蓋面**。

（投放手法的逐句細節版另見 `details/dialogue-targeting-technique.md`，本檔只點到原則。）

### 2. FormList 作為投放名單

RDO 新增 18 個 FormList，命名即用途，是 `IsInList`(936) 的彈藥：

- `aaa_RDOVoicesAll` / `aaa_RDOVoicesMaleList` / `aaa_RDOVoicesFemaleList`——全部 / 男 / 女語音類型集合
- `aaa_RDOVoicesFollowerAll` / `aaa_RDOVoicesMarriageAll`——隨從 / 配偶語音集合
- `_RDOVoicesFollowerAllPlusUniques`、`a_RDOVoicesFollowerGenericResponses`——隨從專用回應名單
- `aaa_RDOPreventedActorsList` / `…HatePL` / `…Friend`——**排除名單**（不該被投放的 actor，避免覆蓋到劇情關鍵或不合適的 NPC）

把「哪些語音 / 哪些 actor 屬於這一類」抽成 FormList，再以 `IsInList` 一次性套用到大量 INFO——這是 RDO 把投放規則**集中管理**的手段（改一個 list，所有引用它的台詞投放面同步變動）。

### 3. 嫁接進 vanilla Story Manager 樹

Story Manager 是 Skyrim 觸發「環境 scene 對話」的事件樹。RDO 同時 **override vanilla 節點** 與 **新增自己的節點**：

**7 個 StoryManagerQuestNode**（4 override + 3 新）：

| FormID:plugin | EditorID | 性質 |
|---|---|---|
| `016FA1:Skyrim.esm` | GenericScenesSpecial | override vanilla |
| `03524A:Skyrim.esm` | SolitudeWinkingSkeeverScenes | override vanilla |
| `046E1A:Skyrim.esm` | PawnedPrawnConversations | override vanilla |
| `071227:Skyrim.esm` | RiftenBeggarConversations | override vanilla |
| `D0093A:Relationship Dialogue Overhaul.esp` | a_RDOKaieConfrontQuestNode | RDO 新增 |
| `FC05F2:Relationship Dialogue Overhaul.esp` | a_RDOAssaultActorNode | RDO 新增 |
| `FCF908:Relationship Dialogue Overhaul.esp` | RDOSolitudeMarketplaceScenes | RDO 新增 |

**3 個 StoryManagerBranchNode**（全部 RDO 新增）：

- `FCF905:Relationship Dialogue Overhaul.esp` RDOHaafingarHoldScenes
- `FCF906:Relationship Dialogue Overhaul.esp` RDOSolitudeScenes
- `FCF907:Relationship Dialogue Overhaul.esp` RDOSolitudeMarketScenes

手法：override `GenericScenesSpecial` / `SolitudeWinkingSkeeverScenes` 等既有節點，等於把新的環境對話 scene 掛到 vanilla 已在跑的事件流上（沿用引擎已配置好的觸發條件）；同時新增 `RDOHaafingar…` / `RDOSolitudeMarket…` 等自家 branch/quest 節點，承載 RDO 原創的城市 marketplace scene。**override 既有節點 = 蹭 vanilla 的觸發；新增節點 = 擴充新觸發點。**

### 4. Scene / Package / 新 NPC

<!-- wf-nav -->
- **Scene（34）**：31 override + 3 新。override 的多是 `DialogueSolitude…` / `DialogueRiften…` 等 vanilla 城市閒聊 scene（RDO 替換對白內容）；3 個新 scene 服務 RDO 原創角色劇情。
- **Package（74）**：54 新 + 20 override。AI package 支撐新 NPC 的行為（走位、值守），以及讓既有 NPC 配合新 scene 的動作。
- **17 個新 Npc**：兩類。其一是 RDO 原創的具名對話角色（帶完整關係檔）——`_KaieRDO "Kaie"`、`_SarynRDO "Saryn"`、`_RazitaRDO "Razita"`、`_LorionRDO "Lorion"`、`_DunoreRDO "Dunore"`、`_NubareeRDO "Nubaree"`，每個都配一條 `Relationship` record（`_KaiePlayerRelationshipRDO` 等 6 條）定義其與玩家的初始關係。其二是 encounter/leveled 用的泛型角色（`_RDOEncOrcHunter0xF`、`_RDOEncHunterNordM`、`_WEAdventurerSpellSword…`）。
- **6 個 Relationship record**：全部是上述 6 名 RDO 原創 NPC 對「玩家」的關係定義——這是 mod 名「Relationship」的字面落點，但量極小（6 條），相對於 1683 次 `GetRelationshipRank` 條件，可見**關係系統主要靠「讀 vanilla 既有關係」來分流台詞，而非自己定義大量新關係**。
- 另有少量道具支援原創角色：`_RDOKaieSwordAbsorbHealth "Kaie's Sword of Leeching"`、一批 `a_RDO*` Spell（Fireball/IceStorm/ConjureGargoyleSentinel 等，給 NPC 施法用）、若干 Book（吟遊詩人新詩節 `a_RDOBardEddaVerse*`）。

