# RDO Final CHT 相容性與正體中文覆寫審計

日期：2026-08-16

## 結論

本機 `RDO Final CHT-22207-Final-1546039712.zip` 與現役官方 RDO Final 是精確結構相容的
text-only translation seed。它不是只靠 archive 名稱判定：ESP 的 record topology／semantic header／
全部非文字 payload，及六個 PEX 的 declaration／bytecode tail 都已逐項比對。

已建立可重現產物：

[`mod-library/l10n/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/`](../../../mod-library/l10n/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/README.md)

## 鎖定來源

| 項目 | SHA-256 |
|---|---|
| 官方 Final archive | `99988d898c1356e37341a44ed95e8ed0b15bcefcf7626f797d5bd04b9388d5f2` |
| 官方 ESP | `b8d33bd731dded257b517402135cc7ba69be8d7e2b2cc8f038481802b363c2d0` |
| 官方 BSA | `40e20585512cc5fe796faab112863592a5549165fd378d5d14a098652207be42` |
| RDO Final CHT archive | `45271a07353ef99bac7ecff6cbf19da59afec17bdfc8f2f3cb2db43fafbbafd5` |
| 最終正體 ESP | `60deb5dd577848a302a3c78b13484caad4c3b2b3db3c4d4e6ac6208963651c32` |

已安裝的官方 ESP／BSA 與官方 archive 逐 byte 相同。

## ESP 差異證據

- source／seed／output 都是 9,766 records；
- record order、signature、raw FormID、GRUP path、flags、version bytes、compression state 與
  subrecord tag topology 相同；
- 4,071 個差異全部是 canonical zstrings，target 全部是嚴格 UTF-8；
- 非文字 payload 差異為 0；
- tag 分布：NAM1 3,776、FULL 180、RNAM 72、NNAM 16、DESC 13、DNAM 11，CNAM／MNAM／SHRT 各 1；
- 來源 record type 主要是 INFO 3,848，另含 DIAL、QUST、BOOK、NPC、MGEF、SPEL 等玩家可見文字。

品質 gate 沒有空目標、U+FFFD、`???`、換行漂移或設定的常見簡體殘字。唯一 token mismatch 是：

```text
官方：Do you remember now? (<bribecost> gold)
seed：你還記得嗎？（賄賂<BribeCost>枚金幣）
最終：你還記得嗎？（賄賂<bribecost>枚金幣）
```

最終產物把 token case 精確還原；其餘 seed 文字不改。

## 六個 PEX

翻譯 archive 夾帶的六個 PEX 不是任意重編譯。每個與官方 BSA 成員有相同 PEX header、prestrings、
string count 和完整 tail；各只改一個既有 string-table slot，內容是 Gelebor、Isran、Valerica 各自
「仍在等待／離隊」通知。沒有 declaration、property、control flow 或 bytecode 差異。

因此產物保留這六個 loose PEX，讓 script 產生的通知也能正體化；未納入任何其他 script。

## 邊界與下一步

這份證據足以判定可作 Dev-only 獨立覆寫，但不等於 runtime 顯示已驗收。部署後需抽查一般關係對話、
對話選項／字幕、任務／通知、賄賂金額 token，以及六條 follower script 通知。未通過前不移到
Play profile。
