# Mantella — 原始碼出處索引

> 路徑根: `external/frameworks/Mantella/`
> 注意: Mantella 是 Python 外部程序，遊戲端 Mantella Spell（SKSE Papyrus plugin）在另一個 repo。以下指向 Mantella Python 端原始碼。

---

## 1. 世界狀態總結相關原始碼

### 1.1 遊戲狀態接收與解析

| 檔案:行號 | 內容 |
|-----------|------|
| `src/game_manager.py:57-76` | `start_conversation()` — 建立 Context + Conversation |
| `src/game_manager.py:282-327` | `__update_context()` — **解析來自遊戲的 JSON 狀態**（actors list, location, time, game_days, ingame_events, weather, npcs_nearby, config_settings, custom_context_values） |
| `src/game_manager.py:330-431` | `load_character()` — **從 JSON 建構 Character 物件**（base_id, ref_id, name, gender, race, voice_type, is_in_combat, is_enemy, relationship_rank, equipment, custom_values；bio/voice_model 從 CSV 查表或 cache） |

### 1.2 Context 物件 — 世界狀態聚合與變化偵測

| 檔案:行號 | 內容 |
|-----------|------|
| `src/conversation/context.py:22-47` | `Context.__init__()` — 狀態變數初始化 |
| `src/conversation/context.py:105-130` | `set_vision_hints()` — Vision hints（距離分類: very close/close/medium/far/very far） |
| `src/conversation/context.py:174-241` | `update_context()` — **核心：世界狀態更新入口**（location/time/weather/npcs_nearby/custom_events/custom_context_values 全部在這裡被更新並生成 ingame_events） |
| `src/conversation/context.py:244-281` | `__update_ingame_events_on_npc_change()` — **NPC 狀態變化偵測**（combat 狀態變化 → "{name} is now in combat!"；enemy 狀態變化 → "{name} is attacking {player}"；relationship 變化） |
| `src/conversation/context.py:283-309` | `__get_trust()` — 信任關係計算（stranger → acquaintance → friend → close friend / lover / enemy，由 relationship_rank + 對話次數共同決定） |
| `src/conversation/context.py:331-349` | `__get_trusts()` — 所有 NPC 的信任關係文字生成 |
| `src/conversation/context.py:351-368` | `get_character_names_as_text()` — NPC 名字列表自然語言格式化 |
| `src/conversation/context.py:371-383` | `__get_bios_text()` — NPC bio 聚合 |
| `src/conversation/context.py:385-395` | `__get_npc_equipment_text()` — NPC 裝備描述聚合 |
| `src/conversation/context.py:397-413` | `__get_action_texts()` — Legacy action prompt 文字生成 |
| `src/conversation/context.py:416-521` | `generate_system_message()` — **核心：Prompt 變數填入**（用 Python `.format()` 填入 player_name/player_description/bios/trust/location/weather/time/language/conversation_summaries/actions 等 ~20 個變數；token limit 檢查 → 先丟 summaries 再丟 bios） |

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

## 2. NPC 下令相關原始碼

### 2.1 Action JSON 定義

| 檔案 | 內容 |
|------|------|
| `data/actions/follow.json` | `Follow` action（NPC 跟隨玩家） |
| `data/actions/unfollow.json` | `Unfollow` action |
| `data/actions/attack.json` | `Attack` action |
| `data/actions/flee.json` | `Flee` action |
| `data/actions/stand_down.json` | `Stand Down` action |
| `data/actions/barter.json` | `Barter` (trade) action |
| `data/actions/inventory.json` | `Inventory` action |
| `data/actions/wait.json` | `Wait` action |
| `data/actions/move_to.json` | `Move To` action |
| `data/actions/lead_to.json` | `Lead To` action |
| `data/actions/travel_to.json` | `Travel To` action |
| `data/actions/cancel_travel.json` | `Cancel Travel` action |
| `data/actions/check_directions.json` | `Check Directions` action |
| `data/actions/look.json` | `Look` action |
| `data/actions/loot.json` | `Loot` action |
| `data/actions/collect_ingredients.json` | `Collect Ingredients` action |
| `data/actions/brawl.json` | `Brawl` action |
| `data/actions/cast_spell.json` | `Cast Spell` action |
| `data/actions/emote.json` | `Emote` action（idle animation） |
| `data/actions/listen.json` | `Listen` action（extended STT pause） |
| `data/actions/teleport.json` | `Teleport` action |
| `data/actions/absolve_crime.json` | `Absolve Crime` action |
| `data/actions/report_crime.json` | `Report Crime` action |
| `data/actions/share_conversation.json` | `Share Conversation` action（跨 NPC 對話分享） |
| `data/actions/add_to_conversation.json` | `Add To Conversation` action |
| `data/actions/end_conversation.json` | `End Conversation` action |

### 2.2 Function Manager — Action 引擎

| 檔案:行號 | 內容 |
|-----------|------|
| `src/actions/function_manager.py:14-17` | `FunctionManager` class — **action 註冊表** (`_actions` dict) |
| `src/actions/function_manager.py:154-218` | `load_all_actions()` — 從 `data/actions/*.json` 載入所有 actions；支援 disabled actions filter |
| `src/actions/function_manager.py:222-246` | `get_legacy_actions()` — 轉換為 legacy prompt-based Action 物件 |
| `src/actions/function_manager.py:250-277` | `_load_action_file()` — 單一 JSON 載入，處理 single/array 兩種格式，prefix `mantella_` |
| `src/actions/function_manager.py:19-152` | `parse_function_calls()` — **解析 LLM 回應中的 function calls**（validate arguments against schema, validate entity names, resolve parameter IDs, duplicate filter, side effects） |
| `src/actions/function_manager.py:281-340` | `generate_context_aware_tools()` — **生成 OpenAI tools**（filter by game compatibility, conversation type, populate dynamic enums, add NPC context to parameters） |
| `src/actions/function_manager.py:435-460` | `_validate_arguments_against_schema()` — 過濾 LLM hallucinated 參數 |
| `src/actions/function_manager.py:464-521` | `_validate_npc_names()` — **驗證 LLM 指定的 NPC 名稱存在於 scope 內**（支援 "player" alias） |
| `src/actions/function_manager.py:525-555` | `_populate_dynamic_enums()` — 動態填充 enum 值（如 idle names） |
| `src/actions/function_manager.py:559-607` | `_add_npc_context_to_parameters()` — **scope-based entity list 注入**（conversation/nearby/all_npcs + _w_player variant） |
| `src/actions/function_manager.py:637-680` | `_resolve_parameter_to_id()` — 參數 → 遊戲 ID 解析（idle name → FormID, NPC name → ref_id） |

### 2.3 Action 配置

| 檔案:行號 | 內容 |
|-----------|------|
| `src/config/definitions/action_definitions.py:34-69` | `ActionDefinitions` — `advanced_actions_enabled` / `disabled_actions` / `custom_function_model` 設定 |
| `src/config/definitions/action_definitions.py:48-70` | Default disabled actions 列表 |

### 2.4 對話中的 Action 觸發

| 檔案:行號 | 內容 |
|-----------|------|
| `src/game_manager.py:177-223` | `player_input()` — **玩家關鍵字觸發 action**（clean_text == action.keyword → 直接發送 NPCACTION response，不走 LLM）；Listen/Vision internal actions |
| `src/conversation/conversation.py:154-157` | `continue_conversation()` — action-only sentence 處理（`KEY_REPLYTYPE_NPCACTION`） |
| `src/conversation/conversation.py:395-422` | `resume_after_interrupting_action()` — action 結果回來後的 LLM 續寫 |

---

## 3. 對話改變相關原始碼

### 3.1 對話流程

| 檔案:行號 | 內容 |
|-----------|------|
| `src/conversation/conversation.py:34-80` | `Conversation.__init__()` — 對話初始化 |
| `src/conversation/conversation.py:112-126` | `start_conversation()` — 建立起始 greeting → 開始 LLM generation |
| `src/conversation/conversation.py:128-201` | `continue_conversation()` — **主對話循環**（token check → player interruption check → sentence queue → NPCTALK/NPCACTION/PLAYERTALK/ENDCONVERSATION reply） |
| `src/conversation/conversation.py:203-224` | `__interruption_enabled()` / `__interrupt_response()` — **玩家打斷機制** |
| `src/conversation/conversation.py:227-314` | `process_player_input()` — **玩家輸入處理**（mic/text 輸入、silence auto-response、end keyword / dismiss NPC / action keyword 檢查、user message 建立 → LLM generation） |
| `src/conversation/conversation.py:335-348` | `update_context()` — 對話中 context 更新 |
| `src/conversation/conversation.py:374-393` | `update_game_events()` — **ingame events 注入 user message**（將累積的世界變化事件注入到玩家輸入的前面） |
| `src/conversation/conversation.py:425-444` | `retrieve_sentence_from_queue()` — blocking 取下一句 |
| `src/conversation/conversation.py:447-463` | `initiate_end_sequence()` — 對話結束（goodbye sentence + `ACTION_ENDCONVERSATION`） |
| `src/conversation/conversation.py:480-489` | `end()` — 結束對話 + 儲存 summary |
| `src/conversation/conversation.py:492-507` | `__start_generating_npc_sentences()` — 背景 thread 開始 LLM generation（含 tools generation） |
| `src/conversation/conversation.py:529-574` | `__save_conversation()` / `__prepare_eject_npc()` / `__initiate_reload_conversation()` / `reload_conversation()` |

### 3.2 對話類型系統

| 檔案:行號 | 內容 |
|-----------|------|
| `src/conversation/conversation_type.py:1-62` | `conversation_type` abstract base — `generate_prompt()`, `get_user_message()`, `should_end()` |
| `src/conversation/conversation_type.py:64-90` | `pc_to_npc` — **玩家對單一 NPC**（automatic greeting "Hello Lydia."） |
| `src/conversation/conversation_type.py:92-116` | `multi_npc` — **玩家對多 NPC**（group greeting） |
| `src/conversation/conversation_type.py:118-156` | `radiant` — **NPC 之間對話**（無玩家；start_prompt → LLM 回應 → continue_prompt → ... → end_prompt；max_turns 限制） |

### 3.3 LLM Response Parsing

| 檔案:行號 | 內容 |
|-----------|------|
| `src/llm/output/output_parser.py` | Output parser base |
| `src/llm/output/sentence_end_parser.py` | 句子邊界偵測 |
| `src/llm/output/actions_parser.py` | **Legacy action parsing**（從 LLM 回應文字中擷取 `ActionName: response` 格式） |
| `src/llm/output/narration_parser.py` | Narration parsing |
| `src/llm/output/italics_parser.py` | Italics parsing |
| `src/llm/output/change_character_parser.py` | Character change parsing |
| `src/llm/output/clean_sentence_parser.py` | 句子清理 |
| `src/llm/output/sentence_accumulator.py` | 句子累積器 |

### 3.4 LLM Clients

| 檔案 | 內容 |
|------|------|
| `src/llm/llm_client.py` | 主要 LLM client |
| `src/llm/function_client.py` | Function calling client（OpenAI tools） |
| `src/llm/summary_client.py` | Summary LLM client |
| `src/llm/image_client.py` | Vision/image client |
| `src/llm/message_thread.py` | 對話 thread 管理 |
| `src/llm/messages.py` | Message 類別（SystemMessage, UserMessage, AssistantMessage） |

### 3.5 Output Manager

| 檔案 | 內容 |
|------|------|
| `src/output_manager.py` | `ChatManager` — TTS 合成、語音管理、sentence 生成 |

### 3.6 GameManager — 對話生命週期

| 檔案:行號 | 內容 |
|-----------|------|
| `src/game_manager.py:57-79` | `start_conversation()` — 建立 Context + Conversation + STT |
| `src/game_manager.py:115-174` | `continue_conversation()` — 對話循環（調用 `Conversation.continue_conversation()` → 處理 TTS/prepare voice files/sentence_to_json） |
| `src/game_manager.py:177-223` | `player_input()` — 玩家輸入 → `Conversation.process_player_input()` |
| `src/game_manager.py:226-236` | `end_conversation()` — 結束對話 + summary |
| `src/game_manager.py:238-251` | `process_stt_setup()` — STT 設定（mic/text/push-to-talk） |
| `src/game_manager.py:253-277` | `character_to_json()` / `sentence_to_json()` — JSON 序列化 |
