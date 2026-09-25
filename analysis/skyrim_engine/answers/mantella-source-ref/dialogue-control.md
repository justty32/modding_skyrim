# 3. 對話改變相關原始碼

[返回入口](../mantella-source-ref.md)

## 3. 對話改變相關原始碼

### 3.1 對話流程

3.1 對話流程的記錄已抽到 [dialogue-control-conversation-functions.json](dialogue-control-conversation-functions.json)（12 列）。

檔案:行號：保留原表「檔案:行號」欄內容。

內容：保留原表「內容」欄內容。

統計：共 12 筆記錄、2 欄。

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
