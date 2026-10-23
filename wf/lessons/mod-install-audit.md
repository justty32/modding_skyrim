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

## pre-install-evaluation-gaps-requirements-and-prereqs

> Nexus requirements 表、使用者的前置放行、施工前的調查報告，三者都只覆蓋表面，評估裝不裝前要主動補查。

2026-08-29～10-10：Nexus 頁面 requirements 欄顯示 `none` 不代表沒前置，正文常另外寫明 CC 內容或畫質前置（Mihail 生物 mod、升龍槍系列「貼圖專用必要前置」都是正文才找得到）；官方主題合集與其收錄的 standalone 散件會重複生成內容，裝合集前要核對 Features 收錄清單逐一停用重複的 standalone esp；「缺前置」屬於全域性框架（overhaul/成人內容/全域語音）時預設判放棄，不為救一件 mod 引入整個框架；使用者對某次整包放行的前置依賴不能推廣成通用許可，每次都要重新取得明確同意；兩個地點/建築 mod 重疊前，先查 Nexus 有沒有官方 patch 或相容性建議，能省下大量自製 forward patch；中文基底換裝類常是互斥關係（必須先卸載舊漢化包、語言設英文），不是疊裝即可；施工線不要照抄前置調查報告的「已裝/未裝」結論，開工時自己重新 grep 一次 modlist/plugins。

**Why:** Nexus 結構化欄位、使用者的一次性放行、舊調查報告，都是「某個時間點/某個檢查範圍」的切片，不會自動涵蓋正文細節、新情境或現狀變化。

**How to apply:** 評估任何候選 mod 前，requirements 表之外一定讀完整 description 找 CC/INI/相容性說明；合集類先核對 Features 收錄清單找重複；前置依賴屬於全域框架就預設放棄，使用者放行只適用當次整包；重疊類任務先查官方 patch 再自製；施工開工時重新驗證前置調查的「已裝/未裝」結論，不要照抄。
source: agentctl/handoffs/done/2026-08-29/cx-mihail/REPORT.md:53；agentctl/handoffs/done/2026-10/home-2026-10-03/suramodel/REPORT.md
