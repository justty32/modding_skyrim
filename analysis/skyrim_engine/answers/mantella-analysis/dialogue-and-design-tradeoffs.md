# 3. 對話改變機制 (Dialogue Changes)

[返回入口](../mantella-analysis.md)

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
