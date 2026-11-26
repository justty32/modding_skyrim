# 拔 mod 與隱性依賴的稽核

[lessons 索引](README.md)

裝前評估、安裝包對帳與 FOMOD 安裝在 [mod-install-audit](mod-install-audit.md)。

## rule-out-a-concept-scan-same-batch-siblings

> 使用者裁示「不要 X」時，要連同一批裡「同概念的兄弟 mod」一起掃，不能只拔名字對得上的那一個

2026-09-05 使用者裁示「不裝 Open Cities」，只拔了 `Open Cities Skyrim`，同一個 commit 裝進去的 `SR Exterior Cities`（87954，作者自稱「open cities 概念」）漏掉；使用者在 Riften 看到物件消失，問「Open Cities 是不是沒刪乾淨」——名字錯了但直覺對。使用者拒絕的是「城搬到主世界」這個玩法，不是某個 mod 名；DynDOLOD／Occlusion 是照舊佈局產的，這類 mod 一進來就會「有時候看不到東西」。

**How to apply:** 拔掉某 mod 時，同批（同一 commit／同一 install batch）裡用 Nexus 描述、tags、requirements 找同概念的兄弟（例：exterior cities／open cities／city overhaul 把室內 worldspace 搬出來的），一起列給使用者裁；並把整個概念寫進 CSV 擋死清單，不是只擋一個 id。相關：[[handoff-scope-words-expand]]（範圍用排除法寫死，但「同概念」要主動掃）。

## dyndolod-esp-masters-pin-content-mods

> 拔任何有外景改動的 mod 前先查 DynDOLOD.esp／Occlusion.esp 的 MAST；它們把內容 mod 釘成 master，拔了就缺 master 要重跑 LOD

DynDOLOD／xLODGen 輸出會覆寫內容 mod 的外景 REFR，所以把該 mod 釘進 masters（2026-09-14 例：`DynDOLOD.esp` 以 `CollegeOfWinterholdImmersive.esp` 為 master、`Occlusion.esp` 以 OCW 為 master、`DynDOLOD.esm` 以 JK's 為 master）；只停用內容 mod 會讓 LOD plugin 缺 master → 啟動 CTD。適用於仍啟用 DynDOLOD 的 profile（modpack-main 已於 2026-10-08 整組停用，見 [[new-save-plan-2026-10-04]]；`instance/profiles/dsport-dev` 仍啟用）。

**How to apply:** 任何「停用／移除 mod」的線，交接書先加一步 `instance/tools/check_masters.py --out` 再 grep 該 esp 出現在 master 欄的每一支；命中 DynDOLOD.esp／Occlusion.esp 就把「重跑 TexGen→DynDOLOD（照 want5 LOD-RUNBOOK）」列進工作量與時程，別走清 master 捷徑；剛重跑過的 LOD 也照樣得再跑。裁「留哪個」時也把這條算進去（學院三改留 OCW 一部分就因為 Occlusion.esp 依賴它）。

DynDOLOD/TexGen 的兩個 Output 要放 modlist **最高**優先權，否則 mods/ 底下 BSA 自帶的舊 terrain/object LOD 會蓋掉新產出；TexGen Fixes 的用途是蓋掉它所修的 mod，放最低等於零作用（2026-09-03）。DynDOLOD 對 unresolved reference 一次只彈一筆，不能把前置靜態掃描的候選全集當成要逐一修的清單，要以 log 實際報出的子集逐輪收斂，否則會修到大量假陽性。外觀異常混在一起時，比較 DynDOLOD／Occlusion 輸出的 mtime 與可疑 mod 的裝入時間，把「浮空/重疊城牆」（兩套內容疊在一起，靠拆分 mod 解決）跟「遠處幽靈輪廓」（LOD 比 mod 裝入早，靠重跑 LOD 解決）切開（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-09/sol/REPORT.md:30-33`）。

相關：[[dyndolod-runtime-and-traps]]、[[missing-master-scan-mast-not-housecarl]]、[[rule-out-a-concept-scan-same-batch-siblings]]。
source: instance/docs/lod/output.md:7-24；agentctl/handoffs/done/2026-09/home-2026-09-03/SESSION-LOG.md:100

## copied-fomod-choices-need-soft-dependency-audit
<a id="lorerim-copied-patches-soft-deps"></a>

> 照抄別人整合包（LoreRim）的 FOMOD 選項，會帶進為「我們沒裝的 mod」而設的補丁；這類依賴是 mesh／貼圖／初始停用 ref／位移，不在 MAST 裡，check_masters 全綠也抓不到（2026-10-18）

補丁的 MAST 只列它覆寫的 plugin；為「只有 mesh／貼圖的 mod」或「要讓位給另一個大 mod」做的選項，對方不會出現在 MAST，照抄選項時抄的是別人的 modlist 前提。例：`Great Village of Kynesgrove - 3D Wheat Patch.esp` 把 `0110CD:HearthFires.esm` 的模型指到沒裝的 3D Trees mesh（VFS ABSENT），Hearthfire 自宅小麥消失，還洗掉 USSEP 的採收物與中文名；ULP 補丁為讓位給 Frozen Lands／LOTD／Legendary Cities 把自家 ref 設成初始停用；另有引用不存在的貼圖、位移 ref、憑空改地毯與遮擋面的。這些全是 ESL、沒人拿它們當 master，`check_masters.py` 是 `present=no 0`。

**How to apply:** 照抄別人整合包的 FOMOD 選項／Patch Collection 後，除了 check_masters 再補三項：① 選項名、檔名提到的 mod 是否在 modlist 的 `+` 行；② 補丁自帶 loose nif 與 MODL 指到的 mesh／dds 在 VFS 是否 ABSENT；③ 對 master 原紀錄比初始停用旗標（0x800）、位移、base 改指。工具：`instance/tools/patch_audit.py`；單支細查 `agentctl/handoffs/home-2026-10-18/lorerim-patch-audit/tools/inspect_patch.py`（未升格）；整個 mod 的缺貼圖面 `instance/tools/smim_scan.py`。症狀是「東西消失／紫色或沒貼圖／擺設浮空或錯位」時先懷疑這類補丁，再懷疑存檔或本體。停用時拿掉 `*` 之外也把檔案改 `.mohidden`，免得遊戲當孤兒 plugin 重新啟用（[[game-rewrites-plugins-orphans-and-seq-bsa]]）。

裁示（2026-10-23）：LoreRim 借用段的這類補丁已停用、nif 已藏；Snazzy 缺的 SMIM 貼圖**只抽 34 張**做成「SMIM Textures for Snazzy (extract)」，**不整包裝 SMIM**（違反 08-30 不裝全域精修的裁示）；Ryn's Standing Stones USSEP patch 裁留。

相似但不同：esp 引用作者自己沒打包的 .pex 腳本，只會造成 Papyrus「Cannot open store」警告，不是裝壞也不會崩潰；新裝／裝回 mod 後新增這個錯誤，先比對該腳本是否存在於上游壓縮檔，整包本來就沒附就記成上游打包缺陷（2026-09-12，`agentctl/handoffs/done/2026-09/home-2026-09-12/want4/REPORT.md:96,221`）。

相關：[[rule-out-a-concept-scan-same-batch-siblings]]、[[missing-master-scan-mast-not-housecarl]]、[[fomod-install-tooling]]。
