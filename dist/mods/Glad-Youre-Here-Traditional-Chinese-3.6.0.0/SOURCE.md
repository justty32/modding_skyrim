# Source — Glad You're Here Traditional Chinese 3.6.0.0

## 版本依據

唯一版本來源是現役 `Modpack-KR-Dev` 的已安裝主檔：

```text
/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/Glad You're Here - Main File/
```

- `meta.ini`：`version=d2026.6.13.0`、`newestVersion=3.6.0.0`、`modid=41856`。
- 上游檔：`interface/translations/ImGladYoureHere_english.txt`
- 上游 SHA-256：`a28b0f834f8db92de2a4cccc28bd41350a5d471ac90f2f782b039f33b7e3ae1c`
- 上游格式：UTF-16 LE BOM、213 筆、每筆一個 Tab。來源本身是 LF；依本交付的明確格式要求，覆寫產物使用 UTF-16 LE BOM 與 CRLF。
- 檢查／建置日期：2026-08-15。

gameplay seed 是 Nexus 82669 `I'm Glad You're Here 3.2.3` 簡中 ESP：archive SHA-256
`2a19d83ac9a92336222643f149dc82bf5138a70c85396508a9011f47dd65c21f`，ESP SHA-256
`1335bba1c37ac8c96345aa930ba48e13f9fc2bcca7c6c2ea227f4241770cf94e`。它不會直接覆蓋新版；
建置器只抽取穩定 FormID／欄位對應的譯文，經 OpenCC `s2twp` 與人工主題校訂後寫回精確 3.6.0
來源 ESP。

## 衍生內容與邊界

本包的 MCM 譯文由本地自行校訂；gameplay ESP 譯文則以 Nexus 82669 作語意種子，並由現役
3.6.0 ESP 重建 text-only overlay。它不含 MCM JSON、腳本、動畫、模型、材質或語音。

Glad You're Here 及其資產的權利屬原作者。此處未驗證公開再散布授權，故應作為本地使用與審閱產物；公開發布前須另行確認作者的 Permissions 條款。

## 可重建性

- 可審閱來源：`tools/translation-source.tsv`（UTF-8）
- 建置工具：Python 3 標準函式庫
- 遊戲資產：`interface/translations/ImGladYoureHere_english.txt`
- 指令：`python tools/build_translation.py`

這是資料型 text-only override，不是由 `projects/` 下程式 repo 編譯而成，因此沒有對應的專案 commit。
