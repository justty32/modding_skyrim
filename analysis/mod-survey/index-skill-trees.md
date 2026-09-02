# 自訂技能樹與求生框架

← [mod-survey](README.md)｜[survey index](index.md)

## 自訂技能樹（Custom Skills Framework）

| 主題 | 文件 | 重點 |
| --- | --- | --- |
| Custom Skills Framework 技術調查 | [custom-skills-framework/README.md](custom-skills-framework/README.md) | CSF 架構、兩代格式斷層、案例研究（VIGILANT/GLENMORIL）、Constellations schema/接線 |
| 實作指南（動手教學） | [custom-skill-tree-guide/README.md](custom-skill-tree-guide/README.md) | 自訂技能樹分析 + 實作指南（roadmap 功能項） |
| Constellations（CSF 最高品質參考實作） | [findings/constellations.md](findings/constellations.md) | CSF 路線確認正確；MVP = JSON+PERK+GLOB+KYWD+薄 Papyrus；Fortify 附魔 native dll 超出 MVP |

## 求生 / 框架系統型（Campfire 堆疊 + PROTEUS）

<!-- wf-nav -->

| Mod | Finding | 機制重點 | ModForge 意義 |
| --- | --- | --- | --- |
| Campfire（求生框架） | [findings/campfire.md](findings/campfire.md) | **in-world 3D 技能樹引擎**：星點/連線/背板都是真實 ObjectReference，相對 CenterObject 偏移 spawn、轉向面對玩家、OnActivate 點 perk、距離 480 自毀；公開 API `RegisterPerkTree` | **第二條自訂技能樹生成路線**（vs CSF Scaleform）；零件全在 record 能力域，玩家端只依賴 Campfire.esm；缺 PositionRef layout 模板 |
| Frostfall（求生 mod） | [findings/frostfall.md](findings/frostfall.md) | 天賦樹＝註冊進 Campfire Skill System 的「Endurance」樹（6 perk，`_Frost_PerkRank_*` GLOB ↔ CampPerkNode）；exposure/warmth 系統 | Campfire 掛樹 API 的活範例；星(視覺)與 MGEF(效果)解耦 |
| PROTEUS（角色 build 管理） | [findings/proteus.md](findings/proteus.md) | native `Proteus.dll` + 6 個 JSON 模板 runtime 序列化角色狀態；UILib 選單 | 忽略（閉源 native，無生成成分）；JSON 角色 schema 純對照參考 |

> 使用者 2026-06-16 指定調查：Frostfall 天賦樹 + 「星點如何成為 3D world space object」→ 答案全在 [campfire.md §2](findings/campfire.md)。
