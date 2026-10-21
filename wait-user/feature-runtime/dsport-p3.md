## DSPort P3 可見性候選（2026-10-21）

使用者本輪只允許離線修復，明確禁止螢幕、遊戲、滑鼠鍵盤；候選沒有部署。隔離分支 `dsp-winding-20261021` 的 `fcad6f5` 已完成來源與產物稽核：69 個 render NIF 每個三角面序恰反轉一次，其餘資料不變；367 項離線測試與獨立 review 通過。後續實機驗收仍 open，不能用離線綠燈宣稱可見性已修好。

候選是該隔離工作樹 `out/DSPortP3-Winding-20261021.zip`，SHA-256 `79910aff6c4f727671cae90ed6e8d5ba92ad20feb32de1a2615c0a1e87b7f47f`；同目錄 `winding-manifest.json` 記來源與前後雜湊。converter 固定 `cf12ae9`，沿用原 ModForge `0af3188` 基準 ESP；**沒有重建 ESP，也未改碰撞、貼圖或腳本**。

等使用者允許部署與遊戲操作後，先核受測包／基準雜湊，再驗牢房與進場落點的地板、牆、光柱：多角度／距離仍可見、碰撞保留，基本敵對追擊與隨從跨格不退步。範圍說明在隔離分支 `p3/WINDING.md`；本輪不執行這些步驟。

## 物件邊界歷史（2026-09-14 至 09-25；已被後續定位取代）

10-03 的 A/B 已排除舊 OBND 假說；下方保留歷史背景，不作為現役操作指令。09-25 staging 路徑目前不存在，不能照舊清單直接開跑。

地板／天空盒隨位置與視角消失、碰撞仍在；OBND 全零是已觀測資料，是否造成症狀仍待實機。離線修正與可重建步驟見 [OBND 調查](../../projects/darksouls-port/p3/OBND-INVESTIGATION-2026-09-14.md)。回家由同一版 ModForge、同一份 P3 來源產生僅 bounds 不同的對照包，先記工具／spec／ESP 雜湊，再於原先消失位置用相同視角與距離比較地板、穹頂與天空盒；確認碰撞與可見範圍無退步。保持 navmesh 模式相同，不能同時切換多層網格後把差異都歸因於 bounds。

**2026-09-25 22:2x 推進**：cx-wu-dsp 已產四包到 `~/skyrim_mods/_staging-2026-09-25/dsp/`
（bounds-A／bounds-B 除 OBND 外拓撲相同；navmesh-flat／navmesh-authored 只差 `--include-navmesh`），
雜湊在 `manifest.json`，ModForge 主樹未動；**實機比較步驟見
`agentctl/handoffs/done/2026-09/home-2026-09-25/wu/dsp/REPORT.md`，待使用者**。

## DSPort P3 多層 navmesh（2026-09-14）

2026-10-21 本輪只改 render NIF，沒有變更 navmesh；此項保持 open。下列 09-25 產物已不在原路徑，未來若重開網格驗收，須先重建可追溯對照包，不能直接執行舊路徑。

NAVI 的 NVMI owning-cell 座標離線修正不等於 CTD 已消失。回家使用同一版工具、同一份 source/spec/bounds，同輪產生新版 flat 與 authored 兩個測試包，只切換 `--include-navmesh`；舊正式 flat 留作回復。依 [navmesh 調查](../../projects/darksouls-port/p3/NAVMESH-INVESTIGATION-2026-09-14.md) 核對 NVMI 與 CELL 座標，再於原 crash 點及兩個跨格邊界各做 60 秒敵對追擊，確認持續靠近、可跨格、無 CTD 與新 crash log。隨從跨格跟隨另外記錄，不以敵人追擊通過代替；實機通過前不恢復自訂網格為預設。

**2026-09-25 22:2x 推進**：cx-wu-dsp 已產四包到 `~/skyrim_mods/_staging-2026-09-25/dsp/`
（bounds-A／bounds-B 除 OBND 外拓撲相同；navmesh-flat／navmesh-authored 只差 `--include-navmesh`），
雜湊在 `manifest.json`，ModForge 主樹未動；**實機比較步驟見
`agentctl/handoffs/done/2026-09/home-2026-09-25/wu/dsp/REPORT.md`，待使用者**。
