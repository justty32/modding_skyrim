# mod 庫帳務：身分辨識與欄位可信度

[lessons 索引](README.md)

暫存可回復性、清理工具邊界、版本比較與刪除安全在 [mod-library-cleanup-safety](mod-library-cleanup-safety.md)。

## nexus-identity-confusion-many-forms

> 名稱／摘要／縮寫／記憶都可能把不相關的 mod 誤認成同一個；判準永遠是 mod id／byte-exact／實測內容，不是字面。

2026-08-27～10-18 多線反覆踩到：縮寫相近但無關（SCAR(72014) vs SCAR VR(89492) vs Smooth Combat Non Combat Animation；DAC 同時指三個 mod）；目標相同機制不同（Immersive Citizens AI Overhaul vs AI Overhaul）；summary 行誤導（Shadow of Skyrim summary 寫「不用存讀檔」像「受傷不死」，讀完整 description 才知道是另一套機制）；使用者記得的舊愛 mod 名字常是錯的；通用命名（「All in one」）；頁面標題與落地檔名完全不同（SIGMA 系列，關鍵字零命中）；可選檔名跟效果方向相反（`Melana_CM_Evolve2xSlower` 實際更慢）；名稱自動比對寧漏不誤判仍會誤配（關鍵字誤命中 NPC 名 Lod）。meta.ini 的 modid 可能因頁面遷移跟下載檔 id 對不上，兩個 id 都要查一次確認同一個 mod。

**How to apply:** 認定 mod 身分一律核對 Nexus mod id，不用縮寫／頁面標題字面比對；通用命名用 byte-exact＋houseCARL 反查實際 provide 的檔案定身分；摘要／檔名只當線索，可疑時讀完整 description 或實測內容；關鍵字零命中時改用已知／反查到的 mod id 再搜一輪；`ask-status` 類「搜尋異常」優先假設是子頁／翻譯頁／命名差異，追到本體頁再判；查無 Nexus 來源時先核對是否為上游整合包自製 patch；選版相容性找「明確列版本＋實測回報」的檔，不只憑「version independent」字樣。
source: agentctl/handoffs/done/2026-08-27/cx-dl2/HANDOFF.md:56；agentctl/handoffs/done/2026-08-27/opus-gaps/staging/recall-lost-favorites-2026-08-27.md:345,350；agentctl/handoffs/done/2026-09/home-2026-09-02/lrdl/REPORT.md:31

## library-and-ingest-bookkeeping-fields-lie

> 下載佇列／庫存索引／衍生清單的「狀態欄」常常是過期快照，不代表磁碟或 Nexus 的真實現狀；要嘛重讀檔案系統，要嘛用 id/byte/md5 核對。

2026-08-27～10 命中：`library_hit`／`status=DOWNLOADED` 不保證磁碟真的有檔；庫存檔名有兩種命名慣例，只認一種會少算；Nexus row-name 生成的落地檔名可能跟 manifest 不同但 id/byte 仍對得上；衍生 json 候選清單可能只是 prose 的子集；前置框架常手動安裝、`meta.ini` 的 `modid=0`，用 id 掃描會全部誤報未裝；無時間戳的 legacy 檔名裡的 id 不可信要 md5 回溯；判斷是不是 mod 不能只看副檔名（行為檔／BodySlide／SkyProc patcher 沒有頂層 .esp/meshes）。入庫 dedupe 只比對「來源↔庫」會漏掉瀏覽器重複下載出的 `X.7z`/`X (1).7z`；反過來 `nexus_intake_check.py dedupe` 常把自己的 `_dl-*` 下載暫存誤判成庫內重複，是已知路徑衝突不是真重複。`sizeInBytes=null` 的判法見 [[housecarl-nexus-api-field-quirks]]。

**How to apply:** 「已下載／已入庫／已裝」的判定，狀態欄只當起點：核對磁碟路徑、用 mod_id+file_id+bytes 或 md5 比對、框架類前置改用目錄名＋實體檔案驗證；`MANIFEST.sha256` 類清單一律 `cat` 全檔不 `head`（會漏看後面的目標而誤刪）；就地修補已部署且由自動化管線管理的檔案（如 ESP）要馬上同步回 mod-library 來源層，否則下次自動 redeploy 會悄悄蓋掉；衍生候選清單要對照 prose/README 交叉核對完整性。
source: agentctl/handoffs/done/2026-09/home-2026-09-03/lrrev/REPORT.md:191；agentctl/handoffs/done/2026-08-27/opus-gaps/_COMMON-LIMITS.md:17；mod-library/README.md:36-58
