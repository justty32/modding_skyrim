# Verification

## 離線 gate

`tools/translation_pipeline.py verify` 對精確官方 2.51 baseline 驗證：

1. source ESP／BSA 與 seed ESP／8 PEX 的 SHA-256 全部精確符合；
2. source／seed／output ESP 都有 1,742 records，record 順序、signature、raw FormID、GRUP nesting、
   semantic header 與 subrecord tag 順序相同；
3. seed ESP 的 1,665 個差異全部位於顯示文字 payload，非文字差異為零；
4. output ESP 只有 ledger 列出的 1,665 個 UTF-8 zstring 改變，其他解壓後 payload 逐 byte 相同；
5. 8 個 PEX 的 header、prestrings、string count 與完整 declaration／properties／control-flow／
   bytecode tail 與官方來源相同，只改 105 個 ledgered string-table slots；
6. 所有 token 與換行數保持一致，沒有空 target、U+FFFD 或 `???`；
7. fresh in-memory rebuild 與 packaged ESP／PEX／ledger 逐 byte 相同。

沒有增加、刪除或搬移 record，也沒有改 VMAD、conditions、FormLink、scripts 綁定、AI package、
navmesh、voice path 或 gameplay 數值；PEX 沒有改任何 executable bytecode。

## Runtime 邊界

離線 gate 不替代遊戲內顯示驗收。部署到 `Modpack-KR-Dev` 後應抽查 Sofia 的招募／一般對話、
字幕、任務日誌、MCM、關係狀態與左上角通知，確認沒有方框、mojibake、空白、截斷或新 crash；
英語配音與 FUZ 不受本覆寫影響。
