# MinAI 分析：世界狀態、NPC 指令、對話控制

> 來源: `external/frameworks/MinAI/` (clone from https://github.com/MinLL/MinAI)
> 分析日期: 2026-07-30
> 狀態: **已棄用**（官方建議改用 SkyrimNet）
> 關注範圍: 世界狀態總結機制、NPC 下令、對話改變（排除 TTS/STT/AI 截圖等）

---

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

## 2. NPC 下令機制 (NPC Command/Control)

### 2.1 Action Registry

MinAI 透過 CHIM 的 action registry 管理 NPC 指令。Action 定義在 `minai_AIFF` 中：

```papyrus
; 註冊 action（內部）
RegisterAction("ExtCmd"+actionName, actionName, mcmDescription, 
               categoryStr, enabled, cooldown, 
               minBackoff, maxBackoff, backoffWindow, 
               addToAllNPCs, addToPlayer)

; 外部 mod 註冊的 action（儲存到 context store + action registry）
StoreAction(actionName, actionPrompt, enabled, ttl, 
            targetDescription, targetEnum, npcName)
```

Action 支援：
- **Cooldown with exponential backoff**: 每次使用後冷卻時間遞增，隨時間衰減回基礎值
- **Per-NPC 或 global scope**
- **MCM 開關**（可從 MCM 選單啟用/停用）
- **Category system**: actions 可歸入類別

### 2.2 Modder Action API

`ModdersGuide.md` 記錄了外部 mod 註冊 action 的方式：

```papyrus
; MinAI_RegisterAction — 對所有人可用的 action
int handle = ModEvent.Create("MinAI_RegisterAction")
ModEvent.PushString(handle, actionName)        ; 不可含空格
ModEvent.PushString(handle, actionPrompt)      ; LLM prompt 描述
ModEvent.PushString(handle, mcmDescription)    ; MCM 顯示文字
ModEvent.PushString(handle, targetDescription) ; 目標描述
ModEvent.PushString(handle, targetEnum)        ; 「目標清單」或「everyone」
ModEvent.PushInt(handle, enabled)              ; 預設啟用
ModEvent.PushFloat(handle, cooldown)           ; 冷卻秒數
ModEvent.PushInt(handle, ttl)                  ; context TTL
ModEvent.Send(handle)

; MinAI_RegisterActionNPC — 僅特定 NPC 可用的 action
; （參數同上，加上 npcName）
```

### 2.3 控制 Actions 的 Factions

MinAI 用 faction 系統控制哪些 actions 對哪些 NPC 可用：

| Faction (部分名稱匹配) | 效果 |
|------------------------|------|
| `NoActionsFaction` | 停用所有 MinAI 添加的 actions |
| `NoSexActionsFaction` | 停用性愛相關 actions |
| `NoNSFWActionsFaction` | 停用所有 NSFW actions |

Mod 不需要硬依賴 MinAI，只需建立同名 faction 即可。

### 2.4 跟隨系統

`minai_AIFF` 內建跟隨系統：
- `FollowPlayerPackage` + `FollowingPlayerFaction`
- `CheckIfActorShouldStillFollow()`: 檢查 NPC 是否應該繼續跟隨（cleanup）
- 支援 `Follow`, `Wait`, `Dismiss` 指令

---

## 3. 對話改變機制 (Dialogue Changes)

### 3.1 事件流

MinAI 的核心對話改變機制是**事件注入**。在對話發生時，MinAI 攔截對話事件，注入額外的遊戲狀態 context，然後讓 AI 框架處理回應。

**Mantella 整合** (`minai_Mantella.psc`):
```
Mantella 對話發生
  → OnActorSpeak Event
    → ActionResponse(): 各模組檢查對話內容並可能觸發 action
    → UpdateEvents(): 收集所有模組的狀態事件 → mantella.AddInGameEvent()
    → BuildReminderStr(): 建立 action keyword 提醒字串
```

**CHIM/AIFF 整合** (`minai_AIFF`):
```
AIFF dialogue hook
  → SetContext(): 更新所有 actor variables
  → 各模組 UpdateEvents() / SetContext()
  → AIFF 將 actor variables 送入 prompt 模板
```

### 3.2 BuildReminderStr() — Action Keyword 提示

`minai_Mantella.psc:147-179` 的一個關鍵函數。它在對話開始時動態建立一個提醒字串，告知 LLM 有哪些 action keywords 可用：

```
"Respond only with spoken dialog and defined -keywords- for your actions. 
Avoid narration and internal dialog. There are action -keywords- for 
trading with, spanking, molesting, kissing, hugging, feeding, 
serving a meal to, renting a room to, giving drugs or skooma to, 
vibrating, giving an orgasm to, teasing, or having sex with Lydia."
```

這個字串根據已安裝的 mod 動態組合，確保 LLM 知道哪些 action 是合法的。

### 3.3 Modder Event API — 對話控制

MinAI 定義了五個 ModEvent 作為外部 mod 的 API (`ModdersGuide.md`)：

| ModEvent | 用途 | 觸發 LLM 回應？ |
|----------|------|------------------|
| `MinAI_RegisterEvent` | 告知 LLM 某事件發生 | 否（僅注入 context） |
| `MinAI_RequestResponse` | 告知 LLM + 請求特定 NPC 回應 | 是（指定 targetName） |
| `MinAI_RequestResponseDialogue` | 告知 LLM 某 actor 說了什麼 + 請求回應 | 是 |
| `MinAI_SetContext` | 設定持久 context（含 TTL），所有 NPC 可見 | 否 |
| `MinAI_SetContextNPC` | 設定持久 context（含 TTL），僅特定 NPC 可見 | 否 |
| `MinAI_RegisterAction` | 註冊新 action | N/A |
| `MinAI_RegisterActionNPC` | 為特定 NPC 註冊新 action | N/A |

### 3.4 Request/Response 冷卻

`MainQuestController` 有 `requestResponseCooldown` 設定，防止事件洪水導致 LLM 被反覆呼叫。如果在冷卻期內收到 `RequestResponse` 事件，會降級為 `RegisterEvent`（僅注入 context，不請求回應）。

### 3.5 對話腳本響應 (ActionResponse)

`minai_Mantella.ActionResponse()` (`minai_Mantella.psc:189-210`)：
每次 NPC 發言時被呼叫。各模組檢查對話內容（sayLine）是否匹配觸發條件（如特定 keyword、性愛場景中的對話等），如果匹配則觸發對應的遊戲內 action。

模組依序檢查：`arousal.ActionResponse()` → `sex.ActionResponse()` → `survival.ActionResponse()` → `devious.ActionResponse()`

---

## 4. 設計亮點與取捨

### 4.1 世界狀態總結

| 設計 | 優點 | 代價 |
|------|------|------|
| SetActorVariable() key-value store | 極度彈性、任何模組可新增任意變數 | 無 schema，key 名稱靠約定 |
| 每個模組獨立收集狀態 | 模組化、可單獨開關 | 重複的 playerRef/null check 遍佈各模組 |
| 21 層級時間描述 | 極細膩的情境感知 | 比單純數字佔更多 prompt token |
| Location keyword brute-force 檢查 | 無需依賴外部資料 | 60+ 個 if 檢查，效能浪費 |
| TTL-based context | 自動過期，防止舊資料污染 | TTL 選擇是 magic number |

### 4.2 NPC 下令

| 設計 | 優點 | 代價 |
|------|------|------|
| Exponential backoff cooldown | 防止 action spam | 複雜度高 |
| Faction-based action 控制 | Mod 可無硬依賴控制行為 | 依賴 faction name 約定 |
| 外部 action 註冊 API | 第三方 mod 可擴充 | 依賴 CHIM 的 action execution |

### 4.3 對話系統

| 設計 | 優點 | 代價 |
|------|------|------|
| 事件攔截 + 注入模式 | 不修改對話框架本身 | 被動、只能在對話發生時反應 |
| BuildReminderStr() 動態組合 | LLM 知道當前可用的 actions | 佔 prompt token，可能無效 |
| RequestResponse cooldown | 防止 LLM 洪水 | 可能錯過重要事件 |

---

## 5. 與其他 repos 的關係

- **MinAI 是 CHIM 的擴充**：CHIM 提供 AI framework（HTTP server + agent management），MinAI 提供遊戲狀態收集 + mod 整合
- **MinAI 與 Mantella 的關係**：`minai_Mantella.psc` 是 MinAI→Mantella 的橋接層。當 Mantella 安裝時，MinAI 監聽 Mantella 的對話事件，注入額外的 mod context
- **MinAI 與 SkyrimNet 的關係**：MinAI 已被棄用，官方建議改用 SkyrimNet。SkyrimNet 的 `skynet_MinAIBridge.psc` 複製了 MinAI 的五個 ModEvent API（MinAI_RegisterEvent/SetContext/RequestResponse/RequestResponseDialogue），保持向後相容
- **CHIM (DwemerAI4Skyrim)**：MinAI 依賴的 AI 框架，PHP-based，不在本次分析的四個 repo 中
