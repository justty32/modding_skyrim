# 文件整理與 wf kernel

[lessons 索引](README.md)

## user-facing-pages-go-in-wf-user

> 2026-09-26 使用者裁示：給他看的東西（清單／審批／裁示單）放母 repo 頂層 wf/user/，不放 agentctl/handoffs 也盡量不進 agentctl（原 type: memory）

2026-09-26 使用者原話：「以後給我看的東西不要放在 handoffs 那邊，也盡量不要放在 agentctl 裏面。盡量往頂層 wf/ 那邊放」。當場建 `wf/user/`（README＋`YYYY-MM-DD-<主題>.md`），09-26 的 PRE-PLAY-CHECKLIST 搬進去，agentctl 原位留轉址。

**Why:** agentctl/handoffs 是 agent 間的內部交接與證據堆，他不想在裡面翻；頂層 wf/ 是他的入口。

**How to apply:** 濃縮給使用者的成品（開玩前清單、要他裁示的選項頁、驗收單）寫到 `wf/user/`，內文連回 agentctl 的 REPORT 當證據；agent 內部 REPORT／RT-QUEUE／COMMON 仍留 handoffs。要拍板的仍可同時做 Artifact（見 [[send-screenshots-to-session]]），但檔案本體在 wf/user/。與 [[archive-obsolete-and-unlink]] 的分層原則一致：給人導航的留 md。

2026-10-23 補：多個 artifact-update 系列報告（換臉挑選頁、隨從名冊）一致採用「產出的 HTML（數十 KB 到 2 MB）不進版控，只有產頁腳本、模板、來源 CSV/JSON 進版控」，需要重現頁面時直接重跑腳本；更新頁面優先改腳本重產生，不要手改輸出的 HTML。來源：`agentctl/handoffs/done/2026-10/home-2026-10-10/artifact-update-H1p9Y7/REPORT.md`。

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

2026-10-23 補：B 法拆檔的驗收再加兩條——子檔檔名用英文 kebab-case 語意名不用流水號、單一子檔不低於約 1.5 KB（低於就併回入口或鄰居），2026-09-25 兩次退件都是切太細。拆任何被腳本讀的索引/路由頁（如 `CODE_MAP.md`）前，先 grep 哪支工具寫死了它的路徑——`check_code_map_coverage.py` 的 `INDEX_PAGES` 不讀子檔，拆完立刻讓整批模組變 UNINDEXED，拆完必須重跑該工具比對拆前基線。來源：`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/team-docs/REPORT.md:21`、`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/team-mom/REPORT.md:41,50`。

2026-10-23 補：把檔案搬進 `archive/` 子樹會讓它相對原位置多一層路徑深度，往外的相對連結全部少算一層而斷掉——2026-08-31 封存 479 檔後全庫斷鏈 53% 是這個原因；封存後務必在母 repo 根再跑一次全庫連結檢查（submodule 自己的 lint 抓不到跨 repo 那面）。`handoffs/done/`、`archive/`、`logs/` 這類歷史紀錄檔裡的斷鏈只准降級成純文字，不准刪句改述；整句/整列刪除只適用於活文件裡「唯一目的就是連到已封存檔」的導覽列。來源：`agentctl/handoffs/done/2026-08-31/condense-2026-08-31/team-a/gotchas-snippets.md:34-56`。

2026-10-23 補：全庫政策文字掃描/修正要把命中分三類：LIVE（現行文件，要改）、SENT（已送出的 orders/交接書，改了也追不回，留著當證據）、ARCHIVE（歷史紀錄，刻意保留舊規則文字）——只改 LIVE 且與新規則牴觸的。來源：`agentctl/handoffs/done/2026-08-30/scrn-2026-08-30/SWEEP-cx-scrn1.md:118-145`。

2026-10-23 補：自動推論欄位遇到可疑命中（如撞名）要加 `SUSPECT(...)：` 前綴留在表裡，不要為了數字好看靜默清掉或填掉。抽表時每列保留一個「原文」欄存完整原始 markdown，逐行比對快照才能證明沒丟東西；open 項目數量遠超活層 byte 預算時，改成「群組＋筆數＋卡在哪」的 ledger，但群組筆數加總必須精確等於原始總數（差額 0），逐項明細另存成可回溯的 tsv。來源：`agentctl/handoffs/done/2026-09-02/vfo-2026-09-02/REPORT.md:33-44`、`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/team-docs/REPORT.md:4`、`agentctl/handoffs/done/2026-08-31/condense-2026-08-31/team-a/REPORT.md:38-49`。

2026-10-23 補：別人會往檔尾追加的活檔（如 ROSTER.md），抽歷史時把「已收線」節搬到「現役」節前面，現役節留在檔尾，照舊習慣追加的人才會落對位置，別改規則要求別人改習慣。信箱積壓時照這順序整併：new/read 併日 → `done/<日>/` 整成「正文在 messages.json、.md 只留索引」→ teams close → mail/orders 搬 trash，每步驗收都是「逐行比對缺 0 行」。任何手寫維護的索引/計數表（WAIT_USER 計數、`logs/README.md` 這類）沒有機械檢查大約一個月內必失效，要嘛納入 wf-lint 掃描（目錄項⊆索引項），要嘛改成生成式索引或乾脆不做索引、靠檔名/日期導航。來源：`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/team-inbox/REPORT.md:5-14`、`agentctl/handoffs/done/2026-09/home-2026-09-03/hub/REPORT.md:55`、`logs/README.md:5`。

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


## doc-restructure-safety-checklist

> 拆檔／封存前要先做幾個機械檢查，否則斷的連結不會被 lint 抓到。

2026-08-29～09-25 歸納連結檢查器看不到的陷阱：①拆檔前 `grep -rn "<檔名>#"` 找錨點連入者，標題原文留入口檔；②可達性掃描把「走不到連結」當封存候選，但至少六類不該封存：非 `.md` 引用、上游 fork 文件、自成體系知識樹、行號引用、跨 repo anchor、目錄登記但個別檔未列；③`file:line` 行號引用，reflow 會讓行號指錯而 gate 全綠，檔尾純追加是例外。

**Why:** 連結檢查器只看 md 連結，看不到行號引用與非 md 程式引用這類陷阱。

**How to apply:** 拆/封存/去重前固定跑這幾項檢查。來源：`agentctl/handoffs/done/2026-08-29/doc-refactor/REACHABILITY.md:59-139`。相關 [[archive-obsolete-and-unlink]]。

2026-10-23 補：另兩個同類陷阱——跨 repo markdown anchor 連結會被 lint 驗，但紅燈出現在引用端 repo，弄壞它的是被引用端改了標題文字，兩邊常非同一人在管，改標題等於改了別人的 API；兩份文件內容完全相同不能只用 `cmp` 判斷重複，可能其中一份其實是 mode `120000` 的跨 repo symlink，把它當重複副本改寫會把內容寫穿到正典檔案。改任何現役文件標題前先 `git grep -n '#<標題 slug>'`；疑似重複文件先 `git ls-files -s` 看 mode。來源：`agentctl/handoffs/done/2026-08-29/doc-refactor/REACHABILITY.md:117-133`、`agentctl/handoffs/done/2026-08-29/doc-refactor/LINEREF-FREEZE.md:89-93`。


## corpus-reliability-flagging

> agent 產出的參考語料（網頁快照、調查文件）要逐段標可信度，不能整份當原文或整份當定論。

2026-09-02 抓 LoreRim wiki 28 頁，10 頁因版權限制拒絕逐字重現、落檔是結構化事實抽取（專名/數字保留，敘事措辭已改寫），另 3 頁由 JS 產生根本抓不到，均標 PARTIAL。`analysis/mod-survey/index.md:19` 同樣警告：survey agent 對「mod 怎麼運作」可信，但對「ModForge 缺什麼」是未查原始碼的推斷。

**Why:** 「可逐字引用的事實」與「agent 的推斷」不分開標記，後續線會把推斷當定論用。

**How to apply:** 網頁快照逐檔標 PARTIAL/FULL；依調查文件的「缺口」結論做決策前先對原始碼校正。來源：`agentctl/handoffs/done/2026-09-02/lorerim-2026-09-02/team-web/REPORT.md:25-27,50-51`。


## home-dir-cleanup-safety

> 家目錄級刪除不可逆（ext4 無快照、quarantine.py 已不能用）；盤點時算的雜湊在執行瞬間要重驗，不能用舊快照直接刪。

2026-10-17 沿用既有判準（已解壓且已裝進 MO2 的 `_staging` 可刪；`_dl-*`、含 backup/rollback 字樣的留）：逐路徑 dry-run（不用萬用字元）、刪前查 MO2／housecarl-mirror 有無 symlink 指向、大型輸出要逐檔 byte 比對 MO2 內副本才判定可刪。2026-08-06 曾因誤刪永久丟失 107 檔。

**Why:** 磁碟級刪除沒有救援路徑；舊雜湊/舊快照在執行當下可能已經不準。

**How to apply:** dry-run 清單＋閘門檢查寫進執行腳本本身、逐路徑不用萬用字元，使用者面板確認後才真刪。來源：`agentctl/handoffs/home-skyrim-cleanup-2026-10-17/REPORT.md`。
