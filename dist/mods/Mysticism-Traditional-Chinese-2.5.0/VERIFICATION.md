# Verification

2026-08-16 靜態驗證：PASS。`tools/verify_translation.py` 已確認：

- 來源 ESP SHA-256、masters、record 數量符合 `tools/contract.json`。
- 3,204 筆記錄（含 TES4）及全部 GRUP／record／subrecord 拓撲一致。
- 62 筆來源壓縮記錄可解壓、重建並以解壓後 payload 比對。
- 除 TES4 localized flag 與 3,871 個文字欄位的 string ID 外，所有 header 語意與非文字 payload 完全一致。
- 2,323 筆 `STRINGS`、1,548 筆 `DLSTRINGS` 完整覆蓋；不產生空的 `ILSTRINGS`。
- English／Chinese 字串表逐 byte 相同、UTF-8 有效、數字與 `<mag>`／`<dur>`／HTML／alias token 保留、無 replacement marker 或常見簡體字形。
- 最終 ESP 與字串檔可由版本鎖定來源及 TSV 逐 byte 重建；`MANIFEST.sha256` 完整涵蓋成品。
- houseCARL raw-file parser 可讀取最終外掛，辨識 3,203 筆 gameplay records、44 種 record type 與完整 master list。

尚需實機肉眼確認：法術書、物品名稱、法術說明與 Active Effects 顯示繁中；施法與數值行為不變。
