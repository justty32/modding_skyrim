# CT77 Remodeled Armor SE 2.8.1 正體中文

這是 CT77 **CBBE No Physics 2.8.1** 的 **English／Vanilla Replacer／非 AE** 車道專用、可獨立停用的
正體中文文字覆寫。它不包含 meshes、textures、BodySlide、scripts、distribution config 或原模組的
其他資產；使用時仍需要官方主模組。

遊戲會載入的內容只有：

```text
Remodeled Armor - Vanilla Replacer.esp
Strings/Remodeled Armor - Vanilla Replacer_English.STRINGS
Strings/Remodeled Armor - Vanilla Replacer_English.DLSTRINGS
Strings/Remodeled Armor - Vanilla Replacer_Chinese.STRINGS
Strings/Remodeled Armor - Vanilla Replacer_Chinese.DLSTRINGS
```

`English` 與 `Chinese` 的兩套表內容逐 byte 相同：前者服務目前的 `sLanguage=ENGLISH`，後者保留中文
語言設定的對應入口。來源沒有 `ILSTRINGS` 欄位，因此不製造空檔。

## 翻譯範圍

- 70 個 `FULL`：12 個 Skyrim 原版 FormID 逐筆採用 Skyrim Traditional Chinese 8.20 的正中名稱；
  58 個 CT77 自有名稱依同一套材質、派系、地名與裝備術語翻譯。
- 69 個原本為空的 `DESC`：仍保持空字串，只因 plugin 改為 localized 而轉成 `DLSTRINGS` 索引。
- 完整逐筆來源、目標、EditorID、FormKey 與 provenance 在
  [translation-source.tsv](tools/translation-source.tsv)。

## 相容範圍

只對應 Nexus 22168 file `767936` 的 `Remodeled Armor SE - CBBE - No Physics` 2.8.1，並只覆寫
`Remodeled Armor - Vanilla Replacer.esp`。不要拿它覆寫 3BA、AE/CC、Standalone、Underwear、WACCF
或其他版本／分支的同名或相近 plugin。

## 重建與驗證

先從官方 archive 精確抽出 English Vanilla Replacer ESP，再執行：

```bash
python tools/build_translation.py --source "/path/to/Remodeled Armor - Vanilla Replacer.esp"
python tools/verify_translation.py --source "/path/to/Remodeled Armor - Vanilla Replacer.esp"
sha256sum -c MANIFEST.sha256
```

建置與驗證只用 Python 標準函式庫。工具不透過通用 plugin writer 重序列化來源，而是保留原檔的
GRUP／record／subrecord 順序與所有非文字 payload，只改 TES4 localized flag、`FULL`／`DESC` 的
string id 以及因此必須更新的 size 欄位。

本目錄是 release artifact，尚未部署到 MO2，也沒有遊戲內驗收。部署時應讓此包在完全相同的官方
Vanilla Replacer source mod 之後勝出；停用此包即可回到原英文 plugin。

