# 兩份唯讀盤點結果

> 屬於 [工作區統整與四條新線（2026-08-23）](README.md)。

## 盤點結果（2026-08-23，唯讀）：`~/notes/projects/modding/skyrim`

171MB／1047 檔。notes repo 已追蹤 994 檔、未追蹤 5 檔、**忽略 48 檔**。

### 發現一：體積主力是不該進 git 的東西

| 路徑 | 大小 | 檔數 | 性質 |
|---|---|---|---|
| `logs/` | 76M | 182 | 其中 **66M 是四個批次的實機截圖 PNG**（character-beauty 22M、simonrim-batch4 三批 42M、final-smoke 12M）；文字紀錄本身很小 |
| `backups/` | 57M | 20 | 16 個 MongoDB 快照（54M）＋ 2 個自製 AgentBridge DLL。**notes 的 .gitignore 已排除整個 `backups/`——從未進過 git 歷史** |
| `qa/` | 21M | 296 | QA harness 的 specs／reports／baselines，JSON 文字 |
| `agent-archive-2026-08-22/` | 15M | 457 | 約 25 條 codex 線的封存輸出 |
| `docs/` `tools/` `artifacts/` `agents/` | 3.3M | 83 | 調查文件、32 個 Python 工具、自製 esp 成品 |

**所以「搬 171MB」是錯的量級。** 扣掉截圖與 DB 快照後，真正該進版控的大約 40MB。
建議定一條規則：**實機截圖與資料庫快照不進 git**——留本機並在對應目錄放一份 INDEX 說明去哪找。
`backups/` 已經被 notes 排除了，搬過來時不要「順手」把它加進版控，那是把 57MB 塞進一個新 repo 的歷史。

### 發現二：有一個我原本不知道的元件——本機 MongoDB mod 資料庫

`backups/skyrim-mongo-*.json`（54M 快照）＋ `docs/mongodb-schema.md`＋掃庫工具。
這是**本地 mod 庫的索引資料庫**，正是第 2 條線（本地 mod 管理）的核心基礎設施，
之前完全沒出現在母 repo 的 README 裡。`mod-library` 這條線要以它為中心，而不是只放成品檔案。

### 發現三：第 3 條線（整合包設計）已經有實體，不是新開的

- `modpack-kr-dev-plan.md`（577 行）—— Modpack-KR 六階段整包計畫：
  Preflight → 人物基線 → NPC 外觀 → 裝備 → Perk/魔法 → 任務/隨從，含 rollback 與完成條件。
- `technical-debt.md`（129 行）—— 現役技術債的單一權威清單。
- `deployment-scope.md`（32 行）—— 現役 profile 的裝／不裝取捨。
- `docs/` 的 `global-source-index.md`、`korean-source-index.md`、`translation-matrix.md`、
  `candidate-review.md` 等 mod 選型調查。

加上母 repo 現有的 `analysis/mod-survey/`（136 份），第 3 條線一開張就是有份量的。

### 發現四：第 4 條線的主線文件也已經存在

`SESSION-LOG.md`（873 行）是整條 Skyrim modding 工作線的 agent 交接主線，
含續行點、人工測試啟動規則、Nexus 自動下載規則。它應該是 `agentctl` 的入口文件。
`tools/` 的 32 個 Python 腳本（漢化層建置、翻譯比對、崩潰分析、profile 稽核）
大部分也歸這裡。

### 發現五：敏感掃描過關，但有一個要處理的殘留

- API key／token／密碼／個資：**沒有真正外洩**。`NEXUS_API_KEY` 兩處命中，一處是讀環境變數的程式碼，
  一處是執行紀錄裡本來就是 `<REDACTED>` 字面值。使用者信箱未出現。
- **要處理**：`agent-archive-2026-08-22/` 底下有多個 git worktree 殘留
  （`codex-l10n/worktrees/profiles-anomaly-main/`、`codex-enairim/worktrees/profiles-enairim/`、
  `codex-pandora/worktrees/profiles-pandora-release/`），這些曾經是 **private profiles repo** 的
  worktree checkout。搬進任何 public 位置前必須確認裡面沒有夾帶 profiles 的實際檔案內容。
- 注意這是 pattern 掃描不是逐行審閱；`docs/` 19 檔與 `agent-archive/` 457 檔未逐檔看過。

### 修正後的分流

| 新線 | 從 notes 搬什麼 |
|---|---|
| `instance` (private) | `README.md` `deployment-scope.md` `jackify-manjaro-plan.md`；`backups/` 的 mongo 快照（**不進版控**）；`logs/` 的部署類文字紀錄 |
| `mod-library` (private) | **MongoDB mod 資料庫**（schema＋掃庫工具＋快照策略）；`my-mods.md`；`artifacts/`（自製 esp 成品）；`agent-archive/PENDING-ARTIFACTS/`；漢化層建置工具與產物；母 repo 現 `dist/` |
| `modpack-design` (public) | `modpack-kr-dev-plan.md` `technical-debt.md`；`docs/` 的選型調查群；母 repo 現 `analysis/mod-survey/` |
| `agentctl` (public) | `SESSION-LOG.md`（入口）；`housecarl.md`；`agents/`；`agent-archive-2026-08-22/`（清過 worktree 殘留後）；`qa/`；`tools/` 多數；母 repo 現 `inbox/` `tools/agent_inbox/` `scripts/` `tests/` |
| **不搬，留本機** | `logs/` 的 66MB 截圖、`backups/` 的 54MB mongo 快照、所有 `__pycache__/` |

---

## 盤點結果（2026-08-23，唯讀）：`~/` 底下

**結論：幾乎沒有東西該搬。** 使用者要求的第 2 步（「~/ 底下屬於我們的也都放進來」）
盤完之後是個近乎空集合——候選項目全部落在這三類：

| 類別 | 例子 |
|---|---|
| 第三方軟體原樣安裝 | `~/games/mod-organizer-2-skyrimspecialedition`（27G，MO2 本體）、`~/dev/mo2installer`、`~/tools/` 的 papyrus-compiler／godot-mcp／vcpkg／steamcmd |
| 執行期狀態／建置產物 | `~/tools/housecarl/server/`（279M，是 `projects/houseCARL` submodule publish 出來的產物，commit 日期 2026-07-10 與 submodule 實際 commit 吻合）、`~/data` 的 mongodb 資料、各種 log |
| 與 Skyrim 無關 | 其他遊戲、`~/ai-models`、dotfiles、`~/venvs` |

### 兩個要使用者拍板的

1. **`~/games/skyrim-qa-baselines`**（3.1M，我們自製的 QA baseline 存檔）。
   技術上是我們的產物，但 `wf/workflows/plans/ai-ingame-qa-loop/README.md` 是**刻意**把它設計成
   repo 外的唯讀主檔，且多份文件寫死這個絕對路徑。搬＝推翻既有設計＋改一堆路徑。
   **建議不搬**，改在 `agentctl/` 放一份 pointer 說明它為什麼在外面。
2. **`~/code/capture`**（20K，手勢／語音辨識小腳本）。名字很像
   `scene-capture-bridge`／`skyrim-voicegen`，但程式碼裡找不到任何 Skyrim 關聯字串，也不是 git repo。
   **需要確認是廢棄原型還是該併入某個 submodule。**

### 順帶發現：`~/Downloads` 有 71 個 Nexus 格式壓縮檔（0.8GB）

這些是下載但沒歸檔的 mod。它們該進的是 `~/skyrim_mods/`（既有的 125GB 下載庫，使用者決定留原地），
**不是母 repo**。但「下載完沒歸檔」這件事本身該由第 2 條線 `mod-library` 的入庫流程管起來——
這正是 MongoDB mod 資料庫該回答的問題：哪些下載過、哪些入庫了、哪些裝了。
建議列為 `mod-library` 的第一個實際工作項。

---
