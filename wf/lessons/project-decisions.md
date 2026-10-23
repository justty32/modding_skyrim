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

2026-10-23 補四條 Dark Souls→Skyrim 轉檔管線具體坑：(a) 自訂 worldspace 進場 `coc <起點標記>` 結構性不可行，要用 `cow <worldspace名> <x> <y>`＋`player.setpos z <高度值>`。(b) 純觸發/音源類物件（objbnd 無可渲染幾何）轉 glTF 再轉 NIF 會報 `glTF has no meshes`，不是工具 bug，整批排除出 placement 清單即可。(c) `convert_or_reuse()` 以 `cwd=model-converter` 啟動子程序，傳相對路徑得到 `cannot read source`，一律傳絕對路徑。(d) 同時有 `oXXXX` 與 `oXXXX_1` 兩份 FLVER 時，`_1` 通常不是 LOD 而是「破壞後型態」（8 樣本 7 個 `_1` 三角數更多），先比三角面數再決定轉不轉；MSB 只引用主 stem。(e) DS→Skyrim 旋轉必須用基底變換 `R_sky = B·R_ds·B⁻¹`，不能用「交換 Euler 軸」的捷徑，要寫共軛恆等式測試釘住（`agentctl/handoffs/done/2026-08-29/dsport/cx-ds3-HANDOFF.md:14-27`、`cx-ds2-HANDOFF.md:26-36,64-68`、`agentctl/handoffs/done/2026-09-05/dsport4-2026-09-05/STATE.md:165-166`）。

2026-10-23 補：**EMEVD 初始狀態**：DS 地圖移植若只照抄 MSB 擺放資料會出錯——DS 原引擎用「同座標放兩份（完整版／破壞版），開場靠 EMEVD 關掉其中一份」表達可破壞物與劇情狀態，只讀 MSB 會把壞掉前後同時擺出來，或把短暫碰撞當永久幽靈碰撞擺死；移植前先跑 EMEVD 初始狀態過濾（找同模型同座標重複 entity、找被 Constructor 關掉的 entity）（`agentctl/handoffs/done/2026-08-30/dsport2-2026-08-30/FINDING.md:48-62`）。判斷分支確定性時：前向 `SkipLines` 類指令在 `join=i+1+line_count` 處與未跳過路徑匯流，只有 `[i+1,join)` 段算條件性，join 之後要當確定性保留；但 `ReturnIf*` 沒有 join 點，之後整段事件降為條件性——漏掉「join 後恢復確定性」會把本該確定關掉的 entity 誤判成條件性（`agentctl/handoffs/done/2026-08-30/dsport3-2026-08-30/HANDOFF-cx-dsp6.md:40-55`）。

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

2026-10-23 補：ModForge 產生跨格 persistent placement（含觸發器/連結 ref）時，REFR/ACHR 本身與其 XESP/XLKR 連結目標都要檢查有沒有設 persistent flag（0x400）——DSPortP3 曾出現結構合法但與 vanilla（持久物件全 persistent）相悖的缺失，只靠 refscan 的型別比對過不了關；ModForge 現已為 type-8 placement 自動補 0x400 並預判連結目標為 persistent（`agentctl/handoffs/done/2026-09/home-2026-09-13/dsp5/struct/REPORT.md:79`）。

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

2026-10-18 補：Campfire 安裝包內含的 `SKSE/Plugins/PapyrusUtil.dll` 會與現役已裝版本衝突——這是非 .esp 層級的衝突，常規 esp 層面的衝突檢查會漏掉，現役雖未裝但一裝即踩。下次新周目真的要裝 Campfire（含 Campfire 2026／Survival Skills CSF）時，安裝步驟要加一條：手動排除該 mod 包裡的 PapyrusUtil.dll，不要整包覆蓋安裝。
source: modpack-design/sources/OPEN.md:18

## self-made-vs-repack-classification

> 2026-10-10 使用者定的 mod 分類：別人 mod 的重包／改版算原作，只有自己從零做的（patch 等）才算自製；中文層另歸漢化

使用者原話（2026-10-10）：「我們修改過的版本，類似這種重包的，都算原作。只有我們自己做的，包括patch等，才算自製」。

**Why:** 頁面篩選「只看非漢化包和自製的」要能看到所有第三方內容；Katana Flattened 這類重包被算成自製就看不到了。

**How to apply:** 分類規則（共用來源 `mod-library/viewer/content_class.py`）：重包、改條件版、修正重包 → 第三方原作；patch、相容件、合併層、overlay、換臉層、轉發層等從零自製 → 自製；中文翻譯層 → 漢化。各頁產頁腳本都要對齊這份規則。

同日補充判準（使用者原話）：「只要我們動過後，那個檔案仍對標於原作檔，那就算」原作——修正層只覆蓋原作同路徑檔（如 Facegen/Mesh-Texture-Fix-Combined、SmeltingPlus-Fix、JH NPC Beauty Dev）算原作；換臉層算自製（使用者確認）。

2026-10-23 補：這條分類規則不等於授權規則——動畫/moveset 格式轉換（如 MCO→BFCO）查證 Nexus 授權頁顯示「私人轉換僅供自用可以，轉換後再發布不被允許」，跟「整包分發」是兩條獨立的授權問題；任何涉及格式轉換/移植的調查，授權查證要分別寫清楚「自用轉換」vs「整包分發」各自的結論，不要用其中一個代表全部（`analysis/mod-survey/action-system/findings/mco-to-bfco-conversion/costs-and-validation.md:27,61-64,113-115`）。


## safe-refactor-characterization-and-extract-method

> 重構前用原檔產生 golden 並 byte-equal 比對，但 byte-equal 在跨平台/CRLF 情境會騙人；抽方法時 continue／具名引數委派編譯器不會報錯卻會執行期出錯。

2026-09-02～09-25 三條教訓：(1) 拆 >300 行工具前先用 fixture 跑 CLI 產生 golden（在原檔上先跑綠），拆後輸出含 exit code byte-equal；沒有已追蹤 fixture 的函式（NIF、DLL、Mongo）要明列殘餘風險（`agentctl/handoffs/done/2026-09-25/tidy-2026-09-25/team-code/REPORT.md:31,52-54`）。(2) Windows 上 python 文字 stdout 會變 CRLF，CLI 原始輸出跟 `--out` 檔／API 輸出不是 byte-identical，但兩次 CLI 互比又一致，驗收抓不到；要比「CLI stdout＝檔案＝API」三者，輸出走 `sys.stdout.buffer.write(...encode("utf-8"))`（`agentctl/handoffs/done/2026-09-02/spike-2026-09-02/REPORT.md:132-136`）。(3) extract-method 兩陷阱：迴圈內 continue 抽出後要改 `return null`＋呼叫端補 `if (x is null) continue`；具名引數傳給 `Action<>` 委派要改位置引數（委派參數名是 arg1..argN）；捕獲多個外層可變變數的區塊優先不抽（`agentctl/handoffs/done/2026-08-27/opus-modforge/RESULTS.md:51`）。

**Why:** 這些陷阱編譯器都不報錯，只有實際執行/跨平台情境才現形。

**How to apply:** 重構交接書寫死 golden-on-original 流程；byte-identical 驗收一律三方比對並確認輸出走 bytes；extract-method 前先掃 continue/break 與具名引數委派呼叫。

## worldfix-and-mod-conflict-diagnosis-notes

> 世界/地點修正與疑難排解的五個判準：LOD 重跑看牽動範圍、NAVM 復原先查替代、patch 驗收算真正生效筆數、「bug」常是設計限制。

2026-09～10 五條教訓：(1) 地形小改動不必跑 xLODGen 地形，但 plugin 增刪牽動 LOD plugin 的 master、或外景 REFR 大量改動，TexGen/DynDOLOD/Occlusion 三件套要整套重跑（先用 TES4 MAST 掃描判斷，窗口約 1.5 小時）。(2) 每次讀檔就回寫固定設定值的效能 mod（如 SSE FPS Stabilizer）跟手動調的 ini 打架，修法是整個停用，改它的 ini 會被自己蓋回去。(3) forward_record 類世界修正 patch 驗收要逐筆跟目前贏家比對，報告「實際有效改動的筆數」，不要只報 forward 了幾筆（rigmor-ubg 15 筆裡只 2 筆真改）。(4) NAVM undelete 前查刪除者有沒有補替代 navmesh；只有「純刪除、無替代、有懸空引用/crash 證據」的才優先復原，其餘列孤島風險讓使用者裁示。(5) Custom Skills Framework 只讓一個 mod 接管原版技能選單 UI，「裝了技能樹但 Tab 看不到」常是缺統一入口 mod（如 Custom Skills Menu/Denji），不是資料層問題。來源：`agentctl/handoffs/done/2026-10/home-2026-10-03/worldfix/`（lod/ASSESS.md、data/{idlefps,idlefix,rigmor-ubg,snazzy,navmesh}/）、`agentctl/handoffs/done/2026-09/home-2026-09-29/n4batch/REPORT.md:46`

**Why:** 這些都是「表面像 bug，真因是設計/依賴關係」的模式，在不同子系統反覆出現。

**How to apply:** 世界修正部署前先查 master 牽動範圍；mod 衝突疑難先查是否回寫設定或缺統一入口；patch 類驗收一律附「實際有效改動」統計；NAVM 類復原先查替代方案。相關：[[dsport-render-constraints]]、[[avif-perktree-overridden-by-non-overhaul-mods]]

## verify-before-acting-process-rigor

> 施工前先驗證：隱性基線要寫下來、QA 多項不可互相外推、升級第三方庫要查授權不只 API、舊報告的版本假設要重查、想動實體路徑先問是否必要。

2026-08～10 五條教訓：(1) 持續影響判定的隱性基線決策（body base、ENB、runtime 版本）一發現它在擋候選就要補文件寫理由/代價/推翻條件，不要停留在 tribal knowledge（`agentctl/handoffs/done/2026-08-27/opus-gaps/staging/body-skin-baseline-2026-08-27.md:54`）。(2) 多項並列 QA 任務每項要獨立終態，不可用已驗項外推到同類未驗項（`agentctl/handoffs/done/2026-08-31/rtqa-2026-08-31/CHARTER.md:7`）。(3) 升級第三方庫解安全漏洞時，新主版本可能牽涉商業授權而非只是 API breaking change，ModForge 的 ImageSharp 4.x Release 組態就需要 Six Labors 商業授權（`agentctl/handoffs/home-2026-10-17/improve/REPORT.md`）。(4) 其他報告裡「現況是什麼版本/狀態」的斷言要重新查證最新 commit 證據，不能直接沿用（同上）。(5) 想重新整理檔案佈局（如按字母分桶）前先問是否真要動實體路徑——mod-library 的 Mongo 掃描快取以絕對路徑為鍵不是內容雜湊，搬動會觸發約 90 GiB 全量重 hash；多數「好找」需求用 repo 外 symlink view 就能滿足（`agentctl/handoffs/done/2026-08-29/cx-libsort/REPORT.md:130-164`）。

**Why:** 都是「省一步查證/記錄，後面要付更大代價」的模式。

**How to apply:** 隱性基線發現即補文件；QA 清單逐項覆核禁止外推；庫升級查授權；舊報告斷言重查；大規模檔案搬動先問必要性。相關：[[verify-waituser-against-logs]]

## follower-dialogue-volume-and-voice-type-notes

> 隨從對話資料分析三個陷阱：換 VoiceType 前要查別家台詞是否只錄了舊聲線、OOC 抱怨先查作者頁有沒有聲明重新詮釋、統計對話量要依角色選對歸因方法而非套單一計數公式。

2026-10-08～10-09 三條教訓：(1) IFD 把萊迪亞 VoiceType 從原版 FemaleEvenToned 改成自訂聲線，本包裡約 170 句由 Inigo/Vilja/Feris/RDO/Rigmor 等別家 mod 寫給她、只錄了原版聲線的台詞，到她嘴裡只剩字幕沒聲音（Fuz Ro D'oh 讓字幕照播，容易被誤判為 bug）（`agentctl/handoffs/done/2026-10/home-2026-10-08/newsave/REPORT-lydia.md`）。(2) 使用者反映隨從「OOC」，查證發現 IFD 作者頁明寫刻意重新詮釋人設（不想寫成典型忠僕），疊加「別家台詞用舊人設寫」造成混搭觀感，不是翻譯或腳本錯誤（同上）。(3) 跨 66 位隨從對話量比較：naive OR INFO 計數被同 plugin 角色灌水，只認 GetIsID 的嚴格計數對共用 voice_type 的角色嚴重低估（某角色嚴格值 167 vs 實際 2655）；正確做法按角色分情況取 GetIsID∪voice_type 聯集並記錄 attribution_method（`modpack-design/content-plan/dialogue/SUMMARY.md:12-17`）。

**Why:** plugin／voice_type 的共享關係會讓單純的字面統計或換設定操作產生隱藏副作用。

**How to apply:** 換隨從 VoiceType 前掃全載入順序裡引用該 NPC 的 INFO，比對語音檔錄在哪個 voice type；收到 OOC 反映先查作者頁聲明；統計對話量先判斷角色是否共用 plugin/voice_type 再選歸因方法。
