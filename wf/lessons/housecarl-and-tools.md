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

## xedit-linux-needs-ascii-data-root

> "2026-09-10 實證：xEdit／QuickAutoClean 經 MO2（wine）跑時，VFS Data 根有非 ASCII 檔名就 Fatal「Invalid characters in path」；`run -a` 帶 plugin 檔名位置參數也炸；DynDOLOD deleted-reference 一次只報一支"（原 type: memory）

2026-09-10 lead-sol2 實測（DynDOLOD 重跑途中）：

- **xEdit 在 Linux（MO2 + Proton）下**，只要 VFS 的 Data 根目錄有任何非 ASCII 名字（韓文空資料夾 `새 폴더`、中文資料夾 `中文`、`记录.txt`），
  `wbLoadModules → TDirectory.GetFiles` 就丟 `EArgumentException: Invalid characters in path`，Wine 把它們轉成 `?`。
  改成 ASCII 名字後立刻正常。09-04 能跑純粹是那時還沒裝這幾個 mod。
- 用 `ModOrganizer.exe -p <profile> run -a "-sse -IKnowWhatImDoing <plugin>" <exe>` 想無人值守自動選檔也會炸；
  可靠做法是 09-04 的 `-e QuickAutoClean`（`~/skyrim_mods/tools/run-qac.sh`），plugin 由人在視窗選。
- DynDOLOD 對 deleted reference **一次只報一支、只報它實際處理到的 cell**；全載入序掃描（24 支帶刪除引用）只是候選表。
  CC 官方檔（goldbrand 等 9 支）QuickAutoClean 只 undelete、不動 ITM，**不會掉中文**；一般 mod 清 ITM 會掉中文 FULL（09-04 Midas 先例）。

**How to apply:** 開 xEdit／DynDOLOD 前先掃 mods 頂層＋Data＋overwrite 的非 ASCII 名字（`os.listdir` 逐項，別用 grep）；
QAC 走 run-qac.sh 手動選檔；DynDOLOD 停在哪支就清哪支，CC 直接清、mod 先比 FULL 數。
相關：[[dyndolod-runtime-and-traps]]、[[vanilla-masters-cleaned-in-data]]

## dyndolod-runtime-and-traps

> 2026-09-04 首跑實測：DynDOLOD Medium 約 36 分（不是 1.5–4 小時）、TexGen 約 1.5 分；輸出路徑欄顯示會騙人、只能 Save and Exit、舊 TexGen_Output 啟用會擋 TexGen（原 type: project）

2026-09-04 lod 線在這台機器（16 核、Proton＋MO2 VFS、`run-lod-tool.sh`）首跑：TexGen 1 分 07 秒～1 分 24 秒；DynDOLOD 3.00 Alpha-210 Medium＋Occlusion、不開 grass、約 830 plugin：**36 分 13 秒**（按 Save and Exit 後再寫 10 分）。產物 3.9 GB／16,084 檔，`Occlusion.esp` 65 MB。三道上游硬門檻：deleted large references（要 xEdit QuickAutoClean 原版 master）、Unresolved FormID（真懸空要就地設 `000000:Skyrim.esm`；Mutagen 對 Skyrim.esm 的 384 筆是假陽性）、舊 `TexGen_Output` 仍啟用時 TexGen 直接擋下。

**Why:** runbook 原估 1.5–4 小時是上游估值，會讓排程過度保守（今天差點因此不跑）；輸出路徑欄每次開 Wizard 都顯示預設值但實際用上次瀏覽選的路徑，`Save, Zip and Exit` 會把輸出目錄刪掉。
**How to apply:** LOD 排程抓 1.5 小時整段（含重跑 TexGen、裝 Output、實機）即可；跑完看 log 末三行 `Saving …` 確認輸出位置；只按 `Save and Exit`；重跑前先把舊 Output 在 modlist 改 `-`。CC／exterior mod 變動後要重跑（先 TexGen 再 DynDOLOD）。相關：[[vanilla-masters-cleaned-in-data]]。

**2026-09-12 補充（lead-want5 重跑實錄）：**
- 「跑前停用舊輸出」只適用 `DynDOLOD_Output`；TexGen 跑完要**立刻裝回 MO2 並啟用 `TexGen_Output`**，否則 DynDOLOD 報 `LOD billboard(s) not found`。輸出根目錄不同：TexGen → `tools/DynDOLOD/TexGen_Output/`，DynDOLOD → `tools/DynDOLOD_Output/`。
- 標題凍結＋CPU 高＝在算；標題凍結＋沒寫盤＝停在 Save 對話框等人按 `Save and Exit`（Occlusion 那段近 20 分鐘）。
- profile 三檔行尾不可假設一致（當時 plugins.txt 純 LF、另兩檔 CRLF，MO2 跑過又變回 CRLF）；改檔腳本要就地偵測。
- 這次 4.5 GB／17,016 檔、DynDOLOD Medium＋Occlusion 38 分；GUI 用 xdotool 按鈕（使用者不在時才准）。


**2026-09-14 補：** TexGen／DynDOLOD 啟動後先停在 Options／Wizard 視窗等人按 Start；log 檔要到結束才寫，靠「等 log 出現」判斷會空等（cow 線空等 20 分鐘，頂層 `xdotool search --name "TexGen Options"` 找到視窗代按）。派線時寫死：每個 GUI 步驟先 `import -window` 截圖看有沒有對話框，再等。另：舊 DynDOLOD.esp 的 master 被拔掉時，DynDOLOD 會報 already exists 且無法 update，只能從零重生成。

2026-10-23 補（第三方快照，未實測，暫無現役用途——本機 DynDOLOD 已於 2026-10-08 整組停用，見 project-decisions 的 new-save-plan-2026-10-04）：DynDOLOD 3.0 輸出的 plugin 排序規則是 `DynDOLOD.esm` 排在所有 worldspace ESM 之後、`DynDOLOD.esp` 倒數第二、`Occlusion.esp` 最後（除非有 Synthesis patcher 排在最末）；若用 ACMOS 類道路生成 addon，`DynDOLOD_SSE.ini` 要先設 `Expert=1`／`Level32=1`。留待未來重新啟用遠景生成時使用。相關：[[dyndolod-esp-masters-pin-content-mods]]。

## vanilla-masters-cleaned-in-data

> 2026-09-04 為了 DynDOLOD 硬性檢查，Update/Dawnguard/HearthFires.esm 已用 xEdit QuickAutoClean 清理並寫回遊戲 Data/；Steam Verify 會還原成髒檔、DynDOLOD 得重跑（原 type: project）

2026-09-04 lod 線首跑 DynDOLOD 3.00 Alpha-210 被擋：`Update.esm`／`Dawnguard.esm`／`HearthFires.esm`／`ccvsvsse004-beafarmer.esl` 有 deleted large references，上游明文只能清理。lead-lod 用 SSEEdit 4.0.4 QuickAutoClean 清完四支，三支 .esm 直接覆蓋遊戲 `Data/`（原檔逐位元備份在 `~/skyrim_mods/_lod-vanilla-master-backup-2026-09-04/`；結果 CRC 命中 LOOT masterlist 的已清理條目）。

**Why:** 這是遊戲目錄層級的改動，不在 profiles repo 版控裡；任何 Steam「驗證檔案完整性」或重灌都會把它們還原，DynDOLOD 就得整個重跑（1.5–4 小時）。
**How to apply:** 「別按 Verify」的理由多了一條，跨 session 排 Steam 下載時要明講；重灌後先比對三支 esm 的 CRC 再跑 LOD；回滾就是把備份目錄的檔案 cp 回 `Data/`。相關：[[skyrim-no-appmanifest-steam-safe]]、[[launch-skyrim-via-steam]]。

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

## missing-master-scan-mast-not-housecarl

> houseCARL load_order_status 的「缺 master 0」只看 plugins.txt 勾選，證明不了 master 有裝；驗收要用全稱掃 TES4 MAST 的 check_masters.py（原 type: memory）

2026-09-03 lrzh／lrfw 發現：`housecarl_load_order_status` 報「缺 master 0」時，實際有 **13 個**借用 patch 的 master 根本不在 load order（MO2 開關時會自動取消勾選，但 `git checkout --` 還原後又變回啟用）。MO2 回寫 diff 反推也不行（390 行重排只挑得出 3 筆）。

**Why:** 今天 inst2／rt2／lrinst／lrzh 四隊的驗收都用了這個假數字；lrfw 全稱掃 MAST 後遊戲內 plugin 數（790）才第一次與 plugins.txt 對上。
**How to apply:** 安裝／部署類交接書的「缺 master」驗收一律指定 `instance/tools/check_masters.py --out <csv>`（讀 TES4 MAST，`present=no` 必須 0；`--out` 必填，`--candidate` 可讀未安裝的單一 plugin；2026-09-03 晚 18:21 已從 lrfw 交接書搬進 instance，原檔仍留在 `agentctl/handoffs/home-2026-09-03/lrfw/tools/`）。可選 patch 的規則寫死「master 不在啟用集就不勾」。相關：[[verify-game-alive-via-qa-not-ps]]。

2026-09-03 晚補：隱含 master 判定曾是「loadorder 前 13 行」，inst3 工人把新 plugin 塞到 loadorder 開頭就假報 44 筆；20:41 已改成「5 個原版＋`Skyrim.ccc` 中經 MO2 解析器可見的檔」（instance 9cddaef），本機是 13 個（其中 3 個 CC 小件在 `Creation Club Missing Archives (private)` mod 裡，不在遊戲 Data）。三個 profile 檔第 1 行都是 MO2 註解、loadorder 前段是隱含 master、modlist 第 1 行優先權最高——交接書寫「插最上面」一定錯。

2026-08-31 補：自動化「缺前置/缺 master」gate 的「缺」只是起點不是終點——grow 隊的 gate 只比對暫存候選彼此、沒比對現役已裝啟用的全部 mod，誤判了至少 3 件其實前置早已在現役 load order 裡的候選。驗收前要再用 `housecarl_read_plugin_file` 讀出候選 plugin 完整 masters 清單，逐一對現役 `plugins.txt` 比對存在且啟用（`*`），不能只信 gate 回報的第一個「缺哪一個」。source: agentctl/handoffs/done/2026-08-31/fixdis-2026-08-31/FIX-REPORT.md:43-57

2026-10-23 補：同一個「別信二手摘要，查原始紀錄」的坑還有兩個變種——active 集合只掃 plugins.txt 打星號會漏掉隱式啟用的 CC 插件（本機曾差 59 支，真實 active 集合要用 loadorder.txt 扣掉未勾選項，或信 houseCARL/qa_state 的 active 數字，`agentctl/handoffs/done/2026-09/home-2026-09-11/donor/REPORT.md:105-111`）；判斷 mod 實際機制／類別要直接讀該 mod 現役 esp 的 record 組成，不要照抄既有分析文件或 catalog 分類標籤（曾把只有 9 筆 float GMST 的 mod 誤記成天氣 overhaul）。

## bsa-voice-index-false-negative

> 2026-09-18 隨從文本解包：BSA 語音索引靜默回 0 會捏造「缺語音」；語音不只 .fuz；中文層要看文本不只看路徑（原 type: project）

2026-09-18 vf-text 隊（`modpack-design/content-plan/dialogue/`，工具 `dump_follower_dialogue.py`／`translation_pipeline.py`）踩到的假陰性：BSA 語音索引失敗時靜默回 0 → Inigo／Sofia／Recorder 全被標「缺語音」；Rigmor 48%「缺語音」其實是多隨從 plugin（OK_Followers.esp 裝 11 個）的 voice_type 錯歸屬，真值全部 0–7%；語音檔還有 .xwm/.wav 不只 .fuz；中文層偵測只看路徑會把 daegon/kaeserius 判 0%；GetIsID 命中要看比較運算子；「JP TEXT」mod 其實是中文。

**Why:** 這類統計一錯就會推出「要補配音」的假工項。

**How to apply:** 索引結果為 0 一律當錯誤不當數據；多隨從 plugin 用 voice_type 分攤；缺語音率 >20% 先懷疑統計而非 mod。相關：[[voiced-follower-makeover-project]]、[[translation-layer-cost-threshold]]。


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

## esl-binary-format-facts

> 手寫腳本讀寫 ESL/TES4 二進位格式的兩個關鍵位置：旗標 offset 與 cell 覆寫的 Partial Record 旗標

TES4 flags（含 ESL 位元 `0x00000200`）正確位置是 **offset 0x08**，不是曾寫死在交接書裡的 0x18（0x18 讀到的其實是 HEDR 子紀錄；`agentctl/handoffs/done/2026-09/home-2026-09-07/chron/REPORT.md:68`）。另外（第三方指南轉述，未實測）：ESM-flag plugin 正確區分 persistent／temporary 並依序載入；非 ESM-flag plugin（含 ESL）全部記錄視為 persistent；ESL 新增的 cell record 若被另一 plugin 覆寫、覆寫方沒標 **Partial Record**（xEdit unknown 14 旗標），原 cell 的 temporary 引用會被整個忽略，觸發暫態引用消失 bug；要保留的引用要同時標 persistent。

**Why:** 前者已有實測錯誤前例，後者直接對應一類已知的暫態引用消失 bug，兩者都會讓手刻/手補 patch 悄悄壞掉。

**How to apply:** 手寫腳本判斷 ESL/ESPFE 一律讀 offset 0x08；任何改到 ESL 定義的 cell record 的 patch，先查覆寫方是否該標 Partial Record、暫態引用是否同時標 persistent。

## load-order-and-asset-measurement-pitfalls

> 算衝突／重複／贏家這類統計時，好幾種看起來合理的算法會系統性算錯規模


**asset winner ≠ plugin winner**：聲音/lip 等資產檔的 winner 由 MO2 VFS（檔案覆蓋順序）決定，跟 plugin record 的 winner（load order）是兩套獨立規則，要分別驗，不能把 xEdit 單檔視圖當現役結果（`agentctl/handoffs/done/2026-08/cx-serana/REPORT.md`）。

**override 筆數 ≠ 衝突筆數**：借用內容覆寫 98,487 個 FormID，真正與現役也動過的只有 16,780（17%），其餘只是「蓋原版」的正常行為；算衝突規模要用「現役覆寫索引 ∩ 借用側覆寫索引」的交集，不能直接拿 override 總數當衝突數。

**FormID 漂移比對用 EDID 不用 FULL**：素材升版後 FormID 位移，用 FULL 比對會產生假 GONE（中文層 FULL 早是中文名，英文名只活在 EDID）；改用 EDID 且規則由鬆到緊（結尾相符>含名字>完全相符），否則會被語意不同但部分相符的記錄搶走。

**同 VFS 路徑的重複貼圖是 0 VRAM 成本**：只佔硬碟；真正會重複吃 VRAM 的只有「不同 VFS 路徑但位元組相同且同時在場」的檔案，估算前先分這兩組。

**Why:** 四個都是直覺算法高估/算錯規模的例子，會把正常行為誤判成要修的衝突，或把成本算錯一個數量級。

**How to apply:** 算衝突/重複規模前先確認用的是交集而非併集、資產層要分開驗、FormID 比對用 EDID 分級規則。

## papyrus-recompile-for-translation-pitfalls

> 重編譯 Papyrus 源碼來改中文字串，兩個不報錯但會悄悄壞掉的坑

直接餵 UTF-8（無 BOM）的 `.psc` 給編譯器會編譯成功，但中文字串在產物裡變雙重編碼亂碼（編譯器把 UTF-8 位元組誤當 ANSI 讀），不會報編譯錯誤，只有逐字串檢查才會發現；存檔一律加 UTF-8 BOM 才正常。另外，缺編譯旗標檔/缺完整相依 script 時重編譯既有 `.pex`，動手翻譯前要先做 round-trip 驗證：用「未修改」的 `.psc` 編一次，跟原廠 `.pex` 比對字串表 multiset、userFlagTable、檔案大小，證明工具鏈本身保真（差異要能被編譯者/機器名長度等已知因素完全解釋）才算過關；編譯旗標檔可從既有 `.pex` 的 userFlagTable 位元索引重建（`agentctl/handoffs/done/2026-08/opus-zh-summary/SUMMARY.md:667-694`）。

**Why:** 兩個坑都是「編譯成功＝看起來沒事」但產物其實壞了，只有逐字串/逐項比對才抓得到。

**How to apply:** 任何要重編譯含中文字串的 `.psc`，存檔一律加 BOM；動手翻譯前先用未修改源碼做 round-trip 驗證當硬閘門，不要編完直接上。


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
