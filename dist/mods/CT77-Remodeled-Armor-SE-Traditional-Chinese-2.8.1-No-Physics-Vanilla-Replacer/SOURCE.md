# Source provenance

## 官方來源

- Mod：[Remodeled Armor SE - CBBE 3BA（Nexus 22168）](https://www.nexusmods.com/skyrimspecialedition/mods/22168)
- MAIN file id：`767936`
- 版本／車道：`2.8.1`，CBBE No Physics
- archive：`Remodeled Armor SE - CBBE - No Physics 22168 2.8.1 2026-06-25T14-12Z bqv3tSLro.7z`
- archive bytes：`317685078`
- archive SHA-256：`3dc631e4c3b061e0feb999254172ca42d6df98be86c42461a39ed8accedeb4a6`
- archive test：`7z t` 通過（2,594 files）

唯一 binary baseline 是 archive 內：

```text
Remodeled Armor SE - CBBE - No Physics/
  03 Plugins/Replacer/Eng/Remodeled Armor - Vanilla Replacer.esp
```

- ESP bytes：`220695`
- ESP SHA-256：`611cb362893016a25509db6afabd8753398248d08a05bd54ef93ceb8875f157a`
- masters（原順序）：`Skyrim.esm`、`Update.esm`、`Dawnguard.esm`、`Dragonborn.esm`
- source text topology：70 `FULL`、69 個空 `DESC`

工具會先拒絕任何不符合上述 ESP SHA-256 或 master contract 的輸入，避免把舊版、3BA、AE、Standalone
或其他語言分支誤當來源。

## 正中術語來源

12 個 Skyrim override 的目標文字逐 FormID 取自現役
`Skyrim Traditional Chinese 8.20 Core and Fonts/Strings/Skyrim_English.STRINGS`：

- source table SHA-256：`ae1cd52056ab4b06e44a30a6e0509feeea4f0ddfd186cc5027b6c5af53a14ef4`
- 對應 FormID：`036A44`、`036A45`、`036A46`、`06F398`、`0AD5A0`、`0C0165`、`0C0166`、
  `0D3EAB`、`0E35E7`、`0E35E8`、`0E35E9`、`0E35EA`

58 個 CT77 自有名稱以 source English 為語意基準，沿用 8.20 的既有正中詞彙，例如魔族、影蔽、
夜鶯、硬殼、諾德鍛雕、剛冰石、法莫、玄曜石、翠琉璃、鋼鈑、黎明守衛，以及八個領地／城市名稱。
「Thigh Boots」統一譯作「過膝長靴」，避免生硬的逐字「大腿靴」。

本包沒有採用其他語言版 ESP、第三方翻譯 plugin 或俄文翻譯包作 binary baseline。

