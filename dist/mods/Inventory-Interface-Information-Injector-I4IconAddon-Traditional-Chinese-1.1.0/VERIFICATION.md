# Verification — Inventory Interface Information Injector I4 Icon Addon Traditional Chinese 1.1.0

- 驗證日期：2026-08-15
- 結果：PASS
- 遊戲／MO2 啟動：未執行
- 實機部署：未執行

## 來源與範圍檢查

- 上游 `I4IconAddon_ENGLISH.txt`：UTF-16 LE with BOM、CRLF、17 筆、最後一筆無換行。
- 上游 SHA-256：`55154e3fd85ad1fc71624dad7fe3c48cffa0c4fc10afb582e49010e13b4ad376`。
- key 名稱與順序全部保留；本包只增加一個同精確路徑／檔名的 text-only override。
- 本機 CHS 1.0.1 archive 的同路徑檔案含相同 17 個 key，僅用作用語種子；未複製該 archive 的資產。

## 產物檢查

執行：

```bash
python tools/build_translation.py
python tools/verify_translation.py --source "/path/to/I4IconAddon_ENGLISH.txt"
sha256sum -c MANIFEST.sha256
```

結果應確認：UTF-16 LE BOM、CRLF、無最後換行、17 筆精確資料列、上游 hash、key/order parity 與 manifest。

## Repo 回歸檢查

執行 `python -m unittest discover -s tests -v`、`python scripts/check_markdown_links.py` 與 `git diff --check`。這些檢查僅證明產物格式與 repo 連結／測試狀態，並不宣稱已通過遊戲內顯示驗收。
