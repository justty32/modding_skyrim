# IFD Lydia 4.2.2 中文 archive 差異稽核

日期：2026-08-16

## Done when

確認現役官方本體與同版中文 archive 的 ESP／PEX／資產差異；只有在差異可證明為文字時才建立
正體中文產物，否則留下明確 blocker。

## 結論

同版 CHS archive 可作翻譯語意種子，但不能未經驗證直接覆寫。完成解壓與語意 diff 後，主 ESP
與 loose PEX 都證明為 text-only：

- 官方 archive 內 ESP 與現役安裝逐 byte 相同，確實是 4.2.2 baseline。
- 官方與 CHS 主 ESP 各 5,708 records；順序、FormID、GRUP path、record header、壓縮狀態與
  subrecord topology 全部一致。
- 1,794 個 payload 差異全是 canonical source CP1252 → target UTF-8 zstring；分布為 `NAM1` 1,288、
  `FULL` 449、`RNAM` 20、`NNAM` 19、`SHRT` 7、`CNAM` 6、`DNAM` 3、`DESC` 2。其餘 payload
  逐 byte 相同。
- CHS archive 沒有 BSA、voice、mesh 或 texture；只含主 ESP、三個 optional patch ESP 與一個 PEX。
- 官方 BSA 內 PEX 6,517 bytes，CHS loose PEX 6,399 bytes。兩者同為 128-slot string table，只有
  18 個 MCM display strings 改變；string-table 後方 3,986 bytes 逐 byte 相同，因此沒有腳本邏輯差異。

## 產物

已建立
[Improved-Follower-Dialogue-Lydia-Traditional-Chinese-4.2.2](../../../../mod-library/l10n/mods/Improved-Follower-Dialogue-Lydia-Traditional-Chinese-4.2.2/README.md)：

- 只包含同名 ESP 與 `scripts/lydiaconfigscriptnew.pex`；
- 不含三個 optional patch，也不含官方 BSA／voice／資產；
- 79 個 vanilla exact English matches 復用 Skyrim Traditional Chinese 8.20；
- 其餘 1,715 個由同版 CHS seed 轉正體，MCM 18 項人工整理；
- build 與 verifier fail-closed 鎖定 exact source hashes、record topology、non-text bytes、PEX tail 與
  reproducibility。

## 剩餘邊界

產物沿用 CHS archive 的 inline UTF-8 ESP 做法，尚未在目前 Proton／`sLanguage=ENGLISH` 實測。
runtime gate 必須抽查對話選項、字幕、任務／書籍與 MCM；在此之前不能宣稱部署完成。公開發布前
另須核對官方與 CHS 翻譯 permissions。
