# mod 庫帳務、暫存與清理安全

[lessons 索引](README.md)

## temp-dirs-double-as-offline-reinstall-library

> 暫存目錄實際上兼任離線重裝庫；清理前要先分「可重抓／不可重抓」，不是先分「備份／下載暫存」。

2026-10-23 全工作區大整理：使用者裁示 `~/skyrim_mods/_*` 39 夾（~13 GB）全刪並執行。事後 T5 查證發現，10-17 標 keep 的 303 個「庫內唯一原檔」**全部位於 `_dl-*` 下載暫存夾**，刪除後 300/303（9.996 GiB）全機已無第二份——下載暫存一直默默兼任著離線重裝庫，但沒有任何文件把它標成這個角色。實際損失比帳面小：81.5%（bytes 計）經 housecarl nexus 工具逐筆查證仍可從 Nexus 重抓，真正不可回復只有 2 筆 23 MB。

**Why**：「備份 vs 下載暫存」的分類答錯了問題——下載暫存裡躺著的可能是全機唯一副本，而「備份」裡的東西反而可能處處有第二份。決定可不可以刪的軸是**可回復性**，不是目錄名。

**How to apply**：清理任何暫存／下載目錄前，先對內容物回答兩個問題：(1) 全機（含 MO2 downloads、mod-library）還有沒有第二份？(2) 沒有第二份的，上游（Nexus 等）還抓不抓得到（下架／改版／登入牆）？「無第二份＋上游抓不到」的才是真不可回復，要嘛留要嘛先異地備份；其餘都可刪。查證用 housecarl_nexus_identify（md5）／housecarl_nexus_mod files=true／housecarl_nexus_search。範例查證報告：`agentctl/handoffs/home-2026-10-23/tidy/T5/REPORT.md`。


## nexus-identity-confusion-many-forms

> 名稱／摘要／縮寫／記憶都可能把不相關的 mod 誤認成同一個；判準永遠是 mod id／byte-exact／實測內容，不是字面。

2026-08-27～10-18 跨多條線反覆踩到同型坑：SCAR(72014) vs SCAR VR(89492)、SCAR vs Smooth Combat Non Combat Animation 縮寫相近但無關；DAC 縮寫同時指向三個不相關 mod；Immersive Citizens AI Overhaul(Shurah) 與 AI Overhaul(janquadrant) 目標相同機制不同。摘要行也會誤導：Shadow of Skyrim summary 寫「不用存讀檔」像「受傷不死」，讀完整 description 才知道是另一套機制；使用者記得的舊愛 mod 名字 5 筆裡 3 筆直覺是錯的。通用命名（「All in one」）要用 byte-exact＋houseCARL 反查實際 provide 的檔案才能定身分；關鍵字搜尋零命中可能是頁面標題與落地檔名完全不同（SIGMA 系列）；可選檔案的檔名甚至會跟效果方向相反（`Melana_CM_Evolve2xSlower` 實際更慢）；查無 Nexus 來源時先核對是否為上游整合包自製 patch（沒有外部來源可抓）；選版相容性要找「明確列版本＋實測回報」的檔案，不要只憑「version independent」字樣；名稱比對即使兩層正規化、門檻寧漏不誤判，仍會誤配（關鍵字誤命中 NPC 名 Lod）。

**Why:** 這些誤判來源各自獨立（頁面摘要、使用者記憶、通用命名、縮寫巧合、FOMOD 選配檔名、自動比對演算法），共同點是都繞過了「用 id/byte/內容核對」這道關卡。

**How to apply:** 認定一個 mod 的身分前一律核對 Nexus mod id，不用縮寫／頁面標題字面比對；摘要/summary/檔名只當線索不當結論，可疑時讀完整 description 或實測內容；關鍵字零命中時改用已知/反查到的 mod id 再搜一輪；`ask-status` 類「搜尋異常」優先假設是子頁/翻譯頁/命名差異，追到本體頁再判定。
source: agentctl/handoffs/done/2026-08-27/cx-dl2/HANDOFF.md:56；agentctl/handoffs/done/2026-08-27/opus-gaps/staging/recall-lost-favorites-2026-08-27.md:345,350；agentctl/handoffs/done/2026-09/home-2026-09-02/lrdl/REPORT.md:31

## library-and-ingest-bookkeeping-fields-lie

> 下載佇列／庫存索引／衍生清單的「狀態欄」常常是過期快照，不代表磁碟或 Nexus 的真實現狀；要嘛重讀檔案系統，要嘛用 id/byte/md5 核對。

2026-08-27～10：`library_hit`／`status=DOWNLOADED` 欄位不保證磁碟真的有檔；庫存檔名有兩種命名慣例，只認一種把 91 件庫存少算成 69 件；`sizeInBytes=null` 是查詢缺口不是死檔，`=0` 才是；Nexus row-name 生成的落地檔名可能跟 manifest 不同但 id/byte 仍對得上；衍生 json 候選清單可能只是 prose 的子集（25 列漏了本機已有的候選）；前置框架常手動安裝、`meta.ini` 的 `modid=0`，用 id 掃描會全部誤報未裝；就地修補已部署 ESP 不會同步回 mod-library 來源，下次自動 redeploy 會悄悄覆蓋掉修正；`MANIFEST.sha256` 要 `cat` 全檔，`head -5` 曾漏看排第 7 行的目標差點誤刪；入庫 dedupe 只比對「來源↔庫」會漏掉瀏覽器重複下載出的 `X.7z`/`X (1).7z`；無時間戳的 legacy 檔名裡的 id 不可信要 md5 回溯；判斷是不是 mod 不能只看副檔名（行為檔/BodySlide/SkyProc patcher 沒有頂層 .esp/meshes）。

**Why:** 這些欄位都是某個時間點的快照或簡化表示，產生它的流程本身有已知盲區，不會隨實際狀態自動更新。

**How to apply:** 任何「已下載／已入庫／已裝」的判定，狀態欄只當起點：核對磁碟路徑是否存在、用 mod_id+file_id+bytes 或 md5 比對、框架類前置改用目錄名+實體檔案驗證；MANIFEST 類清單一律 `cat` 不 `head`；就地改動已部署且由自動化管線管理的檔案後要馬上同步回來源層；衍生候選清單要對照 prose/README 交叉核對完整性。
source: agentctl/handoffs/done/2026-09/home-2026-09-03/lrrev/REPORT.md:191；agentctl/handoffs/done/2026-08-27/opus-gaps/_COMMON-LIMITS.md:17；mod-library/README.md:36-58

## mod-library-cleanup-tooling-constraints

> `mod-library` 的清理工具（quarantine.py／scan_mod_library.py／esp_refscan.py／verify_merge.py）都刻意或無意地留了邊界，要先摸過才能信。

2026-08-28～10-10：`quarantine.py` 不提供自由查詢選擇器，只有具名 selector，理由是「搬掉所有符合 filter 的東西正是弄丟不該丟檔案的方式」——沒有對應 selector 時寫外部腳本 `import quarantine` 注入新字典項，不改本體；隔離單位是 Mongo doc（以 sha256 為鍵），同一 sha256 多路徑會一次全搬走，無法只留現役那一份；`rm -rf` 目錄樹前要先掃有沒有被索引過的巢狀 archive，有就先 quarantine 移出；「工具解壓目錄」裡 mtime 晚於解壓內容的檔案是執行期工作狀態，要單獨備份不能整棵刪；排除集合要明確涵蓋「已經隔離過」，漏掉會把已處理項目重新選中；`scan_mod_library.py` 只統計壓縮檔，142 GB 裡有 46 GiB 解壓殘留/備份完全不在報表上，要另外 `du` 比對；重建 merge plugin 後不要只信自帶 `verify_merge.py` PASS，要用獨立讀取路徑再抽驗；`esp_refscan.py` 只吃唯一 Skyrim.esm master，多 master/NAVI 會中斷，要改走 esplib 手動查並在 REPORT 註明是工具限制。

**Why:** 這些邊界來自工具的設計取捨（寧可少做也不要誤刪）或掃描範圍的技術限制，不知道就會把「工具沒做到」誤判成「已經查過/清過」。

**How to apply:** 用 `mod-library/db/quarantine.py` 前先確認 selector 涵蓋範圍，沒有就外部注入不改本體；大量刪除前一律先掃 Mongo 索引與 mtime 時間戳；信任任何「自帶驗證腳本 PASS」或「掃描工具零結果」前，先問它的已知範圍邊界在哪。
source: agentctl/handoffs/done/2026-08-28/opus-lib-clean/STATE.md；agentctl/handoffs/done/2026-08-28/opus-lib-tidy/STATE.md

## destructive-action-safety-and-rollback-limits

> 刪除/停用類操作的「安全」要分清三件事：腳本本身有沒有保險、備份放哪裡可逆、已進場存檔的東西回滾程度有限。

2026-08-30～09-05：批次刪除腳本三道保險值得當範本——偵測 MO2/遊戲在跑就 abort、預期筆數與實際變動筆數不符就斷言失敗、真正清除前先 mv 到暫存垃圾目錄待確認能正常啟動才二次確認清掉；回滾備份放 `/tmp`（tmpfs）重開機會永久消失（Bandolier 3.2GB 真的沒了）；有 hand-placed REFR/ACHR 的 mod，「乾淨回滾」只保證安裝前停用乾淨，已進場存檔中途停用只是讓引擎忽略失去來源的 FormID，可能留 orphaned changeforms；跨時間差的刪除操作要在動手當下重讀現行狀態，不採信計畫檔舊快照；CC 內容已在本周目被存檔載入過，中途拔除可能 missing-master 警告、任務物品消失，最安全時機是下個新周目；停用但不刪的 mod 多數有用途，判能不能刪要先查下游 master 相依、再查可還原性，最後才看空間；體積異常小的下載檔先 `7z t` 實測，判壞損也不得私自換源，只能 BLOCKED；多線並行寫同一 profile repo 時「工作樹要乾淨」只能限定本線負責路徑或改單一寫者序列套用；覆寫原版 Papyrus 腳本（不吃 esp 不碰 SEQ）的任務型 mod，拔掉立即生效不需要新開局——跟「改 quest flags/SEQ」需要新周目是兩回事，先查機制再判斷風險。

**Why:** 「可以刪/可以停用」要拆成腳本執行安全、備份媒介的持久性、和已進場存檔的引擎行為三層，各自失敗模式不同。

**How to apply:** 寫刪除/大量修改腳本套這三道保險；回滾備份放非 tmpfs 的實體路徑；評估「中途拔除」風險先查該內容是否已被本周目存檔載入過、是覆寫腳本還是改 flags/SEQ；刪除前一律當下重讀現行狀態；判斷能不能刪先查下游相依與可還原性再看空間。
source: agentctl/handoffs/done/2026-08-30/purge-2026-08-30/README.md:28-31；agentctl/handoffs/done/2026-09-01/hgate-2026-09-01/bandolier/FINDINGS.md
