# runtime-qa — 實機驗收

要真的把遊戲跑起來才能確認的事。QA harness 與歷史證據在
[`agentctl/qa/`](../../../agentctl/qa/)（specs／reports／baselines／fomod-choices）。

```text
Done when: <指定條數逐條有證據、鎖已釋放、profile 無殘留、結論寫進對應 log>
```

## 0. 先確認可以拿資源

**取得順序固定：先桌面 HID 鎖，再遊戲鎖。** 跑 Skyrim 一定佔螢幕，反過來拿會跟
同時持鎖的另一條我方線死鎖。細節見 [`agentctl/docs/resource-locks.md`](../../../agentctl/docs/resource-locks.md)。

**使用者在電腦前時，鍵鼠螢幕的控制權全歸他**——這時候連鎖都不要拿。
（Aetheria agent 2026-08-27 起凍結，跨 agent 優先權條款停用；`desktop.lock` 現在只是我方線之間的 mutex。）

**坑**：遊戲鎖曾指向隨 agent 線封存而刪除的 `~/skyrim_agent_out/_lock/`，使「已釋放遊戲鎖」
恆真通過；現在鎖在 `agentctl/.lock/`，**檢查一個不存在的東西永遠會過。**

## 1. 啟動

**一律從 Steam 點 Skyrim SE**，不手動開 MO2。`SkyrimSELauncher.exe` 已換成 proxy shim，
會開出 MO2 GUI 由使用者按 Run。啟動前確認 `ModOrganizer.ini` 的
`selected_profile` 是 `modpack-main`（該檔是 **CRLF**，用 sed 改要帶 `\r`）。

無人值守走 `mo2ctl launch --background-active`：它暫設 profile `skyrim.ini` 的
`bAlwaysActive=1` 讓失焦時仍能載入，`mo2ctl kill` 會以原始 bytes 還原。

## 2. 基線與證據窗

- **固定 baseline save**：`modpack-main/saves/ModpackKRDev0A.{ess,skse}`，成對且 SHA-256 不變。
  它是唯一由 git 追蹤的存檔，其餘存檔是執行期資料。
- **fresh log window**：每組驗收各自開新的 log 窗，`load_epoch` 要真的遞增。
  工具是 `agentctl/tools/{runtime,skse}_log_window.py`。
- **一次只驗一組**。D3／D4 這類各自需要獨立的 fresh window，
  **無關的錯誤不得順手宣稱已解**。

## 3. 條數寫死

**驗收條數要在開始前寫死。** 「以及其他你認為必要的驗證」等於讓執行線為了保險亂跑，
燒光 token 還交不出東西。

**別把「跑完了」當成「通過了」：曾有回報全 PASS，但 log 只有 2 個 commit、需要 ≥13 個，
三條驗收項的關鍵字出現 0 次，實際活動只有 75 秒。逐條對證據，不要對自我宣告。**

## 4. Teardown

- 兩個鎖都釋放（`~/shared_agent_locks/` 與 `agentctl/.lock/` 應為空）
- 沒有殘留的 `ModOrganizer.exe`／`SkyrimSE.exe`——用 `pgrep -f '[S]kyrimSE\.exe'`
  這種括號寫法，否則會匹配到執行檢查的 shell 自己
- `instance/profiles` 的 **profile 結構稽核**通過（命令見該 repo `tools/README.md`）
- `selected_profile` 沒被留下臨時 profile 名（codex 線做過這件事）
- 結論寫進 `agentctl/logs/`，證據 JSON 進 `agentctl/qa/reports/`

## AI 能對遊戲做什麼

鍵盤 ✅（`xdotool --clearmodifiers` 對 XWayland，或 `sendkey.c` 在遊戲的 wineserver 內
`SendInput`）、主控台與狀態查詢 ✅（AgentBridge）、截圖 ✅（`spectacle -b -n -f -o out.png`，
**唯一可用的**）、load order 資料層 ✅（houseCARL）、**滑鼠 ✅ 有條件**。

**滑鼠（2026-08-27 重測）**：`xdotool mousemove`／`click` 在**有 XWayland 視窗持有焦點**時
可操作 MO2／Skyrim，需要滑鼠的驗收不必一律推給使用者；焦點落到原生 Wayland 視窗就失控，
可用 `QT_QPA_PLATFORM=xcb konsole` 奪回。`ydotool` 仍然不用：daemon 要寫 `/dev/uinput`，
sudo／改 group／改 udev 都是紅線。

實測過的完整能力表與工具限制在
[`agentctl/docs/resource-locks.md`](../../../agentctl/docs/resource-locks.md#這台機器的-hid-實況2026-08-27-重測取代-2026-08-23-版)；
能力總表在 [`agentctl/README.md`](../../../agentctl/README.md)。

## 何時不用

- 靜態就能證明的（record 拓撲、hash、winner 判定）→ 別開遊戲，用 houseCARL 靜態查。
- 要人眼判斷畫面（方框、mojibake、手感）→ 那是使用者的事，記到
  [WAIT_USER.md](../../../WAIT_USER.md)，不要自己宣稱通過。
