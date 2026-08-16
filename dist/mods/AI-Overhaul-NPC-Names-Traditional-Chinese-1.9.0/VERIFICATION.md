# Verification — AI Overhaul 1.9 NPC Names Traditional Chinese

- 驗證日期：2026-08-16
- 離線結果：PASS
- runtime：PASS

Gate 鎖定：

- 精確 1.9 source plugin、四個 master plugin、四個現役 CHT STRINGS 的 SHA-256；
- 3,265-record identity/order/GRUP path/semantic header/subrecord topology；
- 唯一允許差異為 423 個既有 `NPC_ FULL` UTF-8 zstrings；
- 其餘每個 payload byte 必須完全相同；
- 424 個英文 NPC 名稱中，423 個有權威正體來源；一個 Fishing NPC 明示 skipped。

代表性目標：`00013B9E:Skyrim.esm`，`Elrindir → 厄倫德`。

首次 build／verify 已通過：3,265 records preserved、423 個 `NPC_ FULL` 改為正體、所有其他
payload 逐 byte 相同。產物 `AI Overhaul.esp` SHA-256：
`c09e81c431fdb8f55d4ba6e49e26b3139f70f83ffaba2b4ed7e6445e5942341d`。

Dev fresh launch 載入可信 baseline 後，AgentBridge 以 ref `0001A681` 直接讀到 actor name 與 dialogue
speaker 都是 `厄倫德`；使用者肉眼確認成功。三個既有酩酊獵手對話選項仍為正體，本輪沒有新
`crash-*.log`。本批 runtime PASS；尚未部署到 Play。
