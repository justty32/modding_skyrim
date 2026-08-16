# Apothecary Rare Curios Patch 1.4.0 正體中文

這是 Apothecary 官方 Rare Curios Patch 1.4.0 的版本鎖定正體中文覆寫層。它只提供 localized
`Apothecary - Rare Curios Patch.esp` 與 English／Chinese 字串表；仍須另裝 Apothecary 1.3.9、
Rare Curios Creation 及官方 patch。

58 筆 records 中的 60 個 localizable 欄位已轉到 UTF-8 字串表：56 筆 `STRINGS`、4 筆
`DLSTRINGS`。可審閱來源、版本證據與驗證分別見
[`tools/translation-source.tsv`](tools/translation-source.tsv)、[`SOURCE.md`](SOURCE.md) 與
[`VERIFICATION.md`](VERIFICATION.md)。

```bash
python tools/build_translation.py --source '/absolute/path/to/Apothecary - Rare Curios Patch.esp'
python tools/verify_translation.py --source '/absolute/path/to/Apothecary - Rare Curios Patch.esp'
```

