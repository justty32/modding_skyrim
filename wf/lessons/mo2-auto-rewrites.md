# MO2／遊戲自動改寫：load order、plugins.txt、雜目錄與幽靈 profile

[lessons 索引](README.md)｜profile 還原、回寫與並行編輯見 [mo2-profiles](mo2-profiles.md)；其他 MO2 行為坑見 [mo2-behavior-quirks](mo2-behavior-quirks.md)

## game-rewrites-plugins-orphans-and-seq-bsa

> MO2 load order 每次被打亂的真因是 SkyrimSE 把停用＋缺 master 的 plugin 搬到最上面；普通 esp 永遠排在 master 類後；11 個 BSA 重打包了 SEQ，mod 更新要重做（2026-10-10）

（1）MO2（和引擎）一律把普通 esp 排在所有 master 類（ESM 旗標或 `.esm`／`.esl`）之後；把 esp 夾在 USSEP 前「讓它輸」不會生效。MO2 2.5.2 `fixPluginRelationships()` 每次 refresh 都把 master 類搬到普通 esp 前、`setPluginPriority()` 明寫「esp 不准搬到 esm 上面」，lockedorder.txt 也鎖不住。houseCARL 判贏家照 `plugins.txt` 字面順序、沒套這條規則，會判錯。

（2）SkyrimSE 啟動會改寫 `plugins.txt`，把停用且缺 master 的 plugin 搬到最上面，MO2 讀回後 master 區尾段每次亂排。修法：這類孤兒 plugin 改 `.mohidden`（清單 `agentctl/handoffs/2026-10-10/post-test-fix/data/hide-orphans-manifest.json`）。

（3）11 個 mod（arnima、USMP、SPERG、HLIORemi、VLIOVarinia 等）的 SEQ 包在 BSA 裡，已重打包；其餘 42 支用 mod `SEQ Regenerated 2026-10-10`。原 BSA 備份 `~/skyrim_mods/_seq-bsa-backup-2026-10-10/`。

（4）固定一批 ESL/ESM（Aqua、HSResources、DD_warrior、Midnight Sun、Astral、AncientBloodII、Shockwave、FalkreathShades）每次玩完都會被 MO2 回寫排序位置，看到位移可直接 git checkout 還原不必重查。

來源：`agentctl/handoffs/done/2026-10/home-2026-10-10/mo2-reorder/REPORT/investigation.md`、`agentctl/handoffs/done/2026-10/home-2026-10-08/newsave/REPORT-build.md`。

**How to apply:** 新增 plugin 排序時 esp 不能放進 master 區；拔 mod 時連孤兒補丁一起 `.mohidden`；`instance/tools/reverify.py` 的 ORPHAN／SEQBSA 亮紅就照 `mod-library/artifacts/seq-bsa-repack/` 重做。驗贏家要用「引擎實際順序」（`mo2-reorder/tools/winner_diff.py`）。相關：[[mo2-first-launch-drops-new-plugin-star]]、[[copied-fomod-choices-need-soft-dependency-audit]]。

## plugins-txt-format-fragility

> plugins.txt 有兩種合法格式（MO2 產生 vs 遊戲自身產生），格式判斷錯或混用換行會讓 esp 靜默變停用，不報錯。

MO2 版以「Mod Organizer」開頭、要求 CRLF、啟用行帶 `*`；遊戲自身產生版以「This file is used by Skyrim」開頭，不帶 `*` 也算啟用。改 CRLF 檔時只把動到的行寫成 LF 會造成混合換行（2026-09-02～03）。

改 plugins.txt 前先讀首行判斷格式分支，不照抄交接書假設；驗收加一條「整檔逐行同一種換行」。來源：`agentctl/handoffs/done/2026-09/home-2026-09-02/dsview/cx-dsview2/REPORT.md:39`。

## mo2-auto-adds-stray-mods-dirs

> MO2 啟動會把 mods/ 裡不在 modlist.txt 的目錄自動加進 modlist；houseCARL 寫入工具與各線的暫存驗證目錄都落在 mods/，開 MO2 前必須清掉（2026-09-04）

MO2 啟動時把 `mods/` 底下**不在 `modlist.txt` 的目錄**各加一行進 modlist（結尾 `_backup` 的除外），關閉回寫時落在當前 profile 分支上，別線產物就混進施工分支。houseCARL 的寫入／反編譯工具（`bsa_extract`、`decompile_script` 等）產物預設建在 `mods/`（如 `_post5-verify/`、`houseCARL - cx-old-a-decompile/`）。

- 任何線用 houseCARL 寫入或在 `mods/` 放暫存目錄，交接書寫死「驗完立刻 `mv` 到 `/tmp/`」；持遊戲窗的隊開 MO2 前先 `find mods/ -maxdepth 1` 與 modlist 行數對照，差的只該是 `*_backup` 目錄。
- 同類：profiles repo 根的非 profile 目錄會被 MO2 當 profile，見 [[mo2-phantom-profile-workflows-dir]]。
- 同類（2026-10-23）：ReLight 這類 runtime 光照 authoring 工具把成果存成 JSON 寫進 MO2 overwrite，清空 overwrite 會讓成果整份消失且沒有其他備份；用這類「runtime 編輯＋寫回 overwrite」工具前先確認輸出路徑，清理前先備份或移出（`agentctl/handoffs/done/2026-08-30/urlinbox-2026-08-30/team-b/FINDINGS.md:53-58`）。

## mo2-phantom-profile-workflows-dir

> profiles repo 的非 profile 目錄收進隱藏的 `.repo/`，MO2 不再列幽靈 profile；根目錄只准放真 profile（2026-10-03）

`instance/profiles/` 就是 MO2 的 profiles 根，根目錄每個可見子目錄都被當 profile：MO2 會在裡面生六個預設檔，甚至把 `selected_profile` 切過去，SKSE 用空 profile 跑成原版。機制、`.repo/` 佈局、白名單（`modpack-main`＋`dsport-dev`，`check_profiles.py` 的 `ALLOWED_PROFILES`）與 `.repo/retired/` 已寫進 [`instance/profiles/README.md`](../../instance/profiles/README.md)〈目錄佈局〉（報告 `agentctl/handoffs/home-2026-10-03/phantom/REPORT.md`），照那裡做；指令是 `python3 -B .repo/tools/profile_workflow.py …`。文件沒寫的：

- 09-03～09-18 的 handoff 腳本（lrfw verify.sh、dsview verify.sh、dgup/install.sh 等）寫死 `instance/profiles/tools/` 路徑，重跑前要改。
- 驗證載入了哪個 profile：`launch-mo2.sh` 的 `PROFILE` 變數只用來做啟動前非 ASCII 檢查，不切換 profile；`qa_status` 的 `profile` 欄位釘死 `modpack-main` 不可信。切換點是 `ModOrganizer.ini` 的 `selected_profile`，實值是 `@ByteArray(modpack-main)`，照字面 grep 的閘門恆失敗；看對應 `modlist.txt` 的 mtime 是否在 MO2 啟動當下被改寫（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-05/dsport4-2026-09-05/INGAME-PREP.md:34-39`、`agentctl/handoffs/done/2026-09/home-2026-09-03/rt1/REPORT.md:103`）。

**profile_workflow**：`profile_workflow.py start feat/*` 一律從 main 開分支（`start_branch` 寫死 base="main"），不是從 live checkout 繼續；在 main 上 `record -m` 會拒絕，多線改用對明確路徑直接 `git commit`（訊息自己補，不套 `feat(profiles):` 前綴）。`mo2ctl install` 會在 `instance/profiles/` 落下未追蹤的 profile-state.json，`record` 因工作樹不乾淨而拒絕，要先搬出去或加進 .gitignore（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-03/inst/REPORT.md:89,92`、`agentctl/handoffs/done/2026-10/home-2026-10-09/vf-text3/DONE-zhfix.md`）。

**LocalSaves**：`LocalSaves=true` 時存檔寫在 `profiles/<profile>/saves/`，不是 `~/Documents`；煙霧測試載入「最新存檔」前先確認 skyrim.ini 的 LocalSaves（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-12/zhfix2/REPORT.md:92`）。
