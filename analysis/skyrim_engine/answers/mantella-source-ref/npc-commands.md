# 2. NPC 下令相關原始碼

[返回入口](../mantella-source-ref.md)

## 2. NPC 下令相關原始碼

### 2.1 Action JSON 定義

2.1 Action JSON 定義的記錄已抽到 [npc-commands-action-definitions.json](npc-commands-action-definitions.json)（26 列）。

檔案：保留原表「檔案」欄內容。

內容：保留原表「內容」欄內容。

統計：共 26 筆記錄、2 欄。

### 2.2 Function Manager — Action 引擎

2.2 Function Manager — Action 引擎的記錄已抽到 [npc-commands-action-engine-functions.json](npc-commands-action-engine-functions.json)（11 列）。

檔案:行號：保留原表「檔案:行號」欄內容。

內容：保留原表「內容」欄內容。

統計：共 11 筆記錄、2 欄。

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

