# wf 骨架（kernel）與工具形態

[lessons 索引](README.md)

## kernel-tools-not-mcp-not-skill

> 資料檔 CRUD（tabledb）、條列偵測、搬檔修連結這類東西要進工作流 kernel 的 tools/，是 CLI tool 不是 skill、也不做 MCP（太重）

2026-08-30 使用者定調：「這其實是要放進工作流 kernel 中的東西……我會期望這套 CRUD、還有條列式內容的產出，agent 會自動用 tool 來去做，而非 skill」；追問 MCP 時說「mcp 就不用了，那就太重」。

**Why:** skill（slash command）要人叫才跑；kernel 的 tool 由 AGENTS.md 鐵律與 wf-lint 的偵測驅動，agent 碰到條列資料就自然去用。MCP server 對這種幾十行的 CLI 是過度工程。

**How to apply:** 通用的文件工具一律做成 kernel `tools/*.py|sh`（隨 wf-init 複製到專案 `wf/tools/`），在 `STRUCTURE.md` 寫規則、在 `AGENTS.md` 加一條鐵律、讓 `wf-lint` 抓違規；不要做成 `.claude/commands/` skill，也不要起 MCP。專案自己的工具（如母 repo `tools/check_markdown_links.py`）留專案 `tools/`。相關：[[archive-obsolete-and-unlink]]、[[wf-kernel-upstream-and-upgrade]]

**`$fmt` 路徑變數（2026-08-30）**：json 資料檔內跨層路徑用 `$fmt`＋VS Code 風格 `${var}` 變數（以 git repo 邊界定層級、不用會隨開啟目錄／檔案變的），md 連結永遠是真相對路徑。使用者提點：**變數名借鑑 VS Code、之後可能換，不要寫死在解析腳本裡**——變數表獨立成資料檔（name／how／aliases），解析器只實作少數算法，專案可用 local 檔追加。契約在 `wf/workflows/common/data-files-fmt.md`。

## wf-kernel-upstream-and-upgrade

> wf/ 骨架的上游是 ~/repo/workflows；各 repo 以非侵入式 `wf/` 導入，現行版本看各 AGENTS.md 的 wf-kernel 版本戳；升級＝tools 整包覆蓋＋kernel 段三方 diff

工作流模板上游：`~/repo/workflows`（`IMPORT.md`、`CHANGELOG.md`、`tools/wf-init.sh`、`tools/wf-lint.sh`）。導入都是非侵入式 `wf/`、根只有 `AGENTS.md`／`CLAUDE.md`／`.claude/commands/wf-lint.md`：

| repo | flavor | 特殊處 |
|---|---|---|
| 母 repo | dev | `SESSION-LOG.md`/`WAIT_USER.md` 留根；idea/roadmap/specs 在 `wf/workflows/planning.md` |
| modpack-design | knowledge（刪 write、learn） | 純文件 repo，驗證只有 wf-lint |
| agentctl | 只 kernel | multi-agent 包**不裝**，三個薄入口導到既有 docs/PROTOCOL/ROSTER；`TEMPLATE.workflow.md` 兩個連結改指母 repo（升級 kernel 時要重套） |

mod-library、instance 也有版本戳（2026-10-26 導入）。

**版本**：現行版本查 `grep wf-kernel AGENTS.md`（各載點同查），不要把 hash 抄進別的文件。上游 hash 都可從 `~/repo/workflows` 的 `origin/main` 走到，別機可直接當基準；別主動去推上游。tidy 是資料夾（含 `wf/workflows/tidy/content-trim.md`），modpack-design、agentctl 的原 `tidy.md` 留當入口；wf-lint 是可選（母 repo `testing.md`、CI `docs.yml` 不必跑）。做法見 agentctl/handoffs/home-2026-10-26/wfup/REPORT.md、agentctl/handoffs/home-2026-10-26/wfup2/REPORT.md、agentctl/handoffs/home-2026-09-25/wu/kern2/、agentctl/handoffs/home-2026-10-23/improve/kernel-localhook/。

**kernel 工具**：`tabledb.py`（＋`tabledb_links.py`）、`find_big_lists.py`、`fix_moved_links.py`、wf-lint 的 BIGLIST／資料檔斷鏈；契約唯一出處是 `wf/workflows/common/data-files.md`（`wf-table/1`）與 `data-files-fmt.md`（`$fmt`、`tools/fmt-vars.json`、專案用 `fmt-vars.local.json` 追加）。

**本地覆寫與同步排除**：STRUCTURE「archive 規則」kernel 段照舊，過時即刪的覆寫寫在其後的 `<!-- local -->` 段（各載點同文），保留期檢查 `wf/tools/wf-lint-retention.sh` 由各 `wf-lint-local.sh` 呼叫；升級時 kernel 段照抄、local 段與這兩支 project-owned 檔保留。agentctl 與 modpack-design 的 `wf/tools/` 不放 kernel 的 `test_*`（2026-11-05 使用者裁示；母 repo 保留，agentctl 刪於 `5c3d6d88`）。同步沒有腳本（手動「tools 整包覆蓋」），覆蓋這兩處時**只複製非 `test_*` 檔**（例：`rsync -a --exclude='test_*' <來源>/tools/ <repo>/wf/tools/`），覆蓋完 `git status` 不得出現 `test_*.py` 新增；mod-library 與子 repo 若另有刪除照同樣處理。

**local hook 契約**：wf-lint 掃某 dir 時若存在 `<dir>/wf/tools/wf-lint-local.sh` 就以 `bash <它> <dir> <strict>` 執行，finding 平時 warning、`--strict` 才算失敗；`*-local.sh` 是 project-owned，升級整包覆蓋時**不得刪除載點多出的 project-owned 檔**。

**How to apply（升級流程）:** 目標＝上游 main HEAD；tools 整包覆蓋；kernel-owned md（`STRUCTURE.md`、`TEMPLATE.workflow.md` 等）三方 diff（上游舊版／新版／本地）只換 kernel 段、本地段（如 tidy/README「本工作區的實際跑法」）保留；project-owned 只套 CHANGELOG「既有專案要跟」那幾行；lint 只准持平或下降。本地 wf/tools 可能已含上游某版之後的規則，要對齊上游 HEAD、用 diff 合併，不盲目覆蓋舊版（agentctl/handoffs/home-2026-09-25/wu/kern/REPORT.md）。`wf-init.sh` 遇既有 `AGENTS.md` 會拒絕，升級不能直接跑它。驗收命令要加 `--include='*.md'`，否則會命中 `wf-lint.sh` 自己的 pattern 字串。相關：[[workspace-layout-and-duties]]、[[dont-hardcode-mutable-snapshot-values]]

**kernel 工具的操作陷阱**：
- `fix_moved_links.py --apply` 對整目錄搬移會把 wf-table json 整份重排（git 認不出 rename）、把 `/home/...` 絕對路徑改成相對、拿掉目錄連結結尾的 `/`；對含絕對路徑或 json/csv 的被搬檔也有 bug（2026-10-17）。先 `--dry-run` 看 diff，出現非預期的重排就改用以 HEAD 原文為底的自寫 relink 包裝，不要 `--apply`。
- tabledb 工具「檔名＋`| tail -1`」只印 `}`，驗收要列數得自己用 Python 讀 rows；`update` 改一兩欄也會整份重新排版（一次 374 行 diff），只改一兩欄時用最小字串替換。
- `wf-table/1` 的 `_path`／`_link` 字尾會被當連結欄，命中非連結欄位（如 `archive_path`、`lib_path`）製造大量假 BROKEN——新 schema 欄名改用 `_file`／`_rel`；wf-lint 也會把 JSON 資料欄裡像路徑的字串值（如 `output_path`）誤判成文件連結。
- 驗收數字忽小於直覺時先懷疑截斷（shell exit status 只有 0–255），直接 `grep -c` 驗證。

**操作紀律**：陌生機器第一次跑 wf-lint 前先 `python3 -c "print(1)"` 確認是真直譯器（公司機可能是 Microsoft Store 佔位符）；`check_markdown_links.py` 只掃 tracked 檔，批次歸檔／commit 後要再跑一次，不能只信 untracked 階段的綠燈。`KNOWN-ISSUES.md` 記的已知問題要追到真的進程式碼；在 handoffs 工作目錄修好的共用工具，收線時確認已回寫到正典路徑。lint 歸零不是目的：只能靠改資料才能變綠時，加排除規則並在 REPORT 說明，不動資料（尤其是備份副本，價值就在於和原檔逐字相同）。`wf-lint.sh --strict` 要明確列出 tracked 目錄（不傳「.」），且在主工作樹跑，不在隔離 worktree 跑，否則跨 repo 相對連結會假報。

來源：`agentctl/handoffs/done/2026-09/home-2026-09-02/go19/REPORT.md:17`、`agentctl/handoffs/done/2026-09/home-2026-09-02/wrap2/REPORT.md:24`、`agentctl/handoffs/home-2026-10-17/patrol/p1-agentctl/REPORT.md`、`agentctl/handoffs/home-2026-10-17/structure-review/REPORT.md`、`agentctl/handoffs/home-2026-10-17/improve/REPORT.md`、`agentctl/handoffs/done/2026-08-27/opus-modforge/RESULTS.md:32`、`agentctl/handoffs/done/2026-08-30/kern-2026-08-30/REPORT.md:5`、`agentctl/handoffs/done/2026-08-30/ops-2026-08-30/broken-links-triage.md:5-16`、`agentctl/handoffs/done/2026-09-02/spike-2026-09-02/REPORT.md:100-102`、`agentctl/handoffs/done/2026-08-01/cx-links/HANDOFF.md:40-55`、`agentctl/handoffs/done/2026-09/home-2026-09-03/wrap/REPORT.md:153`、`agentctl/handoffs/done/2026-09/home-2026-09-05/dl2/STATE.md:22`。
