# Verification — Nether's Follower Framework Traditional Chinese 2.8.6b

- 驗證日期：2026-08-16
- 結果：PASS
- 遊戲／MO2 啟動：Dev runtime PASS
- 部署、啟用、profile 變更：只部署到 `Modpack-KR-Dev`

## 驗證範圍

```text
python tools/build_translation.py
python tools/verify_translation.py --source "/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/Nether's Follower Framework/Interface/Translations/nwsFollowerFramework_english.txt"
sha256sum -c MANIFEST.sha256
```

驗證器鎖定 NFF 2.8.6b 英文來源 SHA-256，確認 1,398 個 key 的集合與順序，以及每列的數字、
百分比與控制碼完全對齊；唯一結構修正是補回上游 `$FF_LootSpeedDS` 遺失的 Tab。產物另通過
UTF-16 LE BOM、逐列 CRLF、review TSV byte-for-byte 重建與完整 manifest 檢查。

2026-08-16 gameplay audit 補完原本未涵蓋的 ESP／PEX 範圍：

- ESP：2,917 records 完全同身份／順序／GRUP path／semantic header／subrecord topology；只有
  467 個 canonical UTF-8 display zstrings 改為繁中，零非文字 payload 差異。465 筆來自精確
  2.8.6b seed；另兩筆是 runtime 直接觀測到的 `$FF_OutfitCreateMenu`／`$FF_SaySubmenu` 未解析 key，
  以現役 1,398-key 繁中表中的對應 literal 取代。
- PEX：20/20 string-table slot 數一致，header／prestrings／declaration／properties／bytecode tail
  逐 byte 相同；只有 297 個既有顯示字串槽改為繁中。
- 使用者回報的 `I'd like to see your additional follower inventory.` 已對應為
  `我想看你的額外追隨者物品欄。`。

首次 Dev runtime 已由 AgentBridge 證明 NFF、GYH、USSEP plugin 全部由引擎載入，Lydia follower
menu 中 `我想看你的額外追隨者物品欄。` 與 `很高興你在這裡。` 正常；同場抓到上述兩個原始 key
後立即停止 QA、修正 artifact，未把缺陷當成驗收通過。

最終重啟後 AgentBridge 與使用者共同確認 Lydia menu 的四個 NFF／GYH 目標均為正體，包含修正後的
`我想給你設計一套服裝。`、`我要佔用你一點時間。(NFF)`；沒有 raw key、方框、亂碼或截斷。
本批 Dev runtime PASS；尚未授權部署到 Play。
