# MO2 與 profile

[lessons 索引](README.md)

## cc-download-lands-in-cwd-data

> 1.6.1170 遊戲內 Creations 下載其實會成功，但檔案寫到「啟動時的工作目錄/Data」而不是遊戲目錄；2026-09-03 70 件 CC 落在 repo 根的 data/（原 type: memory）

2026-09-03 19:25–19:34 使用者用 `ae2/tools/launch-vanilla-skyrim.sh` 開純本體、在 Creations 按下載，70/75 件（140 檔、5.8 GB）**真的下來了**，但寫進 `~/repo/moddings/skyrim/data/`（他跑腳本時的 cwd），遊戲目錄 `Data/` 不變。當晚我查三次都以「Data 仍 8 個 cc 檔」判成空跑——錯了。現在檔案在 `~/skyrim_mods/cc-ae-download-2026-09-03/`（09-04 早上搬的）。

**Why:** 遊戲的 CC 下載器用相對路徑 `Data\`，Proton 下 cwd 是 shell 的 cwd，不是 exe 所在目錄；launcher 沒 `cd` 進遊戲目錄。
**How to apply:** `launch-vanilla-skyrim.sh` 要加 `cd "$G"`（或在 REPORT 註明先 cd）。CC 做成 MO2 mod（`Skyrim.ccc` 原廠 75 行從未被裁，一個位元組都別動）：**`.ccc` 列名且檔案在 VFS Data/ 的 plugin 一律當隱含 master 自動載入、不看 plugins.txt**，所以「啟用」＝勾 mod，「排除某幾件」＝把它們的 plugin＋bsa 搬到另一個停用的姊妹目錄（2026-09-04 cc 線：啟用 53、排除 17，隱含 master 13→59；USCCCP 46 支才走 plugins.txt）。官方簡中字串在每件 BSA 裡，抽成 `Strings/<原大小寫>_English.*` 層即可（mod-library `CC-Official-CHS-Strings-EnglishSlot-2026-09-04`）。找檔案時先 `find / -newermt` 全機掃，別只看預期目錄。相關：[[skyrim-no-appmanifest-steam-safe]]。

2026-10-23 補：掃描「真正啟用的 plugin」清單不能只抓 plugins.txt 裡標 `*` 的行，要另外併入原版與 CC 等隱含載入的 masters——實測 1266 支裡 1207 支是 `*`、另外 59 支是隱含載入，字面執行「只看 `*`」會漏掉它們。來源：`agentctl/handoffs/done/2026-09/home-2026-09-20/cell/REPORT.md:21`。

## profile-restore-order-and-flags

> MO2 profile 事故（2026-08-27 全停用＋名稱序重排）的教訓：還原要同時還原「順序」與「旗標」；MO2 開著時絕不改 profile 檔；檔案層啟用要連 plugins.txt 一起補（原 type: memory）

2026-08-27 晚間實機施工的事故鏈：使用者在 MO2 裡誤觸讓 modlist 全部停用並**按名稱重排**；
MO2 退出時把 plugins/loadorder/archives 清成只剩原版。我用 git HEAD 只還原了**啟用旗標**，
沿用了事故檔的**字母序**——結果 TK Dodge RE 的原版行為圖壓過 Pandora Output，第三人稱無法攻擊；
5485 個 loose 檔勝出者改變，多個中文層與 ElevenLabs 配音層被本體壓掉。

**Why**：modlist.txt 的行序就是優先度（檔內越上越優先，MO2 左欄相反）。只看啟用數 289 對得上
就宣告還原成功，是「檢查失效時給出最令人安心的答案」的又一例。

**How to apply**：
- 還原 profile 一律以「已知正確順序的副本」為基準（git HEAD 或各線收線前的 `modlist.txt.bak`），
  再把新 mod 插回、再套旗標；驗收要跑 loose-file winner 模擬（opus-qa-triage 的方法），
  不能只比啟用數。
- **MO2 開著時絕不改 profile 檔**——它退出會整份覆寫。批次啟用改走「關 MO2 → 改檔 → 重開」。
- 檔案層把 mod 改 `+` 後，MO2 認到的新插件**預設未勾**，plugins.txt 要一起補 `*`。
- Python 改檔先讀後寫，且 `open(...,"w")` 在參數求值前就會截斷檔案——腳本炸在 join 也會留下空檔；
  改前一律先 cp 備份。
- 中文層在 MO2 左欄要排在本體**下面**（檔內在上面）；跟使用者講順序用「左欄」的說法。
- Steam 若在啟動前跳更新：Downloads 暫停 → Go Offline → 再啟動；1.6.1170 備份在
  `~/skyrim_mods/steam-build-backup/`。

相關：[[launch-skyrim-via-steam]]、[[verify-waituser-against-logs]]

**2026-09-16 補：** MO2／遊戲開著時 profile 檔是暫態（plugins.txt 會變 LF、archives.txt 變 0 bytes）；我在遊戲跑著時 commit＋push 了這個暫態快照。規則：commit profile 三檔前先 `ps` 確認 MO2 已退出、`file` 確認 CRLF，否則等 MO2 退出回寫後再 commit。

2026-10-23 補：modlist.txt 的 separator 行位於它所轄群組「之後」（歸屬＝行號大於它的第一個 separator），且 plugins.txt／loadorder.txt 的優先方向與 modlist.txt 相反（modlist 越上面優先權越高；plugins/loadorder 是檔尾後載入者贏、master 必須排在依賴它的 plugin 前）；同一支腳本若要同時改寫兩者不能共用一套拓撲排序，上線前先拿已知答案的樣本驗證方向（本輪一次誤判方向造成 36 件裡 32 件假陽性）。來源：`agentctl/handoffs/done/2026-09-02/lorerim-2026-09-02/team-src/REPORT.md:30-33`、`agentctl/handoffs/done/2026-09/home-2026-09-05/lrin/REPORT.md:78`、`agentctl/handoffs/done/2026-09-01/hzh-2026-09-01/cx-hz2/REPORT.md:1-15`。

2026-10-23 補：檔案優先度（中文層蓋過英文本體檔）與 plugin 記錄層的載入順序是兩套獨立機制——中文層在檔案層贏了，不代表沒有其他以該插件為 master 的 ESP 在記錄層把同欄位蓋回英文，調整 modlist 優先度救不了這種情況。驗收「中文層生效」要另外用 `cross_plugin_query(..., conflict_tree=true)` 追 override_depth，有後載入插件蓋掉就得做 patch plugin 轉發，不是調檔案優先度。來源：`agentctl/handoffs/done/2026-08-28/opus-apply-order/STATE.md:207-222,273-286`。

2026-10-23 補：批次插入多筆 modlist 行要由檔案下方往上插（insert_order 由大到小），由上往下插會讓先插入那行把下面所有錨點行號推移一行、後續全錯。新裝帶 ESM 旗標（TES4 flags 含 0x1）的 master 不能直接附加到 plugins.txt/loadorder.txt 檔尾，要插在 DynDOLOD.esm 那一行正上方，否則 MO2/引擎會重排、星號掉掉。來源：`agentctl/handoffs/done/2026-08-28/opus-install-prep/PLAN.md:34-42`、`agentctl/handoffs/done/2026-09/home-2026-09-12/want5/REPORT.md:84`。

2026-10-23 補：契約寫「REMOVE-FROM-MODLIST」若只把啟用行改成 `-`（停用）、不整行刪除＋搬走 mod 目錄，該行仍指向已移走的目錄，MO2 下次開啟會顯示異常；真正的「移除」必須整行刪除＋搬目錄兩步一起做。來源：`agentctl/handoffs/done/2026-09/home-2026-09-03/inst5/REPORT.md:59`。

2026-10-23 補（E2bs-12）：09-11 裁示——MO2／遊戲重開造成的 profile 三檔整檔重排／換行漂移，不得跟持鎖隊自己的變更混進同一筆 commit；收線時把這類回寫漂移另立一筆、訊息標明「MO2 回寫」，方便回溯（`agentctl/handoffs/done/2026-09/home-2026-09-11/COMMON/03-rulings-morning.md:8`）。

## mo2-first-launch-drops-new-plugin-star

> 2026-09-09 實測——新 plugin 第一次被 MO2 看到時，MO2 重排 plugins.txt 會把它寫成未啟用（掉 *），第二次啟動才穩定；MO2 跑過之後 profile 三檔必須重驗，不能沿用啟動前的 houseCARL／鏡像結果（原 type: feedback）

2026-09-09 lead-audit 22:28 把 `RSChildren-Forward…esp` 加進 plugins.txt（有 `*`），22:33 開 MO2 跑煙霧，
MO2 重排整份 plugins.txt、把這支沒見過的新 plugin 寫成未啟用（`*` 掉了）；驗收卻用 22:28 那份
houseCARL 鏡像跑，回報 24/24 贏家 PASS，使用者看到的仍是大媽臉。補回 `*` 再開一次 MO2 就留住了。

**Why:** MO2 啟動時會依自己的規則重寫 profile 三檔；鏡像快照是「跑之前」的狀態。
「跑之前 PASS」不等於「跑之後 PASS」。

**How to apply:**
- 任何加新 plugin 的窗：**MO2／遊戲關掉之後再實讀 plugins.txt 那一行有沒有 `*`**（`tr -d '\r'` 後 grep），
  再刷新鏡像重驗贏家；驗收證據要標明時間在 MO2 關閉之後。
- 新 plugin 第一次被 MO2 看到可能被寫成未啟用；煙霧後補 `*`、第二次啟動穩定。
- 相關 [[profile-restore-order-and-flags]]（MO2 開著絕不改 profile）、[[interactive-grep-is-ugrep]]（CRLF）、
  [[rs-children-missing-esp]]。

2026-10-23 補：MO2 正常結束會重寫 plugins.txt／loadorder.txt（CRLF 轉 LF、重排、拿掉已停用 mod 對應的已不存在 plugin 列）但不動 modlist.txt；驗證「有沒有損失」時 modlist.txt 可直接比 md5，plugins.txt／loadorder.txt 要先正規化（排序、去 CRLF）再比對集合是否一致，不能逐行 diff。來源：`agentctl/handoffs/done/2026-08-30/fix-2026-08-30/REPORT.md:107-125`。

## mo2-auto-adds-stray-mods-dirs

> MO2 啟動會把 mods/ 裡不在 modlist.txt 的目錄自動加進 modlist；houseCARL 寫入工具與各線的暫存驗證目錄都落在 mods/，開 MO2 前必須清掉（原 type: memory）

2026-09-04 lead-inst4 實測：MO2 啟動時會把 `mods/` 底下**不在 `modlist.txt` 的目錄**各自動加一行進 modlist（結尾 `_backup` 的目錄除外），關閉回寫時就落在當前 profile 分支上。houseCARL 的寫入／反編譯工具（`bsa_extract`、`decompile_script` 等）產物預設就建在 `mods/`；post5 的 `_post5-verify/`、cx-old-a 的 `houseCARL - cx-old-a-decompile/` 都是這樣留下的。

**Why:** 這些目錄不在 modlist 時不影響載入，但只要有人開一次 MO2 就變成 profile 髒污，而且是別線的產物混進施工分支。
**How to apply:** 任何線用 houseCARL 寫入或在 `mods/` 放暫存目錄，交接書要寫死「驗完立刻 `mv` 到 `/tmp/`」；持遊戲窗的隊開 MO2 前先 `find mods/ -maxdepth 1` 與 modlist 行數對照（09-04 基準：目錄 1288、modlist 1291，差的只有三個 `ModForge*_backup`）。同類：profiles repo 根的 `tests/`／`tools/`／`workflows/` 也曾被 MO2 當 profile 補檔（2026-10-03 已收進 `.repo/` 根治，見下節）。

2026-10-23 補：同類陷阱——像 ReLight 這類 runtime 光照 authoring 工具會把編輯成果存成 JSON 寫進 MO2 的 overwrite 資料夾，清空 overwrite 會讓成果整份消失且沒有其他備份；評估/使用這類「runtime 編輯＋寫回 overwrite」工具前要先確認輸出路徑，清理前先備份或移出。來源：`agentctl/handoffs/done/2026-08-30/urlinbox-2026-08-30/team-b/FINDINGS.md:53-58`。

## mo2-phantom-profile-workflows-dir

> 2026-10-03 已根治——profiles repo 的非 profile 目錄（tools/tests/workflows/baselines）收進隱藏的 `.repo/`，MO2 不再列幽靈 profile；根目錄只准放真 profile（原 type: project）

**事故**：2026-09-18 20:32 MO2 在 `instance/profiles/workflows/` 生了 archives/loadorder/lockedorder/modlist/plugins/settings.ini 六個預設檔；
2026-10-03 MO2 把 `selected_profile` 切成幽靈 profile `tests`，SKSE 用空 profile 跑成原版（usvfs 559 節點）。
原因：`instance/profiles/` 就是 MO2 的 profiles 根（MO2 端是 symlink），根目錄下每個可見子目錄都被當 profile。

**根治**（profiles `934b24c`，報告 `agentctl/handoffs/home-2026-10-03/phantom/REPORT.md`）：四個非 profile 目錄 `git mv` 到 `.repo/`
（`.repo/tools`、`.repo/tests`、`.repo/workflows`、`.repo/baselines`）。MO2 列 profile 不帶 `QDir::Hidden`，Wine 把點開頭目錄標 hidden，同層 `.git/` 從沒被當 profile。
施工後開關 MO2：`selected_profile=modpack-main`、`.repo/` 沒被生預設檔、profile 檔 md5 不變。

**How to apply:** 不要在 `instance/profiles/` 根新增非 profile 目錄；指令改成 `python3 -B .repo/tools/profile_workflow.py …`；
09-03～09-18 舊 handoff 腳本（lrfw verify.sh、dsview verify.sh、dgup/install.sh 等）寫死 `instance/profiles/tools/` 舊路徑，重跑前要改。
另：plugins.txt 在 MO2 跑過後可能整檔重排（ESL 漂移），啟用集合比對才算數（同 [[profile-restore-order-and-flags]]）。

（2026-10-23 依記憶條目補）根目錄白名單是 `modpack-main`（必備）＋`dsport-dev`（`check_profiles.py` 的 `ALLOWED_PROFILES`）；
`crash-ab-carp`、`crash-ab-doomperk` 2026-10-03 依使用者裁示封存到 `.repo/retired/`（要再用得 `git mv` 回根並加進白名單）。
baseline 在 `instance/profiles/.repo/baselines/`；舊的 6 個 workflows 垃圾檔收在 `~/skyrim_mods/_staging-2026-10-03/phantom/mo2-junk-workflows/`。

2026-10-23 補：`launch-mo2.sh` 寫死的 `PROFILE` 變數只用來做啟動前非 ASCII 檢查，不會切換 MO2 實際載入的 profile；`qa_status` 的 `profile` 欄位同樣釘死 `modpack-main` 不可信。真正的切換點是 `ModOrganizer.ini` 的 `selected_profile`，但它存的實際值是 `@ByteArray(modpack-main)` 不是字面字串，照字面 grep 比對的閘門會恆為失敗；要驗證載入了哪個 profile，看對應 `modlist.txt` 的 mtime 有沒有在 MO2 啟動當下被改寫。來源：`agentctl/handoffs/done/2026-09/home-2026-09-05/dsport4-2026-09-05/INGAME-PREP.md:34-39`、`agentctl/handoffs/done/2026-09/home-2026-09-03/rt1/REPORT.md:103`。

2026-10-23 補：`profile_workflow.py start feat/*` 一律從 main 開分支（`start_branch` 寫死 base="main"），不是從目前 live checkout 繼續；在 main 分支上 `record -m` 會直接拒絕，近期多線改用對明確路徑直接 `git commit` 繞過（commit message 自己補，不套 `feat(profiles):` 前綴）。`mo2ctl install` 會在 `instance/profiles/` 落下一個未追蹤的 profile-state.json，導致 `record` 因工作樹不乾淨而拒絕，要先搬出去或加進 .gitignore。來源：`agentctl/handoffs/done/2026-09/home-2026-09-03/inst/REPORT.md:89,92`、`agentctl/handoffs/done/2026-10/home-2026-10-09/vf-text3/DONE-zhfix.md`。

2026-10-23 補：`LocalSaves=true` 時存檔實際寫在 `profiles/<profile>/saves/`，不是 `~/Documents`；煙霧測試載入「最新存檔」前先確認 skyrim.ini 的 LocalSaves 設定。來源：`agentctl/handoffs/done/2026-09/home-2026-09-12/zhfix2/REPORT.md:92`。

## dsport-dev-profile-drift

> 2026-09-18 抓到 dsport-dev profile 是 09-05 快照，漏掉 09-14／09-16 兩輪共 12 項裁示（BCE、ICOW 6、RSC 4）；測試 profile 要跟 modpack-main 的裁示對帳（原 type: project）

2026-09-18 dsp-game 隊發現 `dsport-dev` profile 停在 09-05 狀態：09-16 停用 Better Combat Escape（MaxsuCombatEscape.dll cell hook，同址 CTD `SkyrimSE.exe+04D0038` 真凶）只做進 modpack-main；ICOW 組 6 個仍開、取代它的 OCW 補丁關著；RSC 組 4 個也沒同步。當天先停 BCE（c5b9893），使用者拍板整批同步後 15:44 完成（profiles 0d6ba5f）：實際 10 mod＋13 plugin，plugins.txt 比對才是權威（6 支母 mod 兩邊都開只是 esp 個別關）；第「11 項」DSPortP3 本身是 dsport-dev 存在的理由不能同步（差異在 `handoffs/home-2026-09-18/dsp-game/data/profile-drift.json`）。

**Why:** 在過期的測試 profile 上做實機驗收，CTD 會被錯歸因給受測物（09-13 dsp8 把 BCE 的鍋算到 navmesh 頭上）。

**How to apply:** 用非 main profile 做實機前，先 diff 它跟 modpack-main 的 modlist/plugins，把「已裁示停用的 mod」列出來；crash 先看 callstack 點名哪個 SKSE DLL，再怪內容。相關：[[custom-navm-combat-pathing-ctd]]、[[profile-restore-order-and-flags]]。

2026-10-23 補：同類的 profile 名稱漂移也發生在 baseline 工具上——`agentctl/qa/baselines/modpack-kr-dev/baseline-manifest.json` 寫的 profile 是舊名「Modpack-KR」，現役早已是 modpack-main，preflight 載存檔會因 profile 不符 fail-closed；改 profile 名稱時要連同所有 baseline manifest 一起改，派 QA 線前先核對一致。來源：`agentctl/handoffs/done/2026-09/home-2026-09-05/ab/REPORT.md:77`。

## game-rewrites-plugins-orphans-and-seq-bsa

> 2026-10-10 MO2 load order 每次被打亂的真因是 SkyrimSE 把停用＋缺 master 的 plugin 搬到最上面；普通 esp 永遠排在 master 類後；11 個 BSA 重打包了 SEQ，mod 更新要重做

2026-10-10 三層發現：

1. MO2（和引擎）一律把普通 esp 排在所有 master 類（ESM 旗標或 `.esm`／`.esl`）之後；record 把 esp 夾在 USSEP 前「讓它輸」從沒生效過。houseCARL 判贏家照 `plugins.txt` 字面順序、沒套這條規則，會判錯。
2. SkyrimSE 啟動會改寫 `plugins.txt`，把停用且缺 master 的 plugin 搬到最上面，MO2 讀回後 master 區尾段每次亂排。修法：這類孤兒 plugin 改 `.mohidden`（清單 `agentctl/handoffs/2026-10-10/post-test-fix/data/hide-orphans-manifest.json`）。
3. 11 個 mod（arnima、USMP、SPERG、HLIORemi、VLIOVarinia 等）的 SEQ 包在 BSA 裡，已重打包；其餘 42 支用 mod `SEQ Regenerated 2026-10-10`。原 BSA 備份 `~/skyrim_mods/_seq-bsa-backup-2026-10-10/`。

**Why:** 開 MO2＋遊戲後 profile 永遠 dirty、驗收規則寫了不可能成立的順序。

**How to apply:** 新增 plugin 排序時 esp 不能放進 master 區；拔 mod 時連孤兒補丁一起 `.mohidden`；`instance/tools/reverify.py` 的 ORPHAN／SEQBSA 亮紅就照 `mod-library/artifacts/seq-bsa-repack/` 重做。驗贏家要用「引擎實際順序」（`mo2-reorder/tools/winner_diff.py`）。相關：[[mo2-first-launch-drops-new-plugin-star]]、[[copied-fomod-choices-need-soft-dependency-audit]]。

2026-10-23 補：MO2 2.5.2 原始碼 `fixPluginRelationships()` 每次 refresh 都會把 master 類搬到所有普通 esp 前面、`setPluginPriority()` 明寫「esp 不准搬到 esm 上面」，連 lockedorder.txt 也鎖不住；本機 18 支普通 esp 長期被寫在 USSEP/USMP 之前但從未真的生效過，實測只有 8 筆 record 因此真的翻盤。另外同一批固定的 7 支 ESL/ESM（Aqua、HSResources、DD_warrior、Midnight Sun、Astral、AncientBloodII、Shockwave、FalkreathShades）每次玩完都會被 MO2 回寫排序位置，是既有回寫行為，看到位移可直接 git checkout 還原不必重查。來源：`agentctl/handoffs/done/2026-10/home-2026-10-10/mo2-reorder/REPORT/investigation.md`、`agentctl/handoffs/done/2026-10/home-2026-10-08/newsave/REPORT-build.md`。


## plugins-txt-format-fragility

> plugins.txt 有兩種合法格式（MO2 產生 vs 遊戲自身產生），格式判斷錯或混用換行會讓 esp 靜默變停用，不報錯。

2026-09-02～03 三線各踩一次：MO2 版以「Mod Organizer」開頭、要求 CRLF、啟用行帶 `*`；遊戲自身產生版以「This file is used by Skyrim」開頭，不帶 `*` 也算啟用——曾有交接書誤寫「無 `*`」的假設。codex 改 CRLF 檔也曾只把自己動到的行寫成 LF，其餘仍 CRLF，造成混合換行。

**Why:** 格式判斷錯或混用換行都讓 esp 變「存在但停用」，且無錯誤訊息。

**How to apply:** 改 plugins.txt 前先讀首行判斷格式分支，不照抄交接書假設；驗收加一條「整檔逐行同一種換行」。來源：`agentctl/handoffs/done/2026-09/home-2026-09-02/dsview/cx-dsview2/REPORT.md:39`。


## concurrent-profile-edits-need-ref-reads

> 多線並行改同一個 profile 時，讀檔要走 git ref 不讀工作樹；撤銷某一輪要寫反向 manifest，不能直接 revert。

2026-10-03 worldfix 連套 7 輪修正、中途被別線改動，對某輪跑 `layer_apply --revert` 因 sha256 不符被拒，改手寫「反向 manifest」並先 dry-run（`--force` 會吃掉別線的事）。10-10 至少 4 條產頁線發現工作樹常被別線切分支，改統一 `git show <ref>:modpack-main/modlist.txt` 讀 blob，不直接 `cat` 工作樹。

**Why:** 本工作區常態多線碰同一份 profile；讀工作樹或 `--force` revert 都會吃掉別線進度。

**How to apply:** 只讀腳本一律 `git show <ref>:<path>`；撤銷某輪且中間已有別線動作，優先寫反向 manifest 並 dry-run。來源：`agentctl/handoffs/done/2026-10/home-2026-10-03/worldfix/REPORT.md`。


## eslify-overlay-snapshot-goes-stale

> 整包覆蓋 mod（如 ESLify-Overlay）凍結的是建立當下的贏家快照，更新同一支 plugin 的層只要排序在它之下，就會被靜默蓋掉，毫無錯誤訊息。

2026-10-09 vf-text3 查出 ESLify-Overlay 固定排在 modlist 第 5 行，manifest 寫「要重查 sha256」但沒工具自動做，LovelyLetter 中文層因新版沒排到其上而被蓋掉。覆蓋同批 plugin 的新層要保留 ESL flag 並排其上，否則 FormID 槽位改變、存檔道具錯位。

**Why:** overlay「凍結贏家」設計跟後續單獨更新同一 plugin 天生衝突，且無錯誤訊息。

**How to apply:** 更新被 overlay 收錄的 plugin 要保留 ESL flag 並排其上；疑似誤停用先查 deploy-manifest，別看到停用就重啟。來源：`agentctl/handoffs/done/2026-10/home-2026-10-09/vf-text3/DONE-eslify-shadow.md`。


## mo2-silent-collision-failure-modes

> MO2 有幾種常見靜默失效：同名 plugin 撞號、非 ASCII 資料夾名——全不報錯，只表現成「裝了沒用」或忽然 CTD。

2026-08-30～09-01：①同名 `.esp/.esm/.esl` 已知會 CTD，MO2 也拒絕還原該 load order；②同名 plugin 的 VFS 只疊最高優先度一份，判定同角色要讀 EDID，不能只看檔名；③mod 資料夾中文命名會被剝高位元、整包靜默停用，一律改純 ASCII。

**Why:** 三種情況都無錯誤訊息，容易誤判成「沒裝」而查錯方向。

**How to apply:** 啟用新 mod 前掃同名 provider／EDID；新建資料夾一律純 ASCII。來源：`agentctl/handoffs/done/2026-08-31/grow-2026-08-31/dedup_fix.py:1-7`。相關 [[profile-restore-order-and-flags]]。

2026-10-23 補：另兩種同類靜默失效——archive 內部路徑帶 `Data/` 前綴直接鋪成 `mods/<層>/Data/...` 會對應到遊戲 `Data/Data/...`，裝前先 `7z l` 檢查頂層再剝掉這層；純覆蓋式更新層（跟既有 mod 同一個 esp 檔名、靠 VFS 排序蓋過去）絕對不能在 plugins.txt／loadorder.txt 另外加一行，它不是新增 plugin 槽。來源：`agentctl/handoffs/done/2026-09/home-2026-09-01/hdmk-2026-09-01/HANDOFF-cx-hd1.md:19-35`、`agentctl/handoffs/done/2026-09/home-2026-09-08/face/REPORT.md:158`。
