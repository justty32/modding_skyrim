# Follower Dialogue Expansion - Jenassa：approval 靜態接點

內容型隨從對話擴充，作者 Anbeegod；公開來源是 [Nexus 120255](https://www.nexusmods.com/skyrimspecialedition/mods/120255)。本筆記固定研究本機 v8.0，非最新版追蹤。作者頁面與 changelog 描述 approval、romance、同行與環境對話；公開功能聲明不等於已逐條驗證。來源查證紀錄：private `agentctl/handoffs/home-2026-11-02/resume-parked/living-fde/REPORT.md:19–21`。

## 一條確證的 producer → GLOB → consumer

本機 `FDE Jenassa.esp` 的 QUST `0008F2`（`aaJenassa2`）VMAD 掛接 `aaJenassaApprove`，其 property `aaJenassaApproval` 指向同 plugin 的 GLOB `000B4B`。這是 quest-level producer，不能改稱 INFO／TIF producer。

單一原作者 PEX `aaJenassaApprove.pex` 的 `OnUpdateGameTime` 檢查 `HirelingJenassaRef.IsInFaction(CurrentFollowerFaction)`，成立則對 approval 執行 `Mod(1)`。不論是否符合 faction，該 event 最後都以 `RegisterForSingleUpdateGameTime(24)` 註冊下一次更新。同一腳本的 `ap(int modifier)` 亦會修改 approval 並依正負顯示訊息；其 caller 未追。首次 timer 由誰排程未證，不能由這段靜態程式宣稱每位玩家已實際開始累加。

真 consumer 為 INFO `00098E:FDE Jenassa.esp`：Mutagen 將 CTDA 解為 `GetGlobalValue`、`GreaterThanOrEqualTo`，讀取 approval `000B4B`，比較值為另一 GLOB `000B5B`（`aaJenassaAppThreshold3`，值 -2）。因此條件是 **approval >= threshold(-2)**，不是按名稱推測的門檻演算法。該 INFO 還有其他 AND gates（另一 global == 2、quest completed == 1、faction == 1）；approval 初值 0 已滿足 -2，不能說 +1 才新解鎖這條台詞，也不能把單一 gate 成立當成整條台詞必播。

以上是本機實作的靜態閉環；精確 VMAD／CTDA、解碼方法與私有證據保留於 `agentctl/handoffs/home-2026-11-02/resume-parked/living-fde/APPROVAL-PROOF.md:9–11`（單一 PEX 的 `OnUpdateGameTime`；consumer overlay 輸出），不在公共筆記複製完整反編譯 PSC 或原資產。

## Living Adventurers 可對照的範圍

可借鏡的是「獨立關係 GLOB → 明確修改者 → 另一 threshold GLOB 作比較值」。Living 已有 per-NPC Favor GLOB／SetGlobal Delta，及使用 Deeds 的 GetGlobalValue gate，來源 `projects/ModForge/src/ModForge.Core/Macros/Generator.LivingNpcs.cs:173–195`；本次未證其條件 spec 可直接表達 global-to-global comparison。這不等於 FDE 與 Living 可直接互連、可共管招募，也不是離場冒險模擬的證據。

本文不把 FDE 人格、timer、faction contract 或 threshold 數字轉成 YUA 設計；其餘 approval 加減事件、防重、cooldown、完整對話路徑與 runtime 行為未驗。Living 對照的證據邊界見 private `agentctl/handoffs/home-2026-11-02/resume-parked/living-fde/APPROVAL-PROOF.md:13`。
