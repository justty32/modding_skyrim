# racemenu／bake-export — 6b 匯出頭

[bake](bake.md)｜[racemenu](README.md)

段 6b：主角套上 preset 後，用 skee 把頭匯出成 NIF＋tint，給 6c 上架。**已實證做法是在 RaceMenu 介面內操作**（2026-11-22 face-pilot-2 S3，Hatak 部件全部正確）。授權同 [README](README.md#授權邊界)：開遊戲、取 desktop／game 鎖、**不存檔**。

## 做法（已實證）

工具：`agentctl/tools/menu_drive.py`（鍵鼠操作細節見 [menu-drive](../runtime-qa/menu-drive.md#racemenu-一輪主角套-preset-並匯出頭)）。F5／F9 必帶 `--require-menu "RaceSex Menu"`，選單沒開就拒送，免得變成快存／快讀。

1. `/console showracemenu` → `wait-menu "RaceSex Menu" --open`。
2. **Sliders 分頁點種族**：先點別的種族，再點回目標種族，強制重建頭。
3. **Presets 分頁** → F9 載 preset → `aim` 點 preset 檔名。
4. **Sliders 分頁把「體型」（weight）滑桿調到目標 NPC 最終體重÷100**（`--keep-weight` 用 NPC 原值，否則用 preset 的 weight）。每按一次 Right 動 0.01；Muiri 是 100 → 1.00，按 100 下。**不調會有脖縫**：匯出頭的脖子照匯出當下主角的體型烤（runtime-3 A1–A4，見 [lessons](../../lessons/faces-racemenu-runtime.md#facegen-neck-seam-export-weight)）。
5. **Sculpt 分頁** → F5 Export Head → Return。頭檔落在 overwrite 的 `SKSE/Plugins/CharGen/Head_<日期>.nif|.dds`。
6. 關 RaceMenu，不存檔。匯出檔先複製到 staging（附 SHA256SUMS），原檔搬出 overwrite。

匯出後**先**讀 NIF 的 shape 名（`npc_face/nifio.py`）對 preset 的部件，再交給 `build_layer`／`facegen_install`。`build_layer` 要帶 `--export-weight W`（第 4 步的滑桿值×100，0–100）：NPC 最終 NAM7 和它差超過 0.5 就 FAIL（`deployable=false`），不帶只留 WARN「無法檢查脖縫」。

## 為什麼以前失敗

根因：**用主控台 `setrace`／`sexchange` 改主角之後，頭 3D 不重建**。之後不論用 Papyrus（`LoadPreset`／`LoadCharacter`）或在 UI 載 preset，匯出的都是舊部件。證據：runtime-pilot 場 2–5，加上 face-pilot-2 S1–S2。face-pilot-2 S3 另外否定了「關選單時才重建」：在 RaceMenu 內按 F5 匯出也一樣是舊件，直到改成 UI 點種族才對。換性別仍可先用主控台 `sexchange`，只要之後在 UI 點一次種族（runtime-3 A3 實證）。細節見 [lessons](../../lessons/faces-racemenu-runtime.md#racemenu-export-head-parts-not-applied)。

## 耳朵等多餘 shape

- Goam 精靈耳把耳朵做成女性可選的 Facial Hair 類 HDPT。UI 換種族時，RaceMenu 把這個滑桿設成第一件，匯出頭就多掛一個 shape（例：`GoamElvenEarsBreton`）。
- UI 裡拿不掉：「面部毛髮」只有 Goam 耳朵各款和 `00`，沒有「無」（S4）。
- 離線刪：`build_layer.py`／`facegen_install.py` 加 `--drop-shape <shape名>`（可重複），連同只屬於該 shape 的 block 一起刪並重編 ref；不能刪期望清單內的部件。
- 要不要刪由人判斷：preset 的 jslot 本來沒有這件就刪（Hatak 就是）。

## 舊紀錄（歷史）

2026-11-22 runtime-pilot 4 場走觸發 ESP＋Papyrus：主控台 `sexchange`／`setrace` → `LoadPreset`／`LoadCharacter` → `ExportHead`。每場都出檔，但頭部件是原主角（或 `coc` 新角色的種族預設件），一件 Hatak 部件都沒上。當時真因未定位，現已查明是上面的根因。

觸發 ESP 路線（`npc_face/trigger/`，含 v4「只匯出」開關）**已被 UI 路線取代，保留作備援**；收回流程見 trigger README，每輪 `layer_apply --revert` 逐位元組還原。
