# Verification

## 離線 gate

`tools/translation_pipeline.py verify` 對精確官方 Final baseline 與精確 CHT seed 驗證：

1. source ESP、source BSA 與 seed archive hash 全部精確吻合；
2. source／output 都有 9,766 records，record 順序、signature、raw FormID、GRUP nesting、flags、
   version bytes、壓縮狀態與 subrecord tag 順序相同；
3. 只有 ledger 列出的 4,071 個 canonical zstring payload 改變，全部可嚴格 UTF-8 解碼；
4. 所有其他解壓後 subrecord payload bytes 完全相同；
5. 六個 PEX 各只有一個既有 display string slot 改變，完整 tail 逐 byte 相同；
6. `<...>`／`%...%`／`$key`／escaped control token 與換行數均保留；
7. 沒有空目標、U+FFFD、`???` 或設定的常見簡體殘字；
8. fresh audited rebuild 與包內 ESP／PEX／ledger 逐 byte／逐值相同；
9. manifest 覆蓋所有 release 檔案（manifest 自身除外）。

## 允許的差異

- ESP：4,071 個 ledgered display zstrings；其中一項包含 `<BribeCost>` → `<bribecost>` 的 token-case
  修正。payload 長度變更只允許連帶更新 record／ancestor GRUP size；若 record 壓縮，壓縮流可重建，
  但解壓後除文字外不得改變。
- PEX：六個既有 string-table slots 的 UTF-8 內容與 length prefix；其餘 slots、header、prestrings 與
  完整 declaration／bytecode tail 不變。

沒有增加、刪除或搬移 record，也沒有改 VMAD、conditions、FormLink、scripts、AI package、voice
path 或 gameplay 數值。

## Runtime 邊界

離線 gate 不取代目標環境的顯示與字幕驗收。Dev profile 後續應抽查一般關係對話、對話選項、任務／
通知，以及 Gelebor／Isran／Valerica 等六條 script 通知，確認無方框、mojibake、空白、截斷、未替換
`<bribecost>` 或新 crash。profile 部署與 runtime 結果不在本 artifact 內維護。
