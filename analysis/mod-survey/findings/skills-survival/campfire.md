# Campfire — Complete Camping System（求生框架 + in-world 3D 技能樹）

← [survey index](../../index.md)｜姊妹文件：[custom-skills-framework/README.md](../../custom-skills-framework/README.md)（CSF＝**另一條**自訂技能樹路線）

| 項目 | 值 |
| --- | --- |
| 類型 | **框架型**（survival 框架，被 Frostfall 等 mod 當依賴）+ 內含一套**自訂技能樹引擎** |
| Plugin | `Campfire.esm`（調查版本：1.11SE，內含於 Frostfall Campfire SSE Fix）| 
| 規模 | quests=25 npcs=0 items=112 magic=79 books=43；附 `Campfire.bsa`（155 支 .psc 原始碼隨附）+ native `Campfire.dll`? （無，純 Papyrus + meshes；DLL 在更新版才有，1.11SE 無 DLL，全 Papyrus + SKSE event）|
| 敘事價值 | 無（純機制）；**機制價值：極高** |

> 調查重點＝使用者問的兩件事：**(1) Frostfall 天賦樹**（→ 它是 Campfire 的「Skill System」，見 [frostfall.md](frostfall.md)）、**(2) 那些天賦星點怎麼變成 3D world space 裡的 object**（← 本檔主體）。

---

<!-- wf-nav -->
- [1. 一句話結論](campfire/skill-tree-mechanism.md)
- [3. 第三方怎麼掛自己的樹（公開 API）](campfire/integration.md)
