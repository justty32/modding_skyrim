# Thaumaturgy 1.5 正體中文

這是 `Thaumaturgy - An Enchanting Overhaul` 1.5 的版本鎖定正體中文覆寫層。它只提供
localized `Thaumaturgy.esp` 與英文／中文語系別名 STRINGS；官方 BSA、腳本與
`Thaumaturgy_DISTR.ini` 仍由原模組供應。

可審閱譯文位於 `tools/translation-source.tsv`。重建與驗證：

```bash
python tools/build_translation.py --source /absolute/path/to/Thaumaturgy.esp
python tools/verify_translation.py --source /absolute/path/to/Thaumaturgy.esp
```
