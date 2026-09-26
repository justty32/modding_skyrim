# houseCARL、xEdit、DynDOLOD 等工具坑（2/2）

[lessons 索引](README.md)｜同主題：[housecarl-and-tools](housecarl-and-tools.md)

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
