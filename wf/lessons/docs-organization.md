# 文件整理：刪過時、拆檔與頁面歸屬

[lessons 索引](README.md)｜刪除前的掃描見 [deletion-safety](deletion-safety.md)

## user-facing-pages-go-in-wf-user

> 2026-09-26 使用者裁示：給他看的東西（清單／審批／裁示單）放母 repo 頂層 wf/user/，不放 agentctl/handoffs 也盡量不進 agentctl

2026-09-26 使用者原話：「以後給我看的東西不要放在 handoffs 那邊，也盡量不要放在 agentctl 裏面。盡量往頂層 wf/ 那邊放」。`wf/user/` 的結構是 README＋`YYYY-MM-DD-<主題>.md`。

**Why:** handoffs 是 agent 間的交接與證據堆，他不想在裡面翻；頂層 wf/ 是他的入口。

**How to apply:** 濃縮給使用者的成品（開玩前清單、要他裁示的選項頁、驗收單）寫到 `wf/user/`，內文連回 agentctl 的 REPORT 當證據；agent 內部 REPORT／RT-QUEUE／COMMON 仍留 handoffs。要拍板的可同時做 Artifact（[[send-screenshots-to-session]]），檔案本體仍在 wf/user/。給人導航的留 md（[[archive-obsolete-and-unlink]]）。

產頁類成品（換臉挑選頁、隨從名冊等）的 HTML 不進版控，只有產頁腳本、模板、來源 CSV/JSON 進版控；要重現或更新頁面就改腳本重產生，不手改輸出的 HTML（2026-10-23，`agentctl/handoffs/done/2026-10/home-2026-10-10/artifact-update-H1p9Y7/REPORT.md`）。`wf/user/` 的保留期見 [STRUCTURE](../STRUCTURE.md) local 段。

## archive-obsolete-and-unlink

> 2026-08-30 使用者定的五條文件整理原則；現行條文在 tidy README、STRUCTURE 與 data-files。過時的直接刪（2026-11-05 起不再封存），指向它的連結拿掉、不改指

現行條文：[tidy「五條原則」](../workflows/tidy/README.md#五條原則)（過時即刪、資料夾別擠、小檔合併、給人點的留 md／給 AI 讀的進資料檔）、[STRUCTURE](../STRUCTURE.md)（archive 規則 local 段、觸發 A／B）、[data-files](../workflows/common/data-files.md)（連結表超過十條才考慮、給人導航的留 md；抽表後的 md 不寫查詢指令）。

使用者原話：2026-08-30「不用這麼嚴格，反正就是整理，**過時或已經解決的可以清掉**」；2026-11-05「封存的其實也可以刪掉了」（封存改為一律 `git rm`，追溯靠 git history）。

**Why:** 舊文件留連結，後續的線會把它當現役材料讀進去。

**How to apply:** 派整理線前先讀該 repo 的 `wf/workflows/tidy/README.md`，不要憑印象寫交接書。指向被刪檔的連結拿掉（改純文字或整句刪）；`fix_moved_links.py` 只用於「搬位置但仍現役」的檔。拆檔與掃描的陷阱見 [[doc-restructure-safety-checklist]]。相關：[[wf-kernel-upstream-and-upgrade]]、[[investigate-all-then-install-once]]

## doc-restructure-safety-checklist

> 拆檔、抽表、刪檔、全庫改字前要先做的機械檢查與做法；連結檢查器看不到的陷阱

拆檔前查錨點連入者見 [content-trim](../workflows/tidy/content-trim.md)、[tidy gotchas](../workflows/tidy/gotchas.md)；以下是那裡沒寫的。

**可達性與引用**（`agentctl/handoffs/done/2026-08-29/doc-refactor/REACHABILITY.md:59-139`）：可達性掃描把「走不到連結」當刪除候選，但至少六類不該刪：非 `.md` 引用、上游 fork 文件、自成體系知識樹、行號引用、跨 repo anchor、目錄登記但個別檔未列。`file:line` 行號引用在 reflow 後指錯而 gate 全綠（檔尾純追加例外）。跨 repo anchor 的紅燈出在引用端、弄壞的是被引用端改了標題，改現役文件標題前先 `git grep -n '#<標題 slug>'`。兩份內容相同的文件可能有一份是 mode `120000` 的跨 repo symlink，當重複副本改寫會寫穿正典檔，先 `git ls-files -s` 看 mode（`agentctl/handoffs/done/2026-08-29/doc-refactor/LINEREF-FREEZE.md:89-93`）。

**量測工具自己會說謊，而且總是往「乾淨」的方向說謊**（2026-10-24）：
- 「同一份內容可能有多條路徑」時（symlink 掛在父目錄），`Path.is_symlink()` 只看最後一段、代表權退化成字典序。**去重鍵用 inode（或 `git ls-files -s` 的 blob），不要用路徑字串的任何判斷函式**；修法要兩層：`traverses_symlink()` 查整條路徑，且同一 inode 的所有路徑共享可達性。
- 「非 md 檔裡出現完整 md 路徑＝算可達（`coderef`）」會讓進了版控的 scratch 腳本把它掃過的檔全變可達。**常設工具裡不准寫死被量測對象的完整路徑**（`classify_unreached.py` 的豁免常數只存目錄字串）；一次性腳本非留不可就放 `handoffs/<場次>/<線>/tools/` 並在 REPORT 註明會污染 coderef。
- 報告把「bug 修好了」與「我盯的那個數字變了」分開寫：修好的 bug 可能不動你盯的統計口徑、卻修掉別處的假孤兒。

來源：`agentctl/handoffs/home-2026-10-24/reachbug/REPORT.md`、`agentctl/handoffs/home-2026-10-24/orphan6/REPORT.md`、`agentctl/handoffs/home-2026-10-24/reachbug/data/false-orphans-fixed.tsv`。

**B 法拆檔**：子檔檔名用英文 kebab-case 語意名不用流水號、單一子檔不低於約 1.5 KB（低於就併回入口或鄰居）。拆被腳本讀的索引／路由頁（如 `CODE_MAP.md`）前先 grep 哪支工具寫死了它的路徑——`check_code_map_coverage.py` 的 `INDEX_PAGES` 不讀子檔，拆完整批模組變 UNINDEXED，拆完重跑該工具比對拆前基線（`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/team-docs/REPORT.md:21`、`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/team-mom/REPORT.md:41,50`）。

**全庫政策文字掃描**要把命中分三類：LIVE（現行文件，要改）、SENT（已送出的交接書，改了追不回，留當證據）、歷史紀錄（刻意保留舊規則文字）——只改 LIVE 且與新規則牴觸的（`agentctl/handoffs/done/2026-08-30/scrn-2026-08-30/SWEEP-cx-scrn1.md:118-145`）。

**抽表**：自動推論欄位遇到可疑命中（如撞名）加 `SUSPECT(...)：` 前綴留在表裡，不要靜默清掉或填掉。每列保留一個「原文」欄存完整原始 markdown，逐行比對快照才能證明沒丟東西；open 項目遠超活層 byte 預算時改成「群組＋筆數＋卡在哪」的 ledger，群組筆數加總必須精確等於原始總數，逐項明細另存可回溯的 tsv（`agentctl/handoffs/done/2026-09-02/vfo-2026-09-02/REPORT.md:33-44`、`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/team-docs/REPORT.md:4`、`agentctl/handoffs/done/2026-08-31/condense-2026-08-31/team-a/REPORT.md:38-49`）。

**活檔與索引**：別人會往檔尾追加的活檔，抽歷史時把已結束的節搬到現役節前面、現役節留檔尾，照舊習慣追加的人才落對位置。手寫維護的索引／計數表沒有機械檢查大約一個月內必失效：納入 wf-lint 掃描（目錄項⊆索引項），或改生成式索引、或不做索引靠檔名／日期導航（`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/team-inbox/REPORT.md:5-14`、`agentctl/handoffs/done/2026-09/home-2026-09-03/hub/REPORT.md:55`、`logs/README.md:5`）。

相關：[[archive-obsolete-and-unlink]]、[[cite-by-anchor-not-line-number]]

## corpus-reliability-flagging

> agent 產出的參考語料（網頁快照、調查文件）要逐段標可信度，不能整份當原文或整份當定論。

網頁快照可能不是原文：因版權限制拒絕逐字重現的頁面，落檔是結構化事實抽取（專名／數字保留，敘事措辭已改寫）；JS 產生的頁面根本抓不到；這兩種都標 PARTIAL（2026-09-02 LoreRim wiki 快照）。`analysis/mod-survey/index.md:19` 同樣警告：survey agent 對「mod 怎麼運作」可信，但對「ModForge 缺什麼」是未查原始碼的推斷。

**Why:** 「可逐字引用的事實」與「agent 的推斷」不分開標記，後續線會把推斷當定論用。

**How to apply:** 網頁快照逐檔標 PARTIAL/FULL；依調查文件的「缺口」結論做決策前先對原始碼校正。來源：`agentctl/handoffs/done/2026-09-02/lorerim-2026-09-02/team-web/REPORT.md:25-27,50-51`。
