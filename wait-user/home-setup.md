# 回家下載／重建

## LoreRim 借用後續：只剩三題（2026-09-05 核對後縮小）

2026-09-03 已入庫 439 件／8.966 GB，借用段 359 件、42 個中文層與 16 個框架／解鎖件已上線。
原本六題，**四題已在 09-03／09-04 落地或裁示**（搬到本檔末尾的已完成節），剩下這三題還等你：

1. **21 件中文層拓撲 FAIL 是否全改自製。** 09-03 `lrzh` 契約寫死不碰，至今沒動；
   `lrrev` 已逐件記 `fail_reason`。證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/lrzh/REPORT.md:128`
   （「沒做：FAIL 21 件」）、同檔 `:155`。
2. **五件 `NO-PEX-UPSTREAM` 借用件（CFTO 以外）留著還是停用。** 三處（archive／Nexus／BSA）都沒有 `.pex`，
   Papyrus `Cannot open store` 剩的 5 筆正是它們。逐件表：
   `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/lrzh/REPORT.md:56-60`
   （LR-0267 CFTO、LR-0292、LR-0302、LR-0206、LR-0085）。
3. **xLODGen 要不要找站外來源。** 全站查證結論是**不在 Nexus**（正式管道是 Sheson 在 `stepmodifications.org` 的發佈帖），
   本機 DynDOLOD Alpha-210 的 65 個 docs 檔也查不到下載位址或版本要求，**不能推定版號**。
   不要＝遠景地表停在原版精度，不影響已完成的物件 LOD／樹 LOD／Occlusion。
   證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/lr3/REPORT.md:28`、
   `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/lod/REPORT.md:28`／`:76`。

> **2026-09-05 追加的上位裁示**：使用者當日 14:00 說「LoreRim 裡面的東西我全都要」，範圍＝371 件
> （BORROW 176＋ASK 195，621 件 SKIP 不碰），已由 `lead-lr` 解析對版、依賴閉包與下載入庫，安裝計畫 B0–B8 已 push。
> 證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/STATE.md:73`／`:84`、
> modpack-design commit `c064897`。**那是新的一批，不取代上面這三題。**
> **19:20 後續更正**：使用者已改選 LoreRim 清單，371 件全收計畫不再是現行下載範圍；目前等待使用者貼回
> localStorage 選單，下載暫停。原 14:00 裁示留在上段作歷史，不可再當執行指令。
> 證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/STATE.md:97`。

## GO19 剩餘幾何：只剩兩件（2026-09-05 核對後縮小）

原文五項裡**三項已落地**（見本節末），還等你的只有幾何覆核這一段：

- **95283 The Tempest Isle（13 筆）與 136457 Pride of the Niben（38 筆）的 xEdit 幾何覆核由誰做**，
  以及**已安裝件的空間紀錄人眼覆核**。
  A＝開 xEdit 專線逐區看完（`cx-go19x2` 已把 136457 按 worldspace／grid 象限分成 ≤12 組，一區一次看得完）；
  B＝維持現況，延後所有視覺風險。
  證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/go19x/REPORT.md:110`／`:112`、
  `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/inst2/REPORT.md:126-127`／`:141`
  （dispatcher 依使用者「隨便」的裁示決定今天不裝、留日後 xEdit 專線）。

**已落地、不再列 open 的三項**（2026-09-05 實讀證據）：

- **71864 MCO moveset 已裝**——`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:594`
  ＝`+GO19-71864-ER-Twinblade-MCO`（啟用）；施工紀錄
  `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/inst3/REPORT.md:23`／`:74`
  （`instance/profiles` commit `34d1809`）。
- **`go19x-130252-cr.esp` 已停用**——同上 `modlist.txt:819`＝`-houseCARL - go19x-130252-cr`。
- **LOD 排程已完成**——2026-09-04 DynDOLOD 首跑成功（TexGen 1:24／DynDOLOD 35:38），
  `DynDOLOD_Output` 已裝成 mod，profiles promote 到 `ff1a09a`。證據：
  `/home/lorkhan/repo/moddings/skyrim/agentctl/logs/lod-run-2026-09-04.md`、
  `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/lod/REPORT-run.md`、
  `instance/profiles` commit `ff1a09a`。

## 現役 modlist 整合度盤點的三個待辦

盤點結論見 [`modpack-design/content-plan/modlist-coverage-2026-09-01.md`](../modpack-design/content-plan/modlist-coverage-2026-09-01.md)
（2026-09-01 公司端離線產出，未經 xEdit 與實機驗證）。回家要決／要查的三件：

1. **敵人／AI／怪物多樣性要不要補**，以及是否在開新檔前補。現役只有 AI Overhaul 一個家族，
   查無怪物池類 mod；敵人池晚加會影響已生成 encounter。**仍未裁示。**
   （2026-09-05 相關進展：`lead-lrgq` 已把 LoreRim 的 creature 102 件逐件盤完並出 `DECISION.html`，
   同日使用者裁「LoreRim 的東西全都要」371 件——那批**可能覆蓋一部分怪物池**，但不等於本題已答。
   證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/STATE.md:68`／`:73`、
   `/home/lorkhan/repo/moddings/skyrim/modpack-design/content-plan/lorerim/gameplay-quest/`。）
2. **需求／生存要不要開**（飢渴／體溫／紮營）。文件面是「尚未決」而非「決定不做」
   （`modpack-design/content-plan/gameplay/OPEN.md:9`）。**仍未裁示。**
   （2026-09-05 只裁了相鄰但不同的一題：**CC 的 Survival Mode 維持永久關**，
   證據 `/home/lorkhan/repo/moddings/skyrim/modpack-design/content-plan/lorerim/cc-plan.md` 第八節。
   那是「不用官方 CC 那套」，沒有回答「要不要用第三方需求／生存 mod」。）
3. **查 mo2ctl 為何沒追上 profile 變動**。**2026-09-05 實讀仍然對不上**：
   `/home/lorkhan/repo/moddings/skyrim/instance/profiles/manifest.json` 的 `updated_at`＝`2026-09-03T05:20:04Z`，
   而 `instance/profiles` main 已到 `5f47044`（2026-09-05）、`modlist.txt` 啟用 1278／`plugins.txt` 啟用 851。
   原文寫的「停在 2026-08-30T09:52」已過期，但**漂移本身沒修好**。同一件事在
   `/home/lorkhan/repo/moddings/skyrim/agentctl/status/todo/06-manifest數字對不上.md` 另有一份筆記。

   **狀態（2026-09-02 晚，home 隊）**：已定位——`updated_at` 實為 2026-09-01T11:47Z；mo2ctl `cmd_enable/cmd_disable`、人工直寫與 MO2 關閉寫回都不更新 manifest，差集 605／488／181／64；修法建議（`commit_profile()` 收口／關 MO2 後 reconcile）見 [mo2ctl-drift-diagnosis.md](../agentctl/handoffs/home-2026-09-02/home/mo2ctl-drift-diagnosis.md)。
   **裁示（2026-09-02 晚，引文）**：home-3 C——拆 provenance／live checkpoint，`mo2fix` 隊承接。

另：`major-content-preflight-2026-09-01/` 的 9 件裡有 6 件其實早已安裝啟用，該批任務單與批次計畫
的框架語意需要對現況重新校正（更正段已加在 `home-batching-plan.md` 開頭）。

## 已完成（封存）

> 以下六項在 2026-09-05 逐條對照證據後判定已完成，從 open 清單移到這裡保存歷史；每項附證據絕對路徑或 commit hash。

### ~~改走 MCO：照遷移計畫執行（2026-09-02 裁示）~~（2026-09-02 由 dispatcher 完成，證據 /home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-02/mco2/REPORT.md）

**判定：已完成（2026-09-02 施工，2026-09-05 核對無異動）。**

使用者 2026-09-02 決定把戰鬥框架從 BFCO 移回 MCO。計畫與清單由團隊 `mco` 產出：
`modpack-design/content-plan/gameplay/mco-migration-plan-2026-09-02.md`（七階段：備份基線→框架切換→33 件 moveset 還原→相容層→Pandora 重跑→中文→16 條實機驗收）
與 `data/mco-{migration-steps,restore-list,framework-queue}.csv`。回家先做第一階段備份，再照 `steps.csv` 的 `status` 逐步推進；
框架隊列的 Nexus id／版本走 houseCARL，DLL 一律找 1.6.1170 對應版。**通過**＝16 條實機驗收全過、缺 master 0、無新 crash。

**狀態（2026-09-02 22:33，dispatcher）**：**本項完成。** P2／P3／P5／P6 由 mco2 隊施工，P4／P7 16 條＋字形 gate 使用者 22:15 實機全過，`release/2026.09.02-mco` 已 promote 到 `instance/profiles` main（`9e188e2`）並 push；回滾窗解除。只剩 SCAR 2 v2.01 安裝（V-A 已過，可裝）列在 `agentctl/handoffs/NEXT-SESSION.md` 第 8 項。

### AE DLC 授權確認與 CC 第二輪

**判定：已完成（2026-09-03 查明＋2026-09-04 施工）。** 兩段證據：
① AE 授權沒問題、卡點不是授權——Anniversary Upgrade（appid 1746860）在 Steam 的資料裡**連一個 depot 都沒有**，
   走 Steam 永遠拿不到 CC；現役安裝已是三個公開 depot 的 100%（size 16,092,533,099 兩邊完全相同）。
   證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/ae2/REPORT.md`（第一節與 8 行摘要）、
   同目錄 `depot-findings.md`、`data/depots-489830.csv`。
② CC 內容改由遊戲內 Creations（Bethesda.net 登入）取得後已落地：2026-09-04 `cc` 隊
   **啟用 53 件／排除 LoreRim 四類 17 件／USCCCP 46／官方簡中字串層 210 檔涵蓋 70 件**，隱含 master 13→59。
   證據：`instance/profiles` commit `01c1957`、
   `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/cc/REPORT.md`、
   `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/SESSION-LOG.md`（「09-04 使用者裁示」節，CC＝B）。
exe 仍為 1.6.1170、釘版未破。**LoreRim 的 `5-after-AE` 34 列不再被擋。**

**裁示：買。**（2026-09-02 使用者當場口頭，LoreRim 調查衝突帳第 2 件。）但同場裁示 ① 維持 1.6.1170 釘版。
購買本身不動 exe；**下載 Creation Club 內容要 Steam 上線並進遊戲主選單，上線即會觸發更新到 1.7.99**
（`AutoUpdateBehavior` 風險見 2026-09-01 裁示 8A）。回家順序：先備份現役 exe／`Data` 的 CC 相關檔與 depot manifest，
確認有降版手段（depot 回滾或 downgrader；**使用者記得有，回家先找出來驗證可用**），再上線購買與下載 CC，下載完立刻回離線並核對 exe 仍為 1.6.1170。
**通過**＝CC 內容全部到位、exe 版本不變、現役 profile 可開到主選單。之後 LoreRim 的 Creation Club 段
（`quests-and-lands.json` 的 25 件 CC 與其 patch）才能進借用盤點。

**狀態（2026-09-02 晚，home 隊）**：降版前置已就緒——本機 `~/skyrim_mods/steam-build-backup/…-FULL/` 可回填 1.6.1170（三份 exe hash 相同、小備份 sha256sum -c 4/4）；wSkeever patcher 169962 本機沒有，下載單已寄 lead-lrdl。證據：[downgrade-readiness.md](../agentctl/handoffs/home-2026-09-02/home/downgrade-readiness.md)。
**裁示（2026-09-02 晚，引文）**：home-4 A——降版用 FULL 回填；patcher 169962 只當第二備援。

**狀態（2026-09-03）**：Steam 升到 1.7.104 後已用 FULL 完整回填 1.6.1170，smoke PASS，但付費 CC 一個都沒下載到；
請親自確認 Anniversary Upgrade 是否真的買了、DLC 是否勾選。若都有，A＝授權約一小時第二輪只抓 CC depot 再回填；
B＝不跑，LoreRim `5-after-AE` 34 列繼續擋住。`pre/post-ae-2026-09-03/` 440 MB 建議等答案後再決定是否清。

### ~~Serana Dialogue Add-On 4.3.2 exact 簡中 topology gate~~（2026-09-02 由 dispatcher 完成，證據 /home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-02/sda/REPORT.md）

**判定：已完成（2026-09-02 施工，2026-09-05 核對無異動）。**

**裁示：A —— SDA 升 4.3.2 並採 exact 簡中層。**（2026-09-01，使用者當場口頭裁示；見
[裁示簡報](decision-briefs-2026-09-01.md)第 1 條。）回家取得 SDA 4.3.2 official archive 與 `78511`
簡中 `4.3.2v1.2` exact archive，做 binary topology gate；核對 plugin／master、record 與 script／asset
覆寫面，不能讓舊版繁中層回滾 4.3.2 修正。**通過**＝版本與 master 對版、中文層只改預期文字面、
沒有舊版 record／script／asset 回滾；證據落檔後才可進部署。

**狀態（2026-09-02 晚，home 隊）**：4.3.2 本體與 exact 簡中 archive 均已在庫、`sda-2026-08-31` 3 gates PASS 且兩層已啟用；舊 4.1.1.3 中文層（modlist 第 29 行）仍啟用，待裁示是否停用。證據：[sda-mihail-library-precheck.md](../agentctl/handoffs/home-2026-09-02/home/sda-mihail-library-precheck.md)。
**裁示（2026-09-02 晚，引文）**：home-1——先搜有無更新／更完整中文層，沒有就自製（沿用 zh-layer 自製翻譯輪）；舊 4.1.1.3 層（modlist 29）停用列入下一批 profile 變更；查證見 [zh-check](../agentctl/handoffs/home-2026-09-02/rule/zh-check.md)。
**狀態（2026-09-02 22:34，dispatcher）**：**本項完成。** sdazh 隊自製補完層（81 欄）已入庫，sda 隊發現現役 esp 贏家其實是英文本體（中文層被遮），新層插英文本體之前、舊 4.1.1.3 停用，已套用並 record（`instance/profiles` `9eb708d`，分支 `feat/zh-dsport-2026-09-02`）。實機看 Serana 是否中文改列 [整包驗收](integrated-runtime.md)。

### Mihail 自然核心首批 4–6 件 preflight

**判定：已完成（2026-09-04 施工）。** 首批 **5 個本體＋5 個 CHS 中文層**（全 ESPFE，loadorder 末尾）已部署。
證據：`instance/profiles` commit `af632e9`（訊息「old 施工包：Mihail 自然核心首批 5 本體＋5 個 CHS 中文層」）、
`/home/lorkhan/repo/moddings/skyrim/modpack-design/content-plan/lorerim/`（download-queue 追加 Mihail 首批 10 列，modpack-design `9467563`）。
2026-09-02 的「home-2 A——`targets.json` 8 件全進」裁示與實際落地 5 件的差額，若要補齊請另立一條，本項不再列 open。

**裁示：A —— 自然核心小批、原生 hand-placed、接受 exact CHS。**（2026-09-01，使用者當場口頭裁示；
見[裁示簡報](decision-briefs-2026-09-01.md)第 3 條。）回家取得選中 4–6 件的 base／中文 archives，
逐件掃 CELL／worldspace placement、asset 與 record，並對新增 ingredient／food、actor stats／ability／
combat style 做 Apothecary 與現役 EnaiRim 語意 preflight；不得偷換成全域 SkyPatcher 分布。
**通過**＝每件都有可回滾單位、exact 中文對版與明列的 winner／patch 結論，CELL／asset／record 衝突及
Apothecary／Enai 接觸面全數有處置，才能排入施工。

**狀態（2026-09-02 晚，home 隊）**：首批（`hmih-2026-09-01/targets.json`）14/14 archive 在庫且大小符合，8/8 件已有 preflight gate 證據，無需下載；但該 8 件相對裁示 3A「自然核心 4–6 件」的範圍差異待使用者裁示。證據：[sda-mihail-library-precheck.md](../agentctl/handoffs/home-2026-09-02/home/sda-mihail-library-precheck.md)。
**裁示（2026-09-02 晚，引文）**：home-2 A——`targets.json` 8 件全進，安裝排入下一批 profile 變更。

### ~~scene-capture-bridge 完整離線測試~~（2026-09-02 由 home 隊完成，證據 /home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-02/home/scene-capture-bridge-mingw-build.md）

**判定：已完成（2026-09-02 由 home 隊補上 vcpkg `x64-mingw-static`，2026-09-05 核對無異動）。**

`scene-capture-bridge` 的 portable MinGW CTest 2/2 PASS，但完整 `x64-mingw-static` nlohmann-json
triplet 仍缺，需要能跑 vcpkg build 的環境補上；不得改測試掩蓋缺依賴。

**狀態（2026-09-02 晚，home 隊）**：已補上——本機 vcpkg `x64-mingw-static` 交叉編譯完成，CTest 2/2 PASS（含 ModForge contract），未改測試碼。證據：[scene-capture-bridge-mingw-build.md](../agentctl/handoffs/home-2026-09-02/home/scene-capture-bridge-mingw-build.md)。

另外兩個已於 2026-08-25 在家補完，見
[`handoffs/done/README.md`](../agentctl/handoffs/done/README.md)：`darksouls-port` 35/35、
`ModForge` 1190/1190，兩者都沒有測試碼變更。

### DMK 1.5.0 人工校對版

**判定：已完成（人工校對層已上線）。** 2026-09-05 實讀現役 profile：
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:520`
＝`+Directional Movement Keys Traditional Chinese Human Reviewed 1.5.0`（**啟用**），
同檔 `:519`＝`-Directional Movement Keys Traditional Chinese 1.5.0 Machine Private 2026-08-21`（**已停用**），
`:521`＝`+Directional Movement Keys 1.5.0 Dev 2026-08-21` 本體啟用。
原文「現役 `Machine-Private.7z` 仍是未校對機翻包」**已不成立**。
建置腳本在 `/home/lorkhan/repo/moddings/skyrim/mod-library/l10n/tools/build_dmk_cht_layer.py`（docstring 明寫 human-reviewed DMK 1.5.0 CHT layer）。
**實機抽查（一般設定／相機／按鍵／OAR 警告／移動 smoke）仍未跑**，那一條列在
[`整包 UI／中文／任務驗收`](integrated-runtime.md) 的「DMK 中文層 smoke」項，不在本檔重複計。

用 exact official／CHS archives、7z、OpenCC 執行
`mod-library/l10n/tools/` 的 DMK 繁中層建置腳本，確認 gate 為
`human_reviewed_zh_tw`、66 reviewed、38 override、0 unresolved；部署單檔
`Data/Viny Mods/DMK/Language.json` layer。抽查一般設定、相機、PC／手把按鍵、OAR converter 警告
並做移動 smoke。現役 `Machine-Private.7z` 仍是未校對機翻包；證據見
[`安裝結果`](../agentctl/logs/mcm-helper-dmk-cht-install-2026-08-21.md)。
