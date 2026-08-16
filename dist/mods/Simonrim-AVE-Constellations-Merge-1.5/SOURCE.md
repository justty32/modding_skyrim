# 來源與建構

- Thaumaturgy 1.5：Nexus Mods 57138，file id 787801。
- Thaumaturgy - Armor Variant Expansion Patch 1.1：Nexus Mods 58671，file id 444724。
  - donor plugin SHA-256：`2be517fdb58262230c1e1100680d2ff95301c2221655c9b019fc64d2027894a0`
- 舊 Constellations merge：
  - `ModpackKR_AVE_Constellations_LeveledListMergeDev.esp`
  - SHA-256：`eb49df3069040d41a8f20c2f6592d7dafbe553687b3e47975b0fb2cef38402ee`

建構方式：先以 houseCARL 從 `AVE - Thaumaturgy.esp` 明確 forward 全部 95 筆
winner，再從 Thaumaturgy 1.5 forward 其餘 89 筆會被 Constellations 舊資料覆蓋
的清單。最後以 all-or-nothing `bulk_apply` 加入 93 筆清單內全部 162 個
Constellations-owned reference；只合入其自有記錄，不把 Constellations 攜帶的
舊版 vanilla 清單重新灌回去。來源 plugin 均未被 in-place 修改。

`tools/contract.json` 保存 184 筆 base 記錄的逐記錄語意 SHA-256 與 162 個明確
addition，因此驗證不需要重新散布第三方 Nexus plugin，也能證明來源清單內容
均未遺失或改寫。
