# runtime-qa／menu-drive — agent 操作遊戲內選單

[runtime-qa](README.md)｜[WORKFLOWS](../../WORKFLOWS.md)

AgentBridge 的 `input_tap` 在選單裡不派送，所以主控台以外的選單（Esc、日誌、MCM、RaceMenu）以前都做不到。2026-11-22 face-pilot-2 實測：Skyrim 是 XWayland 視窗，**持有焦點時 `xdotool` 送的鍵盤會進遊戲；滑鼠只吃相對位移**。工具是 `agentctl/tools/menu_drive.py`（[tool-index](../../../agentctl/docs/tool-index.md)「遊戲內選單操作」列）。

**授權**：送按鍵＝會搶輸入。只在使用者不在電腦前、或他當場同意時用；每一次送輸入前工具都會檢查焦點是遊戲視窗、游標沒被別人動過，不過就停（exit 4）。發現有人在用鍵鼠：停手、正常收尾、回報。

## 能力矩陣

已抽到 [menu-drive.json](menu-drive.json)（15 列）。欄位：

- `op`：操作。
- `status`：可行／不可行／部分。
- `method`：用哪個子命令、按哪個鍵、點哪裡。
- `verify`：怎麼確認做到了（`menus_open` 或截圖）。
- `success`：實測成功次數。
- `latency`：每步耗時。
- `notes`：坑與座標。

統計：可行 12、部分 1、不可行 2。

## 做法要點

- **開關選單用 `menus_open` 驗**：AgentBridge `/state` 的 `game.menus_open` 列出所有開著的選單（`Console`、`Journal Menu`、`RaceSex Menu`、`MessageBoxMenu`…），比截圖可靠；`wait-menu` 就是輪詢它。選單**裡面**的狀態（哪個分頁、滑桿數值、MCM 值）只能截圖讀。
- **滑鼠一律用 `aim`**：遊戲游標不跟絕對座標。`aim` 先把 X 指標放回螢幕中央（這一步遊戲游標不動），再送大量負位移把遊戲游標推到左上角歸零，最後用相對位移走到目標。增益在 1920×1080、本機設定下約 1.52。
- **自己用原生 `xdotool` 動過滑鼠後要 `rebase`**，否則下一次送輸入會被「游標被別人動過」擋下（這是刻意的）。
- **F5／F9 是快存／快讀**：在 RaceMenu 裡分別是 Save Preset／Load Preset（Presets 分頁）或 Export Head／Import Head（Sculpt 分頁）。工具要求 `--require-menu "RaceSex Menu"`，選單不在就拒送。
- **日誌系統分頁預設選中「快速存檔」**：在那裡按 Enter／E 會存檔。只用 `aim` 直接點要的項目。
- **MessageBox 用 AgentBridge**：`select_message_box(index=…)` 比按鍵穩，且能先讀訊息內容與按鈕文字再選。
- **截圖**：`shot` 先走 AgentBridge `/screenshot`（只拍遊戲畫面，不受其他視窗遮擋），失敗才退 spectacle。看細節用 `crop --scale`。

## RaceMenu 一輪（主角套 preset 並匯出頭）

已實機（face-pilot-2 S3）：

1. `/console showracemenu` → `wait-menu "RaceSex Menu" --open`。
2. 要換種族：Sliders 分頁 → 種族類別 → `aim` 點種族名（先點別的種族再點回來，強制重建頭）。**不要用主控台 `setrace`**，原因見 [lessons](../../lessons/faces-racemenu-runtime.md)。
3. Presets 分頁 → `key F9 --require-menu "RaceSex Menu"` → `aim` 點 preset 檔名。
4. Sculpt 分頁 → `key F5 --require-menu "RaceSex Menu"` → `key Return`，頭檔落在 overwrite 的 `SKSE/Plugins/CharGen/Head_<日期>.nif|.dds`。
5. `key r` → `select_message_box(index=0)` → `key Return` 關閉。不存檔。

## 不做的事

- 不改 MCM 值、不改遊戲設定選單（離開設定選單會把 prefs 寫回 ini）。
- 不在系統分頁按確認鍵；不送 F5／F9 到沒開 RaceMenu 的遊戲。
- 使用者在電腦前且沒同意時不送任何輸入。
