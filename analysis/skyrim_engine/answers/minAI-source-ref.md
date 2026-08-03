# MinAI — 原始碼出處索引

> 路徑根: `external/frameworks/MinAI/`
> 注意: MinAI 是純 Papyrus mod，無 Python、無 C++。CHIM/AIFF server 端在另一個 repo（DwemerAI4Skyrim），不在此分析範圍。

---

## 1. 世界狀態總結相關原始碼

### 1.1 環境感知模組（最精細的狀態收集）

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_EnvironmentalAwareness.psc:32-79` | `GetDayState()` — **21 層級時間描述**（"midnight" → "dead of night" → "just before sunrise" → "dawn" → ... → "almost midnight"） |
| `Scripts/Source/minai_EnvironmentalAwareness.psc:81-207` | `SetFrostfallContext()` — **Frostfall 狀態收集**（temperature 9 層級、weatherSeverity、isSheltered、wetnessLevel 5 層級、exposureLevel 5 層級、baselineExposure、warmthRating 5 層級、coverageRating 5 層級） |
| `Scripts/Source/minai_EnvironmentalAwareness.psc:247-318` | `SetContext()` — **核心：所有 actor 變數寫入**（玩家: dayState, weatherClassification, moonPhase, moonCount, isNight；NPC: isBribed, isIntimidated, relationshipRank, isChild, hasFamily, sleepState, career；所有 actor: level, isSneaking, isSwimming, isOnMount, isEncumbered, sitState） |
| `Scripts/Source/minai_EnvironmentalAwareness.psc:334-393` | `GetCurrentMoonPhase()` / `GetCurrentMoonSync()` — 月相計算（0-7）／雙月同步（Masser + Secunda, 5 天週期） |
| `Scripts/Source/minai_EnvironmentalAwareness.psc:396-681` | `SetLocationData()` — **極詳細地點關鍵字收集**（~60+ LocType 檢查: city/town/village/dungeon/fort/temple/tavern/shop/house/farm/mine/camp/.../temple_of_akatosh）；也收集 currentLocation/currentHold/currentWorldspace/currentCell/isInterior/isTrespassing |
| `Scripts/Source/minai_EnvironmentalAwareness.psc:680-681` | `isTrespassing` 寫入 |

### 1.2 Context Effect — 狀態排程收集

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_ContextEffect.psc:1-42` | `OnEffectStart()` — 掛載到 AI 管理的 NPC 上，初始化 inventory tracking，註冊首次 update |
| `Scripts/Source/minai_ContextEffect.psc:59-65` | `DisableSelf()` — 移除 context spell，停止追蹤 |
| `Scripts/Source/minai_ContextEffect.psc:67-105` | `OnUpdate()` — **定時狀態更新**（檢查 actor 是否仍被 AI 管理 → `aiff.SetContext()` → 重新註冊下次 update；如果 actor 不再被管理則移除追蹤） |
| `Scripts/Source/minai_ContextEffect.psc:107-154` | `OnItemAdded()`/`OnItemRemoved()` — 物品變化追蹤（有限流機制: burst detection → throttle → 只追蹤 gold） |

### 1.3 AIFF Facade — Actor Variable Store

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_AIFF.psc:1-67` | Properties 宣告 — `contextMutexMap` (JMap), `inventoryTracker` (JMap), `actionRegistry`, `lastDialogueTimes` (JMap) |
| `Scripts/Source/minai_AIFF.psc:84-154` | `Maintenance()` — **初始化**（JMap 管理: contextMutexMap, inventoryTracker, inventoryBurstTracker, updateTracker；maxInventoryBatchSize=40；action registry reset on version update） |

### 1.4 模組化狀態收集 — 子模組

| 檔案 | 內容 |
|------|------|
| `Scripts/Source/minai_Survival.psc` | 生存模組（Sunhelm hunger/thirst/fatigue、Gourmet intoxication、Requiem substance effects） |
| `Scripts/Source/minai_Sex.psc` | 性愛場景模組（SexLab/OStim 狀態） |
| `Scripts/Source/minai_SexOstim.psc` | OStim 整合 |
| `Scripts/Source/minai_SexSexlab.psc` | SexLab 整合 |
| `Scripts/Source/minai_Arousal.psc` | Arousal 模組（level tracking + 時間衰減） |
| `Scripts/Source/minai_DeviousStuff.psc` | Devious Devices / Devious Followers 模組 |
| `Scripts/Source/minai_DirtAndBlood.psc` | Dirt & Blood 整合（清潔度/血跡） |
| `Scripts/Source/minai_Relationship.psc` | 關係模組 |
| `Scripts/Source/minai_Followers.psc` | 跟隨者模組 |
| `Scripts/Source/minai_Reputation.psc` | 聲望模組 |
| `Scripts/Source/minai_Crime.psc` | 犯罪/賞金模組 |
| `Scripts/Source/minai_CombatManager.psc` | 戰鬥管理模組 |
| `Scripts/Source/minai_ItemCommands.psc` | 物品交易模組 |
| `Scripts/Source/minai_FertilityMode.psc` | Fertility Mode 整合 |

---

## 2. NPC 下令相關原始碼

### 2.1 Action Registry（CHIM 端）

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_AIFF.psc` | `RegisterAction()` — 向 CHIM 註冊 action（含 category, cooldown, minBackoff, maxBackoff, backoffWindow, addToAllNPCs, addToPlayer） |
| `Scripts/Source/minai_AIFF.psc` | `StoreAction()` — 儲存外部 mod 的 action（含 prompt, ttl, targetDescription, targetEnum, npcName） |
| `Scripts/Source/minai_AIFF.psc` | `ResetAllActionBackoffs()` — 重置所有 action backoff |

### 2.2 外部 Mod 的 Action API

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_MainQuestController.psc:411-418` | `OnRegisterAction()` — **接收外部 ModEvent 註冊 action**（ExtCmd+actionName prefix；存入 StoreAction） |
| `Scripts/Source/minai_MainQuestController.psc:435-442` | `OnRegisterActionNPC()` — 接收 per-NPC action 註冊 |
| `ModdersGuide.md:1-156` | **完整 Modder API 文件**（MinAI_RegisterEvent, MinAI_RequestResponse, MinAI_RequestResponseDialogue, MinAI_SetContext, MinAI_SetContextNPC, MinAI_RegisterAction, MinAI_RegisterActionNPC 的參數格式與用法） |

### 2.3 Action 控制用 Factions

| 檔案:行號 | 內容 |
|-----------|------|
| `ModdersGuide.md:4-10` | Faction 控制系統（`NoActionsFaction`, `NoSexActionsFaction`, `NoNSFWActionsFaction` — 部分名稱匹配即可，無需硬依賴 MinAI） |

### 2.4 跟隨系統

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_AIFF.psc:68-81` | `InitFollow()` — 載入 `FollowPlayerPackage` + `FollowingPlayerFaction` |
| `Scripts/Source/minai_AIFF.psc` | `CheckIfActorShouldStillFollow()` — cleanup 檢查 |

### 2.5 主要控制器 — 事件路由

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_MainQuestController.psc:62-157` | `Maintenance()` — 初始化所有 15+ 子模組、註冊 ModEvent 監聽、設定 keybinds、檢測安裝的 AI 框架（Mantella/AIFF） |
| `Scripts/Source/minai_MainQuestController.psc:160-165` | `RegisterAction()` — 轉送 action 到 Mantella 或 AIFF |
| `Scripts/Source/minai_MainQuestController.psc:168-184` | `RegisterEvent()` — 轉送事件到 Mantella/AIFF（自動 prefix "info_" 到 event type） |
| `Scripts/Source/minai_MainQuestController.psc:187-200` | `RequestLLMResponse()` — **請求 LLM 回應**（含 cooldown 檢查；冷卻期內降級為 RegisterEvent） |
| `Scripts/Source/minai_MainQuestController.psc:203-237` | `RequestLLMResponseFromActor()` — 請求特定 actor 回應（支援 "player"/"npc"/"both" responseTarget） |
| `Scripts/Source/minai_MainQuestController.psc:240-252` | `RequestLLMResponseNPC()` — NPC→NPC 對話請求（格式: `speaker@target@eventLine`） |

---

## 3. 對話改變相關原始碼

### 3.1 對話事件攔截 — Mantella 橋接

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_Mantella.psc:18-46` | `Maintenance()` — 註冊監聽 `Mantella_ActorSpeakEvent` + `Mantella_PlayerInputEvent`；取得 MantellaConversation/formlist handles |
| `Scripts/Source/minai_Mantella.psc:55-57` | `OnActorSpeak()` → `ActionResponse()` — **攔截 Mantella 對話事件** |
| `Scripts/Source/minai_Mantella.psc:59-77` | `OnPlayerInput()` — 攔截玩家輸入（2 人對話時呼叫 UpdateEvents 初始化 context） |
| `Scripts/Source/minai_Mantella.psc:81-93` | `RegisterAction()` / `RegisterEvent()` → `mantella.AddInGameEvent()` — **注入事件到 Mantella 對話 context** |
| `Scripts/Source/minai_Mantella.psc:108-133` | `UpdateEvents()` — **核心：在每次對話時收集所有模組的狀態並注入**（devious → arousal → survival → dirtAndBlood → BuildReminderStr） |
| `Scripts/Source/minai_Mantella.psc:135-143` | `FactionInScene()` — 檢查 faction 是否在對話參與者中 |
| `Scripts/Source/minai_Mantella.psc:147-179` | `BuildReminderStr()` — **動態建立 action keyword 提醒字串**（根據已安裝 mod 組合: "Respond only with spoken dialog and defined -keywords- for your actions... trading with, spanking, molesting, kissing, hugging, feeding, serving a meal to, renting a room to, giving drugs or skooma to, vibrating, giving an orgasm to, teasing, or having sex with Lydia."） |
| `Scripts/Source/minai_Mantella.psc:189-210` | `ActionResponse()` — **對話內容匹配觸發**（各模組檢查 sayLine 是否匹配觸發條件 → 執行對應 action；模組順序: arousal → sex → survival → devious → UpdateEvents） |

### 3.2 Context API（外部 Mod 對話注入）

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_MainQuestController.psc:326-329` | `OnRegisterEvent()` — 接收外部 ModEvent → `RegisterEvent(eventLine, eventType)` |
| `Scripts/Source/minai_MainQuestController.psc:340-343` | `OnRequestResponse()` — 接收外部 ModEvent → `RequestLLMResponseFromActor()` |
| `Scripts/Source/minai_MainQuestController.psc:354-357` | `OnRequestResponseDialogue()` — 接收外部 ModEvent → `RequestLLMResponseNPC()` |
| `Scripts/Source/minai_MainQuestController.psc:368-376` | `OnSetContext()` — 接收外部 ModEvent → `AIFF.StoreContext()` 或 fallback `RegisterEvent()` |

### 3.3 Dungeon Master / Narrator / Roleplay / Diary 快捷鍵

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_MainQuestController.psc:578-610` | `OnKeyDown()` — 10 個快捷鍵的 dispatch（sapience toggle, sing, narrator, narrator text, roleplay, roleplay text, diary, dungeon master, dungeon master text） |
| `Scripts/Source/minai_MainQuestController.psc:614-633` | `OnKeyUp()` — 語音錄製鍵釋放處理 |
| `Scripts/Source/minai_MainQuestController.psc:636-663` | `OnSingKeyPressed()`/`OnSingKeyReleased()` — Sing 功能 |
| `Scripts/Source/minai_MainQuestController.psc:666-693` | `OnNarratorKeyPressed()`/`OnNarratorKeyReleased()` — Narrator 對話 |
| `Scripts/Source/minai_MainQuestController.psc:837-869` | `OnDiaryKeyPressed()` — Diary 快捷鍵（蹲下→narrator diary；看向NPC→該NPC diary；站立→所有 follower + player diary） |
| `Scripts/Source/minai_MainQuestController.psc:892-937` | `OnDungeonMasterKeyPressed()`/`OnDungeonMasterKeyReleased()` — Dungeon Master 直接提示（crosshair target 或 "everyone"） |

### 3.4 Sensuality/Sex 場景的對話處理

| 檔案 | 內容 |
|------|------|
| `Scripts/Source/minai_SexAwareness.psc` | 性愛場景感知 |
| `Scripts/Source/minai_AmbientSexTalk.psc` | 性愛場景中的 ambient dialogue |
