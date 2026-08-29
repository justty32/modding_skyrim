# WORKFLOWS — 工作流派發器

[INDEX](INDEX.md)｜結構 [STRUCTURE](STRUCTURE.md)

使用者要做事 → **從派發表選工作流 → 讀它的入口檔**；細節都在入口檔。

**可以跳流程**：單行或小範圍、低風險、不跨 session 的修正；純查詢或一次性回答，不留 durable 知識；使用者明確要求快速處理；既有工作流只會增加同步成本而不降低風險。跳流程不等於跳過工程規矩——仍要讀必要上下文、不破壞使用者改動、能測就測。

## 派發表

### Skyrim 專屬工作流

這幾條是從實際做過很多次的事凝結出來的，每一條都帶著踩過的坑。**先看這張表**。

| 觸發 | 工作流 | 入口檔 |
|------|--------|--------|
| 「想找 mod，還不知道要哪個」 | mod-discovery | [workflows/mod-discovery/README.md](workflows/mod-discovery/README.md) |
| 「要抓某個 mod 下來裝」 | nexus-intake | [workflows/nexus-intake/README.md](workflows/nexus-intake/README.md) —— 單件與衛星件（擴充／patch／漢化）|
| 「要抓一整套系列（動作、perk、任務框架…）」 | nexus-intake | [workflows/nexus-intake/series.md](workflows/nexus-intake/series.md) —— 每層各自成批、生成式 output |
| 「做中文層／補全現有中文層」 | localization | [workflows/localization/README.md](workflows/localization/README.md) |
| 「改 MO2 profile：裝／移除／改排序」 | profile-change | [workflows/profile-change/README.md](workflows/profile-change/README.md) |
| 「規劃整合包要玩什麼」 | modpack-planning | [workflows/modpack-planning/README.md](workflows/modpack-planning/README.md) |
| 「派一條 codex 線去做事」 | agent-dispatch | [workflows/agent-dispatch/README.md](workflows/agent-dispatch/README.md) |
| 「讓 agent 操作遊戲做測試／實機驗收」 | runtime-qa | [workflows/runtime-qa/README.md](workflows/runtime-qa/README.md) |

典型串接：

```text
mod-discovery → nexus-intake → localization → profile-change → runtime-qa
                                    ↑
                            modpack-planning 決定要哪些
```

### 開發 flavor

碰原始碼的工作流共用 [common/conventions](workflows/common/conventions.md)（寫碼慣例＋真相層優先序）與 [common/code-map](workflows/common/code-map/CODE_MAP.md)（哪個檔負責什麼）。

| 觸發（你說…）| 工作流 | 入口檔（先讀這個）|
|--------------|--------|-------------------|
| 「開發 / 修改某個功能」「**修 bug**」 | **feature-dev** | [workflows/feature-dev/README.md](workflows/feature-dev/README.md) |
| 「跑測試 / 驗證」「這樣改有沒有壞」 | **testing** | [workflows/testing.md](workflows/testing.md) |
| 「重構 / 拆檔 / 整理結構」（行為不變）| **refactor** | [workflows/refactor/README.md](workflows/refactor/README.md) |
| 「搬檔案 / 改目錄名 / 拆 repo」 | **refactor** | [workflows/refactor/moving-things.md](workflows/refactor/moving-things.md) —— 六類會斷的東西 |
| 「查清楚這是怎麼運作的」「這樣做可不可行」 | **investigation** | [workflows/investigation/README.md](workflows/investigation/README.md) |
| 「環境怎麼裝」「fresh clone 後要做什麼」「指令是什麼」「外部工具 / env var」 | **dev-env** | [workflows/dev-env.md](workflows/dev-env.md) |
| 「討論方案」「寫動工計畫」（詳規）| **planning**（管線的後兩段）| [workflows/planning.md](workflows/planning.md) |

### 外部材料／通用

| 觸發 | 工作流 | 入口檔 | 分辨 |
|------|--------|--------|------|
| 「初次接觸陌生專案，建立可延續分析」 | analysis | [workflows/analysis.md](workflows/analysis.md) | 產物落在 `analysis/`；它同時是 `analysis/` 的佈局說明 |
| 「做一包可套用到原專案的 patch」 | patch | [workflows/patch/README.md](workflows/patch/README.md) | 跨 repo、無 git、交給冷啟動 agent、或不能直接改原 repo 時才用 |
| 「把設計方案展開成動工計畫」 | plan | [workflows/plans/README.md](workflows/plans/README.md) | [planning](workflows/planning.md) 管線的**詳規落點**；idea／roadmap 兩階段直接記在 planning.md 的表裡 |

外部材料管線：

```text
analysis → patch 或 planning（roadmap / 詳規）
```

<!-- wf-insert:WORKFLOWS -->

### kernel 內建

| 觸發（你說…）| 工作流 | 入口檔 |
|--------------|--------|--------|
| 「記 / 查踩坑」 | **gotchas** | [workflows/common/gotchas.md](workflows/common/gotchas.md) |
| 「記個想法」「以後要做」「排進 roadmap」「幫我規劃」 | **planning** | [workflows/planning.md](workflows/planning.md) |
| 「記個決定」「為什麼選 A 不選 B」 | **decisions** | [workflows/decisions.md](workflows/decisions.md) |
| 「我的偏好是…」「以後直接做 / 先問」 | **user** | [workflows/common/user.md](workflows/common/user.md) |

**都不符 → 看 [INDEX.md](INDEX.md)**。新開工作流 → 複製 [workflows/TEMPLATE.workflow.md](workflows/TEMPLATE.workflow.md) 並在上表加一列；工作流的統一形式與四級成長軌跡見 [STRUCTURE.md](STRUCTURE.md)。

## 活狀態記哪裡（只列 open，完成即刪）

| 在等誰 | 記哪裡 |
|--------|--------|
| 等**使用者**做 / 驗證 / 決定 | [../WAIT_USER.md](../WAIT_USER.md) |
| 等**同 repo 另一個 session / fork** | [../SESSION-LOG.md](../SESSION-LOG.md) 一行 open |
| 等**別資料夾的 agent** | 信件軸 [`agentctl/inbox/`](../agentctl/inbox/)；協議見 [`agentctl/tools/agent_inbox/PROTOCOL.md`](../agentctl/tools/agent_inbox/PROTOCOL.md)，派線走 [agent-dispatch](workflows/agent-dispatch/README.md) |
