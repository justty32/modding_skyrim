# 一、這個工具做什麼 + 工作原理

← [原文入口](../po3-tweaks.md)

## 一、這個工具做什麼 + 工作原理

po3's Tweaks 是一個純 SKSE native 外掛（C++ DLL），**不生成任何 .esp record**，純粹在引擎層打 patch 或修改行為。它將所有開關集中在 `SKSE/Plugins/po3_Tweaks.ini` 中，以 key = value 形式控制。

**三大分區**：

| 分區 | 性質 | 說明 |
|------|------|------|
| `[Fixes]` | Bug fix | 修引擎本身的 bug，幾乎全部預設 `true` |
| `[Tweaks]` | 行為改變 | 可選的遊戲機制調整，預設多為 `false` 或低衝擊值 |
| `[Experimental]` | 實驗性 | 效能最佳化或邊緣功能，需手動啟用 |

**工作原理**：遊戲啟動時 SKSE 載入 DLL，DLL 在記憶體對引擎函數做 detour/hook（不碰 ESM/ESP），ini 設定決定哪些 hook 啟動。無執行期依賴，也無 Quest/Script/Form 需求。

---

## 二、ini 設定檔結構（完整說明）

### [Fixes] — 引擎 Bug 修正

所有 Fixes 預設 `= true`（部分有數值模式）。

本表整理「[Fixes] — 引擎 Bug 修正」的逐項記錄。

已抽到 [runtime-and-settings-engine-fixes.json](runtime-and-settings-engine-fixes.json)（23 列）。

欄位「Key」：保留原表的Key。

欄位「說明」：保留原表的說明。

欄位「與 ModForge 的交集」：保留原表的與 ModForge 的交集。

統計：23 筆記錄，3 個欄位。


### [Tweaks] — 可選行為調整

本表整理「[Tweaks] — 可選行為調整」的逐項記錄。

已抽到 [runtime-and-settings-optional-tweaks.json](runtime-and-settings-optional-tweaks.json)（17 列）。

欄位「Key」：保留原表的Key。

欄位「預設值」：保留原表的預設值。

欄位「說明」：保留原表的說明。

欄位「與 ModForge 的交集」：保留原表的與 ModForge 的交集。

統計：17 筆記錄，4 個欄位。


### [Experimental] — 實驗性

| Key | 預設值 | 說明 |
|-----|--------|------|
| `Fast RandomInt() = false` | false | 加速 Utility.RandomInt 呼叫 |
| `Fast RandomFloat() = false` | false | 加速 Utility.RandomFloat 呼叫 |
| `Clean Orphaned ActiveEffects = false` | false | 移除缺少 ability perk 的 NPC 的 active effects |
| `Update GameHour Timers = false` | false | GameHour.SetValue 推進時間後同步更新遊戲計時器 |
| `Stack Dump Timeout Modifier = 30.0` | 30.0 | Papyrus stack dump 等待秒數（0=停用） |

---

