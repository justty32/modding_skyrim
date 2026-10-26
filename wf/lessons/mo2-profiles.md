# MO2 與 profile

[lessons 索引](README.md)

## profile-restore-order-and-flags

> MO2 profile 事故（2026-08-27 全停用＋名稱序重排）的教訓：還原要同時還原「順序」與「旗標」；MO2 開著時絕不改 profile 檔；檔案層啟用要連 plugins.txt 一起補（原 type: memory）

2026-08-27：modlist 被誤觸全部停用並**按名稱重排**，MO2 退出時把 plugins/loadorder/archives 清成只剩原版；只用 git HEAD 還原**啟用旗標**、沿用事故檔的**字母序**，結果 TK Dodge RE 的原版行為圖壓過 Pandora Output（第三人稱無法攻擊），大量 loose 檔勝出者改變，多個中文層與 ElevenLabs 配音層被本體壓掉。

**Why**：modlist.txt 的行序就是優先度（檔內越上越優先，MO2 左欄相反）。只看啟用數對得上就宣告還原成功，是「檢查失效時給出最令人安心的答案」的又一例。

**How to apply**：
還原 profile 一律以「已知正確順序的副本」為基準（git HEAD 或各線收線前的 `modlist.txt.bak`），
再把新 mod 插回、再套旗標；驗收要跑 loose-file winner 模擬（opus-qa-triage 的方法），
不能只比啟用數。

**MO2 開著時絕不改 profile 檔**——它退出會整份覆寫。批次啟用改走「關 MO2 → 改檔 → 重開」。

MO2／遊戲開著時 profile 檔是暫態（plugins.txt 會變 LF、archives.txt 變 0 bytes）：commit profile 三檔前先 `ps` 確認 MO2 已退出、`file` 確認 CRLF，否則等 MO2 退出回寫後再 commit（2026-09-16）。

MO2／遊戲重開造成的 profile 三檔整檔重排／換行漂移，不得跟持鎖隊自己的變更混進同一筆 commit；收線時把這類回寫漂移另立一筆、訊息標明「MO2 回寫」（09-11 裁示，`agentctl/handoffs/done/2026-09/home-2026-09-11/COMMON/03-rulings-morning.md:8`）。

檔案層把 mod 改 `+` 後，MO2 認到的新插件**預設未勾**，plugins.txt 要一起補 `*`。

Python 改檔先讀後寫，且 `open(...,"w")` 在參數求值前就會截斷檔案——腳本炸在 join 也會留下空檔；
改前一律先 cp 備份。

中文層在 MO2 左欄要排在本體**下面**（檔內在上面）；跟使用者講順序用「左欄」的說法。

Steam 若在啟動前跳更新：Downloads 暫停 → Go Offline → 再啟動；1.6.1170 備份在
`~/skyrim_mods/steam-build-backup/`。

modlist.txt 的 separator 行位於它所轄群組「之後」（歸屬＝行號大於它的第一個 separator）；plugins.txt／loadorder.txt 的優先方向與 modlist.txt 相反（modlist 越上面優先權越高；plugins/loadorder 是檔尾後載入者贏、master 必須排在依賴它的 plugin 前）。同一支腳本要同時改寫兩者不能共用一套拓撲排序，上線前先拿已知答案的樣本驗證方向（方向判錯會整批假陽性）。來源：`agentctl/handoffs/done/2026-09-02/lorerim-2026-09-02/team-src/REPORT.md:30-33`、`agentctl/handoffs/done/2026-09/home-2026-09-05/lrin/REPORT.md:78`、`agentctl/handoffs/done/2026-09-01/hzh-2026-09-01/cx-hz2/REPORT.md:1-15`。

檔案優先度（中文層蓋過英文本體檔）與 plugin 記錄層的載入順序是兩套獨立機制：中文層在檔案層贏了，仍可能有以該插件為 master 的後載 ESP 在記錄層把同欄位蓋回英文，調 modlist 優先度救不了。驗收「中文層生效」要另外用 `cross_plugin_query(..., conflict_tree=true)` 追 override_depth，有後載入插件蓋掉就做 patch plugin 轉發。來源：`agentctl/handoffs/done/2026-08-28/opus-apply-order/STATE.md:207-222,273-286`。

批次插入多筆 modlist 行要由檔案下方往上插（insert_order 由大到小），由上往下插會推移下面所有錨點行號。新裝帶 ESM 旗標（TES4 flags 含 0x1）的 master 不能直接附加到 plugins.txt/loadorder.txt 檔尾，要插在 DynDOLOD.esm 那一行正上方，否則 MO2/引擎會重排、星號掉掉。來源：`agentctl/handoffs/done/2026-08-28/opus-install-prep/PLAN.md:34-42`、`agentctl/handoffs/done/2026-09/home-2026-09-12/want5/REPORT.md:84`。

契約寫「REMOVE-FROM-MODLIST」時，只把啟用行改成 `-`（停用）不算；真正的「移除」必須整行刪除＋搬走 mod 目錄兩步一起做，否則該行指向已移走的目錄，MO2 下次開啟會顯示異常。來源：`agentctl/handoffs/done/2026-09/home-2026-09-03/inst5/REPORT.md:59`。

相關：[[launch-skyrim-via-steam]]、[[verify-waituser-against-logs]]

## dsport-dev-profile-drift

> 2026-09-18 抓到 dsport-dev profile 是 09-05 快照，漏掉 09-14／09-16 兩輪共 12 項裁示（BCE、ICOW 6、RSC 4）；測試 profile 要跟 modpack-main 的裁示對帳（原 type: project）

2026-09-18：`dsport-dev` profile 停在 09-05 狀態，Better Combat Escape（MaxsuCombatEscape.dll cell hook，同址 CTD `SkyrimSE.exe+04D0038` 真凶）的停用只做進 modpack-main；ICOW 組、RSC 組也沒同步。使用者拍板整批同步，已於 2026-09-18 完成（profiles 0d6ba5f）。plugins.txt 比對才是權威（母 mod 兩邊都開時可能只是 esp 個別關）；DSPortP3 本身是 dsport-dev 存在的理由，不能同步（差異在 `handoffs/home-2026-09-18/dsp-game/data/profile-drift.json`）。

**Why:** 在過期的測試 profile 上做實機驗收，CTD 會被錯歸因給受測物（BCE 的鍋曾被算到 navmesh 頭上）。

**How to apply:**
- 用非 main profile 做實機前，先 diff 它跟 modpack-main 的 modlist/plugins，把「已裁示停用的 mod」列出來；crash 先看 callstack 點名哪個 SKSE DLL，再怪內容。
- 改 profile 名稱時要連同所有 baseline manifest 一起改，派 QA 線前先核對一致：`agentctl/qa/baselines/modpack-kr-dev/baseline-manifest.json` 寫的 profile 是舊名「Modpack-KR」，現役是 modpack-main，preflight 載存檔會因 profile 不符 fail-closed（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-05/ab/REPORT.md:77`）。

相關：[[custom-navm-combat-pathing-ctd]]、[[profile-restore-order-and-flags]]。

## game-rewrites-plugins-orphans-and-seq-bsa

> 2026-10-10 MO2 load order 每次被打亂的真因是 SkyrimSE 把停用＋缺 master 的 plugin 搬到最上面；普通 esp 永遠排在 master 類後；11 個 BSA 重打包了 SEQ，mod 更新要重做

（1）MO2（和引擎）一律把普通 esp 排在所有 master 類（ESM 旗標或 `.esm`／`.esl`）之後；把 esp 夾在 USSEP 前「讓它輸」不會生效。MO2 2.5.2 原始碼 `fixPluginRelationships()` 每次 refresh 都把 master 類搬到所有普通 esp 前面、`setPluginPriority()` 明寫「esp 不准搬到 esm 上面」，lockedorder.txt 也鎖不住（本機長期寫在 USSEP/USMP 前的普通 esp 實測只有 8 筆 record 真的翻盤）。houseCARL 判贏家照 `plugins.txt` 字面順序、沒套這條規則，會判錯。

（2）SkyrimSE 啟動會改寫 `plugins.txt`，把停用且缺 master 的 plugin 搬到最上面，MO2 讀回後 master 區尾段每次亂排。修法：這類孤兒 plugin 改 `.mohidden`（清單 `agentctl/handoffs/2026-10-10/post-test-fix/data/hide-orphans-manifest.json`）。

（3）11 個 mod（arnima、USMP、SPERG、HLIORemi、VLIOVarinia 等）的 SEQ 包在 BSA 裡，已重打包；其餘 42 支用 mod `SEQ Regenerated 2026-10-10`。原 BSA 備份 `~/skyrim_mods/_seq-bsa-backup-2026-10-10/`。

（4）固定一批 ESL/ESM（Aqua、HSResources、DD_warrior、Midnight Sun、Astral、AncientBloodII、Shockwave、FalkreathShades）每次玩完都會被 MO2 回寫排序位置，是既有回寫行為，看到位移可直接 git checkout 還原不必重查。

來源：`agentctl/handoffs/done/2026-10/home-2026-10-10/mo2-reorder/REPORT/investigation.md`、`agentctl/handoffs/done/2026-10/home-2026-10-08/newsave/REPORT-build.md`。

**Why:** 開 MO2＋遊戲後 profile 永遠 dirty、驗收規則寫了不可能成立的順序。

**How to apply:** 新增 plugin 排序時 esp 不能放進 master 區；拔 mod 時連孤兒補丁一起 `.mohidden`；`instance/tools/reverify.py` 的 ORPHAN／SEQBSA 亮紅就照 `mod-library/artifacts/seq-bsa-repack/` 重做。驗贏家要用「引擎實際順序」（`mo2-reorder/tools/winner_diff.py`）。相關：[[mo2-first-launch-drops-new-plugin-star]]、[[copied-fomod-choices-need-soft-dependency-audit]]。


## plugins-txt-format-fragility

> plugins.txt 有兩種合法格式（MO2 產生 vs 遊戲自身產生），格式判斷錯或混用換行會讓 esp 靜默變停用，不報錯。

- MO2 版以「Mod Organizer」開頭、要求 CRLF、啟用行帶 `*`。
- 遊戲自身產生版以「This file is used by Skyrim」開頭，不帶 `*` 也算啟用。
- 改 CRLF 檔時只把動到的行寫成 LF 會造成混合換行。
（2026-09-02～03）

**Why:** 格式判斷錯或混用換行都讓 esp 變「存在但停用」，且無錯誤訊息。

**How to apply:** 改 plugins.txt 前先讀首行判斷格式分支，不照抄交接書假設；驗收加一條「整檔逐行同一種換行」。來源：`agentctl/handoffs/done/2026-09/home-2026-09-02/dsview/cx-dsview2/REPORT.md:39`。


## concurrent-profile-edits-need-ref-reads

> 多線並行改同一個 profile 時，讀檔要走 git ref 不讀工作樹；撤銷某一輪要寫反向 manifest，不能直接 revert。

- 中途有別線改動時，`layer_apply --revert` 會因 sha256 不符被拒；改寫「反向 manifest」並先 dry-run（`--force` 會吃掉別線的事）（2026-10-03）。
- 工作樹常被別線切分支，只讀時用 `git show <ref>:modpack-main/modlist.txt` 讀 blob，不直接 `cat` 工作樹（2026-10-10）。

**Why:** 本工作區常態多線碰同一份 profile；讀工作樹或 `--force` revert 都會吃掉別線進度。

**How to apply:** 只讀腳本一律 `git show <ref>:<path>`；撤銷某輪且中間已有別線動作，優先寫反向 manifest 並 dry-run。來源：`agentctl/handoffs/done/2026-10/home-2026-10-03/worldfix/REPORT.md`。
