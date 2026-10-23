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

2026-09-07 補：第一輪修了 USMP 蓋種族 headparts／BSA 未載入後，玩家仍回報光頭——第二輪查到完全不同的另一層：晨風地圖 mod 的 BSA 恰好帶同路徑素材，加上自己線 9/5 自動產生的 Facegen-Texture-Fix-Combined 合併包，兩者用更高優先權蓋掉了 RSC 的髮型貼圖。症狀修了但沒消失時不能假設第一輪診斷是唯一病灶，要連己方自動產生的合併包一起納入嫌疑鏈重掃。另：RSkyrimChildren.esm 與 RSChildren.bsa／RSChildren - Textures.bsa 檔名對不上，遊戲不會自動載入該 BSA 也不報錯，是整組資源從裝上那天起就沒被讀進遊戲的根本原因，建議做成常設 gate（掃「有 BSA 但沒登記且檔名不符」的 mod）。
source: agentctl/handoffs/done/2026-09/home-2026-09-07/rsc/REPORT.md:18,101

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

2026-10-23 補：archive 檔名（如帶「-DXP」）不代表安裝結果，要展開 `fomod/ModuleConfig.xml` 實際看選項樹，選對選項才是關鍵；archive 內的 `d3d11.dll`/`dxgi.dll` 若躺在跟主功能無關的子目錄（如 DAR 條件夾），多半是誤塞的 ENB 檔不是功能依賴，不要直接當成 SKSE DLL 依賴；帶多個可選變體的 archive，其原始 conflicts_n 只是上界，要先依 fomod_choice（實際會裝的那個變體）narrow 過才能報告規模；esp 埋在沒攤平的 FOMOD 子目錄（如 `10 Main/Follower/`）時 MO2 不會當 plugin 看待、plugins.txt 裡不會有它；FOMOD apply 等依賴 0-based 索引的批次腳本要明確用 `bash` 執行，zsh 陣列 1 起算會讓目錄內容整批錯位。
source: agentctl/handoffs/done/2026-09/home-2026-09-02/mco/REPORT.md:32,34,67；agentctl/handoffs/done/2026-09/home-2026-09-03/lrrev/REPORT.md:66；agentctl/handoffs/done/2026-09/home-2026-09-11/donor/REPORT.md:36；agentctl/handoffs/done/2026-10/home-2026-10-10/batch4b/REPORT.md

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

2026-09-03 補：DynDOLOD/TexGen 的兩個 Output 要放 modlist 最高優先權不是最低——2026-09-03 版 runbook 曾寫錯「放最低」，結果 mods/ 底下 33 支 BSA 自帶的舊 terrain/object LOD 排在它之上蓋掉新產出，3–6 小時整趟白跑；TexGen Fixes 的用途是蓋掉它所修的 mod，放最低優先權等於零作用。另：DynDOLOD 對 unresolved reference 一次只彈一筆，不能把前置靜態掃描出的候選全集（本場 1,096 筆）直接當成要逐一修的清單，要以 log 實際報告出來的子集為準逐輪收斂，否則會修到大量假陽性。
source: instance/docs/lod/output.md:7-24；agentctl/handoffs/done/2026-09/home-2026-09-03/SESSION-LOG.md:100

2026-10-23 補：外觀異常症狀混在一起時，比較 DynDOLOD／Occlusion 輸出的 mtime 與可疑 mod 的裝入時間，能把「浮空/重疊城牆」（兩套內容疊在一起，靠拆分 mod 解決）跟「遠處幽靈輪廓」（LOD 比 mod 裝入早，靠重跑 LOD 解決）兩類症狀切開，避免重跑 LOD 卻解決不了實體重疊問題（`agentctl/handoffs/done/2026-09/home-2026-09-09/sol/REPORT.md:30-33`）。

## copied-fomod-choices-need-soft-dependency-audit

> 照抄別人整合包（LoreRim）的 FOMOD 選項，會帶進為「我們沒裝的 mod」而設的補丁；這類依賴是 mesh／貼圖／初始停用 ref／位移，不在 MAST 裡，check_masters 全綠也抓不到（2026-10-18）

2026-10-18 Hearthfire 自宅小麥消失，真因是 `Great Village of Kynesgrove - 3D Wheat Patch.esp` 把 `0110CD:HearthFires.esm` 的模型指到沒裝的 3D Trees mesh（VFS ABSENT），還洗掉 USSEP 的採收物與中文名。順著查 LoreRim 借用段 277 支啟用 plugin，38 支＋5 個 loose nif 都是同型：ULP 補丁為讓位給 Frozen Lands／LOTD／Legendary Cities，把 103 個自家 ref 設成初始停用；Daedric Shrines、Praedy's Castle Volkihar 選項引用不存在的貼圖；New Dibella Statues 補丁把 20 個 ref 位移；Rugnarok、SPO 補丁憑空改地毯與遮擋面。38 支全是 ESL、沒人拿它們當 master——`check_masters.py` 一直是 `present=no 0`。

**Why:** 補丁的 MAST 只列它覆寫的 plugin。為「只有 mesh／貼圖的 mod」或「要讓位給另一個大 mod」做的選項，對方根本不會出現在 MAST；照抄選項時抄的是別人的 modlist 前提。
**How to apply:**
- 照抄別人整合包的 FOMOD 選項／Patch Collection 後，除了 check_masters 再補三項：① 選項名、檔名提到的 mod 是否在 modlist 的 `+` 行；② 補丁自帶 loose nif 與 MODL 指到的 mesh／dds 在 VFS 是否 ABSENT；③ 對 master 原紀錄比初始停用旗標（0x800）、位移、base 改指。
- 現成可重跑工具：`instance/tools/patch_audit.py`（2026-10-23 自 handoffs 升格）；單支補丁細查用 `agentctl/handoffs/home-2026-10-18/lorerim-patch-audit/tools/inspect_patch.py`（未升格）；整個 mod 的缺貼圖面用 `instance/tools/smim_scan.py`。
- 症狀是「東西消失／紫色或沒貼圖／擺設浮空或錯位」時，先懷疑這類補丁，再懷疑存檔或本體。
- 停用時拿掉 `*` 之外也把檔案改 `.mohidden`，免得遊戲當孤兒 plugin 重新啟用（[[game-rewrites-plugins-orphans-and-seq-bsa]]）。
相關：[[rule-out-a-concept-scan-same-batch-siblings]]、[[missing-master-scan-mast-not-housecarl]]、[[fomod-install-tooling]]。

（2026-10-23 補；記憶條目 `lorerim-copied-patches-soft-deps` 即本條）處置結果：38 支＋5 nif 中已停 37 支＋藏 nif；
Snazzy 缺的 SMIM 貼圖**只抽 34 張**做成「SMIM Textures for Snazzy (extract)」，**不整包裝 SMIM**（違反 08-30 不裝全域精修的裁示）；
Ryn's Standing Stones USSEP patch 裁留。

2026-09-12 補：還有一種非「軟依賴缺件」的相似症狀要分清——esp 引用了作者自己沒打包進壓縮檔的 .pex 腳本，只會造成 Papyrus「Cannot open store」警告，不是裝壞也不會崩潰；三個獨立場次（want4/want5/zhfix2）都是同型。新裝/裝回 mod 後新增這個錯誤，先比對該腳本是否存在於上游壓縮檔裡，整包本來就沒附的話記成上游打包缺陷，不用當本線裝壞去查。
source: agentctl/handoffs/done/2026-09/home-2026-09-12/want4/REPORT.md:96,221

## temp-dirs-double-as-offline-reinstall-library

> 暫存目錄實際上兼任離線重裝庫；清理前要先分「可重抓／不可重抓」，不是先分「備份／下載暫存」。

2026-10-23 全工作區大整理：使用者裁示 `~/skyrim_mods/_*` 39 夾（~13 GB）全刪並執行。事後 T5 查證發現，10-17 標 keep 的 303 個「庫內唯一原檔」**全部位於 `_dl-*` 下載暫存夾**，刪除後 300/303（9.996 GiB）全機已無第二份——下載暫存一直默默兼任著離線重裝庫，但沒有任何文件把它標成這個角色。實際損失比帳面小：81.5%（bytes 計）經 housecarl nexus 工具逐筆查證仍可從 Nexus 重抓，真正不可回復只有 2 筆 23 MB。

**Why**：「備份 vs 下載暫存」的分類答錯了問題——下載暫存裡躺著的可能是全機唯一副本，而「備份」裡的東西反而可能處處有第二份。決定可不可以刪的軸是**可回復性**，不是目錄名。

**How to apply**：清理任何暫存／下載目錄前，先對內容物回答兩個問題：(1) 全機（含 MO2 downloads、mod-library）還有沒有第二份？(2) 沒有第二份的，上游（Nexus 等）還抓不抓得到（下架／改版／登入牆）？「無第二份＋上游抓不到」的才是真不可回復，要嘛留要嘛先異地備份；其餘都可刪。查證用 housecarl_nexus_identify（md5）／housecarl_nexus_mod files=true／housecarl_nexus_search。範例查證報告：`agentctl/handoffs/home-2026-10-23/tidy/T5/REPORT.md`。


## nexus-identity-confusion-many-forms

> 名稱／摘要／縮寫／記憶都可能把不相關的 mod 誤認成同一個；判準永遠是 mod id／byte-exact／實測內容，不是字面。

2026-08-27～10-18 跨多條線反覆踩到同型坑：SCAR(72014) vs SCAR VR(89492)、SCAR vs Smooth Combat Non Combat Animation 縮寫相近但無關；DAC 縮寫同時指向三個不相關 mod；Immersive Citizens AI Overhaul(Shurah) 與 AI Overhaul(janquadrant) 目標相同機制不同。摘要行也會誤導：Shadow of Skyrim summary 寫「不用存讀檔」像「受傷不死」，讀完整 description 才知道是另一套機制；使用者記得的舊愛 mod 名字 5 筆裡 3 筆直覺是錯的。通用命名（「All in one」）要用 byte-exact＋houseCARL 反查實際 provide 的檔案才能定身分；關鍵字搜尋零命中可能是頁面標題與落地檔名完全不同（SIGMA 系列）；可選檔案的檔名甚至會跟效果方向相反（`Melana_CM_Evolve2xSlower` 實際更慢）；查無 Nexus 來源時先核對是否為上游整合包自製 patch（沒有外部來源可抓）；選版相容性要找「明確列版本＋實測回報」的檔案，不要只憑「version independent」字樣；名稱比對即使兩層正規化、門檻寧漏不誤判，仍會誤配（關鍵字誤命中 NPC 名 Lod）。

**Why:** 這些誤判來源各自獨立（頁面摘要、使用者記憶、通用命名、縮寫巧合、FOMOD 選配檔名、自動比對演算法），共同點是都繞過了「用 id/byte/內容核對」這道關卡。

**How to apply:** 認定一個 mod 的身分前一律核對 Nexus mod id，不用縮寫／頁面標題字面比對；摘要/summary/檔名只當線索不當結論，可疑時讀完整 description 或實測內容；關鍵字零命中時改用已知/反查到的 mod id 再搜一輪；`ask-status` 類「搜尋異常」優先假設是子頁/翻譯頁/命名差異，追到本體頁再判定。
source: agentctl/handoffs/done/2026-08-27/cx-dl2/HANDOFF.md:56；agentctl/handoffs/done/2026-08-27/opus-gaps/staging/recall-lost-favorites-2026-08-27.md:345,350；agentctl/handoffs/done/2026-09/home-2026-09-02/lrdl/REPORT.md:31

## library-and-ingest-bookkeeping-fields-lie

> 下載佇列／庫存索引／衍生清單的「狀態欄」常常是過期快照，不代表磁碟或 Nexus 的真實現狀；要嘛重讀檔案系統，要嘛用 id/byte/md5 核對。

2026-08-27～10：`library_hit`／`status=DOWNLOADED` 欄位不保證磁碟真的有檔；庫存檔名有兩種命名慣例，只認一種把 91 件庫存少算成 69 件；`sizeInBytes=null` 是查詢缺口不是死檔，`=0` 才是；Nexus row-name 生成的落地檔名可能跟 manifest 不同但 id/byte 仍對得上；衍生 json 候選清單可能只是 prose 的子集（25 列漏了本機已有的候選）；前置框架常手動安裝、`meta.ini` 的 `modid=0`，用 id 掃描會全部誤報未裝；就地修補已部署 ESP 不會同步回 mod-library 來源，下次自動 redeploy 會悄悄覆蓋掉修正；`MANIFEST.sha256` 要 `cat` 全檔，`head -5` 曾漏看排第 7 行的目標差點誤刪；入庫 dedupe 只比對「來源↔庫」會漏掉瀏覽器重複下載出的 `X.7z`/`X (1).7z`；無時間戳的 legacy 檔名裡的 id 不可信要 md5 回溯；判斷是不是 mod 不能只看副檔名（行為檔/BodySlide/SkyProc patcher 沒有頂層 .esp/meshes）。

**Why:** 這些欄位都是某個時間點的快照或簡化表示，產生它的流程本身有已知盲區，不會隨實際狀態自動更新。

**How to apply:** 任何「已下載／已入庫／已裝」的判定，狀態欄只當起點：核對磁碟路徑是否存在、用 mod_id+file_id+bytes 或 md5 比對、框架類前置改用目錄名+實體檔案驗證；MANIFEST 類清單一律 `cat` 不 `head`；就地改動已部署且由自動化管線管理的檔案後要馬上同步回來源層；衍生候選清單要對照 prose/README 交叉核對完整性。
source: agentctl/handoffs/done/2026-09/home-2026-09-03/lrrev/REPORT.md:191；agentctl/handoffs/done/2026-08-27/opus-gaps/_COMMON-LIMITS.md:17；mod-library/README.md:36-58

## asset-existence-and-overlay-diagnosis-needs-multilayer

> 「這東西存不存在／有沒有被蓋掉」不能只查一層；record 層、原版 BSA、同路徑跨 mod 覆蓋序，任一層漏查都會下錯結論。

2026-08-30～10-09：判斷 mod A 是否覆蓋 mod B，檔案路徑交集為 0 不代表沒衝突——兩個 mod 可能用完全不同檔名表達同一護甲槽，要查 record 層（ARMA model path 實際解析到哪個檔案）才知道真贏家；「某類資產是否存在」要五層都查完才能下「不存在」結論：壓縮檔列表、已安裝 loose files、BSA 內容原始位元組掃描、本機 DB regex、md5 回溯，少一層就要標 UNKNOWN；查缺件工具若只掃鬆散檔與 mod 自己的 BSA、不掃原版遊戲 BSA，會把原版自帶檔案誤判成「缺件」；UI 面板消失但沒報錯時，真因常是另一個 mod 用更舊版本的同路徑資產（如 `interface/*.swf`）覆蓋序更高，要在全 mods 目錄找所有同路徑同名資產逐一比對內容特徵，不能只查功能 mod 自己的 log。

**Why:** 檔案路徑交集、工具自己的索引範圍、功能 mod 自身的 log，三者都只是「真相」的子集，各有結構性盲區。

**How to apply:** 查「覆蓋/相容」類問題除了檔案路徑交集一定加 record-level 解析（houseCARL resolve/cross_plugin_query）；查「存不存在」依序跑完五層再宣告「不存在」；查「功能/UI 消失但無錯誤」先 find 全 mods 目錄同路徑資產，列優先序與內容特徵再判贏家。相關：[[missing-master-scan-mast-not-housecarl]]。
source: agentctl/handoffs/done/2026-08-30/bikini-2026-08-30/FINDINGS.md:25-73；agentctl/handoffs/done/2026-10/home-2026-10-09/crash/REPORT-console.md

2026-10-23 補（E2bs-13）：「部分部位貼圖壞但不是全部」這類局部缺失，yva 線的做法是建一次 esp→ARMO→ARMA→nif→BSShaderTextureSet 全鏈路索引（對全部啟用 mod 的 loose＋BSA），逐貼圖路徑判 WINS／BSA／ABSENT 三類，再拿原始 FOMOD 包清單核對 ABSENT 是否原本就沒附——33 條 ABSENT 全數歸因成「上游漏檔／optional 沒裝／無害執行期覆蓋」（`agentctl/handoffs/done/2026-09/home-2026-09-19/yva/REPORT.md:14-37`）。

## engine-file-loading-mechanics-not-intuitive

> plugin/資產贏家判定有一串違反直覺的引擎規則，不能用副檔名、modlist 位置或檔名猜；要讀 TES4 flag／實際 conflict tree／skse64.log。

2026-09～10 跨線反覆驗證：`.esl` 副檔名一律贏過所有 ESP 不管 modlist 位置多低，ESPFE（esp+ESL旗標）保留原位置不一定贏，判 light master 要讀 TES4 header `0x200` 不能猜；`Skyrim.ccc` 裡落地的 plugin 是隱含 master、不受 plugins.txt 勾選控制（70 件 CC 落地會讓隱含 master 從 13 跳到 75-80）；拔一般 esp 型 mod，Skyrim 按名字重新對應不會讓其他 plugin FormID 位移，真正留痕的是殘留腳本而非槽位；BSA 檔名若跟自己 plugin 不同名，遊戲不會自動載入也不報錯（RS Children 踩過兩輪：BSA 不同名先漏一次，修完又被另兩個 mod 更高優先權蓋掉）；「Alternate Armors」算 1 件 mod 實際是 14 個獨立 plugin，估算規模要用檔案數不是 mod 名稱數；多包一層頂層 `data/` 會讓 MO2 VFS 映射成 `Data/data/...`，整包死檔不報錯；ESLified 補丁重排 FormID，換裝後存檔寫入即不可逆，所有 addon 要全套跟著換；modlist（檔案優先權）與 plugins.txt（紀錄勝者）方向沒對齊會做出自相矛盾的混合狀態；「有沒有東西流失」才是要不要建 forward patch 的判準，不是 winner 是誰；「Plugin Replacer」只換 esp 不換 bsa，要新舊都啟用用排序贏；兩個 mod 給同名 DLL/INI 要看 skse64.log 確認載入哪個版本；評估「只改某 CELL」的 mod 常連帶覆寫 persistent ACHR 所需的 WRLD 頂層與外層 persistent CELL，是引擎結構性要求；有些原版 GMST 是引擎硬編預設值、esm 裡沒有該 record，衝突檢查要按 EditorID 不能按 FormID；navmesh 若雙方都是實質改動（非 CK ±1 頂點雜訊），排序只會讓一邊整片退化，要停工列選項給使用者裁示。

**Why:** 這些都是「看起來應該怎樣」跟「引擎實際怎麼做」對不上的地方，要讀 TES4 flag/record 或看 houseCARL conflict tree/skse64.log 等執行期證據才知道。

**How to apply:** 裝完任何借用/覆蓋件第一步讀安裝後實際 winner（houseCARL resolve/conflict tree 或 skse64.log），不要用副檔名/modlist 位置/檔名猜；部署 CC/框架前先查 implicit master 數；懷疑 mod「裝了沒效果」先核對 BSA 檔名是否與 plugin 同名、VFS 底下有沒有多包一層 `data/`；GMST/navmesh 類衝突查無結果就改查 EditorID 或停工回報，不要硬排序。相關：[[game-rewrites-plugins-orphans-and-seq-bsa]]。
source: agentctl/handoffs/done/2026-09/home-2026-09-03/ae2/REPORT.md:104；agentctl/handoffs/done/2026-09/home-2026-09-07/rsc/REPORT.md:18,101；agentctl/handoffs/done/2026-10/home-2026-10-10/batch3/REPORT.md

## runtime-state-mechanics-not-file-based

> mod 的某些狀態活在存檔／執行期而非檔案層，裝新版 esp、改覆寫層、或用載入期篩選工具都動不了它。

2026-10：用 GLOBAL 控制數值且已寫入存檔的設定（如 DAc0da 延後開始等級），重裝新版 esp 不會回溯更新存檔裡的舊值，必須玩家手動主控台 `set` 覆蓋；OBody NG 的快捷鍵是 Papyrus 屬性存在存檔裡，MCM 改鍵會呼叫 `OnOptionKeyMapChange` 寫回存檔，覆寫層（layer_apply）完全碰不到，只能進遊戲用 MCM 改；SkyPatcher 這類「載入期依基底屬性篩選」的工具，對 NFF 之類「執行期才把普通 NPC 收成隨從」的情況天生擋不到，因為那些 NPC 的基底一開始沒有隨從 faction。

**Why:** 檔案層的改動只在遊戲讀取那一刻生效一次；一旦值被寫進存檔或由執行期腳本動態轉換身份，之後的檔案層修改就追不上去。

**How to apply:** 收到「改某設定/排除某類 NPC」需求前，先確認目標是存在 ini/esp（可覆寫層）還是存檔內 Papyrus 屬性/GLOBAL（只能進遊戲或主控台改）；用 SkyPatcher/SPID 類工具做排除清單時要在交接書寫明「無法涵蓋執行期才轉換身份的對象」，不要承諾完全涵蓋。
source: agentctl/handoffs/done/2026-10/home-2026-10-10/batch2/REPORT.md；agentctl/handoffs/done/2026-10/home-2026-10-03/obodykey/REPORT.md

## mod-library-cleanup-tooling-constraints

> `mod-library` 的清理工具（quarantine.py／scan_mod_library.py／esp_refscan.py／verify_merge.py）都刻意或無意地留了邊界，要先摸過才能信。

2026-08-28～10-10：`quarantine.py` 不提供自由查詢選擇器，只有具名 selector，理由是「搬掉所有符合 filter 的東西正是弄丟不該丟檔案的方式」——沒有對應 selector 時寫外部腳本 `import quarantine` 注入新字典項，不改本體；隔離單位是 Mongo doc（以 sha256 為鍵），同一 sha256 多路徑會一次全搬走，無法只留現役那一份；`rm -rf` 目錄樹前要先掃有沒有被索引過的巢狀 archive，有就先 quarantine 移出；「工具解壓目錄」裡 mtime 晚於解壓內容的檔案是執行期工作狀態，要單獨備份不能整棵刪；排除集合要明確涵蓋「已經隔離過」，漏掉會把已處理項目重新選中；`scan_mod_library.py` 只統計壓縮檔，142 GB 裡有 46 GiB 解壓殘留/備份完全不在報表上，要另外 `du` 比對；重建 merge plugin 後不要只信自帶 `verify_merge.py` PASS，要用獨立讀取路徑再抽驗；`esp_refscan.py` 只吃唯一 Skyrim.esm master，多 master/NAVI 會中斷，要改走 esplib 手動查並在 REPORT 註明是工具限制。

**Why:** 這些邊界來自工具的設計取捨（寧可少做也不要誤刪）或掃描範圍的技術限制，不知道就會把「工具沒做到」誤判成「已經查過/清過」。

**How to apply:** 用 `mod-library/db/quarantine.py` 前先確認 selector 涵蓋範圍，沒有就外部注入不改本體；大量刪除前一律先掃 Mongo 索引與 mtime 時間戳；信任任何「自帶驗證腳本 PASS」或「掃描工具零結果」前，先問它的已知範圍邊界在哪。
source: agentctl/handoffs/done/2026-08-28/opus-lib-clean/STATE.md；agentctl/handoffs/done/2026-08-28/opus-lib-tidy/STATE.md

## destructive-action-safety-and-rollback-limits

> 刪除/停用類操作的「安全」要分清三件事：腳本本身有沒有保險、備份放哪裡可逆、已進場存檔的東西回滾程度有限。

2026-08-30～09-05：批次刪除腳本三道保險值得當範本——偵測 MO2/遊戲在跑就 abort、預期筆數與實際變動筆數不符就斷言失敗、真正清除前先 mv 到暫存垃圾目錄待確認能正常啟動才二次確認清掉；回滾備份放 `/tmp`（tmpfs）重開機會永久消失（Bandolier 3.2GB 真的沒了）；有 hand-placed REFR/ACHR 的 mod，「乾淨回滾」只保證安裝前停用乾淨，已進場存檔中途停用只是讓引擎忽略失去來源的 FormID，可能留 orphaned changeforms；跨時間差的刪除操作要在動手當下重讀現行狀態，不採信計畫檔舊快照；CC 內容已在本周目被存檔載入過，中途拔除可能 missing-master 警告、任務物品消失，最安全時機是下個新周目；停用但不刪的 mod 多數有用途，判能不能刪要先查下游 master 相依、再查可還原性，最後才看空間；體積異常小的下載檔先 `7z t` 實測，判壞損也不得私自換源，只能 BLOCKED；多線並行寫同一 profile repo 時「工作樹要乾淨」只能限定本線負責路徑或改單一寫者序列套用；覆寫原版 Papyrus 腳本（不吃 esp 不碰 SEQ）的任務型 mod，拔掉立即生效不需要新開局——跟「改 quest flags/SEQ」需要新周目是兩回事，先查機制再判斷風險。

**Why:** 「可以刪/可以停用」要拆成腳本執行安全、備份媒介的持久性、和已進場存檔的引擎行為三層，各自失敗模式不同。

**How to apply:** 寫刪除/大量修改腳本套這三道保險；回滾備份放非 tmpfs 的實體路徑；評估「中途拔除」風險先查該內容是否已被本周目存檔載入過、是覆寫腳本還是改 flags/SEQ；刪除前一律當下重讀現行狀態；判斷能不能刪先查下游相依與可還原性再看空間。
source: agentctl/handoffs/done/2026-08-30/purge-2026-08-30/README.md:28-31；agentctl/handoffs/done/2026-09-01/hgate-2026-09-01/bandolier/FINDINGS.md

## pre-install-evaluation-gaps-requirements-and-prereqs

> Nexus requirements 表、使用者的前置放行、施工前的調查報告，三者都只覆蓋表面，評估裝不裝前要主動補查。

2026-08-29～10-10：Nexus 頁面 requirements 欄顯示 `none` 不代表沒前置，正文常另外寫明 CC 內容或畫質前置（Mihail 生物 mod、升龍槍系列「貼圖專用必要前置」都是正文才找得到）；官方主題合集與其收錄的 standalone 散件會重複生成內容，裝合集前要核對 Features 收錄清單逐一停用重複的 standalone esp；「缺前置」屬於全域性框架（overhaul/成人內容/全域語音）時預設判放棄，不為救一件 mod 引入整個框架；使用者對某次整包放行的前置依賴不能推廣成通用許可，每次都要重新取得明確同意；兩個地點/建築 mod 重疊前，先查 Nexus 有沒有官方 patch 或相容性建議，能省下大量自製 forward patch；中文基底換裝類常是互斥關係（必須先卸載舊漢化包、語言設英文），不是疊裝即可；施工線不要照抄前置調查報告的「已裝/未裝」結論，開工時自己重新 grep 一次 modlist/plugins。

**Why:** Nexus 結構化欄位、使用者的一次性放行、舊調查報告，都是「某個時間點/某個檢查範圍」的切片，不會自動涵蓋正文細節、新情境或現狀變化。

**How to apply:** 評估任何候選 mod 前，requirements 表之外一定讀完整 description 找 CC/INI/相容性說明；合集類先核對 Features 收錄清單找重複；前置依賴屬於全域框架就預設放棄，使用者放行只適用當次整包；重疊類任務先查官方 patch 再自製；施工開工時重新驗證前置調查的「已裝/未裝」結論，不要照抄。
source: agentctl/handoffs/done/2026-08-29/cx-mihail/REPORT.md:53；agentctl/handoffs/done/2026-10/home-2026-10-03/suramodel/REPORT.md
