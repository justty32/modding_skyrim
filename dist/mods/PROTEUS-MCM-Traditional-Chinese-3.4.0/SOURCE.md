# Source provenance

- 目標版本：PROTEUS 3.4.0。
- 原始 `Source/Scripts/ProteusMCMScript.psc` SHA-256：`36ba7794673108c9b025b95cd0a03a81cad9d469e9f8e9429391e8da69569740`。
- 原始 `Scripts/ProteusMCMScript.pex` SHA-256：`2f84e5bd5dcafcaa1e036d2cee1e3420fccd14df3743a104975108a6750f0beb`。
- 頁籤記錄：`17DC8D:PROTEUS.esp`，EditorID `ZZProteusMCMQuest`。

腳本以原始 PEX 的乾淨反編譯結果為基底，替換 34 個玩家可見常值；相容性判斷字串
`Sacrosanct - Vampires of Skyrim.esp` 保持不變。另新增 `OnConfigOpen`，在 SkyUI 讀取頁籤前把
saved `Pages` property 重建為兩個翻譯鍵；這是 2026-08-16 首輪 runtime 發現既有存檔仍保留
`General`／`Hotkeys`、導致空頁後加入的 save compatibility 修正。編譯使用 Creation Kit 隨附的
Papyrus Compiler，以及 [SkyUI 官方原始碼](https://github.com/schlangster/skyui) 的 SDK source；
未採用 MCM Recorder 內含的修改版相依 source。

`tools/translation-source.tsv` 是可審閱的唯一翻譯來源，建置工具由它生成遊戲讀取的 UTF-16LE 翻譯檔。
