# Verification — USSEP Traditional Chinese 4.3.8a

- 驗證日期：2026-08-16
- 狀態：offline gate PASS；runtime 尚未執行

## 合約

- source hash 必須精確等於現役 USSEP 4.3.8a。
- seed hash 必須精確等於 Nexus 143324 的 4.3.6c CHS ESP。
- output 必須保留 58,965 筆 record identity/order/GRUP path、semantic headers 與 subrecord topology。
- ledger 以外的所有 payload 必須逐 byte 相同；翻譯欄位必須精確等於 UTF-8 正體目標。
- 可安全套用 17,904 個文字欄位；562 個跨版本 token／換行不一致或空來源候選必須保留現役原文。
- Dev runtime 必須重測 Elrindir 兩個選項與回答、一般 USSEP 覆寫對話、方框／mojibake、Papyrus
  與 crash logs；通過前不得部署 Play。

實跑結果：58,965 筆現役 records 全數保留；17,904 個文字欄位精確落地，ledger 以外所有 payload
逐 byte 相同。562 個跨版本 token／換行不一致或空來源候選已排除，沒有以舊譯文覆蓋新版語義。
