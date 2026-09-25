# 2. NPC 下令機制 (NPC Command/Control)

[返回入口](../skyrimNet-gameplugin-analysis.md)

## 2. NPC 下令機制 (NPC Command/Control)

### 2.1 三層 Action 系統

Action 是對 NPC 下令的核心機制，有三種註冊方式：

#### Layer 1: YAML-defined actions（最常見）
YAML 檔案定義 action → C++ 端解析 → 透過 `executionFunctionName` 呼叫 Papyrus 腳本的函數。

YAML 結構 (`WORKFLOW_ACTIONS.md:236-268`):
```yaml
name: "ActionName"
description: "描述給 LLM 看，讓 LLM 判斷何時使用"
questEditorId: "QuestEditorID"
scriptName: "ScriptName"
executionFunctionName: "FunctionName"
parameterMapping:
  - type: "speaker"       # 自動填為執行 action 的 NPC
  - type: "dynamic"       # LLM 選擇參數值
    name: "param_name"
    description: "描述給 LLM"
  - type: "static"        # 固定值
    value: "fixed_value"
eligibilityRules:
  - conditions:
      - decoratorName: "is_in_faction"
        arguments: ["currentActor", "FactionEditorID"]
        comparisonOperator: "=="
        expectedValue: true
    logicalOperator: "AND"
    required: true
```

參數映射支援的型別：
| Papyrus Type | Mapping |
|--------------|---------|
| Actor (self) | `speaker` |
| Actor (target) | `dynamic` (LLM 選) |
| Int/Float (fixed) | `static` |
| Int/Float (variable) | `dynamic` |
| Bool/String | `static` 或 `dynamic` |

#### Layer 2: Papyrus-registered actions
透過 `SkyrimNetApi.RegisterAction()` 在 runtime 註冊（`SkyrimNetApi.psc:27-31`）：
```papyrus
SkyrimNetApi.RegisterAction(
    actionName, description,
    eligibilityScriptName, eligibilityFunctionName,
    executionScriptName, executionFunctionName,
    triggeringEventTypesCsv, categoryStr,
    defaultPriority, parameterSchemaJson, customCategory, tags)
```

#### Layer 3: Native C++ actions
其他 SKSE plugin 可以注入 C++ 實作的 actions。

### 2.2 Action 的兩個執行路徑

#### Path A: 嵌入對話（`embed_actions_in_dialogue`）
`0750_embedded_actions.prompt` 讓 LLM 在生成對話的同時輸出 action：
```
NPC 的對話文字
ACTION: ActionName PARAMS: {"param": "value"}
```
C++ 端解析 response，先送對話去 TTS，同時解析並執行 action。

#### Path B: 獨立 Action Selector
`native_action_selector.prompt` 是一個**獨立的 LLM 呼叫**，專門判斷對話後應該執行哪個 action。輸入包含：
- NPC 的完整 character profile
- 對話歷史（compact event history）
- 最近一次交換（玩家說了什麼、NPC 回了什麼）
- 附近 actors 清單（含距離、狀態）
- **Eligible Actions 清單**（已預先過濾/filtered by eligibility + cooldown）

### 2.3 Action 分類系統 (Categories → Drill-down)

Actions 可以分組到 categories 中。當 LLM 選擇一個 category（而非具體 action）時，系統會觸發 **第二次 LLM 呼叫** (`native_action_selector_drilldown.prompt`) 用更便宜的 model 來選具體 action。Category 選擇時必須帶 `intent`：
```json
{"ACTION": "Economy", "PARAMS": {"intent": "sell a health potion to the player for 450 gold"}}
```

### 2.4 Eligibility 預熱 (Pre-warming)

在玩家語音輸入期間，系統**預先計算**每個附近 NPC 對每個 action 的 eligibility，所以當玩家說完話時，LLM 已經知道哪些 actions 是合法選項。

### 2.5 GameMaster 自主行為

`gamemaster_action_selector.prompt` 控制 NPC **在沒有玩家輸入時的自主行為**：

- **StartConversation**: 發起 NPC-to-NPC 對話（優先），或 NPC-to-Player（僅在有直接原因時）
- **ContinueConversation**: 維持進行中的對話
- **Scene Plan**: 預先規劃的場景節奏（scene beats），每個 beat 有 type/description/characters/purpose
- **Continuous Mode**: GM 持續導演場景，不能選 None

### 2.6 Papyrus Package 管理

`SkyrimNetApi.psc:117-145` 提供了 package 管理 API：
```papyrus
RegisterPackage(actor, packageName, priority, flags, isPersistent)
UnregisterPackage(actor, packageName)
ClearAllPackages(actor)
ReinforcePackages(actor)  ; 重新套用所有 SkyrimNet packages
```

這用於讓 NPC 看向說話對象（`TalkToPlayer`/`TalkToNPC` packages）。

### 2.7 Mod 社群 action 生態

README 提到兩個主要社群 plugin：
- **SeverActions**: 71 actions (combat, gold/debt, crafting, crime/arrest system)
- **IntelEngine**: NPC 自主行動、dynamic quest creation、faction politics（這是第四個要分析的 repo）

---

