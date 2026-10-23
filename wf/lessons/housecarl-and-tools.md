# houseCARL、xEdit、DynDOLOD 等工具坑

[lessons 索引](README.md)

## nexus-api-version-is-not-proof

> "Nexus API 的 version 欄位只是篩選門檻,不是同版證明;真正的閘門是二進位拓撲比對"（原 type: memory）

一直在用的規則是「Nexus API 的 `version` 欄位是判準，檔名裡的版本字串不算數」。
**這條只對了一半，2026-08-22 被實測推翻。**

案例：`Ordinator - Perks of Skyrim - Chinese Localisation Based on WOK-57464-9-30-1-...zip`
- Nexus API version 標 **9.31.0** → 依舊規則會直接放行
- 實際 ESP 只有 **5,013 records**，本體 9.31.0 是 **5,015**，少兩筆 IDLE
- 另有 464 個 record 的 VMAD 差異、36 個 CTDA、PERK DATA/PRKE/PRKC、AVIF HNAM、
  LVLI LVLO、NPC inventory、WEAP CRDT、RACE 行為資料等大量非文本改動
- **檔名裡那個 `9-30-1` 才是真的**；作者上傳時填錯了 version 欄位

修正後的規則：

1. API version 是**必要不充分**條件——版本對不上直接刷掉，版本對上**不代表**可以裝
2. 真正的閘門是二進位比對：ordered masters、record 總數、
   **signature + FormID key 集合**、subrecord 序列
3. 非文本差異（VMAD、CTDA、數值 DATA、PERK 結構、FormID 引用、record 增刪）
   出現就不是「純翻譯層」，不管檔名和頁面寫什麼
4. CJK 數量只能排除假中文層，**不能**證明它是同版

換句話說：**中文化的預檢閘門要真的跑，不能靠 metadata 放行。**
這次 7 個候選跑下來 4 GO、1 NO-GO、1 需合併、1 待下載——閘門真的擋下了東西。

相關：[[no-cht-chs-preference]]（繁簡皆可，唯一硬門檻就是同版）、
[[translation-layer-cost-threshold]]、[[agent-driven-nexus-download]]

## housecarl-setfield-cjk-byte-drop

> houseCARL set_field 寫中文會靜默丟位元組（cp1252 解碼吃掉 81 8D 8F 90 9D），check_errors 驗不出；寫中文一律用 bulk_apply CopyFrom（原 type: project）

2026-09-01 hcell 隊實測：houseCARL/Mutagen 讀寫字串欄走 Windows-1252，檔案實為 UTF-8。cp1252 未定義的五個位元組（81 8D 8F 90 9D）在「讀」的階段就被靜默丟掉——「讀出中文再寫回」會毀掉多數 CJK 名稱（實測「區」E5 8D 80 → E5 80）。check_errors 驗不出（只查 FormLink/master/parse）。既有 docs 只記了寫出變 ?，沒記讀取丟位元組這半邊。

**Why:** 會靜默毀損所有經 set_field 轉寫的中文字串，且無工具告警。

**How to apply:** houseCARL 寫中文欄一律 `bulk_apply verb=CopyFrom`（DeepCopy 位元組保真、不經顯示層）；驗收必做位元組級 diff 對正本，不能只靠 check_errors。位元組層讀 CELL FULL 可用 agentctl/handoffs/hcell-2026-09-01/tools/cellfull.py。相關：[[chinese-diff-ok-but-no-tofu]]。

2026-10-23 補：這個 cp1252↔UTF-8 問題不只寫會壞，houseCARL 的 `cross_plugin_query`／raw 讀取「顯示」中文也會變 mojibake（還原公式 `x.encode('cp1252').decode('utf-8')`，但 81/8D/8F/90/9D 五個位元組在顯示層已永久丟失、無法還原，`agentctl/handoffs/done/2026-08/opus-apply-order/STATE.md:110-119`）；另外用寫入工具對 esp 做其他就地改寫（如補懸空引用）也有風險連帶動到 CJK 子紀錄，改完同一支 esp 要對 FULL／DESC／RNAM／EPFD 等欄位做前後字串 diff，不能只看 check_errors 的結構性數字。

## housecarl-cannot-point-real-mo2-instance

> houseCARL 指不到真實 MO2 實例（ModOrganizer.ini 的 gamePath 是 wine 的 Z:\ 形式），要用 POSIX 鏡像；profiles 用快照複製不 symlink（原 type: memory）

2026-09-05 lead-ayop 實測：`housecarl_set_mo2_instance` 指真實 `/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2` **必定失敗**（「game Data folder is missing: Z:\home\...\Skyrim Special Edition/Data」），因為真實 `ModOrganizer.ini` 的 gamePath 是 wine 的 `Z:\...` 形式，houseCARL 不做 Windows→POSIX 轉換。上午各線用 /tmp 鏡像不是偷懶，是唯一解。

**Why:** 交接書若寫「先指回真實實例」，每條線都會白撞一次；而指到某線 session 的 scratchpad 鏡像則會隨 session 消失、profiles 快照也會過時。
**How to apply:** 用鏡像目錄：`ModOrganizer.ini` 的 gamePath 改 POSIX、`mods`／`Data` symlink 到真實目錄、`profiles` 用 `cp -a` **快照**（不 symlink，否則 houseCARL 寫入路徑會指回版控目錄）。有線改過 modlist/plugins 就先重新 cp 再讀。2026-09-05 的鏡像在 `/tmp/housecarl-mirror-2026-09-05`（重開機就沒了）；常設化＋刷新腳本收進 `instance/tools/` 登記在 `agentctl/docs/backlog.md`。相關：[[mo2-auto-adds-stray-mods-dirs]]（houseCARL 寫入產物別落在真實 mods/）。

**2026-09-08 追加：** 鏡像是快照，profile 剛改過（新 patch 套上）而鏡像沒刷新時，houseCARL 會高信心回報「這支 esp 不在載入順序／沒贏」——lead-rsc2 因此誤判第一輪 patch 沒生效、白做一輪。**做記錄層贏家判定前先刷新鏡像的 profile 快照**（`~/.local/share/housecarl-mirror`），並把「鏡像時間戳 ≥ profiles 最後 commit」寫進驗收。

2026-10-10 補：houseCARL 偶發「Could not determine plugin listings path」等間歇性錯誤，常見原因是別線同時在跑 `housecarl-mirror.sh` 刷新鏡像（而非鏡像過期）；`cross_plugin_query` 或 esplib 自寫的 `resolve_load_order.py` 這類不依賴同一份鏡像快照的替代算法通常仍可用，重試幾次或改路即可，不必停工等候（`agentctl/handoffs/done/2026-10/home-2026-10-10/smi/REPORT.md`）。

## housecarl-merge-facegen-backslash-filename

> houseCARL merge_plugins 在 Linux 把 facegen 輸出寫成含反斜線的單一檔名，不是真目錄；合併後要手動攤開並對齊大小寫（原 type: memory）

2026-09-06 lead-rm 合併 Thora／Torvi／Hrefna 三支 esp 時實測：houseCARL `merge_plugins` 會自動把 FaceGen 搬到新 plugin 名的資料夾（這是選它而不選 xEdit 的原因），但在 Linux 上寫出來的是 `textures\actors\character\...\00000800.dds` 這種**含反斜線的單一檔名**，遊戲找不到。

**Why:** Windows 路徑分隔符沒轉 POSIX；MO2／Proton 下大小寫也要對齊原 mod 用的 `Meshes/actors/character/FaceGenData/FaceGeom/`。
**How to apply:** 合併後先 `find mods/<new> -name '*\\*'` 抓出來，逐個攤成真目錄再驗；FormID 對照表另存（FormID 全變，招募中的隨從會消失）。相關：[[housecarl-cannot-point-real-mo2-instance]]（鏡像在 `~/.local/share/housecarl-mirror`，profiles 改過要重跑 `instance/tools/housecarl-mirror.sh`）。

2026-10-23 補：同樣的 FormID 重編風險也出現在 `compact_plugin`（compact 成 ESL）——若該 esp 帶 NPC facegen 且檔名就是 FormID，compact 後 FormID 變了、facegen 檔名對不上會當場黑臉；compact 帶 facegen 的 esp 前先掃是否有 FormID 命名的 facegen 檔，優先避免 compact，先清點 full 槽餘量是否真的不夠（`agentctl/handoffs/done/2026-09/home-2026-09-12/lgperk/REPORT.md:116`）。

## housecarl-copy-tools-pull-more-than-asked

> houseCARL 的 forward_record／merge_plugins 等複製類工具，拿到的往往比你要的多；用法不對會整批作廢重做

2026-10-03 worldfix 隊：`forward_record` 若先 forward REFR 再 forward 其所屬 CELL，houseCARL 會把 cell 底下其他 child ref 整批清掉；要先 forward 容器（WRLD/CELL，取現役贏家版本）再 forward 子記錄。同隊另發現：`forward_record` 抄 REFR 會自動把父 CELL/WRLD 一起帶過來，且是**來源 plugin 自己的版本**不是引擎贏家，修法是先用 `engine_winners.py` 算好父記錄贏家、換上贏家版、子記錄再補 forward 一次（`agentctl/handoffs/done/2026-10/home-2026-10-10/mo2-reorder/REPORT/construction.md`）。`from_plugin` 必須是現役 active load order 裡的 plugin，未安裝的 mod 不能直接當來源，改成對現役 winner forward、日後排序奪回（`agentctl/handoffs/done/2026-09/hmpatch-2026-09-01/REPORT.md`）。對含中文 FULL 的 record，`forward_record` 有時丟 `TargetInvocationException`，可改手工 raw 複製 record bytes 繞過（前提：內部 FormID 都是本檔 master index 00）。另外 `merge_plugins` 的契約是整份複製 donor 的所有 records，不是挑子集——只要部分內容，先在隔離環境建出範圍受限的 donor plugin 再合併。

**Why:** 這幾個行為都不直覺，照字面用容易把容器或非目標內容也複製／蓋掉，產物要整批重做。

**How to apply:** 用這些工具前照順序：先父後子；`from_plugin` 先確認在現役 load order；中文 FULL 丟例外就手工 raw 複製＋`check_errors` 驗證；`merge_plugins` 只要子集就先建範圍受限 donor。

## housecarl-nexus-api-field-quirks

> houseCARL／Nexus keyless API 有多個回傳欄位不可信，要交叉查證或改走別的查詢面

2026-08～2026-10 多線各自命中：`housecarl_nexus_mod(files=true)` 不回傳數字 `fileId`，要精確指定檔案版本得改走 `housecarl_nexus_graphql` 查 `modFiles`；`directDownloadEnabled`／`download_route` 在 keyless 模式下對每個 mod 都回同一個常數，不能拿來判斷「作者關掉直接下載」；GraphQL 的 `bytes`／`sizeInBytes` 常回 `null`（`bytes` null 改用 `nexus_identify` md5 核身分，`sizeInBytes` null 改用 `size`(KB)×1024）；`nexus_search` 排序不等於按 endorsements，排行前面的可能背書數反而較低；meta.ini 的 modid 可能因頁面遷移跟下載檔 id 對不上，兩個 id 都要查一次確認同一個 mod；houseCARL 的 Nexus 工具讀不到作者自建外部站或 Nexus posts 分頁，這類資訊只能請人用瀏覽器讀。`nexus_intake_check.py dedupe` 常把自己的 `_dl-*` 下載暫存誤判成庫內重複，是已知路徑衝突不是真重複。批量查詢（>50 件）改用免金鑰 GraphQL 端點 `api-router.nexusmods.com/graphql` 自寫節流腳本，比逐件呼叫 MCP 快一個數量級（lr 線 371 件 6 分鐘跑完）。

**Why:** 這些欄位「看起來合理但其實是常數/null/假排序」，已在多條獨立線上重複造成誤判。

**How to apply:** 遇到上述欄位先假設不可信，照各自替代查法核實；大量查詢一律走批次 GraphQL 腳本，不要逐件呼叫 MCP。

## housecarl-silent-wrong-answer-bugs

> houseCARL 有多處會在特定情境下悄悄給錯答案，不是「查無結果」而是「結果是錯的」


**大小寫／反斜線（native Linux）：** LooseCache 大小寫不敏感比對但只記第一次出現的大小寫，查過小寫路徑的子樹之後對 resolver 永久隱形；內部路徑正規化成反斜線，碰 loose filesystem 前沒轉本機路徑，`housecarl_skse_inventory` 會回報 0 DLL 即使檔案都在（本機 fork 已修，換 source／重裝要重查；`analysis/houseCARL/answers/linux-manjaro-mo2-runbook/verification.md`）。

**`resolve_names=true` 在本機必定失敗**（`Could not determine plugin listings path`），重試也沒用，要查人類可讀名稱改用 esplib/whichmod（2026-10 多條獨立線各自命中）。

**判贏家照 plugins.txt 字面順序**，不套引擎「master 類（.esm/.esl/ESM旗標）排所有普通 esp 前面」的規則；候選群混有 master 類時要另外跑 `engine_winners.py` 模擬引擎實際順序交叉驗證（2026-10-10 六條線的「排序讓某 mod 輸」驗收都建立在這個會出錯的前提上，實測 8 筆翻盤；`agentctl/handoffs/done/2026-10/home-2026-10-10/mo2-reorder/REPORT.md`）。

**Why:** 三類都不報錯，給出看似正常但錯誤的答案，前兩類已有多條獨立線踩過。

**How to apply:** 碰到 0 DLL／resolve_names 失敗／排序判贏家，先假設是已知 bug，不要照字面信任結果；候選群混 master 類時一律跑 `engine_winners.py` 交叉驗證。

## version-compare-must-abstain-not-guess

> 版本號比較沒有單一安全讀法：10 位 timestamp 排序把新式無 timestamp 檔名判成最舊；整數 tuple 讀法在 `1.06` vs `1.1`、`1.9` vs `1.10` 前導零/位數不一致時判反；過濾腳本把 None（不適用）與 False（確認為否）當同一布林處理，等於排除掉庫裡絕大多數候選卻誤讀成「沒有候選」

2026-08-28 opus-lib-tidy／opus-tool-fix 兩線實測：`cleanup_report.py` 單用 10 位 unix timestamp 排序，把帶日期字串、無 timestamp 的新式命名判成 ts=0=最舊，6 組現役框架層最新版被誤判成舊版；改用整數 tuple 又在 `6817 KS Hairdos SSE`（1.9 vs 1.10）、`77566 Civil War Lines Expansion`（1.06 vs 1.1）這類位數不一致案例判反。另一道閘門 `runtime_ok_1_6_1170 is True` 把 None（該檔不含 SKSE dll，不適用）與 False（已知不相容）混為一談，使該閘門永遠產出 0 筆清理候選，長期被誤讀成「庫裡沒有舊版本」。

**Why:** 兩種版本比較啟發式單獨用都會在實庫踩雷；欄位值 None（未知/不適用）與 False（確認為否）語意不同，共用同一布林判斷會系統性排除候選而不自知。

**How to apply:** 版本語意比較函式遇到 qualifier 不同、位數矛盾等情況要明確回傳「無法判定」，呼叫端把 None 當整組不動，不要賭方向；拿 KS Hairdos／Civil War Lines Expansion 當回歸測試案例。過濾/分級腳本的 None 與 False 要分開判斷；某閘門長期 0 筆候選時先懷疑閘門語意，不要直接採信「真的沒有」。


## agent-bridge-endpoints-dont-guarantee-success

> agent-bridge（驅動 Skyrim 實機的 HTTP 橋接層，與 houseCARL／qa_* 是不同工具）的 `/state`、`/console` 回應正常不代表資料完整或指令真的生效

2026-09-05 `/state` inventory 用指標位址排序，`limit=32` 時背包遠超過，被截掉的物品是隨機的，同份 qa.json 有時過有時不過（`agentctl/handoffs/done/2026-09/home-2026-09-05/ab/REPORT.md:63`）。`/console` 無論指令對不對都回 `ok:true`——`CompileAndRun` 簽名是 void 不回傳結果，程式寫死 `ran=true`，送不存在指令一樣拿 HTTP 200（同報告:46）。

**Why:** 兩端點只回報「請求送進去了」，不回報「內容完整」或「指令真的生效」。

**How to apply:** 送指令後不能只看 `ok:true`，要另用 `/state` 或可觀察變化驗效果；inventory 自動驗收前先確認截斷順序，不能單憑一次 PASS 下結論。
