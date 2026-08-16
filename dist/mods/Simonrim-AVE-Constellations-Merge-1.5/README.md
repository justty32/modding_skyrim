# Simonrim／AVE／Constellations 合併補丁

這是 `Thaumaturgy 1.5`、`Armor Variants Expansion` 與
`ConstellationsNewSkills.esp` 的 leveled-list 最終 winner。

補丁完整保留 `AVE - Thaumaturgy.esp` 1.1 的 95 筆 `LVLI` 內容，另外保留
Thaumaturgy 在其餘 89 筆衝突清單的完整語意，再將 Constellations 自有的 162
個物件精確合入 93 筆清單。它取代下列兩個 active patch：

- `AVE - Thaumaturgy.esp`
- `ModpackKR_AVE_Constellations_LeveledListMergeDev.esp`

安裝後讓 `ModpackKR_Simonrim_AVE_Constellations_MergeDev.esp` 位於三個來源
plugin 之後。此補丁沒有文字欄位，不需要漢化。

驗證：

```bash
python tools/verify_merge.py
sha256sum -c MANIFEST.sha256
```
