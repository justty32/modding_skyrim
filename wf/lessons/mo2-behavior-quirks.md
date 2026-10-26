# MO2 本體行為坑（首次啟動、幽靈 profile、靜默失效）

[lessons 索引](README.md)

## cc-download-lands-in-cwd-data

> 1.6.1170 遊戲內 Creations 下載其實會成功，但檔案寫到「啟動時的工作目錄/Data」而不是遊戲目錄；2026-09-03 70 件 CC 落在 repo 根的 data/（原 type: memory）

用 `ae2/tools/launch-vanilla-skyrim.sh` 開純本體、在 Creations 按下載，檔案**真的會下來**，但寫進跑腳本時的 cwd 下的 `data/`（2026-09-03 是 `~/repo/moddings/skyrim/data/`），遊戲目錄 `Data/` 不變——只看遊戲 `Data/` 會誤判成空跑。那批 70/75 件（140 檔、5.8 GB）現在在 `~/skyrim_mods/cc-ae-download-2026-09-03/`。

**Why:** 遊戲的 CC 下載器用相對路徑 `Data\`，Proton 下 cwd 是 shell 的 cwd，不是 exe 所在目錄；launcher 沒 `cd` 進遊戲目錄。
**How to apply:** `launch-vanilla-skyrim.sh` 要加 `cd "$G"`（或在 REPORT 註明先 cd）。CC 做成 MO2 mod（`Skyrim.ccc` 原廠 75 行從未被裁，一個位元組都別動）：**`.ccc` 列名且檔案在 VFS Data/ 的 plugin 一律當隱含 master 自動載入、不看 plugins.txt**，所以「啟用」＝勾 mod，「排除某幾件」＝把它們的 plugin＋bsa 搬到另一個停用的姊妹目錄（2026-09-04 起啟用 53、排除 17，隱含 master 59；USCCCP 46 支才走 plugins.txt）。官方簡中字串在每件 BSA 裡，抽成 `Strings/<原大小寫>_English.*` 層即可（mod-library `CC-Official-CHS-Strings-EnglishSlot-2026-09-04`）。找檔案時先 `find / -newermt` 全機掃，別只看預期目錄。相關：[[skyrim-no-appmanifest-steam-safe]]。

掃描「真正啟用的 plugin」清單不能只抓 plugins.txt 裡標 `*` 的行，要另外併入原版與 CC 等隱含載入的 masters（2026-10-23 實測 1266 支裡 1207 支是 `*`、另外 59 支是隱含載入）。來源：`agentctl/handoffs/done/2026-09/home-2026-09-20/cell/REPORT.md:21`。

## mo2-first-launch-drops-new-plugin-star

> 2026-09-09 實測——新 plugin 第一次被 MO2 看到時，MO2 重排 plugins.txt 會把它寫成未啟用（掉 *），第二次啟動才穩定；MO2 跑過之後 profile 三檔必須重驗，不能沿用啟動前的 houseCARL／鏡像結果（原 type: feedback）

實例：`RSChildren-Forward…esp` 加進 plugins.txt（有 `*`）後開 MO2 跑煙霧，MO2 重排整份 plugins.txt、把它寫成未啟用；用啟動前的 houseCARL 鏡像驗收全 PASS，實際仍壞。補回 `*` 再開一次 MO2 就留住了。

**Why:** MO2 啟動時會依自己的規則重寫 profile 三檔；鏡像快照是「跑之前」的狀態。
「跑之前 PASS」不等於「跑之後 PASS」。

**How to apply:**
- 任何加新 plugin 的窗：**MO2／遊戲關掉之後再實讀 plugins.txt 那一行有沒有 `*`**（`tr -d '\r'` 後 grep），
  再刷新鏡像重驗贏家；驗收證據要標明時間在 MO2 關閉之後。
- 新 plugin 第一次被 MO2 看到可能被寫成未啟用；煙霧後補 `*`、第二次啟動穩定。
- 相關 [[profile-restore-order-and-flags]]（MO2 開著絕不改 profile）、[[interactive-grep-is-ugrep]]（CRLF）、
  [[rs-children-missing-esp]]。
- MO2 正常結束會重寫 plugins.txt／loadorder.txt（CRLF 轉 LF、重排、拿掉已停用 mod 對應的已不存在 plugin 列）但不動 modlist.txt；驗證「有沒有損失」時 modlist.txt 可直接比 md5，plugins.txt／loadorder.txt 要先正規化（排序、去 CRLF）再比對集合是否一致，不能逐行 diff（2026-10-23，`agentctl/handoffs/done/2026-08-30/fix-2026-08-30/REPORT.md:107-125`）。

## mo2-auto-adds-stray-mods-dirs

> MO2 啟動會把 mods/ 裡不在 modlist.txt 的目錄自動加進 modlist；houseCARL 寫入工具與各線的暫存驗證目錄都落在 mods/，開 MO2 前必須清掉（原 type: memory）

2026-09-04 實測：MO2 啟動時會把 `mods/` 底下**不在 `modlist.txt` 的目錄**各自動加一行進 modlist（結尾 `_backup` 的目錄除外），關閉回寫時就落在當前 profile 分支上。houseCARL 的寫入／反編譯工具（`bsa_extract`、`decompile_script` 等）產物預設就建在 `mods/`（如 `_post5-verify/`、`houseCARL - cx-old-a-decompile/`）。

**Why:** 這些目錄不在 modlist 時不影響載入，但只要有人開一次 MO2 就變成 profile 髒污，而且是別線的產物混進施工分支。
**How to apply:** 任何線用 houseCARL 寫入或在 `mods/` 放暫存目錄，交接書要寫死「驗完立刻 `mv` 到 `/tmp/`」；持遊戲窗的隊開 MO2 前先 `find mods/ -maxdepth 1` 與 modlist 行數對照（09-04 基準：目錄 1288、modlist 1291，差的只有三個 `ModForge*_backup`）。同類：profiles repo 根的 `tests/`／`tools/`／`workflows/` 會被 MO2 當 profile 補檔，已收進 `.repo/`，見下節。

同類陷阱（2026-10-23）：像 ReLight 這類 runtime 光照 authoring 工具會把編輯成果存成 JSON 寫進 MO2 的 overwrite 資料夾，清空 overwrite 會讓成果整份消失且沒有其他備份；評估/使用這類「runtime 編輯＋寫回 overwrite」工具前要先確認輸出路徑，清理前先備份或移出。來源：`agentctl/handoffs/done/2026-08-30/urlinbox-2026-08-30/team-b/FINDINGS.md:53-58`。

## mo2-phantom-profile-workflows-dir

> 2026-10-03 已根治——profiles repo 的非 profile 目錄（tools/tests/workflows/baselines）收進隱藏的 `.repo/`，MO2 不再列幽靈 profile；根目錄只准放真 profile（原 type: project）

**機制**：`instance/profiles/` 就是 MO2 的 profiles 根（MO2 端是 symlink），根目錄下每個可見子目錄都被當 profile——MO2 會在裡面生 archives/loadorder/lockedorder/modlist/plugins/settings.ini 六個預設檔，甚至把 `selected_profile` 切到幽靈 profile，SKSE 用空 profile 跑成原版。

**現狀**（報告 `agentctl/handoffs/home-2026-10-03/phantom/REPORT.md`）：四個非 profile 目錄在 `.repo/`
（`.repo/tools`、`.repo/tests`、`.repo/workflows`、`.repo/baselines`）。MO2 列 profile 不帶 `QDir::Hidden`，Wine 把點開頭目錄標 hidden，同層 `.git/` 也不被當 profile。
2026-10-03 開關 MO2 驗過：`selected_profile=modpack-main`、`.repo/` 沒被生預設檔、profile 檔 md5 不變。

**How to apply:**
不要在 `instance/profiles/` 根新增非 profile 目錄；指令是 `python3 -B .repo/tools/profile_workflow.py …`；
09-03～09-18 的 handoff 腳本（lrfw verify.sh、dsview verify.sh、dgup/install.sh 等）寫死 `instance/profiles/tools/` 路徑，重跑前要改。

plugins.txt 在 MO2 跑過後可能整檔重排（ESL 漂移），啟用集合比對才算數（同 [[profile-restore-order-and-flags]]）。

根目錄白名單是 `modpack-main`（必備）＋`dsport-dev`（`check_profiles.py` 的 `ALLOWED_PROFILES`）；
`crash-ab-carp`、`crash-ab-doomperk` 2026-10-03 依使用者裁示封存到 `.repo/retired/`（要再用得 `git mv` 回根並加進白名單）。
baseline 在 `instance/profiles/.repo/baselines/`；當年 workflows 生的 6 個垃圾檔收在 `~/skyrim_mods/_staging-2026-10-03/phantom/mo2-junk-workflows/`。

`launch-mo2.sh` 寫死的 `PROFILE` 變數只用來做啟動前非 ASCII 檢查，不會切換 MO2 實際載入的 profile；`qa_status` 的 `profile` 欄位同樣釘死 `modpack-main` 不可信。真正的切換點是 `ModOrganizer.ini` 的 `selected_profile`，但它存的實際值是 `@ByteArray(modpack-main)` 不是字面字串，照字面 grep 比對的閘門會恆為失敗；要驗證載入了哪個 profile，看對應 `modlist.txt` 的 mtime 有沒有在 MO2 啟動當下被改寫（2026-10-23）。來源：`agentctl/handoffs/done/2026-09/home-2026-09-05/dsport4-2026-09-05/INGAME-PREP.md:34-39`、`agentctl/handoffs/done/2026-09/home-2026-09-03/rt1/REPORT.md:103`。

`profile_workflow.py start feat/*` 一律從 main 開分支（`start_branch` 寫死 base="main"），不是從目前 live checkout 繼續；在 main 分支上 `record -m` 會直接拒絕，近期多線改用對明確路徑直接 `git commit` 繞過（commit message 自己補，不套 `feat(profiles):` 前綴）。`mo2ctl install` 會在 `instance/profiles/` 落下一個未追蹤的 profile-state.json，導致 `record` 因工作樹不乾淨而拒絕，要先搬出去或加進 .gitignore（2026-10-23）。來源：`agentctl/handoffs/done/2026-09/home-2026-09-03/inst/REPORT.md:89,92`、`agentctl/handoffs/done/2026-10/home-2026-10-09/vf-text3/DONE-zhfix.md`。

`LocalSaves=true` 時存檔實際寫在 `profiles/<profile>/saves/`，不是 `~/Documents`；煙霧測試載入「最新存檔」前先確認 skyrim.ini 的 LocalSaves 設定（2026-10-23）。來源：`agentctl/handoffs/done/2026-09/home-2026-09-12/zhfix2/REPORT.md:92`。

MO2 開關一輪也會補寫 `archives.txt`：之前裝了 BSA 卻沒登記的會被補上，CC BSA 也可能重新排序。這是 MO2 的回寫，不是本次施工的改動。驗收時對 archives.txt 比集合差異，差異只有補登記的 BSA 就單獨 commit（例：「MO2 回寫 archives」），**不要跟本次 modlist 改動混在同一個 profile commit**（2026-10-26 shell-esl 正規化 Arcane 後第一次開關，補了 `Arcane.bsa`／`Arcane - Textures.bsa`；profiles `3e4587d`，`agentctl/handoffs/home-2026-10-26/decide1026/REPORT.md` §4）。

## eslify-overlay-snapshot-goes-stale

> 整包覆蓋 mod（如 ESLify-Overlay）凍結的是建立當下的贏家快照，更新同一支 plugin 的層只要排序在它之下，就會被靜默蓋掉，毫無錯誤訊息。

ESLify-Overlay 在 modlist 的位置不是固定的（2026-10-26 實讀在第 112 行），manifest 寫「要重查 sha256」但沒工具自動做（2026-10-09 LovelyLetter 中文層沒排到其上而被蓋掉）。覆蓋同批 plugin 的新層要保留 ESL flag 並排其上，否則 FormID 槽位改變、存檔道具錯位。反方向也成立：旗標複本放進 overlay 時，**來源 mod 若排在 overlay 上面（優先權更高），複本會被來源蓋掉、旗標不生效**；也不能為此把整個 overlay 往上搬（會反過來蓋掉刻意排在它上面的中文層），要另開一層緊貼在來源 mod 上面（2026-10-26 `NSV Spell Copies.esp` 的來源在第 49 行，改放 `ESLify-Overlay-NSV`；`agentctl/handoffs/home-2026-10-26/eslapply/REPORT.md`）。

**Why:** overlay「凍結贏家」設計跟後續單獨更新同一 plugin 天生衝突，且無錯誤訊息。

**How to apply:** 更新被 overlay 收錄的 plugin 要保留 ESL flag 並排其上；往 overlay 加新複本前，先逐支查來源 mod 的 modlist 行號是否在 overlay 之下，在上面的另開緊貼層；疑似誤停用先查 deploy-manifest，別看到停用就重啟。來源：`agentctl/handoffs/done/2026-10/home-2026-10-09/vf-text3/DONE-eslify-shadow.md`。

## mo2-silent-collision-failure-modes

> MO2 有幾種常見靜默失效：同名 plugin 撞號、非 ASCII 資料夾名——全不報錯，只表現成「裝了沒用」或忽然 CTD。

（2026-08-30～09-01）①同名 `.esp/.esm/.esl` 已知會 CTD，MO2 也拒絕還原該 load order；②同名 plugin 的 VFS 只疊最高優先度一份，判定同角色要讀 EDID，不能只看檔名；③mod 資料夾中文命名會被剝高位元、整包靜默停用，一律改純 ASCII。

**Why:** 三種情況都無錯誤訊息，容易誤判成「沒裝」而查錯方向。

**How to apply:** 啟用新 mod 前掃同名 provider／EDID；新建資料夾一律純 ASCII。來源：`agentctl/handoffs/done/2026-08-31/grow-2026-08-31/dedup_fix.py:1-7`。相關 [[profile-restore-order-and-flags]]。

另兩種同類靜默失效（2026-10-23）：archive 內部路徑帶 `Data/` 前綴直接鋪成 `mods/<層>/Data/...` 會對應到遊戲 `Data/Data/...`，裝前先 `7z l` 檢查頂層再剝掉這層；純覆蓋式更新層（跟既有 mod 同一個 esp 檔名、靠 VFS 排序蓋過去）絕對不能在 plugins.txt／loadorder.txt 另外加一行，它不是新增 plugin 槽。來源：`agentctl/handoffs/done/2026-09/home-2026-09-01/hdmk-2026-09-01/HANDOFF-cx-hd1.md:19-35`、`agentctl/handoffs/done/2026-09/home-2026-09-08/face/REPORT.md:158`。

同一個 mod 裡大小寫不同的重複資料夾（`textures/` 和 `Textures/` 並存，Linux 允許、Windows 不允許）也是同一類（2026-10-26，現役 22 個 mod）。內容沒衝突時 MO2 VFS 會把兩份合併，看起來正常；但 wine 下跑的 Windows 工具（ESLifier）開檔時可能挑到沒有那個檔的一邊，跑到一半崩潰。同路徑兩份內容不同的檔（例：`FOL-Recorder-Bugfix` 的 `000261ff.nif`／`000261FF.nif`），哪一份生效不確定。處理：跑 Windows 工具前先掃描並合併大小寫；內容不同的檔要人看過再決定留哪一份（`agentctl/handoffs/home-2026-10-26/eslifierpoc/REPORT.md` 步驟 3，清單 `eslifierpoc/data/case-duplicate-dirs.txt`）。
