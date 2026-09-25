# 3. 對話改變相關原始碼

[返回入口](../minAI-source-ref.md)

## 3. 對話改變相關原始碼

### 3.1 對話事件攔截 — Mantella 橋接

3.1 對話事件攔截 — Mantella 橋接的記錄已抽到 [dialogue-control-mantella-bridge-functions.json](dialogue-control-mantella-bridge-functions.json)（8 列）。

檔案:行號：保留原表「檔案:行號」欄內容。

內容：保留原表「內容」欄內容。

統計：共 8 筆記錄、2 欄。

### 3.2 Context API（外部 Mod 對話注入）

| 檔案:行號 | 內容 |
|-----------|------|
| `Scripts/Source/minai_MainQuestController.psc:326-329` | `OnRegisterEvent()` — 接收外部 ModEvent → `RegisterEvent(eventLine, eventType)` |
| `Scripts/Source/minai_MainQuestController.psc:340-343` | `OnRequestResponse()` — 接收外部 ModEvent → `RequestLLMResponseFromActor()` |
| `Scripts/Source/minai_MainQuestController.psc:354-357` | `OnRequestResponseDialogue()` — 接收外部 ModEvent → `RequestLLMResponseNPC()` |
| `Scripts/Source/minai_MainQuestController.psc:368-376` | `OnSetContext()` — 接收外部 ModEvent → `AIFF.StoreContext()` 或 fallback `RegisterEvent()` |

### 3.3 Dungeon Master / Narrator / Roleplay / Diary 快捷鍵

3.3 Dungeon Master / Narrator / Roleplay / Diary 快捷鍵的記錄已抽到 [dialogue-control-narrator-hotkey-functions.json](dialogue-control-narrator-hotkey-functions.json)（6 列）。

檔案:行號：保留原表「檔案:行號」欄內容。

內容：保留原表「內容」欄內容。

統計：共 6 筆記錄、2 欄。

### 3.4 Sensuality/Sex 場景的對話處理

| 檔案 | 內容 |
|------|------|
| `Scripts/Source/minai_SexAwareness.psc` | 性愛場景感知 |
| `Scripts/Source/minai_AmbientSexTalk.psc` | 性愛場景中的 ambient dialogue |
