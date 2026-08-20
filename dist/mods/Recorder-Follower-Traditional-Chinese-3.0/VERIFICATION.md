# Verification

## 離線 gate

`tools/translation_pipeline.py verify` 對精確官方 3.0 baseline 驗證：

1. source 與 seed SHA-256 精確符合已記錄版本；
2. source／seed／output 都有 1,380 records，record 順序、signature、raw FormID、GRUP nesting、
   semantic header 與 subrecord tag 順序相同；
3. seed 的 1,429 個差異全部位於可顯示文字 payload，非文字差異為零；
4. output 只有 ledger 列出的 1,429 個 UTF-8 zstring 改變，所有其他解壓後 payload 逐 byte 相同；
5. 所有 token 與換行數保持一致，沒有空 target、U+FFFD 或 `???`；
6. fresh in-memory rebuild 與包內 ESP／ledger 逐 byte 相同。

沒有增加、刪除或搬移 record，也沒有改 VMAD、conditions、FormLink、scripts、AI package、navmesh、
voice path 或 gameplay 數值。

## Runtime 邊界

離線 gate 不替代遊戲內顯示驗收。部署到 `Modpack-KR-Dev` 後仍應抽查 Recorder 的招募／一般對話、
字幕、任務日誌、書籍與通知，確認沒有方框、mojibake、空白、截斷或新 crash；英語配音與 FUZ 不受
本覆寫影響。
