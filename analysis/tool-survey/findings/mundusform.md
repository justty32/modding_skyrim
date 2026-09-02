# Mundusform — Tool Survey Finding

**Source**: https://github.com/kaosnyrb/Mundusform  
**Author**: kaosnyrb / Bryn Stringer｜**Version**: v1（2020-06-16）｜**License**: MIT  
**Surveyed**: 2026-09-02（本機 shallow clone 原始碼檢視；未 build／未實機）

## 1. 一句話結論

可借概念，不可直接用：玩家走位粗鋪 navmesh 與 connector/bounding-box block grammar 有研究價值，但現成 DLL／export 鏈停在 1.5.97-era 且缺完整 NAVM/NAVI、跨 cell 與 1.6.1170 證據。

## 2. 它做什麼、怎麼做

**玩家走位 navmesh。** Papyrus effect 每 0.1 秒呼叫 `CaptureNavTile()`，native hook 取玩家座標交給
`MarkTile()`（`analysis/tool-survey/repos/Mundusform/datafiles/Source/Scripts/Mundusform_NavTileCapture.psc:5-10`；
`analysis/tool-survey/repos/Mundusform/Undaunted/MyPlugin.cpp:120-124`）。座標以 `2 * quadsize` 量化、同格只記一次；
每格中心向四角展開成一個 quad、拆成兩個三角形（`analysis/tool-survey/repos/Mundusform/Undaunted/NavMeshTool.cpp:250-278`、
`:87-140`）。相同 XY 且 `|ΔZ| < NavmeshCorriderHeight` 的角點共用 vertex；再以反向共邊搜尋 triangle index，
找不到就留 `-1` 邊界（同檔 `:326-341`、`:373-429`）。因此只會連同一張 mesh 內、垂直差在門檻內的相鄰格；
沒有跨 CELL `EdgeLink`。`ExportNavmesh()` 把 Pascal `Process(CELL)`、NVNM vertices/triangles 寫到
`Navmesh.pas`（同檔 `:71-78`、`:147-162`），但只設 `Parent Cell` 與 `NavMeshGrid='00'`；作者註解也要求進
CK 稍改再存，否則缺 grid 會造成 memory leak（同檔 `:57-59`）。它是 rough-out，不是可直接出貨的 finalize。

**方塊式程序化地城。** `LoadBlocks()` 從 JSON 讀 block type、offset、bounding box、入口、references、
nav tiles 與出口（`analysis/tool-survey/repos/Mundusform/Undaunted/StartupManager.cpp:93-195`）。`Work()` 洗牌後依 connector
type 選 hall/room，旋轉、平移，拒絕 bounding-box 重疊，維護主路與支路，最後用 dead-end 封口
（`analysis/tool-survey/repos/Mundusform/Undaunted/RiftManager.cpp:210-325`）；`PlaceBlock()` 同時合併 refs 與 nav tiles
（同檔 `:181-199`）。`BuildRift()` 最後以 `PlaceAtMe` 建 runtime references（同檔 `:328-389`）。README 所稱
xEdit 成品需再走快照/export；`BuildRift()` 本身沒有直接寫 ESP。

**Cell 快照。** `CaptureArea()` 掃目前 cell、篩選可放置類型，記 base FormID、position、rotation、scale，輸出
`UndauntedRift.pas`：建立新 CELL、加 REFR，並附上目前 navmesh chunk
（`analysis/tool-survey/repos/Mundusform/Undaunted/LocationUtils.cpp:269-335`）。另有 `CaptureAreaJson()` 把 refs 與 nav tiles
印成 block 用的 JSON-like rows（同檔 `:337-393`），但未自行開獨立 JSON 檔。

## 3. 資料流

```mermaid
flowchart LR
    A[玩家移動] --> B[Papyrus 每 0.1 秒 CaptureNavTile]
    B --> C[MarkTile 量化並去重 TileList]
    C --> D[ExportNavmesh 或 CaptureArea]
    D --> E[Navmesh.pas / UndauntedRift.pas]
    E --> F[xEdit Process 目標 CELL]
    F --> G[ESP 的 REFR / NAVM]
```

注意：現行 `hook_ExportNavMesh()` 實際呼叫 `CaptureAreaJson()`，`ExportNavmesh()` 被註解
（`analysis/tool-survey/repos/Mundusform/Undaunted/MyPlugin.cpp:126-131`），所以上圖是存在的 producer 路徑，不代表按鈕已接通。

## 4. 建置與 runtime

專案是 MSVC v142、C++17 DLL，直接 project-reference repo 內的 `skse64`／`skse64_common`
（`analysis/tool-survey/repos/Mundusform/Undaunted/Undaunted.vcxproj:29-38`、`:152-157`）。SDK 版本來源是
`analysis/tool-survey/repos/Mundusform/skse64_common/skse_version.h:5-10`，明列 SKSE **2.0.17**、target runtime
**1.5.97**（同檔 `:42-43`）。addrlib 依賴在 `analysis/tool-survey/repos/Mundusform/Undaunted/SKSELink.h:21-26`；
`VersionDb::Load()` 依 executable version 尋找 `version-X-X-X-X.bin`，缺檔即失敗
（`analysis/tool-survey/repos/Mundusform/Undaunted/addrlib/versiondb.h:167-186`），plugin query 也會因初始化失敗拒載
（`analysis/tool-survey/repos/Mundusform/Undaunted/main.cpp:38-48`）。repo 只附 `version-1-5-97-0.bin`，故現成 DLL 對
1.6.1170 **不可直接用**。移植至少要換成支援 1.6.1170 的 SKSE ABI／relocation 層並重審直接欄位存取；僅重編不足，
精確工量無 build/runtime 證據不能量化。

## 5. 與我們四個接點的關係

### ModForge navmesh／DSPortP2b

ModForge 已能直接建立每 cell 的平面 NAVM/NAVI，並為正交相鄰 cell 建雙向
external edge links（`projects/ModForge/src/ModForge.Core/Build/Generator.Build.Navmesh.cs:20-70`、`:73-116`）；
DSPortP2b 的跨格結果仍只有離線證據（`agentctl/SESSION-LOG.md:91-99`）。Mundusform 沒有 NAVI／跨 CELL links，
不能補這個 runtime 驗收缺口；可借的是玩家腳下取樣 UX。

### scene-capture-bridge

我方以 CommonLibSSE-NG/C++23 讀 runtime refs，轉 durable FormKey 後輸出可直接餵
ModForge 的 `scene.json`（`projects/scene-capture-bridge/README.md:7-11`）；現行 exporter 還以 ownership gate 排除
vanilla、engine dynamic refs 與 actors（`projects/scene-capture-bridge/src/SceneExporter.Placements.cpp:88-145`）。Mundusform
是「整 cell 篩類型 → raw FormID → xEdit Pascal」，資料契約較脆；其 ghost/preview 也不及我方已存在的即時 ghost
（`projects/scene-capture-bridge/src/Preview.cpp:200-235`）。

### darksouls-port

我方是忠實讀 MSB Object、套 EMEVD 初始狀態排除，再做座標／旋轉轉換成 placements
（`projects/darksouls-port/tools/obj_placements.py:25-60`；`projects/darksouls-port/tools/ds_transform.py:87-110`）；
Mundusform 則從 block grammar 隨機選 tile。兩者只在「base＋transform 列表」重疊；生成邏輯互補，但與目前 DS
場景重現目標無關。

### xEdit script vs 直接 writer

Mundusform 少寫 binary serializer，且輸出可在標準工具續編；代價是多一個人工
Process/CK finalize、raw FormID 與不完整 NAVM metadata。ModForge 的 JSON 經 validate/build 後由 `PluginIo` 直接寫
`.esp`（`projects/ModForge/workflows/common/code-map/CODE_MAP.md:57-63`），較可重建，但 TES record invariants 都由我方維護。

## 6. 可借概念／可行的下一步

planning 候選只有三項：把「走位取樣＋高度門檻」改成 scene-capture-bridge 的明確 polygon/preview UX；把 block 的
connector＋bounding-box schema 當未來程序化 prefab grammar 參考；若真要復用演算法，先做輸出到 ModForge JSON 的
小型 spike，不沿用 Pascal/NVNM writer。MIT 允許使用、修改、合併與散布作者程式碼，但副本或 substantial portions
須保留 copyright/permission notice（`analysis/tool-survey/repos/Mundusform/License:5-13`）；這不自動涵蓋隨附第三方 SDK
或遊戲資產。

## 7. 沒查到／需驗證的事

- 未 build、未在 1.5.97 或 1.6.1170 載入，無法證明現行 source/package 可運作。
- `ExportNavMesh` hook 與 README 流程不一致；xEdit script、CK finalize 後的 NAVM 正確性及 memory leak 均未驗。
- 未找到跨 CELL、外景 parent/NAVI、cover、door triangle 或完整 grid/bounds 的 exporter；不能推定 NPC 可跨格。
- `CaptureAreaJson()` 只見 log rows，從它產生可重載 block JSON 的人工步驟與錯誤處理未文件化。
