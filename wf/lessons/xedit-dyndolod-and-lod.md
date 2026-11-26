# xEdit、DynDOLOD 與 LOD 前置

[lessons 索引](README.md)

## xedit-linux-needs-ascii-data-root

> xEdit／QuickAutoClean 經 MO2（wine）跑時，VFS Data 根有非 ASCII 檔名就 Fatal「Invalid characters in path」；`run -a` 帶 plugin 檔名位置參數也炸；DynDOLOD deleted-reference 一次只報一支（2026-09-10）

- VFS 的 Data 根目錄有任何非 ASCII 名字（韓文空資料夾 `새 폴더`、中文資料夾 `中文`、`记录.txt`），`wbLoadModules → TDirectory.GetFiles` 就丟 `EArgumentException: Invalid characters in path`（Wine 把它們轉成 `?`），改成 ASCII 立刻正常。開 xEdit／DynDOLOD 前先掃 mods 頂層＋Data＋overwrite 的非 ASCII 名字（`os.listdir` 逐項，別用 grep）。
- `ModOrganizer.exe -p <profile> run -a "-sse -IKnowWhatImDoing <plugin>" <exe>` 想無人值守自動選檔會炸；可靠做法是 `-e QuickAutoClean`（`~/skyrim_mods/tools/run-qac.sh`），plugin 由人在視窗選。
- DynDOLOD 對 deleted reference **一次只報一支、只報它實際處理到的 cell**；全載入序掃描只是候選表，停在哪支就清哪支。CC 官方檔 QuickAutoClean 只 undelete、不動 ITM，**不會掉中文**，直接清；一般 mod 清 ITM 會掉中文 FULL（09-04 Midas 先例），先比 FULL 數。

相關：[[dyndolod-runtime-and-traps]]、[[vanilla-masters-cleaned-in-data]]

## dyndolod-runtime-and-traps

> DynDOLOD Medium 約 36 分（不是 1.5–4 小時）、TexGen 約 1.5 分；輸出路徑欄顯示會騙人、只能 Save and Exit、舊 TexGen_Output 啟用會擋 TexGen（2026-09-04）

本機 DynDOLOD 已於 2026-10-08 整組停用（見 project-decisions 的 new-save-plan-2026-10-04），以下供重新啟用遠景生成時用。

**時長**（16 核、Proton＋MO2 VFS、`run-lod-tool.sh`、約 830 plugin）：TexGen 約 1.5 分；DynDOLOD 3.00 Alpha-210 Medium＋Occlusion、不開 grass 約 36–38 分（含 Save 後寫檔）。LOD 排程抓 1.5 小時整段（含重跑 TexGen、裝 Output、實機）。CC／exterior mod 變動後要重跑（先 TexGen 再 DynDOLOD）。

**上游硬門檻**：deleted large references（要 xEdit QuickAutoClean 原版 master）、Unresolved FormID（真懸空要就地設 `000000:Skyrim.esm`；Mutagen 對 Skyrim.esm 的 384 筆是假陽性）、舊 `TexGen_Output` 仍啟用時 TexGen 直接擋下。

- 輸出路徑欄每次開 Wizard 都顯示預設值，實際用上次瀏覽選的路徑：跑完看 log 末三行 `Saving …` 確認位置。只按 `Save and Exit`（`Save, Zip and Exit` 會把輸出目錄刪掉）。
- 「跑前停用舊輸出」只適用 `DynDOLOD_Output`（modlist 改 `-`）；TexGen 跑完要**立刻裝回 MO2 並啟用 `TexGen_Output`**，否則 DynDOLOD 報 `LOD billboard(s) not found`。輸出根：TexGen → `tools/DynDOLOD/TexGen_Output/`，DynDOLOD → `tools/DynDOLOD_Output/`（2026-09-12）。
- profile 三檔行尾不可假設一致，改檔腳本要就地偵測。
- 舊 DynDOLOD.esp 的 master 被拔掉時，DynDOLOD 報 already exists 且無法 update，只能從零重生成。

**GUI 等待**：TexGen／DynDOLOD 啟動後先停在 Options／Wizard 視窗等人按 Start；log 要到結束才寫，「等 log 出現」會空等。標題凍結＋CPU 高＝在算；標題凍結＋沒寫盤＝停在 Save 對話框等人按 `Save and Exit`（Occlusion 那段近 20 分鐘）。派線時寫死：每個 GUI 步驟先 `import -window` 截圖看有沒有對話框再等；可用 `xdotool search --name "TexGen Options"` 找視窗代按（使用者不在時才准）（2026-09-14）。

（2026-10-23 第三方快照，未實測）DynDOLOD 3.0 輸出的 plugin 排序：`DynDOLOD.esm` 排在所有 worldspace ESM 之後、`DynDOLOD.esp` 倒數第二、`Occlusion.esp` 最後（除非有 Synthesis patcher 排在最末）；用 ACMOS 類道路生成 addon 時 `DynDOLOD_SSE.ini` 先設 `Expert=1`／`Level32=1`。相關：[[dyndolod-esp-masters-pin-content-mods]]、[[vanilla-masters-cleaned-in-data]]。

## vanilla-masters-cleaned-in-data

> Update/Dawnguard/HearthFires.esm 已用 xEdit QuickAutoClean 清理並寫回遊戲 Data/；Steam Verify 會還原成髒檔、DynDOLOD 得重跑（2026-09-04）

為了 DynDOLOD 的 deleted large references 硬門檻（上游明文只能清理），`Update.esm`／`Dawnguard.esm`／`HearthFires.esm`／`ccvsvsse004-beafarmer.esl` 用 SSEEdit 4.0.4 QuickAutoClean 清過，三支 .esm 直接覆蓋遊戲 `Data/`（CRC 命中 LOOT masterlist 的已清理條目；原檔逐位元備份 `~/skyrim_mods/_lod-vanilla-master-backup-2026-09-04/`）。

這是遊戲目錄層級的改動，不在 profiles repo 版控裡；Steam「驗證檔案完整性」或重灌都會還原它們。「別按 Verify」的理由多一條，跨 session 排 Steam 下載時要明講；重灌後先比對三支 esm 的 CRC 再跑 LOD；回滾就是把備份目錄的檔案 cp 回 `Data/`。相關：[[launch-skyrim-via-steam]]。
