# 2. NPC 下令機制 (NPC Command/Control)

[返回入口](../minAI-analysis.md)

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

