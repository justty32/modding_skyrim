# MO2 與 profile（2/2）

[lessons 索引](README.md)｜同主題：[mo2-profiles](mo2-profiles.md)

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

## cc-download-lands-in-cwd-data

> 1.6.1170 遊戲內 Creations 下載其實會成功，但檔案寫到「啟動時的工作目錄/Data」而不是遊戲目錄；2026-09-03 70 件 CC 落在 repo 根的 data/（原 type: memory）

2026-09-03 19:25–19:34 使用者用 `ae2/tools/launch-vanilla-skyrim.sh` 開純本體、在 Creations 按下載，70/75 件（140 檔、5.8 GB）**真的下來了**，但寫進 `~/repo/moddings/skyrim/data/`（他跑腳本時的 cwd），遊戲目錄 `Data/` 不變。當晚我查三次都以「Data 仍 8 個 cc 檔」判成空跑——錯了。現在檔案在 `~/skyrim_mods/cc-ae-download-2026-09-03/`（09-04 早上搬的）。

**Why:** 遊戲的 CC 下載器用相對路徑 `Data\`，Proton 下 cwd 是 shell 的 cwd，不是 exe 所在目錄；launcher 沒 `cd` 進遊戲目錄。
**How to apply:** `launch-vanilla-skyrim.sh` 要加 `cd "$G"`（或在 REPORT 註明先 cd）。CC 做成 MO2 mod（`Skyrim.ccc` 原廠 75 行從未被裁，一個位元組都別動）：**`.ccc` 列名且檔案在 VFS Data/ 的 plugin 一律當隱含 master 自動載入、不看 plugins.txt**，所以「啟用」＝勾 mod，「排除某幾件」＝把它們的 plugin＋bsa 搬到另一個停用的姊妹目錄（2026-09-04 cc 線：啟用 53、排除 17，隱含 master 13→59；USCCCP 46 支才走 plugins.txt）。官方簡中字串在每件 BSA 裡，抽成 `Strings/<原大小寫>_English.*` 層即可（mod-library `CC-Official-CHS-Strings-EnglishSlot-2026-09-04`）。找檔案時先 `find / -newermt` 全機掃，別只看預期目錄。相關：[[skyrim-no-appmanifest-steam-safe]]。

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
