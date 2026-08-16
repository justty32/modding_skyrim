# Verification — Crafting Categories for SkyUI Traditional Chinese 1.1.1

- 驗證日期：2026-08-15
- 遊戲／MO2 啟動：未執行
- 實機部署：未執行

## 靜態驗證

`tools/verify_translation.py --source` 會要求上游 1.1.1 檔案精確符合 SHA-256 `ed93daca5f50c8b02fcf78a801842ce4bad1527340495a34900a4f52c5eeb5c5`，再驗證其 17 個 key 與順序。產物驗證會確認 UTF-16 LE BOM、CRLF（包含最終 CRLF）、每列恰有一個 Tab、與 TSV 完全一致，並檢查 manifest。

本產物不會改動 MO2、遊戲、Chrome、profile 或任何部署端檔案。
