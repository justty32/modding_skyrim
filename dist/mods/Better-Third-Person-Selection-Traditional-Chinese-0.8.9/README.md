# Better Third Person Selection 0.8.9 繁體中文 text-only override

這是 [Better Third Person Selection](https://www.nexusmods.com/skyrimspecialedition/mods/64339) 0.8.9 的繁體中文介面文字覆寫。它只包含 MCM／介面翻譯，不含原模組的 ESP、DLL、SWF、腳本或其他資產。

## 安裝內容

遊戲會讀取的唯一檔案是：

```text
Interface/Translations/BetterThirdPersonSelection_ENGLISH.txt
```

`ENGLISH` 檔名刻意保留，供 `sLanguage=ENGLISH` 的 Skyrim 設定載入。此包是 text-only override，應在原模組之後安裝／覆寫其同路徑翻譯檔；本次沒有進行 MO2 安裝、啟用、排序或遊戲內測試。

## 範圍與相容性

- 目標版本：Better Third Person Selection `0.8.9`。
- 保留現役 0.8.9 英文檔的全部 146 個 key、其順序與 placeholder／數值／運算子 token。
- 遊戲檔為 UTF-16LE with BOM、CRLF，且沒有最後換行；所有資料列各有一個 Tab。
- 不支援其他版本的 key 集合；更新原模組後須重新執行來源比對。

## 可重建與驗證

在本資料夾執行：

```bash
python tools/build_translation.py
python tools/verify_translation.py --source "/path/to/Better Third Person Selection 0.8.9/Interface/Translations/BetterThirdPersonSelection_english.txt"
sha256sum -c MANIFEST.sha256
```

可人工審閱的繁中譯文位於 `tools/translation-source.tsv`（UTF-8）。來源、授權邊界與版本證據見 [SOURCE.md](SOURCE.md)；本次檢查結果見 [VERIFICATION.md](VERIFICATION.md)。
