# 3. 對話改變機制 (Dialogue Changes)

[返回入口](../minAI-analysis.md)

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
