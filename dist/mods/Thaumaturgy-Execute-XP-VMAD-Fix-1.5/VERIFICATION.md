# 驗證

`tools/verify_translation.py` 鎖定 source patch SHA-256、三個 masters、兩筆 record、兩個文字欄位，
並驗證 localized 產物除了 TES4 localized flag 與 `FULL`／`DNAM` string ID 外，record 路徑、
subrecord 拓撲與所有非文字 payload 都完全相同；同時檢查 UTF-8、token、可重現建置與完整 manifest。

部署後另須由 houseCARL 驗證：本 patch 為 `2EDE92:Thaumaturgy.esp` 的最終 winner、
`MAG_EnchantmentXP_Script.PlayerRef = 000014:Skyrim.esm`，且 scoped script-property gate 不再回報
這筆 unbound。其他 shader／吸收特效的可選屬性保持上游原樣，不在此修補擴張範圍。
