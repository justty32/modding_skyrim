# 專案裁示與地圖／內容限制

[lessons 索引](README.md)

## dsport-render-constraints

> 移植地圖到 Skyrim 的三個引擎限制（09-13 dsp6 實證）：從零建的 WTHR 看不到雲要用原版當模板；SmallWorld 單體 >110k 單位會被 far clip；cell 水位是整格平面會淹下層樓（原 type: project）

2026-09-13 dsp6 三線實機定案：
1. **WTHR**：ModForge 從零建的 WTHR 就算貼圖路徑對、slot 開著也只有平灰；要以原版 WTHR（無雨用 `SkyrimClear_A 0x10E1F2`）當模板覆寫 cloud slot；雲貼圖用 DXT5；另外 P3 的雲貼圖曾因 esp 路徑少 `m18/` 對不上（資產稽核只查 NIF 引用沒查 WTHR）。
2. **遠景**：單一 mesh 可見面離 REFR 原點 >110k 單位在 SmallWorld 會被 far clip，`Full LOD` 旗標（ModForge `fullLod`）與 ini fade 倍率都救不了；縮小拉近可見；dsp7 實測 scale 0.45（最近面 ≥15k 單位）從庭院看得到山稜、0.1 像貼牆的平板。真正解法要切塊或 DynDOLOD。
3. **水**：exterior cell 的 XCLW 是整格 4096 的無限平面，多層建築會淹下層；改擺原版 `Water512/1024/2048…` ACTI 水面片（`0x0FD0CD`／`0x0CC7B8`／`0x0CC7B9`），片要按碰撞三角形 XY 投影用 512 格裁（交集 ≥30% 才留），不要用 bbox（dsp7：10 池 38 片）。

**How to apply:** 換地圖時這三件直接照做，不要再從零試。
相關：[[gltf2nif-effect-shader-ctd]]、[[achr-base-must-be-npc-not-lvln]]

## stat-zero-obnd-culls-large-statics

> ModForge 產的 STAT/MSTT OBND 全 0，大型 map piece 同一原點時引擎按原點淡出／剔除，出現「有碰撞沒貼圖」、天空盒／白洞從多數角度看不到（原 type: memory）

2026-09-13 dsp9 使用者親自實機：地板碰撞在但看不到、天空盒很多位置角度看不見。頂層解析
`DSPortP3.esp`：461 個 STAT／ACTI／MSTT 的 OBND 全是 (0,0,0,0,0,0)。NIF 本身的
bounding sphere 正確（`model-converter/gltf2nif/nif_writer.py` `_bounding_sphere`），問題在 esp 記錄。
DS 的 45 個 map piece 全放同一個 ANCHOR 原點，OBND=0 讓引擎把每片當原點上的小物件做距離淡出／視錐
剔除，所以離原點遠或原點不在畫面內整片消失；碰撞是另一個 STAT（`col/h####_c#.nif`）所以還在。
dsp8 把 m9100 穹頂判成「引擎 cull 結案」，其實很可能就是這個。

**Why:** ModForge `ee02b25` 只給 ACTI 補了 objectBounds；STAT/MSTT 從沒寫過。而且 dsp9 flatnav 版連
聲音 ACTI 的 OBND 也歸 0（validate 報 `objectBoundsMin/Max unknown field`）＝那條線跑到的 ModForge 不是
`ee02b25`，pipeline 呼叫的 ModForge 路徑要查。

**How to apply:** 任何 ModForge 產的 esp，驗收加一條「STAT/MSTT/ACTI OBND 非零」gate（解析 esp 直接數）。
修法：ModForge STAT/MSTT 支援 objectBounds，spec 從 NIF 頂點算 AABB（int16，Skyrim 單位）；重建後同點
同角度對照截圖。相關：[[dsport-render-constraints]]、[[custom-navm-combat-pathing-ctd]]。

## bloodchill-inigo-land-dirty-edit

> 2026-09-20 CC Bloodchill Manor 洞口被 Inigo.esp 的髒 LAND 009FC4 埋住；Nexus 138140 補丁會退化 navmesh 別裝；修法是只 forward Dawnguard 的 LAND，10-03 已隨 worldfix 部署（原 type: project）

Tamriel cell (14,16)／東鄰格 LAND `009FC4:Skyrim.esm`：Inigo.esp 那筆與原版 Skyrim.esm VHGT 逐位元組相同（髒編輯），洗掉 Dawnguard 為 Bloodchill 洞口挖的 200 個頂點，CC 落點 Z=1906 被地面 Z=2201 埋住。
方案 E（Nexus 58317＋138140）被 cx-bcfix 推翻：138140 把該格 navmesh 從 277 頂點/346 三角退化成 265/341。
採用：新 ESL 只 forward Dawnguard 的 LAND（30 子記錄全同），成品在 `agentctl/handoffs/home-2026-09-20/bcfix/`，
**2026-09-20 12:10 使用者裁「就這樣吧，那個 CC mod 我也不是很喜歡」＝擱置不部署**；**後來 10-03 worldfix 已部署 `Bloodchill-Inigo-Astrid-Compat-Dev-2026-09-20`，MO2 啟用中（2026-10-17 盤點查證）**；部署後要 xLODGen 地形 LOD（估 50–120 分）與五條實機驗收（走出走回＋隨從跟行，不能 tcl/coc）。
houseCARL 不能逐格寫 VHGT（WriteEngine.cs Array2d 限制）。

**How to apply:** 已部署，別再當待辦；若洞口仍有問題先查 xLODGen 地形 LOD；驗收需使用者本人或前景操作（Skyrim 忽略合成輸入）。（2026-10-23 依記憶條目更新部署狀態）
相關：[[dyndolod-esp-masters-pin-content-mods]]

## avif-perktree-overridden-by-non-overhaul-mods

> 2026-09-20 Destruction 只剩 21 格真因：Elemental Destruction 蓋掉 Vokriinator 的 AVIF PerkTree，中文層又照抄；裝任何動 AVIF 的 mod 後要用 houseCARL 比 18 棵樹的贏家（原 type: memory）

2026-09-20 使用者回報 Destruction 天賦樹只有一小撮。真因：`Elemental Destruction.esp` 不認識 Vokriinator Black，用「原版＋自家 6 格」整筆覆蓋 `AVDestruction`／`AVEnchanting` 的 PerkTree；09-03 自製的 `ZH-AVIF-SkillNames-Dev` 中文層拿當時贏家（ED）當底 forward，於是贏家＝21 格＋中文名。Conjuration 也被 `PilgrimOrdinatorPatch`（Ordinator 底）蓋掉 Vokriinator 與 Midas 的格子。

修法（cx-perk，已裝、使用者目視 OK）：`Vokriinator-PerkTree-Restore-2026-09-20.esp`（ESL、3 override）放在所有動 AVIF 的 plugin 之後，PerkTree＝Vokriinator ∪ 原贏家，外加節點排上方獨立列、座標去重；產物在 `agentctl/handoffs/home-2026-09-20/perk/`。官方 patch 路線已死（26702 EDM patch REMOVED、ED 440 已刪）。

**Why:** 天賦總覽 mod 的樹存在 AVIF 記錄裡，任何魔法／技能 mod 只要帶自家 perk 就會整筆覆蓋 PerkTree；自製 forward 層若拿錯底會把錯誤固化成贏家。

**How to apply:** 裝或更新任何會加 perk 的 mod（法術包、Pilgrim、Midas 之類）後，刷新鏡像跑 `cross_plugin_query type=AVIF conflict_tree=true`，比 18 棵樹贏家的 perk 集合是否 ⊇ Vokriinator Black 的集合；有缺就把 Restore patch 重做（不是改 Vokriinator 本體）。自製 forward 層永遠以 Vokriinator 為底，不以「當時贏家」為底。相關：[[zh-layer-gate-base-mod-must-be-enabled]]、[[housecarl-cannot-point-real-mo2-instance]]。

## new-save-plan-2026-10-04

> 使用者 10-04 說要開新檔並陸續提新檔前的改動；10-08 調查＋施工完成（拔 Rigmor／FC／Spell Research／Biggie／SkyInteract、IFD Lydia→FDE、DynDOLOD 整組停用），待新檔實機確認

2026-10-04 使用者說要開新檔，並開始列新檔前想做的改動，說「還有其他的，稍微等我」，但當天沒說完就收工。清單權威來源：母 repo 頂層 `play-notes.md`（使用者自己寫，10-08 內容）：刪 rigmor 兩個、spell research、forgotten city、biggie traits；Improved Follower Dialogue - Lydia 要換一個（bug／衝突多、有些台詞靜音、OOC）。

**Why:** 使用者要一次說完再施工（見 [[investigate-all-then-install-once]]）。

**How to apply:** 下次 session 先問使用者其餘新檔想法，收齊後整理成清單給他確認再派線；刪 mod 前查 DynDOLOD.esp／Occlusion.esp 的 master（[[dyndolod-esp-masters-pin-content-mods]]）與同概念兄弟。同日已做：OBody 隨從黑名單＋Zeroed preset 排除、Aniya 皮膚修正、launch-mo2.sh 快取變數（HUD 預設關），報告在 `agentctl/handoffs/home-2026-10-04/`。

10-08 調查完成（`agentctl/handoffs/home-2026-10-08/newsave/REPORT-{quests,systems,lydia}.md`），使用者裁示：Lydia 換 FDE Lydia 1.5＋簡中（安裝包已在庫）；拔 Rigmor 後恢復原版邊境隱形牆（不補 `bBorderRegionsEnabled`）；SkyInteract 隨 Biggie 一起拔。施工要點：Rigmor 與 IFD Lydia 被 DynDOLOD／Occlusion 釘 master → 合併重跑一次 TexGen+DynDOLOD；IFD 另被 `JhNPCBeautyDev.esp`×2、Lydia-Look-From 換臉層當 master，ESLify-Overlay 內有 IFD 修正層副本。

10-08 施工完成（profiles `2cdbf1a`，REPORT-build.md）：39 mod／26 plugin 停用，FDE Lydia 上線，**DynDOLOD 整組停用**（含 Resources、TexGen Fixes；使用者裁「很想停掉」遠景→以後拔 mod 不用重跑 LOD）。待使用者新檔實機確認：Lydia 語音／外觀、主選單外的實際遊玩。殘留未清：OBody 黑名單與 IGYH FLM ini 內的 IFD／Rigmor 條目（無害）。

## campfire-deferred-to-next-playthrough

> 2026-10-10 使用者裁「campfire 下個新檔吧」；Campfire 一族留到下一個新周目一次裝，現周目不裝

2026-10-10 使用者原話「campfire下個新檔吧」。現周目只裝了 Dovah Rider Carriage＋Simple Hunting Overhaul＋DAK（profiles `c3a4321`），Campfire 不裝。

下個新周目要一起評估的包：Campfire 667（排除包內舊 PapyrusUtil.dll）＋Script Optimization 149913，或改用 Campfire 2026（193929，ESL 版只能新檔，含 DAK／SHO 補丁，10-10 時太新：10/3 發布 6 天 5 版）；Survival Skills CSF（171040，接現役 CSF 選單）；可選 Skills of the Wild 37693（會拿掉羅盤）。Frostfall 不裝。調查細節：`agentctl/handoffs/2026-10-10/campfire-frostfall/REPORT.md`。

**Why:** Campfire 的 ESL 版與 Survival Skills 都偏好新檔，中途加裝風險高。

**How to apply:** 使用者說要開新周目時，把這包列進新檔清單一起調查施工（[[investigate-all-then-install-once]]），屆時重查 Campfire 2026 的 bug 頁與版本穩定度。

## self-made-vs-repack-classification

> 2026-10-10 使用者定的 mod 分類：別人 mod 的重包／改版算原作，只有自己從零做的（patch 等）才算自製；中文層另歸漢化

使用者原話（2026-10-10）：「我們修改過的版本，類似這種重包的，都算原作。只有我們自己做的，包括patch等，才算自製」。

**Why:** 頁面篩選「只看非漢化包和自製的」要能看到所有第三方內容；Katana Flattened 這類重包被算成自製就看不到了。

**How to apply:** 分類規則（共用來源 `mod-library/viewer/content_class.py`）：重包、改條件版、修正重包 → 第三方原作；patch、相容件、合併層、overlay、換臉層、轉發層等從零自製 → 自製；中文翻譯層 → 漢化。各頁產頁腳本都要對齊這份規則。

同日補充判準（使用者原話）：「只要我們動過後，那個檔案仍對標於原作檔，那就算」原作——修正層只覆蓋原作同路徑檔（如 Facegen/Mesh-Texture-Fix-Combined、SmeltingPlus-Fix、JH NPC Beauty Dev）算原作；換臉層算自製（使用者確認）。
