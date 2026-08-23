# runtime-qa — 實機驗收

要真的把遊戲跑起來才能確認的事。QA harness 與歷史證據在
[`agentctl/qa/`](../../../agentctl/qa/)（specs／reports／baselines／fomod-choices）。

```text
Done when: <指定條數逐條有證據、鎖已釋放、profile 無殘留、結論寫進對應 log>
```

## 0. 先確認可以拿資源

**取得順序固定：先桌面 HID 鎖，再遊戲鎖。** 跑 Skyrim 一定佔螢幕，反過來拿會跟
Aetheria agent 死鎖。細節見 [`agentctl/docs/resource-locks.md`](../../../agentctl/docs/resource-locks.md)。

**使用者在電腦前時，鍵鼠螢幕的控制權全歸他**——這時候連鎖都不要拿。
跨 agent 的優先權是 **Aetheria 優先**，對方要用就盡快釋放，不爭論。

**坑**：遊戲鎖曾經指向 `~/skyrim_agent_out/_lock/`，該目錄隨 agent 線封存被刪除，
於是每次「已釋放遊戲鎖」的檢查都在檢查一個**不可能存在的路徑，恆真通過**。
現在鎖在 `agentctl/.lock/`——但這個教訓要記著：**檢查一個不存在的東西永遠會過。**

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

**別把「跑完了」當成「通過了」。** 一次實例：回報全 PASS，但 log 只有 2 個 commit、
需要 ≥13 個，其中三條驗收項的關鍵字出現 **0 次**，實際活動只有 75 秒。
**逐條對證據，不要對自我宣告。**

## 4. Teardown

- 兩個鎖都釋放（`~/shared_agent_locks/` 與 `agentctl/.lock/` 應為空）
- 沒有殘留的 `ModOrganizer.exe`／`SkyrimSE.exe`——用 `pgrep -f '[S]kyrimSE\.exe'`
  這種括號寫法，否則會匹配到執行檢查的 shell 自己
- `python3 instance/profiles/tools/check_profiles.py` 通過
- `selected_profile` 沒被留下臨時 profile 名（codex 線做過這件事）
- 結論寫進 `agentctl/logs/`，證據 JSON 進 `agentctl/qa/reports/`

## AI 能對遊戲做什麼

鍵盤 ✅（`xdotool` 對 XWayland，或 `sendkey.c` 在遊戲的 wineserver 內 `SendInput`）、
主控台與狀態查詢 ✅（AgentBridge）、截圖 ✅（`spectacle`）、
load order 資料層 ✅（houseCARL）、**滑鼠 ❌**（兩條路徑都不通，這是唯一缺口）。
完整表在 [`agentctl/README.md`](../../../agentctl/README.md)。

## 何時不用

- 靜態就能證明的（record 拓撲、hash、winner 判定）→ 別開遊戲，用 houseCARL 靜態查。
- 要人眼判斷畫面（方框、mojibake、手感）→ 那是使用者的事，記到
  [WAIT_USER.md](../../../WAIT_USER.md)，不要自己宣稱通過。
