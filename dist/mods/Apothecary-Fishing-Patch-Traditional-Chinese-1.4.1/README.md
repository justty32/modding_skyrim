# Apothecary Fishing Patch 1.4.1 正體中文

這是 Apothecary 官方 Fishing Patch 1.4.1 的版本鎖定正體中文覆寫層。它只提供 localized
`Apothecary - Fishing Patch.esp` 與 English／Chinese `STRINGS`，仍須另裝 Apothecary 1.3.9、
Fishing Creation 及官方 patch。

10 筆 records 中的 9 個 ingredient 名稱已轉到 UTF-8 字串表。可審閱來源、版本證據與驗證分別
位於 [`tools/translation-source.tsv`](tools/translation-source.tsv)、[`SOURCE.md`](SOURCE.md) 與
[`VERIFICATION.md`](VERIFICATION.md)。

```bash
python tools/build_translation.py --source '/absolute/path/to/Apothecary - Fishing Patch.esp'
python tools/verify_translation.py --source '/absolute/path/to/Apothecary - Fishing Patch.esp'
```

