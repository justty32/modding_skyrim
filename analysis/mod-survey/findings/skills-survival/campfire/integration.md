# campfire — integration

← [調查入口](../campfire.md)

## 3. 第三方怎麼掛自己的樹（公開 API）

`CampPerkSystemRegister extends ReferenceAlias`（隨 mod 的 quest 出貨）：

```papyrus
; required_node_controller = 你那棵樹的 CampPerkNodeController Activator base form
; mod_name = log 顯示用
Event OnInit() / OnPlayerLoadGame()
    RegisterForModEvent("Campfire_Loaded", "OnCampfireLoaded")
    AttemptRegistration()
Event AttemptRegistration()
    GlobalVariable ver = Game.GetFormFromFile(0x03F1BE,"Campfire.esm") as GlobalVariable  ; CampfireAPIVersion
    if ver.GetValueInt() >= 4
        CampUtil.RegisterPerkTree(required_node_controller, mod_name)   ; ★ 一行掛樹
```

→ **任何 mod，純 esp + 幾支薄 Papyrus，就能在營火選單加一棵 3D 技能樹**：需要 (a) 一個 `CampPerkNodeController` Activator（填 12 槽 PerkNode/Line + PositionRef markers + ArtPlane），(b) N 個 PerkNode Activator（掛 `CampPerkNode` script + 兩個 rank GLOB + 兩個 description Message），(c) N 個 PerkLine Activator，(d) 一個帶 `CampPerkSystemRegister` alias 的 register quest。perk 的**實際效果**另走普通 ability/MGEF（與星點視覺解耦）。

---

## 4. 對 ModForge / roadmap 的意義

**這是 [custom-skill-tree-guide/README.md](../../../custom-skill-tree-guide/README.md) 之外的第二條自訂技能樹生成路線，且全部落在 ModForge 現有能力域內**（無需 CSF 那種 Scaleform JSON）：

| Campfire 路線零件 | ModForge 現況 |
| --- | --- |
| PerkNode / PerkLine / Controller **Activator** records | ✅ 可生成（普通 ACTI；掛 script 走 VMAD/AttachScripts，與 perk-conditiontabcount 同類已驗證路徑）|
| rank GLOB（`required_perk_rank_global` + `_max`）| ✅ 可生成（簡單 GLOB）|
| perk description **Message** records | ✅ 可生成（MESG）|
| **PositionRef 擺位 markers** + 連線拓樸（node 屬性指向 downstream） | ⚠️ 需要：在某 cell 內擺一組相對 marker（placements）+ ACTI 屬性互指；本質是 **cell ref 佈局 + record 屬性連結**，ModForge 有 placements/cellrefs 基礎，缺「一組固定相對 layout 模板」|
| register quest + `CampPerkSystemRegister` alias（一行 `RegisterPerkTree`）| ✅ 可生成（quest + ReferenceAlias + alias script 屬性）|
| 星/線/背板 **NIF** | 直接重用 Campfire 的（依賴 Campfire.esm 即可引其 form），免自製美術 |

**槓桿點**：相較 CSF（要 native dll 玩家端 + Scaleform JSON + UTF-16 翻譯檔），**Campfire 路線的玩家端依賴只有 Campfire.esm 本身**，產物全是 ESP record + 薄 Papyrus——對 AI-agent 友善的「JSON spec → 技能樹」更貼合。代價：外觀固定（營火旁 3D 樹）、節點上限 12/樹、且綁 survival 情境（要先有營火）。

**建議 roadmap 動作**：把本檔與 [custom-skills-framework/README.md](../../../custom-skills-framework/README.md) 並列為「自訂技能樹兩條路線」，在 roadmap 標注 Campfire 路線為**低依賴 MVP 候選**（純 record 可生成，只缺 layout 模板生成器）。

---

## 5. 對 Sofia patch 的意義

無直接關係（Sofia 不碰 survival/技能樹）。間接：Campfire 的 **`_Camp_ObjectPlacementThreadManager` async 放置 + future 模式** 是「在玩家面前可靠 spawn 一組臨時物件並保證回收」的成熟範式——若日後 Sofia/follower 要做「召喚一組臨時互動物件」（如行動選單實體化），這套 RequestLock/PlaceObject-future/wait_all/distance-takedown/cell-detach-failsafe 是值得借鏡的健壯骨架。
</content>
</invoke>

## 6. 安裝坑與 SE/AE／中文層現況（2026-09-02 補查）

一句話結論：若需求／生存選 Campfire／Frostfall，Campfire 是必經基座；先剔除隨包 DLL、由現役 PapyrusUtil 覆蓋，再驗 1.6.1170。

- PapyrusUtil／StorageUtil：Classic 包帶 `StorageUtil.dll`，SE 包帶 `PapyrusUtil.dll`（`analysis/tool-survey/repos/Campfire/Campfire_BuildRelease.py:87`）；Frostfall 因 Campfire 已內含而移除 PapyrusUtil（`analysis/tool-survey/repos/Campfire/readmes/Frostfall_changelog.txt:389`）。Campfire 腳本查無 `StorageUtil.` 呼叫。`modpack-design/sources/OPEN.md:15` 警告 `PapyrusUtil.dll`，此 clone 實存卻是 `StorageUtil.dll`；不可混稱，可能是不同 build／版本。
- SSE/AE：舊證據只到 PapyrusUtil 3.4b、SKSE64 2.0.7、SSE 1.5.39（`analysis/tool-survey/repos/Campfire/readmes/Campfire_changelog.txt:20`），無 AE／1.6.1170 證據，不能判相容。
- 中文層：`mod-library/l10n/` 與 zh-layer 清單均無 Campfire，尚無翻譯層。
- 待裁決：只新增 DLL、中文與 1.6.1170 gate；不代決需求／生存（`modpack-design/content-plan/gameplay/OPEN.md:9`、`wait-user/home-setup.md:61`）。
