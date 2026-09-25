# 大規模對話如何精準投放：RDO 的 condition 投放技術 — info-structure-and-recipes

[返回入口](../dialogue-targeting-technique.md)

## 3. 一個完整 INFO 的解剖

挑 Serana（Dawnguard 唯一隨從）的隨從旅途閒聊。topic `[07F4D6] DialogTopic SeranaNonHateHello`（category=Misc subtype=Hello，quest=`aa_RDODLC1SeranaNonHate`，行 50326）。

```
[20AA1D:Relationship Dialogue Overhaul.esp] DialogResponses
    response[1] (Happy): "So where are we off to, now?"
    condition: GetIsVoiceTypeConditionData          (1)
    condition: IsInDialogueWithPlayerConditionData  (2)
    condition: GetVMQuestVariableConditionData       (3)
    condition: GetPlayerTeammateConditionData        (4)
    condition: GetVMQuestVariableConditionData       (5)
    condition: GetRelationshipRankConditionData      (6)
    condition: GetStageDoneConditionData             (7)
    condition: GetInWorldspaceConditionData          (8)
    condition: GetInWorldspaceConditionData          (9)
    condition: LocationHasKeywordConditionData       (10–16，共 7 個)
```

逐行翻成白話（運算子 / 數值依語意推斷，dump 未印出）：

| # | condition | 白話 |
|---|-----------|------|
| 1 | GetIsVoiceType | 說話者必須是 Serana 的嗓音（FemaleYoungEager 系）|
| 2 | IsInDialogueWithPlayer | 此刻正面對玩家（是搭話而非背景旁白）|
| 3 | GetVMQuestVariable | RDO 對話狀態機變數允許此句（輪替閘）|
| 4 | GetPlayerTeammate | Serana 必須是**現役隨從**——非隨從時整句失格 |
| 5 | GetVMQuestVariable | 第二個狀態變數（多軸輪替）|
| 6 | GetRelationshipRank | 關係達到友好門檻（呼應 emotion `Happy` 與 NonHate）|
| 7 | GetStageDone | 某前置劇情階段已完成 |
| 8–9 | GetInWorldspace ×2 | 限定在某些 worldspace（戶外旅途語境，OR 關係）|
| 10–16 | LocationHasKeyword ×7 | 當前地點需帶某類 keyword（多個做地點分類交集 / 並集）|

**綜合語意**：這句「So where are we off to, now?」只會在——*說話者是 Serana 嗓音、她是我現役隨從、與我關係夠好、相關劇情已推進、我們正在某些戶外地點面對面、且輪替變數與擲骰都放行* ——時才從她嘴裡冒出。把任一條件去掉，這句台詞就會洩漏到不該說它的場合或 NPC。

同 topic 下的 `[20AA19]`（"I'm glad you're here with me."）、`[20AA1A]`（"Just you and me against the world, now."）共用前 7 條身份 / 關係 / 狀態條件，僅在後段地點條件上分流——這正是「同一桶台詞靠 condition 尾段做最後分配」的縮影。

## 4. DialogBranch / DialogTopic 的角色

condition 掛在 **`DialogResponses`（INFO）這一層**——精準投放的全部邏輯都在這裡。上層兩級只是**分類容器**：

- **DialogTopic**：一組 INFO 的歸類。它帶 `category`（Combat / Detection / Misc / Topic）、`subtype`（Hello / Goodbye / Idle / Attack / Hit …）、所屬 `quest`、與可選 `branch`。subtype 決定**引擎在什麼時機輪詢這組 INFO**（玩家靠近 → Hello；離開 → Goodbye；閒置 → Idle）。dump 中 `category / subtype` 分布（`grep -oE 'category=... subtype=...'`）前段為：Topic/Custom 153、Misc/Hello 106、Misc/Idle 76、Misc/Goodbye 71、Detection/NormalToCombat 56、Combat/Taunt 55……
- **DialogBranch**：對 player-initiated 對話樹做更細的分支管理。RDO 的 INFO 絕大多數 `branch=<null>`（1179 筆無 branch），少數劇情對話才用具名 branch（如 `RDOKaieQuestGreet`、`RDOFriendConversationStart`）。

換句話說：**topic/branch 回答「這是什麼類型、何時輪詢」；condition 回答「在合格候選裡，到底投給誰、現在能不能講」。** topic 的 subtype 把搜尋空間先縮到「此刻該類事件的 INFO」，condition 再在其中做最終的 NPC / 情境 / 隨機篩選。

## 5. 可複製的配方（供 ModForge 參考）

把上面歸納成「程式化生成一句規模化台詞」要產出的 condition 範本。要訣是**從寬到窄分層**，每層各管一個投放維度：

**最小規模化配方（一句通用 Hello）**

| 層 | condition | 設定 | 作用 |
|----|-----------|------|------|
| 身份（必填）| `GetIsVoiceType == <某 VoiceType>` | 選一個目標嗓音 | 一次命中所有共用該嗓音、已有配音的 NPC |
| 關係（動態）| `GetRelationshipRank >= <N>` | N=1 友好 / 3 摯友 | 同句的不同關係版本各設不同 N |
| 隨機（防重複）| `GetRandomPercent <= <P>` | P=20~30 | 多句同層時各自擲骰輪替 |

即：`GetIsVoiceType == FemaleNord  AND  GetRelationshipRank >= 1  AND  GetRandomPercent <= 25`。

**收窄到特定族群 / 情境（疊加，AND 交集）**

- 加 `GetInFaction == <faction>`：限該陣營（嗓音 ∩ 陣營）。
- 加 `GetPlayerTeammate == 1`：限現役隨從（旅途閒聊必加）。
- 加 `LocationHasKeyword == <locKeyword>` 或 `GetInCurrentLoc == <loc>`：綁地點類別。
- 加 `IsInCombat == 0` / `GetSleeping == 0` / `IsSneaking == 0`：排除不合時宜的場合。

**指名單一 NPC（放棄規模化時）**

- 用 `GetIsID == <actor FormID>` 取代 `GetIsVoiceType`，其餘層照舊。只在「這句確實獨屬某 NPC」時用。

**節流 / 輪替（進階，可選）**

- 配一個 per-voicetype 全域 float 計時器 + `GetGlobalValue` 比較，做冷卻防刷屏（對應 RDO 的 `a_RDO_*NextComment`）。
- 配 quest 變數 + `GetVMQuestVariable` / `GetStageDone`，把多句做成有序、不回頭的輪替序列。

**鐵律**：condition 是 AND 交集，且必須**全部命中**才放行；漏掉任一個收窄條件，台詞就會洩漏到錯誤的 NPC 或場合（如忘記 `GetPlayerTeammate` 會讓隨從專屬台詞跑到路人嘴裡）。把容器（topic subtype）選對來框定觸發時機，再用 condition 串逐層收窄——這就是「一份 ESP 精準餵養上萬 NPC」的全部祕密。

---

### 取證索引（dump 行號 / FormID）

- condition 頻率：`grep -oE 'condition: [A-Za-z]+' /tmp/mfdump/rdo.txt | sort | uniq -c | sort -rn`
- 解剖 INFO：`[20AA1D:Relationship Dialogue Overhaul.esp] DialogResponses`（行 50523），topic `[07F4D6] DialogTopic SeranaNonHateHello`（行 50326）
- 關係維度：`[521050:Relationship Dialogue Overhaul.esp] DialogResponses`（行 49009），topic `[07A3C1] DialogTopic MYoungEagerNonHateGoodbye`（行 48970）
- 情境維度：`[0284F7:Skyrim.esm] DialogResponses`（行 4250），topic `[055DEB] DialogTopic HirelingIdles`（行 4248）
- 身份 / 種族：`[043AD9:Skyrim.esm] DialogResponses` "Khajiit."（行 911）
- 冷卻全域：`[047683] GlobalFloat a_RDO_FNORDNextComment` 等（dump 行 6 起）
- quest 桶：`grep -oE 'quest=aa_RDO[A-Za-z]+' /tmp/mfdump/rdo.txt | sort -u`（44 個，幾乎全為 `<嗓音>NonHate`）
