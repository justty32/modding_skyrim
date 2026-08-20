# Sofia Follower 2.51 正體中文 v2

這是 Sofia - The Funny Fully Voiced Follower `2.51` 的正體中文覆寫，語意來源為 Nexus mod
[183562](https://www.nexusmods.com/skyrimspecialedition/mods/183562) 的 Traditional Chinese
Localization Patch v2。使用時仍需先安裝官方主模組；本包只讓下列檔案在 MO2 中勝出：

```text
SofiaFollower.esp
scripts/qf_jjsofiadrunk_0201a866.pex
scripts/sofiacatchupnewscript.pex
scripts/sofialeadthewayscript.pex
scripts/sofiamarriagescript.pex
scripts/sofiamcmscript.pex
scripts/sofiaplayergive.pex
scripts/tif__0205d40d.pex
scripts/tif__02061f74.pex
```

不包含 BSA、語音、模型、材質或 Sofia bugfix；停用本包即可回到官方英文 ESP／PEX。

## 翻譯範圍

- ESP：1,665 個玩家可見文字欄位，包括 1,464 段對話回應、111 個 topic、任務／目標、NPC、
  地點、物品、法術、訊息與說明。
- PEX：8 個既有腳本共 105 個 string-table slots，包括完整 Sofia MCM 與左上角通知。
- 正體 v2 seed 已是繁中；重建時再用 OpenCC `s2tw` 統一殘留字形。12 個純標點欄位
  `...` → `……` 以明確人工 ledger 納入，不放寬一般文字 gate。

逐欄來源與目標在 [translation-source.json](tools/translation-source.json)。

## 版本邊界

只對應官方 `SofiaFollower.esp` 2.51 的精確 SHA-256：
`8c70186252d0a4415e1ff02584b87adca4c685a4fc4d2dec94c09040ef3ec3c9`，以及同 archive 的
`SofiaFollower.bsa`：
`bc4b3bc004a95dd70681a7d4417ed6926c8ccf6fa38ade77069853d949ba0574`。不要覆寫其他版本。

## 重建與驗證

先解開 Nexus v2 archive，再執行：

```bash
python tools/translation_pipeline.py build \
  --source-esp "/path/to/official/SofiaFollower.esp" \
  --source-bsa "/path/to/official/SofiaFollower.bsa" \
  --seed-dir "/path/to/extracted/Sofia-Traditional-Chinese-v2"

python tools/translation_pipeline.py verify \
  --source-esp "/path/to/official/SofiaFollower.esp" \
  --source-bsa "/path/to/official/SofiaFollower.bsa" \
  --seed-dir "/path/to/extracted/Sofia-Traditional-Chinese-v2"

sha256sum -c MANIFEST.sha256
```

來源契約見 [SOURCE.md](SOURCE.md)，離線 gate 見 [VERIFICATION.md](VERIFICATION.md)。
