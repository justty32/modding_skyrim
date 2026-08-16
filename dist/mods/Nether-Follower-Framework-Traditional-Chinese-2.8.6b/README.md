# Nether's Follower Framework 2.8.6b 繁體中文文字覆寫

這是 NFF 2.8.6b 的完整繁體中文文字覆寫。除了 1,398 個介面、MCM、通知與腳本翻譯鍵，
也包含精確同版的 ESP 對話與 20 個 PEX 內嵌顯示字串：

```text
Interface/Translations/nwsFollowerFramework_english.txt
nwsFollowerFramework.esp
Scripts/*.pex
```

`english` 檔名刻意保留，供目前使用 `sLanguage=ENGLISH` 的設定載入。ESP 與 PEX 都是從
Nexus 67680 的精確 `2.8.6b` 繁中包經語意稽核後納入：ESP 的 2,917-record 身份、順序、GRUP
路徑、header、subrecord 拓撲與所有非文字 payload 不變；20 個 PEX 的 declaration／properties／
bytecode tail 逐 byte 相同。本包不含 SWF、模型、材質或其他 gameplay 資產。

## 版本與修正範圍

- 目標版本：Nether's Follower Framework `2.8.6b`（Nexus mod ID `55653`）。
- 保留上游所有 key、順序、數字、百分比與 `\\n` 控制碼。
- 修正上游 `$FF_LootSpeedDS` 遺失 Tab、因而無法成為有效翻譯列的問題。
- 修正翻譯草稿中錯誤加入的 `350`、`100%` 語意錯譯，以及兩個遺失的換行控制碼。
- Dev runtime QA 發現 dialogue menu 不會解析兩個 `$` translation key；ESP 因此把
  `$FF_OutfitCreateMenu`、`$FF_SaySubmenu` 精確替換成同一份繁中表內的 literal，避免玩家看到原始 key。

## 重建與驗證

```bash
python tools/build_translation.py
python tools/verify_translation.py --source "/path/to/NFF/Interface/Translations/nwsFollowerFramework_english.txt"
python tools/gameplay_translation_pipeline.py verify --source-mod "/path/to/NFF" --seed-dir "/path/to/extracted/NFF-CHT"
sha256sum -c MANIFEST.sha256
```

可審閱的翻譯真相來源是 UTF-8 的 `tools/translation-source.tsv`。遊戲檔固定使用 UTF-16 LE BOM
與 CRLF。來源與驗證證據分別見 [SOURCE.md](SOURCE.md) 與 [VERIFICATION.md](VERIFICATION.md)。
