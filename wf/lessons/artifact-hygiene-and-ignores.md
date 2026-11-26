# 產物衛生、.gitignore 與刪除前的掃描

[lessons 索引](README.md)｜入站連結掃描與家目錄級刪除見 [deletion-safety](deletion-safety.md)

## handoffs-junk-not-tracked-periodic-hygiene

> agentctl/handoffs 不該進 git 的中間產物要擋：版控政策＋hygiene_check＋pre-commit hook＋收線必跑

2026-09-25 使用者原話：「agentctl 感覺有可以優化的地方，比如 handoff 那邊，堆積了一大堆垃圾，很多時候這些都是不該進 git tracked 的」「然後也沒有定期清理」。

**Why**：線交付時把中間產物（掃描 csv、ledger json、存檔、截圖、dll）留在 handoff 目錄再整目錄 `git add`；只擋目錄名的 .gitignore 擋不住副檔名與大小。

**How to apply**：
- 准／不准的清單在 `agentctl/handoffs/README.md`「什麼能進版控」與 `agentctl/.gitignore`；場次夾的保留期與刪除四步在同檔「保留期」（刪除要使用者在對話裡當場說）。
- 工具：`agentctl/tools/hygiene_check.py`（`tracked`／`staged`／`disk`）＋ `agentctl/tools/hooks/pre-commit`（`git config core.hooksPath tools/hooks`）。收線必跑 `hygiene_check.py tracked` → 0；交接書寫「>1 MB 產物放 work/（gitignored）」；已追蹤的違規檔用 `git rm --cached`（留磁碟），刪實體與改歷史都要先問使用者。

共用分析工具若從未進版控（`git status` 顯示 `??`），「sha256 跑前跑後一致」不能當「工具沒被動過」的憑證；多線用同一支共用腳本驗收前，先把腳本收進版控（2026-10-23，`agentctl/handoffs/done/2026-10/home-2026-10-09/vf-text3/DONE-merge.md`）。

政策文件允許的例外沒實作進 `hygiene_check.py` 會誤擋合規 commit（例：`work/backup/**` 純文字備份要留版控）；改政策文件時同步檢查工具，誤擋就補規則＋正負向測試（2026-10-23，`agentctl/handoffs/done/2026-10/home-2026-10-10/git-tidy/REPORT/git-cleanup.md`）。

相關：[[commit-explicit-paths-only]]、[[dont-clutter-home-with-agent-output]]、[[archive-obsolete-and-unlink]]

## ignored-is-not-a-deletion-policy

> 「被 git ignore」不能直接當刪除理由——先 `git check-ignore -v` 查規則來源：來自版控內 `.gitignore` 的才是政策，來自 `info/exclude`／global 的只是個人本機設定。

**關於「這個檔重不重要」，git 的沉默從來不是答案**——`ignored` 不等於可刪、`info/exclude` 不等於政策、「未進版控」更不等於不重要：未進版控且全機無第二份＝刪了就沒了（2026-10-23 兩份 HANDOFF.md 因 `.git/modules/agentctl/info/exclude` 的本機規則被當「政策判定可丟」而永久遺失，該規則還與「`*.md` 一律進版控」衝突）。

**How to apply**：以 ignore 狀態生成刪除候選時，逐項（或逐規則）跑 `git check-ignore -v` 分流：`gitignore:policy`（來源是版控內 `.gitignore`）可列候選；`gitignore:local`（`info/exclude`、`core.excludesFile` global）**預設不列**，改列「ignore 規則與版控政策衝突」待人裁。未進版控＋全機無第二份另列 `IRRECOVERABLE`，預設排除。`info/exclude` 裡與政策衝突的規則本身就該清。工具：`agentctl/handoffs/home-2026-10-23/tidy/T1/tools/build_candidates.py`。

自製隔離／待刪機制也一樣：清空前一律走它自己的 restore／release 指令（如 `quarantine.py restore`），不要把「反正是暫存／隔離區」當成可以直接 rm 的理由（2026-08-06 `~/skyrim_mods/.quarantine/2026-08-06/` 被直接 `rm`；`mod-library/audits/2026-08-06-deletion-incident.md`）。

## gitignore-exclusion-and-negation-pitfalls

> .gitignore 的目錄級排除會擋住內層的 `!` 白名單，改規則本身還可能讓現役線的證據被悄悄忽略。

- 排除整個目錄（`teams/`）後 Git 不會再進去套用 `!teams/*/members`；要排除到檔案層級（`teams/*/*`）再對特定檔名取反，寫完用 `git check-ignore -v` 雙向驗證（`agentctl/handoffs/done/2026-08-30/inbox-layering/HANDOFF.md:111-114`）。
- 父目錄已被排除時否定條目一樣不生效；要讓 `handoffs/**/work/backup/` 例外，`!handoffs/**/work/backup/` 與 `!handoffs/**/work/backup/**` 兩條都要寫（`agentctl/handoffs/done/2026-09/home-2026-09-18/hygiene/REPORT.md:56`）。
- 新增忽略規則（如 before/、after/、*.log、*.png）後，還在跑的線 `git add` 同類證據會被靜默略過，git 只提示要 `-f`（2026-09-25，`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/team-hand/REPORT.md:45`）。改 `.gitignore` 後通知現役線，收線前 `git status --ignored` 抽查有沒有該進版控卻被忽略的產物。

相關：[[handoffs-junk-not-tracked-periodic-hygiene]]

## list-scripts-before-deleting-staging

> 刪暫存／staging 夾前要先列出夾內的腳本與工具，逐類核對「已進版控」——紀錄、產物、腳本是三件事，不能整夾一句「內容已入版控」帶過。

2026-11-21：使用者當場授權刪 `~/skyrim_mods/_staging-2026-11-18-bodyslide-{trial,retro,close}/`，頂層刪前只說是「試刷產物」、收包 REPORT 也寫「本包已入版控，只剩證據價值」；夾裡實際用來保證隔離的 bwrap runner 與驗 NIF／TRI 的解析器都沒進版控，一併丟失，只好重做成 `tools/bodyslide_*.py`（[審查 F2／F3](../../agentctl/handoffs/home-2026-11-21/bodyslide-review/REPORT.md)）。

**Why:** 「已入版控」通常只核了文件與證據；腳本藏在 `run/`、`tools/`、`probe/` 子目錄裡，名字也不像要留的東西。使用者授權的是他聽到的描述，描述漏了腳本，授權就不涵蓋腳本。

**How to apply:** 刪前跑一次 `find <夾> -type f \( -name '*.py' -o -name '*.sh' -o -name '*.ps1' \)` 列出所有腳本，每支標「已有版控對應（路徑）」或「之後還要用、先收進 `tools/`」或「一次性、可丟」，連同大小一起放進給使用者的刪除說明。紀錄、產物、腳本分三行報，不合併成一句。相關：[[temp-dirs-double-as-offline-reinstall-library]]、[[scan-inbound-links-before-delete]]。

## rebuild-config-must-not-point-at-staging

> 會重複用的流程（重建設定、測試）不可讀 staging 或 `wf/temp` 的東西：暫存一清，流程就斷或只能留垃圾

2026-11-22 清暫存時發現 `agentctl/tools/bodyslide/*.json` 的 `staging_root`、`extra_sources`、`obody.presets_dirs` 指向 `_staging-2026-11-22-*`，測試讀 staging 匯出物與 `wf/temp` 裡的 `chargen.psc`（[cleanup-temp REPORT](../../agentctl/handoffs/home-2026-11-22/cleanup-temp/REPORT.md)「KEEP」）。現行固定位置：重建根 `~/skyrim_mods/bodyslide-sources/<female|male|body-fit>/`、測資 `~/skyrim_mods/test-samples/`、`chargen.psc` 從已安裝 RaceMenu 的 BSA 讀（[final-wrap REPORT](../../agentctl/handoffs/home-2026-11-22/final-wrap/REPORT.md)）。

**Why:** staging 的名字就說它是暫存，下一個清理者會照名字判斷；被長期流程引用的東西放在那裡，清理就只能二選一：斷流程或留垃圾。

**How to apply:**
- 線產出「之後還要重跑」的設定時，路徑指向固定位置（非 `_staging-<日期>`、非 `wf/temp`）；REPORT 寫明哪些路徑是長期依賴。
- 測試要的真樣本放固定樣本區並可用環境變數覆寫；第三方檔（mod 內附的 psc 等）不進版控，測試從已安裝的 mod 讀，找不到才 skip，skip 訊息寫清楚找過哪裡、怎麼指定。
- 清 staging 前先 `grep -rn "_staging-<日期>"` 掃 `agentctl/tools`、`tools`、`wf/workflows`，有引用就先搬再改設定、跑 `plan --dry-run` 與測試，最後才刪。相關：[[list-scripts-before-deleting-staging]]。
