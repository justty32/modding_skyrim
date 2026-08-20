# Recorder Follower 3.0 正體中文

這是 Recorder Follower `3.0` 的可停用正體中文覆寫。使用時仍需先安裝官方主模組；本包只讓
`Recorder Follower Base.esp` 在 MO2 中勝出，不包含 BSA、語音、模型、材質或 bugfix patch。
停用本包即可回到官方英文 ESP。

## 翻譯範圍

- 1,429 個玩家可見文字欄位：1,132 段回應字幕、99 個 response prompt、134 個對話 topic、
  24 個任務／目標，以及 NPC、書籍、物品、地點、法術與說明。
- 以標示 Recorder 3.0 的正體中文 ESP 作語意種子，再用 OpenCC `s2tw` 統一殘留字形。
- 79 個未變的英文欄位是資產路徑、內部 head-part／quest 名稱、作者名、控制資料或刻意保留的專名；
  不將可解碼的二進位資料誤翻成文字。

逐欄來源與目標在 [translation-source.json](tools/translation-source.json)。

## 版本邊界

只對應官方 `Recorder Follower Base.esp` 3.0 的精確 SHA-256：
`85c36c5e264980e4f2b7e0913c4647b24b4351e7cea4f3c431d4cb3d3f8c58ca`。不要覆寫其他版本。

## 重建與驗證

```bash
python tools/translation_pipeline.py build \
  --source-esp "/path/to/official/Recorder Follower Base.esp" \
  --seed-esp "/path/to/Recorder 3.0 CHT/Recorder Follower Base.esp"

python tools/translation_pipeline.py verify \
  --source-esp "/path/to/official/Recorder Follower Base.esp" \
  --seed-esp "/path/to/Recorder 3.0 CHT/Recorder Follower Base.esp"

sha256sum -c MANIFEST.sha256
```

來源契約見 [SOURCE.md](SOURCE.md)，離線 gate 見 [VERIFICATION.md](VERIFICATION.md)。
