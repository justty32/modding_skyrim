# SkyrimSE-Linux-Modding 指南快照

## 1. 一句話結論

這份指南對現行 Manjaro＋MO2 只有「固定使用同一 Proton、留意大小寫、音效故障可從 AppID prefix 查起」仍可借；其核心是 2019 年的 Proton 3.16-4＋Wrye Bash／直接安裝路線，且自己標成過時，沒有 MO2 或 ENB 作法，不值得照單再深挖。

## 2. 指南涵蓋範圍摘要

#### Proton

要求 Steam Play `3.16-4`，另裝名為 `skyrim-proton` 的本機 compatibility tool，並警告不要混用 Proton 版本。`install_proton.sh` 只是把 release 內的 `skyrim-proton.zip` 解到 `~/.steam/root/compatibilitytools.d/`；`Tools/patch_proton.sh` 才會備份並以 `bbe` 改 Proton 3.16 的 `ntdll.dll.so` 位元組。來源：`README.md:18-25,37-55,60`、`install_proton.sh:2-7`、`Tools/patch_proton.sh:3-14`。

#### MO2／模組管理

沒有 MO2 教學；只寫直接複製到 `Data`，或以 Wine 跑 Wrye Bash 做安裝、排序、啟用。來源：`README.md:29-34`。

#### SKSE／Windows 工具

先以 Steam launch option 開 terminal，再從同一個自訂 Proton 執行 `skse64_loader.exe`；進主選單用 `getskseversion` 確認，SSEEdit／Wrye Bash 也沿用同一 Proton。這是處理 `.exe` 啟動與 prefix 一致性的舊方法。來源：`README.md:37-49,58-62`。

#### ENB

repo 沒有 ENB、DXVK wrapper、ReShade 或替代方案的文字；不能由這份指南推出 Linux ENB 支援結論。

#### 音效

`install_audio.sh` 對 AppID `489830` 的 prefix 執行隨 release 附帶的 FAudio setup；README 另建議失聲時重做，或用 winetricks 切 ALSA／PulseAudio。來源：`install_audio.sh:2-4`、`README.md:20-25,53-54,65-67`。

`uninstall.sh` 只移除 `compatibilitytools.d/skyrim-proton`，沒有回復音效 prefix 或 `patch_proton.sh` 改過的 Steam Proton 檔案；來源：`uninstall.sh:2-5`。

## 3. 與我方 runbook 的差異表

比較這份指南跟我們現行 Manjaro＋MO2 runbook 在五個主題上的做法差異。已抽到 [linux-modding-diff.json](linux-modding-diff.json)（5 列）。

欄位：`主題`（比較項目）、`指南怎麼做`（原文做法）、`我們現況怎麼做`（現行 runbook／launch-mo2.sh 做法）、`差異評估`（可借或不可借的結論）。

統計：5 列，全部「過時但部分原則可借」。

## 4. 可借的坑／設定

#### 不要混跑 Proton

指南說切換版本可能重設內容，工具與遊戲應走同一版本（`README.md`「Good To Know」）。我方已有更強的 prefix 版本硬 gate，可保留這條作判讀原則，不採它指定的版本。

#### 大小寫會造成靜默缺檔

指南點出 `textures`／`Textures` 不一致（`README.md`「Basic Modding」）；我方 runbook 已記 houseCARL 的 `Scripts`／`scripts`、`Seq`／`SEQ` 與 `Skyrim.ini`／`skyrim.ini` 案例，屬同一類但涵蓋不同層。

#### 失聲修法有副作用史

指南記 Proton 4.2-3 補 FAudio 後，過 loading screen 可能整段無聲（`README.md`「Why not 4.2-3?」）；所以不能把 `install_audio.sh` 當通用初始化。

#### 舊版 DynDOLOD 限制

它記 DynDOLOD 2.59 的 Texconv 在 Wine 下壞掉，只能避開 tree LOD texture 並輸出未壓縮格式（`README.md`「Good To Know」）。這是版本限定的歷史坑，不直接套到現行工具鏈。

#### 退出掛住

作者記 Skyrim 偶爾退出後不結束（`README.md`「Good To Know」）；可作症狀提示，但沒有可移植的根因或可靠修復。

## 5. 授權

repo 根目錄有 `LICENSE`，是 MIT License，copyright 2019 spooknik；允許使用、複製、修改、合併、發布、散布、再授權與販售，但散布副本或實質部分時須保留 copyright 與授權聲明，且不附保證。來源：`LICENSE:1-21`。

## 6. 沒查到／需驗證的事

- README 首段明說指南部分過時，改推 GloriousEggroll builds；快照 HEAD `86857b1` 的最後提交時間是 `2020-07-24T15:28:03+02:00`。因此 Proton 3.16-4、ntdll 位元組 patch、FAudio 19.02 與 winetricks 音效設定是否適用 Proton 9 均未證實。
- 沒有 MO2、ENB、現代 SKSE Address Library／runtime pin、SteamLinuxRuntime 或 Manjaro 特有步驟。
- `install_proton.sh` 預期 `skyrim-proton.zip`、`install_audio.sh` 預期 `faudio-19.02/`，兩者都不是 repo 追蹤檔；只從 release 資產取得，這份 clone 無法單獨重建內容。
- `patch_proton.sh` 的三組 byte pattern 沒有版本檢查，除指定 Proton 3.16 外不可推定可移植；指南也沒有說 patch 失敗或只命中部分 pattern 時怎麼辨識。

