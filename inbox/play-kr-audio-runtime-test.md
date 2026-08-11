# 信：接管 MO2／Skyrim 並驗證 Play-KR 環境音

**寄件人**：在 `~/notes` 工作的 Skyrim 部署 agent（依使用者指示轉交）
**回信地址**：不需回信；請把權威結果記回你方現行 SESSION-LOG／驗收紀錄

## 要對方做什麼／要告知什麼

使用者明確將 **MO2 與 Skyrim 的指揮權轉交給 `~/repo/moddings/skyrim` 的 agent**。從收到本信起，請由你方使用既有 agent-bridge MCP、`mo2ctl` 與 QA 工作流接管遊戲／MO2；寄件方不再操作兩者，避免資源衝突。

請驗證目前選中的隔離 profile `Play-KR` 之環境音基線：

- `Regional Sounds Expansion 2.1.0`
- `Reverb Interior Sounds Expansion 1.5.0`（Non-VR；Wind required + Rain + Thunder；Rain／Thunder volume sliders；RSE integration）
- `Acoustic Space Improvement Fixes SkyPatcher 1.3.3`（SkyPatcher main + Reverb compatibility patch）

請先確認 MO2／Skyrim 未被其他 session 佔用，再依你方權威工作流進行短程 runtime 驗收：確認六個 plugin 實際載入、可載入既有測試存檔、能切換／抵達適合的戶外與室內 cell、在相關天候下不出現新 crash／Papyrus／SKSE 錯誤。若 MCP 無法觀測實際音訊，請明確把「主觀聽感」保留為使用者 handoff，不要把穩定性通過誤寫成音質通過。

## 證據／脈絡

- 目前 selected profile：`Play-KR`
- MO2 profile repo：`~/games/mod-organizer-2-skyrimspecialedition/modorganizer2/profiles`
- 安裝 commit：`7a39f37 Install isolated environment audio baseline for Play-KR`
- profile 基線 commit：`a981044 Create isolated Play-KR profile before content installs`
- 壓縮檔：`~/skyrim_mods/hdd/manually/audio-environment-2026-08-11/`
- manifest 已記錄三個原始 archive 的 SHA-256 與手動 materialize 的 FOMOD 選項。
- 安裝後 scoped static gates：load order PASS、check errors PASS、script validation PASS；SKSE inventory WARN 僅因沒有 before-baseline，未報新模組特定錯誤。
- 完整 static report：`/tmp/play-kr-audio-static-gates.json`（若已被系統清掉，以 profile commit 與現場重跑為準）。
- notes 側狀態：`~/notes/projects/modding/skyrim/SESSION-LOG.md`；人耳驗證：`~/notes/WAIT_USER.md`。

六個 active plugin：

1. `Regional Sounds Expansion.esp`
2. `Reverb Interior Sounds Expansion.esp`
3. `Reverb Interior Sounds Expansion_VolumeSlider_Rain.esp`
4. `Reverb Interior Sounds Expansion_VolumeSlider_Thunder.esp`
5. `AcousticTemplateFixes.esp`
6. `AcousticTemplateFixes_ReverbInteriorSounds.esp`

## 完成準則

- agent-bridge／MCP 觀測到六個 plugin 在 runtime 實際載入。
- 測試存檔與至少一個戶外、一個室內場景可正常運作，無可歸因於本批模組的新 crash 或明顯 runtime error。
- 結束時乾淨關閉遊戲／MO2，確認 profile 語意與 git 狀態；若產生合法 MO2 churn，按你方工作流處理。
- 將自動化可證明的結果與仍需使用者人耳確認的部分分開記錄。
