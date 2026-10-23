# 調度：交接書與查證

[lessons 索引](README.md)

## handoff-scope-words-expand

> 交接書裡「與 X 相關的」這類範圍詞會被線遞移展開成數十倍規模，範圍要用排除法寫死（原 type: feedback）

2026-08-29 使用者說「beyond reach 那些，與相關的，都要下載」，我在交接書寫成
「**把 `3008` 列為 requirement、或名稱／說明明確服務 Beyond Reach 的作品，
連同它們自己的中文層與 hard requirement 一起收**」。

線忠實執行，盤出 **226 件／19 GB**：本體 1 件 2.7 GB、中文層 13 件 0.08 GB，
其餘 **周邊 patch 174 件 10.2 GB ＋ requirement 33 件 4.07 GB**。
跑了兩個半小時才到 179/221，使用者說「他下載太久了」。

**兩條規則各自製造了膨脹**：

1. **「無專檔時取 current MAIN」（83 件）**——某 mod 把 BR 列為 requirement 但沒有 BR 專用檔，
   於是**整個 mod 本體被抓下來**（SWIFT SE、QUASIPC、The Mad Shaman…）。
   那些是「支援 X 的 mod」，不是「X 的東西」。它們的 hard requirement 再展開一層＝再 4 GB。
2. **「專屬頁的全部現役檔」（110 件）**——單一頁常有同一東西的多版本與變體
   （Dark Forest 一頁 6 檔 ＝ v1.0/v1.1 × Main/Main+Billboards ＝ 950 MB）。

**Why:** 線不會替我收斂範圍，它只會忠實展開。**「相關的」在依賴圖上是遞移閉包**，
每多一跳就是一個數量級。錯不在線，在我把範圍寫成「包含什麼」而不是「排除什麼」。

**How to apply:** 下載／盤點類交接書的範圍段落一律用**排除法**寫死，至少三條：

- **「僅僅支援 X 不算」**——檔名或說明必須明確服務 X，才算 X 的東西。
- **反向 requirement 只展開一跳**，被展開者自己的 requirement 不再展開。
- **同一頁多版本只取 latest**；變體超過 2 個要先發 `BLOCKED` 問。

另外**件數 gate 要跟容量 gate 並列**。這次只設了 20 GB 沒設件數，17 GB 沒觸發閘門，
但 221 件的**時間**成本才是使用者感受到的問題——容量沒爆不代表時間沒爆。
與 [[investigate-all-then-install-once]] 一致：擋住施工的常常是節奏不是權限。

2026-10-23 補：牽涉外觀修復等有風險替代方案的交接書要明寫禁止項，例如「不准借用第三人的臉/身體頂替」，否則下屬會自作主張用繞過的 fallback（`agentctl/handoffs/done/2026-09/home-2026-09-09/face4/REPORT.md:89-90`）。交接書範本也要固定一段「必用工具」，列出既有工具名＋用途——retro 回顧發現工具做出來沒人用（使用次數 0）跟有沒有寫進交接書強相關，寫了的 check_masters.py 用了 134 次（`agentctl/handoffs/done/2026-10/home-2026-10-03/retro/SUMMARY.md`）。

## handoff-must-split-no-evidence-from-negative-evidence

> 交接書的失敗處置要把「證據不足」和「證據為負」分開寫，否則線會把測不出來當成東西壞掉而回滾（原 type: feedback）

2026-09-25 cx-cnsguard：交接書第 8 步寫「第 5 或第 6 條不過 → 停用覆蓋層並回報 FAILED」。
結果線根本沒能啟動遊戲（`launch-mo2.sh --skse` 這條無人值守路徑的已知毛病），
於是「沒有新 log」被判成第 5、6 條不過，它就把裝好的補丁停用了。

**Why**：補丁其實完全正常——頂層重新啟用後由使用者自己啟動，一次就驗過
（`01000020` → `01000030` loaded correctly，外掛總數 130 不變）。白繞一圈。

**How to apply**：驗收條款寫死時，失敗處置要分兩路——
「跑出來的結果是錯的」才回滾；「沒跑成、拿不到證據」是 `BLOCKED`，保持現狀等指示。
線本身的判斷是對的（它拒絕拿舊 log 冒充、也不生假的 `skse64-after.log`），錯的是我的契約。

另：**無人值守啟動 Skyrim 不可靠，不要為了驗收去修它**。使用者反正要開遊戲，
讓他開到主選單就好——SKSE 在主選單出現前就寫完 log，不必退出、不必重開。

相關：[[leads-must-not-end-turn-to-wait]]、[[verify-game-alive-via-qa-not-ps]]、[[launch-skyrim-via-steam]]

2026-10-23 補：同一類「先查根因再動手」的案例——覆核線報「差 35 件」，逐條查完全是契約文字缺漏（規則寫進個別工人交接書卻沒補回共用 CONTRACT），不是資料錯；先判「資料錯」還是「契約漏寫」再動手，否則會把三條正確規則刪掉（`agentctl/handoffs/done/2026-09-02/lorerim-2026-09-02/team-borrow/REPORT.md:54-67`）。同理，使用者裁示附帶的理由若可查證（如「因為沒買十週年版」），要查證後改寫成事實，不能照抄使用者口述的錯誤前提，裁示本身仍照辦（`agentctl/handoffs/done/2026-08-29/cx-ruling/HANDOFF.md:20`）。

2026-10-23 補：多線精簡文件時若發現文件互相矛盾（同一事實兩種說法），一律不自己選邊，記進共用 CONFLICTS.md 交回裁決（`agentctl/handoffs/done/2026-08-29/doc-refactor/CONFLICTS.md`）；調查卡在唯讀鐵律但答案需要遊戲內才能讀到時，直接在 REPORT 給使用者 1–2 步零風險操作與判讀方式，不要把缺口留給下一輪重查（`agentctl/handoffs/done/2026-10/home-2026-10-07/meleeslow/REPORT-accum.md`）。

## verify-waituser-against-logs

> WAIT_USER/SESSION-LOG 會落後於實際進度;派線前先查 agentctl/logs/ 與 inbox/done/ 有沒有同名線做過（原 type: feedback）

`WAIT_USER.md`／`wait-user/*.md`／`SESSION-LOG.md` 標的 open 項可能已經被前一條線做完但沒清。
派線前先掃 `agentctl/logs/`、`agentctl/inbox/done/`、`agentctl/handoffs/done/` 有沒有同名或同主題的線，
再看實體產物（檔案是否真的在 `~/skyrim_mods/hdd/`、bytes 對不對），才決定要不要派。

**Why:** 2026-08-25 依 `wait-user/home-setup.md` 規劃了「EnaiRim Batch 0 五件 Nexus 下載」整條線，
講完計畫才發現 2026-08-24 的 `enairim-b0-dl` 線早就做完並回報 DONE、五件都在庫裡。
差一步就整晚重跑已完成的工作，而且是使用者稀缺的在家時段。

**How to apply:** 收線時同步清掉對應的 WAIT_USER 項（見 [[im-dispatcher-codex-implements]] 的收線流程）。
派線前的查證用 sonnet subagent 背景跑就好，見 [[delegate-simple-work-to-sonnet]]。

2026-10-23 補：線要被後續彙整線看見，第一步就要在 ROSTER.md 登記並至少發一則 inbox PROGRESS/DONE，否則它的「收線自述」會永久遺失，只能靠事後讀檔反推（`agentctl/handoffs/done/2026-08-28/opus-zh-summary/SUMMARY.md:579-596`）。開新團隊前先查 `inbox/teams/` 有沒有同名未關閉的舊隊，有的話先 close 再建，隊名不是依日期自動隔離的（`agentctl/handoffs/done/2026-09/home-2026-09-02/wrap/REPORT.md:29`）。


## dont-trust-subordinate-self-report-verify-yourself

> 下屬自報「檢查通過」「已完成」不能直接採信，收線要重算或要可查證依據

2026-08-27 某線自報連結檢查通過，上游重跑同一腳本才抓出 9 條斷鏈（`agentctl/handoffs/done/2026-08-27/opus-gaps/_COMMON-LIMITS.md:29`）。2026-09-08 face 線逐層清點才發現 7 層自報「已內化」其實仍依賴素材 mod（`agentctl/handoffs/done/2026-09/home-2026-09-08/face/REPORT.md:105`）。同類坑：`FAILED-not-started` 只是未開始非真失敗；沒收終局訊息也可能是延遲非沒做完；領隊自稱「使用者說過 X」同樣不算數。

**Why:** 自報天生帶偏差，謊報誤報不會自動被攔下。

**How to apply:** 能重算的一律重算（連結、資產內化、批次統計），不能重算的查可驗證來源；見 [[verify-waituser-against-logs]]。


## cite-by-anchor-not-line-number

> 證據表／交接書引用檔案要用錨點字串定位，不能寫死行號——別線同時在改會讓行號整批漂移

2026-09-02 lead-lrgap 引用的現役檔被別線同時在改，行號位移兩次，80 列證據全漂掉（`agentctl/handoffs/done/2026-09-02/lorerim-2026-09-02/team-gap/REPORT.md:46-63`）；09-03 old 隊的部署包同因 profile 檔被別線同改而行號失真（`agentctl/handoffs/done/2026-09/home-2026-09-03/old/REPORT.md:52`）。另一面：覆核發現領隊把跨行複合敘述塞一欄只引一行，被引行自己證不了主張。

**Why:** 行號只是快照，多線同寫一檔必漂移；複合敘述硬塞一行會讓審計者查不到依據。

**How to apply:** 證據表附錨點重定位腳本、commit 前再跑一次；每列主張要能被所引那一行單獨證實，跨行脈絡移進備註欄。


## dont-hardcode-mutable-snapshot-values

> 驗收斷言、共用計數表若寫死被裁示改變的快照值，值一變就連環 BLOCKED

2026-09-01 兩線同改一張計數表，改成「開工當下讀到數字加減，不寫目標值」解掉衝突（`agentctl/handoffs/done/2026-09-01/cx-land-plan/HANDOFF.md:55-57`）。同類坑：09-03 dl 隊驗收寫死「件數分佈 10/5/12」，裁示多收 4 件變 14/1/12 後連環 BLOCKED（`agentctl/handoffs/done/2026-09/home-2026-09-03/dl/REPORT.md:133`）；inst 隊把「sha256 不變」寫成建包常數，多包套用同一 profile 時前包已改過，直接 FAIL（`inst/REPORT.md:94`）。

**Why:** 分佈／aux sha／計數表都是會被裁示或別線改動的活值，寫死常數等於賭它不變。

**How to apply:** 驗收只斷言總數與集合完整性；aux「未變」當下重算；計數表給增減量不給目標值。
