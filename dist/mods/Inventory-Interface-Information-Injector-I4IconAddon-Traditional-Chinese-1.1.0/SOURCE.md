# Source — Inventory Interface Information Injector I4 Icon Addon Traditional Chinese 1.1.0

## 上游來源

- 模組：[Inventory Interface Information Injector](https://www.nexusmods.com/skyrimspecialedition/mods/85702)
- Nexus Mods ID：`85702`
- 目標版本：`1.1.0`
- 本次檢查日期：2026-08-15
- 已安裝來源封存檔名：`Inventory Interface Information Injector (SE)-85702-1-1-0-1713968718.7z`
- 上游翻譯檔：`Interface/Translations/I4IconAddon_ENGLISH.txt`
- 上游翻譯檔 SHA-256：`55154e3fd85ad1fc71624dad7fe3c48cffa0c4fc10afb582e49010e13b4ad376`
- 上游翻譯檔格式：UTF-16 LE with BOM、CRLF、17 筆、最後一筆無換行

本產物以現役安裝的 1.1.0 英文檔為 key、順序與格式的權威來源。另只讀檢查本機 `Inventory Interface Information Injector - CHS` 1.0.1 封存檔中的同路徑檔案，確認其也有相同 17 個 key；其簡體文字僅作術語種子，未把該封存檔或任何其他資產納入產物。

## 衍生內容與授權邊界

本產物只含 17 筆自行編修的繁體中文譯文、由此產生的介面文字檔，以及本專案自己的說明與驗證工具。它不散布原模組的 ESP、DLL、JSON、SWF、Papyrus、模型、材質、語音或英文原檔。

原模組及美術的權利仍屬原作者。未在本次工作中確認公開再散布條件；本產物應視為本地使用／審閱用。公開發布前仍須確認 Nexus Mods 的 Permissions 頁面或取得作者許可。

## 建置

- 建置日期：2026-08-15
- 技術棧：Python 3 標準函式庫
- 可審閱譯文：`tools/translation-source.tsv`（UTF-8）
- 產物：`Interface/Translations/I4IconAddon_ENGLISH.txt`（UTF-16 LE with BOM、CRLF）
- 建置指令：`python tools/build_translation.py`
