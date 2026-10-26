# 天際儲藏庫（mod 資產庫頁）— 2026-10-26 刷新

線上頁：[天際儲藏庫](https://claude.ai/artifact/JSf2pBj7nuY5zKemTp7gEt)（Version 7，私人頁；要給別人看得從頁面的 Share 選單開）。

## 這頁是什麼

`~/skyrim_mods` 下載庫的瀏覽頁：每件 mod 的 Nexus 連結、類別、簡介、裝了沒，「已安裝」分頁照 MO2 modlist 順序列。
頁面由腳本產生，不手改 HTML；腳本、資料來源與重產步驟在 [mod-library/viewer/README.md](../../mod-library/viewer/README.md)。

## 這次刷新了什麼

- 庫存 3,141 件（10-10 版是 3,238；減少的是 10-23 清掉的下載暫存夾和整併掉的中文層）。
- 已安裝狀態對到 profiles `9401c61`（10-26 08:32）：啟用 1,236、停用 68。
- **新功能：舊命名檔的來源辨識。** 檔名看不出 Nexus 編號的 146 個舊壓縮檔，今天逐個查過出處。
  打開一件 mod 看「檔案清單」，這類檔名下面會多一行標籤：
  - **Nexus 原檔（改名或重包）**：其實就是某個 Nexus mod 的檔，附連結。
  - **已辨識，非 Nexus 原檔**：知道是什麼（例如某 mod 的對岸漢化包、Tweaked Conditions 動作補丁、Creation Club 備份），附它對應的 Nexus mod。
  - **工作區自產**：我們自己做的衍生包。
  - **來源不明**：查不到可信出處的 31 個，沒有硬猜，標籤下有線索。
- 146 個裡有 137 個還在庫裡、頁面看得到；其餘 9 個檔案已不在磁碟上，結論只留在資料庫。

## 細節在哪

- 146 筆逐筆結論與統計：[mod-library/audits/README.md](../../mod-library/audits/README.md)（明細資料檔在同目錄）。
- 這條線的內部報告：[agentctl/handoffs/home-2026-10-26/mlib/REPORT.md](../../agentctl/handoffs/home-2026-10-26/mlib/REPORT.md)。
