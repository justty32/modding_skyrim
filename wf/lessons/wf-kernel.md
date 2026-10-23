# wf 骨架（kernel）與工具形態

[lessons 索引](README.md)

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

**2026-09-25 tidy 輪抓到的 kernel 待修（升級 v0.5.1 時一併看上游有沒有修）**：① `wf-lint.sh`／`find_big_lists.py` 不看 `.gitignore`，掃 `analysis` 永遠多出 `tool-survey/repos/`（第三方 clone）那 34 段，驗收命令要排除路徑；② `fix_moved_links.py --apply` 對整目錄搬移會把 wf-table json 整份重排（git 認不出 rename）、把 `/home/...` 絕對路徑改成相對、拿掉目錄連結結尾的 `/`——team-hand 改用自寫 relink.py 以 HEAD 原文為底修；③ tabledb 工具「檔名＋`| tail -1`」只印 `}`，驗收要列數得自己用 Python 讀 rows。

**2026-09-25 試升 v0.5.1 失敗並撤回**：本地三處 wf/tools 已含上游 v0.5.1（c813844，2026-09-02）之後的規則（submodule 路徑跳過、skills 目錄豁免、mail inbox／superseded 視同 archive；母 repo `wf/tools/test_*` 15 項有 3 項專測這些），純覆蓋會倒退、測試紅。下次升級要對齊上游 **v0.6 或更新**（上游 CHANGELOG 已列 v0.6 與未發布項），用 diff 合併不用覆蓋；對照報告在 agentctl/handoffs/home-2026-09-25/wu/kern/REPORT.md。三處 AGENTS 版本戳實讀：母 repo與 modpack-design 是 v0.4.1、agentctl 是 v0.5（不一致，升級時一併對齊）。

**2026-09-25 23:30 已對齊上游 main `794d6d2`（v0.6＋三個未發布 lint 修正）**：三載點版本戳 `<!-- wf-kernel v0.6+794d6d2 (2026-09-25 對齊) -->`，tools 整包與上游 byte-equal，kernel-owned 文件只換 kernel 段、本地段（tidy/README「本工作區的實際跑法」等）保留，母 repo `wf/tools` 帶上游 15 項測試（全 55 項綠）。做法記在 agentctl/handoffs/home-2026-09-25/wu/kern2/。

**2026-10-23 已對齊上游 `682c778`（v0.6＋gitignored 跳過修正 32e5e55＋wf-lint project-local hook 機制）**：三載點版本戳 `<!-- wf-kernel v0.6+682c778 (2026-10-23 對齊) -->`。local hook 契約：wf-lint 掃某 dir 時若存在 `<dir>/wf/tools/wf-lint-local.sh` 就以 `bash <它> <dir> <strict>` 執行，finding 平時 warning、`--strict` 才算失敗；`*-local.sh` 是 project-owned，升級整包覆蓋時**不得刪除載點多出的 project-owned 檔**。**上游 `682c778` 經使用者 2026-10-23 裁示僅存本機、不推遠端（終局決定，不是暫緩，不要去推）。** 後果：三載點版本戳 `v0.6+682c778` 在任何其他機器上都無法解析；從別機對齊 kernel 時不能用這個 hash 當基準，要改用最後一個有推上去的上游 commit（`32e5e55`）加上本機差異來比對。這是既定狀態，不是待辦。做法記在 agentctl/handoffs/home-2026-10-23/improve/kernel-localhook/。**下次升級的正確流程**：目標＝上游 main HEAD；tools 整包覆蓋；kernel-owned md 三方 diff（上游舊版／新版／本地）只換 kernel 段；project-owned 只套 CHANGELOG「既有專案要跟」那幾行；lint 只准持平或下降。

**2026-10-23 tidy 輪再追加的 kernel 待修／操作陷阱**：④ `wf-table/1` 的 `_path`／`_link` 保留字命中非連結欄位（如 `archive_path`、`lib_path`）會製造大量假陽性 BROKEN（一次 189 筆、一次 460 筆）——新建 schema 欄名避開這兩個字尾，改用 `_file`／`_rel`；wf-lint 也會把 JSON 資料欄裡長得像路徑的字串值（如 `output_path`）誤判成文件連結。⑤ tabledb 的 `update` 子指令改一兩個欄位也會把整份 json 重新排版縮排（一次產生 374 行 diff），只改一兩欄時改用最小字串替換。⑥ `tools/check_markdown_links.py` 的 `github_heading_slug()` 把連續空白壓成單一連字號、沒過濾非 ASCII 符號（→、✅），會把正確連結誤報斷掉，已驗證的修法在 `opus-modforge/check_markdown_links-slug-fix.patch`；該腳本也不接受目錄參數，子 repo 要先 `git -C <repo> ls-files -z '*.md'` 展開成檔案清單（zsh 下包 `bash -c`）。⑦ `wf-lint.sh` 的 `check_links()` 拿未解碼連結字串測存在性，含空白/括號的百分號編碼連結會被誤報；修好前「wf-lint 乾淨」不可達成，基線判準改成「broken 數與動工前相同且已證明誤報」。⑧ `check_links()` 曾用 shell exit status（僅 0–255）回傳 BROKEN 筆數，超過 255 會截斷（3,589 筆顯示成 517），已改用內部變數傳遞，驗收數字忽小於直覺時先懷疑截斷、直接 `grep -c` 驗證。⑨ `fix_moved_links.py` 對含絕對路徑或 json/csv 的被搬檔仍有 bug（10-17 施工線仍要用包裝腳本繞過，工具本體未修）；呼叫前先 `--dry-run` 看 diff，出現非預期的格式重排就改手寫包裝，不要 `--apply`。另外兩條操作紀律：公司機的 `python3` 可能是 Microsoft Store 佔位符，陌生機器第一次跑 wf-lint 前先 `python3 -c "print(1)"` 確認是真直譯器；`check_markdown_links.py` 只掃 tracked 檔，批次歸檔/commit 完成後要再跑一次，不能只信 commit 前 untracked 階段的綠燈。`KNOWN-ISSUES.md` 記錄的已知問題要追蹤到真的進程式碼，不是寫了就算修好，任何在 handoffs 工作目錄修好的共用工具，收線時要確認已回寫到各線預設引用的正典路徑。lint 歸零不是目的：遇到「只能靠改資料才能變綠」時正確動作是加排除規則並在 REPORT 說明，不是動資料（尤其是備份副本，價值就在於和原檔逐字相同）。`wf-lint.sh --strict` 要明確列出 tracked 目錄清單（不要傳「.」），且一定要在主工作樹跑，不要在隔離 worktree 裡跑，否則跨 repo 相對連結會假報幾十條。來源：`agentctl/handoffs/done/2026-09/home-2026-09-02/go19/REPORT.md:17`、`agentctl/handoffs/done/2026-09/home-2026-09-02/wrap2/REPORT.md:24`、`agentctl/handoffs/home-2026-10-17/patrol/p1-agentctl/REPORT.md`、`agentctl/handoffs/home-2026-10-17/structure-review/REPORT.md`、`agentctl/handoffs/home-2026-10-17/improve/REPORT.md`、`agentctl/handoffs/done/2026-08-27/opus-modforge/RESULTS.md:32`、`agentctl/handoffs/done/2026-08-30/kern-2026-08-30/REPORT.md:5`、`agentctl/handoffs/done/2026-08-30/ops-2026-08-30/broken-links-triage.md:5-16`、`agentctl/handoffs/done/2026-09-02/spike-2026-09-02/REPORT.md:100-102`、`agentctl/handoffs/done/2026-08-01/cx-links/HANDOFF.md:40-55`、`agentctl/handoffs/done/2026-09/home-2026-09-03/wrap/REPORT.md:153`、`agentctl/handoffs/done/2026-09/home-2026-09-05/dl2/STATE.md:22`。
