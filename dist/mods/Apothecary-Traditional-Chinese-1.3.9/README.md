# Apothecary 1.3.9 正體中文

這是 `Apothecary - An Alchemy Overhaul` 1.3.9 主檔的版本鎖定正體中文覆寫層。它只提供
localized `Apothecary.esp` 與英文／中文語系別名 STRINGS，不包含原模組的 BSA、腳本、模型或
`Apothecary_DISTR.ini`；使用時仍須安裝官方 1.3.9 MAIN。

本產物把 674 筆 record 中的 615 個玩家可見／localizable 欄位轉到 UTF-8 字串表：526 筆
`STRINGS`、89 筆 `DLSTRINGS`。官方 ESP 的 masters、FormID、EditorID、record／subrecord 拓撲、
條件、效果、數值與 scripts 均不變。

可審閱譯文在 [`tools/translation-source.tsv`](tools/translation-source.tsv)。來源與授權邊界見
[`SOURCE.md`](SOURCE.md)，驗證結果見 [`VERIFICATION.md`](VERIFICATION.md)。

重建與驗證：

```bash
python tools/build_translation.py --source /absolute/path/to/Apothecary.esp
python tools/verify_translation.py --source /absolute/path/to/Apothecary.esp
```

