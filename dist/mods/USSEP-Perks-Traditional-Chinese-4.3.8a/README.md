# USSEP Perks Traditional Chinese 4.3.8a

USSEP 4.3.8a 技能天賦文字的繁體中文補丁。它翻譯 99 筆同時具有名稱與說明的 `PERK`，包含
原版十八系技能樹、吸血鬼／狼人技能與少量 DLC perk；不會整份覆蓋 USSEP，也不修改任何天賦效果。

## 安裝契約

需要 Unofficial Skyrim Special Edition Patch 4.3.8a，以及該版本宣告的原版／Creation Club masters。
啟用本模組，並讓 `USSEP Perks Traditional Chinese 4.3.8a.esp` 在 USSEP 後載入。

外掛採 localized 格式，繁中文字串存於 UTF-8 `STRINGS`／`DLSTRINGS`。同時提供 byte-identical
的 `_English` 與 `_Chinese` 檔；目前 `sLanguage=ENGLISH` 的 profile 會使用 `_English` 檔。

本補丁只改 99 個 `FULL` 與 99 個 `DESC` 的顯示文字。FormID、EditorID、效果、條件、rank chain
及所有其他 payload 均維持 USSEP 4.3.8a 不變。Constellations 後置覆寫的兩筆 standing-stone perk
未納入，因此不會把已驗收的 Constellations winner 蓋回 USSEP。

來源、人工調整與驗證證據分別見 [SOURCE.md](SOURCE.md) 與 [VERIFICATION.md](VERIFICATION.md)。
