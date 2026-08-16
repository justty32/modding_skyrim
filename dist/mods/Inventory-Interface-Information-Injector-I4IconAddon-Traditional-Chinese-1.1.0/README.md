# Inventory Interface Information Injector — I4 Icon Addon 1.1.0 繁體中文 text-only override

這是一份供 Skyrim Special Edition 模組 [Inventory Interface Information Injector](https://www.nexusmods.com/skyrimspecialedition/mods/85702) 的 I4 Icon Addon 1.1.0 使用的繁體中文介面文字覆寫。它只翻譯圖示類別名稱，不含原模組本體。

## 安裝內容

遊戲會讀取的檔案只有：

```text
Interface/Translations/I4IconAddon_ENGLISH.txt
```

檔名中的 `ENGLISH` 是刻意保留的。現役 Skyrim profile 使用 `sLanguage=ENGLISH`，而該模組正是以這個檔名查找 17 個 I4 Icon Addon key；改成 `_CHINESE.txt` 不會覆寫現役的英文載入槽。

## 相容性與範圍

- 目標版本：Inventory Interface Information Injector 1.1.0（I4 Icon Addon）。
- 只含一個 UTF-16LE 介面文字檔；不含 ESP、DLL、JSON、SWF、Papyrus、模型、材質、語音或原模組英文資產。
- `tools/translation-source.tsv` 是可審閱的 UTF-8 繁中來源；它借鑑本機 CHS 1.0.1 相同 key 的用語作種子，但所有用字已自行轉為繁體並校正（例如「馬具」與「耐奇皮革」）。
- 此產物沒有執行 MO2 安裝、啟用、排序或遊戲內測試；部署狀態仍由 `~/notes/projects/modding/skyrim/` 管理。

## 驗證與重建

在本資料夾執行：

```bash
python tools/build_translation.py
python tools/verify_translation.py --source "/path/to/I4IconAddon_ENGLISH.txt"
sha256sum -c MANIFEST.sha256
```

來源、授權邊界與建置資訊見 [SOURCE.md](SOURCE.md)，本次實際驗證結果見 [VERIFICATION.md](VERIFICATION.md)。
