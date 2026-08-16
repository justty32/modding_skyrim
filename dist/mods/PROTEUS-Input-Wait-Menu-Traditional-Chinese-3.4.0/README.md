# PROTEUS 3.4.0 Input Wait Menu 繁體中文 text-only override

這是現役 [PROTEUS](https://www.nexusmods.com/skyrimspecialedition/mods/62934) `3.4.0` 之 Input Wait Menu 繁體中文介面覆寫。它只包含一個翻譯檔；不包含 ESP、PEX、DLL、SWF 或任何其他原模組資產。

## 安裝內容

遊戲會讀取的唯一檔案是：

```text
Interface/translations/Input Wait Menu_english.txt
```

同名 `english` 與路徑大小寫均刻意保留，讓使用 `sLanguage=ENGLISH` 的 Skyrim 載入。此包應在原 PROTEUS 後安裝／覆寫同一路徑檔案。本產物尚未部署到 MO2，亦未進行遊戲內測試。

## 相容性範圍

- 只適用於 PROTEUS `3.4.0` 的上述英文來源檔。
- 保留 80 個 key、其順序、`{}` placeholder 與數值 token。
- 遊戲檔為 UTF-16LE with BOM、CRLF、沒有最後換行，逐列恰有一個 Tab，與現役來源相同。
- 更新 PROTEUS 後，必須重新執行來源驗證；不要把本包當作整套 PROTEUS 漢化。

## 可重建與驗證

在本資料夾執行：

```bash
python tools/build_translation.py
python tools/verify_translation.py --source "/path/to/PROTEUS/Interface/translations/Input Wait Menu_english.txt"
sha256sum -c MANIFEST.sha256
```

可人工審閱的繁中譯文在 `tools/translation-source.tsv`（UTF-8）。版本、來源雜湊、授權邊界見 [SOURCE.md](SOURCE.md)；檢查結果見 [VERIFICATION.md](VERIFICATION.md)。
