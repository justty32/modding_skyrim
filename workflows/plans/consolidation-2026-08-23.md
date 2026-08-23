# plan：工作區統整與四條新線（2026-08-23）

狀態：**提案中，未執行。** 使用者說「不一定要像我說的那樣，你可以按照你覺得合理的方式做修改，
然後我們一起討論」，所以本文是待討論的設計，不是已定案的待辦。

## 使用者的要求

1. 把 `~/notes/projects/modding/skyrim` 搬進 `~/repo/moddings/skyrim`。
2. 把 `~/` 底下屬於我們的東西也收進來（`~/skyrim_mods` 除外）。
3. `projects/` 下新增四條線：
   1. **本地 Skyrim 管理** —— 裝了哪些 mod、現役 profile、MO2 設定；profile repo 當 submodule。
   2. **本地 Skyrim mod 管理** —— 下載的 mod、我們做的漢化 mod、自製插件與 mod。
   3. **整合包設計** —— mod 調查、想玩的內容與對應 mod 集合的討論、規劃。
   4. **讓 AI 操控 Skyrim 的總控 repo** —— 工作流、插件、文檔、資源；使用者建議提升到頂層。

## 兩個硬約束（先講，因為它們決定整個設計）

### A. 公開性降級

| repo | 位置 | 可見性 |
|---|---|---|
| `justty32/comp_manjaro` | `~/notes` | **PRIVATE** |
| `justty32/modding_skyrim` | `~/repo/moddings/skyrim` | **PUBLIC** |
| `justty32/modpack-kr-profiles` | MO2 instance 內 | **PRIVATE** |

`~/notes/projects/modding/skyrim`（171MB）現在活在 private repo 裡。整包倒進 public 母 repo
等於把它全部公開。**所以「搬過來」不能是單純 `mv`**——必須依內容性質分流，敏感的落到
private submodule。這也正好是下面把 1、2 設為 private 的理由。

### B. profiles 的工作目錄不能有兩份

profiles repo 的實體在
`~/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles`（57MB），
**MO2 執行期要直接讀它**。git submodule 需要工作目錄真的在 submodule 路徑上，
所以「掛成 `projects/instance/profiles`」與「留在 MO2 底下」天然衝突。三個選項：

| 選項 | 做法 | 代價 |
|---|---|---|
| **B1 symlink**（建議） | 實體移到 `projects/instance/profiles`，MO2 原位置改成 symlink 指過去 | Wine 走 `Z:\home\...` 能跟隨 Linux symlink，但這是動到能跑的遊戲設定，要先備份＋實機驗證一次啟動 |
| B2 二次 clone | submodule 路徑放一份唯讀鏡像，MO2 那份照舊 | 兩份會漂移，等於沒統整；MO2 每次改 profile 都要手動同步 |
| B3 不做 submodule | 只在 `projects/instance/` 寫一份 pointer 文件記 remote 與現役 commit | 最安全、零風險，但沒達成使用者「profile 當 submodule」的要求 |

**建議 B1，但排在最後做**，且做之前先 `git push` profiles 的 4 個未推 commit。

## 提議的佈局

```
skyrim/                          ← public 母 repo
├─ README.md  AGENTS.md  CLAUDE.md        入口三件套
├─ wf/                                    工作流骨架（8 個骨架 md + 現 workflows/）
│
├─ agentctl/          ★4  AI 操控總控     public submodule，頂層
│
├─ projects/
│  ├─ instance/       ★1  本地 Skyrim 管理  private submodule
│  │   └─ profiles/                        → modpack-kr-profiles (private)
│  ├─ mod-library/    ★2  本地 mod 管理     private submodule
│  ├─ modpack-design/ ★3  整合包設計        public submodule
│  └─ （原有 11 個軟體開發 repo 不動）
│
├─ analysis/                              引擎／SKSE 知識（扣掉 mod-survey）
├─ external/                              他人素材落點
└─ patches/
```

### 為什麼 1／2 要 private

- **`mod-library`**：我們做的漢化層是**他人 mod 譯文的衍生作品**。放 public repo 是散布問題，
  不是隱私問題，但一樣不能做。
- **`instance`**：本身不算機密，但它掛的 `profiles` 已經是 private，且內容是從 private 的
  `~/notes` 搬過來的。維持 private 才不會在搬移過程中降級。
- **`modpack-design`** 是調查與規劃，public 沒問題。
- **`agentctl`** 是工作流與工具，public 沒問題（Nexus API key 一律走環境變數，不進 repo）。

### 一點保留意見：`projects/` 的語意被稀釋

`projects/` 現在的定義是「獨立**軟體**開發 repo，彼此靠協議／CLI 對接、不整合」
（見根 README）。1／2／3 是**狀態與知識**，不是軟體。混在一起後這層分類就不再說明任何事。

我照使用者說的放進 `projects/`，但建議在根 README 把表格拆成
**開發線**（ModForge、scene-capture-bridge…）與**管理線**（instance、mod-library、modpack-design）
兩張，讓分類重新有意義。若你偏好乾淨切開，替代方案是 1／2／3 也升頂層，`projects/` 維持純軟體。

## 內容怎麼分流

這四條線**不是四個新空資料夾**——三條的內容已經散在現有各處，這次是重新分割：

| 新線 | 從哪裡來 |
|---|---|
| `instance` | `~/notes/.../skyrim/` 的 `logs/` `backups/` `qa/`；MO2 設定備份；`WAIT_USER.md` 的部署類條目；profiles submodule |
| `mod-library` | 現 `dist/`（59MB／393 檔，自製成品）→ `mine/`；漢化層產物 → `l10n/`；`~/skyrim_mods/`（125GB 留原地）只放 manifest → `downloads/`；現 `external/` 的職責併入 |
| `modpack-design` | 現 `analysis/mod-survey/`（136 份他人 mod 調查）；`workflows/plans/` 的選型類計畫；新增「想玩什麼」的規劃 |
| `agentctl` | 現 `inbox/` `tools/agent_inbox/` `scripts/` `tests/`；`workflows/` 的 agent 相關部分；`~/notes/.../skyrim/` 的 `agents/` `agent-archive-2026-08-22/` `tools/`；Nexus 下載流程的工程化 |

### `agent-bridge` 怎麼辦

`mo2ctl` 在 `projects/agent-bridge/client/`，它就是「AI 操控 Skyrim」的核心。兩種做法：

- **建議：留在 `projects/agent-bridge`**，`agentctl` 只做編排層（工作流、交接書範本、inbox、
  Nexus 下載器、runbook），README 指過去說明哪幾個 `projects/` repo 是它的插件。
  這符合根 README 已宣示的「靠協議對接、不整合」原則，churn 最小。
- 替代：`agent-bridge`／`scene-capture-bridge`／`houseCARL` 變成 `agentctl` 的巢狀 submodule。
  分類更漂亮，但巢狀 submodule 日常更新很煩。

## 風險

1. **敏感內容**：從 notes 搬出的每個檔案都要先過 API key／token／個資掃描（已派 subagent 盤點）。
2. **交叉連結**：`analysis/mod-survey/` 搬走會斷母 repo 內大量相對連結（`analysis/` 共 716 個追蹤檔）。
   搬完要跑 `scripts/check_markdown_links.py` 歸零。
3. **git 歷史**：搬進新 repo 預設會失去 notes 側的 commit 歷史。要保留就得用
   `git subtree split` 或 `git filter-repo`；不保留就在新 repo 的 README 註明歷史在 comp_manjaro 哪個路徑。
4. **未推的 commit**：動手前必須清乾淨——母 repo 3 個、profiles 4 個。
5. **`external/` 只有 1 個追蹤檔**（193MB 是 gitignore 掉的 frameworks clone），搬移前別誤以為有內容。

## 前置條件（動手前必須完成）

- [ ] 母 repo 3 個未推 commit → push
- [ ] profiles repo 4 個未推 commit → push；工作目錄 2 個未提交變更 → 決定去留
- [ ] `~/notes` 的 9 個 untracked 檔 → commit + push（含本次要搬走的 3 份 log 與 CONSOLIDATION-TODO）
- [ ] 全量 tar 備份（母 repo + notes/skyrim + profiles）
- [ ] 兩份盤點報告（`INV-notes-skyrim.md`、`INV-home.md`）確認無敏感內容

## Done when

- [ ] `~/notes/projects/modding/skyrim` 清空（或只剩一份轉址 README）
- [ ] `~/` 底下該收的都收了，`~/skyrim_mods` 未被觸碰
- [ ] 四條線各自有 remote、各自可獨立 clone、可見性正確
- [ ] `check_markdown_links.py` 全綠
- [ ] 從 Steam 點 Skyrim 仍能正常啟動（B1 若採用，這是唯一的實機驗收）

---

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

`backups/skyrim-mongo-*.json`（54M 快照）＋ `docs/mongodb-schema.md`＋`tools/scan_mod_library.py`。
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
`tools/` 的 32 個 Python 腳本（漢化層建置、翻譯比對、崩潰分析 `triage_crash.py`、
profile 稽核 `audit_overwrite.py`）大部分也歸這裡。

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
| `mod-library` (private) | **MongoDB mod 資料庫**（schema＋`scan_mod_library.py`＋快照策略）；`my-mods.md`；`artifacts/`（自製 esp 成品）；`agent-archive/PENDING-ARTIFACTS/`；漢化層建置工具與產物；母 repo 現 `dist/` |
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
   技術上是我們的產物，但 `workflows/plans/ai-ingame-qa-loop.md` 是**刻意**把它設計成
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

## 執行結果（2026-08-23，已完成）

使用者拍板：1／2／3 也升頂層（`projects/` 維持純軟體）；profiles 走 B1 symlink；
`~/games/skyrim-qa-baselines` 不搬；`~/code/capture` 別管。

### 落地佈局

```
skyrim/                    public 母 repo
├─ instance/               private submodule  ← profiles/ (private submodule)
├─ mod-library/            private submodule  ← 必須永遠 private
├─ modpack-design/         private submodule
├─ agentctl/               private submodule
├─ projects/               11 個軟體 repo，未動
└─ analysis/ external/ patches/ scripts/ tests/ workflows/
```

四個 repo：`skyrim_instance`、`skyrim_mod_library`、`skyrim_modpack_design`、`skyrim_agentctl`。
**全部先開 private**，避免未審內容有任何一刻躺在公開位置。

### 搬移驗證

以「size + basename」對 notes 側 1047 檔逐檔比對，未落地的只有 14 個：

- 10 個是**刻意排除**的 private profiles worktree 複本（`agent-archive/*/worktrees/`）
- `README.md` → 改寫成轉址 stub
- `CONSOLIDATION-TODO.md` → `agentctl/handoffs/superseded/`，標記已被取代
- 2 個 `.html`/`.csv` 驗證輸出 → 補進 `agentctl/logs/`

刻意留在 notes 不搬的：53 個實機截圖（66MB）、20 個 MongoDB 快照與 DLL 備份（57MB）、
28 個 `__pycache__`。notes 側留一份轉址 README 說明每樣東西去了哪。

### 順帶修掉的曝險

`dist/mods/` 的 34 個資料夾**幾乎全是他人 mod 的繁中翻譯層，內含完整原始 ESP 複本**
（`USSEP-Traditional-Chinese-4.3.8a/` 裡是 20MB 的完整 USSEP plugin），**一直躺在 public 母 repo**。
已移到 private 的 `mod-library/l10n/mods/`。

**但母 repo 的 git 歷史仍然保有它們**——HEAD 乾淨了，歷史沒有。

### profiles symlink

```
modorganizer2/profiles -> /home/lorkhan/repo/moddings/skyrim/instance/profiles
```

改動當下 MO2 與 Skyrim 都沒在跑（唯一的 wineserver 屬於 appid 553850，不是 Skyrim 的 489830），
也沒有行程開著該目錄。改完確認：透過 symlink 讀得到 290 個啟用 mod、`git status` 乾淨、
`selected_profile=@ByteArray(Modpack-KR)` 未受影響。備份在 scratchpad。
還原指令寫在 `instance/README.md`。

### 收工狀態

7 個 repo（母、四條線、profiles、notes）全部 `dirty=0 unpushed=0`；
`check_markdown_links.py` 433 檔 595 連結全綠。

## 還沒做的

| # | 事項 | 為什麼還沒做 |
|---|---|---|
| 1 | **從 Steam 啟動一次驗證 symlink** | 只有使用者能做。這是 B1 唯一的實機驗收 |
| 2 | `modpack-design` 與 `agentctl` 是否翻成 public | 需要逐檔審完 457 檔 archive 與 296 檔 qa 才能確定沒夾帶第三方內容 |
| 3 | 母 repo 是否用 `git filter-repo` 清掉歷史裡的翻譯層 | 要重寫歷史並強制推送，是獨立決定 |
| 4 | `~/Downloads` 71 個 Nexus 壓縮檔（0.8GB）歸檔 | 待使用者確認要不要進 `~/skyrim_mods/` |
| 5 | SCB camera-ray 15 條驗收 | 中斷於統整之前，證據只支持 2 條 |
