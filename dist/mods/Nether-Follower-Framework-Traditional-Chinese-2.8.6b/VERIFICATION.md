# Verification — Nether's Follower Framework Traditional Chinese 2.8.6b

- 驗證日期：2026-08-16
- 結果：PASS
- 遊戲／MO2 啟動：未執行
- 部署、啟用、profile 變更：未執行

## 驗證範圍

```text
python tools/build_translation.py
python tools/verify_translation.py --source "/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/Nether's Follower Framework/Interface/Translations/nwsFollowerFramework_english.txt"
sha256sum -c MANIFEST.sha256
```

驗證器鎖定 NFF 2.8.6b 英文來源 SHA-256，確認 1,398 個 key 的集合與順序，以及每列的數字、
百分比與控制碼完全對齊；唯一結構修正是補回上游 `$FF_LootSpeedDS` 遺失的 Tab。產物另通過
UTF-16 LE BOM、逐列 CRLF、review TSV byte-for-byte 重建與完整 manifest 檢查。

本次未宣稱 ESP 對話或 PEX 內嵌文字已翻譯，也未做 runtime 字型、MCM 排版或截斷驗收。
