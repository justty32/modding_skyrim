# 文件整理與 wf kernel

[lessons 索引](README.md)

## user-facing-pages-go-in-wf-user

> 2026-09-26 使用者裁示：給他看的東西（清單／審批／裁示單）放母 repo 頂層 wf/user/，不放 agentctl/handoffs 也盡量不進 agentctl（原 type: memory）

2026-09-26 使用者原話：「以後給我看的東西不要放在 handoffs 那邊，也盡量不要放在 agentctl 裏面。盡量往頂層 wf/ 那邊放」。當場建 `wf/user/`（README＋`YYYY-MM-DD-<主題>.md`），09-26 的 PRE-PLAY-CHECKLIST 搬進去，agentctl 原位留轉址。

**Why:** agentctl/handoffs 是 agent 間的內部交接與證據堆，他不想在裡面翻；頂層 wf/ 是他的入口。

**How to apply:** 濃縮給使用者的成品（開玩前清單、要他裁示的選項頁、驗收單）寫到 `wf/user/`，內文連回 agentctl 的 REPORT 當證據；agent 內部 REPORT／RT-QUEUE／COMMON 仍留 handoffs。要拍板的仍可同時做 Artifact（見 [[send-screenshots-to-session]]），但檔案本體在 wf/user/。與 [[archive-obsolete-and-unlink]] 的分層原則一致：給人導航的留 md。

## archive-obsolete-and-unlink

> 整理文件的五條原則：過時的封存並清連結；資料夾別擠太多檔（同類可放鬆）；太多 <1KB 小檔就合併；>8KB 就拆，大型同質列表抽成 .json/.csv，tabledb 工具統一 CRUD；連結表>10 條才考慮、給人導航的留 md（原 type: memory）

2026-08-30 使用者定調的整理原則（五條）：

<!-- wf-nav -->
1. **過時的舊東西就封存，把指向它的連結清乾淨，當做它不存在。** 不是把連結改指到 `archive/` 路徑，而是從活文件把那條連結拿掉（留純文字或整句刪）；只有 `archive/README.md` 的索引表可以指向它。
2. **一個資料夾下不要擠太多檔案**；但若是**同類檔案**（同一種 log、同一種報告、同一系列 intake gates）這個限制可以放鬆，不必為了數字硬拆。
3. **一個資料夾下太多小檔案（<1 KB）就適當合併**成一份（例如同一天的 inbox 訊息併成一個檔、零碎的 evidence 併成一張表），內容保留、原檔消失。
4. **檔案 >8 KB 就拆**（不只 workflows/，所有活文件）。其中**條列式、每條同質性很高的大列表**（ledger、對照矩陣、候選表）不要再拆成好幾份 markdown——**抽成 `.json`／`.csv` 資料檔**，統一用母 repo 的 tabledb 工具做 CRUD（原本說 python/lua 腳本，同日改口：資料歸資料檔、程式只有一份通用 lib）；markdown 只留摘要與怎麼查。

**Why:** 舊文件留連結會讓後續的線把它當現役材料讀進去（modpack-design 鐵律「archive/ 不讀」就是為此）；硬按檔數拆同類檔只會多一層無意義的目錄；幾十個幾百 byte 的小檔每個都要開一次才知道內容，合併後一眼掃完；幾百列的表塞在 markdown 裡 agent 每次都得整份讀進 context，變成資料檔後只取要的那幾筆。

5. **連結表看對象**：md 裡的連結是給人點的捷徑，別為了 AI 把它拿掉。條列式連結**超過十條**才「開始考慮」轉 `.csv`／`.json`，且先判斷用途——**給人導航的**（README 路由表、目錄、派發表）留 md，走一般 8 KB 上限、超了就分層（上層只列子層入口）；**給 AI 讀的**（候選表、ledger、證據表裡的連結欄）才抽資料檔，因為連結數量會拖累 AI 判斷。

**How to apply:** 派整理線時把這五條寫進交接書；「過時」的判準是文件自述歷史／被取代／前提作廢，或它的目標 profile／批次已不存在。相關：[[wf-kernel-upstream-and-upgrade]]、[[investigate-all-then-install-once]]

**2026-08-30 晚補（第 4 條）**：抽表後的 md **不寫查詢指令、不寫工具路徑**（「怎麼查：」後面再貼三行 tabledb 查詢指令是雜訊）。理由：agent 端 kernel 已內化 `tabledb.py`，不必每檔再教；使用者端只要「看 wf 的資料檔說明」一句，不指定路徑。md 只留目的、`已抽到 [x.json](x.json)（N 列）`、欄位說明、統計。規則進 kernel v0.4.1（data-files.md＋wf-lint `QUERYCMD` 殘留檢查）。

**2026-08-30 放寬——過時或已解決的可以直接刪**：使用者原話「不用這麼嚴格，反正就是整理，
**過時或已經解決的可以清掉**」。所以工作流禁區裡那條「不刪」不是硬規則：

- **明確過時／已解決 → 直接 `git rm`**（git history 保得住，可回復，所以這不是不可逆動作）。
- **還有參考價值但非現役 → 才走 `git mv` 進 `archive/`**。
- 判準：**「這份東西以後還會有人想翻出來看嗎」**。

**我在同一輪犯的錯**：我把「指向被封存檔的連結」寫成用 `fix_moved_links.py` 改指到 `archive/`，
**跟 tidy 工作流第 1 條原則正好相反**——正確做法是**把那條連結拿掉**（改純文字或整句刪），
只有 `archive/README.md` 的索引可以連過去。`fix_moved_links.py` 只用於「搬位置但仍現役」的檔。
**教訓：派整理線之前先讀該 repo 的 `wf/workflows/tidy.md`，不要憑印象寫交接書。**

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
