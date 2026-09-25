## DMK 中文層 smoke 以標準 baseline save 重跑

2026-09-01 的 DMK（**Directional Movement Keys** 1.5.0）smoke 執行時，baseline save pair
不在磁碟上（`7e70ae2` 誤刪，2026-09-02 已於公司復原），因此當時開檔用的不是 `runtime-qa` 規定的固定基準。
回家以復原後的 baseline save pair 重跑一次 DMK 中文層 smoke。
**通過**＝以標準基準開檔，DMK 中文層顯示與 2026-09-01 的結論一致；若不一致，原結論作廢並重驗。

**路徑已變（2026-09-04）**：baseline pair 依使用者 09-04 第 10 題裁示 A 搬到
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/baselines/ModpackKRDev0A.{ess,skse}`
（2026-09-05 實讀該目錄兩檔皆在，2.9 MB／6.2 KB），**不再在 `modpack-main/saves/` 底下**。
證據：`instance/profiles` commit `0f64c20`、母 repo commit `afb530d`（wf baseline save pair 路徑改指 `instance/profiles/baselines`）、
agentctl commit `b009076`、`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/SESSION-LOG.md`（「09-04 使用者裁示」節第 10 題）。
**人工校對層本身已上線**（`modlist.txt:520` 啟用、`:519` 機翻層停用，詳見
[`回家下載／重建`](../home-setup.md) 的已完成節），所以這項剩下的只有「用標準基準重跑一次 smoke」。

**2026-09-25 22:2x 推進**：cx-wu-rt 已把 baseline pair 複製進 `modpack-main/saves/`（SHA 一致）
並用 qa_console 載入（level 1、WhiterunBanneredMare）；**DMK 中文設定頁需使用者自己開 MCM 看**
（agent 不送按鍵，拿不到畫面）。證據同上 REPORT 件 2。

## Modpack-KR Batch 6 final gameplay

自動 lane 21/21 PASS、`load_epoch 1 → 2`、0 new crash 不能代替真人。需驗新遊戲、城市／NPC、~~BFCO~~
**MCO**、Mysticism／Adamant、CT77／~~AVE~~、RDO、VIGILANT Altano 入口／字幕／語音、
自然跨 worldspace、MCM 與 description overlay 書。VIGILANT 四層須同版 1.8.2；Silent Voice 缺口已
接受、不需 TTS。證據見 [`Batch 6 RESULT`](../../agentctl/logs/modpack-kr-final-smoke-2026-08-21/RESULT.md)。

**對象更正（2026-09-05 實讀，清單不刪只改名）**：
- **BFCO → MCO**：2026-09-02 使用者裁示戰鬥框架從 BFCO 移回 MCO 並已施工。
  `/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:407`＝`-BFCO - Attack Behavior Framework 3.100.5`（**停用**）、
  `:403`＝`-BFCO Traditional Chinese 3.100.5 Dev 2026-08-16`（**停用**）；
  現役是 `plugins.txt:864`＝`*Attack_MCO.esp`、`:865`＝`*scar-adxp-patch.esp`，`modlist.txt:404`＝`+SCAR 2.01`。
  所以這條驗的是 **MCO 的輕／重／方向／sprint attack**，不是 BFCO。
- **AVE**：`modlist.txt:620`＝`-Simonrim AVE Constellations Merge 1.5 Dev 2026-08-16`（**停用**）、
  `:457`＝`-Thaumaturgy AVE Patch 1.1 Reference Dev 2026-08-16`（**停用**）。AVE 那半**作廢**，
  CT77 仍在（`:610`／`:613`／`:614`／`:615` 皆 `+`），只驗 CT77。
- Silent Voice 仍在：`modlist.txt:1319`＝`+Fuz Ro D-oh - Silent Voice`。

