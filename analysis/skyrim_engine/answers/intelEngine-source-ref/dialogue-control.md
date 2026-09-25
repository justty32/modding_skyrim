# 3. 對話改變相關原始碼

[返回入口](../intelEngine-source-ref.md)

## 3. 對話改變相關原始碼

### 3.1 敘事旁白（Narration）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:1460-1464` | `SendTaskNarration()` → `SkyrimNetApi.DirectNarration(msgText, akActor, akTarget)` |
| `Source/Scripts/IntelEngine_Core.psc:1637-1640` | `NotifyPlayer()` → `Debug.Notification()` |

### 3.2 Story Engine（Dungeon Master — 自主行為）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_StoryEngine.psc:1-19` | Story types 定義 — 9 種（seek_player, informant, npc_interaction, npc_gossip, road_encounter, ambush, stalker, message, quest） |
| `Source/Scripts/IntelEngine_StoryEngine.psc:29-44` | Dispatch state + constants（ENCOUNTER_PROXIMITY, SNEAK_APPROACH_DISTANCE, AMBUSH_CONFRONT_DISTANCE 等） |
| `Source/Scripts/IntelEngine_StoryEngine.psc:45-100` | MCM 設定（MaxTravelDays, LongAbsenceDays, DangerZonePolicy, PlayerHomePolicy, per-type toggles, per-type hold restriction policies, per-action confirmation, per-action follower skip） |

### 3.3 Faction Politics Engine

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Politics.psc` | Faction 政治系統（9 faction, 6 遊戲小時政治事件、faction wars、player standing） |
| `SKSE/Plugins/SkyrimNet/config/plugins/IntelEngine/factions.sample.yaml` | Faction 設定 sample |
| `SKSE/Plugins/SkyrimNet/config/plugins/IntelEngine/manifest.yaml` | Plugin manifest |

### 3.4 Battle Engine

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Battle.psc` | 戰鬥系統（ambush attack sequence、faction war battles、5 waves, 22 per side） |

### 3.5 NPC Tasks（多步驟任務）

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_NPCTasks.psc` | `FetchNPC()`, `DeliverMessage()`, `EscortTarget()`, `SearchForActor()` — **多步驟 NPC 任務**（travel → find target → interact → return） |

### 3.6 Dashboard State & Events

| 檔案:行號 | 內容 |
|-----------|------|
| `Source/Scripts/IntelEngine_Core.psc:1918-2029` | `RegisterDashboardEvents()` + event handlers — **PrismaUI Dashboard 整合**（Dashboard opened/refresh/cancel task/cancel quest/cancel schedule/toggle story/settings/remove packages/dispatch story/social/politics/execute action/auto bio update） |
| `Source/Scripts/IntelEngine_Core.psc:2029+` | Dashboard state push methods |

### 3.7 MCM 介面

| 檔案 | 內容 |
|------|------|
| `Source/Scripts/IntelEngine_MCM.psc` | MCM 設定頁面 |
| `Interface/MCMHelper/IntelEngine/config.json` | MCM Helper 設定 |

### 3.8 Plugin 設定

| 檔案 | 內容 |
|------|------|
| `SKSE/Plugins/SkyrimNet/config/plugins/IntelEngine/manifest.yaml` | SkyrimNet plugin manifest |
| `SKSE/Plugins/SkyrimNet/config/plugins/IntelEngine/settings.sample.yaml` | Settings sample |
| `SKSE/Plugins/SkyrimNet/config/plugins/IntelEngine/factions.sample.yaml` | Faction 設定 sample |
