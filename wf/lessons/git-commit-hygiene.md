# 版控：commit、工作樹與產物衛生

[lessons 索引](README.md)

## commit-explicit-paths-only

> 2026-09-11 事故：調度者用 `git -C agentctl add handoffs` 掃進別隊 68 MB 中間產物並 push，agentctl 歷史永久變胖；任何 repo 的 commit 只加明確檔案路徑，各隊 >5 MB 中間產物 gzip 或不進版控（原 type: feedback）

2026-09-11 23:1x：COMMON 61 那筆 commit 用目錄級 `git add handoffs`，把 lead-zhgap2 還沒壓縮的 68 MB 掃描中間產物一起收進 agentctl 並 push（pack 391 MB）。

**Why：** 領隊還在工作時目錄裡有大量暫存；目錄級 add 等於替別人 commit。COMMON 硬規則 4 早就寫「commit 只加明確路徑」，調度者自己違反。

**How to apply：**
1. 頂層與領隊 commit 一律列明檔案（`git add <file> <file>`），COMMON／NEXT-SESSION／STATE 各自單獨加。
2. 各隊 `data/` 產物 >5 MB 先 gzip；純中間產物寫進 `.gitignore` 或放 `~/skyrim_mods/_staging-*`。
3. 誤 push 大 blob 後要瘦身只能 `git filter-repo`＋force push，要先問使用者。
相關：[[dont-clutter-home-with-agent-output]]

**10-03 補**：並行線會先 `git add` 暫存自己的改動；頂層這時用「add 明確路徑＋不帶 pathspec 的 commit」會把別線已暫存的東西一起帶走（retro `19a51bba` 吃進 toolify 15 個改名）。有並行線時一律 `git commit -- <paths>`（含 untrack 的批次例外，見 [[pathspec-commit-drops-untrack]]）。

2026-10-23 補：多隊並行寫 git index 時 `git mv`／`git add` 會撞 `.git/index.lock`；遇到就 sleep 2 重試、最多 10 次，或把 git 寫入動作收斂到單一條線（`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/SPEC.md:102`）。

2026-10-23 補：codex 工人搬移/封存檔案慣用 `os.rename`/`shutil.move` 而非 `git mv`，會讓 git 把整批搬移看成「N 刪＋N 未追蹤新檔」，`git diff --cached -M` 偵測不到 rename；交接書對大量搬檔任務要寫死「用 git mv」，並把「搬移後 `--name-status -M` 全部是 R、D=0」列成工人自己要跑的自證（`agentctl/handoffs/done/2026-08-31/condense-2026-08-31/team-a/gotchas-snippets.md:20-28`）。

2026-10-23 補：驗證「重排過的清單有沒有破壞既有相對順序」不必重跑完整模擬，先對 HEAD 做 `git diff` 數 insertions/deletions——0 deletions（純插入）數學上保證舊項目相對順序不變；大量 deletions 代表被全面翻攪過，才值得花成本重跑模擬（`agentctl/handoffs/done/2026-08-28/opus-apply-order/STATE.md:82-94`）。

2026-10-23 補：多線平行對同一個 profile 做純插入式修改時，各自 commit 會把別線尚未定案的內容一起鎖進歷史；改由一條指定的收尾線在所有線套用完後，用 `git apply --cached` 做出只含自己 hunk 的 patch、驗證 `git diff --cached` 只剩自己那幾行才 commit，做不到就不 commit、REPORT 寫明（`agentctl/handoffs/done/2026-10/home-2026-10-03/want-watch/rounds/20261003-1355/REPORT.md`）。

## pathspec-commit-drops-untrack

> 2026-09-25 tidy 收尾踩到：`git commit -- <paths>` 會忽略 index 裡的 `git rm --cached`，讓「改不追蹤」整批消失；多隊同 repo 要分批 commit 時只能對純內容改動用 pathspec（原 type: project）

2026-09-25 tidy-2026-09-25 收尾：agentctl 一個 index 混著五隊改動，我想逐隊 `git commit -- docs`／`-- tools`／`-- inbox`／`-- handoffs` 分批提交。前三隊沒問題，但 team-hand 那批含 5,190 個 `git rm --cached`（檔案留磁碟），pathspec commit 會拿**工作樹內容**建臨時 index，把這些檔當成「還在、未變」，untrack 全部不生效；pre-commit hook（hygiene_check staged）因此擋下，才發現。

**Why**：`git commit <pathspec>` 的語意是「提交這些路徑在工作樹的內容、忽略 staged 狀態」，對 `rm --cached` 這種「索引與工作樹刻意不同」的操作天生不相容。

**How to apply**：含 untrack 的批次一律用完整 index 的 `git commit`（先把別隊的改動 commit 掉或 stash 掉，再 `git add -u <範圍>` 後直接 commit）；只有純內容修改的批次才用 pathspec 分批。多隊同 repo 施工時，收尾順序：先 commit 不含 untrack 的隊，最後一次完整 commit 收 untrack 那隊。hook 擋下時看它列的路徑是不是 `dir:work/` 這類「已 rm --cached 但工作樹仍在」的檔，就是這個問題。相關：[[handoffs-junk-not-tracked-periodic-hygiene]]、[[commit-explicit-paths-only]]

2026-10-23 補：同類全有全無陷阱也出現在 `git restore --staged <path1> <path2> ...`——只要有一個 pathspec 不存在，整條指令中止、一個都不還原，不是忽略不存在的那個繼續處理其餘；批次取消 staged 要一條一條下指令，或先用 `git status` 確認每個路徑都存在（`agentctl/handoffs/done/2026-08-31/slim-modlib-2026-08-31/SPEC.md:42`）。

## profile-promote-switches-worktree

> profile_workflow promote 會 switch 到 main（動 live 工作樹）；別的線還在 feat 分支施工時，用 git branch＋update-ref 快轉 main 再 push，收線後再正式 promote（原 type: memory）

`instance/profiles/.repo/tools/profile_workflow.py promote` 的實作是 `update-ref main` 後 **`git switch main`**，且 `start release/*` 必須從被凍結的 feat 分支上跑。所以當另一條線正在 live checkout 的 feat 分支寫三檔時，不能跑它。

2026-09-03 做法（已驗證可行）：`git branch release/<日期>-<段> <feat 尖端>` ＋ `git update-ref refs/heads/main <尖端> <舊 main>`（不動工作樹）→ push main／release／feat；等那條線收線、工作樹乾淨後，再 `start release/...`＋`promote` 正式跑一次，live checkout 就回到 main。

**Why:** 使用者 14:50 說「我要 promote 與 push」時 lrfw 還在 feat/lrfw 上施工，直接跑工具會把它的工作樹切走。
**How to apply:** promote 前先看 `git -C instance/profiles branch --show-current` 與 `status --short`；不乾淨或不是要 promote 的分支就走 update-ref 路徑。`record -m` 會自帶 `feat(profiles): ` 前綴，交接書要寫死訊息別重複。相關：[[profiles-repo-has-remote]]、[[profile-restore-order-and-flags]]。

2026-10-23 補：同樣「不想動主 checkout」的需求也適用於一般 submodule：要修改被母 repo gitlink 釘選的 submodule 文件、又不想讓母 repo 的 gitlink 顯示變更，開一個臨時 `git worktree add` 的 detached worktree 建 commit、fast-forward 推到該 submodule 遠端分支，`git show origin/<branch>:<file>` 驗證遠端內容後 `git worktree remove` 清理，全程不動母 repo 內的 primary submodule checkout（`agentctl/handoffs/done/2026-08-29/cx-rename/REPORT.md:31`）。

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

## run-tests-in-worktree-not-main-tree

> 2026-09-18 modforge 隊在主工作樹跑 build/test，重建 dll 打掉 dsp-build 釘選的 ModForge 二進位 sha256；多隊共用 repo 時測試一律在 worktree 或隔離 clone（原 type: feedback）

2026-09-18 事故：modforge 隊在 `projects/ModForge` 主工作樹跑 `dotnet build`＋測試，產出的 dll 覆蓋了 dsp-build 隊釘選在 `0af3188` 的二進位；dsp-build 的 sha256 閘門擋下（零污染產出），之後改用隔離 clone 重釘。

**Why:** 同一 repo 的 bin/ 是共享的可變狀態；一隊的 build 就是另一隊的環境變更。

**How to apply:** 交接書寫死：任何 build／test 在 `git worktree add` 或獨立 clone 裡跑；消費二進位的一方釘 commit＋sha256 並在每次使用前驗；隊間共用 repo 時在 COMMON.md 列「誰可以動主工作樹」。相關：[[commit-explicit-paths-only]]。

## ignored-is-not-a-deletion-policy

> 「被 git ignore」不能直接當刪除理由——先 `git check-ignore -v` 查規則來源：來自版控內 `.gitignore` 的才是政策，來自 `info/exclude`／global 的只是個人本機設定。

2026-10-23 T1 清理 handoffs 未追蹤實體：兩份 7.8/8.0 KB 的 HANDOFF.md（`done/2026-09/home-2026-09-16/` 的 rsrm 與 yros）被列入刪除並執行，**永久遺失**（從未進版控、無備份）。根因：清單判準把 `git ls-files --others --ignored` 的輸出一律當「政策判定可丟」，但這兩檔被 ignore 的來源是 `.git/modules/agentctl/info/exclude` 的本機個人規則——不進版控、別人 clone 看不到，且與工作區「`*.md` 一律進版控」政策直接衝突。同類 `gitignore:other` 共 138 項，餘者均為 .pyc／鎖標記／可重產物，損失未擴散，但純屬僥倖。

**How to apply**：以 ignore 狀態生成刪除候選時，逐項（或逐規則）跑 `git check-ignore -v` 分流：`gitignore:policy`（來源是版控內 `.gitignore`）可列候選；`gitignore:local`（來源是 `info/exclude`、`core.excludesFile` global）**預設不列**，改列「ignore 規則與版控政策衝突」待人裁。另外 `info/exclude` 裡任何與政策衝突的規則本身就該清。工具已修：`agentctl/handoffs/home-2026-10-23/tidy/T1/tools/build_candidates.py`。

2026-10-23 補：同一模式也出現在自製隔離機制上——2026-08-06 `~/skyrim_mods/.quarantine/2026-08-06/` 被直接 `rm` 整個目錄（未經 `quarantine.py restore`），107 筆/6.26 GiB 一度視為不可復原（事後核對實質損失為零，但安全網本身的意義被破壞）。任何自製隔離/待刪機制，清空前一律走它自己的 restore／release 指令，不要把「反正是暫存/隔離區」當成可以直接 rm 的理由（`mod-library/audits/2026-08-06-deletion-incident.md`）。


## submodule-push-order-and-staleness

> 多層 submodule 收尾順序錯、或沒先確認子 repo／本地分支與遠端同步，會讓 gitlink 指到拉不到的 commit，甚至實質退版。

2026-08-31～09-05 三次教訓：(1) 多層 submodule（profiles→instance→各子 repo→母 repo）一次性提交要「內到外」：先最內層，逐個子 repo，最後母 repo 收所有 gitlink，每個 repo push 完都用 `git log --all --not --remotes` 驗證未推 commit 為 0（`agentctl/handoffs/done/2026-08-31/ship-2026-08-31/HANDOFF.md:9-12`）。(2) bump 子專案 gitlink 前要先確認該子專案自己 ahead/unpushed 是 0，不是工作樹乾淨就等於遠端同步（`agentctl/handoffs/done/2026-09/home-2026-09-05/close/REPORT.md:72`）。(3) instance repo 本地 main 曾落後 origin/main 兩個 commit，照文件字面 `git switch main` 會丟掉那兩個 commit；要先 `git branch -f main <origin/main sha>` 快轉再切換（`agentctl/handoffs/done/2026-09/home-2026-09-03/swe/REPORT.md:32`）。

**Why:** gitlink 記的是 commit，本地分支也可能落後遠端；兩者都會讓「看起來乾淨」騙過人。

**How to apply:** 多層 submodule 收尾固定「內到外」順序；bump gitlink 前查子 repo ahead/unpushed；切分支前用 `git merge-base --is-ancestor` 確認本地不落後 origin。相關：[[gitlink-is-a-commit-not-a-branch]]、[[profiles-repo-has-remote]]

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
