# 架構總覽

[返回入口](../mantella-analysis.md)

## 架構總覽

Mantella 是 **外部 Python 程序**，與遊戲透過 HTTP 通訊。遊戲端是 Mantella Spell（一個 SKSE Papyrus plugin，在另一個 repo），負責讀取遊戲狀態、播放語音、執行動作，然後透過 HTTP POST 跟 Python 端交換 JSON。

```
Skyrim (SKSE Papyrus plugin: Mantella Spell)
  │  HTTP POST /mantella (JSON)
  ▼
Python (FastAPI server)
  ├─→ GameStateManager: 管理 conversation lifecycle
  ├─→ Context: 聚集世界狀態、角色資訊、事件
  ├─→ Conversation: 控制對話流程
  ├─→ FunctionManager: OpenAI function-calling actions
  ├─→ Remembering (Summaries): 記憶/摘要管理
  └─→ LLMClient: 調用 LLM API
```

---

## 1. 世界狀態總結 (World State Summarization)

### 1.1 遊戲狀態傳輸：JSON over HTTP

Mantella 的遊戲狀態**不是 C++ 直接讀記憶體**，而是 SKSE Papyrus plugin 收集後打成 JSON 送到 Python 端。

從 `communication_constants.py` 可以看到傳輸的結構：

**每個 Actor 的欄位**（`game_manager.py:286-328` parse）：
```
base_id, ref_id, name, gender, race, is_player, relationship_rank,
voice_type, is_in_combat, is_enemy, custom_values (dict), equipment
```

**場景 context 欄位**（`context.py:174-241`）：
```
location, time (ingame hour), weather (id → CSV查表), game_days (float),
nearby_actors, ingame_events (list[str]), custom_context_values (dict),
config_settings (dict)
```

### 1.2 Context 物件的狀態聚合

`Context` (`context.py`) 是 Mantella 的世界狀態中樞。它**主動偵測狀態變化並生成自然語言事件**：

**位置變化** → `"The location is now {location}."`

**時間變化** → `"The time is {hour} {time_group}."` 或 `"The conversation now takes place {time_group}."`（time_group = morning/afternoon/evening/night）

**天氣變化** → 從 `skyrim_weather.csv` 查表：weather_id → 文字描述（如 `"The sky is cloudy."`），fallback 用四個天氣分類

**NPC 戰鬥狀態變化** → `"{name} is now in combat!"` / `"{name} is no longer in combat."`

**NPC 敵對狀態變化** → `"{name} is attacking {player}. This is either because he is an enemy or {player} has attacked him first."`

**關係變化** → `"{player} is now {trust} to {npc}."`（trust = stranger/acquaintance/friend/close friend/lover/enemy，由 relationship_rank + 對話次數共同決定）

**附近 NPC 變化** → `"Characters nearby (from nearest to furthest): {names}"`

**Vision hints** → `"Characters currently in view: {name} ({distance_category})"`（very close/close/medium distance/far/very far）

### 1.3 天氣查表機制

`Skyrim.get_weather_description()` (`skyrim.py:244-257`):
- 優先查 weather ID → `skyrim_weather.csv` → description 欄位
- Fallback: weather classification (0-3) → `["pleasant", "cloudy", "rainy", "snowing"]`

### 1.4 Prompt 組合機制

`Context.generate_system_message()` (`context.py:416-521`) 用 **Python `str.format()`** 填入以下變數：

```python
player_name, player_description, player_equipment, player_gender, player_race,
name (=最後加入的 NPC 名字),
names (=所有 NPC 名字列表),
names_w_player (=含玩家的名字列表),
bios (=所有 NPC 的 bio 串接),
trust (=所有 NPC 對玩家的信任關係文字),
gender, race, genders, races, genders_and_races,
equipment (=NPC 裝備描述),
location, weather, time, current_day, time_group,
language,
conversation_summary / conversation_summaries (=之前對話的摘要),
actions (=基本 action 的 prompt 文字)
```

**Token 限制處理**：如果 prompt 太長，先丟 summaries，再丟 bios。雙雙被丟時記錄 warning。

### 1.5 Character Bio 管理

Bio 來源：`data/Skyrim/skyrim_characters.csv`（預先手寫的角色 bio CSV）。

Bio template 系統（`BioTemplateManager`）：支援 tag-based 模板展開。角色可以有 tags，對應的模板文字會被注入 bio。

對於找不到 CSV 記錄的 generic NPC：`load_unnamed_npc()` 生成一個極簡 bio：
```
"You are a {male/female} {race} {name}."
```

### 1.6 記憶/摘要系統

`Summaries` (實作 `Remembering`)：每場對話結束時，對每位 NPC 生成對話摘要（用專門的 summary LLM），儲存為檔案。下次對話時摘要文字注入 prompt。

---

