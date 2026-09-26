# 版控、repo 佈局與文件整理（4/4）

[lessons 索引](README.md)｜同主題：[git-and-repos](git-and-repos.md)、[git-and-repos-2](git-and-repos-2.md)、[git-and-repos-3](git-and-repos-3.md)

## kernel-tools-not-mcp-not-skill

> 資料檔 CRUD（tabledb）、條列偵測、搬檔修連結這類東西要進工作流 kernel 的 tools/，是 CLI tool 不是 skill、也不做 MCP（太重）（原 type: feedback）

2026-08-30 使用者定調：「這其實是要放進工作流 kernel 中的東西……我會期望這套 CRUD、還有條列式內容的產出，agent 會自動用 tool 來去做，而非 skill」；追問 MCP 時說「mcp 就不用了，那就太重」。

**Why:** skill（slash command）要人叫才跑；kernel 的 tool 由 AGENTS.md 鐵律與 wf-lint 的偵測驅動，agent 碰到條列資料就自然去用。MCP server 對這種幾十行的 CLI 是過度工程。

**How to apply:** 通用的文件工具一律做成 kernel `tools/*.py|sh`（隨 wf-init 複製到專案 `wf/tools/`），在 `STRUCTURE.md` 寫規則、在 `AGENTS.md` 加一條鐵律、讓 `wf-lint` 抓違規；不要做成 `.claude/commands/` skill，也不要起 MCP。專案自己的工具（如母 repo `tools/check_markdown_links.py`）留專案 `tools/`。相關：[[archive-obsolete-and-unlink]]、[[wf-kernel-upstream-and-upgrade]]

**2026-08-30 追加（`$fmt` 路徑變數）**：json 資料檔內跨層路徑用 `$fmt`＋VS Code 風格 `${var}` 變數（以 git repo 邊界定層級、不用會隨開啟目錄／檔案變的），md 連結永遠是真相對路徑。使用者提點：**變數名借鑑 VS Code、之後可能換，不要寫死在解析腳本裡**——變數表獨立成資料檔（name／how／aliases），解析器只實作少數算法，專案可用 local 檔追加。

## wf-kernel-upstream-and-upgrade

> wf/ 骨架的上游是 ~/repo/workflows（Kernel v0.4，2026-08-30）；母 repo、modpack-design、agentctl 三處導入，各自 flavor 與升級路徑；v0.3 帶 tabledb/find_big_lists/fix_moved_links 工具與 wf-table/1 契約（原 type: memory）

工作流模板上游：`~/repo/workflows`（Kernel v0.4, 2026-08-30 commit `a2a4077`；v0.3 是 `20a9818`；v0.2 是 2026-08-29；`IMPORT.md`、`CHANGELOG.md`、`tools/wf-init.sh`、`tools/wf-lint.sh`）。
2026-08-30 三處導入，都是非侵入式 `wf/`、根只有 `AGENTS.md`/`CLAUDE.md`/`.claude/commands/wf-lint.md`：

| repo | flavor | 特殊處 |
|---|---|---|
| 母 repo | dev | 升級自舊骨架（PRINCIPLES/DEV-GUIDE 那套已刪）；`SESSION-LOG.md`/`WAIT_USER.md` 留根；idea/roadmap/specs 併進 `wf/workflows/planning.md` |
| modpack-design | knowledge（刪 write、learn） | 純文件 repo，驗證只有 wf-lint |
| agentctl | 只 kernel | multi-agent 包**不裝**，三個薄入口導到既有 docs/PROTOCOL/ROSTER；`TEMPLATE.workflow.md` 兩個連結改指母 repo（升級 kernel 時要重套） |

**How to apply:** 升級時 kernel-owned（`STRUCTURE.md`、`TEMPLATE.workflow.md`、`wf-lint.sh`、`/wf-lint`）整檔覆蓋，project-owned 讀 CHANGELOG 手動套；版本戳 `grep wf-kernel AGENTS.md`。`wf-init.sh` 遇既有 `AGENTS.md` 會拒絕，升級不能直接跑它。驗收命令要加 `--include='*.md'`，否則會命中 `wf-lint.sh` 自己的 pattern 字串。相關：[[workspace-layout-and-duties]]

**v0.3（2026-08-30）**：文件整理工具進 kernel `tools/`——`tabledb.py`(+`tabledb_links.py`) 資料檔 CRUD 與 `links/check/open/resolve`、`find_big_lists.py`（>1 KB 條列、>10 連結）、`fix_moved_links.py`（跨 repo 搬檔連結重寫，含資料檔內）、wf-lint 掃 BIGLIST 與資料檔斷鏈（`--strict` 時 oversize 也算失敗）；`workflows/common/data-files.md` 是 `wf-table/1` 契約唯一出處；`workflows/tidy.md` 內建；AGENTS 鐵律「條列走資料檔、導航留 md」。升級時 kernel-owned 覆蓋清單在 CHANGELOG v0.3 節；母 repo 早先暫放在 `tools/` 的三支前身要收掉、改用 `wf/tools/`。

**v0.4（2026-08-30）**：json 內路徑變數 `$fmt`——`{"$fmt": "${gitRoot}/x.md#a"}` 物件形式、純字串永不展開；變數由 `tools/fmt-vars.json` 定義（`wf-fmt-vars/1`：name／how／aliases；專案用 `fmt-vars.local.json` 追加），解析器只實作 file-dir／git-self／git-parent／git-top／env；`tabledb.py fmt [--vars]`；`fix_moved_links` 搬檔時同代號重寫；契約在 `workflows/common/data-files-fmt.md`。母 repo／agentctl 已升到 v0.4。

**2026-09-25 tidy 輪抓到的 kernel 待修（升級 v0.5.1 時一併看上游有沒有修）**：① `wf-lint.sh`／`find_big_lists.py` 不看 `.gitignore`，掃 `analysis` 永遠多出 `tool-survey/repos/`（第三方 clone）那 34 段，驗收命令要排除路徑；② `fix_moved_links.py --apply` 對整目錄搬移會把 wf-table json 整份重排（git 認不出 rename）、把 `/home/...` 絕對路徑改成相對、拿掉目錄連結結尾的 `/`——team-hand 改用自寫 relink.py 以 HEAD 原文為底修；③ `tabledb.py <json> | tail -1` 只印 `}`，驗收要列數得自己 `python3 -c` 讀 rows。

**2026-09-25 試升 v0.5.1 失敗並撤回**：本地三處 wf/tools 已含上游 v0.5.1（c813844，2026-09-02）之後的規則（submodule 路徑跳過、skills 目錄豁免、mail inbox／superseded 視同 archive；母 repo `wf/tools/test_*` 15 項有 3 項專測這些），純覆蓋會倒退、測試紅。下次升級要對齊上游 **v0.6 或更新**（上游 CHANGELOG 已列 v0.6 與未發布項），用 diff 合併不用覆蓋；對照報告在 agentctl/handoffs/home-2026-09-25/wu/kern/REPORT.md。三處 AGENTS 版本戳實讀：母 repo與 modpack-design 是 v0.4.1、agentctl 是 v0.5（不一致，升級時一併對齊）。

**2026-09-25 23:30 已對齊上游 main `794d6d2`（v0.6＋三個未發布 lint 修正）**：三載點版本戳 `<!-- wf-kernel v0.6+794d6d2 (2026-09-25 對齊) -->`，tools 整包與上游 byte-equal，kernel-owned 文件只換 kernel 段、本地段（tidy/README「本工作區的實際跑法」等）保留，母 repo `wf/tools` 帶上游 15 項測試（全 55 項綠）。做法記在 agentctl/handoffs/home-2026-09-25/wu/kern2/。**下次升級的正確流程**：目標＝上游 main HEAD；tools 整包覆蓋；kernel-owned md 三方 diff（上游舊版／新版／本地）只換 kernel 段；project-owned 只套 CHANGELOG「既有專案要跟」那幾行；lint 只准持平或下降。
