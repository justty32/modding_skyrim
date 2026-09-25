# 2. NPC 下令機制 (NPC Command/Control)

[返回入口](../mantella-analysis.md)

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

