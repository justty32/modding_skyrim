# Source provenance

- 目標版本：Unofficial Skyrim Special Edition Patch 4.3.8a。
- 原始 `unofficial skyrim special edition patch.esp` SHA-256：
  `2df73db3622005e04470e3603f804e2fd855ae932a9847073f386bd8013e9d98`。
- 繁中術語來源：`Skyrim Traditional Chinese 8.20 Core and Fonts`。
- record identity 來源檔：`Skyrim.esm`、`Dawnguard.esm`、`Dragonborn.esm`、
  `ccBGSSSE037-Curios.esl`。

`tools/build_review_tsv.py` 以 FormKey 與原始 localized string id 對應 8.20 翻譯，不做模糊文字匹配。
目標集合是 USSEP 內同時具有非空 `FULL` 與 `DESC` 的 99 筆 PERK，共 198 個欄位；兩筆由
Constellations 後置覆寫的 `0E5F46:Skyrim.esm`／`0E5F4A:Skyrim.esm` 有獨立拒絕 gate。

翻譯來源分布：

- 186 個欄位直接沿用 8.20 的同 FormKey 翻譯。
- 8 個欄位依 USSEP 4.3.8a 的新語意／數值調整：Dragon Smithing、Necromancy、Fence、
  Steady Hand 兩 rank、Green Thumb，以及 Dragonborn 兩個祭司面具名稱。
- 4 個 8.20 仍為英文或不完整的欄位由本包補譯：內部 Skill Boosts 說明、NPC Ward Absorb 名稱、
  Silverbolt 名稱與說明。

`tools/translation-source.tsv` 保存每個 FormKey、EditorID、欄位、USSEP 英文原文、繁中目標與
provenance。建置器逐筆核對來源文字；來源版本或任何英文欄位改變時會拒絕建置。

重建 TSV：

```bash
python tools/build_review_tsv.py \
  --source '/path/to/unofficial skyrim special edition patch.esp' \
  --data-dir '/path/to/Skyrim Special Edition/Data' \
  --strings-dir '/path/to/Skyrim Traditional Chinese 8.20 Core and Fonts/Strings'
```

再執行：

```bash
python tools/build_translation.py \
  --source '/path/to/unofficial skyrim special edition patch.esp'
```
