# Source — Nether's Follower Framework Traditional Chinese 2.8.6b

## 版本依據

唯一 gameplay key 契約來源是現役已安裝的 NFF 2.8.6b：

```text
/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/Nether's Follower Framework/
```

- `meta.ini`：`modid=55653`、`version=2.8.6.0b`。
- 英文來源：`Interface/Translations/nwsFollowerFramework_english.txt`。
- 英文來源 SHA-256：`4a43027afafdd3654d6e17b5a7b5aac7e0f5469ac0743f6646d015d493f2fd2f`。
- 格式：UTF-16 LE BOM、CRLF；1,397 個合法 key，另有一列 `$FF_LootSpeedDS` 因上游漏 Tab 而失效。
- 檢查／建置日期：2026-08-16。

同版本簡中包 `Nether's Follower Framework Chinese Translation-113822-2-8-6b-1712844205.zip`
（SHA-256 `6c99a3d976d4331cb456e0ee2cc30c34fac50ff47fadefbaae71888dbbc0a870`）只作術語與初稿參考。
其 ESP 與 19 個 PEX 均未納入本產物：它們與現役 NFF 本體 byte 不同，且本次未取得足以證明
behavior-preserving 的語意差異證據。

## 衍生內容與邊界

本包只包含自行校訂的繁體中文譯文、由該譯文重建的同名翻譯表、驗證工具與文件。不複製或
散布 NFF 的 ESP、PEX、SWF、模型、材質、原始說明書或其他資產。NFF 及原翻譯包的權利屬各自
作者；公開發布前仍須確認 Permissions 條款。

這是資料型 text-only override，不是由 `projects/` 下的程式 repo 編譯而成，因此沒有對應專案 commit。
