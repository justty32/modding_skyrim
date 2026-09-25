# 1. 世界狀態總結相關原始碼

[返回入口](../minAI-source-ref.md)

## 1. 世界狀態總結相關原始碼

### 1.1 環境感知模組（最精細的狀態收集）

1.1 環境感知模組（最精細的狀態收集）的記錄已抽到 [world-state-environment-awareness-functions.json](world-state-environment-awareness-functions.json)（6 列）。

檔案:行號：保留原表「檔案:行號」欄內容。

內容：保留原表「內容」欄內容。

統計：共 6 筆記錄、2 欄。

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

1.4 模組化狀態收集 — 子模組的記錄已抽到 [world-state-state-modules.json](world-state-state-modules.json)（14 列）。

檔案：保留原表「檔案」欄內容。

內容：保留原表「內容」欄內容。

統計：共 14 筆記錄、2 欄。

---

