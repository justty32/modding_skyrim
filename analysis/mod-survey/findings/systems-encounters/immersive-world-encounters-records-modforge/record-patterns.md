# 2. 關鍵 record 與模式（具體舉例）

← [原文入口](../immersive-world-encounters-records-modforge.md)

## 2. 關鍵 record 與模式（具體舉例）

### 2a. Story Manager：寄生原版 root + branch 分流

IWE 的 SM 節點全部 additive 掛在原版 root 底下，命名一律 `WE_Sette*` / `WI_Sette*`（`Sette` 是作者前綴）：

<!-- wf-nav -->
- **掛載點（原版 root，被 additive override）**：`WEQuests`（`04A601:Skyrim.esm`，World Encounter 主事件）、`WIChangeLocationThiefNode`（`023F1B:Skyrim.esm`）、`WITavernQuestNodeSHARES`（`0DEE94:Skyrim.esm`）、`DLC2WERegionNorthNode`（`01E7DF:Dragonborn.esm`）。
- **IWE branch node（SMBN，做分流）**：`WE_SetteRandomBranch`、`WE_SetteQuests`、`WI_SetteChangeLocationNode01/EM/DLC2`、`WI_SetteCLBranchLocPrior`。
- **IWE quest node（SMQN，掛實際 quest）**，按遭遇種類分桶：
  - 道路類 `WE_SetteRoads`、隨機類 `WE_SetteRandom` / `WE_SeteRandomPrisoners`、陣營類 `WE_SetteFactions`、稀有類 `WE_SetteRare`、賞金 `WE_SetteBountyHunt`、跟隨者 `SetteFollowerQuestNode`、恫嚇 `SetteDGIntimidateNode`、信使 `WI_SetteCourierNode`。
  - 換位置（進城/進村/進 tavern/見龍）一整排：`WE_SetteCLNodeLoc{Solitude,Whiterun,Riften,Markarth,Windhelm}`、`WI_SetteCLNode{City,Village,Tavern,Dragon,DB,TG}`。
  - 這就是「多樣遭遇怎麼被組織」的答案：**一個遭遇種類 = 一個 quest node**，靠 node 的條件（哪個 Hold、哪種地點、原版 WE 是否冷卻）+ 權重分流到不同戲。

### 2b. Encounter Quest：無 journal 的「演出模板」

代表 `WE_SettePrisonerEscortBandits`（`0x22367B`，"Bandits with Prisoner"），`questdiag` 顯示：

```
flags=4 priority=70 type=None event=SCPT
Stages: [0]=StartUpStage  [5]  [10]  [255]=ShutDownStage  （全部 log 為空）
Objectives: 0
```

模式：**stage 沒有日誌文字、沒有 objective**——這些 quest 對玩家「隱形」，只是個容器。stage 純粹當作 fragment script 的狀態機 step（5、10 = 演出階段，255 = 清場）。掛兩個 script：共用的 `WEScript`（2 props）+ 自動產生的 `QF__0522367B`（13 props，stage fragment）。

少數遭遇**有** objective（例如 `SetteFollowerQuest` 有 `objective[10] "<Alias=Follower01> is waiting for you"`），那是會給玩家任務感的（招募跟隨者）；純路邊戲一律無 journal。

### 2c. Quest aliases：runtime 隨機填演員 + 環境 alias

`WE_SetteLeftForDead01Scene`（`0x835F66`）的 host quest（`0x835F65`）有 14 個 alias，分三類：

- **演員 alias**（runtime 從 LeveledNpc 填）：`Wanderer`(#16)、`CaptiveAlias`(#44)、`BanditAlly01/02`(#45/46)、`ThiefAlly01/02`(#47/48)。同一個遭遇用 alias 索引區分「這次是 bandit 版還是 thief 版」。
- **位置/觸發 alias**：`TRIGGER`(#1)、`LocationCenterMarker`(#42)、`TravelMarker1/2`(#9/10)——給 AI package 當 travel target。
- **環境偵測 alias**：`myHoldLocation`/`myHoldContested`/`myHoldImperial`/`myHoldSons`(#4/6/7/8)——偵測當前 Hold 歸屬，讓對白/陣營隨內戰狀態變。

演員池：`LeveledNpc` 65 個，如 `_SetteLCharWEWandererAll`、`_SetteLcharWEBountyHunter`、`_SetteLCharWEPrisonerHoldAll`、`_SetteLCharWEBattleRoyalTeamB/C`。**一個 alias fill from 一個 LVLN list = 每次遭遇演員不同**。

### 2d. Scene：Dialog / Package / Timer 三種動作交織

`scnscan` 顯示 56 個 scene 大量用非對話動作。代表 `WE_SetteLeftForDead01Scene`（`0x835F66`，`scenediag`）：

```
actor: alias #16  behaviorFlags=DeathEnd（演員死亡即結束 scene）
phases (1)
actions (3):
  Type=Dialog   ActorID=16  Topic=0x835F67  Flags=Looping  LoopingMin=1 Max=5
  Type=Package  ActorID=16  Packages=[891252]（走到 marker 的 Travel package）
  Type=Timer    ActorID=16  TimerSeconds=10
```

更複雜的多 phase 例：`WI_SetteTGScene`（12 動作、8 個 Package 動作跨 phase 0→4，多演員走位）；`WERJ_SetteDLC2Drunk02ContestScene`（賭酒，15 動作、9 非對話：每 phase 一個 0.9s Timer + 跨 phase Package）。模式：**Package 動作負責走位/姿勢，Timer 動作負責節奏，Dialog 動作負責台詞，phase 推進串起整段戲**。

### 2e. Dialogue INFO 的 CTDA：反應性對白的核心

scene 對白 topic 用條件做出分歧，這是 IWE「有靈魂」的地方。`TOPIC 0x84F4D8` 一個 topic 掛 8 個 INFO，靠條件選播：

```
INFO 0x84F4D9 "Err...what's a Nightingale?"  conds=9:
  GetStage(0x835F65) == 70
  GetIsAliasRef alias#47 == 1          ← 只有 ThiefAlly01 版才講
  HasKeyword(0x84A3D2) == 1
  GetEquipped(Nightingale 各部位) == 1 [OR 串]   ← 玩家穿夜鶯裝才觸發
INFO 0x84F4DB "Wait, isn't he from the Guild?"  conds=10:
  GetStageDone(0x01F326 TG 主線, stage 200) == 1   ← 玩家完成盜賊公會主線才講
  GetIsVoiceType(0x94C82D) == 0
  GetEquipped(Nightingale...) == 0     ← 沒穿才講（互斥分支）
```

模式：**一個 scene topic = 多個 INFO，靠 `GetIsAliasRef`（哪個演員被填進來）+ `GetStage`（演到第幾步）+ `GetEquipped`/`GetStageDone`/`GetIsVoiceType`（玩家狀態/世界狀態）做精細分歧**。這跟既有筆記 [conditioned-hello-one-topic-many-infos] 完全同構，只是搬到 scene 語境。

### 2f. AI Package：原版 template + alias marker target

`WE_SetteLFDCaptivePackage`（`0x891252`，`packagediag`）：

```
PackageTemplate -> 016FAA:Skyrim.esm   ← 原版 Travel template
Flags = IgnoreCombat, WeaponsUnequipped
PreferredSpeed = Run
Data: [0] PackageDataLocation target=LocationFallback(NearSelf)  [2][4] Bool
ProcedureTree: 0 branch（完全靠 template + data 填充，不自己定義 procedure）
```

模式：**不從零寫 package procedure，而是引用原版 template（Travel `016FAA`、Sandbox 等），只覆寫 flags + PackageData**，target location 指到 quest 的 travel-marker alias。488 個 package 幾乎都是這種薄包裝。

---

