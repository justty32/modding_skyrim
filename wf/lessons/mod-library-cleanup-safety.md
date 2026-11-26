# mod 庫清理與刪除安全

[lessons 索引](README.md)

身分辨識與帳務欄位可信度在 [mod-library-bookkeeping](mod-library-bookkeeping.md)。

## temp-dirs-double-as-offline-reinstall-library

> 暫存目錄實際上兼任離線重裝庫；清理前要先分「可重抓／不可重抓」，不是先分「備份／下載暫存」。

2026-10-23 查證：標 keep 的「庫內唯一原檔」全部位於 `_dl-*` 下載暫存夾——下載暫存默默兼任離線重裝庫，而「備份」裡的東西反而可能處處有第二份。決定可不可以刪的軸是**可回復性**，不是目錄名。

**How to apply**：清理任何暫存／下載目錄前，先對內容物回答兩個問題：(1) 全機（含 MO2 downloads、mod-library）還有沒有第二份？(2) 沒有第二份的，上游（Nexus 等）還抓不抓得到（下架／改版／登入牆）？「無第二份＋上游抓不到」的才是真不可回復，要嘛留要嘛先異地備份；其餘都可刪。查證用 housecarl_nexus_identify（md5）／housecarl_nexus_mod files=true／housecarl_nexus_search。範例報告：`agentctl/handoffs/home-2026-10-23/tidy/T5/REPORT.md`。

## mod-library-cleanup-tooling-constraints

> `mod-library` 的清理工具（quarantine.py／scan_mod_library.py／esp_refscan.py／verify_merge.py）都刻意或無意地留了邊界，要先摸過才能信。

`mod-library/db/quarantine.py` 只有具名 selector、不提供自由查詢（「搬掉所有符合 filter 的東西正是弄丟不該丟檔案的方式」）——沒有對應 selector 就寫外部腳本 `import quarantine` 注入新字典項，不改本體；隔離單位是以 sha256 為鍵的 Mongo doc，同一 sha256 多路徑會一次全搬走，無法只留現役那一份；排除集合要明確涵蓋「已經隔離過」，漏掉會把已處理項目重新選中。`rm -rf` 目錄樹前先掃有沒有被索引過的巢狀 archive，有就先 quarantine 移出；「工具解壓目錄」裡 mtime 晚於解壓內容的檔案是執行期工作狀態，要單獨備份不能整棵刪。`scan_mod_library.py` 只統計壓縮檔，解壓殘留／備份（可達數十 GiB）不在報表上，要另外 `du`。重建 merge plugin 後不要只信自帶 `verify_merge.py` PASS，用獨立讀取路徑再抽驗。`esp_refscan.py` 只吃唯一 Skyrim.esm master，多 master/NAVI 會中斷，改走 esplib 手動查並在 REPORT 註明是工具限制。

**How to apply:** 信任任何「自帶驗證腳本 PASS」或「掃描工具零結果」前，先問它的已知範圍邊界在哪；大量刪除前一律先掃 Mongo 索引與 mtime。
source: agentctl/handoffs/done/2026-08-28/opus-lib-clean/STATE.md；agentctl/handoffs/done/2026-08-28/opus-lib-tidy/STATE.md

## version-compare-must-abstain-not-guess

> 版本號比較沒有單一安全讀法，遇到矛盾要回「無法判定」；None（不適用）與 False（確認為否）不能當同一布林

`mod-library/db/cleanup_report.py` 實測（2026-08-28）：單用 10 位 unix timestamp 排序，會把帶日期字串、無 timestamp 的新式命名判成 ts=0=最舊；整數 tuple 讀法在位數不一致時判反（`6817 KS Hairdos SSE` 1.9 vs 1.10、`77566 Civil War Lines Expansion` 1.06 vs 1.1）。閘門 `runtime_ok_1_6_1170 is True` 把 None（不含 SKSE dll，不適用）與 False（已知不相容）混為一談，閘門永遠 0 筆，被誤讀成「庫裡沒有舊版本」。

**How to apply:** 版本比較函式遇 qualifier 不同、位數矛盾要明確回傳「無法判定」，呼叫端把 None 當整組不動，不賭方向；拿 KS Hairdos／Civil War Lines Expansion 當回歸測試案例。過濾／分級腳本的 None 與 False 分開判；某閘門長期 0 筆候選時先懷疑閘門語意，不要直接採信「真的沒有」。

## destructive-action-safety-and-rollback-limits

> 刪除/停用類操作的「安全」要分清三件事：腳本本身有沒有保險、備份放哪裡可逆、已進場存檔的東西回滾程度有限。

**腳本保險**（範本）：偵測 MO2／遊戲在跑就 abort；預期筆數與實際變動筆數不符就斷言失敗；真正清除前先 mv 到暫存垃圾目錄，確認能正常啟動才二次確認清掉。跨時間差的刪除要在動手當下重讀現行狀態，不採信計畫檔舊快照。多線並行寫同一 profile repo 時「工作樹要乾淨」只能限定本線負責路徑，或改單一寫者序列套用。

**備份媒介**：回滾備份放非 tmpfs 的實體路徑，`/tmp` 重開機會永久消失。

**已進場存檔**：有 hand-placed REFR/ACHR 的 mod，「乾淨回滾」只保證安裝前停用乾淨，存檔中途停用只是讓引擎忽略失去來源的 FormID，可能留 orphaned changeforms；本周目載入過的 CC 內容中途拔除可能 missing-master 警告、任務物品消失，最安全是下個新周目。覆寫原版 Papyrus 腳本（不吃 esp 不碰 SEQ）的任務型 mod 拔掉立即生效不需新開局，跟「改 quest flags/SEQ」要新周目是兩回事，先查機制再判風險。

**判能不能刪**：停用但不刪的 mod 多數有用途，先查下游 master 相依、再查可還原性，最後才看空間。體積異常小的下載檔先 `7z t` 實測，判壞損也不得私自換源，只能 BLOCKED。
source: agentctl/handoffs/done/2026-08-30/purge-2026-08-30/README.md:28-31；agentctl/handoffs/done/2026-09-01/hgate-2026-09-01/bandolier/FINDINGS.md

## unadopted-archive-check-installed-version-and-variant

> 「沒採用的調查包」刪前要逐包對照已裝層的版本與變體；同一 mod 的較新版或另一變體看起來像調查殘留，其實可能是已裝 mod 的唯一來源包

2026-11-22 例：判為未採用的 Feris 1.4.3、Lyra Master 1.0.0.6，刪前查到現役 Feris 層是 1.4.2、Lyra 現役是 **Lite** 變體，才確認兩包都不是已裝層來源（重抓編號 Nexus 142226#841761、179416#749742；[dl-intake REPORT](../../agentctl/handoffs/home-2026-11-22/dl-intake/REPORT.md) §5）。若版本或變體剛好相同，刪掉的就是已裝 mod 唯一能重裝的來源。判斷依據是已裝層 `meta.ini` 的 `installationFile`／版本欄與 MO2 層名，不是哪條線下載的。

**How to apply:** 刪下載包前列出每包的 Nexus `mod#file`、版本、變體（Lite／Master、CBBE／3BA 等），對 `modlist.txt` 啟用層與各層 `meta.ini`（`installationFile`、`version`；`installationFile` 指向不存在的路徑也要記下）比對；同 mod 不同版或不同變體要寫明「不是已裝層來源」的證據；刪前記下重抓編號；永久刪除走二段（先 trash＋sha256 核對，再在使用者面前清）。
source: agentctl/handoffs/home-2026-11-22/dl-intake/REPORT.md；agentctl/handoffs/home-2026-11-22/last-wrap/REPORT.md
