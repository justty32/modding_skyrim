## 4. Bandolier NPC 中文 forward patch（已作廢 —— 2026-09-01 使用者裁示 Bandolier 併入 clothes purge）

**本節不執行，前置條件已不存在。**

**前置條件。** 要有現役 Bandolier NPC 八顆 plugins、Classic 本體、CHS seed archive、現役
`modpack-main/plugins.txt`、Python 與 7z；builder 已把這些 Linux 路徑寫死
（`mod-library/l10n/tools/build_bandolier_for_npc_chinese_layer.py:25`；`:26`；`:34`；`:38`；`:41`）。
CHS seed 與本體／NPC plugins 還有 size／SHA-256 pin，來源一變就不應硬跑
（`mod-library/l10n/tools/build_bandolier_for_npc_chinese_layer.py:47`；`:50`；`:54`；`:62`）。

**實際動作。** 在 repo 根執行：

```bash
python3 mod-library/l10n/tools/build_bandolier_for_npc_chinese_layer.py
```

腳本是無參數 entry point（`mod-library/l10n/tools/build_bandolier_for_npc_chinese_layer.py:535`；`:536`），會先核對現役
plugin 啟用集合，異動即 fail closed（`:152`；`:157`；`:159`；`:160`）。完成後用實際 load-order winner 工具核對
83 unique＋23 realistic 兩批，並保存 record 對帳與 plugin gate；該 winner 工具的本案專用命令 repo 內未記錄，
回家現場確認（`modpack-design/archive/content-plan/zh-layer/zh-layer-coverage/unresolved-and-rulings/rulings.md:16`；`:19`）。
注意 builder ledger 的內部 `220 = 220 + 0` 不是本案寫死的 106 winner gate，不能拿來替代
（`mod-library/l10n/mods/BandolierForNPC-Chinese-3.3.0-Dev-2026-08-30/tools/ledger.json:11`；
`wait-user/home-setup.md:24`；`:25`）。

**通過條件。** 106 個目標字串全由 patch 贏得、93 個 NPC 層 ARMO 不再顯示英文，且 NPC 分發與
less-common／realistic variant 都保留；保存 record 對帳與 plugin gate 證據
（`wait-user/home-setup.md:25`；`:26`）。

**失敗退路。** builder 若報 `SOURCE MISMATCH` 或 winner 數不合即停，不改 pin、不部署部分 patch；腳本的
fail-closed 訊息在 `mod-library/l10n/tools/build_bandolier_for_npc_chinese_layer.py:364`。保留現役 NPC 分發與英文狀態，
待 actual archives／plugins 對齊後重做，不能用排序假裝救回中文
（`modpack-design/archive/content-plan/zh-layer/zh-layer-coverage/unresolved-and-rulings/rulings.md:9`；`:11`）。

**預估時間。** 45–75 分鐘（本單估算）；依據是 builder 已存在，但仍需對 106 targets 做現役 winner 對帳
（`wait-user/home-setup.md:23`；`:24`；`:25`）。

