# Verification — TrueHUD Traditional Chinese d2026.4.12.0

## Done when

遊戲資產以 UTF-16LE BOM/CRLF 產生，並經工具驗證與現役英文來源有完全相同的 key、順序、空白版面和 XML/色碼 token；本次不包含 MO2 部署或遊戲內驗證。

## 已執行

```bash
python tools/build_translation.py --source "/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/TrueHUD/Interface/Translations/TrueHUD_english.txt"
python tools/verify_translation.py --source "/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/TrueHUD/Interface/Translations/TrueHUD_english.txt"
sha256sum -c MANIFEST.sha256
```

結果記錄於交付時的命令輸出；未執行遊戲、GUI、MO2 安裝、啟用或排序。
