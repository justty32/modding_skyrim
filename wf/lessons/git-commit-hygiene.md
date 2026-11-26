# 版控：commit、pathspec 與工作樹

[lessons 索引](README.md)

## commit-explicit-paths-only

> 任何 repo 的 commit 只加明確檔案路徑；目錄級 `git add` 會掃進別隊的中間產物、push 後歷史永久變胖；各隊 >5 MB 中間產物 gzip 或不進版控

目錄級 `git add <dir>` 會把別隊還沒壓縮的中間產物一起收進 commit；push 後 repo 歷史永久變胖（2026-09-11 agentctl）。

**Why：** 領隊還在工作時目錄裡有大量暫存，目錄級 add 等於替別人 commit。COMMON 硬規則 4：「commit 只加明確路徑」。

**How to apply：**
1. 頂層與領隊 commit 一律列明檔案（`git add <file> <file>`），COMMON／NEXT-SESSION／STATE 各自單獨加。
2. 各隊 `data/` 產物 >5 MB 先 gzip；純中間產物寫進 `.gitignore` 或放 `~/skyrim_mods/_staging-*`。
3. 誤 push 大 blob 後要瘦身只能 `git filter-repo`＋force push，要先問使用者。

有並行線時（別線可能已 `git add` 暫存自己的改動），「add 明確路徑＋不帶 pathspec 的 commit」會把別線已暫存的東西一起帶走：一律 `git commit -- <paths>`（含 untrack 的批次例外，見 [[pathspec-commit-drops-untrack]]）（2026-10-03）。

多隊並行寫 git index 時 `git mv`／`git add` 會撞 `.git/index.lock`：sleep 2 重試、最多 10 次，或把 git 寫入收斂到單一條線（`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/SPEC.md:102`）。

工人搬檔若用 `os.rename`／`shutil.move` 而非 `git mv`，git 看到的是「N 刪＋N 未追蹤新檔」，`git diff --cached -M` 認不出 rename；大量搬檔的交接書寫死「用 git mv」，並列自證「`--name-status -M` 全部是 R、D=0」（`agentctl/handoffs/done/2026-08-31/condense-2026-08-31/team-a/gotchas-snippets.md:20-28`）。

驗「重排過的清單有沒有破壞既有相對順序」先對 HEAD `git diff` 數 insertions／deletions：0 deletions（純插入）就保證舊項目相對順序不變，大量 deletions 才值得重跑模擬（`agentctl/handoffs/done/2026-08-28/opus-apply-order/STATE.md:82-94`）。

多線平行對同一個 profile 做純插入式修改時，各自 commit 會把別線未定案的內容鎖進歷史：由一條指定的收尾線在所有線套用完後，用 `git apply --cached` 做只含自己 hunk 的 patch、驗 `git diff --cached` 只剩自己那幾行才 commit；做不到就不 commit、REPORT 寫明（`agentctl/handoffs/done/2026-10/home-2026-10-03/want-watch/rounds/20261003-1355/REPORT.md`）。

相關：[[dont-clutter-home-with-agent-output]]

## pathspec-commit-drops-untrack

> `git commit -- <paths>` 會忽略 index 裡的 `git rm --cached`，讓「改不追蹤」整批消失；多隊同 repo 要分批 commit 時只能對純內容改動用 pathspec

pathspec commit 拿**工作樹內容**建臨時 index，含 `git rm --cached`（檔案留磁碟）的那批會被當成「還在、未變」，untrack 全部不生效；pre-commit hook（hygiene_check staged）會擋下（2026-09-25）。

**How to apply**：含 untrack 的批次用完整 index 的 `git commit`（先把別隊改動 commit 掉，再 `git add -u <範圍>` 後直接 commit）；只有純內容修改的批次才用 pathspec 分批。多隊同 repo 收尾順序：先 commit 不含 untrack 的隊，最後一次完整 commit 收 untrack 那隊。hook 擋下時看它列的路徑是不是 `dir:work/` 這類「已 rm --cached 但工作樹仍在」的檔。相關：[[handoffs-junk-not-tracked-periodic-hygiene]]、[[commit-explicit-paths-only]]

同類全有全無陷阱：`git restore --staged <path1> <path2> ...` 只要有一個 pathspec 不存在，整條中止、一個都不還原；批次取消 staged 要一條一條下，或先 `git status` 確認每個路徑都存在（`agentctl/handoffs/done/2026-08-31/slim-modlib-2026-08-31/SPEC.md:42`）。

## profile-promote-switches-worktree

> profile_workflow promote 會 switch 到 main（動 live 工作樹）；別的線還在 feat 分支施工時，用 git branch＋update-ref 快轉 main 再 push，收線後再正式 promote

`instance/profiles/.repo/tools/profile_workflow.py promote` 是 `update-ref main` 後 **`git switch main`**，且 `start release/*` 必須從被凍結的 feat 分支上跑；另一條線正在 live checkout 的 feat 分支寫三檔時不能跑它。

做法（2026-09-03 驗證可行）：`git branch release/<日期>-<段> <feat 尖端>` ＋ `git update-ref refs/heads/main <尖端> <舊 main>`（不動工作樹）→ push main／release／feat；等那條線收線、工作樹乾淨後，再 `start release/...`＋`promote` 正式跑一次，live checkout 就回到 main。

**Why:** 使用者 2026-09-03 說「我要 promote 與 push」時別線還在 feat 分支上施工，直接跑工具會把它的工作樹切走。
**How to apply:** promote 前先看 `git -C instance/profiles branch --show-current` 與 `status --short`；不乾淨或不是要 promote 的分支就走 update-ref 路徑。`record -m` 會自帶 `feat(profiles): ` 前綴，交接書要寫死訊息別重複。相關：[[profiles-repo-has-remote]]、[[profile-restore-order-and-flags]]。

一般 submodule 也一樣：要改被母 repo gitlink 釘選的 submodule 文件、又不想動 primary checkout（母 repo 不顯示 gitlink 變更），開臨時 `git worktree add` 的 detached worktree 建 commit、fast-forward 推到該 submodule 遠端分支，`git show origin/<branch>:<file>` 驗證後 `git worktree remove`（`agentctl/handoffs/done/2026-08-29/cx-rename/REPORT.md:31`）。

## run-tests-in-worktree-not-main-tree

> 多隊共用 repo 時 build／test 一律在 worktree 或隔離 clone 跑；主工作樹重建 dll 會打掉別隊釘選的二進位 sha256

在 `projects/ModForge` 主工作樹跑 `dotnet build`＋測試，產出的 dll 會覆蓋別隊釘選 commit 的二進位；消費方的 sha256 閘門擋得下，解法是隔離 clone 重釘（2026-09-18）。

**Why:** 同一 repo 的 bin/ 是共享的可變狀態；一隊的 build 就是另一隊的環境變更。

**How to apply:** 交接書寫死：任何 build／test 在 `git worktree add` 或獨立 clone 裡跑；消費二進位的一方釘 commit＋sha256 並在每次使用前驗；隊間共用 repo 時在 COMMON.md 列「誰可以動主工作樹」。相關：[[commit-explicit-paths-only]]。

## submodule-push-order-and-staleness

> 多層 submodule 收尾順序錯、或沒先確認子 repo／本地分支與遠端同步，會讓 gitlink 指到拉不到的 commit，甚至實質退版。

gitlink 記的是 commit（[[gitlink-is-a-commit-not-a-branch]]），本地分支也可能落後遠端；兩者都會讓「看起來乾淨」騙過人。

**How to apply:**
- 多層 submodule（profiles→instance→各子 repo→母 repo）一次性提交照「內到外」：先最內層、逐個子 repo、最後母 repo 收所有 gitlink；每個 repo 用 `git log --all --not --remotes` 驗未推 commit 為 0（`agentctl/handoffs/done/2026-08-31/ship-2026-08-31/HANDOFF.md:9-12`）。
- bump 子專案 gitlink 前先確認該子專案 ahead／unpushed 是 0，工作樹乾淨不等於遠端同步（`agentctl/handoffs/done/2026-09/home-2026-09-05/close/REPORT.md:72`）。
- 本地 main 落後 origin/main 時，`git switch main` 會丟掉遠端那幾個 commit；切分支前用 `git merge-base --is-ancestor` 確認不落後，落後就先 `git branch -f main <origin/main sha>` 快轉再切（`agentctl/handoffs/done/2026-09/home-2026-09-03/swe/REPORT.md:32`）。

母 repo 設了 `submodule.recurse=true` 時，`git pull` 會把每個子 repo checkout 成母 repo 記的 gitlink（detached HEAD），gitlink 比子 repo main 舊就等於退版，之後的 commit 也落在 detached HEAD（2026-10-26 agentctl；`agentctl/handoffs/home-2026-10-26/tidyall/agentctl/REPORT.md:5`）。母 repo 拉更新一律 `git pull --no-recurse-submodules`；子 repo 開工前先 `git -C <子 repo> branch --show-current`，空的＝detached。

相關：[[profiles-repo-has-remote]]
