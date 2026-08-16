# Crafting Categories for SkyUI 1.1.1 繁體中文 text-only override

這是給 Crafting Categories for SkyUI 1.1.1 的繁體中文介面文字覆寫包。遊戲資產只有：

```text
Interface/Translations/CraftingCategories_ENGLISH.txt
```

`ENGLISH` 的檔名、大小寫與路徑必須保留：現役 profile 使用英文語言檔案作為該模組的 lookup。這個包只覆寫原本的 17 個分類名稱，不含本體 DLL、JSON、ESP、SKSE 設定、MO2 profile 或其他遊戲資產。

## 可重建與驗證

可審閱的 UTF-8 譯文在 `tools/translation-source.tsv`。它完整保留上游 1.1.1 的 17 個 key、順序與每列一個 Tab；遊戲資產以 UTF-16 LE BOM、CRLF（包含最終 CRLF）建立。

```bash
python tools/build_translation.py
python tools/verify_translation.py
python tools/verify_translation.py --source "/path/to/Crafting Categories for SkyUI/Interface/Translations/CraftingCategories_ENGLISH.txt"
sha256sum -c MANIFEST.sha256
```

來源與授權範圍見 [SOURCE.md](SOURCE.md)，實際驗證紀錄見 [VERIFICATION.md](VERIFICATION.md)。

Done when: 此資料夾可由可審閱的 UTF-8 TSV 重建遊戲資產，且能驗證來源 hash、格式、key 順序與 manifest；不包含部署、啟用、排序或遊戲內測試。
