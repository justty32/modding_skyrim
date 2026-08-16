# Verification — VIGILANT SE 1.8.1 MCM Traditional Chinese

- 驗證日期：2026-08-15
- 遊戲／MO2 啟動：未執行
- 部署、啟用、排序：未執行

靜態檢查確認現役來源為 UTF-16 LE BOM、CRLF、12 筆且最後無換行；上游 SHA-256 為 `148a04073297213ec84de8e55491b02559649ea7be63cde16616bf0ab1bd1d6f`。本產物保留完全相同的 key、順序與檔案路徑，並在驗證工具中檢查 source hash、UTF-16LE BOM、CRLF、無終端換行與 manifest。

已執行：

```text
python tools/verify_translation.py --source "/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/VIGILANT SE/interface/Translations/VIGILANT_ENGLISH.txt"
sha256sum -c MANIFEST.sha256
python -m unittest discover -s tests -v
python scripts/check_markdown_links.py
git diff --check
```

結果：

```text
PASS reviewable source: UTF-8, 12 unique keys, exact order
PASS game asset: UTF-16 LE BOM, CRLF, no final newline, 12 exact rows, sha256=ab1645d29669602e20499f3e70e26e727fd7141e5d89ae4d88ca2935f279b4cd
PASS upstream parity: exact source hash and key/order match
PASS manifest: 7 files match
RESULT: PASS

python -m unittest discover -s tests -v: Ran 6 tests — OK
python scripts/check_markdown_links.py: Markdown links OK: 429 file(s), 580 local link(s)
git diff --check: PASS
```
