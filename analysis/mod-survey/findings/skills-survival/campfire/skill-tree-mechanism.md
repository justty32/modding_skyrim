# campfire — skill-tree-mechanism

← [調查入口](../campfire.md)

## 1. 一句話結論

Campfire 的天賦樹**不是 Scaleform/UI 選單**。它在玩家面前的**真實世界座標**裡，用 Papyrus 動態 spawn 出一堆**普通的 in-world ObjectReference**——星點是 NIF activator、連線是 NIF activator、背板是一張 static「art plane」——排成一棵樹的形狀、整體轉向面對玩家；玩家用準心**啟動（OnActivate）**某顆星來點 perk，走遠 480 unit 整棵樹自動 disable+delete。這套引擎透過公開 API `CampUtil.RegisterPerkTree(...)` 開放給任何 mod 掛自己的樹（Frostfall 的「Endurance」就是這樣掛上去的）。

對照組：[CSF（Custom Skills Framework）](../../../custom-skills-framework/README.md) 走的是 Scaleform 假 perk-skydome 選單（重用原版星座菜單外殼）。**Campfire 與 CSF 是兩條完全不同的自訂技能樹技術路線**——CSF＝改 UI 層、Campfire＝擺世界物件。

---

## 2. 機制全解：星點如何成為 3D 世界物件

### 2.1 物件家族（meshes/campfire/）

| NIF | 角色 | 對應 record |
| --- | --- | --- |
| `_camp_intperkstars01.nif` | **天賦星點**（一顆可點的星） | Activator + `CampPerkNode` script |
| `_camp_intperkline01.nif` | **節點間連線**（點亮後播 `Unlock` 動畫） | Activator（無腳本，靠動畫狀態） |
| `_camp_perkartplane.nif` | 背板「art plane」（深色面板，營造選單氛圍 + 播 `UISkillsGlow` 音效） | Static |
| `_camp_perksystementerexp.nif` | 進入特效 | — |
| 三隻「Bug」(Next/Prev/Exit) activator | 導覽螢火蟲（切換樹／離開） | `_Camp_NextBug`/`_Camp_PrevBug`/`_Camp_ExitBug` |

### 2.2 三層 controller（都 extends `_Camp_PlaceableObjectBase`）

```
CampCampfire（營火本體，玩家對它選「Tend / Skills」）
   │  ShowPerkTree() → 在營火位置 spawn ↓
   ├── CampPerkNodeController          ← 一棵樹一個；持有 12 槽 PerkNode + 12 槽 PerkLine + 1 ArtPlane
   │      持有 PositionRef 標記（PerkNodeXX_PositionRef）＝每顆星相對中心的擺位
   └── _Camp_PerkNavController         ← 導覽；spawn Next/Prev/Exit「bug」、管距離自毀
```

### 2.3 擺位的數學：相對 CenterObject 的偏移（這就是「3D 空間」的關鍵）

`_Camp_PlaceableObjectBase.Initialize()` 的核心序列：

```
RotateOnStartUp()                       ; 自身先轉 Setting_StartUpRotation
self.SetAngle(0,0, GetAngleZ()+GetHeadingAngle(Player)+180)  ; ★整個 controller 轉向面對玩家
PlacementSystem.RequestLock(self)
PlaceObjects()                          ; 子類覆寫：對每個節點呼叫 PlaceObject(...)
PlacementSystem.wait_all()              ; 等所有 async 放置完成
GetResults()                            ; 收 future、EnableNoWait()、接 controller、連線
PlacementSystem.ReleaseLock(self)
```

- **CenterObject = controller 自己的 PositionRef**。每顆星不是寫死世界座標，而是 `PlacementSystem.PlaceObject(self, PerkNodeXX_Activator, PerkNodeXX_PositionRef, ...)`——`PositionRef` 是一組擺在 controller 周圍的**標記 ObjectReference**，記錄「相對中心的 local 偏移 + 角度 + scale」。
- 因為 controller 先 `SetAngle` 轉成面對玩家，**整組 local 偏移就一起旋轉**，所以無論玩家站哪、營火朝哪，樹永遠正面展開在玩家眼前。連線用 `inverted_local_y=true` + `is_propped=true` + 取 PositionRef 的 X/Z 角度貼合兩星之間。
- `PlaceObject` 回傳的是一個 **future 物件**（`_Camp_ObjectFuture`，async 放置佇列），`wait_all()` 後 `GetFuture(x).get_result()` 才拿到真正 spawn 出的 ref。這是 1.11SE 純 Papyrus 時代避免 `PlaceAtMe` 卡頓的並行放置系統（`_Camp_ObjectPlacementThread01..30` + `ThreadManager`，30 條 worker thread）。

### 2.4 互動與生命週期

<!-- wf-nav -->
- **點 perk**（2026-06-21 原始碼覆核更正）：星 = `CampPerkNode extends ObjectReference`。`OnActivate` → `controller.NodeActivated(self)`（`campperknode.psc:46`）。**不是直連 `IncreasePerkRank`**——`NodeActivated`（`campperknodecontrollerbehavior.psc:25-60`）先 gate：可買 iff **起始 node 或下游 child node 已買**（`downstream_node_*.required_perk_rank_global >= 1`，注意是「**下游 child 已買**」不是「parent rank」——Frostfall 樹根在底、`downstream` 指向原點）且 未滿 rank 且 `required_perk_points_available > 0`；通過後彈 Yes/No 確認選單，選 Yes 才 `IncreasePerkRank()`（+1 寫回 rank GLOB、`PlayAnimation("OwnedWild")`、`UpdateLines()` 下游連線播 `Unlock`）+ 點數池 `-1` + `SendEvent_CampfirePerkPurchased()`（`:117-124`）。**spend/gate/確認選單全在 Campfire 自己的 `CampPerkNodeControllerBehavior`，消費端（Frostfall）只負責賺點數（增 `required_perk_points_available` GLOB）。**
- **視覺狀態靠 GLOB 重建**：`AssignController` 時讀 `required_perk_rank_global.GetValueInt()`，>0 就立刻播 `OwnedWild`——所以**已點的 perk 每次開樹都正確顯示亮起**，狀態全存在 GLOB（存檔安全）。
- **連線拓樸**：每個 node 有 `downstream_node_1/2` + `downstream_line_1/2`（指 Activator base form）。`AssignDownstreamNodes()` 用 controller 的 `NodeActMap`/`NodeRefMap` 把 base form 解析成 runtime ref。**樹形是在 esp 裡用屬性連好的**，不是 JSON。
- **自毀**：`_Camp_PerkNavController.CheckConditions()` 每 3 秒檢查 `Player.GetDistance(self) > 480` → `TakeDownPerkTree()` + 全部 `TryToDisableAndDeleteRef`。另有 `OnCellAttach/Detach` 失效偵測 + `FindClosestReferenceOfType` failsafe 回收漏網 ref——因為這些是 temp ref，**絕不能殘留存檔**。

### 2.5 切換多棵樹

Next/Prev「bug」呼叫 `CampCampfire.ShowNextPerkTree()/ShowPrevPerkTree()`——takedown 當前 controller、spawn 下一個。註冊進來的每棵樹是一個 `CampPerkNodeController` Activator，Campfire 維護清單（`_Camp_PerkNodeControllerCount` GLOB）輪播。

---

