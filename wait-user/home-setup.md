# 回家下載／重建

## YouTube 候選 SOURCE-HOLD（可選）

35 支候選影片已完成 owner routing；未重查 current metadata／archive 的項目保持 HOLD。只有要升級
某一件時，回到有 Nexus API key／houseCARL／archives 的環境，依
[`coverage` reopen procedure](../modpack-design/content-plan/youtube-candidate-final-coverage-audit-2026-08-25.md)
一次查一件；不得直接改成 GO。

## scene-capture-bridge 完整離線測試

`scene-capture-bridge` 的 portable MinGW CTest 2/2 PASS，但完整 `x64-mingw-static` nlohmann-json
triplet 仍缺，需要能跑 vcpkg build 的環境補上；不得改測試掩蓋缺依賴。

另外兩個已於 2026-08-25 在家補完，見
[`handoffs/done/README.md`](../agentctl/handoffs/done/README.md)：`darksouls-port` 35/35、
`ModForge` 1190/1190，兩者都沒有測試碼變更。

## DMK 1.5.0 人工校對版

用 exact official／CHS archives、7z、OpenCC 執行
[`build_dmk_cht_layer.py`](../mod-library/l10n/tools/build_dmk_cht_layer.py)，確認 gate 為
`human_reviewed_zh_tw`、66 reviewed、38 override、0 unresolved；部署單檔
`Data/Viny Mods/DMK/Language.json` layer。抽查一般設定、相機、PC／手把按鍵、OAR converter 警告
並做移動 smoke。現役 `Machine-Private.7z` 仍是未校對機翻包；證據見
[`安裝結果`](../agentctl/logs/mcm-helper-dmk-cht-install-2026-08-21.md)。
