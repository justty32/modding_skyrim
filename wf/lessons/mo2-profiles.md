# MO2 與 profile（1/2）

[lessons 索引](README.md)｜同主題：[mo2-profiles-2](mo2-profiles-2.md)

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

## mo2-auto-adds-stray-mods-dirs

> MO2 啟動會把 mods/ 裡不在 modlist.txt 的目錄自動加進 modlist；houseCARL 寫入工具與各線的暫存驗證目錄都落在 mods/，開 MO2 前必須清掉（原 type: memory）

2026-09-04 lead-inst4 實測：MO2 啟動時會把 `mods/` 底下**不在 `modlist.txt` 的目錄**各自動加一行進 modlist（結尾 `_backup` 的目錄除外），關閉回寫時就落在當前 profile 分支上。houseCARL 的寫入／反編譯工具（`bsa_extract`、`decompile_script` 等）產物預設就建在 `mods/`；post5 的 `_post5-verify/`、cx-old-a 的 `houseCARL - cx-old-a-decompile/` 都是這樣留下的。

**Why:** 這些目錄不在 modlist 時不影響載入，但只要有人開一次 MO2 就變成 profile 髒污，而且是別線的產物混進施工分支。
**How to apply:** 任何線用 houseCARL 寫入或在 `mods/` 放暫存目錄，交接書要寫死「驗完立刻 `mv` 到 `/tmp/`」；持遊戲窗的隊開 MO2 前先 `find mods/ -maxdepth 1` 與 modlist 行數對照（09-04 基準：目錄 1288、modlist 1291，差的只有三個 `ModForge*_backup`）。同類：profiles repo 根的 `tests/`／`tools/`／`workflows/` 也曾被 MO2 當 profile 補檔（2026-10-03 已收進 `.repo/` 根治，見下節）。

## mo2-phantom-profile-workflows-dir

> 2026-10-03 已根治——profiles repo 的非 profile 目錄（tools/tests/workflows/baselines）收進隱藏的 `.repo/`，MO2 不再列幽靈 profile；根目錄只准放真 profile（原 type: project）

**事故**：2026-09-18 20:32 MO2 在 `instance/profiles/workflows/` 生了 archives/loadorder/lockedorder/modlist/plugins/settings.ini 六個預設檔；
2026-10-03 MO2 把 `selected_profile` 切成幽靈 profile `tests`，SKSE 用空 profile 跑成原版（usvfs 559 節點）。
原因：`instance/profiles/` 就是 MO2 的 profiles 根（MO2 端是 symlink），根目錄下每個可見子目錄都被當 profile。

**根治**（profiles `934b24c`，報告 `agentctl/handoffs/home-2026-10-03/phantom/REPORT.md`）：四個非 profile 目錄 `git mv` 到 `.repo/`
（`.repo/tools`、`.repo/tests`、`.repo/workflows`、`.repo/baselines`）。MO2 列 profile 不帶 `QDir::Hidden`，Wine 把點開頭目錄標 hidden，同層 `.git/` 從沒被當 profile。
施工後開關 MO2：`selected_profile=modpack-main`、`.repo/` 沒被生預設檔、profile 檔 md5 不變。

**How to apply:** 不要在 `instance/profiles/` 根新增非 profile 目錄；指令改成 `python3 -B .repo/tools/profile_workflow.py …`；
09-03～09-18 舊 handoff 腳本寫死 `instance/profiles/tools/` 舊路徑，重跑前要改。
另：plugins.txt 在 MO2 跑過後可能整檔重排，啟用集合比對才算數（同 [[profile-restore-order-and-flags]]）。

## dsport-dev-profile-drift

> 2026-09-18 抓到 dsport-dev profile 是 09-05 快照，漏掉 09-14／09-16 兩輪共 12 項裁示（BCE、ICOW 6、RSC 4）；測試 profile 要跟 modpack-main 的裁示對帳（原 type: project）

2026-09-18 dsp-game 隊發現 `dsport-dev` profile 停在 09-05 狀態：09-16 停用 Better Combat Escape（MaxsuCombatEscape.dll cell hook，同址 CTD `SkyrimSE.exe+04D0038` 真凶）只做進 modpack-main；ICOW 組 6 個仍開、取代它的 OCW 補丁關著；RSC 組 4 個也沒同步。當天先停 BCE（c5b9893），使用者拍板整批同步後 15:44 完成（profiles 0d6ba5f）：實際 10 mod＋13 plugin，plugins.txt 比對才是權威（6 支母 mod 兩邊都開只是 esp 個別關）；第「11 項」DSPortP3 本身是 dsport-dev 存在的理由不能同步（差異在 `handoffs/home-2026-09-18/dsp-game/data/profile-drift.json`）。

**Why:** 在過期的測試 profile 上做實機驗收，CTD 會被錯歸因給受測物（09-13 dsp8 把 BCE 的鍋算到 navmesh 頭上）。

**How to apply:** 用非 main profile 做實機前，先 diff 它跟 modpack-main 的 modlist/plugins，把「已裁示停用的 mod」列出來；crash 先看 callstack 點名哪個 SKSE DLL，再怪內容。相關：[[custom-navm-combat-pathing-ctd]]、[[profile-restore-order-and-flags]]。
