# Verification — Glad You're Here Traditional Chinese 3.6.0.0

- 驗證日期：2026-08-15
- 結果：PASS
- 遊戲／MO2 啟動：未執行
- 部署、啟用、profile 變更：未執行

## 執行結果

```text
python tools/build_translation.py
python tools/verify_translation.py --source "/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/Glad You're Here - Main File/interface/translations/ImGladYoureHere_english.txt"
sha256sum -c MANIFEST.sha256
```

驗證器確認上游 SHA-256、213 個 key 與順序、每列一個 Tab、`%` 與字面 `\\n` token；並確認產物使用 UTF-16 LE BOM 與 CRLF。`MANIFEST.sha256` 覆蓋所有交付檔（不含 manifest 自身）。

## 範圍檢查

本次只讀取現役來源的 `meta.ini` 與英文翻譯檔以決定版本與鍵契約。未改動來源模組、MO2、任何 profile 或遊戲資料，亦未開啟遊戲 GUI。
