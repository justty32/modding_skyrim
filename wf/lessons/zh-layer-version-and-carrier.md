# 中文層對版與載體型態

[lessons 索引](README.md)｜部署 gate 與引擎字串機制見 [translation-and-zh](translation-and-zh.md)，工具見 [zh-tooling-and-scans](zh-tooling-and-scans.md)

## zh-layer-exact-match-protocol-topology-not-version-string

> 判斷中文層是否對版，要比對 masters／record 拓撲／FormID 集合是否完全相同，而不是看版本號或 bytes

七步協定：身分記錄→分開解壓→二進位拓撲比對（masters/record 計數/FormID set/GRUP 與 subrecord 順序全同才算對齊，硬 gate）→CELL/placement 掃描→asset winner→records/gameplay 接觸面→回滾單位結論（`agentctl/handoffs/done/2026-09-01/hmih-2026-09-01/ANALYSIS-COMMON.md:33-121`）。版本不嚴格匹配時改用「字串ID集合覆蓋率」量化：100% 覆蓋且非文字欄位不動才可裝（`agentctl/handoffs/done/2026-10/home-2026-10-03/want-watch/rounds/20261003-1410/REPORT.md`）。

**Why:** 版號、header、bytes 都可能騙人——header 版號常落後於頁面最新檔案，唯一可信的是逐欄位拓撲比對。

**How to apply:** 搜中文層要廣搜本體全名＋常見後綴變體（CHS/CHT/zh_CN/譯者自訂名），不要只加 Chinese 關鍵字；選檔比對 Nexus files 分頁的精確 MAIN 版本，不信 header；判定「已有/已完整」前先查實際 load order winner（不要只憑有 CHT 資料夾就假設已中文化），翻譯層幾乎都在 Nexus、中文站只當補充；偵測是否已含中文要用 UTF-8 解碼＋連續漢字門檻＋濾假名；同一 plugin 若有多個兄弟 overlay 要先合併成單一 Combined 層才能裝，覆蓋率統計對每層各自 diff 再聯集，不能只看最上層；分母排除英文原本就空的欄位，BSA-only 字串算不出時要註明是下界。相關：[[zh-layer-gate-base-mod-must-be-enabled]]、[[zhport-editorid-fallback-and-hdpt-untranslatable]]

## zh-carrier-type-determines-deploy-risk
<a id="apocalypse-rebuild-waits-new-playthrough"></a>

> 中文層的實作方式（純 Strings／整支 esp 替換／MCM txt／BSA 注入／DSD）決定它會不會被本體升版拖垮、會不會動到存檔，體積與檔案型態就是訊號

純 Strings 型（如 Frozen Heart 只換 3 支 Strings 檔，ESM localized flag）本體升版不受影響，只需比對字串編號集合；整支 esp 替換型（如 BnB）升版會把新版記錄整個蓋回舊版，須走拓撲 gate（`agentctl/handoffs/done/2026-10/home-2026-10-10/frozenheart-zh/REPORT.md`）。體積是另一訊號：KB 級通常純字串替換，百 MB 級是整包重打包，BSA 注入型層會整包蓋掉本體資產、需獨立驗收（`agentctl/handoffs/done/2026-09/home-2026-09-03/zhnex/REPORT.md:118`；`agentctl/handoffs/done/2026-08-28/opus-zh-summary/SUMMARY.md:730-732`）。DSD 是 runtime 字串替換，不參與 record 衝突、恆勝過 ESP 層且會遮蔽版本漂移（`agentctl/handoffs/done/2026-08-30/zh-2026-08-30/DSD-WINNER-CONTRACT.md:6-60`）；MCM 的 translations txt 只改介面文字，解決不了 ESP record 缺口。

**同名覆蓋型中文層不是「翻譯」而是「整支替換」**，版本不同就是換了本體：底版不同，record 集合就不同（2026-09-25）。部署前用 record 型別＋raw FormID 集合比對現役 winner（cx-deploy 的 `deploy/work/preflight.py`）；集合相同可直接換（RDO 62500 Final 與現役同為 9,765 筆）；集合不同，換上去會讓舊存檔指到不存在的 FormID（已學的法術消失要重學），不能逕自在舊存檔上換，要把存檔代價交使用者裁。Apocalypse 已於 2026-11-22 經使用者裁「1.換。」換成 10.2.3 重建層（`agentctl/handoffs/home-2026-11-22/apocalypse-swap/BRIEF.md`）。

**Why:** 不同載體的升版風險、覆蓋範圍、失效模式完全不同，用同一套 gate 驗收會漏判。

**How to apply:** 部署前先判定載體型態；純 Strings 型比對編號集合即可，整支替換型要走拓撲比對；補丁排在整支替換層之後又帶英文 FULL/DESC 要疊 forward 層把中文聯集加回去；覆蓋層 MO2 優先度用 `--priority before:`，`after:` 是排後面＝更低優先權，容易弄反；自帶 checksum/完整性檢查的 mod（如 OStim）覆寫前先讀原始碼找出被鎖定檔名，改完重算 checksum 附上；框架用「目錄列舉＋先讀先贏」載入翻譯檔的，只能同名覆蓋不能靠加新檔案。相關：[[slanguage-english-chinese-in-english-slot]]、[[zhport-editorid-fallback-and-hdpt-untranslatable]]

現成中文包版本落後本體時（如 Chatty NPCs 中文包 1.51 比本體 1.6.1 少 QUST 條件、FLST 的 LNAM、整筆 KYWD），直接拿中文包 esp 出貨等於把 mod 降級；一律改以本體 esp 當載體、用 zhport 類工具只搬中文字串，記錄結構一個位元不動，讓完整性由「結構沒改過」保證而不靠版本號（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-11/zh/REPORT.md:46-49`）。
