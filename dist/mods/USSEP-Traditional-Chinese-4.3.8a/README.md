# USSEP 4.3.8a 正體中文 text-only override

本包以現役 `Unofficial Skyrim Special Edition Patch 4.3.8a` 的精確 ESP 為唯一 gameplay 基底，
將 4.3.6c 簡中種子中能以 record FormID＋localizable tag occurrence 穩定對齊的文字轉成台灣正體。
遊戲資產只有同名 ESP：

```text
unofficial skyrim special edition patch.esp
```

它保留 58,965 筆現役 records 的身份、順序、header、GRUP path、subrecord topology 與所有非文字
payload；只修改經 ledger 記錄的 17,904 個文字欄位。另有 562 個跨版本 token／換行或空來源
不相容候選被 gate 排除。Elrindir 的 `Why the name "Drunken Huntsman"?`、
`Who should I talk to for work?` 與相關回答已依現有 Skyrim 8.20 正體術語人工校訂。

這不是把 4.3.6c 舊 ESP 覆蓋到 4.3.8a。新版無法安全對齊的文字刻意保留英文，不冒充百分之百
完整翻譯。Play profile 在 Dev runtime 驗收前不納入。

## 重建與驗證

```bash
python tools/translation_pipeline.py verify \
  --source "/path/to/USSEP-4.3.8a/unofficial skyrim special edition patch.esp" \
  --seed "/path/to/extracted/USSEP-4.3.6c-CHS/unofficial skyrim special edition patch.esp"
sha256sum -c MANIFEST.sha256
```
