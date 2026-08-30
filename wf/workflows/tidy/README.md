# tidy — 文件結構整理（封存過時、分類雜亂、抽資料檔）

[WORKFLOWS](../../WORKFLOWS.md)｜[INDEX](../../INDEX.md)

把文件層收乾淨：活文件只留現役與 open 的東西，過時的封存、雜亂的分類、指向被封存檔的連結清掉、過大的條列抽成資料檔。方法本身在 [STRUCTURE](../../STRUCTURE.md)；上半是 kernel 的通用流程（盤點 → 交接書 → 派工 → 核驗），下半是**這個工作區的實際跑法與踩坑**。

**何時用**：「幫我整理 X」；一個資料夾幾十個檔扁平混放；某份表格被歷史項塞到幾十 KB；log／inbox 堆了一堆沒消化；文件自述「歷史」「已被取代」卻還被活文件連著。
**何時不用**：改程式碼結構 → [refactor](../refactor/README.md)；只搬一兩個檔 → [refactor/moving-things](../refactor/moving-things.md)；骨架升級 → 照上游 CHANGELOG 手動套。

## 四條原則

<!-- wf-nav -->
1. **過時的就封存，把指向它的連結清乾淨，當做它不存在**：活文件裡的連結是**拿掉**（改純文字或整句刪），不是改指到 `archive/` 路徑；只有 `archive/README.md` 的索引表可以連過去。「過時」的判準：文件自述歷史／被取代／前提作廢；文件描述的目標（計畫、批次、profile）已不存在；結論已整份被某現役文件吸收。
2. **一個資料夾別擠太多檔，但同類檔案可以放鬆**：同一系列 log／報告／記錄不必為了檔數硬拆；不同用途混放才拆。
3. **一個資料夾下太多小檔案（<1 KB）就適當合併**：同一批零散記錄併成一個檔或一張表；內容保留、原檔消失。找法：`find <dir> -type f -size -1024c | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn`。
4. **考慮使用者——給人點的留 md、給 AI 讀的進資料檔**：同質記錄表（每列一筆記錄）> 1 KB 就抽成 `.json`／`.csv`（存取統一走 `wf/tools/tabledb.py`）；連結表不看 bytes，超過**十條**才考慮，給人導航的（路由表、目錄表、派發表）留 md，給 AI 消化的（候選表、ledger 裡的連結欄）才抽資料檔。**整檔 > 8 KB 就按語意拆資料夾**——這兩個門檻各自獨立觸發，格式契約與 A／B 拆法在 [common/data-files.md](../common/data-files.md)，不在這裡重述。掃描：`wf/tools/find_big_lists.py`、`find … -size +8192c`。

## Done when

- 目標資料夾根層只剩入口 README ＋ 語意子資料夾（或同類檔案集合），每個子資料夾有 README。
- 每個被封存檔：`grep -rn --include='*.md' '<檔名>' <repo> | grep -v archive/` → 0 行；`archive/README.md` 有它一列。
- `wf/tools/wf-lint.sh --strict .` → `TOTAL broken=0 residue=0 oversize=0 biglist=0`（`biglist` 只算同質記錄表；連結表超標印 `BIGLIST-LINKS`，只 warning 不計入）。
- `find <repo> -name '*.md' -not -path '*/archive/*' -size +8192c | wc -l` → 0。
- 報告附 `moves.tsv`（`舊路徑<TAB>新路徑`）。

## 流程

角色分工：**調度者**只盤點、寫交接書、核驗、修跨資料夾／跨 repo 的連結；**實作線**分類、切批、逐批驗收。線**不得**進交接書範圍以外的資料夾或 repo。

1. **盤點（調度者）**：
   ```bash
   find . -path ./.git -prune -o -type f -print | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head   # 哪個資料夾擠
   find <dir> -maxdepth 1 -type f -printf '%s %f\n' | sort -rn | head   # 哪個檔肥
   find <dir> -type f -size -1024c | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn   # 哪個資料夾小檔太多
   python3 wf/tools/find_big_lists.py --min 1024 <dir>    # 哪個表／清單超標（含 links=N / linked=）
   python3 wf/tools/find_big_lists.py --links-only <dir>    # 哪個連結表 > 10 條，人判斷留 md 或抽
   ```
   把病灶寫成編號清單放進交接書；不要讓線自己找範圍。
<!-- wf-nav -->
2. **交接書**固定寫：分類方案（類別數 5–7，一張表列每類收什麼）、**檔名一律不改**（外部連結靠檔名對映修）、一律 `git mv`、每個子資料夾要 README、封存規則與四條原則、禁區（不 commit／不進交接書以外的範圍／不刪／不碰 kernel 檔與 `AGENTS.md` 實質內容）、**固定條數**的驗收命令、報告要附 `moves.tsv`。
3. **線跑**：按檔案性質選 A／B 拆法（見 [common/data-files.md](../common/data-files.md)）；共通：一律 `git mv`／新檔 `git add`，不留副本，不改內容實質，不重新判定任何狀態。多批可平行（各批只動自己範圍）。
4. **核驗（調度者）**：不信報告，自己跑一次 Done when 的命令；看 `git diff --cached --name-status -M` 確認是 R 不是 D+A；`archive/` 與 `AGENTS.md` 若被動到，只准是連結路徑那種修改。
5. **搬檔後修連結**：用各批的 `moves.tsv` 跑 `wf/tools/fix_moved_links.py`（先 dry-run 再 `--apply`；它跳過 code fence、解析相對路徑後重算）。**指向被封存檔的連結不重寫**——拿掉。跨資料夾／跨 repo 的壞連結留給調度者。
6. **收尾**：確認 Done when 全過，commit 由使用者或調度者決定。

## 本工作區的實際跑法

<!-- wf-nav -->
- **三層**（2026-08-30 定）：主 session（Fable）＝調度者；**一個 repo 一條 Fable 管理線**（`Agent` `model: fable`）分類、切批、派工人、逐批驗收；工人預設 **codex gpt-sol**，判斷密集用 Opus，機械活 Sonnet 不限。簡報範本 [manager-brief.md](manager-brief.md)；交接書契約照 [agent-dispatch](../agent-dispatch/README.md)。
- 盤點加兩條：`git log --since=<兩週前> --oneline -- <檔>`（誰沒人動）、`grep -rlE --include='*.md' '<repo>/<dir>/' <其他 repo…> | wc -l`（入站連結量）。
- Done when 加碼：子資料夾 README ≤ 300 行、入口 README ≤ 100 行；名冊／登記表 ≤ 8192 bytes；`SESSION-LOG.md` ≤ 4096 bytes 只列 open；母 repo 根 `python3 tools/check_markdown_links.py`（不帶參數、全庫）→ OK。
- 跨 repo 連結：各線收完後由調度者拿各線的 `moves.tsv` 跑 [`wf/tools/fix_moved_links.py`](../../tools/fix_moved_links.py) `--prefix <submodule>`，再全庫 `check_markdown_links.py`；交接書明寫「跨 repo 壞連結不追」，否則線會自己列對映表想幫忙修。
- 收尾：submodule 先 commit，母 repo 再 commit pin（pin 可達性由 `tools/hooks/pre-push` 擋）；三處 `unpushed=0`。

## 踩過的坑

<!-- wf-nav -->
- `check_markdown_links.py` 吃**檔案**路徑不吃目錄、只掃母 repo 追蹤的檔；submodule 內部用該 repo 的 `wf-lint.sh`，全庫檢查由調度者在母 repo 根不帶參數跑。
- ```markdown 圍籬內可能刻意放「壞」連結當測試字串；改寫器與檢查都要跳過 code fence。
- `youtube-audits/` 這種**目錄改名**會留正文引註殘留（`x.md:48` 這種），連結檢查抓不到，要另外 grep 舊目錄名。
- 線會把「archive 不維護內部連結」讀成「archive 不能動」而卡住 `broken=0`；交接書明說：archive 內只准動「取代者」連結，`archive/README.md` 只准**追加**列。
- 名冊（ROSTER）、領地登記（line-claims）要**把規則段留在活檔**、只搬歷史條目；「狀態」欄不可信，判準改用 `SESSION-LOG.md`／`docs/line-claims.md` 的「現役線 N 條」，證據直接寫進交接書，否則線「不敢猜」留一半。
- 「不搬 `logs/`」與「清指向 archive 的連結」會在同一批檔上打架；驗收命令只擋 rename／delete（`git diff --cached --name-status -M logs/ | grep -v '^M'`），不擋 modify。
- `inbox/new/` 可能有 `.`-開頭的隱藏訊息；用 `ls -A`。
- 線報告的「NEEDS-DISPATCHER」清單要照 [WAIT_USER](../../../WAIT_USER.md) 的格式落地，不能只留在回報裡。

## 交接

- 完成後 → 要裁示的事 [WAIT_USER](../../../WAIT_USER.md) 一行；為什麼這樣分類 → [decisions](../decisions.md)。
- 骨架本身要升級 → 記憶 `wf-kernel-upstream-and-upgrade`；上游 `~/repo/workflows`。
