# VIGILANT SE 1.8.1 MCM 繁體中文 text-only override

這是 [VIGILANT SE](https://www.nexusmods.com/skyrimspecialedition/mods/11849) 1.8.1 的 MCM 介面文字覆寫。它只提供十二筆繁體中文介面字串，不含 VIGILANT 本體或完整劇情漢化。

## 安裝內容

```text
interface/Translations/VIGILANT_ENGLISH.txt
```

目標路徑、`interface` 的小寫、`Translations` 的大寫與檔名 `VIGILANT_ENGLISH.txt` 均精確沿用現役 VIGILANT SE 1.8.1。`ENGLISH` 是刻意保留：這個 profile 以英文語言載入介面翻譯；改名為 CHINESE 不會取代原 MCM 文本。

## 範圍與相容性

- 目標版本：VIGILANT SE 1.8.1。
- 只覆寫 12 個 MCM `$key`；Vigilant.esm 的任務、對話、書籍、物件名稱，以及 Papyrus 的其他文字不在範圍內。
- 不包含 ESM/ESP、BSA、PEX、SKSE DLL、模型、材質、音效或語音。
- 安裝時將本包置於 `VIGILANT SE` 之後，使同一路徑的文字檔覆寫原檔；未執行 MO2 安裝、啟用、排序或遊戲內測試。

## 可重建與驗證

```bash
python tools/build_translation.py
python tools/verify_translation.py --source "/path/to/VIGILANT SE/interface/Translations/VIGILANT_ENGLISH.txt"
sha256sum -c MANIFEST.sha256
```

來源、衍生邊界見 [SOURCE.md](SOURCE.md)，實際靜態驗證見 [VERIFICATION.md](VERIFICATION.md)。
