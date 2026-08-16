# Source — AI Overhaul 1.9 NPC Names Traditional Chinese

- exact gameplay source：現役 `AI Overhaul.esp` 1.9.0.0（Nexus 21654）。
- source SHA-256：`8296a6ad435f6e31a74f24dd91444fa777c24a3a77a8c4989d9a8738db42a3ef`。
- 名稱權威來源：現役 `Skyrim Traditional Chinese 8.20 Core and Fonts` 的 English-suffix
  `Skyrim`／`Dawnguard`／`Hearthfires`／`Dragonborn` STRINGS；這正是目前
  `sLanguage=ENGLISH` profile 實際使用的正體核心表。
- 建置日期：2026-08-16。

每個 AI Overhaul `NPC_` override 依 defining-master index 與 24-bit local FormID 找回 master
NPC record，再用其 localized `FULL` string ID 讀取現役正體名稱。沒有可靠 core table 的 Fishing
NPC 不翻譯。`tools/name-translation-source.json` 保存每一筆 FormID、原文、目標、master、string ID
與來源。

本包只重建本機版本鎖定的文字覆寫；原 mod 與核心翻譯的權利屬各自作者。公開散布前須另行確認
Permissions。
