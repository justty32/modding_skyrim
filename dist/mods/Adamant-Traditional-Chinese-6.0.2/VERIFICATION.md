# Verification

2026-08-16 靜態驗證：PASS。`tools/verify_translation.py` 已確認：

- 來源 ESP SHA-256、masters、record 數量符合 `tools/contract.json`。
- 2,012 筆記錄（含 TES4）及全部 GRUP／record／subrecord 拓撲一致。
- 除 TES4 localized flag 與 3,240 個文字欄位的 string ID 外，所有 header 語意與非文字 payload 完全一致。
- 1,700 筆 `STRINGS`、1,540 筆 `DLSTRINGS` 完整覆蓋；不產生空的 `ILSTRINGS`。
- English／Chinese 字串表逐 byte 相同、UTF-8 有效、數字與 `<mag>`／`<dur>` token 保留、無 replacement marker 或常見簡體字形。
- 最終 ESP 與字串檔可由版本鎖定來源及 TSV 逐 byte 重建；`MANIFEST.sha256` 完整涵蓋成品。
- houseCARL raw-file parser 可讀取最終外掛，辨識 2,011 筆 gameplay records、29 種 record type 與完整 master list。

尚需實機肉眼確認：18 棵技能樹、Active Effects、訊息與新增吟遊詩人內容顯示繁中；天賦取得、攻擊／格擋／施法與分發行為不變。
