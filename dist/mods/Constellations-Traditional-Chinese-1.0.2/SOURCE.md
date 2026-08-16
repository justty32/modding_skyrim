# Source — Constellations Traditional Chinese 1.0.2

## 上游來源

- 模組：[Constellations - Additional Player Skills](https://www.nexusmods.com/skyrimspecialedition/mods/117352)
- Nexus Mods ID：`117352`
- 作者：Parapets
- 目標／最新 main file 版本：`1.0.2`
- 最新 main file 日期：2024-11-03
- 本次檢查日期：2026-08-15
- 已安裝來源封存檔名：`Constellations-117352-1-0-2-1730665883.7z`
- 上游翻譯檔 SHA-256：`69646dc81195b7e4faeb81cc88ddecf76af7a2b1a7467af2d26e45eb3aa0caa4`
- 上游翻譯檔格式：UTF-16 LE with BOM、CRLF、6 筆、最後一筆無換行

版本與相依資訊以 houseCARL 的 Nexus Mods 唯讀查詢及本機已安裝來源交叉確認。來源 JSON 為：

```text
SKSE/Plugins/CustomSkills/Constellations/Athletics.json
SKSE/Plugins/CustomSkills/Constellations/HandToHand.json
SKSE/Plugins/CustomSkills/Constellations/Sorcery.json
```

三者的 `name` 與 `description` 共引用六個翻譯 key，本產物逐項保留 key 與順序。

## 衍生內容與授權邊界

本產物只含六筆自行撰寫的繁體中文譯文、由該譯文產生的介面文字檔，以及本專案自己的說明與驗證工具。它不再散布原模組的 ESP、DLL、JSON、Papyrus、模型、材質、語音或英文原檔。

原模組及美術的權利仍分別屬於原作者。這次檢查沒有取得足以確認公開再散布條件的授權文字，因此此產物應視為本地使用／審閱用；公開發布前仍須確認 Nexus Mods 的 Permissions 頁面或取得作者許可。

## 建置

- 建置日期：2026-08-15
- 技術棧：Python 3 標準函式庫
- 可審閱譯文：`tools/translation-source.tsv`（UTF-8）
- 產物：`Interface/Translations/ConstellationsNewSkills_ENGLISH.txt`（UTF-16 LE with BOM、CRLF）
- 建置指令：`python tools/build_translation.py`

這不是由 `projects/` 下某個程式 repo 編譯出的二進位；它是直接依上游 1.0.2 語言 key 製作的資料型衍生產物，因此沒有對應的專案 commit。
