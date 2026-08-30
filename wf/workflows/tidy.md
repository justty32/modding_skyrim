# tidy — 文件結構整理（封存過時、分類雜亂、清連結）

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

把一個 repo（母 repo 或任一 submodule）的**文件層**收乾淨：活文件只留現役與 open，過時的封存、雜亂的分類、指向被封存檔的連結清掉。方法本身在 [STRUCTURE](../STRUCTURE.md)（膨脹即拆／雜亂即分類／archive 規則）；本檔記的是**這個工作區實際怎麼跑一輪**——2026-08-30 對 agentctl 與 modpack-design 各跑過一次。

**何時用**：「幫我整理 X」；一個資料夾幾十個檔扁平混放；某份「名冊／登記表」被歷史項塞到幾十 KB；inbox／log 堆了幾十則沒消化；文件自述「歷史」「已被取代」卻還被活文件連著。
**何時不用**：改程式碼結構 → [refactor](refactor/README.md)；只搬一兩個檔 → [refactor/moving-things](refactor/moving-things.md)；只是 wf 骨架升級 → 照 `~/repo/workflows/CHANGELOG.md` 手動套。

## 四條使用者定的原則（2026-08-30）

1. **過時的就封存，把指向它的連結清乾淨，當做它不存在。** 活文件裡的連結是**拿掉**（改純文字或整句刪），不是改指到 `archive/` 路徑；只有 `archive/README.md` 的索引表可以連過去。
2. **一個資料夾別擠太多檔，但同類檔案可以放鬆**：同一系列 log／report／intake gates 不必為了檔數硬拆；不同用途混放才拆。
3. **一個資料夾下太多小檔案（<1 KB）就適當合併**：同一天的 inbox 訊息併成一個檔、零碎 evidence 併成一張表；內容保留、原檔消失。找法：`find <dir> -type f -size -1024c | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn`。
4. **>8 KB 就拆**，所有活文件都算（不只 `workflows/`）。**條列式、每條同質性很高的大列表**（ledger、對照矩陣、候選表、合併的訊息集）不要拆成好幾份 markdown——**抽成資料檔**（Python 或 Lua），提供按 index／key 取一筆的存取（`python3 x.py <index>` 或 `import`），markdown 只留摘要、欄位說明與怎麼查；散文式的長文才按語意拆成子頁＋入口。找法：`find <dir> -name '*.md' -not -path '*/archive/*' -size +8192c -printf '%s %p\n' | sort -rn`。

「過時」的判準：文件自述歷史／被取代／前提作廢；目標 profile／批次／計畫已不存在；結論已整份被某現役決策層吸收。

## Done when

- 目標資料夾根層只剩入口 README ＋ 語意子資料夾（或同類檔案集合），每個子資料夾有 `README.md` ≤ 300 行；入口 README ≤ 100 行。
- 名冊／登記表類活檔 ≤ 8192 bytes；`SESSION-LOG.md` ≤ 4096 bytes、只列 open。
- 每個被封存檔：`grep -rn --include='*.md' '<檔名>' <repo> | grep -v archive/` → 0 行；`archive/README.md` 有它那一列。
- 該 repo `wf/tools/wf-lint.sh --strict .` → `TOTAL broken=0 residue=0`；母 repo 根 `python tools/check_markdown_links.py`（不帶參數、全庫）→ OK。
- 報告附 `moves.tsv`（`舊路徑<TAB>新路徑`）。

## 流程

角色分工照 [agent-dispatch](agent-dispatch/README.md)：調度者只盤點、寫交接書、核驗、修跨 repo 連結；搬檔與寫 README 交給一條 Opus 線（一個 repo 一條線，**線不得進別的 repo**）。

1. **盤點（調度者，10 分鐘）**：每個 repo 跑一次——
   ```bash
   find . -path ./.git -prune -o -type f -print | sed 's|/[^/]*$||' | sort | uniq -c | sort -rn | head   # 哪個資料夾擠
   find <dir> -maxdepth 1 -type f -printf '%s %f\n' | sort -rn | head                                   # 哪個檔肥
   for f in <dir>/*.md; do echo "$(git log --since=<兩週前> --oneline -- "$f" | wc -l) $f"; done | sort -n  # 誰沒人動
   grep -rlE --include='*.md' '<repo>/<dir>/' <其他 repo…> | wc -l                                         # 入站連結量
   ```
   把病灶寫成編號清單，直接放進交接書；不要讓線自己找範圍。
2. **交接書**（範本：[agent-dispatch](agent-dispatch/README.md) 的契約）固定寫：分類方案（類別數 5–7，一張表列每類收什麼）、**檔名一律不改**（跨 repo 連結靠檔名對映修）、一律 `git mv`、每個子資料夾要 README、封存規則與四條原則、禁區（不 commit／不進別的 repo／不刪／不碰 kernel 檔與 `AGENTS.md` 實質內容）、**固定條數**的驗收命令、報告要附 `moves.tsv`。
3. **線跑**：多個 repo 可平行，因為各線只動自己的 repo；跨 repo 壞連結是預期的，留給第 5 步。
4. **核驗（調度者）**：不信報告，自己跑一次 Done when 的命令；看 `git diff --cached --name-status -M` 確認是 R 不是 D+A；`archive/` 與 `AGENTS.md` 若被動到，只准是連結路徑。
5. **跨 repo 連結**：兩線都收完後，用各線的 `moves.tsv` 跑 [`tools/fix_moved_links.py`](../../tools/fix_moved_links.py)（`--prefix <submodule>` 指定該份 tsv 的路徑基準；先 dry-run 再 `--apply`；它跳過 code fence、解析相對路徑後重算），再全庫 `check_markdown_links.py`。**指向被封存檔的連結不重寫**——拿掉。
6. **收尾**：各 submodule 先 commit，母 repo 再 commit pin（`push.recurseSubmodules=on-demand` 會先推 submodule；pin 可達性由 `tools/hooks/pre-push` 擋）；三處 `unpushed=0`。

## 踩過的坑

- `check_markdown_links.py` 吃**檔案**路徑不吃目錄，且只掃母 repo 追蹤的檔；要查 submodule 內部，線用該 repo 的 `wf-lint.sh`，全庫檢查由調度者在母 repo 根不帶參數跑。
- 文件裡的 ```markdown 圍籬內可能刻意放「壞」連結當測試字串；連結改寫器必須跳過 code fence。
- `youtube-audits/` 這種**目錄改名**會留正文引註殘留（`` `youtube-audits/x.md:48` ``），連結檢查抓不到，要另外 grep 舊目錄名。
- 線會把「archive 不維護內部連結」讀成「archive 不能動」而卡住 `broken=0`；交接書要明說：archive 內只准動指向現役檔的「取代者」連結。
- 名冊（ROSTER）、領地登記（line-claims）這類檔要**把規則段留在活檔**、只搬歷史條目，否則線會連規則一起封存。
- 名冊裡的「狀態」欄不可信：線收線時多半沒回填，73 格裡一堆仍寫「現役／進行中」。判準改用 `SESSION-LOG.md`／`docs/line-claims.md` 的「現役線 N 條」，交接書要直接給這個證據，否則線會「不敢猜」留一半。
- 「不搬 `logs/`」與「清指向 archive 的連結」會在同一批檔上打架；驗收命令要寫成只擋 rename／delete（`git diff --cached --name-status -M logs/ | grep -v '^M'`），不要擋 modify。
- 「`archive/` 既有內容不動」要留一個口子：**`archive/README.md` 只准追加列**，否則新封存的東西登記不進帳本。
- 線收不到跨 repo 的新佈局（對方還沒 commit）時會自己列出對映表想幫忙修——交接書明寫「跨 repo 壞連結不追、由調度者收尾」就夠，不要讓它算。
- `inbox/new/` 可能有 `.`-開頭的隱藏訊息，`ls` 看不到、驗收也數不到；用 `ls -A`。
- 線報告的「⚠ NEEDS-DISPATCHER」清單是整理的副產物，要照 [WAIT_USER](../../WAIT_USER.md) 的格式落地，不能只留在線的回報裡。

## 交接

- 完成後 → 若整理揭露了要裁示的事，[WAIT_USER](../../WAIT_USER.md) 一行；為什麼這樣分類 → [decisions](decisions.md)。
- 骨架本身要升級 → 記憶 `wf-kernel-upstream-and-upgrade`；上游 `~/repo/workflows`。
