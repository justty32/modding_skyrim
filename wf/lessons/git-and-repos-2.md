# 版控、repo 佈局與文件整理（2/4）

[lessons 索引](README.md)｜同主題：[git-and-repos](git-and-repos.md)、[git-and-repos-3](git-and-repos-3.md)、[git-and-repos-4](git-and-repos-4.md)

## gitlink-is-a-commit-not-a-branch

> 別在文件裡寫「某個 submodule 釘在某條分支上」；gitlink 指的是 commit，寫成分支會讓人拿錯東西對帳（原 type: feedback）

2026-08-26 使用者看到 `AGENTS.md` 寫「houseCARL 釘在 `justty32/houseCARL` 的
`fix/dialogue-encoding-lint`」，指示刪掉，理由是「pin 這個概念不應該存在」。

**Why:** submodule 的 gitlink 記的是一個 **commit**，不是一條分支。把它描述成「釘在分支 X」，
後來的人就會去對分支 X 而不是對那個 commit——實際上 houseCARL 的 gitlink 是 `fork/main` 上的
`efe28f8`，跟文件寫的分支不同。同一晚母 repo 還有 5 個 gitlink 指向側分支上的 commit，
一連串誤判都源自這個錯的心智模型。

**How to apply:** 文件要描述 submodule 關係時，寫真正的規則（例：「只維護自有 fork、不追
upstream」），不要寫「釘在哪條分支」。要講具體狀態就給 commit hash，並說明它從哪些遠端 ref
可達（那才是它會不會變孤兒的判準）。這是針對**文件寫法**的指示，不是要我去清洗 repo 裡
既有的 `chore: 推進 pin` 這類 commit 訊息用語——參見 [[dont-inflate-light-preferences]]。
相關：[[workspace-layout-and-duties]]、[[verify-waituser-against-logs]]。

## commit-explicit-paths-only

> 2026-09-11 事故：調度者用 `git -C agentctl add handoffs` 掃進別隊 68 MB 中間產物並 push，agentctl 歷史永久變胖；任何 repo 的 commit 只加明確檔案路徑，各隊 >5 MB 中間產物 gzip 或不進版控（原 type: feedback）

2026-09-11 23:1x：COMMON 61 那筆 commit 用目錄級 `git add handoffs`，把 lead-zhgap2 還沒壓縮的 68 MB 掃描中間產物一起收進 agentctl 並 push（pack 391 MB）。

**Why：** 領隊還在工作時目錄裡有大量暫存；目錄級 add 等於替別人 commit。COMMON 硬規則 4 早就寫「commit 只加明確路徑」，調度者自己違反。

**How to apply：**
1. 頂層與領隊 commit 一律列明檔案（`git add <file> <file>`），COMMON／NEXT-SESSION／STATE 各自單獨加。
2. 各隊 `data/` 產物 >5 MB 先 gzip；純中間產物寫進 `.gitignore` 或放 `~/skyrim_mods/_staging-*`。
3. 誤 push 大 blob 後要瘦身只能 `git filter-repo`＋force push，要先問使用者。
相關：[[dont-clutter-home-with-agent-output]]

## pathspec-commit-drops-untrack

> 2026-09-25 tidy 收尾踩到：`git commit -- <paths>` 會忽略 index 裡的 `git rm --cached`，讓「改不追蹤」整批消失；多隊同 repo 要分批 commit 時只能對純內容改動用 pathspec（原 type: project）

2026-09-25 tidy-2026-09-25 收尾：agentctl 一個 index 混著五隊改動，我想逐隊 `git commit -- docs`／`-- tools`／`-- inbox`／`-- handoffs` 分批提交。前三隊沒問題，但 team-hand 那批含 5,190 個 `git rm --cached`（檔案留磁碟），pathspec commit 會拿**工作樹內容**建臨時 index，把這些檔當成「還在、未變」，untrack 全部不生效；pre-commit hook（hygiene_check staged）因此擋下，才發現。

**Why**：`git commit <pathspec>` 的語意是「提交這些路徑在工作樹的內容、忽略 staged 狀態」，對 `rm --cached` 這種「索引與工作樹刻意不同」的操作天生不相容。

**How to apply**：含 untrack 的批次一律用完整 index 的 `git commit`（先把別隊的改動 commit 掉或 stash 掉，再 `git add -u <範圍>` 後直接 commit）；只有純內容修改的批次才用 pathspec 分批。多隊同 repo 施工時，收尾順序：先 commit 不含 untrack 的隊，最後一次完整 commit 收 untrack 那隊。hook 擋下時看它列的路徑是不是 `dir:work/` 這類「已 rm --cached 但工作樹仍在」的檔，就是這個問題。相關：[[handoffs-junk-not-tracked-periodic-hygiene]]、[[commit-explicit-paths-only]]

## profile-promote-switches-worktree

> profile_workflow promote 會 switch 到 main（動 live 工作樹）；別的線還在 feat 分支施工時，用 git branch＋update-ref 快轉 main 再 push，收線後再正式 promote（原 type: memory）

`instance/profiles/tools/profile_workflow.py promote` 的實作是 `update-ref main` 後 **`git switch main`**，且 `start release/*` 必須從被凍結的 feat 分支上跑。所以當另一條線正在 live checkout 的 feat 分支寫三檔時，不能跑它。

2026-09-03 做法（已驗證可行）：`git branch release/<日期>-<段> <feat 尖端>` ＋ `git update-ref refs/heads/main <尖端> <舊 main>`（不動工作樹）→ push main／release／feat；等那條線收線、工作樹乾淨後，再 `start release/...`＋`promote` 正式跑一次，live checkout 就回到 main。

**Why:** 使用者 14:50 說「我要 promote 與 push」時 lrfw 還在 feat/lrfw 上施工，直接跑工具會把它的工作樹切走。
**How to apply:** promote 前先看 `git -C instance/profiles branch --show-current` 與 `status --short`；不乾淨或不是要 promote 的分支就走 update-ref 路徑。`record -m` 會自帶 `feat(profiles): ` 前綴，交接書要寫死訊息別重複。相關：[[profiles-repo-has-remote]]、[[profile-restore-order-and-flags]]。

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
