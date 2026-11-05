# 階段 1 — agentctl（12,522 檔／271.5 MB → 約 960 檔／14 MB）

[計畫入口](README.md)｜規則見 [rules.md](rules.md)。只動 agentctl；母 repo 只在收尾時 pin。

批次對應 [deletions.csv](deletions.csv) 的 A1–A10。每批都是 `git rm -r <明確路徑>`，不做目錄級 `git add -A`；刪前先 `git ls-files <路徑> | wc -l` 與 csv 的檔數對帳。

## 1a 刪封存類（A1、A3、A5、A6、A10）— Sonnet

**範圍**：`handoffs/done/`（9,217 檔／203.4 MB）、`handoffs/history/`＋`superseded/`（30 檔）、`archive/`（557 檔／10.7 MB）、`logs/`（275 檔／1.8 MB）、`tools/archive/`（7 檔）。合計 10,086 檔／216 MB。

**風險**：低。全部自述「視為不存在／凍結」。連結斷鏈：live md 指向 `handoffs/done/` 的 md 連結 29 條（13 檔）、指向 `logs/` 17 條（11 檔）、指向 `archive/` 23 處（15 檔，多為說明句）、`history/` 1 條；lessons 裡 204 處 `handoffs/done/...` 是 code span 引用（鐵律 6 的來源位置），**不改**——歷史路徑仍可 `git show` 取回。

**做法**：刪 → 母 repo 根 `python3 tools/check_markdown_links.py` → 活文件的斷鏈**降純文字**（不刪句）；`handoffs/README.md` 的 done／superseded 表列刪、`README.md` 目錄表的 archive／logs 兩列刪、`docs/driving-codex/lessons-from-done-handoffs.md` 開頭加一句「來源交接書已刪，路徑可由 git history 取回」。

**Done when**：`git ls-files handoffs/done handoffs/history handoffs/superseded archive logs tools/archive | wc -l` → 0；母 repo 根 `check_markdown_links.py` → OK；`grep -rn --include='*.md' '](.*handoffs/done/' agentctl wf wait-user modpack-design mod-library/audits mod-library/README.md` → 0 行。

**使用者確認**：決策 2、4（一次勾）。

## 1b 刪到期場次夾（A2）— 刪檔 Sonnet、吸收結論 Opus

**範圍**：`handoffs/home-2026-10-17/`、`home-2026-10-18/`、`home-2026-10-23/`、`home-2026-10-24/`、`home-2026-10-26/`、`home-2026-11-01/`、`home-2026-11-02/`、`home-skyrim-cleanup-2026-10-17/`，947 檔／16.3 MB。**不動** `home-2026-11-03/`、`home-2026-11-04/`、`home-2026-11-05/`（PoE 凍結資料 24 MB 與現役續行點；PoE 解凍或 30 天到期後再依規則 2 處理）。

**風險**：中。102 個活檔 208 處提到 `handoffs/home-*`，其中指向這 8 夾的要逐條看：`WAIT_USER`／`wait-user/*.md`（實機驗收項的證據連結）、`wf/workflows/decisions.md`（5 處）、`wf/lessons/*`、`wf/user/2026-10-21-offline-fixes.md`、`agentctl/SESSION-LOG.md`「其他積壓」（指 10-23／10-24）、`mod-library/plugins/path-of-the-companions.md`（指 11-01／11-02 的 Varinia 取證與驗收原句）。

**做法**（Opus 先做①②，Sonnet 再做③）：①列出 8 夾被活文件連到的檔（`grep -rln --include='*.md' 'home-2026-1[01]-\(17\|18\|23\|24\|26\)\|home-2026-11-0[12]\|home-skyrim-cleanup' <五個 repo 活目錄>`），逐條判定：使用者原句／驗收結論 → 抄進引用它的活文件（wait-user 子檔、decisions、plugins md）；純證據 → 連結降純文字。②`agentctl/SESSION-LOG.md`「其他積壓」兩項：live-gap 一筆隨 10-23 夾刪除自然消失（刪該段）；`MEMORY.md` 指標項搬 WAIT_USER later-decisions。③`git rm -r` 8 夾；跑連結檢查。

**Done when**：`git ls-files handoffs/home-2026-10-* handoffs/home-2026-11-01 handoffs/home-2026-11-02 handoffs/home-skyrim-cleanup-2026-10-17 | wc -l` → 0；`check_markdown_links.py` → OK；①的判定表存 `handoffs/home-2026-11-05/slim/absorbed.csv`（欄：source_path、target_live_doc、kind=原句|結論|降純文字）。

**使用者確認**：決策 3。

## 1c inbox 與名冊（A4）— Sonnet

- **範圍**：`inbox/done/`（217 檔／9.7 MB）、`inbox/roster-history.json`（453 KB／247 列）、`inbox/done/README.md`；`inbox/mail/`、`orders/`、`teams/`、`topics/` 的執行期殘留（README 自述「歸檔或清除待裁示」）只留各自 README。
- **風險**：低；13 處連結（`wf/workflows/testing.md` 3、`dispatch-handoffs` 2 等）降純文字；`inbox_ack.sh`、`PROTOCOL.md`、`inbox/README.md` 的 done/ 敘述改成規則 3（屬規則改寫，Opus 在階段 0 寫定文字、本批只套）。
- **Done when**：`git ls-files inbox/done inbox/roster-history.json | wc -l` → 0；`ls inbox/mail inbox/orders inbox/teams inbox/topics` 各只剩 README.md（teams/ 五個 members 小檔一併刪）；`python3 -m unittest discover -s tools -p 'test_*.py'` 中 inbox 相關測試仍綠（若測試寫死 done/ 行為 → 交階段 4 一起改，本批不碰測試檔）。
- **使用者確認**：決策 6。

## 1d 紀錄表瘦身（A7、A8、A9）— Sonnet

- **範圍**：`qa/reports/` 278 檔／14.7 MB（全部 2026-08）；`status/todo/` 已結 24 件＋`STATUS.html`（179 KB，產出物；加 `.gitignore`）；`docs/line-claims-history.json`、`docs/backlog-history/`（6 檔／84 KB）。合計 309 檔／15 MB。
- **風險**：低。`qa/README.md` reports 段改成「最近 2 批」；`status/README.md` 件數句改；`docs/README.md` 兩句改；`status/tests/fixtures/expected.html` 是測試夾具，**不碰**（階段 4）。
- **Done when**：`git ls-files qa/reports | wc -l` → 0；`status/todo/index.json` 的 rows 數 → 1；`git check-ignore status/STATUS.html` → 命中；`git ls-files docs/line-claims-history.json docs/backlog-history | wc -l` → 0。
- **使用者確認**：決策 5；A8／A9 併決策 2 一起勾。

## 1e hub 精簡（規則 2 套用）— Opus

- `SESSION-LOG.md` 4.1 KB → ≤ 2 KB：open 段留「無」；PoE 暫凍留一句＋連 NEXT；「PoE暫凍前技術快照」「關機收線」兩段刪（內容已在 11-04 evening-recovery REPORT／STATE）。
- `handoffs/NEXT-SESSION.md` 4.8 KB → ≤ 4 KB：刪「舊段與歷史」段（history/ 已刪）；「暫凍前最新 checkpoint」與「現行約束」合併，只留使用者原句與現行邊界。照 [content-trim](../../tidy/content-trim.md) 跑原文檢查。
- **Done when**：`wc -c SESSION-LOG.md handoffs/NEXT-SESSION.md` 分別 ≤ 2048／≤ 4096；content-trim 原文檢查 → 0 行 `LOST`；`bash wf/tools/wf-lint.sh .` 的 `HUB-OVERSIZE` → 0。

## 重複與超標（本階段不另開批）

- agentctl 內 864 個重複 blob（24.7 MB）幾乎全在 `handoffs/done/` 與舊場次夾（backup manifest、check_masters 快照各存多份），隨 1a／1b 消失；規則 2 的 2 MB／場上限防再犯。
- 程式 >300 行：`tools/movesets/movecond.py`（626）、`build_movesets_all.py`（415）、`status/render_eli5.py`（421）。movesets 現役且有測試，拆檔屬 refactor 工作流、不在瘦身範圍，記 backlog 不動；`render_eli5.py` 隨 status 是否續用一起決定（status 儀表板上次更新 10-26，若使用者不再看就整個 `status/` 刪——**待使用者決定**，未列入預設批次）。
- 文件 >300 行：僅 `logs/` 兩份（隨 1a 刪）。
