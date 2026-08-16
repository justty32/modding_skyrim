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
（SHA-256 `6c99a3d976d4331cb456e0ee2cc30c34fac50ff47fadefbaae71888dbbc0a870`）只作 MCM 術語初稿參考。

ESP／PEX 改採 Nexus 67680 的 `Nether's Follower Framework - Traditional Chinese 2.8.6b`
（archive SHA-256 `be9e3a791f140deb1321e3d10f61ee3b81c9cae5f1f9bfbed1339079024b377a`）。
其 ESP SHA-256 是 `5509f40b3b9af4b7711dbbe3e1818c47ddc4aa7a3872933cec58555b9b958dd8`；
它提供 465 個 display zstrings。Dev runtime QA 另證明 dialogue menu 不會解析
`$FF_OutfitCreateMenu` 與 `$FF_SaySubmenu`，所以最終 ESP 以同一份已稽核繁中表的兩個 literal
取代這兩個原始 key；總計只改 467 個 display zstrings。20 個 PEX 只改 297 個既有 string-table slots，
其餘 header、prestrings、declaration、properties 與 bytecode tail 不變。

## 衍生內容與邊界

本包的 MCM 翻譯表是自行校訂；ESP／PEX 譯文來自 Nexus 67680 並只供本地整合與稽核。
NFF 及原翻譯包的權利屬各自作者；公開發布或再散布前必須另行確認 Permissions 條款。

這是資料型 text-only override，不是由 `projects/` 下的程式 repo 編譯而成，因此沒有對應專案 commit。
