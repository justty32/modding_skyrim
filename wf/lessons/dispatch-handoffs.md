# 調度：交接書

[lessons 索引](README.md)｜收線查證與報告證據見 [dispatch-evidence-and-reports](dispatch-evidence-and-reports.md)

## handoff-scope-words-expand

> 交接書裡「與 X 相關的」這類範圍詞會被線遞移展開成數十倍規模，範圍要用排除法寫死

2026-08-29 使用者說「beyond reach 那些，與相關的，都要下載」，交接書寫成「列為 requirement、或名稱／說明明確服務 X 的作品，連同它們的中文層與 hard requirement 一起收」；線盤出 226 件／19 GB（本體與中文層只佔 3 GB），使用者說「他下載太久了」。膨脹來自兩條規則：「無專檔時取 current MAIN」把「支援 X 的 mod」整個本體抓下來、再展開它們的 requirement；「專屬頁的全部現役檔」把一頁的多版本 × 多變體全收。

**Why:** 線不會替我收斂範圍，只會忠實展開；「相關的」在依賴圖上是遞移閉包，每多一跳一個數量級。錯在把範圍寫成「包含什麼」而不是「排除什麼」。

**How to apply:** 下載／盤點類交接書的範圍一律用**排除法**寫死，至少三條：
- **「僅僅支援 X 不算」**——檔名或說明必須明確服務 X。
- **反向 requirement 只展開一跳**，被展開者自己的 requirement 不再展開。
- **同一頁多版本只取 latest**；變體超過 2 個先發 `BLOCKED` 問。

**件數 gate 與容量 gate 並列**：只設容量時，件數帶來的時間成本才是使用者感受到的問題。與 [[investigate-all-then-install-once]] 一致。

有風險替代方案的交接書（如外觀修復）要明寫禁止項，例如「不准借用第三人的臉/身體頂替」，否則下屬會自作主張用繞過的 fallback（`agentctl/handoffs/done/2026-09/home-2026-09-09/face4/REPORT.md:89-90`）。交接書固定一段「必用工具」列既有工具名＋用途：工具有沒有被用跟有沒有寫進交接書強相關（2026-10-23，`agentctl/handoffs/done/2026-10/home-2026-10-03/retro/SUMMARY.md`）。

## handoff-must-split-no-evidence-from-negative-evidence

> 交接書的失敗處置要把「證據不足」和「證據為負」分開寫，否則線會把測不出來當成東西壞掉而回滾

2026-09-25：交接書寫「第 5 或第 6 條不過 → 停用覆蓋層並回報 FAILED」，線沒能無人值守啟動遊戲、「沒有新 log」被判成不過，就把其實正常的補丁停用了。

**Why:** 測不出來不等於壞掉；契約沒分兩路，線只能照字面回滾。

**How to apply:**
- 失敗處置分兩路：「跑出來的結果是錯的」才回滾；「沒跑成、拿不到證據」是 `BLOCKED`，保持現狀等指示。
- **無人值守啟動 Skyrim 不可靠，不要為了驗收去修它**：讓使用者開到主選單就好——SKSE 在主選單出現前就寫完 log，不必退出重開。

同一類「先查根因再動手」：

- 覆核線報數量對不上時，先判「資料錯」還是「契約漏寫」（規則寫進個別工人交接書卻沒補回共用 CONTRACT）再動手，否則會把正確規則刪掉（`agentctl/handoffs/done/2026-09-02/lorerim-2026-09-02/team-borrow/REPORT.md:54-67`）。
- 使用者裁示附帶的理由若可查證（如「因為沒買十週年版」），查證後改寫成事實，不照抄口述的錯誤前提；裁示本身仍照辦（`agentctl/handoffs/done/2026-08-29/cx-ruling/HANDOFF.md:20`）。
- 多線精簡文件時發現文件互相矛盾，不自己選邊，記進共用 CONFLICTS.md 交回裁決（`agentctl/handoffs/done/2026-08-29/doc-refactor/CONFLICTS.md`）。
- 調查卡在唯讀鐵律但答案要進遊戲才讀得到時，直接在 REPORT 給使用者 1–2 步零風險操作與判讀方式，不留給下一輪重查（`agentctl/handoffs/done/2026-10/home-2026-10-07/meleeslow/REPORT-accum.md`）。

相關：[[leads-must-not-end-turn-to-wait]]、[[verify-game-alive-via-qa-not-ps]]、[[launch-skyrim-via-steam]]

## verify-waituser-against-logs

> WAIT_USER/SESSION-LOG 會落後於進度；派線前先核完成證據，過期路徑由 git history 取回

`WAIT_USER.md`／`wait-user/*.md`／`SESSION-LOG.md` 標的 open 項可能已被前一條線做完但沒清（2026-08-25 差點整晚重跑已完成的下載線）。

**How to apply:**
- 派線前先掃現役信箱／handoffs 與 git history 有沒有同名或同主題的線，再看實體產物（檔案是否真的在 `~/skyrim_mods/hdd/`、bytes 對不對）才決定派不派；這種查證交 sonnet 背景跑（[[delegate-simple-work-to-sonnet]]）。收線時同步清掉對應的 WAIT_USER 項。
- 線要被後續彙整線看見，第一步就要登記（ROSTER／claims）並至少發一則 PROGRESS／DONE，否則它的收線自述會永久遺失（`agentctl/handoffs/done/2026-08-28/opus-zh-summary/SUMMARY.md:579-596`）。
- 開新團隊前先查有沒有同名未關閉的舊隊，有就先 close 再建；隊名不會依日期自動隔離（`agentctl/handoffs/done/2026-09/home-2026-09-02/wrap/REPORT.md:29`）。

## oral-dispatch-brief-must-follow-template

> 頂層口頭派的線，存檔時 BRIEF 也要照 `agentctl/templates/BRIEF.md` 分段；否則 pre-commit 的 `brief_lint --strict` 擋下 commit，存檔線要回頭逐份補段

2026-11-22（[checkpoint-2 REPORT](../../agentctl/handoffs/home-2026-11-22/checkpoint-2/REPORT.md)）：派線原文直接存檔的 BRIEF 常缺「必用工具」表、件數／容量 gate、交付絕對路徑、鎖與遊戲三選一。hook 只看檔案結構，補段拖到存檔線就得逐份重讀原文、容易卡住（[[checkpoint-line-silent-stall]]）。

**How to apply:** 派線訊息裡就寫「照範本分段存成 BRIEF 並過 `brief_lint --strict`」，由該線開工第一步自己做（BRIEF 開頭加一行「依派線原文照範本分段，不改原意」，例：[cleanup-temp BRIEF](../../agentctl/handoffs/home-2026-11-22/cleanup-temp/BRIEF.md)）；頂層直接寫檔時也照範本。原文照留，只補必填段。

## brief-conflicting-gates-need-an-exit

> 交接書的兩條限制互相衝突（「什麼都不刪」對上容量 gate、件數上限對上「整夾刪」），又沒給出路時，線會自己選一邊偏離；寫 BRIEF 時先對一遍限制有沒有互斥，互斥就寫明優先序或出路

2026-11-22 的偏離（都已自首；證據在各線 REPORT：`bodyslide-morph-build` §8、`body-fit`「刪除」段、`face-loop`、[cleanup-temp REPORT](../../agentctl/handoffs/home-2026-11-22/cleanup-temp/REPORT.md)「異常與偏差」）：為守容量 gate 刪了自己建的可重產物、違反「連自己的暫存也不刪」；`pkill -f` 比對到自己的驅動腳本；被 `.git` 保險擋下後把一個夾拆成多個兄弟項、超過自訂件數上限。線不會停下來問，會挑一條自己覺得較重要的照做再揭露；偏離是 BRIEF 造成的。

**How to apply:**
- 寫完 BRIEF 對一遍：容量 gate 與「不刪」、件數 gate 與「整夾處理」、「刪 X」與「不能斷 Y」有沒有互斥；有就寫「衝突時以 A 為準，B 改成 …（例：舊草稿改名保留、超過就停下回報）」。
- 計數 gate 寫明單位（「頂層目錄」還是「刪除腳本的目標行」），並給拆分後的處置。
- 殺行程只准 `kill <自己記下的 pid>`；`pkill`／`killall` 在 BRIEF 明文禁止。
- 派結案線：「結案項直接刪」與「不改歷史報告」互斥，被刪子檔／錨點若有舊場次夾連著就只能留斷鏈。BRIEF 先給出路：准把那些連結改成不可點的「（<日期> 結案後刪除，見 git 歷史）」，或等場次夾到期一起刪。
