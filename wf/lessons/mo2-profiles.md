# MO2 與 profile

[lessons 索引](README.md)｜plugin 排序被引擎／MO2 改寫與 plugins.txt 格式見 [mo2-auto-rewrites](mo2-auto-rewrites.md)

## profile-restore-order-and-flags

> 還原 profile 要同時還原「順序」與「旗標」；MO2 開著時絕不改 profile 檔；檔案層啟用要連 plugins.txt 一起補；MO2 回寫另立 commit（2026-08-27）

modlist.txt 的行序就是優先度（檔內越上越優先，MO2 左欄相反）。只還原啟用旗標、沿用錯的順序，會讓行為圖、loose 檔勝出者、中文層與配音層整批被壓掉；只看啟用數對得上就宣告還原成功，是「檢查失效時給出最令人安心的答案」。

- 還原一律以「已知正確順序的副本」為基準（git HEAD 或各線收線前的 `modlist.txt.bak`），再插回新 mod、再套旗標；驗收跑 loose-file winner 模擬（opus-qa-triage 的方法），不能只比啟用數。
- **MO2 開著時絕不改 profile 檔**——它退出會整份覆寫。批次啟用走「關 MO2 → 改檔 → 重開」。
- 檔案層把 mod 改 `+` 後，MO2 認到的新插件**預設未勾**，plugins.txt 要一起補 `*`。
- Python `open(...,"w")` 在參數求值前就截斷檔案，腳本炸在 join 也會留空檔；改前一律先 cp 備份。
- 中文層在 MO2 左欄要排在本體**下面**（檔內在上面）；跟使用者講順序用「左欄」的說法。
- 契約寫「REMOVE-FROM-MODLIST」時，只改 `-`（停用）不算；要整行刪除＋搬走 mod 目錄兩步一起做，否則該行指向已移走的目錄（`agentctl/handoffs/done/2026-09/home-2026-09-03/inst5/REPORT.md:59`）。

**MO2 回寫**：MO2／遊戲開著時 profile 檔是暫態（plugins.txt 會變 LF、archives.txt 變 0 bytes）；commit 三檔前先 `ps` 確認 MO2 已退出、`file` 確認 CRLF（2026-09-16）。MO2 開關一輪造成的整檔重排、換行漂移、archives.txt 補登先前沒登記的 BSA（CC BSA 也可能重排），不得跟持鎖隊自己的變更混進同一筆 commit：另立一筆、訊息標明「MO2 回寫」（09-11 裁示，`agentctl/handoffs/done/2026-09/home-2026-09-11/COMMON/03-rulings-morning.md:8`；archives 例 profiles `3e4587d`，`agentctl/handoffs/home-2026-10-26/decide1026/REPORT.md` §4）。比對方法見 [[mo2-revert-check-normalized-diff]]。

**方向**：modlist.txt 的 separator 行位於它所轄群組「之後」（歸屬＝行號大於它的第一個 separator）；plugins.txt／loadorder.txt 的優先方向與 modlist.txt 相反（檔尾後載入者贏、master 必須排在依賴它的 plugin 前）。同一支腳本要同時改寫兩者不能共用一套拓撲排序，上線前先拿已知答案的樣本驗方向（方向判錯會整批假陽性）。來源：`agentctl/handoffs/done/2026-09-02/lorerim-2026-09-02/team-src/REPORT.md:30-33`、`agentctl/handoffs/done/2026-09/home-2026-09-05/lrin/REPORT.md:78`、`agentctl/handoffs/done/2026-09-01/hzh-2026-09-01/cx-hz2/REPORT.md:1-15`。

**批次插入**：多筆 modlist 行由檔案下方往上插（insert_order 由大到小），由上往下插會推移下面所有錨點行號。新裝帶 ESM 旗標（TES4 flags 含 0x1）的 master 不能直接附加到 plugins.txt／loadorder.txt 檔尾，要插在 DynDOLOD.esm 那一行正上方，否則 MO2／引擎會重排、星號掉掉。來源：`agentctl/handoffs/done/2026-08-28/opus-install-prep/PLAN.md:34-42`、`agentctl/handoffs/done/2026-09/home-2026-09-12/want5/REPORT.md:84`。

**兩層機制**：檔案優先度（中文層蓋過英文本體檔）與 plugin 記錄層的載入順序互相獨立：中文層在檔案層贏了，仍可能有以該插件為 master 的後載 ESP 在記錄層把同欄位蓋回英文，調 modlist 救不了。驗「中文層生效」要另用 `cross_plugin_query(..., conflict_tree=true)` 追 override_depth，被後載插件蓋掉就做 patch plugin 轉發。來源：`agentctl/handoffs/done/2026-08-28/opus-apply-order/STATE.md:207-222,273-286`。

相關：[[launch-skyrim-via-steam]]、[[verify-waituser-against-logs]]

## dsport-dev-profile-drift

> 測試 profile（dsport-dev）會落後 modpack-main 的裁示；用它做實機前要對帳，改 profile 名要連 baseline manifest 一起改（2026-09-18）

在過期的測試 profile 上做實機驗收，CTD 會被錯歸因給受測物（2026-09-18 dsport-dev 漏同步 Better Combat Escape 的停用，MaxsuCombatEscape.dll cell hook 的 CTD `SkyrimSE.exe+04D0038` 被算到 navmesh 頭上；整批同步見 profiles `0d6ba5f`）。

- 用非 main profile 做實機前，先 diff 它跟 modpack-main 的 modlist／plugins，列出「已裁示停用的 mod」；plugins.txt 比對才是權威（母 mod 兩邊都開時可能只是 esp 個別關）。DSPortP3 是 dsport-dev 存在的理由，不同步（差異表 `handoffs/home-2026-09-18/dsp-game/data/profile-drift.json`）。crash 先看 callstack 點名哪個 SKSE DLL，再怪內容。
- 改 profile 名稱時連同所有 baseline manifest 一起改，派 QA 線前先核對：`agentctl/qa/baselines/modpack-kr-dev/baseline-manifest.json` 寫的 profile 是舊名「Modpack-KR」，現役是 modpack-main，preflight 載存檔會因 profile 不符 fail-closed（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-05/ab/REPORT.md:77`）。

相關：[[custom-navm-combat-pathing-ctd]]、[[profile-restore-order-and-flags]]。

## concurrent-profile-edits-need-ref-reads

> 多線並行改同一個 profile 時，讀檔要走 git ref 不讀工作樹；撤銷某一輪要寫反向 manifest，不能直接 revert。

- 工作樹常被別線切分支：只讀腳本一律 `git show <ref>:modpack-main/modlist.txt` 讀 blob，不直接 `cat` 工作樹（2026-10-10）。
- 中途有別線改動時，`layer_apply --revert` 會因 sha256 不符被拒；改寫「反向 manifest」並先 dry-run，`--force` 會吃掉別線的事（2026-10-03）。

來源：`agentctl/handoffs/done/2026-10/home-2026-10-03/worldfix/REPORT.md`。

## mo2-revert-check-normalized-diff

> MO2 回寫會使還原前置 hash 不符；強制還原不是例行跳過保護。

- 情境：收場時 MO2 回寫 plugins／loadorder，普通 revert 遇到基線差異。差異可能限標頭、行尾與停用行，但不能簡化為永遠只有 CRLF／LF。
- 驗法：停止遊戲及 MO2 後，保留原 bytes／hash／還原前副本；另做正規化行尾的 diff，並人工核啟用星號、有效順序及所有非行尾差異；最後對照裝前 hash。
- 避法：只有授權的實體座位在差異全數可解釋、確認沒有新使用者改動後，才按工具還原程序評估 `--force`。遇不明差異停下回報，不把 force 當工具拒絕的繞過法。
- 出處：`agentctl/handoffs/home-2026-11-25/miku-face/gpt-nomouse/REPLIES-instance.md:31`、`:48`（agentctl `a43517d9`）。
