# 裝 mod 的稽核（裝前評估、安裝包對帳、FOMOD）

[lessons 索引](README.md)

拔 mod 前的稽核與照抄選項的隱性依賴在 [mod-removal-and-soft-deps](mod-removal-and-soft-deps.md)。

## rs-children-missing-esp

> mod「裝了但沒效果」先對安裝包內容 vs 實際裝了什麼：RS Children 光頭／大媽臉的真因是只裝了 Core 的 RSkyrimChildren.esm，帶 44 筆原版小孩 NPC_ 覆寫的 RSChildren.esp 從沒進載入序（2026-09-09）

RS Children Overhaul 1.1.3HF1 安裝包：`00 - Core/RSkyrimChildren.esm`（種族／頭部零件／裝備、8 個範本 NPC）＋ `01 - ESP/<Playable|Non Playable>[ - USSEP]/RSChildren.esp`（44 筆原版小孩 NPC_ 覆寫）。只裝 Core 時素材、種族、NPC 層都「帳面正確」，只查已裝的東西找不到；placeatme 原版小孩（Braith）與 RSC 範本小孩對照「兩個都有頭髮、都是大媽臉」，對安裝包才切開。Face Discoloration Fix 讓「不符」表現成成人素頭而非黑臉。

**How to apply:** 任何 mod「裝了但沒效果」先對**安裝包內容 vs 實際裝了什麼**（`7z l` 列 plugin／FOMOD ModuleConfig），再查記錄層；FOMOD 多步驟安裝最容易漏後面的步驟。RSC 的修法：裝 `Non Playable - USSEP` 變體、放 USSEP 與 esm 之後，再做 forward patch 把臉欄位推過 AI Overhaul 等蓋小孩的 mod；`RSC-ChildRace-Restore-B` 保留（2026-09-09 使用者親眼確認**成功**）。

**profile 寫入的驗收要實讀 plugins.txt 那一行有沒有 `*`**（forward patch 漏 `*` 會讓驗收無效），houseCARL 鏡像的「贏家」不等於遊戲真的啟用。症狀修了沒消失時，不能假設第一個診斷是唯一病灶，要連己方自動產生的合併包一起納入嫌疑鏈重掃（例：晨風地圖 mod 的 BSA 與自產的 Facegen-Texture-Fix-Combined 合併包以更高優先權蓋掉 RSC 的髮型貼圖）。esm 與 BSA 檔名對不上（RSkyrimChildren.esm vs RSChildren.bsa／RSChildren - Textures.bsa）時遊戲不會自動載入該 BSA 也不報錯；建議做成常設 gate（掃「有 BSA 但沒登記且檔名不符」的 mod）。

相關 [[look-layer-must-carry-hdpt-flst-clfm]]、[[verify-waituser-against-logs]]。
source: agentctl/handoffs/done/2026-09/home-2026-09-07/rsc/REPORT.md:18,101

## fomod-install-tooling

> 裝 FOMOD 包一律走 instance/tools/fomod/（inspect→plan→apply→audit），選項寫進交接書給使用者拍板（2026-09-19 起）

2026-09-19 使用者定調：「我們現在的安裝方式對 FOMOD 型式的安裝包很不友好，這筆投資勢必要的」。流程（`fomod_inspect` 列選項 → 選項＋理由寫進交接書給使用者拍板 → `fomod_plan` → `fomod_apply --apply` → 留 `fomod-choices.json` → 回填 manifest）、選不出時的預設（Required/Recommended，再不行照 modpack 慣例 CT77、CBBE、有中文選中文）與驗收（`fomod_audit.py <archive> <mod dir>` 要 `complete`，`base-only`／`partial` 就是白裝）已整份寫在 runbook `agentctl/docs/fomod-install-runbook.md`，照它做。只抄 FOMOD `Base/`＋facegen 會整組漏必選群組（Yvanni 163745 身體／鎧甲全壞）。

runbook 沒寫的坑：上游 FOMOD 的「Needed for textures」選配需求也要看（Yvanni 的 Anchorite／Battle Queen 貼圖在別的 mod）。archive 檔名（如帶「-DXP」）不代表安裝結果，要展開 `fomod/ModuleConfig.xml` 實際看選項樹（2026-10-23）。archive 內的 `d3d11.dll`/`dxgi.dll` 若躺在跟主功能無關的子目錄（如 DAR 條件夾），多半是誤塞的 ENB 檔，不是 SKSE DLL 依賴。帶多個可選變體的 archive，原始 conflicts_n 只是上界，要先依 fomod_choice narrow 過才能報規模。

整包 FOMOD 原樣倒進 mod 目錄（`fomod/` 與各選項資料夾並列在根、根層 0 個 plugin／BSA），或 esp 埋在沒攤平的子目錄（如 `10 Main/Follower/`），都是白裝：MO2 不當 plugin 看、plugins.txt 沒它。`instance/tools/check_masters.py`／`resolve_load_order.py` 用 `os.walk` 找 plugin 會把子資料夾的 esp 當成存在，所以這類白裝要用 `fomod_audit` 判，不能靠 check_masters（`agentctl/handoffs/home-2026-10-26/shell-esl/REPORT.md` A5 節與「順帶看到」）。FOMOD apply 等依賴 0-based 索引的批次腳本要明確用 `bash` 執行，zsh 陣列 1 起算會讓目錄內容整批錯位。

相關：[[face-bugs-check-real-actor-and-upstream-fomod]]、[[investigate-all-then-install-once]]
source: agentctl/handoffs/done/2026-09/home-2026-09-02/mco/REPORT.md:32,34,67；agentctl/handoffs/done/2026-09/home-2026-09-03/lrrev/REPORT.md:66；agentctl/handoffs/done/2026-09/home-2026-09-11/donor/REPORT.md:36；agentctl/handoffs/done/2026-10/home-2026-10-10/batch4b/REPORT.md

## pre-install-evaluation-gaps-requirements-and-prereqs

> Nexus requirements 表、使用者的前置放行、施工前的調查報告，三者都只覆蓋表面，評估裝不裝前要主動補查。

2026-08-29～10-10 歸納，三者都是「某個時間點／某個檢查範圍」的切片：

- requirements 欄顯示 `none` 不代表沒前置，正文常另寫 CC 內容或畫質前置（Mihail 生物 mod、升龍槍系列「貼圖專用必要前置」）——一定讀完整 description 找 CC/INI/相容性說明。
- 官方主題合集與其收錄的 standalone 散件會重複生成內容，裝合集前核對 Features 收錄清單，逐一停用重複的 standalone esp。
- 「缺前置」屬於全域性框架（overhaul／成人內容／全域語音）時預設判放棄，不為救一件 mod 引入整個框架。
- 使用者對某次整包放行的前置依賴不能推廣成通用許可，每次都要重新取得明確同意。

- 兩個地點／建築 mod 重疊前，先查 Nexus 有沒有官方 patch 或相容性建議，能省下大量自製 forward patch。
- 中文基底換裝類常是互斥關係（先卸載舊漢化包、語言設英文），不是疊裝即可。
- 施工線不照抄前置調查報告的「已裝／未裝」結論，開工時自己重新 grep 一次 modlist/plugins。

source: agentctl/handoffs/done/2026-08-29/cx-mihail/REPORT.md:53；agentctl/handoffs/done/2026-10/home-2026-10-03/suramodel/REPORT.md
