# 回家下載／重建

## YouTube 候選 SOURCE-HOLD（可選）

35 支候選影片已完成 owner routing；未重查 current metadata／archive 的項目保持 HOLD。只有要升級
某一件時，回到有 Nexus API key／houseCARL／archives 的環境，依
[`coverage` reopen procedure](../modpack-design/content-plan/youtube-candidate-final-coverage-audit-2026-08-25.md)
一次查一件；不得直接改成 GO。

## 三個 subproject 完整離線測試

- `scene-capture-bridge`：portable MinGW CTest 2/2 PASS；完整 `x64-mingw-static` nlohmann-json
  triplet 仍缺。
- `darksouls-port`：29/35；6 項因必要的 `scipy`／`shapely` 未安裝而 ERROR。
- `ModForge`：公司 Windows 無 `dotnet`；WSL 無 `bash` 且 repo 未掛載，1123 offline suite 未重跑。

回到可補依賴的環境後依各 repo README 重跑；不得改測試掩蓋缺依賴。

## DMK 1.5.0 人工校對版

用 exact official／CHS archives、7z、OpenCC 執行
[`build_dmk_cht_layer.py`](../mod-library/l10n/tools/build_dmk_cht_layer.py)，確認 gate 為
`human_reviewed_zh_tw`、66 reviewed、38 override、0 unresolved；部署單檔
`Data/Viny Mods/DMK/Language.json` layer。抽查一般設定、相機、PC／手把按鍵、OAR converter 警告
並做移動 smoke。現役 `Machine-Private.7z` 仍是未校對機翻包；證據見
[`安裝結果`](../agentctl/logs/mcm-helper-dmk-cht-install-2026-08-21.md)。
