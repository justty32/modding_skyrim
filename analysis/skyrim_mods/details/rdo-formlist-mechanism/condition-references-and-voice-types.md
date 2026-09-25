# RDO 的 FormList 投放機制 — condition-references-and-voice-types

[返回入口](../rdo-formlist-mechanism.md)

## 2. FormList 怎麼被 condition 引用

`IsInList` condition 在 dialogue 中出現 **936 次**（dump `grep -c 'IsInList' = 936`）。離線解碼每一筆 `IsInList` 指向的 FormList 與比較值，結果單一得驚人：

```
-- IsInList referenced FormLists (count) --
   936  aaa_RDOPreventedActorsList     ← 936 次全指這一個

-- IsInList list==value breakdown --
   923  aaa_RDOPreventedActorsList ==0  ← 守門：NOT in list
    13  aaa_RDOPreventedActorsList ==1  ← 邊緣用途（見下）
```

**沒有任何一筆 `IsInList` 指向 Voices 名單。** Voices FormList 從不透過 `IsInList` 投放；它們只透過 `GetIsVoiceType`（把 VoiceType-or-List 槽指向整個 FormList）使用，見 §3。

### 2.1 真實 INFO：IsInList 當排除守門（==0）

解碼一筆典型的 RDO 自製 follower 台詞（`[BF944D]`，完整 condition 串）：

```
[BF944D] DialogResponses
    GetIsVoiceType EqualTo 1 v=FemaleCommoner  (013ADE:Skyrim.esm) [OR]
    GetIsVoiceType EqualTo 1 v=FemaleEvenToned (013ADD:Skyrim.esm) [OR]
    GetIsVoiceType EqualTo 1 v=FemaleYoungEager(013ADC:Skyrim.esm)
    GetRandomPercent LessThanOrEqualTo 97
    IsInList        EqualTo 0 list=aaa_RDOPreventedActorsList   ← 守門
    GetRelationshipRank EqualTo 4
    GetInFaction    EqualTo 0 faction=PlayerMarriedFaction
    GetInFaction    EqualTo 0 faction=CurrentFollowerFaction
```

讀法：嗓音是三種女性泛用嗓音之一（OR 群）**且** 隨機 97% 過關 **且** `IsInList(aaa_RDOPreventedActorsList) == 0`（**這個 NPC 不在排除名單**）**且** 關係等級=4 **且** 不在婚姻/隨從陣營 → 才講這句。

`IsInList==0` 在此是**否決閘**：把這句話投給「符合嗓音/關係條件、但又不在黑名單上的所有 NPC」。

另一筆（`[F37AA5]`，給「會跑腿的小孩」的台詞）同樣模式：

```
[F37AA5] DialogResponses
    GetIsID EqualTo 1 id=Player
    GetRelationshipRank GreaterThanOrEqualTo 1
    GetInFaction EqualTo 0 faction=CurrentFollowerFaction
    GetIsVoiceType EqualTo 1 v=FemaleChild
    GetAllowWorldInteractions EqualTo 1
    IsInList EqualTo 0 list=aaa_RDOPreventedActorsList   ← 守門
    GetInFaction EqualTo 0 faction=BYOHRelationshipAdoptionFaction
```

「目標是 `FemaleChild` 嗓音、關係≥1、不在排除名單」——投放靠 `GetIsVoiceType` 鎖嗓音，`IsInList==0` 只負責剔除被列入黑名單的個別 NPC。

### 2.2 邊緣的 ==1 用途（13 筆）

13 筆 `IsInList==1` 不是「白名單投放」，而是 RDO 覆寫 vanilla follower INFO 時保留的 vanilla OR 群的一部分。例如 `[0D8E14]`：

```
[0D8E14] "All right."
    GetIsVoiceType    EqualTo 0 v=FemaleSultry          [OR]
    GetVMQuestVariable EqualTo 0                        [OR]
    IsInList          EqualTo 1 list=aaa_RDOPreventedActorsList
    GetIsVoiceType    EqualTo 1 v=VoicesFollowerNeutral
    GetInFaction      EqualTo 1 faction=CurrentFollowerFaction
```

`==1` 在這裡是「**如果**這個 NPC 在排除名單上，就走 vanilla 的這條 follower 回應」——即被排除者退回原版台詞的回退分支，屬於相容性收尾，不是主力投放手段（僅 13/936 ≈ 1.4%）。

### 2.3 PreventedActorsList 被掛在哪

離線統計「哪些 record 持有指向各 FormList 的 FormLink」：

```
aaa_RDOPreventedActorsList  被引用：DialogResponses 936、Quest 76
aaa_RDOVoicesFemaleList     被引用：DialogResponses 58、Quest 2
aaa_RDOVoicesMaleList       被引用：DialogResponses 60、Quest 2
aaa_RDOVoicesAll            被引用：DialogResponses 20、Quest 1
aaa_RDOPreventedActorsHatePL 被引用：（無）
aaa_RDOPreventedActorsFriend 被引用：（無）
```

排除名單橫跨 936 句台詞 + 76 個 quest 的 condition——是整個 mod 共用的單一守門 list。`HatePL` / `Friend` 兩個排除名單在 ESP 內**完全沒被引用**，是為未來/補丁預留的空殼。

---

## 3. Voices FormList 與 GetIsVoiceType 的分工

這是本主題最容易誤判的一點。數字（離線統計 dialogue condition）：

```
Total GetIsVoiceType in dialogue conditions: 9245
   - 指向「單一 VoiceType」 : 9035  (97.7%)
   - 指向「Voices FormList」 :  210  (2.3%)
Total IsInList               :  936  （全部指 PreventedActorsList，與 Voices 無關）
```

**結論：RDO 以「`GetIsVoiceType` 逐句直接鎖單一嗓音」為絕對主力**（9035 次）。`GetIsVoiceType` 的參數槽（VoiceType-or-List）原生就能塞「一個 VoiceType」或「一個裝 VoiceType 的 FormList」；RDO 絕大多數選擇逐句指名單一嗓音，常以 `[OR]` 串接幾個嗓音（如 §2.1 的三條 Female OR 群）。

Voices FormList 只在 **210 次**「想用一條 condition 涵蓋一整組嗓音」時當捷徑（解碼前幾名）：

```
   60  GetIsVoiceType -> aaa_RDOVoicesMaleList
   58  GetIsVoiceType -> aaa_RDOVoicesFemaleList
   20  GetIsVoiceType -> aaa_RDOVoicesAll
   12  GetIsVoiceType -> _RDO_OriginalVoicesFollowerAll
    4  GetIsVoiceType -> aaa_RDOVoicesUnique
    3  GetIsVoiceType -> a_RDO_USKPVendorMiscVoices
   ...（其餘為 vanilla 既有的 VoicesFollowerNeutral 等清單）
```

也就是說，Voices FormList 的角色是「**把 N 個 OR 的 `GetIsVoiceType` 壓成一條**」——當某句話要投給「全部男性嗓音」時，用 `GetIsVoiceType==1 voice/list=aaa_RDOVoicesMaleList` 一條，省掉 27 條 OR。但 RDO 大部分台詞要鎖的是 1～3 種特定嗓音（語氣要對），所以逐句指名才是常態。

**分工總結：**
- `GetIsVoiceType(單一 VoiceType)` = 主力，精準到「語氣對的那幾種嗓音」。
- `GetIsVoiceType(Voices FormList)` = 捷徑，用在「要涵蓋一大組嗓音」的少數場合（集中管理 + 一條搞定）。
- `IsInList(PreventedActorsList==0)` = 與嗓音正交的**全域排除閘**，每句台詞都加一條，剔除不該講話的個別 NPC。

三者**並用、各司其職**，不是「擇一」。

---

