# 回家下載／重建

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

## Bandolier NPC 中文 forward patch

**裁示：B —— 保留 NPC 分發並做小型中文 forward patch。**（2026-09-01，使用者當場口頭裁示；見
[裁示簡報](decision-briefs-2026-09-01.md)第 4 條。）回家以實際 archives／plugins 建 patch，把 CHS `FULL`
forward 到 NPC 層後的 winners；依既定 realistic variant 覆蓋 83 unique＋23 變體兩批。
**通過**＝106 個目標字串全由 patch 贏得、93 個 NPC 層 ARMO 不再顯示英文，且 NPC 分發與
less-common／realistic variant 都保留；保存 record 對帳與 plugin gate 證據。

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
