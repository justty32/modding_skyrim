# Relationship Dialogue Overhaul (RDO Final, v1187) — modforge-implications

[返回入口](../relationship-dialogue-overhaul.md)

## 對 ModForge 的意義

ModForge 目前的 dialogue/quest builder 是**「新增導向」**：它能做 storyEvent 掛 SM、scene phase → dialog、AI package、以及一組 condition（見 ModForge CLAUDE.md「已落地功能」與 `src/ModForge.Core/Generator.Build.Conditions.cs`）。RDO 揭示了三個 ModForge **尚未涵蓋** 的能力，若要做「對話包」式內容缺一不可。務實列出差距：

### (a) override 既有 vanilla record 的能力 —— 完全沒有

ModForge 的 dialogue 路徑只把 condition 掛到**自己建的** INFO 上：`WireDialogueConditions()` 用 `dialogResponsesByEd.TryGetValue(d.EditorId, …)` 找的是 spec 內自建 record（`src/ModForge.Core/Generator.Build.Conditions.cs:128-159`）。沒有「取出某個 Skyrim.esm 既有 Quest / DialogTopic / INFO，覆寫它、往裡塞 response」的入口。而 RDO 的 1612 個 override（含 51 個 vanilla Quest、1304 個 vanilla INFO）正是靠此。Mutagen 本身支援 `GetOrAddAsOverride`（ModForge 已在 navmesh/exterior-cell 等 world 路徑用到 override），但 **dialogue/quest builder 沒有暴露這條路**。這是最大、也最根本的差距。

### (b) 以 condition 模板批次套用到「一類 NPC」 —— 沒有

ModForge 的 condition 是「逐句手寫」：spec 裡每個 dialogue 條目各自帶一個 `conditions[]` 陣列。RDO 的玩法是**一束台詞共用一組投放條件**（同一 VoiceType + Faction + RandomPercent），靠 FormList 集中管理目標集合。ModForge 沒有：
- FormList builder（RDO 的 18 個 `aaa_RDOVoices*` 名單機制）；
- 「把一組 condition 套用到 N 句台詞」的模板/批次語法。
要做對話包，需要一個「投放模板」抽象，而非逐句複製條件。

### (c) `GetIsVoiceType` / `IsInList` 這類 condition 的 spec 支援 —— 缺

ModForge 的 `SupportedConditionFunctions`（`Generator.Build.Conditions.cs:6-13`）目前涵蓋 `GetInFaction`、`GetRelationshipRank`、`GetRandomPercent`、`GetIsID`、`GetActorValue` 等——與 RDO 高頻條件有交集，但**關鍵的 `GetIsVoiceType`（RDO 第一名，9245 次）與 `IsInList`（936 次）都不在支援清單內**。沒有 `GetIsVoiceType`，就無法做「投到一整類語音的 NPC」這個 RDO 最核心的手法；沒有 `IsInList`，就無法配合 FormList 名單投放。`LocationHasKeyword`、`GetPlayerTeammate`、`GetVMQuestVariable` 也都缺。

### 小結（差距優先序）

| 缺口 | 對「做對話包」的阻塞程度 |
|---|---|
| override 既有 vanilla quest/topic/INFO | 致命——沒有它根本無法「接管 vanilla 對話」 |
| `GetIsVoiceType` + `IsInList` condition | 致命——RDO 規模化投放的兩支主刷子 |
| FormList builder | 高——投放名單的集中管理載體 |
| condition 批次/模板套用 | 高——否則逐句手寫無法規模化 |
| `GetPlayerTeammate` / `LocationHasKeyword` / `GetVMQuestVariable` | 中——投放維度的補強 |

不誇大：ModForge 現有的 condition framework 與 SM 掛載能力，已經是這條路的**地基**（BuildCondition 的 dispatch 架構加幾個 case 即可補上 VoiceType/IsInList）。真正缺的是「override 入口」與「批次投放」這兩個結構性能力——前者是 Mutagen API 已有、ModForge 未暴露；後者是純粹的 spec 設計工作。RDO 證明這條路可行且有明確的工程模式可抄，但它與 ModForge 當前「新增導向」的設計是兩種不同的內容生產範式。

→ 對照建議見 `others/modforge-relevance.md`。
