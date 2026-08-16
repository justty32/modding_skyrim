# Source provenance

- 目標模組：[Adamant - A Perk Overhaul](https://www.nexusmods.com/skyrimspecialedition/mods/30191) 6.0.2 MAIN，Nexus file id `790023`，上傳於 2026-08-15。
- 官方 archive：`Adamant - A Perk Overhaul 30191 6.0.2 2026-08-15T00-37Z eVtX7JLTx.7z`
- 官方 archive SHA-256：`116f715a9608a4f0b8b07fe017bc05c8f6ff0926bbdffb51dfdbf0233dc95afc`
- 官方 `Adamant.esp` SHA-256：`50c954f8807f10701c8e587a41c12ac5b515e803715dcaa5ce8646028cc29ca4`
- 舊版英文精確種子：Adamant 5.9.2 archive SHA-256 `947c7ba68a00798e92b0d7d4cfd8cb4d740fd681e6a4113bb6a56994cdd884c4`；ESP SHA-256 `0122c516a8035b2bcb88356b006b34903d4d5e9b242db4d246374a843de3cfb8`。
- 舊版繁中精確種子：[Adamant Mandarin 5.9.2](https://www.nexusmods.com/skyrimspecialedition/mods/89657)，archive SHA-256 `4ff1d64b24690789476609ee9ca14ffb3e28131ee5fd06de870bb6e5b5701e3f`；ESP SHA-256 `741c664085677ce59c91e56d57dbf8a00c283dc34348df23b8c5896565a72fa3`。

`tools/translation-source.tsv` 保存每個 FormKey、record type、EditorID、subrecord 與 occurrence。2,020 筆由 5.9.2 相同 FormKey 精確轉送，496 筆由舊版相同英文片語轉送，724 筆 6.0.2 新增／改寫欄位依 Skyrim Traditional Chinese 8.20 與既有 Adamant 術語校訂。外部機器翻譯只用於未發布初稿；最終 TSV 已統一法力、護具防禦力、失衡、致命一擊、魔力塑形武器等遊戲術語並通過 token gate。

官方 archive 的 `fomod/info.xml` 仍標示 6.0.0；Nexus MAIN file、archive 名稱與實際 ESP 鎖定為 6.0.2。本包以 archive／ESP SHA-256 為版本真相，不依賴該陳舊 FOMOD 顯示值。數值型 GMST `DATA` 不是文字且全部排除；只處理 EditorID 以小寫 `s` 開頭的字串型 GMST。
