# 系統／機制型 · 遭遇生成與底層 record 機制

← [mod-survey](README.md)｜[survey index](index.md)

逐 mod 機制拆解 + 對 ModForge 的「可生成 / 需新支援 / 純參考」標記。共通缺口已彙整進 [roadmap](../../projects/ModForge/workflows/roadmap/README.md)「mod-survey 浮現的 record/生成缺口」。

<!-- wf-nav -->

| Mod | Finding | 機制重點 | ModForge 缺口 |
| --- | --- | --- | --- |
| Extended Encounters | [findings/extended-encounters.md](findings/extended-encounters.md) | 純 SM 驅動 ~140 遭遇；navmesh-tester 動態生怪 | SM branch/quest-node 子樹；spawn-near-player 模板 |
| Immersive World Encounters | [findings/immersive-world-encounters.md](findings/immersive-world-encounters.md) | SM 容器 quest + Scene(Package/Timer/Dialog) | LVLN alias fill；package target=alias |
| Missives | [findings/missives.md](findings/missives.md) | 公告板 radiant 工廠（Activator+FLST+Quest.Start，無 SM）；alias findMatching 填 | FLST 建立（最高價值）；LVLN/alias 間接 |
| Spellforge | [findings/spellforge.md](findings/spellforge.md) | 預製 SPEL 池、索引對齊 FLST、非 runtime 組裝 | FLST 建立；程序化法術族（高階） |
| Arrowblock | [findings/arrowblock.md](findings/arrowblock.md) | PERK `ModIncomingDamage` + Script-MGEF `OnHit` | MagicEffectSpec 缺 script-attach(VMAD) |
| Immersive Interactions | [findings/immersive-interactions.md](findings/immersive-interactions.md) | perk `AddActivateChoice` + Global-as-DAR-selector | perk entry-point AddActivateChoice；_conditions.txt 生成器 |
| Animated Ships / Carriage | [findings/animated-vehicles.md](findings/animated-vehicles.md) | ship=NIF 自動畫；carriage=linkedRef 節點鏈路線 | placements 缺 `linkedRef` 欄位 |
| SM（Story Manager）子系統 | [findings/sm-subsystem.md](findings/sm-subsystem.md) | SMBN/SMQN/SMEN record 結構；event 路由；多層巢狀設計 | 多層巢狀 SMBN（缺口 #2 partial）；LVLN alias fill；package target=alias |
| Script-attached MGEF（VMAD） | [findings/mgef-vmad.md](findings/mgef-vmad.md) | VMAD 結構 + ActiveEffect 繼承；OnEffectStart/Finish 事件；三層 PERK→SPEL→MGEF→Script | partial 缺口 #3（MagicEffectSpec 缺 inline scripts 欄位；通用 AttachScripts 可繞路） |
| FLST 工廠模式 | [findings/flst-factory.md](findings/flst-factory.md) | FLST record | 高（缺口撤銷，模式有價值） | 索引對齊池 / 分類容器 / FLM 追加 三種模式 |
| Global-as-Selector + linkedRef 鏈 | [findings/runtime-selector-patterns.md](findings/runtime-selector-patterns.md) | GLOB/XLKR | 中 | runtime 狀態共享 + 路線節點鏈 + OAR/DAR condition 銜接 |
| PERK entry-point 機制 | [findings/perk-entry-points.md](findings/perk-entry-points.md) | PERK record | 高（缺口 #1） | entry-point 種類全表 + fragment 膠水 + AddActivateChoice 深挖 |
| NPC Senses（Nexus 178532） | [findings/npc-senses.md](findings/npc-senses.md) | `NPC Senses.esp`（646B，僅 6 ACTI）+ `NPCSenses.dll`（CommonLibSSE-NG，SE/AE/VR/GOG，無 ini/psc/README） | 無 | **NPC 感知區可視化 + 進出事件派發**（modder's resource／debug 工具，非平衡 mod）：DLL 對規則選中的 NPC attach Vision 視線錐（可選 LOS）+ Aura 近身球，進出時廣播 `NPCSenses_Vision/Area Enter/Exit` mod event 供 Papyrus 接；規則走 `Rules/*.json`（FormID/EditorID/Race/Keyword/Perk filter）+ 內建 ImGui 遊戲內規則編輯器（非 MCM）。esp 純幾何供應站。**不碰 GMST/SPID/perk** → **純參考，無新缺口**；ModForge 唯一能生的 6 ACTI 脫離 DLL 無意義 |
