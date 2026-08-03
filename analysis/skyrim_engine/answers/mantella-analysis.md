# Mantella 分析：世界狀態、NPC 指令、對話控制

> 來源: `external/frameworks/Mantella/` (clone from https://github.com/art-from-the-machine/Mantella)
> 分析日期: 2026-07-30
> 關注範圍: 世界狀態總結機制、NPC 下令、對話改變（排除 TTS/STT/AI 截圖等）

---

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

## 2. NPC 下令機制 (NPC Command/Control)

### 2.1 雙層 Action 系統

#### Legacy (基本) Actions
LLM 在對話文字中輸出一行 `ActionName: NPC response`。Python 端 parse response 文字，如果找到 action keyword，分離出 action 和對話文字。

Action JSON 定義（`data/actions/*.json`）：
```json
{
    "identifier": "mantella_npc_follow",
    "name": "Follow",
    "description": "Make NPC(s) follow the player.",
    "key": "Follow",
    "parameters": {
        "source": {
            "type": "array",
            "description": "The NPC(s) willing to follow.",
            "items": {"type": "string"},
            "scope": "conversation"
        }
    },
    "required": ["source"],
    "prompt": "If the player asks you to follow them... begin your response with '{key}:'",
    "allowed_games": ["skyrim","Fallout4"],
    "one-on-one": true,
    "multi-npc": true,
    "radiant": false
}
```

關鍵欄位：
- `prompt`: 注入 system prompt 中，告訴 LLM 何時觸發此 action 及格式
- `key`: legacy 系統用的 keyword（LLM 輸出 `Follow: Lead the way.`）
- `one_on_one`/`multi_npc`/`radiant`: 控制此 action 在哪種對話類型中可用

#### Advanced Actions (OpenAI Function Calling)
當 `advanced_actions_enabled = true` 時，actions 被轉換為 OpenAI tool definitions (`FunctionManager.generate_context_aware_tools()`)。

**Context-aware 參數強化**：
- `scope` 欄位定義 entity 來源（`conversation` / `nearby` / `all_npcs` + `_w_player` 變體）
- 執行時動態注入 available entities 到參數 description
- Enum source（如 `idles`）動態填充 enum 值

**參數驗證**（`_validate_arguments_against_schema`）：過濾 LLM hallucinated 的參數；沒有在 schema 中的參數直接丟棄。

**實體名稱驗證**（`_validate_npc_names`）：驗證 LLM 給的 NPC 名稱存在於當前 conversation/nearby scope。

**參數解析**（`_resolve_parameter_to_id`）：將 idle name → FormID 整數，或 NPC name → ref_id。

### 2.2 內建 Actions 清單

```
follow, unfollow, attack, flee, stand_down, barter, inventory,
wait, move_to, lead_to, travel_to, cancel_travel,
check_directions, look, loot, collect_ingredients,
brawl, cast_spell, emote, listen, teleport,
absolve_crime, report_crime, share_conversation,
add_to_conversation, end_conversation
```

### 2.3 Action 執行路徑

1. LLM 回應 → `OutputManager` parse → `Sentence.actions` list
2. 每個 Sentence 可以帶 actions（語音線 + 動作的組合）
3. Python 端透過 JSON response 送回 game：
   ```json
   {
     "mantella_reply_type": "mantella_npc_talk",
     "mantella_npc_talk": {
       "mantella_actor_speaker": "Lydia",
       "mantella_actor_line_to_speak": "Sure, lead the way.",
       "mantella_actor_actions": [{"identifier": "mantella_npc_follow", ...}],
       "mantella_actor_voice_file": "...",
       "mantella_actor_line_duration": 3.5
     }
   }
   ```
4. SKSE Papyrus plugin 接收 → 播放語音 + 執行 Papyrus function 對應的 action

也支援 **純 action response**（`KEY_REPLYTYPE_NPCACTION`）：無語音線，只有 action。

### 2.4 玩家關鍵字觸發 Action

`GameStateManager.player_input()` (`game_manager.py:191-214`)：
如果玩家的輸入文字**完全等於**某個 action 的 keyword（如玩家只打 `Follow`），強制觸發該 action，不走 LLM。

### 2.5 特殊 Internal Actions

- **Listen**: 設定 STT 的 extended pause，讓玩家有更多時間說話。不下傳到 game。
- **Vision**: 啟用下一次 LLM call 的 vision 截圖功能。

---

## 3. 對話改變機制 (Dialogue Changes)

### 3.1 三種對話模式

`conversation_type.py` 定義三種對話類型：

| Type | 場景 | Prompt 來源 |
|------|------|------------|
| `pc_to_npc` | 玩家對單一 NPC | `config.prompt` |
| `multi_npc` | 玩家對多 NPC | `config.multi_npc_prompt` |
| `radiant` | NPC 之間（無玩家） | `config.radiant_prompt` + start/end/continue prompts |

切換條件（`conversation.py:351-371`）：
- 無玩家角色 → `radiant`
- 活躍角色 >= 3 → `multi_npc`
- 否則 → `pc_to_npc`

### 3.2 對話流程

```
start_conversation:
  → conversation_type.get_user_message() 生成第一條 user message
     (pc_to_npc/multi_npc: 自動 greeting "Hello Lydia.")
     (radiant: start_prompt)
  → start_generating_npc_sentences() (背景 thread)

continue_conversation:
  → 檢查 token 是否超限 → 觸發 reload
  → 檢查玩家是否打斷
  → 從 sentence queue 取下一句
  → 如果是純 action → NPCACTION response
  → 如果是正常句子 → NPCTALK response（含 actions）
  → 如果 queue 空了 → 檢查是否結束 / 生成更多

player_input:
  → 獲取玩家文字輸入（或 STT 辨識）
  → update_game_events() 注入 ingame events
  → 檢查是否 end keyword / dismiss NPC / action keyword
  → add user message → start generating
```

### 3.3 Ingame Events 注入

`update_game_events()` (`conversation.py:374-393`)：
每次玩家輸入時，將累積的 ingame events（位置/時間/天氣/戰鬥/關係變化等）塞進 user message 的前面。這讓 LLM 在不增加 message count 的前提下感知世界變化。

### 3.4 對話中斷機制

Mantella 支援**玩家打斷 NPC 說話**：
- STT 持續在背景監聽
- 偵測到玩家說話 → `interrupt_response()` → 送回 `KEY_REPLYTYPE_INTERRUPTED`
- Game 端切掉當前語音，進入 player input 狀態
- 對話 thread 的 generation 被停止、queue 被清空

### 3.5 對話結束

- **玩家說 goodbye keyword** → `initiate_end_sequence()` → 生成 goodbye sentence + `ACTION_ENDCONVERSATION`
- **LLM 觸發 end_conversation tool call** → 同上
- **Dismiss 特定 NPC**: 玩家說 "goodbye Lydia" → 只讓該 NPC 離開，對話繼續
- **Token 超限**: 觸發 reload（"gather thoughts" sentence + `ACTION_RELOADCONVERSATION`）
- **Radiant 對話**: `max_turns` 限制自動結束

### 3.6 對話記憶（跨對話）

`Summaries.save_conversation_state()`:
- 儲存對話 log 為 JSON
- 用 summary LLM 為每位 NPC 生成摘要
- 摘要包含時間戳記（game days）
- 下次對話時摘要注入 prompt 的 `{conversation_summaries}` 變數
- 支援 `ShareConversation` action：讓一個 NPC 分享對話摘要給另一個 NPC

---

## 4. 設計亮點與取捨

### 4.1 世界狀態總結

| 設計 | 優點 | 代價 |
|------|------|------|
| HTTP JSON 傳輸 | 簡單、可讀、語言無關 | 序列化開銷、延遲、只傳送 Papyrus 能讀到的東西 |
| Python `.format()` 模板 | 簡單直接 | 無條件邏輯（vs Inja/Jinja2），擴充性受限 |
| Ingame events 注入 user message | LLM 不增加 message count 就感知世界 | 事件累積過多時會截斷 |
| CSV-based 角色 bio | 易編輯、社群維護 | 新 NPC 需手動添加 |
| 天氣 CSV 查表 | 精確的文字描述 | 需維護對應表 |

### 4.2 NPC 下令

| 設計 | 優點 | 代價 |
|------|------|------|
| OpenAI function calling | LLM 原生支援、結構化輸出 | 需要 tool-calling-capable model |
| Legacy prompt-based actions | 兼容任何 LLM | 需 parse response 文字、較脆弱 |
| Action scope 系統 | 限制 entity 選擇範圍 | 需準確定義 scope |
| Param validation + entity name check | 防止 hallucinated 目標 | 增加複雜度 |
| 無 eligibility 預熱 | 簡單 | 不像 SkyrimNet 那樣可以 pre-filter actions |

### 4.3 對話系統

| 設計 | 優點 | 代價 |
|------|------|------|
| 三種 conversation_type class | 乾淨的 OOP 分離 | 不支援混合模式 |
| Ingame events 在 user message 中 | 不佔用 system prompt token | LLM 可能忽略 |
| Player interruption | 自然的對話體驗 | 需要 STT 持續監聽 |
| Summary LLM 做記憶 | 跨對話連續性 | 需要額外的 LLM call |
| Reload on token overflow | 不丟失 context | 打斷對話流暢度 |

---

## 5. 與 SkyrimNet 的關鍵差異

| 面向 | SkyrimNet | Mantella |
|------|-----------|----------|
| 進程模型 | Native C++ DLL（in-process） | 外部 Python（out-of-process HTTP） |
| 世界狀態讀取 | C++ 直接讀記憶體 | Papyrus → HTTP JSON |
| Prompt 模板 | Inja 模板引擎，100+ decorator 函數 | Python `.format()` + config.ini |
| Action 系統 | YAML → Papyrus function（三層註冊） | JSON → OpenAI function calling (tools) |
| NPC 自主行為 | GameMaster agent（scene planning, beats） | Radiant conversation（max_turns, start/end prompts） |
| 記憶系統 | Vector embedding（語義搜尋），importance/decay | Summary LLM 生成摘要，無 vector search |
| 可擴充性 | Modder API（Papyrus + C++ public API） | Action JSON + config.ini |
| 安裝複雜度 | 單一 mod，無外部程序 | 需安裝 Python + pip dependencies |
