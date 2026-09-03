# skyrim — AI agent 專案備忘

skyrim = **Skyrim SE modding 工作區**：母 repo 管開發（`projects/`）與知識（`analysis/`），部署狀態／mod 庫／整合包設計／AI 操控總控各自獨立成線。本檔是最頂層路由器，只指向下一層；分層原則見 [STRUCTURE.md](wf/STRUCTURE.md)。

## 開場與入口

- 每個 session 先看 [SESSION-LOG.md](SESSION-LOG.md) 的「現役工作」段與 [WAIT_USER.md](WAIT_USER.md) 的 open 計數表；母 repo 這份 `SESSION-LOG.md` 只管母 repo 自己。Skyrim 工作線主線在 [`agentctl/`](agentctl/README.md)，每天現況見 `agentctl/handoffs/home-<日期>/STATE.md`（例如 [`2026-09-03`](agentctl/handoffs/home-2026-09-03/STATE.md)），跨場續行點見 [`agentctl/handoffs/NEXT-SESSION.md`](agentctl/handoffs/NEXT-SESSION.md)。
- **碰原始碼前**：慣例與 code map → [conventions.md](wf/workflows/common/conventions.md)、[CODE_MAP.md](wf/workflows/common/code-map/CODE_MAP.md)；環境與指令 → [dev-env.md](wf/workflows/dev-env.md)。
<!-- wf-insert:AGENTS -->
- **要你動手做事** → [WORKFLOWS.md](wf/WORKFLOWS.md) 依意圖派發，再讀該工作流入口檔。
- **想看結構** → [INDEX.md](wf/INDEX.md)；完整佈局在根 [README.md](README.md)——它是外來 agent 的入口，改佈局或新增產物類型時同步更新。
- 使用者偏好與邊界 → [user.md](wf/workflows/common/user.md)。

## 鐵律（always-on）

1. 重構／整理**不改原意**：開發＝行為不變且驗證綠燈；非開發＝原意不變。非微小工作先寫 `Done when:`。
2. **不可逆或對外的動作**（push、刪除、對外送出、動 DB、開新的大型工作）要有**授權來源**：使用者當場確認，或他親自登記的清單項目。都沒有就先問。
3. **具體流程**在各工作流入口檔，不在頂層。
4. 不 revert 使用者或其他 agent 的未確認變更；遇衝突先停下說明。
5. 需使用者親自做／驗證的記 [WAIT_USER.md](WAIT_USER.md)；跨 session 的 open 狀態記 [SESSION-LOG.md](SESSION-LOG.md)。
6. 引用外部程式碼或技術結論要附來源位置（`path:line`、函式名、URL、命令輸出摘要）；圖用 Mermaid／表格，不用需字元對齊的 ASCII 框線。
7. **條列與連結表走資料檔**：表／清單 >1 KB 存 `.json`／`.csv`（契約 `wf-table/1`，見 [data-files.md](wf/workflows/common/data-files.md)），用 `wf/tools/tabledb.py` 讀寫，不整份讀進 context；給人導航的連結表留 md。

## 專案摘要

分析對象是 C++（SKSE／CommonLibSSE-NG）、Papyrus、C#（houseCARL 走 Mutagen）；本 repo 自身以 Markdown 為主，另有 Python stdlib 驗證腳本，無建置產物。

測試：`python -m unittest discover -s tools -p "test_*.py" -v`、`python tools/check_markdown_links.py`。子 repo 測試矩陣見 [testing.md](wf/workflows/testing.md)，環境／houseCARL 建置見 [dev-env.md](wf/workflows/dev-env.md)。

<!-- wf-kernel v0.5 (2026-08-30) -->
