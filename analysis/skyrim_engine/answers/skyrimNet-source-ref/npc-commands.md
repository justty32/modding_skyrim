# 2. NPC 下令相關原始碼

[返回入口](../skyrimNet-source-ref.md)

## 2. NPC 下令相關原始碼

### 2.1 Papyrus API — Action 管理

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/SkyrimNetApi.psc:13-15` | `RegisterDecorator()` — 註冊自訂 decorator |
| `Source/Scripts/SkyrimNetApi.psc:21-43` | `RegisterAction()` / `RegisterSubCategory()` / `RegisterTag()` — **Modder action API** |
| `Source/Scripts/SkyrimNetApi.psc:47-56` | `IsActionRegistered()` / `UnregisterAction()` / `ExecuteAction()` |
| `Source/Scripts/SkyrimNetApi.psc:58-62` | `SetActionCooldown()` / `GetRemainingCooldown()` — 冷卻管理 |

### 2.2 Papyrus API — Package 管理

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/SkyrimNetApi.psc:117-144` | `RegisterPackage()` / `UnregisterPackage()` / `ClearAllPackages()` / `ReinforcePackages()` |

### 2.3 Action 定義格式（YAML）

| 檔案 | 內容 |
|------|------|
| `docs/modding/WORKFLOW_ACTIONS.md` | **Action 建立完整 workflow**（YAML 結構、eligibility rule 邏輯、參數 mapping、validation） |
| `docs/modding/WORKFLOW_MOD_INTEGRATION.md` | Mod 整合指南 |

### 2.4 內建 Action 實作（Papyrus 端）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/SkyrimNetInternal.psc:100-118` | `OpenTrade_IsEligible()` + `OpenTrade_Execute()` |
| `Source/Scripts/SkyrimNetInternal.psc:130-143` | `Companion_IsEligible()` + `CompanionInventory()` |
| `Source/Scripts/SkyrimNetInternal.psc:145-165` | `CompanionFollow_IsEligible()` + `CompanionFollow()` |
| `Source/Scripts/SkyrimNetInternal.psc:166-185` | `CompanionWait_IsEligible()` + `CompanionWait()` |
| `Source/Scripts/SkyrimNetInternal.psc:207-261` | `StartFollow_IsEligible()` → `StopFollow_IsEligible()` — 跟隨系統 |
| `Source/Scripts/SkyrimNetInternal.psc:291-316` | `RentRoom_IsEligible()` + `RentRoom_Execute()` |
| `Source/Scripts/SkyrimNetInternal.psc:357-382` | `AlwaysEligible()` / `Follower_IsEligible()` — Tag-based eligibility |
| `Source/Scripts/SkyrimNetInternal.psc:24-38` | `GetDiaryScopeMessage()` — Diary scope 查詢 |

### 2.5 Papyrus — NPC 對話/跟隨對象設定

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/skynet_MainController.psc:91-114` | `SetActorDialogueTarget()` — 設定 NPC 看向誰、套用 `TalkToPlayer`/`TalkToNPC` package |
| `Source/Scripts/skynet_MainController.psc:121-131` | `SetActorFollowing()` / `ClearActorFollowing()` — 跟隨系統 |

### 2.6 GameMaster 自主行為 Prompt

| 檔案 | 內容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/prompts/gamemaster_action_selector.prompt` | **GameMaster action selector**（StartConversation/ContinueConversation, Scene Plan beats, NPC→NPC 優先） |
| `SKSE/Plugins/SkyrimNet/prompts/gamemaster_scene_planner.prompt` | GameMaster 場景規劃 |

---

