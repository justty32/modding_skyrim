# 驗證

- 官方與同版 CHS 均為 10 筆 records；拓撲、header、masters 與所有非文字 payload 相同。
- 9 個 `INGR.FULL` 轉入 `STRINGS`，localized 產物仍為 10 筆 records。
- masters 精確為 `Skyrim.esm`、`ccBGSSSE001-Fish.esm`、`Apothecary.esp`。
- English／Chinese 表 byte-identical；token、繁簡字形、semantic delta 與重建可重現檢查通過。
- 產物 ESP SHA-256：`2c31e7984b238bec68373a9b8834012c0726c9b7b44d438914f0b4b734a8e47f`。

