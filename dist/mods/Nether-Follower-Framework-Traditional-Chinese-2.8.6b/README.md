# Nether's Follower Framework 2.8.6b 繁體中文文字覆寫

這是 NFF 2.8.6b 的繁體中文翻譯表，共 1,398 個介面、MCM、通知與腳本翻譯鍵。遊戲載入檔只有：

```text
Interface/Translations/nwsFollowerFramework_english.txt
```

`english` 檔名刻意保留，供目前使用 `sLanguage=ENGLISH` 的設定載入。本包不含 ESP、PEX、SWF、
模型、材質或其他 gameplay 資產，也不會覆寫 NFF 的執行邏輯。

## 版本與修正範圍

- 目標版本：Nether's Follower Framework `2.8.6b`（Nexus mod ID `55653`）。
- 保留上游所有 key、順序、數字、百分比與 `\\n` 控制碼。
- 修正上游 `$FF_LootSpeedDS` 遺失 Tab、因而無法成為有效翻譯列的問題。
- 修正翻譯草稿中錯誤加入的 `350`、`100%` 語意錯譯，以及兩個遺失的換行控制碼。

## 重建與驗證

```bash
python tools/build_translation.py
python tools/verify_translation.py --source "/path/to/NFF/Interface/Translations/nwsFollowerFramework_english.txt"
sha256sum -c MANIFEST.sha256
```

可審閱的翻譯真相來源是 UTF-8 的 `tools/translation-source.tsv`。遊戲檔固定使用 UTF-16 LE BOM
與 CRLF。來源與驗證證據分別見 [SOURCE.md](SOURCE.md) 與 [VERIFICATION.md](VERIFICATION.md)。
