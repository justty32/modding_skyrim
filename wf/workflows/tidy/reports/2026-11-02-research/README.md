# 2026-11-02：CHIM 與 AI 世界上下文研究收尾

範圍只含今日新增研究與必要導航、狀態入口；沒有重構其他研究、產品程式、部署或歷史證據。長期結論仍在 analysis，不複製到 handoff；CHIM 借鑑留待以後，Living 仍回家參考 FDE Janessa 後再決定，研究候選不是開工授權。

Done when: 五段 CHIM 原文與六條 AI 分篇路由完成責任拆分，原入口／錨點仍可達；來源與 53 組資料不變；下列八項固定檢查有結果，獨立 review 通過後依子 repo→母 repo 順序收線。

## 盤點與拆法

CHIM 原 modforge-fit.md 為 8746 bytes，混合「既有能力／不擴張邊界」與「一般出貨管線候選／驗收」兩種消費用途。前者移到同名資料夾 README，後者集中 output-gates.md，三候選共用 staging／驗收／發布責任，沒有再切成三份小檔。原路徑保留結論與全部五個舊二級標題，逐節指向原文新位置。

[段落對映 moves.tsv](moves.tsv) 有五筆帶 fragment 的舊→新位置；這是部分內容拆分，原檔仍存在，沒有整檔搬移或刪除。來源已由 51c4700／ce3fa60 保存並推送；新檔明確 add。不能把段落對映當整檔搬移套用 fix_moved_links；所有原入站路徑與 fragment 保留有效。

AI 世界上下文原已有六篇責任清楚的正文與三份資料矩陣，缺少同名資料夾入口。六條閱讀路由整段移到 README；原入口只連下一層索引。通則與 bridge 本地限制／驗收的重疊有不同用途，保留；Mantella 8187 bytes、MinAI 8103 bytes 維持完整採集→consumer 鏈，不按字數切成薄頁。六篇正文與三 JSON 全部 byte-identical。

沒有過時歷史需要刪除，故本批不做內容精簡、不新增封存；沒有改日期、使用者原話、版本、技術限制或候選狀態。既有封存與其他 dirty reference clones 均不處理。

## 八項固定檢查

### 1. 段落、引用與資料保全

以 ce3fa60 為來源，逐段將相對 Markdown 目標解析成相同 repo 相對路徑後比較內容與 SHA-256；五段均須相同，入口原結論仍保留。唯一必要文字例外是將「下文第二、三項」改為連到出貨驗收候選的「第二、三項」；比較時只對這一處指示詞正規化，避免拆檔後仍誤指本頁下文。CHIM 外部 URL multiset 須相同；AI 六分篇與三 JSON 須逐 byte 相同，tabledb 列數仍為 14／22／17。六條閱讀路由須保留同標籤與同解析目標。

### 2. 舊錨點與入站

舊五個二級標題原文保留；新版各轉向目標錨點須存在。原路徑未消失，既有入站不用改指；以變更 Markdown 檢查器與原錨點集合核對。

### 3. 本批 Markdown 連結

明確列入新舊研究入口、分篇 README、整理報告與報告索引、STATE／NEXT；不得只靠 tracked 清單漏掉新增檔。全部本地檔案與 fragment 須通過。

### 4. 大小、資料契約與大清單

研究範圍活 Markdown 不超過 8192 bytes，新增 README 不超過 100 行。三矩陣以 tabledb check 驗證；find_big_lists 掃正文與新報告，不得新增需抽出的同質大表。人用閱讀導航保留 Markdown。

### 5. 全庫連結前後基線

在 repo 根不帶參數各跑一次 check_markdown_links，before 完成前不改工作樹；after 包含新增報告與導航。只接受同七條既存 missing-file links，新增為零，不為全綠而擴修歷史。

### 6. 差異與邊界

母 repo 與 agentctl 的 diff check 須通過；diff 只含指定研究結構、報告／導航、今日 STATE／NEXT 與必要 pin。六篇正文、三 JSON、產品程式、部署和封存均不變。

### 7. 活狀態與 WAIT_USER

開始即登記母 SESSION open，完成刪除；STATE／NEXT 只補正本短指標。WAIT_USER count check 維持 33（6／12／13／2／0），不把研究候選新增為使用者驗收。

### 8. 獨立 review 與遠端收線

獨立 review 核原意、pin、來源邊界、資料保全及導航後，使用 scoped wrap helpers 只收明確檔案。先 commit／push agentctl，再 commit 母 repo 研究／報告與 pin；最後確認兩 repo 與各自 upstream 的 ahead／behind 均為 0／0。

## 驗證結果

獨立 review **PASS**，確認原意、來源固定版本、觀測／推論與 QA／正式玩法邊界，以及僅一處位置指涉修正。五段正文正規化比較通過（合併 SHA-256 `f3c03c8e85f5e1c977711f6a9a72d1eef2d5ec96341b110c83aaab28e08460d7`），CHIM 8 個外部引用不變；AI 六正文、三矩陣逐 byte 相同，53 組資料與固定 pin 均保留，閱讀路由標籤／解析目標相同。

CHIM 原 8746 bytes 拆為入口 1109、已有能力／邊界 3289、出貨候選 5732 bytes；AI 原入口 5101→4551，新增索引 1260 bytes。研究範圍 Markdown 均不超過 8192 bytes；新增 README 均低於 100 行。大清單掃描為 0，三份 tabledb check 均為空壞鏈清單。

全庫 before **5832** 檔、after **5836** 檔（含四個新增 Markdown），均是相同七條既存 missing-file links，missing anchors 為 0，新增斷鏈為 0。檢查器因此仍回非零，不能稱全庫全綠；範圍外歷史／成品斷鏈未改。本批明確路徑 Markdown 檢查及位置指涉修正後補驗均通過；兩 repo diff check、WAIT_USER 33 項核對通過。

母 SESSION 的臨時 open 完成即移除，STATE／NEXT 只加研究正本短指標。產品程式未變，不重跑已完成的 136／530／1337 產品測試。收線使用 scoped wrap helpers，遠端 ahead／behind 由收工輸出終局核對。
