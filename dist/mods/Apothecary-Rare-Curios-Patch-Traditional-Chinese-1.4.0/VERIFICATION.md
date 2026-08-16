# 驗證

- 官方與同版 CHS 均為 58 筆 records；record path、FormID、header、subrecord 拓撲與非文字
  payload 完全一致。
- localized 產物仍為 58 筆 records，masters 精確維持官方 7 個 masters。
- 60 個欄位完整建入字串表：56 筆 `STRINGS`、4 筆 `DLSTRINGS`；English／Chinese byte-identical。
- placeholder／數字 token、繁簡字形、canonical semantic delta 與重建可重現檢查通過。
- 產物 ESP SHA-256：`a695f445d1574257ca0d471e7140b30ada07c3cd52f4e6b09ef7d3636a280989`。

