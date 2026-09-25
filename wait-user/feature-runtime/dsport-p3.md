## DSPort P3 物件邊界（2026-09-14）

地板／天空盒隨位置與視角消失、碰撞仍在；OBND 全零是已觀測資料，是否造成症狀仍待實機。離線修正與可重建步驟見 [OBND 調查](../../projects/darksouls-port/p3/OBND-INVESTIGATION-2026-09-14.md)。回家由同一版 ModForge、同一份 P3 來源產生僅 bounds 不同的對照包，先記工具／spec／ESP 雜湊，再於原先消失位置用相同視角與距離比較地板、穹頂與天空盒；確認碰撞與可見範圍無退步。保持 navmesh 模式相同，不能同時切換多層網格後把差異都歸因於 bounds。

## DSPort P3 多層 navmesh（2026-09-14）

NAVI 的 NVMI owning-cell 座標離線修正不等於 CTD 已消失。回家使用同一版工具、同一份 source/spec/bounds，同輪產生新版 flat 與 authored 兩個測試包，只切換 `--include-navmesh`；舊正式 flat 留作回復。依 [navmesh 調查](../../projects/darksouls-port/p3/NAVMESH-INVESTIGATION-2026-09-14.md) 核對 NVMI 與 CELL 座標，再於原 crash 點及兩個跨格邊界各做 60 秒敵對追擊，確認持續靠近、可跨格、無 CTD 與新 crash log。隨從跨格跟隨另外記錄，不以敵人追擊通過代替；實機通過前不恢復自訂網格為預設。
