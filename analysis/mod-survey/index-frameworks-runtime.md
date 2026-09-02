# 框架型 · runtime 庫與 follower 框架

← [mod-survey](README.md)｜[survey index](index.md)

<!-- wf-nav -->

| Mod | Finding | Plugin / Runtime | 參考價值 | 重點 |
| --- | --- | --- | --- | --- |
| Common Framework / Utility Mods | [findings/common-framework-mods.md](findings/common-framework-mods.md) | SPID / OAR / PapyrusUtil / JContainers / BOS / AOS / Conditional Expressions / IWH / ITH | 高（工具層） | distribution、animation conditions、state storage、object/animobject swap、expression state、collision/dialogue suppression |
| PapyrusUtil SE（深挖） | [findings/papyrusutil.md](findings/papyrusutil.md) | `PapyrusUtil.dll`（SKSE，無 ESP） | 高（狀態儲存 + cell 掃描 + package override） | StorageUtil per-form KV + list（int/float/string/Form 四型）；JsonUtil 外部 JSON 讀寫 + path API；ActorUtil package override priority 0-100；MiscUtil ScanCellNPCs/Objects、檔案操作；PapyrusUtil 陣列 push/diff/merge/slice；v4.6 |
| JContainers SE（深挖） | [findings/jcontainers.md](findings/jcontainers.md) | `JContainers64.dll`（SKSE，無 ESP） | 高（複雜資料結構 + 外部 JSON 雙向） | JArray 無上限動態陣列；JMap/JFormMap/JIntMap key-value 容器；JDB 全域資料庫（跨 mod 共享）；JFormDB per-Form 嵌套結構；JValue readFromFile/writeToFile JSON 序列化；JAtomic 原子操作；生命週期需手動 retain/release；API 4 / Feature 2 |
| Conditional Expressions（深挖） | [findings/conditional-expressions.md](findings/conditional-expressions.md) | `Conditional Expressions.esp` + 16 .psc | 高（表情層） | MFG SetModifier/SetPhoneme/SetExpressionOverride 全索引表；16 種狀態 effect 機制；busy gate 設計；三段式漸變 pattern；GlobalVariable 中介狀態可用於 dialogue condition |
| I'm Walking Here + I'm Talkin' Here | [findings/iwh-ith.md](findings/iwh-ith.md) | `ImWalkinHere.dll`（SKSE）+ `ImTalkinHere.esp` | 中（品質層） | IWH：TOML 四開關碰撞抑制，無 API，純被動；ITH：`PlayerInDialogue` Conditional property，bark condition hook；follower mod 可讀 GetScriptVariable 或自實作 PlayerBusy global |
| Nether's Follower Framework | [findings/nether-follower-framework.md](findings/nether-follower-framework.md) | `nwsFollowerFramework.esp` | 高（主要 follower 框架） | DialogueFollower slot expansion；regular vs imported followers；Sofia import/export；NoImport faction；sandbox/regard/home/storage |
| Extensible Follower Framework | [findings/extensible-follower-framework.md](findings/extensible-follower-framework.md) | `EFFCore.esm` + `EFFDialogue.esp` | 高（slot-bank follower framework） | 100 follower aliases + 100 hidden inventory containers；plugin quests；dialogue menu；alias package override stack；slotFactory reference |
