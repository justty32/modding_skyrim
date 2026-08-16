# PROTEUS MCM Traditional Chinese 3.4.0

PROTEUS 3.4.0 的 MCM 繁體中文補丁。它翻譯兩個頁籤、各項設定、快捷鍵名稱與說明文字，共 34 個字串；不宣稱翻譯 PROTEUS 的所有遊戲內訊息。

## 內容

- `Scripts/ProteusMCMScript.pex`：將玩家可見的英文常值改成 `$PROTEUS_MCM_*` 翻譯鍵；每次
  開啟 MCM 時重建兩頁的 page array，因此既有存檔不會沿用舊的 English Papyrus property。
- `Interface/Translations/PROTEUS_english.txt`：UTF-16LE BOM、CRLF 的繁中翻譯表。檔名刻意使用 `_english`，因為目前遊戲設定是 English。

## 安裝契約

需要原版 PROTEUS 3.4.0。MO2 中本模組必須排在 PROTEUS 後方。這是 script + translation asset
override，沒有 ESP；不要把本包當成獨立 mod 使用。

這是文字與頁籤鍵補丁；新增的唯一控制流程是 save-safe `OnConfigOpen` 頁籤陣列刷新，不修改
快捷鍵值、GlobalVariable 綁定或其他遊戲資料。靜態驗證詳見 [VERIFICATION.md](VERIFICATION.md)。
