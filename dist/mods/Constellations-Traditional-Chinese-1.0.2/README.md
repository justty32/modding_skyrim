# Constellations 1.0.2 繁體中文 text-only override

這是一份供 Skyrim Special Edition 模組
[Constellations - Additional Player Skills](https://www.nexusmods.com/skyrimspecialedition/mods/117352)
1.0.2 使用的繁體中文介面文字覆寫。它只翻譯 Custom Skills Framework 顯示的三個技能名稱與三段技能說明，不含原模組本體。

## 安裝內容

遊戲會讀取的檔案只有：

```text
Interface/Translations/ConstellationsNewSkills_ENGLISH.txt
```

檔名中的 `ENGLISH` 是刻意保留的。製作時檢查的現役 Skyrim profile 設為
`sLanguage=ENGLISH`，而同一環境中的既有繁中介面覆寫也使用 `_english.txt`；若改成
`_CHINESE.txt`，目前環境不會載入它。

翻譯採用：

| Key | 繁體中文 |
|---|---|
| `$Athletics_Name` | 體能 |
| `$HandToHand_Name` | 徒手格鬥 |
| `$Sorcery_Name` | 巫術 |
| `$Athletics_Description` | 受過體能訓練的人能跑得更快，並能更長久地維持耐力。 |
| `$HandToHand_Description` | 徒手格鬥的技藝。精通此技能者能以雙拳更快、更有力地出擊。 |
| `$Sorcery_Description` | 從法杖與卷軸等魔法物品汲取力量的技藝。技藝精湛的巫師甚至能操控周遭世界中的魔法。 |

## 相容性與範圍

- 目標版本：Constellations 1.0.2。
- 需要原模組及其相依套件；本包不含 ESP、DLL、Papyrus、JSON、模型、材質或語音。
- 原模組沒有 MCM 設定檔。三份技能 JSON 的 `name`／`description` 恰好引用本包保留的六個 `$key`。
- `ConstellationsNewSkills.esp` 內仍有 perk、魔法效果、裝備、對話等英文文字；text-only override 無法覆寫它們，因此本包不是完整 ESP 漢化。
- 此產物沒有執行 MO2 安裝、啟用、排序或遊戲內測試。部署狀態仍應由 `~/notes/projects/modding/skyrim/` 管理。

## 驗證

檔案刻意保留上游格式：UTF-16 LE、BOM、CRLF、六筆資料、每筆恰好一個 Tab，且 key 與順序完全相同。

在本資料夾執行：

```bash
python tools/verify_translation.py
python tools/verify_translation.py --source "/path/to/Constellations/Interface/Translations/ConstellationsNewSkills_ENGLISH.txt"
sha256sum -c MANIFEST.sha256
```

可重現建立遊戲資產：

```bash
python tools/build_translation.py
```

來源、授權邊界與建置資訊見 [SOURCE.md](SOURCE.md)，本次實際驗證結果見
[VERIFICATION.md](VERIFICATION.md)。
