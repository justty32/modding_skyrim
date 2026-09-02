# Creation Kit Platform Extended（CKPE）— Tool Survey Finding

**Source**: https://github.com/Perchik71/Creation-Kit-Platform-Extended

**Surveyed**: 2026-09-02（本地 shallow clone；僅 README、`.gitmodules`、TOML 與既有指南快照）

## 一句話結論

**可直接用於穩定／加速 facegen 的 CK GUI 工作流，SSE 預設已設 1024 tint mask；但 CKPE 不提供無頭批次層，且 AE 1.6.1170 對應 CK 版本仍須驗證。**

## 支援版本與修正範圍

README 明示 CKPE 支援 Skyrim Special Edition、Fallout 4、Starfield；同句提到 SSE CK 1.5.73
Unicode patch 是它的前身，不能據此推定現版仍支援 1.5.73
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/README.md:42`）。安裝段把各遊戲的實際支援表
外連到 Wiki `#brief`，本次離線資料沒有該表
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/README.md:62`）。

SSE 設定檔可確認的分界只有 `1.6.1130`：`bSupportFormat171=true` 讓早於 1.6.1130 的 editor
支援新 plugin format 與 compact form indexes
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/Stuffs/SSE/CreationKitPlatformExtended.toml:34`）；
另一項註解另稱 LIP debug output 在 1.6.1130 及以後不作用
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/Stuffs/SSE/CreationKitPlatformExtended.toml:26`）。
這不足以確認 game 1.6.1170（AE）對應 CK 1.6.1130 或其他版本，故不猜測。

設定項顯示的主要修正／擴充範圍如下：

#### 載入速度

`bSkipTopicInfoValidation=true` 跳過 topic info validation，加快 plugin 初載，註解也標為
建議的 crash fix（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/Stuffs/SSE/CreationKitPlatformExtended.toml:20`）。

#### facegen

DDS 自動壓縮由 `bAutoCompressionDDS=true` 控制
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/Stuffs/SSE/CreationKitPlatformExtended.toml:68`）；
匯出格式與解析度另見下一節。

#### 多執行緒

`bThreads=true` 啟用 thread management，並把 CPU 限到 85%，避免其他程式卡頓
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/Stuffs/SSE/CreationKitPlatformExtended.toml:15`）。

#### UI

`bUIHotkeys=true` 開放部分視窗快捷鍵重綁；另有 classic／dark theme
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/Stuffs/SSE/CreationKitPlatformExtended.toml:8`、
`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/Stuffs/SSE/CreationKitPlatformExtended.toml:23`）。

#### 崩潰／卡死

`bRefLinkGeometryHangWorkaround` 處理書架或選 Enable State Parent 時的 CK hang
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/Stuffs/SSE/CreationKitPlatformExtended.toml:11`）；
`bOverlapsGenerateONAM` 替換 ONAM 生成法，註解建議在存 `.esm` crash 時啟用
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/Stuffs/SSE/CreationKitPlatformExtended.toml:30`）。

## facegen 相關設定

SSE preset 的實際值是 `uTintMaskResolution=1024`，作用是把匯出 texture 設為 N×N 解析度
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/Stuffs/SSE/CreationKitPlatformExtended.toml:74`）。
因此 Animonculory 快照所建議的「由 512 改成 1024」在這份 CKPE TOML 已經滿足，不必再改；指南原文位置為
`modpack-design/sources/animonculory-modding-resources-2026-09-02/facegen-regeneration-ck.md:32`。

附近的預設匯出策略是 `bDisableExportDDS=false`、`bDisableExportTGA=true`、
`bDisableExportNIF=false`：DDS tint 與 NIF geometry 會匯出，TGA tint 不匯出
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/Stuffs/SSE/CreationKitPlatformExtended.toml:71`、
`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/Stuffs/SSE/CreationKitPlatformExtended.toml:72`、
`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/Stuffs/SSE/CreationKitPlatformExtended.toml:73`）。
另有 `bDisableAutoFaceGen=true`，預設阻止「存 plugin 時自動建立」facegen；這不等於封鎖使用者手動匯出
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/Stuffs/SSE/CreationKitPlatformExtended.toml:70`）。

## 建置與授權

README 的 Compilation 流程是用 Visual Studio 2022 或更新版開 project，建置 `Release` 或
`Release-NoAVX2`，再把輸出放到 game directory
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/README.md:69`、
`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/README.md:71`）。

自 v0.6／commit `9d93970cc3918099c895872d46a24aa29a34db11` 起為 LGPLv3；更早版本為 GPLv3
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/README.md:85`、
`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/README.md:87`）。README 另警告 FO4 resources pak
與 `d3dcompiler` 內容含 proprietary、未授權檔案；若借用資產須避開
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/README.md:89`）。

## 無頭／腳本化可行性

**CKPE 本身不提供無頭模式，它只是穩定／加速 CK GUI。** 本次允許範圍內沒有找到 SSE facegen 的
command-line、batch 或 headless 介面；README 只要求讓 `ckpe_loader.exe` 與 `CreationKit.exe` 同目錄
（`analysis/tool-survey/repos/Creation-Kit-Platform-Extended/README.md:64`）。

我方指南同樣是 GUI 流程：從 MO2 選 CK 後按 Run、在 Object Window 選 Actors，再按 Ctrl+F4 並確認對話框
（`modpack-design/sources/animonculory-modding-resources-2026-09-02/facegen-regeneration-ck.md:59`、
`modpack-design/sources/animonculory-modding-resources-2026-09-02/facegen-regeneration-ck.md:66`、
`modpack-design/sources/animonculory-modding-resources-2026-09-02/facegen-regeneration-ck.md:75`）。
所以「agent 批次重生成」仍缺可可靠操作 GUI 的自動化層，或另一個有正式批次介面的 facegen exporter。

## 可借的概念／可行的下一步

若要做整包 facegen，應把 CKPE 裝進 CK 環境：它直接改善 plugin 初載、多執行緒資源管理、已知 hang／save
crash，並把 SSE tint mask 預設到 1024；指南本身也把 CKPE 列為必要工具
（`modpack-design/sources/animonculory-modding-resources-2026-09-02/facegen-regeneration-ck.md:22`）。

安裝 CKPE 解決的是「CK GUI 較穩、較快、匯出設定合理」，不解決工作編排。可行下一步是先取得 Wiki 的
CK 版本對照，對目前釘版挑相符 release，再於 modlist 定案後依指南準備 Synthesis loader plugin 與 CK Output；
若一定要無人值守，另立小型可恢復的 GUI automation／結果核對層，不能把 CKPE 當成自動化 API。

## 沒查到／需驗證的事

- 外部 Wiki `#brief` 的完整 game／CK／CKPE 版本矩陣未查；game 1.6.1170 對應 CK 1.6.1130 或其他 build
  **找不到，待查外部 Wiki**。
- 未開 GUI、未 build，故尚未用我方實際 CK build 驗證 loader、穩定性、1024 輸出與三個 export toggle。
- 允許文件中未找到 SSE facegen 無頭模式證據；這能支持目前採 GUI 路線，不能證明未公開介面絕對不存在。
