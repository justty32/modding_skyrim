# 驗證

- 官方與同版 CHS 均為 7 筆 records；record path、FormID、header、subrecord 拓撲與非文字
  payload 完全一致。
- localized 產物仍為 7 筆 records，masters 精確為
  `Skyrim.esm`、`ccbgssse025-advdsgs.esm`、`Apothecary.esp`。
- 7 個欄位完整建入字串表：6 筆 `STRINGS`、1 筆 `DLSTRINGS`；English／Chinese byte-identical。
- placeholder／數字 token、繁簡字形、canonical semantic delta 與重建可重現檢查通過。
- 產物 ESP SHA-256：`57923d237d5e1f69d97944d355d223fe623339dfa0d016e689d1ac43ea9f57e5`。

