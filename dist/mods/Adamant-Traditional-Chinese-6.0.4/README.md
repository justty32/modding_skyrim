# Adamant Traditional Chinese 6.0.4

Adamant 6.0.4 的版本鎖定繁體中文覆蓋層。

## 安裝契約

- 需要原版 `Adamant - A Perk Overhaul` 6.0.4 MAIN 檔及其正式依賴。
- MO2 左側讓本模組排在原版 Adamant 後方；本包用同名 `Adamant.esp` 與字串檔覆蓋文字，不包含 BSA、SPID／KID 設定或 Scrambled Bugs 設定。
- 外掛採 localized 格式，繁中文字串位於 UTF-8 `STRINGS`／`DLSTRINGS`。
- `_English` 與 `_Chinese` 檔逐 byte 相同；目前 `sLanguage=ENGLISH` 的 profile 會讀 `_English`。
- `MysticismMagic.esp` 必須在 `Adamant.esp` 前載入。

本包涵蓋 3,234 個文字欄位：1,697 個一般名稱字串及 1,537 個說明字串。FormID、EditorID、masters、天賦效果、條件、數值、分發設定、資產與腳本均不改動。

## 重建

```bash
python tools/build_translation.py --source '/path/to/official-6.0.4/Adamant.esp'
python tools/update_manifest.py
python tools/verify_translation.py --source '/path/to/official-6.0.4/Adamant.esp'
```
