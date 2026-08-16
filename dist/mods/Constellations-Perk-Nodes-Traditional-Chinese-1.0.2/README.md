# Constellations Perk Nodes Traditional Chinese 1.0.2

Constellations 1.0.2 三棵自訂技能樹的可見天賦節點繁體中文補丁。

三個 JSON 技能樹共有 27 個可見根節點；其中 7 個節點有後續 rank chain，因此實際翻譯 44 筆 PERK 的名稱與說明。補丁刻意排除自動／內部 perk、功能效果 perk，以及原版 Skyrim perk override。

## 安裝契約

需要原版 Constellations 1.0.2。MO2 中本模組排在 Constellations 後方，並讓 `Constellations Perk Nodes Traditional Chinese 1.0.2.esp` 在 `ConstellationsNewSkills.esp` 後載入。

外掛採 localized 格式，繁中文字串存於 UTF-8 `STRINGS`／`DLSTRINGS`。同時提供 byte-identical 的 `_English` 與 `_Chinese` 檔；目前 `sLanguage=ENGLISH` 的 profile 會使用 `_English` 檔。

本補丁只改 44 個 PERK 的 `FULL`／`DESC` 顯示文字。效果、條件、rank chain、FormID、EditorID 與其他 payload 均維持來源不變。
