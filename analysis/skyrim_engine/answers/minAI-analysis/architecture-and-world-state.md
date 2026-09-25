# 架構總覽

[返回入口](../minAI-analysis.md)

## 架構總覽

MinAI 是一個 **純 Papyrus mod**，位於 CHIM/Mantella 等 AI 框架與 Skyrim 各種 mod 之間。它不是 AI 系統本身，而是一個**遊戲狀態聚合層 + 事件路由層 + Modder API**。

```
各種 Skyrim Mod (Frostfall, Sunhelm, SexLab, Dirt&Blood, etc.)
  │  Papyrus function calls / GlobalVariable reads
  ▼
MinAI 模組層 (每個模組收集特定領域的狀態)
  ├─→ minai_EnvironmentalAwareness  (天氣/時間/地點/Frostfall)
  ├─→ minai_Survival               (Sunhelm/Gourmet/Requiem)
  ├─→ minai_Sex / minai_Arousal    (SexLab/OStim)
  ├─→ minai_DirtAndBlood           (清潔度/血跡)
  ├─→ minai_DeviousStuff           (Devious Devices/Followers)
  ├─→ minai_Relationship           (NPC 關係)
  ├─→ minai_Followers              (跟隨者管理)
  ├─→ minai_Reputation             (聲望)
  ├─→ minai_Crime                  (犯罪/賞金)
  ├─→ minai_CombatManager          (戰鬥狀態)
  ├─→ minai_ItemCommands           (物品交易)
  └─→ minai_FertilityMode          (懷孕/Fertility Mode)
  │
  │  SetActorVariable() / StoreContext() / RegisterEvent()
  ▼
minai_AIFF (AI Framework Facade)
  │  對接 CHIM 的 action registry、context store、agent management
  │
  ├──→ CHIM server (PHP-based) → LLM
  └──→ minai_Mantella (Mantella bridge) → Mantella Python → LLM

外來 mod 透過 ModEvent API:
  MinAI_RegisterEvent / MinAI_RequestResponse / MinAI_SetContext / MinAI_RegisterAction
```

---

## 1. 世界狀態總結 (World State Summarization)

### 1.1 設計模式：SetActorVariable() 的 Actor Variable Store

MinAI 的核心世界狀態機是 **`SetActorVariable()`** — 一個在 `minai_AIFF` 中實作的函數，接受任意 key-value pair 並儲存於每個 actor。這是整個 mod 的資料匯流排。

### 1.2 環境感知 (`minai_EnvironmentalAwareness`)

這是 MinAI 最精細的狀態收集模組。`SetContext()` (`minai_EnvironmentalAwareness.psc:247-318`) 為每個 actor 收集：

**玩家專屬變數**：
- `dayState`: 極細膩的時間描述（21 個層級：`"midnight"`, `"dead of night"`, `"just before sunrise"`, `"dawn"`, `"early morning"`, `"morning"`, ..., `"almost midnight"`）
- `weatherClassification`: 天氣分類（0=Clear, 1=Cloudy, 2=Rain, 3=Snow）
- `moonPhase`: 月相（0-7）
- `moonCount`: `"moon"` 或 `"two moons"`（Masser + Secunda 的同步週期）
- `isNight`: 布林值

**Frostfall 整合（如果安裝）**：
- `temperature`: 9 個層級（`"frigid and deadly"` → `"hot"`）
- `weatherSeverity`: severe/dangerous 天氣判斷
- `isSheltered`, `wetnessLevel` (5 層級), `exposureLevel` (5 層級)
- `baselineExposure`: 體溫變化速率（升溫/降溫速度）
- `warmthRating`: 衣著保暖度（5 層級）
- `coverageRating`: 皮膚覆蓋度（5 層級）

**NPC 專屬變數**：
- `isBribed`, `isIntimidated`
- `relationshipRank`, `isChild`, `hasFamily`
- `sleepState`: `"sleeping deeply"` / `"sleeping"` / `"resting"`
- `career`: Class name

**所有 Actor 通用**：
- `level`, `isSneaking`, `isSwimming`, `isOnMount`, `isEncumbered`
- `sitState`: 坐姿狀態 raw value

**位置資料** (`SetLocationData()`, `EnvironmentalAwareness.psc:396-681`)：
- `currentLocation`, `currentHold`, `currentWorldspace`, `currentCell`
- `isInterior`, `isTrespassing`
- `locationKeywords`: 極詳細的地點關鍵字（~60+ 個 LocType 檢查：city/town/village/dungeon/fort/temple/tavern/shop/.../temple_of_akatosh）

### 1.3 SetContext() 排程

`minai_ContextEffect` (`contextEffect.psc`) 是一個 ActiveMagicEffect，掛在每個被 AI 管理的 NPC 上。它：
- 定時觸發 `OnUpdate()` → 呼叫 `aiff.SetContext(akTarget)`
- Update interval 由 `config.contextUpdateInterval` 控制
- 如果 actor 不再被 AI 管理 → 移除 spell，停止追蹤
- 也追蹤 inventory 變化（`OnItemAdded`/`OnItemRemoved`），但有限流機制（burst detection + throttle）

### 1.4 Context 變數 vs Event 的區別

| 機制 | 生命週期 | 用途 |
|------|---------|------|
| `SetContext()` | 每個 update cycle 刷新 | 持久性狀態（天氣、位置、裝備） |
| `SetActorVariable()` | 直到被覆寫 | Actor 屬性快取 |
| `StoreContext()` | TTL（秒），0=永久 | Mod 提供的持久上下文 |
| `RegisterEvent()` | 一次性 | 即時事件通知 |
| `MinAI_SetContext` ModEvent | TTL 控制 | 外部 mod 注入的持久上下文 |

### 1.5 模組化狀態收集

每個子模組都有 `SetContext()` / `UpdateEvents()` 函數：

- **`minai_Survival.UpdateEvents()`**: 檢查 Sunhelm hunger/thirst/fatigue、Gourmet intoxication、Requiem substance effects
- **`minai_Sex.UpdateEvents()`**: 檢查 SexLab/OStim 場景狀態、actor 是否在性愛場景中
- **`minai_Arousal.UpdateEvents()`**: 檢查 arousal level、時間基礎的衰減
- **`minai_DirtAndBlood.UpdateEventsForMantella()`**: 檢查清潔度和血跡程度
- **`minai_DeviousStuff.UpdateEvents()`**: DD 裝置狀態、Devious Followers 狀態

---

