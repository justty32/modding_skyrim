# Mundusform 三片段借用評估

## 1. 一句話結論

navmesh 鋪 quad＝PORT；cell 快照＝SKIP；block 生成＝CONCEPT。

## 2. 三個片段的核心資料結構與演算法回顧

### navmesh 鋪 quad

`TileList` 把玩家 XY 依 `2 * quadsize` 量化去重；每格展成四頂點、兩三角形，再按 XY 與高度門檻合併頂點、搜尋同一 NAVM 的鄰邊（`analysis/tool-survey/repos/Mundusform/Undaunted/NavMeshTool.cpp:250-268`、`analysis/tool-survey/repos/Mundusform/Undaunted/NavMeshTool.cpp:87-138`、`analysis/tool-survey/repos/Mundusform/Undaunted/NavMeshTool.cpp:326-341`）。它不含跨 cell link；簡化 NVNM 仍須進 CK 改存補 grid（`analysis/tool-survey/repos/Mundusform/Undaunted/NavMeshTool.cpp:57-78`）。

### cell 快照

`RefList`／`WorldCellList` 是手動配置的 raw array 與舊 SDK pointer 容器（`analysis/tool-survey/repos/Mundusform/Undaunted/RefList.h:6-16`、`analysis/tool-survey/repos/Mundusform/Undaunted/WorldCellList.h:7-17`）。真正快照逐筆讀目前 cell 的 base FormID、position、rotation、`unk90` scale，篩類型後輸出 xEdit Pascal 或 JSON-like log（`analysis/tool-survey/repos/Mundusform/Undaunted/LocationUtils.cpp:269-335`、`analysis/tool-survey/repos/Mundusform/Undaunted/LocationUtils.cpp:337-393`）。

### block 生成

block 由 type、offset、bounding box、入口、refs、nav tiles、出口組成（`analysis/tool-survey/repos/Mundusform/Undaunted/StartupManager.cpp:93-192`）。generator 旋轉／平移候選、以 AABB 拒絕重疊、維護主支路並封 dead end；最後才把累積的 `FormRef` 逐筆 runtime spawn（`analysis/tool-survey/repos/Mundusform/Undaunted/RiftManager.cpp:139-199`、`analysis/tool-survey/repos/Mundusform/Undaunted/RiftManager.cpp:328-389`）。

## 3. API 對應與重寫比例

### 共通 API

舊端用 `TESObjectREFR*`、`TESObjectCELL*`、`TESWorldSpace*`、`PlayerCharacter*`、`NiPoint3`，並把 1.5.97 位址 `0x009951F0`（PlaceAtMe）、`0x02F26EF8`（player）、`0x01EBE428`（DataHandler）、`0x009AE5C0`（move）、`0x00194230`（LookupFormByID）餵自製 relocation（`analysis/tool-survey/repos/Mundusform/Undaunted/SKSELink.cpp:6-14`）。這些數字不能當 1.6.1170 位址直接沿用；要交由 CommonLibSSE-NG／Address Library 的現行 relocation 與型別佈局。

bridge 改用同名 `RE::` 型別；player/cell 走 `GetSingleton()`、`GetParentCell()`、`GetPosition()`（`projects/scene-capture-bridge/src/Aim.cpp:45-47`、`projects/scene-capture-bridge/src/Aim.cpp:92-105`），refs 走 `ForEachReference`、`GetBaseObject()`、`GetFormType()`、`GetScale()`（`projects/scene-capture-bridge/src/SceneExporter.Placements.cpp:57-68`、`projects/scene-capture-bridge/src/SceneExporter.Placements.cpp:117-125`），spawn/transform 走 `PlaceObjectAtMe`、`SetPosition`、`SetAngle`、`SetScale`（`projects/scene-capture-bridge/src/Palette.cpp:309-332`）。三片段沒有 `NiNode` 操作，不需新增 raw node access。

### 逐片段估算

navmesh 檔共 17 個實函式：12 個資料／量化／鄰接方法可搬演算法，5 個 config、log、Pascal export glue 應重寫，約 **5/17（29%）**；檔內沒有 runtime 記憶體讀取，但取玩家座標的 hook 另須由 `GetPlayer()->pos` 改成上述 CommonLib API（`analysis/tool-survey/repos/Mundusform/Undaunted/MyPlugin.cpp:120-130`）。

cell 快照共 5 個函式：3 個 list method 改用 STL；2 個 capture routine（**2/5，40%**）直接讀 `parentCell`、`baseForm`、`pos`、`rot`、`unk90`，必須重寫。bridge 已有 durable ID、ownership gate 與 cell sweep（`projects/scene-capture-bridge/src/SceneExporter.Placements.cpp:88-145`）。

block 三檔共 19 個實函式：18 個選塊／旋轉／平移／AABB／集合操作可保留邏輯，`BuildRift` 這 1 個 runtime executor（**1/19，5%**）必須重寫；兩個 `VMResultArray` getter 的簽名亦要機械替換。比例低估了 executor 風險，因它集中 `LookupFormByID`、`PlaceAtMe` 與 raw transform 寫入（`analysis/tool-survey/repos/Mundusform/Undaunted/RiftManager.cpp:359-386`）。

MIT 允許直接使用、修改與散布，但任何副本或 substantial portions 都必須保留 Bryn Stringer 的 copyright 與 permission notice（`analysis/tool-survey/repos/Mundusform/License:3`、`analysis/tool-survey/repos/Mundusform/License:5-13`）；這不替第三方 SDK／遊戲資產授權。

## 4. xEdit 腳本 vs 直接 writer

Mundusform 是 DLL 印 Pascal，再由 xEdit 建 REFR/NAVM；metadata 簡化且仍需 CK finalize。ModForge **能從零建立有限範圍的 NAVM**：custom exterior cell 會新建完整 vertices/triangles/grid/bounds 並掛回 CELL（`projects/ModForge/src/ModForge.Core/Build/Generator.Build.Navmesh.cs:20-70`），也會 override Skyrim.esm `0x012FB4` NAVI、補 NVMI parent/magic（同檔 `:118-155`）。但既有 interior 的 `navPatches[]` 只 clone master NAVM 後 append/stitch（`projects/ModForge/src/ModForge.Core/Build/Generator.Build.NavPatches.cs:18-58`），in-spec interior 沒有 from-zero navmesh（`projects/ModForge/src/ModForge.Core/Build/Generator.Build.NavmeshIndex.cs:85-88`）。所以 xEdit **不是捷徑**：缺的是 bridge producer 與 interior/new-NAVM contract；另加一條 metadata 更弱、需人工 finalize 的旁路只會形成第二套真相。

SkyrimIngameEditor repo 本次不可得，僅依既有 finding：其 EspGenerator 能輸出 Cell、placed 與 generic major record，但 LAND 未實作（`analysis/tool-survey/findings/skyrim-ingame-editor.md:43-52`）；沒有原始碼證據可把它外推成 NAVM/NAVI writer。

## 5. 三個判定與第一步

### 片段一：navmesh 鋪 quad — PORT

值得移植「走位取樣、格點去重、polygon preview」而非 Pascal exporter。第一步候選：在 bridge 做最小 `sc nav` registry，將採樣結果輸出為真正 `navPatches[]`，先只接受現有 ModForge interior convex-polygon contract；bridge 目前確實沒有 producer（`projects/ModForge/workflows/investigation/ingame-editor-status-audit-2026-08-25.md:145-149`）。

### 片段二：cell 快照 — SKIP

不搬碼：raw FormID、舊 enum/欄位與手工陣列都弱於 bridge 已有的 durable FormKey、ownership gate、loaded-cell exporter；重做只會複製現役能力。第一步不開新施工，沿用 `AppendPlacements`，若需求是全區快照則另規劃 unloaded-cell 邊界，而不是借 Mundusform。

### 片段三：block 生成 — CONCEPT

只借 connector＋bounding-box grammar；現階段沒有需求值得把 global state、raw arrays、非 deterministic `rand` 與 runtime spawn 鏈搬進 DLL。第一步候選：先定一個可固定 seed 的離線 prefab/block JSON spike，輸出既有 scene placements，再評估是否需要遊戲內 preview。

## 6. 與既有編輯器現況的整體關係

相較 `mundusform.md` 第五節，本次把「玩家腳下取樣 UX」從泛稱可借概念收斂為 **PORT 到 bridge producer**，因 CommonLib API 與 ModForge NAVM backend 都已有可接點；cell 快照則明確降為 **SKIP**，block grammar 維持 **CONCEPT**。沒有修正「不搬 Pascal/NVNM writer」的舊結論；scene-capture-bridge 的 `scene.json`→ModForge 邊界仍是唯一主路（`projects/scene-capture-bridge/README.md:7-11`）。

## 7. 沒查到／需實機的事

本線未 build 或啟動 1.6.1170；因此未證明新增 sampling hook 的頻率、跨樓層高度門檻、preview 與 NPC pathing。CommonLib 對上述現役 API 已有我方 source 證據，但舊 relocation constants 沒有逐一建立 1.6.1170 等價位址，因移植方案本來就應刪掉它們。ModForge 的 from-zero 證據只涵蓋 custom exterior flat NAVM/NAVI，任意 interior 新 NAVM 仍未知；xEdit script＋CK finalize 也未實測。SkyrimIngameEditor repo 本次不可得，相關比較僅依既有 finding。
