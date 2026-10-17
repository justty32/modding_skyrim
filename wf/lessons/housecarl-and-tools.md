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

## housecarl-cannot-point-real-mo2-instance

> houseCARL 指不到真實 MO2 實例（ModOrganizer.ini 的 gamePath 是 wine 的 Z:\ 形式），要用 POSIX 鏡像；profiles 用快照複製不 symlink（原 type: memory）

2026-09-05 lead-ayop 實測：`housecarl_set_mo2_instance` 指真實 `/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2` **必定失敗**（「game Data folder is missing: Z:\home\...\Skyrim Special Edition/Data」），因為真實 `ModOrganizer.ini` 的 gamePath 是 wine 的 `Z:\...` 形式，houseCARL 不做 Windows→POSIX 轉換。上午各線用 /tmp 鏡像不是偷懶，是唯一解。

**Why:** 交接書若寫「先指回真實實例」，每條線都會白撞一次；而指到某線 session 的 scratchpad 鏡像則會隨 session 消失、profiles 快照也會過時。
**How to apply:** 用鏡像目錄：`ModOrganizer.ini` 的 gamePath 改 POSIX、`mods`／`Data` symlink 到真實目錄、`profiles` 用 `cp -a` **快照**（不 symlink，否則 houseCARL 寫入路徑會指回版控目錄）。有線改過 modlist/plugins 就先重新 cp 再讀。2026-09-05 的鏡像在 `/tmp/housecarl-mirror-2026-09-05`（重開機就沒了）；常設化＋刷新腳本收進 `instance/tools/` 登記在 `agentctl/docs/backlog.md`。相關：[[mo2-auto-adds-stray-mods-dirs]]（houseCARL 寫入產物別落在真實 mods/）。

**2026-09-08 追加：** 鏡像是快照，profile 剛改過（新 patch 套上）而鏡像沒刷新時，houseCARL 會高信心回報「這支 esp 不在載入順序／沒贏」——lead-rsc2 因此誤判第一輪 patch 沒生效、白做一輪。**做記錄層贏家判定前先刷新鏡像的 profile 快照**（`~/.local/share/housecarl-mirror`），並把「鏡像時間戳 ≥ profiles 最後 commit」寫進驗收。

## housecarl-merge-facegen-backslash-filename

> houseCARL merge_plugins 在 Linux 把 facegen 輸出寫成含反斜線的單一檔名，不是真目錄；合併後要手動攤開並對齊大小寫（原 type: memory）

2026-09-06 lead-rm 合併 Thora／Torvi／Hrefna 三支 esp 時實測：houseCARL `merge_plugins` 會自動把 FaceGen 搬到新 plugin 名的資料夾（這是選它而不選 xEdit 的原因），但在 Linux 上寫出來的是 `textures\actors\character\...\00000800.dds` 這種**含反斜線的單一檔名**，遊戲找不到。

**Why:** Windows 路徑分隔符沒轉 POSIX；MO2／Proton 下大小寫也要對齊原 mod 用的 `Meshes/actors/character/FaceGenData/FaceGeom/`。
**How to apply:** 合併後先 `find mods/<new> -name '*\\*'` 抓出來，逐個攤成真目錄再驗；FormID 對照表另存（FormID 全變，招募中的隨從會消失）。相關：[[housecarl-cannot-point-real-mo2-instance]]（鏡像在 `~/.local/share/housecarl-mirror`，profiles 改過要重跑 `instance/tools/housecarl-mirror.sh`）。

## missing-master-scan-mast-not-housecarl

> houseCARL load_order_status 的「缺 master 0」只看 plugins.txt 勾選，證明不了 master 有裝；驗收要用全稱掃 TES4 MAST 的 check_masters.py（原 type: memory）

2026-09-03 lrzh／lrfw 發現：`housecarl_load_order_status` 報「缺 master 0」時，實際有 **13 個**借用 patch 的 master 根本不在 load order（MO2 開關時會自動取消勾選，但 `git checkout --` 還原後又變回啟用）。MO2 回寫 diff 反推也不行（390 行重排只挑得出 3 筆）。

**Why:** 今天 inst2／rt2／lrinst／lrzh 四隊的驗收都用了這個假數字；lrfw 全稱掃 MAST 後遊戲內 plugin 數（790）才第一次與 plugins.txt 對上。
**How to apply:** 安裝／部署類交接書的「缺 master」驗收一律指定 `instance/tools/check_masters.py --out <csv>`（讀 TES4 MAST，`present=no` 必須 0；`--out` 必填，`--candidate` 可讀未安裝的單一 plugin；2026-09-03 晚 18:21 已從 lrfw 交接書搬進 instance，原檔仍留在 `agentctl/handoffs/home-2026-09-03/lrfw/tools/`）。可選 patch 的規則寫死「master 不在啟用集就不勾」。相關：[[verify-game-alive-via-qa-not-ps]]。

2026-09-03 晚補：隱含 master 判定曾是「loadorder 前 13 行」，inst3 工人把新 plugin 塞到 loadorder 開頭就假報 44 筆；20:41 已改成「5 個原版＋`Skyrim.ccc` 中經 MO2 解析器可見的檔」（instance 9cddaef），本機是 13 個（其中 3 個 CC 小件在 `Creation Club Missing Archives (private)` mod 裡，不在遊戲 Data）。三個 profile 檔第 1 行都是 MO2 註解、loadorder 前段是隱含 master、modlist 第 1 行優先權最高——交接書寫「插最上面」一定錯。

## bsa-voice-index-false-negative

> 2026-09-18 隨從文本解包：BSA 語音索引靜默回 0 會捏造「缺語音」；語音不只 .fuz；中文層要看文本不只看路徑（原 type: project）

2026-09-18 vf-text 隊（`modpack-design/content-plan/dialogue/`，工具 `dump_follower_dialogue.py`／`translation_pipeline.py`）踩到的假陰性：BSA 語音索引失敗時靜默回 0 → Inigo／Sofia／Recorder 全被標「缺語音」；Rigmor 48%「缺語音」其實是多隨從 plugin（OK_Followers.esp 裝 11 個）的 voice_type 錯歸屬，真值全部 0–7%；語音檔還有 .xwm/.wav 不只 .fuz；中文層偵測只看路徑會把 daegon/kaeserius 判 0%；GetIsID 命中要看比較運算子；「JP TEXT」mod 其實是中文。

**Why:** 這類統計一錯就會推出「要補配音」的假工項。

**How to apply:** 索引結果為 0 一律當錯誤不當數據；多隨從 plugin 用 voice_type 分攤；缺語音率 >20% 先懷疑統計而非 mod。相關：[[voiced-follower-makeover-project]]、[[translation-layer-cost-threshold]]。
