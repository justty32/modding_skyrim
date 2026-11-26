# houseCARL 工具坑（Nexus 欄位、寫入與複製語意）與 agent-bridge

[lessons 索引](README.md)

**平台相關**的節（`housecarl-cannot-point-real-mo2-instance`、`housecarl-merge-facegen-backslash-filename`、`housecarl-silent-wrong-answer-bugs`、`housecarl-localappdata-env-on-linux`）在 [housecarl-on-linux](housecarl-on-linux.md)；Nexus 下載自動化在 [nexus-download-ops](nexus-download-ops.md)；版本號比較在 [mod-library-cleanup-safety](mod-library-cleanup-safety.md#version-compare-must-abstain-not-guess)。本檔是跟 Linux 無關的 houseCARL 坑（Nexus 查詢欄位、寫入編碼、複製類工具語意）與 agent-bridge。

## nexus-api-version-is-not-proof

> Nexus API 的 version 欄位只是篩選門檻，不是同版證明；真正的閘門是二進位拓撲比對

2026-08-22：Ordinator 中文層（`...Based on WOK-57464-9-30-1-...zip`）API version 標 9.31.0，實際 ESP 少兩筆 IDLE、另有大量 VMAD／CTDA／PERK／數值等非文本改動；檔名裡的 `9-30-1` 才是真的，作者上傳時填錯 version 欄位。

規則：(1) API version 是**必要不充分**條件——對不上直接刷掉，對上**不代表**可以裝。(2) 真正的閘門是二進位比對：ordered masters、record 總數、**signature + FormID key 集合**、subrecord 序列。(3) 出現非文本差異（VMAD、CTDA、數值 DATA、PERK 結構、FormID 引用、record 增刪）就不是「純翻譯層」，不管檔名和頁面寫什麼。(4) CJK 數量只能排除假中文層，**不能**證明同版。中文化的預檢閘門要真的跑，不能靠 metadata 放行。

相關：[[no-cht-chs-preference]]（繁簡皆可，唯一硬門檻就是同版）、[[translation-layer-cost-threshold]]、[[agent-driven-nexus-download]]

## housecarl-setfield-cjk-byte-drop

> houseCARL set_field 直接寫中文會變 `?`，把 mojibake 顯示字串貼回去當值會掉位元組；check_errors 驗不出；寫中文一律用 bulk_apply CopyFrom

houseCARL/Mutagen 讀寫 inline 字串欄走 Windows-1252，檔案實為 UTF-8。**寫入**：`set_field` 直接給 Unicode 中文會寫成 `?`（`src/housecarl-core/WriteEngine.cs` 約 2914 行的 TranslatedString 轉換，推論自程式碼）。**讀取不丟位元組**：.NET 的 cp1252 對 81 8D 8F 90 9D 五個位元組可逆（2026-10-26 實測）；掉位元組較可能是把 mojibake 顯示字串複製回去當 `set_field` 的值、控制字元 U+008D 在傳輸／顯示層被吃掉（推論）。讀取顯示的 mojibake 在 `f0148dc8` 起的 build 已修（`agentctl/handoffs/home-2026-10-26/hcjk/REPORT.md` §1、§7）。check_errors 只查 FormLink/master/parse，驗不出這類問題，會靜默毀損中文字串。

**How to apply:** houseCARL 寫中文欄一律 `bulk_apply verb=CopyFrom`（DeepCopy 位元組保真、不經顯示層）；驗收做位元組級 diff 對正本，不能只靠 check_errors。用寫入工具對 esp 做其他就地改寫（如補懸空引用）也可能連帶動到 CJK 子紀錄，改完同一支 esp 要對 FULL／DESC／RNAM／EPFD 等欄位做前後字串 diff。位元組層讀 CELL FULL 可用 agentctl/handoffs/hcell-2026-09-01/tools/cellfull.py。`f0148dc8` 之前的 build 讀出的中文是 mojibake，還原公式 `x.encode('cp1252').decode('utf-8')`（`agentctl/handoffs/done/2026-08/opus-apply-order/STATE.md:110-119`）。相關：[[chinese-diff-ok-but-no-tofu]]。

## housecarl-copy-tools-pull-more-than-asked

> houseCARL 的 forward_record／merge_plugins 等複製類工具，拿到的往往比你要的多；用法不對會整批作廢重做

2026-10-03～10-26 實測：
- `forward_record` 先 forward REFR 再 forward 其所屬 CELL，會把 cell 底下其他 child ref 整批清掉——要先 forward 容器（WRLD/CELL，取現役贏家版本）再 forward 子記錄。
- `forward_record` 抄 REFR 會自動帶入父 CELL/WRLD，且是**來源 plugin 自己的版本**不是引擎贏家：先用 `engine_winners.py` 算父記錄贏家、換上贏家版、子記錄再補 forward 一次（`agentctl/handoffs/done/2026-10/home-2026-10-10/mo2-reorder/REPORT/construction.md`）。
- `from_plugin` 必須在現役 active load order；未安裝的 mod 不能當來源，改對現役 winner forward、日後排序奪回（`agentctl/handoffs/done/2026-09/hmpatch-2026-09-01/REPORT.md`）。

含中文 FULL 的 record，`forward_record` 有時丟 `TargetInvocationException`，可改手工 raw 複製 record bytes 繞過（前提：內部 FormID 都是本檔 master index 00），再用 `check_errors` 驗。`merge_plugins` 的契約是整份複製 donor 的所有 records，不是挑子集——只要部分內容，先在隔離環境建範圍受限的 donor plugin 再合併。對既有 plugin 做 in-place 寫入時，houseCARL 會重排整個 master 表並拿掉沒用到的 master（2026-10-26 Kurone7 層少了 `Update.esm`）；層若被別的 plugin 當 master，寫完要對下游跑 `check_masters.py`（`agentctl/handoffs/home-2026-10-26/bodyswap2/REPORT.md` 順帶看到）。

## housecarl-nexus-api-field-quirks

> houseCARL／Nexus keyless API 有多個回傳欄位不可信，要交叉查證或改走別的查詢面

2026-08～10 多線命中，這些欄位「看起來合理但其實是常數／null／假排序」：
- `housecarl_nexus_mod(files=true)` 不回數字 `fileId`，要走 `housecarl_nexus_graphql` 查 `modFiles`（釘版用法見 [[nexus-fileid-and-uploader-graphql-pinning]]）。
- `directDownloadEnabled`／`download_route`（「manager (nxm) download only」那句）在 keyless 模式下對每個 mod 都回同一個常數，不能拿來判斷作者關掉直接下載，也不能當下載閘門。
- GraphQL `bytes` 常回 `null`，改用 `nexus_identify` md5 核身分；`sizeInBytes=null` 是查詢缺口不是死檔（`=0` 才是），大小改用 `size`(KB)×1024。
- `nexus_search` 排序不等於按 endorsements。

前兩條已收進 `agentctl/docs/housecarl/usage-notes.md`（`directDownloadEnabled` 常數、要 fileId 走 `modFiles`）。houseCARL 的 Nexus 工具讀不到作者自建外部站或 Nexus posts 分頁，這類資訊只能請人用瀏覽器讀。批量查詢（>50 件）改用免金鑰 GraphQL 端點 `api-router.nexusmods.com/graphql` 自寫節流腳本，比逐件呼叫 MCP 快一個數量級（lr 線 371 件 6 分鐘）。meta.ini modid 對不上見 [[nexus-identity-confusion-many-forms]]；`nexus_intake_check.py dedupe` 的假重複見 [[library-and-ingest-bookkeeping-fields-lie]]。

## agent-bridge-endpoints-dont-guarantee-success

> agent-bridge（驅動 Skyrim 實機的 HTTP 橋接層，與 houseCARL／qa_* 是不同工具）的 `/state`、`/console` 回應正常不代表資料完整或指令真的生效

2026-09-05 實測：`/state` inventory 用指標位址排序，`limit=32` 時背包遠超過，被截掉的物品是隨機的，同份 qa.json 有時過有時不過（`agentctl/handoffs/done/2026-09/home-2026-09-05/ab/REPORT.md:63`）。`/console` 無論指令對不對都回 `ok:true`——`CompileAndRun` 簽名是 void，程式寫死 `ran=true`，送不存在指令一樣拿 HTTP 200（同報告:46）。

**How to apply:** 送指令後不能只看 `ok:true`，要另用 `/state` 或可觀察變化驗效果；inventory 自動驗收前先確認截斷順序，不能單憑一次 PASS 下結論。
