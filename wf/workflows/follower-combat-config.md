# NativeCombat 設定契約

[隨從戰鬥相容工作流](follower-combat-compat.md)

設定均在 `SKSE/Plugins/FightWithMePaths_NativeCombat.ini` 的 `[NativeCombat]`，於 DataLoaded 讀取，修改後須完整重啟。沒有存檔 schema 變更，也不支援 runtime 熱切換。確切模式以實際 DLL 版本及相應交付 SPEC 為準。

## r3：受管隨從預設原生選裝

2026-11-02 使用者明確要求「直接改全員預設」。`bDefaultNative=1` 讓 Paths standalone 的 Party 受管隨從預設使用原生普通選裝 AI；非 Party 角色及完整 FWM host 不啟用。技能成長／能力保留，explicit POOL／legacy HAND、battle lock、Bruiser／Skald 拒啟優先序不變。

缺檔、缺 key、空值、舊 Varinia INI 均採預設 1；僅接受修剪空白後的 `0` 或 `1`，壞值／截斷警告並採預設 1。全員模式不解析 `sActorBases`，不受舊名單、其壞值或 16 人上限限制。只有明確 `bDefaultNative=0` 才走下述 legacy 白名單。

交付設定及測試證據見 [r3 SPEC](../../mod-library/plugins/Path-Of-The-Companions-NativeCombat-1.2-r3-2026-11-02/SPEC.md)。全員預設不等於所有自訂腳本已實戰驗證，仍須分開記錄實際角色與能力觀察。

## r1／r2 及 r3 關閉全員模式時的 legacy 白名單

`sActorBases=` 的值為分號分隔的 `Plugin.esp|十六進位localID`，最多 16 個唯一 NPC base。空值停用 NativeCombat；無效／找不到／非 NPC 項警告略過、重複去重、不支援 wildcard；整值超過 4094 UTF-16 code units 截斷時整值拒絕。不支援舊單數 key。

r1／r2 沒有全員開關，未列角色保持原路；r3 僅在明確關閉全員模式時套用此限制。確切核准名單見版本交付證據，不把示例角色當成授權對象。
