# Source — BFCO Traditional Chinese 3.100.5

## 唯一版本基準

本產物唯一使用下列現役 `Modpack-KR-Dev` BFCO 3.100.5 檔案作為版本與結構基準：

```text
/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/BFCO - Attack Behavior Framework 3.100.5/Interface/Translations/SCSI-ACTbfco-Main_english.txt
```

- 檢查日期：2026-08-15
- SHA-256：`58f76ec42ea6d36f1a6a59e1e040fe0bd54bfc640e9a45c7ebb57fc9f9a18abb`
- 格式：UTF-16 LE with BOM、CRLF、51 個行結束符（52 個邏輯行）、最後三個空白行
- 資料列：37 個 key；值為簡體中文，儘管檔名後綴為 `_english.txt`

未使用 BFCO 3.100.3 或其他版本，也未以網頁、Nexus 或其他翻譯檔作為文字／版本來源。

## 衍生內容

`tools/translation-source.txt` 是本包唯一可審閱的繁中譯稿，UTF-8、LF。`tools/build_translation.py` 在不改變行數、key、順序與空白行版面的前提下，轉成遊戲要求的 UTF-16 LE BOM／CRLF 檔案。

產物只含自行撰寫的繁體中文譯文、由它產生的文字覆寫，以及本包的說明／建置／驗證工具；不重新散布 BFCO 的其他檔案。原模組與其資產的權利仍屬原權利人；若要公開發布，應另行確認適用的發布許可。

## 建置

- 建置日期：2026-08-15
- 技術棧：Python 3 標準函式庫
- 指令：`python tools/build_translation.py`
- 輸出：`Interface/Translations/SCSI-ACTbfco-Main_english.txt`

這是資料型覆寫包，並非從 `projects/` 內程式 repo 編譯，因此沒有對應 commit。
