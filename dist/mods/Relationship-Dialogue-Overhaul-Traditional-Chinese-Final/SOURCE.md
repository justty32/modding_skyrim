# Source contract

## 官方 baseline

- Archive：`Relationship Dialogue Overhaul - RDO Final-1187-Final.7z`
- Archive SHA-256：`99988d898c1356e37341a44ed95e8ed0b15bcefcf7626f797d5bd04b9388d5f2`
- `Relationship Dialogue Overhaul.esp` SHA-256：
  `b8d33bd731dded257b517402135cc7ba69be8d7e2b2cc8f038481802b363c2d0`
- `Relationship Dialogue Overhaul.bsa` SHA-256：
  `40e20585512cc5fe796faab112863592a5549165fd378d5d14a098652207be42`

本機已安裝 ESP／BSA 與官方 archive 逐 byte 相同。

## 正體中文來源

- Archive：`RDO Final CHT-22207-Final-1546039712.zip`
- SHA-256：`45271a07353ef99bac7ecff6cbf19da59afec17bdfc8f2f3cb2db43fafbbafd5`
- 取用：同名 ESP 與六個 PEX；不取用其他 patch 或第三方內容。

翻譯 ESP 與官方 Final 具有相同的 9,766 records、FormID／順序／GRUP path、semantic headers 與
subrecord topology。六個 PEX 各只改一個顯示字串 slot，完整 declaration／properties／control flow／
bytecode tail 與官方 BSA 成員逐 byte 相同。

## 本包的額外修正

來源翻譯把官方 token `<bribecost>` 寫成 `<BribeCost>`。本包只把這一處 token case 還原；字串其餘
內容不變。重建器要求來源 archive 恰好有一個 `<BribeCost>` 且沒有 `<bribecost>`，不符合即停止。

本包不重新散布官方 BSA、語音或其他資產。第三方翻譯的再發布／使用權仍由原作者與原頁面條款
約束；此資料夾保存的是本機整合用產物與可重現驗證證據。
