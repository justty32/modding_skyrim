# 回家下載／重建

## LoreRim 借用下載：465 件隊列，回家第一步是解析 Nexus id

隊列 `modpack-design/content-plan/lorerim/data/download-queue.csv`（465 列，四個待回填欄全空、`status=TO-RESOLVE`），
流程 `modpack-design/content-plan/lorerim/download-runbook.md`：houseCARL 逐列解析 id／版本／file id／bytes（每線 ≤60 列、每波 ≤20 GB）→
對 mod-library 去重 → 一波一條瀏覽器線 slow download → 入庫五步；**不安裝**。第 1–4 波（419 件）不等 AE；第 5 波 CC 34 件等上一節前置。
**通過**＝每波 `status` 全為 `RESOLVED`／`IN-LIBRARY`／`ASK`／`DROP-4K` 之一，下載件 hash 已驗、DB 已 rescan。

## 購買 AE 升級，且不得讓 Steam 把 exe 升到 1.7.99

**裁示：買。**（2026-09-02 使用者當場口頭，LoreRim 調查衝突帳第 2 件。）但同場裁示 ① 維持 1.6.1170 釘版。
購買本身不動 exe；**下載 Creation Club 內容要 Steam 上線並進遊戲主選單，上線即會觸發更新到 1.7.99**
（`AutoUpdateBehavior` 風險見 2026-09-01 裁示 8A）。回家順序：先備份現役 exe／`Data` 的 CC 相關檔與 depot manifest，
確認有降版手段（depot 回滾或 downgrader；**使用者記得有，回家先找出來驗證可用**），再上線購買與下載 CC，下載完立刻回離線並核對 exe 仍為 1.6.1170。
**通過**＝CC 內容全部到位、exe 版本不變、現役 profile 可開到主選單。之後 LoreRim 的 Creation Club 段
（`quests-and-lands.json` 的 25 件 CC 與其 patch）才能進借用盤點。

## Serana Dialogue Add-On 4.3.2 exact 簡中 topology gate

**裁示：A —— SDA 升 4.3.2 並採 exact 簡中層。**（2026-09-01，使用者當場口頭裁示；見
[裁示簡報](decision-briefs-2026-09-01.md)第 1 條。）回家取得 SDA 4.3.2 official archive 與 `78511`
簡中 `4.3.2v1.2` exact archive，做 binary topology gate；核對 plugin／master、record 與 script／asset
覆寫面，不能讓舊版繁中層回滾 4.3.2 修正。**通過**＝版本與 master 對版、中文層只改預期文字面、
沒有舊版 record／script／asset 回滾；證據落檔後才可進部署。

## Mihail 自然核心首批 4–6 件 preflight

**裁示：A —— 自然核心小批、原生 hand-placed、接受 exact CHS。**（2026-09-01，使用者當場口頭裁示；
見[裁示簡報](decision-briefs-2026-09-01.md)第 3 條。）回家取得選中 4–6 件的 base／中文 archives，
逐件掃 CELL／worldspace placement、asset 與 record，並對新增 ingredient／food、actor stats／ability／
combat style 做 Apothecary 與現役 EnaiRim 語意 preflight；不得偷換成全域 SkyPatcher 分布。
**通過**＝每件都有可回滾單位、exact 中文對版與明列的 winner／patch 結論，CELL／asset／record 衝突及
Apothecary／Enai 接觸面全數有處置，才能排入施工。

## scene-capture-bridge 完整離線測試

`scene-capture-bridge` 的 portable MinGW CTest 2/2 PASS，但完整 `x64-mingw-static` nlohmann-json
triplet 仍缺，需要能跑 vcpkg build 的環境補上；不得改測試掩蓋缺依賴。

另外兩個已於 2026-08-25 在家補完，見
[`handoffs/done/README.md`](../agentctl/handoffs/done/README.md)：`darksouls-port` 35/35、
`ModForge` 1190/1190，兩者都沒有測試碼變更。

## DMK 1.5.0 人工校對版

用 exact official／CHS archives、7z、OpenCC 執行
`mod-library/l10n/tools/` 的 DMK 繁中層建置腳本，確認 gate 為
`human_reviewed_zh_tw`、66 reviewed、38 override、0 unresolved；部署單檔
`Data/Viny Mods/DMK/Language.json` layer。抽查一般設定、相機、PC／手把按鍵、OAR converter 警告
並做移動 smoke。現役 `Machine-Private.7z` 仍是未校對機翻包；證據見
[`安裝結果`](../agentctl/logs/mcm-helper-dmk-cht-install-2026-08-21.md)。

## 現役 modlist 整合度盤點的三個待辦

盤點結論見 [`modpack-design/content-plan/modlist-coverage-2026-09-01.md`](../modpack-design/content-plan/modlist-coverage-2026-09-01.md)
（2026-09-01 公司端離線產出，未經 xEdit 與實機驗證）。回家要決／要查的三件：

1. **敵人／AI／怪物多樣性要不要補**，以及是否在開新檔前補。現役只有 AI Overhaul 一個家族，
   查無怪物池類 mod；敵人池晚加會影響已生成 encounter。**尚未裁示。**
2. **需求／生存要不要開**（飢渴／體溫／紮營）。文件面是「尚未決」而非「決定不做」
   （`modpack-design/content-plan/gameplay/OPEN.md:9`）。**尚未裁示。**
3. **查 mo2ctl 為何沒追上 profile 變動**。`instance/profiles/manifest.json` 的 `updated_at` 停在
   2026-08-30T09:52，`modlist.txt`／`plugins.txt` 已到 2026-09-01 13:15，兩者數字對不起來。

另：`major-content-preflight-2026-09-01/` 的 9 件裡有 6 件其實早已安裝啟用，該批任務單與批次計畫
的框架語意需要對現況重新校正（更正段已加在 `home-batching-plan.md` 開頭）。
