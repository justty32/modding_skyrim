# Source provenance

- 目標模組：[Adamant - A Perk Overhaul](https://www.nexusmods.com/skyrimspecialedition/mods/30191) 6.0.4 MAIN，Nexus file id `792101`，上傳於 2026-08-19。
- 官方 archive：`Adamant - A Perk Overhaul 30191 6.0.4 2026-08-19T20-58Z Z3mWyIsKY.7z`
- 官方 archive SHA-256：`d68f257da48d4e36a6616ed555962d8bc0237c3705cf9507b89804f7833641b7`
- 官方 `Adamant.esp` SHA-256：`88903af1b94d089858abafbc13bd6172aa1c37e1303cc3fecc0b6fc988ac11a7`
- 直接前版：Adamant 6.0.2 archive SHA-256 `116f715a9608a4f0b8b07fe017bc05c8f6ff0926bbdffb51dfdbf0233dc95afc`；ESP SHA-256 `50c954f8807f10701c8e587a41c12ac5b515e803715dcaa5ce8646028cc29ca4`。
- 舊版英文精確種子：Adamant 5.9.2 archive SHA-256 `947c7ba68a00798e92b0d7d4cfd8cb4d740fd681e6a4113bb6a56994cdd884c4`；ESP SHA-256 `0122c516a8035b2bcb88356b006b34903d4d5e9b242db4d246374a843de3cfb8`。
- 舊版繁中精確種子：[Adamant Mandarin 5.9.2](https://www.nexusmods.com/skyrimspecialedition/mods/89657)，archive SHA-256 `4ff1d64b24690789476609ee9ca14ffb3e28131ee5fd06de870bb6e5b5701e3f`；ESP SHA-256 `741c664085677ce59c91e56d57dbf8a00c283dc34348df23b8c5896565a72fa3`。

`tools/translation-source.tsv` 保存每個 FormKey、record type、EditorID、subrecord 與 occurrence。從已稽核的 6.0.2 版本投影到 6.0.4 時，3,233 個欄位以相同 FormKey／欄位與相同英文精確承接；唯一變動是 `MAG_Barrier02` 說明的英文文法 `effect` → `affect`，人工確認繁中句意不受影響後沿用。上游另移除三個舊 spell records，因此總欄位由 3,240 降為 3,234，沒有新增待翻譯文字。

官方 archive 的 `fomod/info.xml`、Nexus MAIN file 與 archive 名稱均標示 6.0.4；本包仍以 archive／ESP SHA-256 作版本鎖。數值型 GMST `DATA` 不是文字且全部排除；只處理 EditorID 以小寫 `s` 開頭的字串型 GMST。
