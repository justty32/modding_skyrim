# 綜合：四個 AI 框架（SkyrimNet / Mantella / MinAI / IntelEngine）能給 ModForge 什麼

盤點日期 2026-08-01。對照對象是同目錄下 2026-07-30 新增的四份分析與其 source-ref：

- `skyrimNet-gameplugin-analysis.md` + `skyrimNet-source-ref.md`
- `mantella-analysis.md` + `mantella-source-ref.md`
- `minAI-analysis.md` + `minAI-source-ref.md`
- `intelEngine-gameplugin-analysis.md` + `intelEngine-source-ref.md`

> 與 `analysis/skyrim_mods/others/modforge-relevance.md` 的分工：那份談的是 ModForge 的**生成能力**（condition 擴充、MCM、批次展開、dialogue override、狀態後端）；本份談的是生成物的**可觀測性與可操控性**——遊戲狀態怎麼被外部讀到、AI 決策怎麼寫回遊戲。兩份不重疊。

## 一、四者的關鍵差異（只記對 ModForge 有決策影響的部分）

| 框架 | 進程模型 | 對外通道 | 原始碼可得性 |
|---|---|---|---|
| **SkyrimNet** | 單進程 in-process，C++ native DLL 直讀記憶體 → Inja 模板 → LLM | **無對外查詢埠**。架構圖裡的 HTTP/WS 是 out-going 呼叫 LLM/TTS 供應商，不是給外部工具連的 server | Papyrus 層有（`SkyrimNetApi.psc`），**native DLL 原始碼不在 repo** |
| **Mantella** | **唯一真正 out-of-process**：外部 Python FastAPI ＋ 遊戲端 SKSE/Papyrus plugin | **HTTP POST `/mantella`**，JSON 雙向。實作 `src/http/routes/mantella_route.py:65-102`，欄位契約 `src/http/communication_constants.py:1-84` | 全開 |
| **MinAI** | 純 Papyrus，無 C++ 無 Python | 只有 Papyrus `ModEvent`（仍在遊戲進程內），真正的外部連結是它橋接出去的 CHIM/Mantella | Papyrus 全開，但**已棄用**，官方導向 SkyrimNet |
| **IntelEngine** | SkyrimNet 的社群擴充 plugin，另依賴一支效能敏感的 native DLL | PrismaUI dashboard（遊戲內嵌 Chromium overlay），是**遊戲內 UI**，不是外部 API | Papyrus 層有，native DLL 原始碼不在 repo |

**結論**：想「從遊戲外部讀狀態、下指令」，四者裡只有 Mantella 提供了現成、文件化的協定。SkyrimNet/IntelEngine 想擴充也沒源碼可改。

## 二、可借鏡項（依 ROI 排序）

### 1. 遊戲狀態的欄位契約（低成本，直接抄）

不必自己想「一個 AI 要看懂遊戲需要哪些欄位」，兩份現成清單：

- **Mantella**（`src/game_manager.py:282-327 __update_context`、`:330-431 load_character`）：
  角色層 `base_id, ref_id, name, gender, race, relationship_rank, is_in_combat, is_enemy, equipment, custom_values`；
  情境層 `location, time, weather, game_days, nearby_actors, ingame_events`。
- **MinAI**（`minai_EnvironmentalAwareness.psc:32-681`）：21 級時間描述、~60+ 地點關鍵字、Frostfall 溫度/濕度。這是「把數值轉成人看得懂的描述」的分級表。
- **SkyrimNet** 的 `decnpc(actorUUID)` state blob（推導自 `WORKFLOW_PROMPTS.md:97-135`）：另加全技能 0-100、summary/background/personality/speechStyle、四種代名詞、`relationshipRank(-4~4)`、`isVirtual/isDead/isFemale`。
- **SkyrimNet 的行為推論**：`component_npc_state_summary.prompt` 用約 25 種家具關鍵字比對推論 NPC 在做什麼（睡覺/打鐵/祈禱），是規則式而非動畫 hook——低成本得到「NPC 正在幹嘛」。

→ **用途**：當作 agent bridge `GET /state` 的 schema 藍本（見 `wf/workflows/plans/ai-ingame-qa-loop/README.md`）。

### 2. 遊戲↔外部程序的 HTTP+JSON 協定（低成本，設計層面）

Mantella `mantella_route.py:65-102` 是單一 endpoint dispatch（start / continue / player_input / end_conversation）。它證明了兩件事：

1. Skyrim 端（Papyrus/SKSE）可以跟本機外部程序用 HTTP JSON 雙向溝通；
2. 這套在 Linux + Proton 下是可行的（Mantella 有 Linux 使用者）。

→ **用途**：`wf/workflows/plans/ai-ingame-qa-loop/README.md` 的整條路以此為前例。

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

- **不要把 MinAI 當整合對象**：已棄用，官方導向 SkyrimNet；SkyrimNet 靠 `skynet_MinAIBridge.psc:1-160` 監聽它的 5 個 ModEvent 做向後相容而已。MinAI 唯一剩餘價值是第 2.1 節那份環境欄位清單。
- **不要指望擴充 SkyrimNet / IntelEngine 的 native 層**：原始碼不在 repo。
- **不要讓 ModForge 預設依賴任何一個**：延續 `modforge-relevance.md` 第四節結論，全部 opt-in，預設維持零外部依賴。

## 四、去向

- 第 1、2 項 → 已展開成 `wf/workflows/plans/ai-ingame-qa-loop/README.md`（AI 全自動 mod QA 迴圈）。
- 第 3、4、5 項 → 尚未排程，需要時從本檔取用。
