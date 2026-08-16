# Improved Follower Dialogue - Lydia 4.2.2 正體中文

這是 IFD Lydia `4.2.2` 的可停用正體中文覆寫，對應 Nexus mod ID `38473`。使用時仍需先安裝
官方主模組；本包只讓下列兩個檔案在 MO2 中勝出：

```text
ImprovedCompanionsBoogaloo.esp
scripts/lydiaconfigscriptnew.pex
```

不包含 BSA、語音、模型、材質，也不包含 Bruma、Wyrmstooth 或 LOTD optional patch。停用本包即可
回到官方英文 ESP 與 BSA 內的原始 PEX。

## 翻譯範圍

- ESP：1,794 個玩家可見字串，包括 408 個對話選項、1,288 段回應、20 個回應提示、任務名稱／
  目標、書籍、NPC／地點／法術名稱與說明。
- PEX：18 個 MCM 標題、選項與說明。
- 79 個與 Skyrim 原版英文完全相同的字串直接採用現役 Skyrim Traditional Chinese 8.20 譯文；
  其餘 1,715 個以同版 IFD Lydia CHS archive 為語意種子，經 OpenCC `s2tw` 轉換並統一
  `天霜`、`男爵`、`萊迪亞` 等術語。
- MCM 18 項另行人工整理，不直接沿用簡中逐字轉換。

完整逐欄來源、目標與 provenance 在
[translation-source.json](tools/translation-source.json)。

## 版本邊界

只對應官方 `ImprovedCompanionsBoogaloo.esp` 4.2.2 的精確 SHA-256：
`b1f7482ba331618aec8194e154f28eb2e0c78c9ca2ce4d2a09e35668c7f85a8d`。不要拿來覆寫其他版本。

本包的 ESP 沿用翻譯 archive 的做法，將正體中文直接寫成 UTF-8 inline zstring；它不是 localized
STRINGS patch。離線驗證不等同於目前 Proton／`sLanguage=ENGLISH` 的遊戲內顯示驗收；實際 profile
部署與 runtime 狀態以部署工作區為準，本 artifact 不維護機器專屬狀態。

## 重建與驗證

```bash
python tools/translation_pipeline.py build \
  --source-esp "/path/to/official/ImprovedCompanionsBoogaloo.esp" \
  --source-bsa "/path/to/official/ImprovedCompanionsBoogaloo.bsa"

python tools/translation_pipeline.py verify \
  --source-esp "/path/to/official/ImprovedCompanionsBoogaloo.esp" \
  --source-bsa "/path/to/official/ImprovedCompanionsBoogaloo.bsa"

sha256sum -c MANIFEST.sha256
```

來源契約與離線 gate 分別見 [SOURCE.md](SOURCE.md) 和 [VERIFICATION.md](VERIFICATION.md)。
