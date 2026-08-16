# Verification

2026-08-16 靜態驗證與既有存檔 runtime 結果：PASS。

- 原始 PSC／PEX hash 與 PROTEUS 3.4.0 契約一致。
- 34/34 顯示常值均轉成 ASCII 翻譯鍵；非顯示相容性字串未動。
- 修正版最終 PEX 反編譯為 9 個完整、可結構化的 function/event；與打包 PSC 的宣告集合及各
  function/event body 相同，包含 save-compatible `OnConfigOpen` page refresh。
- 翻譯檔為 UTF-16LE BOM + CRLF，34 個鍵與 TSV 完全一致。
- 成品不含 ESP；頁籤在每次 `OnConfigOpen` 時更新，避開既有 save 中 VMAD property 已持久化的問題。

重跑完整 gate：

```bash
python tools/verify_translation.py \
  --upstream-psc '/path/to/PROTEUS/Source/Scripts/ProteusMCMScript.psc' \
  --upstream-pex '/path/to/PROTEUS/Scripts/ProteusMCMScript.pex' \
  --final-decompiled '/path/to/final-decompile/ProteusMCMScript.psc'
```

首輪 runtime 的一-record VMAD 方案在既有存檔出現空頁：save 內仍持久化原始
`Pages = General/Hotkeys`，而 keyed PEX 的分支不再接受舊值。該方案已完整撤除，成品不再含 ESP；
修正版由 `OnConfigOpen` 每次重建 page array。以同一 `ModpackKRDev0A` save 重測後，使用者確認
PROTEUS MCM 兩頁成功載入，繁中內容正常。這項結果同時證明 save compatibility 修正有效。
