# Verification — BFCO Traditional Chinese 3.100.5

- 驗證日期：2026-08-15
- 結果：PASS
- MO2／Skyrim 啟動：未執行
- 實機部署、安裝、啟用與排序：未執行

## 已驗證項目

使用下列命令：

```bash
python tools/build_translation.py
python tools/verify_translation.py --source "/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/BFCO - Attack Behavior Framework 3.100.5/Interface/Translations/SCSI-ACTbfco-Main_english.txt"
sha256sum -c MANIFEST.sha256
```

驗證器確認：

- 審閱譯稿有 37 個不重複 key，且其順序為 BFCO 3.100.5 所定。
- 產物是 UTF-16 LE with BOM、只用 CRLF、有 52 個邏輯行，並與審閱譯稿逐字一致（僅換行編碼不同）。
- 提供的基準檔 SHA-256 必須是 `58f76ec42ea6d36f1a6a59e1e040fe0bd54bfc640e9a45c7ebb57fc9f9a18abb`；並比對 key／順序、空白行配置與所有非 CJK token。
- `MANIFEST.sha256` 覆蓋本包的遊戲資產、文件與工具，重建後可驗證檔案完整性。

上述只驗證資料檔結構與基準相容性，不宣稱已完成遊戲內顯示驗收，也沒有改動 MO2 instance、profile 或 load order。
