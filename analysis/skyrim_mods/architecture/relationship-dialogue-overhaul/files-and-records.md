# Relationship Dialogue Overhaul (RDO Final, v1187) — files-and-records

[返回入口](../relationship-dialogue-overhaul.md)

## 檔案結構

| 部分 | 內容 | 大小 |
|---|---|---|
| `Relationship Dialogue Overhaul.esp` | 全部邏輯：9765 records | 3 MB |
| BSA（語音 archive） | 對應台詞的 `.fuz`（語音 + lip sync）；無 loose 工具解包 | 116 MB |

ESP 即全部可分析素材。每一句 RDO 新台詞理論上對應 BSA 裡一個 `.fuz`——這也是為什麼台詞量（6650 新 INFO）撐起 116 MB 語音。

## record 解剖

### 全體 record 分佈（按來源 plugin 切）

判別法：dump 中每個 record header 形如 `[FormID:plugin名] Type EditorID`。**FormID 高位（plugin index）決定該 record 的「歸屬」**——`:Relationship Dialogue Overhaul.esp]` 是 RDO 自己新增的 record；`:Skyrim.esm]`（或 `:Dragonborn.esm` 等）是 RDO **override 既有 vanilla record**（同一 FormID、被 RDO 的版本覆蓋）。

| Type | vanilla override | RDO 新增 | 小計 |
|---|---:|---:|---:|
| DialogResponses (INFO) | 1304 | 6650 | 7954 |
| DialogTopic | 181 | 1151 | 1332 |
| Quest | 51 | 101 | 152 |
| Package | 20 | 54 | 74 |
| DialogBranch | 2 | 42 | 44 |
| Scene | 31 | 3 | 34 |
| GlobalFloat | 0 | 21 | 21 |
| PlacedNpc | 10 | 8 | 18 |
| FormList | 0 | 18 | 18 |
| Npc | 0 | 17 | 17 |
| Spell | 0 | 15 | 15 |
| MagicEffect | 1 | 13 | 14 |
| PlacedObject | 0 | 12 | 12 |
| Book | 0 | 10 | 10 |
| Cell | 7 | 1 | 8 |
| StoryManagerQuestNode | 4 | 3 | 7 |
| Relationship | 0 | 6 | 6 |
| Class | 0 | 5 | 5 |
| StoryManagerBranchNode | 0 | 3 | 3 |
| CombatStyle | 0 | 3 | 3 |
| GlobalShort | 1 | 2 | 3 |
| Weapon | 0 | 2 | 2 |
| Outfit | 0 | 2 | 2 |
| Faction | 0 | 2 | 2 |
| Armor / Perk / ObjectEffect / MiscItem / Message / LeveledNpc / Container | 0 | 各 1~3 | — |
| **總計** | **1612** | **8153** | **9765** |

來源命令：`grep -E '^  \[[0-9A-F]{6}:[^]]+\] ' /tmp/mfdump/rdo.txt`（2 空格縮排 = 頂層 record header，恰好 9765 行），再按 plugin 與 Type 拆。

### override vs 新增：FormID 判別法（具體例證）

**override 既有 vanilla record**（FormID 屬 Skyrim.esm，被 RDO 整個覆寫，把新 INFO 塞進去）：

- `[04C49D:Skyrim.esm] Quest FollowerCommentary01 "Entrances to Dungeons"`
- `[04C6EB:Skyrim.esm] Quest FollowerCommentary02 "Follower sees an impressive view"`
- `[0367DD:Skyrim.esm] Quest DialogueSolitudeErikurScene1 "Erikur House Scene 1"`
- `[016FA6:Skyrim.esm] Quest DialogueGenericSceneSpecial01`
- `[096500:Skyrim.esm] DialogResponses`（戰鬥嘲諷 INFO，RDO 加入新 response「It's... nothing...」+ 三條 condition）

**RDO 新增 record**（FormID 屬 RDO 自己的 plugin index，EditorID 多帶 `RDO`/`a_RDO`/`_…RDO` 前綴）：

- `[FCF905:Relationship Dialogue Overhaul.esp] StoryManagerBranchNode RDOHaafingarHoldScenes`
- `[CE2329:Relationship Dialogue Overhaul.esp] Npc _KaieRDO "Kaie"`
- `[04767F:Relationship Dialogue Overhaul.esp] GlobalFloat a_RDO_FCMDNextComment`

一句話：**看 `:` 後面的 plugin 名**。屬 `Skyrim.esm`/DLC = override vanilla；屬 `Relationship Dialogue Overhaul.esp` = RDO 原創。

### 一個 vanilla DialogResponses override 的解剖

`/tmp/mfdump/rdo.txt` 的戰鬥嘲諷話題 `[013EE3:Skyrim.esm] DialogTopic`（category=Combat / subtype=Attack）底下，RDO 覆寫的 INFO：

```
[04949B:Skyrim.esm] DialogResponses
    response[1] (Anger): "For Skyrim!"
    condition: GetRandomPercentConditionData
    condition: GetIsIDConditionData -> 000007:Skyrim.esm
    condition: GetIsVoiceTypeConditionData
    condition: HasKeywordConditionData
    condition: GetInFactionConditionData
    condition: GetInCurrentLocConditionData
    condition: GetIsEditorLocationConditionData
```

讀法：這是 vanilla 戰鬥喊話 INFO（FormID 屬 Skyrim.esm），RDO 把新 response 與一整串 condition 灌進去。`GetIsID -> 000007:Skyrim.esm` 是玩家（vanilla Player FormID 0x7）。`GetIsVoiceType` + `GetInFaction` 把這句限定到某一「類」NPC，`GetRandomPercent` 讓它只在一定機率下觸發。**這正是 RDO 的縮影：覆寫 vanilla 容器，內容靠條件投放。**

