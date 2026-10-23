# 產物衛生、.gitignore 與刪除前的掃描

[lessons 索引](README.md)

## handoffs-junk-not-tracked-periodic-hygiene

> 2026-09-25 使用者指出 agentctl/handoffs 堆了一大堆不該進 git 的東西、也沒有定期清理；版控政策＋hygiene_check＋pre-commit hook＋收線必跑（原 type: memory）

2026-09-25 使用者原話：「agentctl 感覺有可以優化的地方，比如 handoff 那邊，堆積了一大堆垃圾，很多時候這些都是不該進 git tracked 的」「然後也沒有定期清理」。當時盤點：agentctl 已追蹤檔 14,720 個、handoffs 佔 12,699；86 個 >1 MB 共 250 MB（含 20 MB 字典 json、兩份 8 MB 存檔 .ess、jsonl 語料），pack 177 MiB；handoffs/ 實體 1.9 GB 多半是各線 work/ 二進位。

**Why**：線每次交付都把中間產物（掃描 csv、ledger json、存檔、截圖、dll）留在自己的 handoff 目錄然後整目錄 `git add`；.gitignore 只擋了 trash/ work/ 幾種目錄名，沒擋副檔名與大小，也沒有人在收線時檢查。

**How to apply**：
- 版控政策（tidy-2026-09-25 team-hand 落地在 `agentctl/handoffs/README.md`「什麼能進版控」與 `.gitignore`）：准 md、≤1 MB 的 json/tsv/csv、≤512 KB 的腳本與 txt；不准任何 >1 MB 單檔、遊戲資產與二進位副檔名、work/ trash/ tmp/ preserved-*/ artifact/ offline/ mirror/ before/ after/ bin/ obj/ .housecarl-work/ 目錄。
- 工具：`agentctl/tools/hygiene_check.py`（`tracked`／`staged`／`disk` 三子命令）＋ `agentctl/tools/hooks/pre-commit`（`git config core.hooksPath tools/hooks`）——team-code 2026-09-25 建。
- 收線必跑 `hygiene_check.py tracked` → 0；每條線的交接書要寫「>1 MB 產物放 work/（gitignored）」；已追蹤的違規檔用 `git rm --cached`（留磁碟），刪實體與改歷史都要先問使用者。
- 定期：每次收工跑 disk 子命令看 handoffs/ 各日目錄 du，>10 MB 的未追蹤目錄列 WAIT_USER 請使用者裁刪；一個月一次 tidy 輪。
相關：[[commit-explicit-paths-only]]、[[dont-clutter-home-with-agent-output]]、[[archive-obsolete-and-unlink]]

2026-10-23 補：共用分析工具若從未進版控（`git status` 顯示 `??`），多線用「sha256 跑前跑後一致」當「工具沒被動過」的憑證並不成立——這個憑證本身沒有版控基礎支撐，任何人本機改過都不會被發現；多線平行使用同一支共用腳本做驗收前，先確認腳本本身是否已追蹤，未追蹤要先收進版控（`agentctl/handoffs/done/2026-10/home-2026-10-09/vf-text3/DONE-merge.md`）。

2026-10-23 補：政策文件允許的例外若沒實作進 `hygiene_check.py` 會變成誤擋合規 commit——`handoffs/README.md` 明寫 `work/backup/**` 純文字備份要留版控，但檢查工具一度沒這條例外，一律判違規。改政策文件時要同步檢查對應工具是否已實作該例外，發現誤擋補規則＋補正負向測試一起鎖住（`agentctl/handoffs/done/2026-10/home-2026-10-10/git-tidy/REPORT/git-cleanup.md`）。

## ignored-is-not-a-deletion-policy

> 「被 git ignore」不能直接當刪除理由——先 `git check-ignore -v` 查規則來源：來自版控內 `.gitignore` 的才是政策，來自 `info/exclude`／global 的只是個人本機設定。

同日第三案補總結：**關於「這個檔重不重要」，git 的沉默從來不是答案**——`ignored` 不等於可刪、`info/exclude` 不等於政策、「未進版控」更不等於不重要（10-23 第三案：唯一一份的 `.ess.bak` 存檔因「未進版控」被推論成「所以可刪」，正確推論恰好相反——未進版控且全機無第二份＝刪了就沒了）。工具端已加 `IRRECOVERABLE` 分流（未進版控＋全機無第二份→預設排除，與 `gitignore:local` 同層級），見 `agentctl/handoffs/home-2026-10-23/tidy/T1/tools/build_candidates.py`。

2026-10-23 T1 清理 handoffs 未追蹤實體：兩份 7.8/8.0 KB 的 HANDOFF.md（`done/2026-09/home-2026-09-16/` 的 rsrm 與 yros）被列入刪除並執行，**永久遺失**（從未進版控、無備份）。根因：清單判準把 `git ls-files --others --ignored` 的輸出一律當「政策判定可丟」，但這兩檔被 ignore 的來源是 `.git/modules/agentctl/info/exclude` 的本機個人規則——不進版控、別人 clone 看不到，且與工作區「`*.md` 一律進版控」政策直接衝突。同類 `gitignore:other` 共 138 項，餘者均為 .pyc／鎖標記／可重產物，損失未擴散，但純屬僥倖。

**How to apply**：以 ignore 狀態生成刪除候選時，逐項（或逐規則）跑 `git check-ignore -v` 分流：`gitignore:policy`（來源是版控內 `.gitignore`）可列候選；`gitignore:local`（來源是 `info/exclude`、`core.excludesFile` global）**預設不列**，改列「ignore 規則與版控政策衝突」待人裁。另外 `info/exclude` 裡任何與政策衝突的規則本身就該清。工具已修：`agentctl/handoffs/home-2026-10-23/tidy/T1/tools/build_candidates.py`。

2026-10-23 補：同一模式也出現在自製隔離機制上——2026-08-06 `~/skyrim_mods/.quarantine/2026-08-06/` 被直接 `rm` 整個目錄（未經 `quarantine.py restore`），107 筆/6.26 GiB 一度視為不可復原（事後核對實質損失為零，但安全網本身的意義被破壞）。任何自製隔離/待刪機制，清空前一律走它自己的 restore／release 指令，不要把「反正是暫存/隔離區」當成可以直接 rm 的理由（`mod-library/audits/2026-08-06-deletion-incident.md`）。


## gitignore-exclusion-and-negation-pitfalls

> .gitignore 的目錄級排除會擋住內層的 `!` 白名單，改規則本身還可能讓現役線的證據被悄悄忽略。

2026-08-30～09-25 三個教訓：(1) 排除整個目錄（`teams/`）後 Git 不會再進去套用 `!teams/*/members` 這類白名單；要排除到檔案層級（`teams/*/*`）再對特定檔名取反，寫完用 `git check-ignore -v` 雙向驗證（`agentctl/handoffs/done/2026-08-30/inbox-layering/HANDOFF.md:111-114`）。(2) 否定條目若父目錄已被排除規則擋住一樣不生效；要讓 `handoffs/**/work/backup/` 例外，必須同時寫 `!handoffs/**/work/backup/` 與 `!handoffs/**/work/backup/**`，只寫目錄那條不夠（`agentctl/handoffs/done/2026-09/home-2026-09-18/hygiene/REPORT.md:56`）。(3) 2026-09-25 新增 before/、after/、*.log、*.png 等規則後，當時還在跑的線之後 `git add` 同類證據被靜默略過，git 只提示要 `-f`（`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/team-hand/REPORT.md:45`）。

**Why:** 目錄排除與否定條目的套用順序違反直覺；規則本身的變動是全域的，會波及當時不知情的其他線。

**How to apply:** 寫「目錄下大部分忽略、少數要留」規則時排除到檔案 glob 層級，否定條目目錄與 `/**` 都要寫；改 `.gitignore` 後通知現役線，收線前 `git status --ignored` 抽查有沒有該進版控卻被忽略的產物。相關：[[handoffs-junk-not-tracked-periodic-hygiene]]

## scan-inbound-links-before-delete

> 刪除前要查的不只是「這檔重不重要」，還有「誰依賴它」——清單產生時就掃活文件的入站連結，正確順序是「刪之前就知道誰會斷」，不是「先刪再發現」。

2026-10-23 T1 刪除 handoffs 未追蹤實體 382 MB 後，全庫 `check_markdown_links.py` 從 0 紅變 178 紅：done/ 的歷史 REPORT 連著自己產的截圖／log／work 目錄，之前全綠只是因為檔「未追蹤但還在磁碟」。事後補救是把 176 條連結批次改成不可點擊註記（工具 `annotate_dead_links.py`，格式統一「原路徑＋移除日期＋不可復原」）。

**Why**：連結檢查的綠燈蓋的是「磁碟上有」，不是「版控裡有」；刪未追蹤檔一樣會弄斷活文件。把封存區排除出掃描不是解法——那會讓下次大刪除完全無聲，跟 HANDOFF.md 誤刪沒被察覺是同一個模式。

**How to apply**：產刪除清單的工具要內建入站連結掃描（tracked md 全掃、連結解析到 repo 相對路徑、與候選集取交集），命中的另列 `linked-review.tsv` 不自動列刪；處置二選一：排除該檔，或刪除批次裡同時帶上連結改寫。已實作：`agentctl/handoffs/home-2026-10-23/tidy/T1/tools/build_candidates.py` 的 `inbound_refs()`；註記工具同目錄 `annotate_dead_links.py`。

同日變形（封存判斷也適用）：**「有人連過來」要先分辨連過來的是歷史文件還是 open 項——那決定的不是「能不能封存」，而是「封存後連結怎麼處理」**。10-23 R3 把兩份被 `wait-user` 與 `status/todo` 點名的文件歸成「已結案但被連結釘住」而不敢動；同日 `xarch` 線拿到使用者裁示「都可以清掉的」後三組全部封存，做法分兩路：被**純歷史文件**釘住的（遷移計畫、工作量估算）走標準 archive 規則，來源連結拿掉改純文字；被 **open 項**釘住的（`modlist-coverage-2026-09-01.md`）**封存不刪、來源連結改指 archive 新路徑**，open 項照樣連得到，封存只表示它退出維護鏈與盤點範圍，不表示待辦結案。另外「被 open 項連著」要實查狀態：那次點名的 `status/todo/05、06、17` 查下去其實早在 2026-09-05 就 `done` 了。
