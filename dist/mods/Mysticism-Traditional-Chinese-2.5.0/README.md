# Mysticism Traditional Chinese 2.5.0

Mysticism 2.5.0 的版本鎖定繁體中文覆蓋層。

## 安裝契約

- 需要原版 `Mysticism - A Magic Overhaul` 2.5.0 MAIN 檔。
- MO2 左側讓本模組排在原版 Mysticism 後方；本包用同名 `MysticismMagic.esp` 與字串檔覆蓋文字，不包含 BSA、腳本或玩法資料的另一份拷貝。
- 外掛採 localized 格式，繁中文字串位於 UTF-8 `STRINGS`／`DLSTRINGS`。
- `_English` 與 `_Chinese` 檔逐 byte 相同；目前 `sLanguage=ENGLISH` 的 profile 會讀 `_English`。
- Adamant 同時使用時，`MysticismMagic.esp` 必須在 `Adamant.esp` 前載入。

本包涵蓋 3,871 個文字欄位：2,323 個一般名稱字串及 1,548 個說明／書籍／任務字串。FormID、EditorID、masters、效果資料、條件、數值、資產與腳本均不改動。

## 重建

```bash
python tools/build_translation.py --source '/path/to/official-2.5.0/MysticismMagic.esp'
python tools/verify_translation.py --source '/path/to/official-2.5.0/MysticismMagic.esp'
```
