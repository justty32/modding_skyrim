# Verification — Better Third Person Selection Traditional Chinese 0.8.9

- 驗證日期：2026-08-15
- 結果：PASS
- 遊戲／MO2 啟動：未執行
- 實機部署：未執行

## 已執行檢查

```bash
python tools/build_translation.py
python tools/verify_translation.py --source "/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/Better Third Person Selection 0.8.9/Interface/Translations/BetterThirdPersonSelection_english.txt"
sha256sum -c MANIFEST.sha256
```

驗證確認：

- 現役英文來源的 SHA-256 完全等於 `00488ab50628c75740c61fb4345a64f66ae99957df9298009e2e3beb11bc365d`。
- 146 個 key 與其順序完全相同；所有方括號 placeholder、數值與 `*` 運算子 token 均未改動。
- 可審閱 TSV 與遊戲資產資料列逐一相同。
- 遊戲資產是 UTF-16LE BOM、只使用 CRLF、無最後換行，且每筆恰有一個 Tab。
- `MANIFEST.sha256` 覆蓋資產、說明、來源、驗證紀錄與兩個工具及 TSV。

這些是檔案層級驗證，不代表已在遊戲中驗收。部署及實機狀態不在本產物區記錄。
