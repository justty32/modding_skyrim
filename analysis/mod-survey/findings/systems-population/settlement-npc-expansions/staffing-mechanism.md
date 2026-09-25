# settlement-npc-expansions — staffing-mechanism

← [調查入口](../settlement-npc-expansions.md)

## Mechanism pattern — 三者的共同骨架（＝「單點聚落 staffing 配方」）

**unique NPC base（指 vanilla race/class/voice/outfit/combatStyle）→ 每人一疊逐時段 Package → ACHR 直接置入聚落的 vanilla cell override → 服務 faction 讓他變店家**。EditorID 前綴分群（ICN=`ICNs_`、ETaC=`MJB…`/`pym_`、ICMF=人名）。下面逐機制拆。

### 1. 置放 = vanilla cell override，**additive 帶 vanilla ref + 加自家 ACHR**

`cellrefs DushnikhYalLonghouse(0x0198E2)`（ETaC 獸人長屋）：

```
npcP 013B7B:Skyrim.esm  ArobREF        ← vanilla 原住民（additive 帶回，不刪）
npcP 013B7F:Skyrim.esm  NagrubREF      ← vanilla
npcT 83013B:…Orc Strongholds  MJBMurzolREF    ← 新增獸人法師商人
npcT 830268:…              MJBBugdurashREF ← 新增
npcT 830269:…              MJBShagarREF   ← 新增
objP 830264:…             （新增家具/裝飾）
# 1 placed object, 5 placed npc, 1 disabled-skipped
```

→ **聚落擴充的本質 = override 該聚落的每個 cell，保留 vanilla 居民、additive 塞進新 NPC 的 ACHR + 新佈景**。ICN 同理 override 學院 8 個 cell（HallofTheElements / Courtyard / dorm 等，全 Skyrim.esm FormID）；ETaC override 四要塞共 37 個 ext/int cell。**異世界版更省**：自家 cell 不必 override、不必背 vanilla 相容（這是 ICN/ETaC 一半複雜度的來源）。

### 2. 行為 = 每人一疊「逐時段 schedule package」（最大工作量、最不可規模化）

ICN 16 人共 101 個包，命名極細：`ICNs_Melker_Sleep_Pkg` / `_Room_Pkg` / `_Study_Pkg` / `_Arc_Pkg`（拱廊閒晃）/ `_Tavern_Pkg` / `_Train_Group2_Part1/2_Pkg`（分組練習）。每包帶 `Schedule: hour/minute/durationMin` + `PackageDataLocation radius` + 目標：

```
ICNs_Lentilus_HotE_Practice_Pkg（0x803）：
  PackageTemplate -> 自製 template；PreferredSpeed=Walk
  Schedule: dayOfWeek=Weekdays hour=7 minute=30 durationMin=150  ← 工作日 07:30 起 2.5h
  Data: LocationTarget(XMarker) radius=32 + TargetObjectType(MeleeWeapons) + SingleRef(練習目標)
```

ETaC 同形但更簡（每獸人 1–2 包）：`MJBDushnikhYalOrcMurzolWork`（hour=8 dur=600 → 早 8 上工 10h），`PackageTemplate -> Skyrim Sandbox/Work template`，target = vanilla 家具 ref。**這是 staffing 的勞力核心：每個 NPC 手刻「睡→上工→用餐→閒晃」一套包，靠 `Schedule` 時段 + `LocationTarget radius` 串成日程**。

排程的「定位點」是 cell 裡置入的 **XMarkerHeading（base 0x000034）**：`cellrefs HallofTheElements` 顯 17 個 `ICNs_*_XMarkH`（如 `ICNs_Practice_Lentilus_XMarkH`）+ `ICNs_*_Target`（base 0x00003B，練習對象）——**先在 cell 放命名 marker，再讓 package 的 LocationTarget 指它**。這正是 [immersive-wenches](../immersive-wenches.md) 同款 marker 模式（只是 IW 在 marker 上 script-spawn LL，這三者是靜態 ACHR）。

### 3. 「mini faction」= **per-NPC Vendor 服務 faction（無 rank！）**，不是 rank-tiered 公會

ICMF/ETaC 的「factions」名字唬人，`factdiag` 拆開都是**每個店員一個 Vendor-flag faction**：

```
factdiag GuntherVendorFaction(ICMF 0x5AFB)：
  Flags = Vendor    Ranks (0)    Relations (0)
  VendorValues: startHour=8 endHour=17 radius=0
  VendorBuySellList = 0937A1:Skyrim.esm   MerchantContainer = 005AFA（自家容器）

factdiag MJBDushnikhYalMageVendorFaction(ETaC 0x830266)：
  Flags = Vendor, CanBeOwner    Ranks (0)
  VendorValues: startHour=8 endHour=18 radius=256
  VendorBuySellList = MJB_VendorItemsMage(自製 FormList)   item -> 9 個 vanilla 法術書
```

→ **「開一間店」的最小配方 = 一個 Vendor-flag FACT（含營業時段 + sell/buy FormList + 自家 MerchantContainer）＋把 NPC 加進該 faction**。ICMF 7 個、ETaC 3 個新 Vendor faction＝給聚落補上「法師店/鐵匠/旅店主」三種服務。**沒有 rank 階層、沒有 crime faction（用 vanilla 學院/獸人 crime faction）、沒有 faction 內部敵我**——所以這不是「迷你公會」而是「**迷你商圈**」。對白接 vanilla generic `OffersTrainingTopic`/服務 menu（NPC 一掛進 Vendor faction 引擎自動上「I'd like to trade」），ICMF 額外手寫各專長的訓練建議對白（`DialogueWinterhold…SpecialtyTopic`）。

ICMF 的 3 個 **Relationship（RELA）** 給少數 NPC 補人際（`MaedrosRelationMirabelle rank=Lover`）——讓店員彼此有關係，是「活感」點綴，非結構。

### 4. NPC base 組裝（`npcdiag`）

ETaC Murzol：`Race/Class/Outfit` 全指 vanilla，`AutoCalcStats + Unique + Protected`、`Level=10`、`AIData Aggression=Unaggressive Confidence=Average`、6 個 faction（vanilla 獸人/crime/服務 + 新 Vendor faction）、3 個 package（vanilla 通用 + 自製 Work + vanilla observe）。**注意都配了 Class**（避開 memory `autocalc-without-class-dead-npc` 的死 NPC 陷阱）。ICN 的 `ICNs_Guardian` 是唯一帶 CombatStyle 的（守衛），其餘學者/學生中立無戰鬥。ICMF 的店員另帶自製 Outfit（店員制服）。

