# tidy／gotchas — 這個工作區整理與拆檔踩過的坑

[tidy](README.md)｜通用規則在 [README](README.md) 上半（kernel 版）與 [data-files](../common/data-files.md)；本檔只記這個工作區踩到的。

## 封存與搬檔（2026-08-30 整理輪）

<!-- wf-nav -->
<!-- wf-nav -->
- `check_markdown_links.py` 吃**檔案**路徑不吃目錄、只掃母 repo 追蹤的檔；submodule 內部用該 repo 的 `wf-lint.sh`，全庫檢查由調度者在母 repo 根不帶參數跑。
- ```markdown 圍籬內可能刻意放「壞」連結當測試字串；改寫器與檢查都要跳過 code fence。
- `youtube-audits/` 這種**目錄改名**會留正文引註殘留（`x.md:48` 這種），連結檢查抓不到，要另外 grep 舊目錄名。
- 線會把「archive 不維護內部連結」讀成「archive 不能動」而卡住 `broken=0`；交接書明說：archive 內只准動「取代者」連結，`archive/README.md` 只准**追加**列。
- 名冊（ROSTER）、領地登記（line-claims）要**把規則段留在活檔**、只搬歷史條目；「狀態」欄不可信，判準改用 `SESSION-LOG.md`／`docs/line-claims.md` 的「現役線 N 條」，證據直接寫進交接書，否則線「不敢猜」留一半。
- 「不搬 `logs/`」與「清指向 archive 的連結」會在同一批檔上打架；驗收命令只擋 rename／delete（`git diff --cached --name-status -M logs/ | grep -v '^M'`），不擋 modify。
- `inbox/new/` 可能有 `.`-開頭的隱藏訊息；用 `ls -A`。
- 線報告的「NEEDS-DISPATCHER」清單要照 [WAIT_USER](../../../WAIT_USER.md) 的格式落地，不能只留在回報裡。

## 拆檔與資料檔（2026-08-30 拆檔輪）

<!-- wf-nav -->
- `link_columns` 只列**整格＝相對路徑或單一 md 連結**的欄。把散文欄（`body`、`理由`、`機制`）或機外路徑欄（`Data/*.bsa`、`~/skyrim_mods/…`）列進去，v0.3 lint 會把整格當路徑驗、報幾百條假斷鏈；散文裡的 md 連結所有欄本來就會掃，不必標。
- B 拆檔最常見的破壞是**別處的 `#錨點`**：submodule 的 wf-lint 不抓，母 repo 根 `python3 tools/check_markdown_links.py` 才抓；拆前先 `grep -rn '<檔名>#'`，被錨定的標題原文保留在入口。
- 入口壓到 8192 邊緣（8125／8094／7979）再改一個字就爆；改字前先 `wc -c`。`wc -c … | awk '$1>8192'` 會被 total 行騙，用 `find -size +8192c`。
- 給人讀的總覽表（README 能力表、tools 說明表）不是記錄表，抽成 json 會被退回；判準是「一列一個要去的地方／要知道的事」vs「一列一筆同構記錄」。
- `grep -c` 接在不存在的腳本後面會印 `0` 假通過；驗收命令要在腳本所在 repo 根跑，或先 `test -f`。
- 用空行把清單切塊躲 BIGLIST 不算解；v0.4 起 `find_big_lists.py` 單一空行併塊。導航清單加 `<!-- wf-nav -->`，同質記錄抽資料檔。

## 派線（Fable 管理線 → 工人）

<!-- wf-nav -->
- Sonnet 工人會把 SendMessage 中途追加的規則當側路訊息**拒收**；規則改了就開新工人、把規則寫進主交接書，不要續同一個。
- 工人偶爾漏 stage 改過的 md；管理線驗收要含 `git status --short | grep -v '^[MADR] '` → 0，並以明確路徑補 `git add`。
- 工人的暫存要放 scratchpad 並帶批次前綴；曾有暫存 `t3.json` 落到母 repo 根、兩個工人撞同名暫存檔。
- 規則中途改三次（.py→json、1 KB 門檻、導航表先抽後收回）的代價是十幾個回補批；能先把契約定稿再派最省。
- 母 repo 的 wf-lint 用 `.` 會遞迴掃進所有 submodule，數字隨別條線在動；母 repo 自己只掃 `wf`。
