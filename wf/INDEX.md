# INDEX — skyrim 專案地圖

skyrim = **Skyrim SE modding 工作區**：母 repo 管開發（`projects/`）與知識（`analysis/`），部署狀態、mod 庫、整合包設計、AI 操控總控各自獨立成線。本檔只描述**頂層**：每列一句話＋連結；**工作區入口見根 [README.md](../README.md)**；開發專案的分工見 [projects/README.md](../projects/README.md)，研究分類見 [analysis/README.md](../analysis/README.md)。

## Repo 佈局（精簡）

| 路徑 | 內容 |
|------|------|
| [`instance/`](../instance/) | **四條主線之一**：本機部署狀態——MO2 instance、現役 profile `modpack-main`、load order、已裝 mod、實機驗收狀態、部署規劃。**本機部署狀況一律歸這裡**（取代舊的「歸 `~/notes` 管」劃分）；`~/notes/projects/modding/skyrim/` 只留不進版控的截圖與 MongoDB 快照 |
| [`mod-library/`](../mod-library/) | **四條主線之一**：mod 庫——MongoDB 索引、自製繁中翻譯層、自製插件與修正 esp |
| [`modpack-design/`](../modpack-design/) | **四條主線之一**：整合包設計——Gameplay 遷移批次、技術債、選型調查 |
| [`agentctl/`](../agentctl/) | **四條主線之一**：AI 操控總控——派線協議、agent 交接、資源鎖、QA harness、執行證據 |
| [`agentctl/handoffs/`](../agentctl/handoffs/) | 每場交接書與各隊 `REPORT.md` |
| [`agentctl/inbox/`](../agentctl/inbox/) | 五通道信箱與 `ROSTER.md` 身份聲明簿 |
| [`agentctl/docs/`](../agentctl/docs/) | 驅動 agent、資源鎖、模型分級與 houseCARL 現行文件 |
| [`projects/`](../projects/README.md) | 獨立開發專案；工具、內容專案與 Git 操作說明都在這一層入口 |
| [`analysis/`](../analysis/README.md) | 引擎、mod、工具與素材來源的研究分類；文件慣例見 [analysis 工作流](workflows/analysis.md) |
| [`external/`](../external/README.md) | 他人框架原始碼的落點 |
| `wf/` | 工作流骨架：派發見 [WORKFLOWS.md](WORKFLOWS.md)、結構原則見 [STRUCTURE.md](STRUCTURE.md)、共享區 [workflows/common/](workflows/common/README.md)、檢查腳本 `wf/tools/wf-lint.sh` |
| `wf/tools/` | `wf-lint.sh`（連結／超標／BIGLIST／殘留檢查）、`tabledb.py`＋`tabledb_links.py`（`wf-table/1` 資料檔 CRUD 與連結檢查）、`find_big_lists.py`（找 >1 KB 條列區塊）、`fix_moved_links.py`（搬檔後按 moves.tsv 重寫連結）|
| [`tools/`](../tools/) | 母 repo 的文件驗證：`check_markdown_links.py`、`check_submodule_pins.py` 與其測試 |
| [`.claude/commands/`](../.claude/commands/) | slash 指令適配層（可選）。Claude Code 只讀專案根的這層，非侵入式佈局也留在根；沒有 slash 機制的工具忽略本目錄，直接跑 `wf/tools/wf-lint.sh` |
<!-- wf-insert:INDEX -->

## 可見性

- **母 repo 是 public**（`justty32/modding_skyrim`，2026-08-03 起），`projects/` 下 11 個軟體 repo 以 submodule 管理。
- **四條主線目前都是 private**；`mod-library` 因含他人 mod 的完整原始 ESP 複本而**必須永遠 private**。
- **不要從 public 母 repo 推論各子 repo 的公開範圍**；`modpack-design`、`agentctl` 標「暫時」是還沒逐檔審查完內容。
- 根 [README.md](../README.md) 是**外來 agent 的入口**：被派來「找做好的 mod 去部署」時，它必須答得出「成品在哪」（`mod-library/`）與「現在裝了什麼」（`instance/`）；新增產物類型或改佈局時同步更新。

## 頂層文件

| 檔案 | 角色 |
|------|------|
| [WORKFLOWS.md](WORKFLOWS.md) | 派發器：意圖 → 工作流入口 |
| [STRUCTURE.md](STRUCTURE.md) | 結構整理參考（被動）：分層、膨脹即拆、四級成長、archive、工作流形式 |
| [../SESSION-LOG.md](../SESSION-LOG.md) | 母 repo 的 open 進度（Skyrim 工作線的交接主線在 `agentctl/SESSION-LOG.md`）|
| [../WAIT_USER.md](../WAIT_USER.md) | 等使用者親自做 / 驗證的事 |
