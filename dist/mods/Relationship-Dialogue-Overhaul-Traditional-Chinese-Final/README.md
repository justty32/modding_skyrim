# Relationship Dialogue Overhaul - RDO Final 正體中文

這是 RDO Final（Nexus mod ID `1187`）的可停用正體中文覆寫。仍需先安裝官方
`Relationship Dialogue Overhaul - RDO Final`；本包只讓同名 ESP 與六個 loose PEX 勝出：

```text
Relationship Dialogue Overhaul.esp
scripts/rdo_geleborfolloweraliasscript.pex
scripts/rdo_geleborfollowerscript.pex
scripts/rdo_isranfolloweraliasscript.pex
scripts/rdo_isranfollowerscript.pex
scripts/rdo_valericafolloweraliasscript.pex
scripts/rdo_valericafollowerscript.pex
```

不包含 BSA、語音、模型、材質或 optional compatibility patches。停用本包即可回到官方英文 ESP
與 BSA 內原始 scripts。

## 翻譯範圍

- ESP：4,071 個玩家可見 UTF-8 字串，其中 3,776 段對話回應；其餘涵蓋對話選項／提示、任務、
  NPC、法術／效果、物品與地點名稱或說明。
- PEX：Gelebor、Isran、Valerica 各兩條「仍在等待／離隊」通知，共六個既有 string-table slots。
- 來源為 `RDO Final CHT`；另外把其唯一大小寫漂移的引擎 token `<BribeCost>` 精確還原為官方
  `<bribecost>`，避免 runtime substitution 風險。

完整逐欄來源、目標與 provenance 在
[translation-source.json](tools/translation-source.json)。

## 版本邊界

只對應官方 Final 的精確 ESP SHA-256：
`b8d33bd731dded257b517402135cc7ba69be8d7e2b2cc8f038481802b363c2d0`，以及 BSA SHA-256：
`40e20585512cc5fe796faab112863592a5549165fd378d5d14a098652207be42`。其他 RDO 版本一律 fail closed。

## 重建與驗證

```bash
python tools/translation_pipeline.py build \
  --source-esp "/path/to/Relationship Dialogue Overhaul.esp" \
  --source-bsa "/path/to/Relationship Dialogue Overhaul.bsa" \
  --seed-archive "/path/to/RDO Final CHT.zip"

python tools/translation_pipeline.py manifest

python tools/translation_pipeline.py verify \
  --source-esp "/path/to/Relationship Dialogue Overhaul.esp" \
  --source-bsa "/path/to/Relationship Dialogue Overhaul.bsa" \
  --seed-archive "/path/to/RDO Final CHT.zip"
```

來源契約與離線 gate 分別見 [SOURCE.md](SOURCE.md) 與 [VERIFICATION.md](VERIFICATION.md)。實際
profile 部署及 runtime 狀態由部署工作區維護，不寫入本 artifact。
