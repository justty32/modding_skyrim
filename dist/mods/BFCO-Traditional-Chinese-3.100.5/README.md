# BFCO 3.100.5 繁體中文 text-only override

這是給 **BFCO - Attack Behavior Framework 3.100.5** 的繁體中文介面文字覆寫包。遊戲會讀取的檔案只有：

```text
Interface/Translations/SCSI-ACTbfco-Main_english.txt
```

`english` 檔名刻意保留：它與現役 `Modpack-KR-Dev` 安裝中的 BFCO 3.100.5 基準檔完全相同。這不是誤植，也不應改為 `chinese` 或 `traditionalchinese`。

## 範圍

- 保留 3.100.5 基準檔的全部 37 個 key、順序、空白行、ASCII／檔名／按鍵等格式 token。
- 遊戲資產維持 UTF-16 LE、BOM、CRLF，且維持原檔最後三個空白行與最終 CRLF。
- 僅覆寫 BFCO 的此一 Interface translation 檔；不含 BFCO 本體、ESP、DLL、動畫、行為檔、設定檔或任何 MO2 profile 資料。
- 基準檔雖名為 `english`，其值實際是簡體中文；本包將這些值改為繁體中文，並未拿其他 BFCO 版本當來源。

## 可審閱與可重建

可審閱的 UTF-8 文字在 `tools/translation-source.txt`。重新建立遊戲資產：

```bash
python tools/build_translation.py
```

驗證目前產物：

```bash
python tools/verify_translation.py
python tools/verify_translation.py --source "/path/to/BFCO 3.100.5/Interface/Translations/SCSI-ACTbfco-Main_english.txt"
sha256sum -c MANIFEST.sha256
```

第二個指令會強制比對唯一允許的 3.100.5 基準檔雜湊、key／順序、空白行配置與非 CJK 格式 token。來源與驗證結果分別見 [SOURCE.md](SOURCE.md) 與 [VERIFICATION.md](VERIFICATION.md)。

Done when: 此資料夾含可由 UTF-8 審閱來源重建的繁中覆寫、並能驗證其與現役 BFCO 3.100.5 基準檔的格式相容性；不包含 MO2 安裝、啟用、排序或遊戲內測試。
