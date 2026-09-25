# 1. 世界狀態總結相關原始碼

[返回入口](../mantella-source-ref.md)

## 1. 世界狀態總結相關原始碼

### 1.1 遊戲狀態接收與解析

| 檔案:行號 | 內容 |
|-----------|------|
| `src/game_manager.py:57-76` | `start_conversation()` — 建立 Context + Conversation |
| `src/game_manager.py:282-327` | `__update_context()` — **解析來自遊戲的 JSON 狀態**（actors list, location, time, game_days, ingame_events, weather, npcs_nearby, config_settings, custom_context_values） |
| `src/game_manager.py:330-431` | `load_character()` — **從 JSON 建構 Character 物件**（base_id, ref_id, name, gender, race, voice_type, is_in_combat, is_enemy, relationship_rank, equipment, custom_values；bio/voice_model 從 CSV 查表或 cache） |

### 1.2 Context 物件 — 世界狀態聚合與變化偵測

1.2 Context 物件 — 世界狀態聚合與變化偵測的記錄已抽到 [world-state-context-functions.json](world-state-context-functions.json)（11 列）。

檔案:行號：保留原表「檔案:行號」欄內容。

內容：保留原表「內容」欄內容。

統計：共 11 筆記錄、2 欄。

### 1.3 天氣查表

| 檔案:行號 | 內容 |
|-----------|------|
| `src/games/skyrim.py:49-53` | 載入 `skyrim_weather.csv` |
| `src/games/skyrim.py:244-257` | `get_weather_description()` — **天氣 ID/classification → 文字描述**（優先查 CSV → fallback 四個預設分類: pleasant/cloudy/rainy/snowy） |
| `src/games/skyrim.py:26-31` | `WEATHER_CLASSIFICATIONS` — 四個天氣分類常數 |

### 1.4 Character Bio 載入

| 檔案:行號 | 內容 |
|-----------|------|
| `src/games/skyrim.py:85-101` | `load_external_character_info()` — 從 `skyrim_characters.csv` 查表，取得 bio/voice_model/llm_service/llm_model，支援 tag-based bio 展開 |
| `src/games/skyrim.py:162-182` | `load_unnamed_npc()` — **generic NPC 的極簡 bio 生成**: `"You are a {male/female} {race} {name}."` |
| `src/bio_template_manager.py` | Bio template 展開系統（tag-based） |

### 1.5 Character 物件

| 檔案:行號 | 內容 |
|-----------|------|
| `src/character_manager.py:5-257` | `Character` class — **角色狀態容器**（base_id, ref_id, name, gender/race(raw+parsed), is_player_character, bio, is_in_combat, is_enemy, relationship_rank, equipment, custom_character_values, voice_model, pronouns, llm_service/model, tts_service） |

### 1.6 記憶/摘要系統

| 檔案:行號 | 內容 |
|-----------|------|
| `src/remember/remembering.py:1-35` | `Remembering` abstract base class — `get_prompt_text()` + `save_conversation_state()` interface |
| `src/remember/summaries.py` | `Summaries` 實作 — 對話摘要生成與儲存 |
| `src/llm/summary_client.py` | Summary LLM client |

### 1.7 HTTP 通訊協定

| 檔案:行號 | 內容 |
|-----------|------|
| `src/http/communication_constants.py:1-84` | **JSON 欄位名定義**（所有 game↔python 通訊的 key 名稱: actors/context/actions 等） |
| `src/http/routes/mantella_route.py:65-102` | `/mantella` POST endpoint — **唯一 API 入口**（dispatch 到 start/continue/player_input/end_conversation） |

---

