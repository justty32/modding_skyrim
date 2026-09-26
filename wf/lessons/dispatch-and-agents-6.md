# 調度、模型分級與交接書（6/9）

[lessons 索引](README.md)｜同主題：[dispatch-and-agents](dispatch-and-agents.md)、[dispatch-and-agents-2](dispatch-and-agents-2.md)、[dispatch-and-agents-3](dispatch-and-agents-3.md)、[dispatch-and-agents-4](dispatch-and-agents-4.md)、[dispatch-and-agents-5](dispatch-and-agents-5.md)、[dispatch-and-agents-7](dispatch-and-agents-7.md)、[dispatch-and-agents-8](dispatch-and-agents-8.md)、[dispatch-and-agents-9](dispatch-and-agents-9.md)

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
