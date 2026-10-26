# 地圖移植的引擎限制與世界／內容衝突

[lessons 索引](README.md)

## dsport-render-constraints

> 移植地圖到 Skyrim 的三個引擎限制（09-13 dsp6 實證）：從零建的 WTHR 看不到雲要用原版當模板；SmallWorld 單體 >110k 單位會被 far clip；cell 水位是整格平面會淹下層樓（原 type: project）

2026-09-13 dsp6 實機定案：
1. **WTHR**：ModForge 從零建的 WTHR 就算貼圖路徑對、slot 開著也只有平灰；要以原版 WTHR（無雨用 `SkyrimClear_A 0x10E1F2`）當模板覆寫 cloud slot；雲貼圖用 DXT5；WTHR 裡的雲貼圖路徑也要驗（資產稽核只查 NIF 引用沒查 WTHR，P3 就漏了 `m18/`）。
2. **遠景**：單一 mesh 可見面離 REFR 原點 >110k 單位在 SmallWorld 會被 far clip，`Full LOD` 旗標（ModForge `fullLod`）與 ini fade 倍率都救不了；縮小拉近可見；實測 scale 0.45（最近面 ≥15k 單位）從庭院看得到山稜、0.1 像貼牆的平板。真正解法要切塊或 DynDOLOD。
3. **水**：exterior cell 的 XCLW 是整格 4096 的無限平面，多層建築會淹下層；改擺原版 `Water512/1024/2048…` ACTI 水面片（`0x0FD0CD`／`0x0CC7B8`／`0x0CC7B9`），片要按碰撞三角形 XY 投影用 512 格裁（交集 ≥30% 才留），不要用 bbox。

**How to apply:** 換地圖時這三件直接照做，不要再從零試。
相關：[[gltf2nif-effect-shader-ctd]]、[[achr-base-must-be-npc-not-lvln]]

Dark Souls→Skyrim 轉檔管線具體坑（2026-10-23 歸納）：(a) 自訂 worldspace 進場 `coc <起點標記>` 結構性不可行，要用 `cow <worldspace名> <x> <y>`＋`player.setpos z <高度值>`。(b) 純觸發/音源類物件（objbnd 無可渲染幾何）轉 glTF 再轉 NIF 會報 `glTF has no meshes`，不是工具 bug，整批排除出 placement 清單即可。(c) `convert_or_reuse()` 以 `cwd=model-converter` 啟動子程序，傳相對路徑得到 `cannot read source`，一律傳絕對路徑。(d) 同時有 `oXXXX` 與 `oXXXX_1` 兩份 FLVER 時，`_1` 通常不是 LOD 而是「破壞後型態」（8 樣本 7 個 `_1` 三角數更多），先比三角面數再決定轉不轉；MSB 只引用主 stem。(e) DS→Skyrim 旋轉必須用基底變換 `R_sky = B·R_ds·B⁻¹`，不能用「交換 Euler 軸」的捷徑，要寫共軛恆等式測試釘住（`agentctl/handoffs/done/2026-08-29/dsport/cx-ds3-HANDOFF.md:14-27`、`cx-ds2-HANDOFF.md:26-36,64-68`、`agentctl/handoffs/done/2026-09-05/dsport4-2026-09-05/STATE.md:165-166`）。

**EMEVD 初始狀態**：DS 地圖移植若只照抄 MSB 擺放資料會出錯——DS 原引擎用「同座標放兩份（完整版／破壞版），開場靠 EMEVD 關掉其中一份」表達可破壞物與劇情狀態，只讀 MSB 會把壞掉前後同時擺出來，或把短暫碰撞當永久幽靈碰撞擺死；移植前先跑 EMEVD 初始狀態過濾（找同模型同座標重複 entity、找被 Constructor 關掉的 entity）（`agentctl/handoffs/done/2026-08-30/dsport2-2026-08-30/FINDING.md:48-62`）。判斷分支確定性時：前向 `SkipLines` 類指令在 `join=i+1+line_count` 處與未跳過路徑匯流，只有 `[i+1,join)` 段算條件性，join 之後要當確定性保留；但 `ReturnIf*` 沒有 join 點，之後整段事件降為條件性——漏掉「join 後恢復確定性」會把本該確定關掉的 entity 誤判成條件性（`agentctl/handoffs/done/2026-08-30/dsport3-2026-08-30/HANDOFF-cx-dsp6.md:40-55`）。

## stat-zero-obnd-culls-large-statics

> ModForge 產的 STAT/MSTT OBND 全 0，大型 map piece 同一原點時引擎按原點淡出／剔除，出現「有碰撞沒貼圖」、天空盒／白洞從多數角度看不到（原 type: memory）

症狀（2026-09-13 dsp9 使用者實機）：地板碰撞在但看不到、天空盒很多位置角度看不見。`DSPortP3.esp` 的
STAT／ACTI／MSTT OBND 全是 (0,0,0,0,0,0)；NIF 本身的 bounding sphere 正確（`model-converter/gltf2nif/nif_writer.py`
`_bounding_sphere`），問題在 esp 記錄。DS 的 map piece 全放同一個 ANCHOR 原點，OBND=0 讓引擎把每片當原點上的
小物件做距離淡出／視錐剔除，所以離原點遠或原點不在畫面內整片消失；碰撞是另一個 STAT（`col/h####_c#.nif`）所以還在。
m9100 穹頂的「引擎 cull」很可能也是這個。

**Why:** ModForge `ee02b25` 只給 ACTI 補了 objectBounds；STAT/MSTT 從沒寫過。而且 dsp9 flatnav 版連
聲音 ACTI 的 OBND 也歸 0（validate 報 `objectBoundsMin/Max unknown field`）＝那條線跑到的 ModForge 不是
`ee02b25`，pipeline 呼叫的 ModForge 路徑要查。

**How to apply:** 任何 ModForge 產的 esp，驗收加一條「STAT/MSTT/ACTI OBND 非零」gate（解析 esp 直接數）。
修法：ModForge STAT/MSTT 支援 objectBounds，spec 從 NIF 頂點算 AABB（int16，Skyrim 單位）；重建後同點
同角度對照截圖。相關：[[dsport-render-constraints]]、[[custom-navm-combat-pathing-ctd]]。

ModForge 產生跨格 persistent placement（含觸發器/連結 ref）時，REFR/ACHR 本身與其 XESP/XLKR 連結目標都要檢查有沒有設 persistent flag（0x400）——缺了是結構合法但與 vanilla（持久物件全 persistent）相悖，只靠 refscan 的型別比對抓不到；ModForge 現已為 type-8 placement 自動補 0x400 並預判連結目標為 persistent（`agentctl/handoffs/done/2026-09/home-2026-09-13/dsp5/struct/REPORT.md:79`）。

## bloodchill-inigo-land-dirty-edit

> 2026-09-20 CC Bloodchill Manor 洞口被 Inigo.esp 的髒 LAND 009FC4 埋住；Nexus 138140 補丁會退化 navmesh 別裝；修法是只 forward Dawnguard 的 LAND，10-03 已隨 worldfix 部署（原 type: project）

Tamriel cell (14,16)／東鄰格 LAND `009FC4:Skyrim.esm`：Inigo.esp 那筆與原版 Skyrim.esm VHGT 逐位元組相同（髒編輯），洗掉 Dawnguard 為 Bloodchill 洞口挖的 200 個頂點，CC 落點 Z=1906 被地面 Z=2201 埋住。
別裝 Nexus 58317＋138140：138140 把該格 navmesh 從 277 頂點/346 三角退化成 265/341。
修法：新 ESL 只 forward Dawnguard 的 LAND（30 子記錄全同），成品在 `agentctl/handoffs/home-2026-09-20/bcfix/`。
2026-09-20 使用者曾裁「就這樣吧，那個 CC mod 我也不是很喜歡」擱置；現況是 10-03 worldfix 已部署 `Bloodchill-Inigo-Astrid-Compat-Dev-2026-09-20`，MO2 啟用中（2026-10-17 盤點查證）；部署後要 xLODGen 地形 LOD（估 50–120 分）與五條實機驗收（走出走回＋隨從跟行，不能 tcl/coc）。
houseCARL 不能逐格寫 VHGT（WriteEngine.cs Array2d 限制）。

**How to apply:** 已部署，別再當待辦；若洞口仍有問題先查 xLODGen 地形 LOD；驗收需使用者本人或前景操作（Skyrim 忽略合成輸入）。
相關：[[dyndolod-esp-masters-pin-content-mods]]

## avif-perktree-overridden-by-non-overhaul-mods

> 2026-09-20 Destruction 只剩 21 格真因：Elemental Destruction 蓋掉 Vokriinator 的 AVIF PerkTree，中文層又照抄；裝任何動 AVIF 的 mod 後要用 houseCARL 比 18 棵樹的贏家（原 type: memory）

2026-09-20 使用者回報 Destruction 天賦樹只有一小撮。真因：`Elemental Destruction.esp` 不認識 Vokriinator Black，用「原版＋自家 6 格」整筆覆蓋 `AVDestruction`／`AVEnchanting` 的 PerkTree；09-03 自製的 `ZH-AVIF-SkillNames-Dev` 中文層拿當時贏家（ED）當底 forward，於是贏家＝21 格＋中文名。Conjuration 也被 `PilgrimOrdinatorPatch`（Ordinator 底）蓋掉 Vokriinator 與 Midas 的格子。

修法（cx-perk，已裝、使用者目視 OK）：`Vokriinator-PerkTree-Restore-2026-09-20.esp`（ESL、3 override）放在所有動 AVIF 的 plugin 之後，PerkTree＝Vokriinator ∪ 原贏家，外加節點排上方獨立列、座標去重；產物在 `agentctl/handoffs/home-2026-09-20/perk/`。官方 patch 路線已死（26702 EDM patch REMOVED、ED 440 已刪）。

**Why:** 天賦總覽 mod 的樹存在 AVIF 記錄裡，任何魔法／技能 mod 只要帶自家 perk 就會整筆覆蓋 PerkTree；自製 forward 層若拿錯底會把錯誤固化成贏家。

**How to apply:** 裝或更新任何會加 perk 的 mod（法術包、Pilgrim、Midas 之類）後，刷新鏡像跑 `cross_plugin_query type=AVIF conflict_tree=true`，比 18 棵樹贏家的 perk 集合是否 ⊇ Vokriinator Black 的集合；有缺就把 Restore patch 重做（不是改 Vokriinator 本體）。自製 forward 層永遠以 Vokriinator 為底，不以「當時贏家」為底。相關：[[zh-layer-gate-base-mod-must-be-enabled]]、[[housecarl-cannot-point-real-mo2-instance]]。

## worldfix-and-mod-conflict-diagnosis-notes

> 世界/地點修正與疑難排解的五個判準：LOD 重跑看牽動範圍、NAVM 復原先查替代、patch 驗收算真正生效筆數、「bug」常是設計限制。

2026-09～10 五條教訓：(1) 地形小改動不必跑 xLODGen 地形，但 plugin 增刪牽動 LOD plugin 的 master、或外景 REFR 大量改動，TexGen/DynDOLOD/Occlusion 三件套要整套重跑（先用 TES4 MAST 掃描判斷，窗口約 1.5 小時）。(2) 每次讀檔就回寫固定設定值的效能 mod（如 SSE FPS Stabilizer）跟手動調的 ini 打架，修法是整個停用，改它的 ini 會被自己蓋回去。(3) forward_record 類世界修正 patch 驗收要逐筆跟目前贏家比對，報告「實際有效改動的筆數」，不要只報 forward 了幾筆（rigmor-ubg 15 筆裡只 2 筆真改）。(4) NAVM undelete 前查刪除者有沒有補替代 navmesh；只有「純刪除、無替代、有懸空引用/crash 證據」的才優先復原，其餘列孤島風險讓使用者裁示。(5) Custom Skills Framework 只讓一個 mod 接管原版技能選單 UI，「裝了技能樹但 Tab 看不到」常是缺統一入口 mod（如 Custom Skills Menu/Denji），不是資料層問題。來源：`agentctl/handoffs/done/2026-10/home-2026-10-03/worldfix/`（lod/ASSESS.md、data/{idlefps,idlefix,rigmor-ubg,snazzy,navmesh}/）、`agentctl/handoffs/done/2026-09/home-2026-09-29/n4batch/REPORT.md:46`

**Why:** 這些都是「表面像 bug，真因是設計/依賴關係」的模式，在不同子系統反覆出現。

**How to apply:** 世界修正部署前先查 master 牽動範圍；mod 衝突疑難先查是否回寫設定或缺統一入口；patch 類驗收一律附「實際有效改動」統計；NAVM 類復原先查替代方案。相關：[[dsport-render-constraints]]、[[avif-perktree-overridden-by-non-overhaul-mods]]
