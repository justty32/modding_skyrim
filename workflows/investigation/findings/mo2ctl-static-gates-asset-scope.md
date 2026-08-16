# mo2ctl static-gates 的 asset scope 與零輸出假象

日期：2026-08-16

## 結論

`mo2ctl static-gates --asset <path>` 不是只執行 asset resolver。它固定先依序呼叫：

1. `housecarl_load_order_status`
2. `housecarl_check_errors`
3. `housecarl_skse_inventory`
4. `housecarl_validate_scripts`
5. 最後才是 `housecarl_asset_status`

`--mod` 只供 lookup／crash attribution，不會縮小前四項的 plugin scope。若沒有同時傳
`--plugin`，check-errors 與 validate-scripts 會掃完整 load order；stdio client 又以 blocking
`readline()` 等待單一 tool 回覆，中間沒有 progress 或 per-tool timeout，因此表面上會像 asset
resolver 卡死。

## 2026-08-16 重現

對 `Scripts/NiOverride.pex` 直接呼叫 `housecarl_asset_status`：

- 0.48 秒完成；
- winner 是 `RaceMenu NiOverride Signature Patch 0.4.20.0 Dev 2026-08-16` loose file；
- provider chain 是該 loose file > `RaceMenu.bsa`。

改用 `static-gates --plugin RaceMenu.esp --asset Scripts/NiOverride.pex`：

- 4.79 秒完成；
- load order：pass；
- `RaceMenu.esp` FormLink／missing-master：pass；
- asset winner：pass；
- script gate 重報 RaceMenu 原本 4 個由 runtime 填入的 properties，與 NiOverride PEX override
  無關。

先前兩次只傳 `--asset`（其中一次另傳 `--mod`）超過 90 秒且零輸出，原因是完整 load-order
script sweep 尚未回覆，asset tool 當時根本還沒有被呼叫。

## 現行安全用法

- 驗單一 mod 的 asset 時，同時傳它的代表性 `--plugin`，避免不必要的全量 script sweep。
- 沒有 plugin 的純資產／script-only mod，選其上游 provider 的小型 plugin 作 scope；本例使用
  `RaceMenu.esp`。
- 遇到零輸出時，先用單一 `HousecarlClient.call_tool()` 隔離目標 tool，再判斷是哪一層慢；不要把
  整條 composite command 的等待時間歸因於最後一項 gate。

## 可選工具改善

若日後要開 feature 工作，可為 `static-gates` 加 per-tool progress、timeout 與 `--only`／`--skip`
選項。現階段已有不改行為的可靠操作方式，不在本次調查直接修改工具。

來源位置：

- `projects/agent-bridge/client/mo2ctl.py:641`：固定 default tool specs。
- `projects/agent-bridge/client/mo2ctl.py:660`：依序執行每個 tool。
- `projects/agent-bridge/client/mo2ctl.py:596`：blocking `stdout.readline()`。
- `projects/agent-bridge/client/mo2ctl.py:2225`：`--asset` CLI 參數。
