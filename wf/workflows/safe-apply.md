# safe-apply — 一次性套用腳本與暫存／備份的生命週期

[WORKFLOWS](../WORKFLOWS.md)｜[INDEX](../INDEX.md)

任何「寫 live 檔案的一次性腳本」（改 profile 三檔、批次刪除、批次部署）該帶的保險，與暫存產物從建立到清掉的規矩。模式固定是 soft baseline＋hard anchor＋寫後驗證回滾，不要每條線自創。

**何時用**：寫會動 live 狀態的套用腳本（profile 檔、mods 目錄、mod-library）；規劃批次刪除；多線備料後的一次性總控套用。
**何時不用**：houseCARL 寫新 plugin（本來就不動原檔）；純讀取／盤點；git 層的回滾（走 git 本身）。

## Done when

- 套用腳本含三道保險且 dry-run 輸出留檔：①前置 guard（MO2/遊戲未在跑、目標狀態符合預期）②筆數／錨點斷言 ③寫後驗證不符自動回滾。
- 備份路徑在**非 tmpfs 的實體磁碟**，且 REPORT 記了備份位置與還原指令。
- 刪除類：trash 目錄仍在（等確認後二次清除）或 REPORT 記了使用者授權的 `--yes` 執行紀錄。

## 流程

### 寫前與備份

1. **寫前**：
   - guard：`ps -eo comm=` 比對 MO2/遊戲行程（別用 pgrep -f，見 lessons/this-machine）；多線同樹時只檢查本線負責路徑乾淨。
   - 基線：目標檔 sha256 做 **soft baseline**（不符印警告不擋）＋關鍵錨列存在性做 **hard gate**（不符即 abort）——檔案會被別線或 MO2 回寫，死鎖在整檔 sha 會誤擋，完全不驗會誤寫。
   - 操作當下重讀現行狀態，不採信計畫檔裡的舊快照。
2. **備份**：寫前備份到實體磁碟路徑（`~/skyrim_mods/_backup-*` 類），**絕不放 `/tmp`**——它是 tmpfs，重開機即消失。備份位置與還原指令寫進 REPORT。
### 套用

3. 斷言與回滾：
   - 預期變動筆數先算好，寫後實際筆數不符＝斷言失敗即停。
   - 寫後重算 sha／重讀錨列驗證，不符自動回滾到備份。
   - 多件總控：固定順序、逐件 verify 通過才推進下一件；中途失敗**留現場**（已過驗證的不回滾），REPORT 標明停在哪。
   - 批次腳本明確用 `bash` 跑（zsh 陣列 1 起算會整批錯位）。
### 刪除與收線

4. **刪除類加碼**：先 `mv` 到磁碟 trash 目錄，不直接 `rm`；確認系統能正常啟動／驗收通過後，才二次確認清掉 trash。子代理只備腳本＋dry-run，`--yes` 由頂層在使用者面前跑（lessons/dispatch-delegation 的 relayed-delete 節）。
5. **暫存生命週期**：中間產物放線目錄或 scratchpad，**收工自清**；>5 MB 的不進版控（gzip 或留磁碟）；寫進 `mods/` 的暫存目錄開 MO2 前必須清掉（MO2 會自動收編散目錄）；解壓殘留要另外 `du` 盤點，掃描工具的報表只統計壓縮檔。
6. **收線**：`hygiene_check.py` 跑過；trash／備份的保留期限與清除條件寫進 REPORT 或 WAIT_USER。

## 交接

- 套用對象是 profile 三檔 → 細則看 profile-change；刪除需要使用者授權 → WAIT_USER 一行；事故回顧 → [lessons/git-commit-hygiene](../lessons/git-commit-hygiene.md)、[lessons/mod-install-audit](../lessons/mod-install-audit.md)。
