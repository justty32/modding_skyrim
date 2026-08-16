# TrueHUD d2026.4.12.0 繁體中文 text-only override

這是現役 TrueHUD 的繁體中文介面文字覆寫；只含一個遊戲會載入的檔案：

```text
Interface/Translations/TrueHUD_english.txt
```

`english` 檔名刻意保留，與來源完全相同，供使用 `sLanguage=ENGLISH` 的設定載入。本包不含 TrueHUD 的 ESL、DLL、SWF、設定、腳本或其他資產。

## 版本與範圍

- 來源版本：Modpack-KR-Dev 現役 `TrueHUD/meta.ini` 的 `version=d2026.4.12.0`。
- 僅適用於其 `Interface/Translations/TrueHUD_english.txt`；來源 SHA-256 固定於驗證工具與 [SOURCE.md](SOURCE.md)。
- 未部署、未修改 MO2/profile，亦未啟動遊戲驗證。

## 重建與驗證

```bash
python tools/build_translation.py --source "/path/to/TrueHUD/Interface/Translations/TrueHUD_english.txt"
python tools/verify_translation.py --source "/path/to/TrueHUD/Interface/Translations/TrueHUD_english.txt"
sha256sum -c MANIFEST.sha256
```

翻譯規則是可審閱的 Python 標準函式庫來源 `tools/build_translation.py`。驗證會比較來源與產物的每個 key、順序、空白分段、XML/色碼 token、UTF-16LE BOM 與 CRLF。
