# 裝／拔 mod 的稽核

[lessons 索引](README.md)

## rs-children-missing-esp

> 2026-09-09 第五輪才抓到：RS Children 光頭／大媽臉真因是安裝包兩支 plugin 只裝了 Core 的 RSkyrimChildren.esm，帶 44 筆原版小孩 NPC_ 覆寫的 RSChildren.esp 從沒進載入序；前四輪只查已裝的東西沒對安裝包（原 type: project）

RS Children Overhaul 1.1.3HF1 安裝包：`00 - Core/RSkyrimChildren.esm`（種族／頭部零件／裝備、8 個範本 NPC）
＋ `01 - ESP/<Playable|Non Playable>[ - USSEP]/RSChildren.esp`（44 筆原版小孩 NPC_ 覆寫）。
2026-09-03 只裝了 Core；09-07～09-09 四輪查素材、種族、NPC 層都「帳面正確」，因為都在查已裝的東西。
09-09 調度者親查：在使用者旁 placeatme Braith 與 RSC 範本小孩 → 「兩個都有頭髮、都是大媽臉」，
再對安裝包才發現少一支 esp。Face Discoloration Fix 讓「不符」表現成成人素頭而非黑臉。

**How to apply:**
- 任何 mod「裝了但沒效果」先對**安裝包內容 vs 實際裝了什麼**（`7z l` 列 plugin／FOMOD ModuleConfig），
  再查記錄層；FOMOD 多步驟安裝最容易漏後面的步驟。
- 修法（2026-09-09 交 lead-audit）：裝 `Non Playable - USSEP` 變體、放 USSEP 與 esm 之後，
  再做 forward patch 把它的臉欄位推過 AI Overhaul 等蓋小孩的 mod；`RSC-ChildRace-Restore-B` 保留。
- 結果：2026-09-09 22:5x 補裝＋forward 後使用者親眼確認**成功**。第一次驗收無效是因為 forward patch 寫進 plugins.txt 時漏了 `*`——**profile 寫入的驗收要實讀那一行有沒有 `*`**，houseCARL 鏡像的「贏家」不等於遊戲真的啟用。
- 相關 [[look-layer-must-carry-hdpt-flst-clfm]]、[[verify-waituser-against-logs]]。

## fomod-install-tooling

> 2026-09-19 起裝 FOMOD 包一律走 instance/tools/fomod/（inspect→plan→apply→audit），選項寫進交接書給使用者拍板；Yvanni 09-08 只抄 Base/ 是教訓（原 type: memory）

2026-09-19 使用者定調：「我們現在的安裝方式對 FOMOD 型式的安裝包很不友好，這筆投資勢必要的」。
fomod 線建了 `instance/tools/fomod/`（fomodlib／inspect／plan／apply／audit／audit_all，57 個測試），runbook 在 `agentctl/docs/fomod-install-runbook.md`。

**Why:** Yvanni（163745）09-08 安裝時 agent 只抄 FOMOD `Base/`＋facegen，三個必選群組整組漏，玩到 09-19 才發現身體／鎧甲全壞；盤點後 mods-scan 另找到 Evolving Locations×3、BDS-CPM 同型漏裝。manifest 的 `fomod_choices` 857 筆幾乎全 `unrecorded`。
**How to apply:**
- 交接書裡裝 FOMOD 包的步驟固定寫：`fomod_inspect` 列選項 → 選項＋理由寫進交接書給使用者拍板（推不出取 Required/Recommended，再不行照 modpack 慣例：CT77 清涼鎧甲、CBBE、有中文選中文）→ `fomod_plan` → `fomod_apply --apply`（dry-run 預設、0 覆蓋）→ 目錄留 `fomod-choices.json` → 回填 manifest。
- 驗收用 `fomod_audit.py <archive> <mod dir>` 要 complete；base-only／partial 就是白裝。
- 上游 FOMOD 的「Needed for textures」選配需求也要看（Yvanni 的 Anchorite／Battle Queen 貼圖在別的 mod）。
相關：[[face-bugs-check-real-actor-and-upstream-fomod]]、[[investigate-all-then-install-once]]

## rule-out-a-concept-scan-same-batch-siblings

> 使用者裁示「不要 X」時，要連同一批裡「同概念的兄弟 mod」一起掃，不能只拔名字對得上的那一個（原 type: memory）

2026-09-05 使用者裁示「不裝 Open Cities」，lrin 線只拔了 `Open Cities Skyrim`；同一個 commit 裝進去的 `SR Exterior Cities`（87954，作者自稱「open cities 概念」，把五個城搬進主世界）沒人發現，隔天使用者在 Riften 看到物件消失，直覺說「Open Cities 是不是沒刪乾淨」——名字錯了但直覺對。

**Why:** 使用者拒絕的是「城搬到主世界」這個玩法，不是某個 mod 名。DynDOLOD／Occlusion 是照舊佈局產的，這類 mod 一進來就會「有時候看不到東西」。
**How to apply:** 拔掉某 mod 時，同批（同一 commit／同一 install batch）裡用 Nexus 描述、tags、requirements 找同概念的兄弟（例：exterior cities／open cities／city overhaul 把室內 worldspace 搬出來的），一起列給使用者裁；並把整個概念寫進 CSV 擋死清單，不是只擋一個 id。相關：[[handoff-scope-words-expand]]（範圍用排除法寫死，但「同概念」要主動掃）。

## dyndolod-esp-masters-pin-content-mods

> 拔任何有外景改動的 mod 前先查 DynDOLOD.esp／Occlusion.esp 的 MAST；它們把內容 mod 釘成 master，拔了就缺 master 要重跑 LOD（原 type: memory）

2026-09-14 冬駐學院三改互蓋（JK's＋ICOW＋OCW 同時啟用）要拔 ICOW 時，`instance/tools/check_masters.py` 顯示 `DynDOLOD.esp` 以 `CollegeOfWinterholdImmersive.esp` 為 master、`Occlusion.esp` 以 OCW 為 master、`DynDOLOD.esm` 以 JK's 為 master。

**Why:** DynDOLOD／xLODGen 輸出會覆寫內容 mod 的外景 REFR，所以把該 mod 釘進 masters；只停用內容 mod 會讓 LOD plugin 缺 master → 啟動 CTD。09-12 才重跑過的 LOD 也照樣得再跑（36 分＋收尾）。

**How to apply:** 任何「停用／移除 mod」的線，交接書要先加一步 `check_masters.py --out` 再 grep 該 esp 出現在 master 欄的每一支；命中 DynDOLOD.esp／Occlusion.esp 就把「重跑 TexGen→DynDOLOD（照 want5 LOD-RUNBOOK）」列進工作量與時程，別走清 master 捷徑。裁「留哪個」時也把這條算進去（本次留 OCW 一部分就因為 Occlusion.esp 依賴它）。相關：[[dyndolod-runtime-and-traps]]、[[missing-master-scan-mast-not-housecarl]]、[[rule-out-a-concept-scan-same-batch-siblings]]。

## copied-fomod-choices-need-soft-dependency-audit

> 照抄別人整合包（LoreRim）的 FOMOD 選項，會帶進為「我們沒裝的 mod」而設的補丁；這類依賴是 mesh／貼圖／初始停用 ref／位移，不在 MAST 裡，check_masters 全綠也抓不到（2026-10-18）

2026-10-18 Hearthfire 自宅小麥消失，真因是 `Great Village of Kynesgrove - 3D Wheat Patch.esp` 把 `0110CD:HearthFires.esm` 的模型指到沒裝的 3D Trees mesh（VFS ABSENT），還洗掉 USSEP 的採收物與中文名。順著查 LoreRim 借用段 277 支啟用 plugin，38 支＋5 個 loose nif 都是同型：ULP 補丁為讓位給 Frozen Lands／LOTD／Legendary Cities，把 103 個自家 ref 設成初始停用；Daedric Shrines、Praedy's Castle Volkihar 選項引用不存在的貼圖；New Dibella Statues 補丁把 20 個 ref 位移；Rugnarok、SPO 補丁憑空改地毯與遮擋面。38 支全是 ESL、沒人拿它們當 master——`check_masters.py` 一直是 `present=no 0`。

**Why:** 補丁的 MAST 只列它覆寫的 plugin。為「只有 mesh／貼圖的 mod」或「要讓位給另一個大 mod」做的選項，對方根本不會出現在 MAST；照抄選項時抄的是別人的 modlist 前提。
**How to apply:**
- 照抄別人整合包的 FOMOD 選項／Patch Collection 後，除了 check_masters 再補三項：① 選項名、檔名提到的 mod 是否在 modlist 的 `+` 行；② 補丁自帶 loose nif 與 MODL 指到的 mesh／dds 在 VFS 是否 ABSENT；③ 對 master 原紀錄比初始停用旗標（0x800）、位移、base 改指。
- 現成可重跑工具：`agentctl/handoffs/home-2026-10-18/lorerim-patch-audit/tools/audit.py`、`inspect_patch.py`；整個 mod 的缺貼圖面用 `smim-eval/tools/smim_scan.py`。
- 症狀是「東西消失／紫色或沒貼圖／擺設浮空或錯位」時，先懷疑這類補丁，再懷疑存檔或本體。
- 停用時拿掉 `*` 之外也把檔案改 `.mohidden`，免得遊戲當孤兒 plugin 重新啟用（[[game-rewrites-plugins-orphans-and-seq-bsa]]）。
相關：[[rule-out-a-concept-scan-same-batch-siblings]]、[[missing-master-scan-mast-not-housecarl]]、[[fomod-install-tooling]]。

（2026-10-23 補；記憶條目 `lorerim-copied-patches-soft-deps` 即本條）處置結果：38 支＋5 nif 中已停 37 支＋藏 nif；
Snazzy 缺的 SMIM 貼圖**只抽 34 張**做成「SMIM Textures for Snazzy (extract)」，**不整包裝 SMIM**（違反 08-30 不裝全域精修的裁示）；
Ryn's Standing Stones USSEP patch 裁留。

## temp-dirs-double-as-offline-reinstall-library

> 暫存目錄實際上兼任離線重裝庫；清理前要先分「可重抓／不可重抓」，不是先分「備份／下載暫存」。

2026-10-23 全工作區大整理：使用者裁示 `~/skyrim_mods/_*` 39 夾（~13 GB）全刪並執行。事後 T5 查證發現，10-17 標 keep 的 303 個「庫內唯一原檔」**全部位於 `_dl-*` 下載暫存夾**，刪除後 300/303（9.996 GiB）全機已無第二份——下載暫存一直默默兼任著離線重裝庫，但沒有任何文件把它標成這個角色。實際損失比帳面小：81.5%（bytes 計）經 housecarl nexus 工具逐筆查證仍可從 Nexus 重抓，真正不可回復只有 2 筆 23 MB。

**Why**：「備份 vs 下載暫存」的分類答錯了問題——下載暫存裡躺著的可能是全機唯一副本，而「備份」裡的東西反而可能處處有第二份。決定可不可以刪的軸是**可回復性**，不是目錄名。

**How to apply**：清理任何暫存／下載目錄前，先對內容物回答兩個問題：(1) 全機（含 MO2 downloads、mod-library）還有沒有第二份？(2) 沒有第二份的，上游（Nexus 等）還抓不抓得到（下架／改版／登入牆）？「無第二份＋上游抓不到」的才是真不可回復，要嘛留要嘛先異地備份；其餘都可刪。查證用 housecarl_nexus_identify（md5）／housecarl_nexus_mod files=true／housecarl_nexus_search。範例查證報告：`agentctl/handoffs/home-2026-10-23/tidy/T5/REPORT.md`。
