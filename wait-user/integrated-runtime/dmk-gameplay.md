## DMK 中文層 smoke 以標準 baseline save 重跑

2026-09-01 的 DMK（**Directional Movement Keys** 1.5.0）smoke 執行時，baseline save pair
不在磁碟上（`7e70ae2` 誤刪，2026-09-02 已於公司復原），因此當時開檔用的不是 `runtime-qa` 規定的固定基準。
回家以復原後的 baseline save pair 重跑一次 DMK 中文層 smoke。
**通過**＝以標準基準開檔，DMK 中文層顯示與 2026-09-01 的結論一致；若不一致，原結論作廢並重驗。

**路徑已變（2026-09-04）**：baseline pair 依使用者 09-04 第 10 題裁示 A 搬到
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/.repo/baselines/ModpackKRDev0A.{ess,skse}`
（2026-09-05 實讀該目錄兩檔皆在，2.9 MB／6.2 KB），**不再在 `modpack-main/saves/` 底下**。
證據：`instance/profiles` commit `0f64c20`、母 repo commit `afb530d`（wf baseline save pair 路徑改指 `instance/profiles/baselines`；2026-10-03 再搬到 `.repo/baselines`）、
agentctl commit `b009076`、`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-03/SESSION-LOG.md`（「09-04 使用者裁示」節第 10 題）。
**人工校對層本身已上線**（`modlist.txt:520` 啟用、`:519` 機翻層停用，詳見
[`回家下載／重建`](../home-setup.md) 的已完成節），所以這項剩下的只有「用標準基準重跑一次 smoke」。

**2026-09-25 22:2x 推進**：cx-wu-rt 已把 baseline pair 複製進 `modpack-main/saves/`（SHA 一致）
並用 qa_console 載入（level 1、WhiterunBanneredMare）；**DMK 中文設定頁需使用者自己開 MCM 看**
（agent 不送按鍵，拿不到畫面）。證據同上 REPORT 件 2。
