# 地圖移植的引擎限制與世界／內容衝突

[lessons 索引](README.md)｜DS 轉檔管線與 EMEVD 初始狀態見 [porting-and-modforge](porting-and-modforge.md#asset-porting-feasibility-checklist)

## dsport-render-constraints

> 移植地圖到 Skyrim 的三個引擎限制（09-13 dsp6 實證）：從零建的 WTHR 看不到雲要用原版當模板；SmallWorld 單體 >110k 單位會被 far clip；cell 水位是整格平面會淹下層樓

2026-09-13 dsp6 實機定案，換地圖時直接照做：
1. **WTHR**：ModForge 從零建的 WTHR 就算貼圖路徑對、slot 開著也只有平灰；以原版 WTHR（無雨用 `SkyrimClear_A 0x10E1F2`）當模板覆寫 cloud slot；雲貼圖用 DXT5；資產稽核要連 WTHR 裡的雲貼圖路徑一起驗（只查 NIF 引用會漏）。
2. **遠景**：單一 mesh 可見面離 REFR 原點 >110k 單位在 SmallWorld 會被 far clip，`Full LOD` 旗標（ModForge `fullLod`）與 ini fade 倍率都救不了；縮小拉近可見（scale 0.45、最近面 ≥15k 單位從庭院看得到山稜，0.1 像貼牆平板）；真正解法是切塊或 DynDOLOD。
3. **水**：exterior cell 的 XCLW 是整格 4096 的無限平面，多層建築會淹下層；改擺原版 `Water512/1024/2048…` ACTI 水面片（`0x0FD0CD`／`0x0CC7B8`／`0x0CC7B9`），按碰撞三角形 XY 投影以 512 格裁（交集 ≥30% 才留），不用 bbox。

相關：[[gltf2nif-effect-shader-ctd]]、[[achr-base-must-be-npc-not-lvln]]

## stat-zero-obnd-culls-large-statics

> ModForge 產的 STAT/MSTT OBND 全 0，大型 map piece 同一原點時引擎按原點淡出／剔除，出現「有碰撞沒貼圖」、天空盒／白洞從多數角度看不到

2026-09-13 dsp9 使用者實機：`DSPortP3.esp` 的 STAT／ACTI／MSTT OBND 全是 0；NIF 的 bounding sphere 正確（`model-converter/gltf2nif/nif_writer.py` `_bounding_sphere`），問題在 esp 記錄。DS 的 map piece 全放同一個 ANCHOR 原點，OBND=0 讓引擎把每片當原點上的小物件做距離淡出／視錐剔除，原點離遠或不在畫面內整片消失；碰撞是另一個 STAT（`col/h####_c#.nif`）所以還在。穹頂類「引擎 cull」先疑這個。ModForge `ee02b25` 只給 ACTI 補了 objectBounds；validate 報 `objectBoundsMin/Max unknown field` 表示 pipeline 呼叫到的 ModForge 不是這版，要查路徑。

**How to apply:** ModForge 產的 esp，驗收加「STAT/MSTT/ACTI OBND 非零」gate（解析 esp 直接數）。修法：ModForge STAT/MSTT 支援 objectBounds，spec 從 NIF 頂點算 AABB（int16，Skyrim 單位）；重建後同點同角度對照截圖。相關：[[dsport-render-constraints]]、[[custom-navm-combat-pathing-ctd]]。

ModForge 產跨格 persistent placement（含觸發器／連結 ref）時，REFR/ACHR 本身與其 XESP/XLKR 連結目標都要有 persistent flag（0x400）；缺了結構合法但與 vanilla 相悖，refscan 的型別比對抓不到。ModForge 現已為 type-8 placement 自動補 0x400 並預判連結目標為 persistent（`agentctl/handoffs/done/2026-09/home-2026-09-13/dsp5/struct/REPORT.md:79`）。

## bloodchill-inigo-land-dirty-edit

> 2026-09-20 CC Bloodchill Manor 洞口被 Inigo.esp 的髒 LAND 009FC4 埋住；Nexus 138140 補丁會退化 navmesh 別裝；修法是只 forward Dawnguard 的 LAND，10-03 已隨 worldfix 部署

Tamriel cell (14,16)／東鄰格 LAND `009FC4:Skyrim.esm`：Inigo.esp 那筆與 Skyrim.esm VHGT 逐位元組相同（髒編輯），洗掉 Dawnguard 為洞口挖的頂點，CC 落點被地面埋住。別裝 Nexus 58317＋138140（138140 會退化該格 navmesh）。修法是新 ESL 只 forward Dawnguard 的 LAND（成品 `agentctl/handoffs/home-2026-09-20/bcfix/`）；houseCARL 不能逐格寫 VHGT（WriteEngine.cs Array2d 限制）。

使用者 2026-09-20 曾裁「就這樣吧，那個 CC mod 我也不是很喜歡」；現況 `Bloodchill-Inigo-Astrid-Compat-Dev-2026-09-20` 已隨 10-03 worldfix 部署、MO2 啟用中（2026-10-17 查證），別再當待辦。部署後要跑 xLODGen 地形 LOD 與五條實機驗收（走出走回＋隨從跟行，不能 tcl/coc），洞口仍有問題先查地形 LOD；驗收要使用者本人或前景操作（Skyrim 忽略合成輸入）。相關：[[dyndolod-esp-masters-pin-content-mods]]

## avif-perktree-overridden-by-non-overhaul-mods

> 2026-09-20 Destruction 只剩 21 格真因：Elemental Destruction 蓋掉 Vokriinator 的 AVIF PerkTree，中文層又照抄；裝任何動 AVIF 的 mod 後要用 houseCARL 比 18 棵樹的贏家

天賦樹存在 AVIF 記錄裡，帶自家 perk 的魔法／技能 mod 會用「原版＋自家 6 格」這類整筆覆蓋 PerkTree（`Elemental Destruction.esp` 蓋 `AVDestruction`／`AVEnchanting`，`PilgrimOrdinatorPatch` 蓋 Conjuration）；自製 forward 層（如 `ZH-AVIF-SkillNames-Dev`）拿「當時贏家」當底會把錯誤固化成贏家。

修法（已裝、使用者目視 OK）：`Vokriinator-PerkTree-Restore-2026-09-20.esp`（ESL、3 override）排在所有動 AVIF 的 plugin 之後，PerkTree＝Vokriinator ∪ 原贏家，外加節點排上方獨立列、座標去重；產物 `agentctl/handoffs/home-2026-09-20/perk/`。官方 patch 路線已死（26702 EDM patch REMOVED、ED 440 已刪）。

**How to apply:** 裝或更新任何會加 perk 的 mod 後，刷新鏡像跑 `cross_plugin_query type=AVIF conflict_tree=true`，比 18 棵樹贏家的 perk 集合是否 ⊇ Vokriinator Black；有缺就重做 Restore patch（不改 Vokriinator 本體）。自製 forward 層永遠以 Vokriinator 為底。相關：[[zh-layer-gate-base-mod-must-be-enabled]]、[[housecarl-cannot-point-real-mo2-instance]]。

## worldfix-and-mod-conflict-diagnosis-notes

> 世界/地點修正與疑難排解的五個判準：LOD 重跑看牽動範圍、NAVM 復原先查替代、patch 驗收算真正生效筆數、「bug」常是設計限制。

「表面像 bug，真因是設計/依賴關係」的五種：
1. 地形小改動不必跑 xLODGen 地形；plugin 增刪牽動 LOD plugin 的 master、或外景 REFR 大量改動，TexGen/DynDOLOD/Occlusion 整套重跑（先用 TES4 MAST 掃描判斷，約 1.5 小時）。
2. 每次讀檔就回寫固定設定的效能 mod（如 SSE FPS Stabilizer）跟手調 ini 打架，修法是整個停用，改它的 ini 會被蓋回。
3. forward_record 類世界修正 patch 驗收逐筆跟目前贏家比，報「實際有效改動的筆數」，不只報 forward 幾筆。
4. NAVM undelete 前查刪除者有沒有補替代 navmesh；只有「純刪除、無替代、有懸空引用/crash 證據」的優先復原，其餘列孤島風險給使用者裁示。
5. Custom Skills Framework 只讓一個 mod 接管技能選單 UI，「裝了技能樹但 Tab 看不到」常是缺統一入口 mod（如 Custom Skills Menu/Denji）。

來源：`agentctl/handoffs/done/2026-10/home-2026-10-03/worldfix/`（lod/ASSESS.md、data/{idlefps,idlefix,rigmor-ubg,snazzy,navmesh}/）、`agentctl/handoffs/done/2026-09/home-2026-09-29/n4batch/REPORT.md:46`。相關：[[dsport-render-constraints]]、[[avif-perktree-overridden-by-non-overhaul-mods]]
