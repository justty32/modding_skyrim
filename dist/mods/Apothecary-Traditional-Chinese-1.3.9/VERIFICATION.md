# 驗證

- 官方 1.3.9 ESP 與同版 CHS 種子均為 674 筆 records；record path、FormID、header、subrecord
  順序及所有非文字 payload 完全一致。
- localized 產物仍為 674 筆 records，masters 精確維持
  `Skyrim.esm`、`Update.esm`、`Dawnguard.esm`、`HearthFires.esm`、`Dragonborn.esm`。
- 615 個欄位完整建入字串表：526 筆 `STRINGS`、89 筆 `DLSTRINGS`；English／Chinese 語系檔
  byte-identical，能在本機 `sLanguage=ENGLISH` 下讀到繁中。
- placeholder／數字 token 零漂移；未檢出 replacement marker、`???` 或常見簡體殘字。僅 5 個
  不在玩家流程顯示的 controller 名稱刻意保留英文。
- canonical semantic diff 證明除 TES4 localized flag、文字 ID、必要的 record／group size 外，
  所有資料與官方來源相同。
- 重建可重現；產物 ESP SHA-256：
  `6703209453d25bd4af1b8db80d90ced8baa8878bd1775c3bacc10957113d5d00`。

遊戲內 UI、SPID distribution 與實際藥劑抽樣屬部署批次驗證，不由本文件的靜態產物 gate 取代。

