# 驗證紀錄

2026-08-16 驗證項目：

- plugin 恰有 184 筆 `LVLI` 資料記錄；
- masters 恰為 `Skyrim.esm`、`Update.esm`、`Dragonborn.esm`、
  `ConstellationsNewSkills.esp`、`AVExpansion.esp`、`Thaumaturgy.esp`；
- 移除聲明的 162 個 Constellations entry 後，95 筆 AVE/Thaumaturgy donor 與
  其餘 89 筆 Thaumaturgy base 的 canonical semantic hash 全數相同；
- 162 個 Constellations entry 在對應的 93 筆清單中各出現一次；
- 四筆重疊清單的最終筆數為 `18 / 17 / 16 / 242`；
- `LLCT` 與實際 `LVLO` 數量一致；
- package manifest 覆蓋全部成品、文件、contract 與驗證器。

結果：PASS。
