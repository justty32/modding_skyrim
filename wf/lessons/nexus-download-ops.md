# Nexus 下載自動化

[lessons 索引](README.md)

CDP 驅動的 Nexus Mods 下載自動化踩過的坑：頁面判定、下載完成判準、並行控制。

## nexus-download-manager-only-and-dom-byte-verify-gotchas

> cdp-download 自動化累積坑：manager-only 頁面沒有手動下載鈕；多 MAIN 檔會誤點隱藏 modal；expected_bytes=null 被當 0 誤判超時；>500MB 多一層 Standard/Resumable 對話框；file_id 會被 Nexus 從 URL 拿掉

2026-08-27～08-30 四條下載線（cx-dl2／cx-dl6／cx-dl7／dl-2026-08-30）踩出同組坑：manager-only mod 頁面根本沒有 Manual download 鈕，重試無意義，先用 houseCARL 查該 mod 是否關閉 direct download；多 MAIN 檔時第二層點擊可能誤點隱藏 modal 抓錯檔，要用 API 回傳 bytes 核對下載結果；`expected_bytes=null` 被 `Number(null)=0` 誤判超時，完成判準改用「大小穩定一段時間＋無 `.crdownload`」；>500MB 多跳一層 Standard/Resumable 選框要選 Standard；點 FILES 後 URL 的 `file_id` 會被拿掉，fallback 要改選可見 DOM 列，落地檔名用瀏覽器 `suggestedFilename` 不要硬比對 expected_filename。

**Why:** Nexus 頁面在新舊 DOM、多檔案、大檔案、關閉直接下載四種情境行為都不同，單一判準會在某情境靜默失敗或抓錯檔。

**How to apply:** 新下載線先讀 `agentctl/handoffs/done/2026-08-27/cx-dl2/tools/KNOWN-ISSUES.md`；完成判準用「大小穩定＋無 .crdownload」；下載後用 `nexus_identify`（MD5）核實身分；遇 manager-only 先查再排程、不要重試。

2026-10-23 補：manager-only 旗標本身不是「下載必失敗」的判別因子——09-05 已證 155 件全標此旗標、68 件照樣成功，09-11 kurone 再驗 15/15 全成功（`agentctl/handoffs/done/2026-09/home-2026-09-11/kurone/REPORT.md:57-59`）。規劃批次時不要因它排除候選，照常排進既有 CDP／Manual 流程實測。

## nexus-concurrent-downloads-must-serialize

> 多條線同時呼叫 nexus_get.sh 下載會互搶同一個 Chrome profile 複本，全部 timeout

2026-10-08 want 線 b、d 兩條平行呼叫 `nexus_get.sh --batch` 同時失敗在「timeout waiting for download start」，判斷是共用同一份 Chrome profile 複本工具互相干擾；後續 BRIEF 明文要求序列化。

**Why:** `nexus_get.sh` 走單一 Chrome profile 複本（見 [[agent-driven-nexus-download]]），本質是獨佔資源，平行呼叫等同兩個 agent 搶同一個瀏覽器視窗。

**How to apply:** 派多條線同時做 Nexus 下載任務時，交接書要明文規定序列化（一次一個 session 用 `nexus_get.sh`），不要假設批次下載可以平行跑。

## nexus-fileid-and-uploader-graphql-pinning

> 批次下載釘版本用 GraphQL modFiles 查 file_id，盤點作者全集用 uploaderId filter——都別靠檔名或關鍵字猜

2026-09-11 kurone／dl2 兩線實證：下載新版或多版本 mod 時，先用 `housecarl_nexus_graphql` 的 modFiles 查詢把目標版本的精確 file_id 釘死再餵下載器，dl2 六件＋kurone 十五件 0 抓錯版（`agentctl/handoffs/done/2026-09/home-2026-09-11/kurone/REPORT.md:40-41`）。盤點某作者全部作品時關鍵字搜尋會混進別人的漢化／衍生（關鍵字撈 86 筆混雜），改用 `housecarl_nexus_mod` 取 uploader.memberId 再用 GraphQL `mods(filter:{uploaderId,gameId})` 查，精準得 29 支全集；盲區剩分身帳號、已下架、LE/AE 分開上架（同報告:63-66）。

**Why:** 檔名／版本字串／關鍵字都是人寫的表面層，file_id 與 uploaderId 才是 Nexus 的主鍵。

**How to apply:** 批次下載前一律先 modFiles 釘 file_id，下載器吃 file_id 不吃檔名；「某作者全部作品」類盤點一律走 uploaderId filter，不拿關鍵字結果當權威清單。
