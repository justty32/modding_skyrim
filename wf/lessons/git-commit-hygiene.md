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

## run-tests-in-worktree-not-main-tree

> 2026-09-18 modforge 隊在主工作樹跑 build/test，重建 dll 打掉 dsp-build 釘選的 ModForge 二進位 sha256；多隊共用 repo 時測試一律在 worktree 或隔離 clone（原 type: feedback）

2026-09-18 事故：modforge 隊在 `projects/ModForge` 主工作樹跑 `dotnet build`＋測試，產出的 dll 覆蓋了 dsp-build 隊釘選在 `0af3188` 的二進位；dsp-build 的 sha256 閘門擋下（零污染產出），之後改用隔離 clone 重釘。

**Why:** 同一 repo 的 bin/ 是共享的可變狀態；一隊的 build 就是另一隊的環境變更。

**How to apply:** 交接書寫死：任何 build／test 在 `git worktree add` 或獨立 clone 裡跑；消費二進位的一方釘 commit＋sha256 並在每次使用前驗；隊間共用 repo 時在 COMMON.md 列「誰可以動主工作樹」。相關：[[commit-explicit-paths-only]]。

## submodule-push-order-and-staleness

> 多層 submodule 收尾順序錯、或沒先確認子 repo／本地分支與遠端同步，會讓 gitlink 指到拉不到的 commit，甚至實質退版。

2026-08-31～09-05 三次教訓：(1) 多層 submodule（profiles→instance→各子 repo→母 repo）一次性提交要「內到外」：先最內層，逐個子 repo，最後母 repo 收所有 gitlink，每個 repo push 完都用 `git log --all --not --remotes` 驗證未推 commit 為 0（`agentctl/handoffs/done/2026-08-31/ship-2026-08-31/HANDOFF.md:9-12`）。(2) bump 子專案 gitlink 前要先確認該子專案自己 ahead/unpushed 是 0，不是工作樹乾淨就等於遠端同步（`agentctl/handoffs/done/2026-09/home-2026-09-05/close/REPORT.md:72`）。(3) instance repo 本地 main 曾落後 origin/main 兩個 commit，照文件字面 `git switch main` 會丟掉那兩個 commit；要先 `git branch -f main <origin/main sha>` 快轉再切換（`agentctl/handoffs/done/2026-09/home-2026-09-03/swe/REPORT.md:32`）。

**Why:** gitlink 記的是 commit，本地分支也可能落後遠端；兩者都會讓「看起來乾淨」騙過人。

**How to apply:** 多層 submodule 收尾固定「內到外」順序；bump gitlink 前查子 repo ahead/unpushed；切分支前用 `git merge-base --is-ancestor` 確認本地不落後 origin。相關：[[gitlink-is-a-commit-not-a-branch]]、[[profiles-repo-has-remote]]
