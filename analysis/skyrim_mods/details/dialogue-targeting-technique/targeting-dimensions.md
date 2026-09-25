# 大規模對話如何精準投放：RDO 的 condition 投放技術 — targeting-dimensions

[返回入口](../dialogue-targeting-technique.md)

## 2. 四大投放維度

### 2.1 誰能說（身份過濾）

身份過濾決定「**這句話有資格從誰嘴裡發出**」。RDO 的規模化核心是 `GetIsVoiceType`：Skyrim 的每個 NPC 都被指派一個 VoiceType（如 `FemaleNord`、`MaleBrute`），數以萬計的 NPC 共用區區數十個 VoiceType。對 VoiceType 投放，等於一次命中所有共用該嗓音的 NPC——而且**已配好同一套語音檔**，不需額外配音。

證據——RDO 的 quest 命名直接揭露此架構。`grep -oE 'quest=aa_RDO[A-Za-z]+'` 得到的 44 個 quest 幾乎全是「`<性別><嗓音>NonHate`」一一對應一個 VoiceType：

```
quest=aa_RDOFemaleNordNonHate
quest=aa_RDOMaleBruteNonHate
quest=aa_RDOFemaleSultryNonHate
quest=aa_RDOMaleCommonerAccentedNonHate
... （共 800 筆 INFO 掛在 *NonHate quest 下；後綴統計：NonHate 800、其餘僅 ThievesGuildUniqueVoices）
```

也就是說，RDO 把台詞庫**先按 VoiceType 切成數十桶**，每桶是一個 quest；桶內每筆 INFO 再用 `GetIsVoiceType` 條件鎖死該嗓音。topic 名同樣編碼了嗓音，例如 `521050` 所屬 topic 為 `MYoungEagerNonHateGoodbye`（`[07A3C1] DialogTopic MYoungEagerNonHateGoodbye`，行 48970）。

其他身份維度由細到粗：

- **GetInFaction（7224）**：投給某陣營全員。常與 VoiceType 疊用做交集（嗓音 ∩ 陣營）。
- **GetIsRace（446）/ GetPCIsRace（玩家種族）**：種族判定。vanilla 的種族自報 INFO `[043AD9] DialogResponses`（行 911，response "Khajiit."）就疊了 `GetPCIsRace ×2 + GetIsSex + GetIsRace ×2 + GetIsVoiceType ×3` 來精確鎖定。
- **IsInList（936）**：以 FormList 列舉一組 record（NPC 群、地點群），是「半指名」。
- **GetIsID（1396）**：指名到底，鎖死單一 actor。例：`condition: GetIsIDConditionData -> 000007:Skyrim.esm`（PlayerRef，出現 271 次，多用來判斷對話另一方是玩家）、`-> 002B6C:Dawnguard.esm`（Serana，127 次，見 §3）。RDO 只在「這句話確實只屬於某個唯一 NPC」時才用它。

### 2.2 關係狀態（動態化）—— mod 名的由來

這是 RDO 區別於普通對話 mod 的招牌。同一個 NPC，隨著與玩家的關係改變，會講出語氣不同的台詞。

- **GetRelationshipRank（1683）**：讀取 NPC 對玩家的關係等級（CK 中 -4 Archnemesis … 0 Acquaintance … +4 Lover）。RDO 用它把同一情境（如 Hello）的台詞分成「敵意 / 中性 / 友好 / 摯愛」幾組，每組掛不同的 rank 閾值。quest 名的 `NonHate` 後綴正是第一層粗篩——「關係沒到 Hate 才進這桶」，桶內再用 GetRelationshipRank 細分。
- **GetPlayerTeammate（2142）**：判斷該 NPC 此刻是否為現役隨從。隨從專屬的旅途閒聊全靠它，例如 §3 的 Serana 台詞。
- **GetActorValue（1811）/ GetActorValuePercent（283）**：讀任意 actor value，可查 disposition（好感度）、技能、或血量百分比（戰鬥中受傷台詞）。

範例——一筆關係化的 Goodbye（`[521050] DialogResponses`，行 49009，topic `MYoungEagerNonHateGoodbye`）：

```
[521050:Relationship Dialogue Overhaul.esp] DialogResponses
    response[1] (Happy): "Oh, goodbye then."
    condition: GetIsVoiceTypeConditionData      ← 嗓音 = MaleYoungEager
    condition: GetRandomPercentConditionData     ← 擲骰（不重複）
    condition: GetRelationshipRankConditionData  ← 關係達到某友好門檻
    condition: GetInFactionConditionData         ← 三個陣營交集進一步收窄
    condition: GetInFactionConditionData
    condition: GetInFactionConditionData
```

emotion 標 `(Happy)` 配上 GetRelationshipRank：友好門檻沒到的玩家，會落到同 topic 下另一組（emotion 與台詞皆不同）的 INFO。

### 2.3 情境（脈絡）

決定「**現在這個當下適不適合講**」。分兩類：

**NPC / 地點脈絡**
- `LocationHasKeyword`（1384）/ `GetInCurrentLoc`（748）/ `GetInWorldspace`（605）/ `GetInCell`（389）：把台詞綁到地點。LocationHasKeyword 最常用，因為它對「一類地點」（城市、酒館、地城）投放而非單一地點，延續了 RDO「按類投放」的一貫思路。
- `GetSleeping`（817）：NPC 在睡覺時通常不該被搭話，或反而有專屬「半夢半醒」台詞。

**玩家當下狀態**
- `IsSneaking`（815）：玩家潛行時 NPC 的反應。
- `IsInCombat`（377）：戰鬥語境的 taunt / hit 台詞。
- `IsInDialogueWithPlayer`（369）：確保是面對面對話而非旁白觸發。

範例——一筆把睡眠 / 潛行 / 地點 / 陣營全疊起來的 Idle 評論（vanilla `HirelingIdles` topic 被 RDO 覆寫並加掛腳本，`[0284F7] DialogResponses`，行 4250；topic `[055DEB] DialogTopic HirelingIdles`，category=Misc subtype=Idle，行 4248）：

```
[0284F7:Skyrim.esm] DialogResponses
    script: RDO_ThisQuestSetStageTIF [2 prop(s)]
    response[1] (Happy): "The College of Winterhold is an amazing sight. I've never set foot on the grounds, but always wanted to."
    condition: ConditionGlobalBinaryOverlay     ← 全域開關（功能是否啟用）
    condition: GetVMQuestVariableConditionData    ← 輪替用 quest 變數
    condition: GetIsIDConditionData -> 02427D:Skyrim.esm  ← 指名某隨從
    condition: GetActorValueConditionData
    condition: GetInFactionConditionData
    condition: GetSleepingConditionData           ← NPC 不在睡
    condition: IsSneakingConditionData            ← 玩家不在潛行
    condition: IsInListConditionData
    condition: GetQuestRunningConditionData (×3)
    condition: GetStageDoneConditionData
    condition: GetInWorldspaceConditionData       ← 限定在某 worldspace
    condition: GetInCurrentLocConditionData       ← 限定在某 location（學院）
```

台詞內容（提到 College of Winterhold）與 `GetInWorldspace + GetInCurrentLoc` 嚴格對應——**這句話只在 NPC 人在學院、清醒、玩家沒潛行時才會冒出來**。

### 2.4 隨機不重複

`GetRandomPercent` 出現 **3112 次**，是排名第三的 condition——幾乎每一句 Hello / Goodbye / Idle 評論都掛它。機制：condition 取一個 0–99 的隨機數，與閾值比較（如 `GetRandomPercent <= 25`），只有擲骰命中才放行。

效果：當一群符合身份 + 情境的 INFO 同時「合格」，引擎不會固定挑第一條，而是讓每條各自擲骰，命中者中再挑——於是同一個 NPC 反覆觸發 Hello 時，會在好幾句之間自然輪替，不會每次都同一句。

它常與兩類同伴搭配：
- **GetVMQuestVariable（1476）/ GetStageDone（363）**：quest 變數做「狀態輪替」——講過 A 句就把變數推進，下次只剩 B、C 句合格，做出「不重複且有序」的對話。
- **`a_RDO_<voicetype>NextComment` 全域 float 冷卻計時器**（dump 開頭即列出 20 個，如 `[047683] GlobalFloat a_RDO_FNORDNextComment`、`[04768A] GlobalFloat a_RDO_MDRNKNextComment`，行 6 起）：每個 VoiceType 一個計時器，配 `ConditionGlobal` 判斷「距上次評論是否已過冷卻」，避免同嗓音 NPC 連珠炮刷屏。

擲骰（每句機率）+ quest 變數（有序輪替）+ 冷卻全域（節流）三者疊加，構成 RDO 的「不重複」層。

