# 一、Animated Ships — 做什麼 + 怎麼運作

← [原文入口](../animated-vehicles.md)

## 一、Animated Ships — 做什麼 + 怎麼運作

**做什麼**：在 Solitude / Windhelm / Dawnstar / Winterhold / Riften 等港灣外海，讓玩家看到大型帆船、長船、Katariah、沉船等在海面上「航行 / 上下浮動」，多數還可登船站到甲板上隨船移動，部分港船附帶 trader/fisherman vendor faction。

**核心機制 = 自帶動畫的 NIF + 腳本同步 NPC，不是 AI package 在移動船**：

<!-- wf-nav -->
1. **船 = `Activator` base，model 指向自帶動畫的 NIF**。例：
   `[00081D] Activator zxActDistantShipLong01 → model: Clutter\Vicn\AnimatedShip\Distant\shiplongboat01.nif`，
   掛 `script: zxShp_DistantShiptBase`。NIF 內部有 NiControllerSequence（航行 / 上下浮動 / 沉船三類路徑：`Distant/` `NarrowPath/` `UpDown/` 三套 NIF + `*_BASE.nif`）。**船體的「動」完全是 NIF 內嵌動畫驅動，引擎只是播放它，沒有任何 ref 在被腳本搬動。**
2. **Papyrus `zxShp_DistantShiptBase`（extends ObjectReference）只做三件事**：
   - 維護一個 `ShipMarker`（隱形 XMarker），每個 tick `MoveToNode(self,"ShipCenterNode")` 貼到船 NIF 的中心節點 — 因為 NIF 在動，所以要用一個跟得上的 marker 當「船現在的真實座標」。
   - `SetNPConShip()`：把 linked-ref 串起來的乘客 Actor，用 `SplineTranslateToRefNode(self,"RidingShipNode<idx>", …)` 黏到甲板節點上（NodeMax 個座位，輪流取模）；NPC 飄離或落水就 `ResetPassengerPosition` 重貼。
   - `OnActivate`：玩家在 `fRidableHeight` 內就 `MoveToNode(self,"RidingShipNodePlayer")`，並播船板嘎吱環境音（`AMBShipCreakBaseLP.Play`）。
   - 距離分級 `RegisterForSingleUpdate`（>32000 停、>9000 待命、近距才同步），純效能節流。
3. **排程 / 隨機出現**：`zxShp_SingleShipManagerQuestScript`（Quest）用 `GameHour` 切 5 個時段 bitmask，比對每艘船的 valid time zone；`RandomShipsPerDay` 用 global `zxASgChanceShips` 擲骰決定今天這艘船航不航；不符就 `DisableNoWait` + `DisableLinkChain`，符合就 `Enable` + `EnableLinkChain`。`zxShp_TriggerLoadForDistantShip`（觸發 Activator）在 `OnLoad/OnCellAttach` 喚醒對應船的 `UpdateShip()`。
4. **4 個 Package（`zxShPlayIdleOnShipboard*` / `zxShCreatureOnShipboard01` / `zxSHFencerSneakingOnShip`）全是 template `Skyrim.esm:0x0654E2`**（vanilla 站樁/idle 模板）— 只是讓甲板上的 NPC 站好/偷偷摸摸，**不負責船的移動**。

**玩家怎麼搭**：走到船邊 activate → 被 spline 黏到甲板 player 節點 → 之後船的 NIF 動畫帶著你「看起來在動」（你其實是貼在隨 NIF 動的節點上）。沒有真正的物理載具。

---

