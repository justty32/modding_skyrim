# Animated Vehicles 調查 — Animated Ships + Animated Carriage

兩個同作者（`zx` / Vicn 資產）的「動態載具」mod，主題成對：海面上會動的船、會跑的馬車。
本篇合併調查，重點放在**「東西怎麼動 + 玩家怎麼搭」**，以及對 ModForge（JSON spec → .esp 生成器）哪些是資料層可生、哪些靠動畫資產或 Papyrus。

- 來源：`Animated Ships-110260-1-2-0`、`Animated Carriage-112397-1-1-0`
- plugin：
  - Ships：`AnimatedShips.esl`（1101 records，light master）
  - Carriage：`AnimatedCarriage.esm`（1660 records，master）＋ 每條路線一個 `ACLine_<Hold>.esp`（範例 `ACLine_Whiterun.esp`，97 records，純 placements）

---

<!-- wf-nav -->
- [ship-mechanism](animated-vehicles/ship-mechanism.md)
- [carriage-mechanism](animated-vehicles/carriage-mechanism.md)
- [record-patterns-and-modforge](animated-vehicles/record-patterns-and-modforge.md)
