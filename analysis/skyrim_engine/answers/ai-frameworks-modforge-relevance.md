# 綜合：四個 AI 框架（SkyrimNet / Mantella / MinAI / IntelEngine）能給 ModForge 什麼

> **2026-11-02 勘誤／續篇**：[世界上下文深究](ai-world-context.md)補齊固定版本採集、刷新與缺值證據。下文保留 2026-08 的 authoring 借鏡脈絡；SkyrimNet 現有文件化 MCP，MinAI 原版當下不可公開取得，不能再將「只有 Mantella 有協定」或「官方已棄用」當本輪確證。

盤點日期 2026-08-01。對照對象是同目錄下 2026-07-30 新增的四份分析與其 source-ref：

- `skyrimNet-gameplugin-analysis.md` + `skyrimNet-source-ref.md`
- `mantella-analysis.md` + `mantella-source-ref.md`
- `minAI-analysis.md` + `minAI-source-ref.md`
- `intelEngine-gameplugin-analysis.md` + `intelEngine-source-ref.md`

> 與 `analysis/skyrim_mods/others/modforge-relevance.md` 的分工：那份談的是 ModForge 的**生成能力**（condition 擴充、MCM、批次展開、dialogue override、狀態後端）；本份談的是生成物的**可觀測性與可操控性**——遊戲狀態怎麼被外部讀到、AI 決策怎麼寫回遊戲。兩份不重疊。

## 一、四者的關鍵差異（只記對 ModForge 有決策影響的部分）

一、四者的關鍵差異（只記對 ModForge 有決策影響的部分）的記錄已抽到 [ai-frameworks-modforge-relevance-framework-comparison.json](ai-frameworks-modforge-relevance-framework-comparison.json)（4 列）。

框架：保留原表「框架」欄內容。

進程模型：保留原表「進程模型」欄內容。

對外通道：保留原表「對外通道」欄內容。

原始碼可得性：保留原表「原始碼可得性」欄內容。

統計：共 4 筆記錄、4 欄。

**版本更正**：本輪 Mantella 的 collector→HTTP→Python 可完整核對；SkyrimNet 亦有官方 MCP 讀取／執行文件，但 native server／collector 不公開。不能再說只有 Mantella 有文件化對外介面，詳見[固定版對照](ai-world-context/skyrimnet.md)。IntelEngine 不在本輪重核範圍。

## 二、可借鏡項（依 ROI 排序）

### 1. 遊戲狀態的欄位契約（低成本，直接抄）

不必自己想「一個 AI 要看懂遊戲需要哪些欄位」，兩份現成清單：

- **Mantella**（`src/game_manager.py:282-327 __update_context`、`:330-431 load_character`）：
  角色層 `base_id, ref_id, name, gender, race, relationship_rank, is_in_combat, is_enemy, equipment, custom_values`；
  情境層 `location, time, weather, game_days, nearby_actors, ingame_events`。
- **MinAI**（`minai_EnvironmentalAwareness.psc:32-681`）：21 級時間描述、~60+ 地點關鍵字、Frostfall 溫度/濕度。這是「把數值轉成人看得懂的描述」的分級表。
- **SkyrimNet** 的 `decnpc(actorUUID)` state blob（推導自 `WORKFLOW_PROMPTS.md:97-135`）：另加全技能 0-100、summary/background/personality/speechStyle、四種代名詞、`relationshipRank(-4~4)`、`isVirtual/isDead/isFemale`。
- **SkyrimNet 的行為推論**：`component_npc_state_summary.prompt` 用約 25 種家具關鍵字比對推論 NPC 在做什麼（睡覺/打鐵/祈禱），是規則式而非動畫 hook——低成本得到「NPC 正在幹嘛」。

→ **用途**：當作 agent bridge `GET /state` 的歷史 schema 藍本；現役能力與差距見[本輪 bridge 對照](ai-world-context/bridge-fit.md)。

### 2. 遊戲↔外部程序的 HTTP+JSON 協定（低成本，設計層面）

Mantella `mantella_route.py:65-102` 是單一 endpoint dispatch（start / continue / player_input / end_conversation）。它證明了兩件事：

1. Skyrim 端（Papyrus/SKSE）可以跟本機外部程序用 HTTP JSON 雙向溝通；
2. 這套在 Linux + Proton 下是可行的（Mantella 有 Linux 使用者）。

→ **用途**：既有 agent-bridge HTTP 路線的前例；目前不必再建第二套傳輸層。

### 3. 預渲染字串快取（低成本，與 ModForge 取向天然契合）

IntelEngine 把持久化欄位**預先渲染成 prompt-ready 純文字**存 StorageUtil（`Intel_TaskHistoryRendered` / `Intel_FactsRendered` / `Intel_GossipRendered`，見 `IntelEngine_Core.psc:374-417, 1487-1525, 1533-1596`），SkyrimNet 的 character bio submodule 直接讀來插 prompt，換取 runtime 零組裝成本。

→ **用途**：ModForge 在**生成時**就把 NPC/場景描述渲染成字串塞進 plugin。ModForge 本來就是「生成期決定一切」的取向，這是同型工作。

### 4. SkyrimNet action 註冊表（中成本，綁依賴）

三層 action 註冊（YAML → Papyrus function／Papyrus runtime 註冊／native C++ action），LLM 選定後經 `executionFunctionName` 呼叫 Papyrus（`WORKFLOW_ACTIONS.md:236-268`）。回寫遊戲的 API 在 `SkyrimNetApi.psc`：`RegisterDialogue()/RegisterDialogueToListener()` (`:89-97`)、`DirectNarration()` (`:184-208`)、`GenerateNPCThought()` (`:250-265`)、`RegisterPackage()` (`:117-144`)。

→ **用途**：新增 opt-in spec 區塊，讓 ModForge 產出的 mod 自帶 action YAML + Papyrus，等於「生成出來的 mod 天生可被 LLM 操控」。
→ **代價**：產物多一個 SkyrimNet 依賴。依 `modforge-relevance.md` 第四節的依賴策略，必須做成 opt-in。

### 5. PrismaUI 遊戲內 Chromium overlay（待調查）

IntelEngine `IntelEngine_Core.psc:1918-2029` 的 `RegisterDashboardEvents()` 註冊 dashboard opened/refresh/cancel task/execute action 等事件，由 PrismaUI（遊戲內嵌 Chromium）呈現。

→ **待查**：如果真的是 Chromium，AI 有機會用 DOM 讀 UI 狀態，而不是靠像素辨識。對「UI 驗證」那一段的自動化程度有潛在影響。

### 6. IntelEngine 的實體移動執行路徑（參考）

四者中唯一有「AI 決策 → NPC 真的在世界裡走路」的寫回路徑：`GoToLocation()` (`IntelEngine_Travel.psc:152-293`)、`ScheduleMeeting()` (`IntelEngine_Schedule.psc:121-187`) 直接操作 AI Package，並用 `SkyrimNetApi.DirectNarration()`（經 `SendTaskNarration()`，`IntelEngine_Core.psc:1460-1464`）回饋敘事。

→ ModForge 已有 10 個 PACK template，這份主要當「AI 驅動的 package 切換該長什麼樣」的參考，不是缺口。

## 三、不要做的事

- **MinAI 的整合判斷需重核來源**：本輪官方 repo 回 404，不能據此判定棄用。公開延續 fork 可研究 provider／builder、分頻和 TTL；其 CHIM／Mantella 出口並不等價，詳見[來源身分與邊界](ai-world-context/minai.md)。SkyrimNet 的相容 bridge 不代表其完整實作已搬入。
- **不要指望擴充 SkyrimNet / IntelEngine 的 native 層**：原始碼不在 repo。
- **不要讓 ModForge 預設依賴任何一個**：延續 `modforge-relevance.md` 第四節結論，全部 opt-in，預設維持零外部依賴。

## 四、去向

- 第 1、2 項 → 已由現役 agent-bridge 承接；當前研究入口是[世界上下文](ai-world-context.md)。
- 第 3、4、5 項 → 尚未排程，需要時從本檔取用。
