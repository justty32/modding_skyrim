# splitting — >8 KB 拆檔的兩種做法

[tidy](README.md)｜[STRUCTURE](../../STRUCTURE.md)

交接書直接引用本檔；工人 prompt 把本檔整份貼進去。

兩個門檻，各自獨立觸發（`archive/` 不算）：

- **條列式區塊 > 1024 bytes**（2026-08-30 定）：一份 md 裡任何一張表或一段清單超過 1 KB，就抽成資料檔（A 法），**不管整檔多大**。掃法：`python3 tools/find_big_lists.py <dir>`（母 repo 根跑；submodule 內 `../tools/`），它列出每個超標區塊的位置、型態、列數。**例外**：導航用的表（README 路由表、派發表、目錄表、code map）本身就是導覽，留在 md——判準是「一列一個要去的地方」而不是「一列一筆記錄」。
- **整檔 > 8192 bytes**：抽完資料檔後還超標的，是散文太長，走 B 法拆資料夾。

先判斷檔案性質：

### A. 同質大列表 → 抽成 `.json`（或 `.csv`）資料檔，用 `tools/tabledb.py` 存取

判準：一張表／一段條列超過 1 KB，且每列是同一組欄位的一筆記錄（ledger、候選表、對照矩陣、intake gate 逐件表、訊息集、證據表）。

做法：
1. 在同目錄建 `<原檔名去掉 .md>.json`（多張表就 `<原檔名>-<表名>.json`），格式固定：
   ```json
   {"source": "<原 md 相對路徑>", "extracted": "YYYY-MM-DD",
    "columns": ["id", "name", "..."],
    "rows": [{"id": "31472", "name": "...", "...": "..."}]}
   ```
   - 欄位順序＝原表欄位；值一律字串、原表怎麼寫就怎麼存（粗體、行內 code、連結原樣保留，不清洗、不拆解）。
   - 多行值（訊息正文）直接放字串；只有扁平、無多行值的表才可選 `.csv`（第一列欄位名）。
   - **不寫任何 per-file 的 .py**——存取一律走母 repo 的 [`tools/tabledb.py`](../../../tools/tabledb.py)（CRUD：`FILE`／`get I`／`find k=v`／`grep RE`／`add`／`update`／`delete`／`--slice A B`；Python 端 `from tabledb import load`）。submodule 內用 `python3 ../tools/tabledb.py <file>`。
2. 原 md **留在原路徑**（外部連結都指它），改成：目的／欄位說明／怎麼查（三行範例：`python3 ../tools/tabledb.py x.json`、`… get 12`、`… find id=31472`）／統計（幾列、GO／DEFER 幾件）／原本表以外的散文段落。≤ 8192 bytes。
3. 資料檔不套大小門檻。
4. 驗證：`python3 ../tools/tabledb.py x.json` 印出 count 與 columns；count 要等於原表列數（先 `grep -c '^|' 原檔` 記下，扣掉表頭 2 行）；`… get 0` 印第一列。

### B. 散文／混合 → 按語意拆成資料夾

判準：抽掉資料檔後仍 > 8 KB，內容是段落式的分析、計畫、步驟、根因。

做法：原檔**留在原路徑**當入口（≤ 8192 bytes：摘要＋各段一句話＋連結），細節按語意拆進同名資料夾 `<原檔名去掉 .md>/` 的幾個檔（每個 ≤ 8192 bytes，檔名即其段落意義）。已有同名資料夾的（如 `mihail-creature-catalog/`）直接往裡加。子頁裡的表若又是同質大表，套 A。

### 共通

- 一律 `git mv`／新檔 `git add`，不 commit、不 push。
- **原路徑一律保留**（入口或摘要），這樣別的 repo 指過來的連結不會斷；行號引註（`x.md:48`）失效是可接受的。
- 同一份東西不要同時存在 md 表與資料檔裡（md 不留原表副本）。
- 不改內容實質、不重新判定任何 GO／DEFER；只搬、只摘要。
- 完成後跑該 repo 的 `wf/tools/wf-lint.sh --strict .` → `TOTAL broken=0 residue=0`。
