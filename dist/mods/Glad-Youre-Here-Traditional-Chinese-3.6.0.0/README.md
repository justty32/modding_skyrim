# Glad You're Here 3.6.0.0 繁體中文 text-only override

這是 Glad You're Here 的繁體中文文字覆寫包，包含 MCM 翻譯表與由精確 3.6.0 ESP 建立的
gameplay 對話覆寫：

```text
interface/translations/ImGladYoureHere_english.txt
ImGladYoureHere.esp
```

`english` 檔名（包含上游的小寫拼法）是刻意精確保留的。ESP 由現役 3.6.0 原檔作唯一基底，
只把舊版 3.2.3 簡中種子能以 record FormID＋localizable tag occurrence 穩定對齊的 828 個欄位
轉成台灣正體；所有 record 身份、順序、header、GRUP path、subrecord topology 與非文字 payload
不變。本包不含 MCM JSON、腳本、動畫、模型、材質或語音。

## 目標版本與範圍

- 目標：Glad You're Here `3.6.0.0`（Nexus mod ID `41856`）。
- 來源版本唯一依據：現役 `Modpack-KR-Dev` 的 `Glad You're Here - Main File/meta.ini` 與 `interface/translations/ImGladYoureHere_english.txt`。
- 完整翻譯 213 筆 MCM 介面鍵；所有 key、順序、`%` 與字面 `\\n` token 都由驗證器鎖定。
- gameplay ESP 翻譯 828 個穩定對齊欄位；使用者回報的 `I'm glad you're here.` 已人工校訂為
  `很高興你在這裡。`。
- 3.6.0 新增且舊種子無法安全對齊的文字刻意保留原文，不冒充完整新版翻譯。
- 遊戲檔採 UTF-16 LE BOM 與 CRLF；檔名精確保留上游的 `_english`。

## 建置與驗證

在本資料夾執行：

```bash
python tools/build_translation.py
python tools/verify_translation.py --source "/path/to/ImGladYoureHere_english.txt"
sha256sum -c MANIFEST.sha256
```

可審閱且可修改的翻譯真相來源是 `tools/translation-source.tsv`（UTF-8、每列一個 `key<TAB>譯文`）。來源、再散布邊界與實際驗證結果分別見 [SOURCE.md](SOURCE.md) 與 [VERIFICATION.md](VERIFICATION.md)。

本產物未安裝、啟用、部署到 MO2 profile，也未啟動遊戲；部署狀態不在此記錄。
