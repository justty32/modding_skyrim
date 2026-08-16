# Verification

## 已完成的離線 gate

`tools/translation_pipeline.py verify` 對精確官方 4.2.2 baseline 驗證：

1. ESP source 與官方 BSA hash 完全吻合；
2. source／output 都有 5,708 records，record 順序、signature、raw FormID、GRUP nesting、flags、
   version bytes、壓縮狀態與 subrecord tag 順序完全相同；
3. 只有 ledger 列出的 1,794 個 canonical zstring payload 改變；所有其他解壓後 subrecord raw bytes
   完全相同；
4. 1,794 個 target 全部可嚴格 UTF-8 解碼，沒有 U+FFFD、`???` 或常見簡體殘字；
5. 官方與簡中 PEX 都有 128 個 string-table slots；只有 18 個顯示字串不同，slot index 不變；
6. PEX string table 後方 3,986 bytes 的宣告、properties、control flow 與 bytecode 逐 byte 相同；
7. fresh in-memory rebuild 與包內 ESP／PEX 逐 byte 相同；
8. manifest 覆蓋所有 release 檔案（manifest 自身除外）。

## 允許的差異

- ESP：1,794 個 ledgered text payload，以及 payload 長度改變必須連帶更新的 record／ancestor GRUP
  size；壓縮 record 會以 zlib level 9 重建壓縮流，但解壓後除文字外不得有任何差異。
- PEX：18 個既有 string-table slot 的 UTF-8 內容與其 length prefix；其餘 slot 與完整 tail 不變。

沒有增加、刪除或搬移 record，也沒有改 VMAD、conditions、FormLink、scripts、AI package、navmesh、
voice path 或 gameplay 數值。

## Runtime 邊界

- 離線 gate 不確認目前 Proton／`sLanguage=ENGLISH` 是否能正常顯示 inline UTF-8。
- 對話選項、字幕、任務日誌、書籍與 Lydia MCM 仍需在目標環境抽查方框、mojibake、截斷與排版。
- profile 部署與 runtime 驗收屬機器專屬狀態，不在本 artifact 內維護。

因此這份 artifact 的結論是「離線可證明 behavior-preserving 的正體文字覆寫」，不單憑本資料夾
宣稱任何目標機器已完成 runtime 驗收。
