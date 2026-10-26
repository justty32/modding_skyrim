# 臉與身體：排錯與升級

[lessons 索引](README.md)

## custom-race-blocks-facegen-load

> 2026-09-11 Yoana 終局真因：某些自訂種族（BB02YoanaRace）會讓引擎對該 NPC 完全不讀 facegeom／facetint（塞外來頭零變化），執行期用頭部件模板重生＝原版五官素臉；記錄層把 RNAM 改成素材的原版種族一次修好；換臉目標是自訂種族時，先做「外來頭塞路徑」實驗判斷（原 type: memory）

2026-09-11 Yoana 大媽臉真因：**她的自訂種族 `BB02YoanaRace` 讓引擎完全不載入預烤 facegen**（facegeom＋facetint 都不讀）。

決定性實驗：
- B1 把別人的臉 nif/dds（Vilja 層的 Lili）改名塞進她的 facegen 路徑 → **零變化**（連貼圖都沒換）→ 整條路徑對她是死的，跟 nif 內容無關。
- B2 記錄層（不是 setrace 指令）把 NPC_ RNAM 改成 `013744 ImperialRace`（素材沙耶的種族）→ **五官立刻變沙耶**。
- 兩種族 RACE DATA flags 只差 Playable 位元；Playable 層做了但使用者裁示直接改種族，沒驗。
- 執行期 `setrace` 指令**不能**當種族實驗（會單向毀掉預烤頭，換回也救不回）。

修法：層 `Yoana-Race-Imperial-Dev-2026-09-11`（NPC_ RNAM=013744，其餘 forward 贏家）。代價：失去該自訂種族的 spells／抗性／技能加成（使用者：隨從強度不是考量）；對話 GetIsRace 全序 0 筆。`Yoana-Outfit-NoWig`（披風假髮）、`Yoana-FaceGen-Match`（補嘴）兩層仍在。

**How to apply：**
1. 換臉目標若是**自訂種族**，第一步不是改層，是做 B1「外來頭塞路徑」：零變化＝種族閘門，直接評估改 RNAM；有變化才去比 nif／PNAM。
2. 種族實驗一律用記錄層＋新局，禁用 setrace。
3. 判準看**五官形狀**（大眼／下巴／嘴寬）與素材本尊同框，不看頭髮、不看妝。
4. 相機：yoana6 REPORT 第 4 節校準配方＋`tai` 定住；不要 tfc。
相關：[[outfit-hair-slot-hides-headparts]]、[[facegen-headpart-count-mismatch-discards-facegen]]、[[look-transplant-workflow-and-picker]]

## face-bugs-check-real-actor-and-upstream-fomod

> 2026-09-10 三張臉壞的三種真因：placeatme 複本正常但真身壞＝存檔臉快取（disable/enable 刷新）；上游 FOMOD 可能漏裝某人的 facegen nif（Chronicon Pack II 2.2.5 的 Ryoko）；facegen nif 指到不存在的 detail 貼圖＝粉紫臉（原 type: memory）

三種真因都不是換臉層本身（2026-09-10）：

1. **Yoana「大媽臉」**：層資料全對、facegen md5 是素材真臉，`placeatme` 的複本正常、真身壞
   → **存檔快取了舊臉**（存檔比層重建早）。修法：遊戲內對真身 `disable` → `enable`（或 setnpcweight）強制重載，不改任何檔。
2. **Ryoko Ukita（Chronicon Pack II 2.2.5）**：上游 FOMOD 把她的臉 nif 放在 `02 Hair Style/Ryoko/<髮型>/`，
   但 ModuleConfig.xml 沒有 Ryoko 的髮型 group → 照 XML 安裝永遠沒有她的臉（1.8.6 臉在 Core）。
   修法：從壓縮檔抽對應髮型資料夾做成獨立層（沒有 esp）。
3. **Frea／Annekke 粉紫臉**：JH NPC Beauty 的 facegen nif tex[3] 指到全機不存在的 `femaleheaddetail_frekles2.dds`（525 顆臉只有這兩顆）。
   粉紫＝缺貼圖。修法：修正層改 nif 貼圖路徑。

**How to apply:**
- 使用者說某人臉壞，先問症狀：大媽臉（素頭）／黑臉／粉紫（缺貼圖）／花掉，各對應不同層。
- 驗臉**看真身不看複本**；複本好真身壞＝存檔快取，先刷新再重建層。
- 裝隨從包後逐人核對 `facegeom/<esp>/<id>.nif` 存在（不能只信 FOMOD 選單）。
- 領隊收線一定要放 `game.lock`（沒放會讓下一隊空等）。
- 裝新外觀/頭髮類 mod 時，先對全 VFS（啟用 mod 的 loose＋BSA）逐一查每支新裝 nif 引用的貼圖是否存在，在安裝階段抓出粉紫風險，並分辨「缺 diffuse/alpha（會粉紫，需補）」與「只缺法線圖（不會粉紫，可不管）」，不要等實機看到粉紫才回頭查（2026-10-23，`agentctl/handoffs/done/2026-10/home-2026-10-10/batch4a-kurone/REPORT.md`）。
相關：[[look-layer-must-carry-hdpt-flst-clfm]]、[[facegen-verify-size-md5-not-existence]]、[[rs-children-missing-esp]]

## outfit-hair-slot-hides-headparts

> 2026-09-11 Yoana 大媽臉真因：NPC 預設服裝的披風佔 biped slot 31（Hair）且 NIF 內縫假髮，引擎藏掉真頭髮；換頭部件／facegen／種族怎麼改都看不出來。臉壞先查裝備 slot 30/31/41/43/130 與 unequipall 對照（原 type: memory）

Yoana the Wanderer 的預設 outfit「小紅帽 - 披風」ARMO 佔 **slot 31（Hair）**，NIF 裡縫了 11 塊假髮（短黑鮑伯）。引擎規則：穿著佔 Hair slot 的裝備會隱藏頭髮 head part → 換臉層寫的髮型永遠看不到，但同一筆 NPC_ 的身高有效（getscale 量尺），facegen 檔藏掉也零變化，placeatme 複製體同樣壞（穿同一套 outfit）。

此案排除過、不是真因的方向：存檔快取、Face Discoloration Fix、ESL、facegen 路徑、自訂種族 HeadData、HDPT ValidRaces FLST、ACHR 覆寫、SkyPatcher／SPID／alias script。

**How to apply（臉／髮壞的第一步）：**
1. 遊戲內先 `<ref>.unequipall` 再看一次；變好＝裝備問題，直接去查 outfit 的 ARMO/ARMA biped slots（30 頭、31 髮、41 長髮、43 耳、130 頭飾等）。
2. 離線：讀 NPC_ 的 DOFT（default outfit）→ OTFT → 每件 ARMO 的 BOD2 slots；任何佔 31／41 的都會蓋髮型。
3. 修法：outfit 層去掉那件，或把 ARMA 的 slot 改掉／NIF 切掉假髮。
4. 「複製體也壞」不代表不是 per-ref；複製體穿同一套 outfit。判斷前先脫裝備。
相關：[[face-bugs-check-real-actor-and-upstream-fomod]]、[[look-layer-must-carry-hdpt-flst-clfm]]

## bodyslide-wine-preset-empty-nam7-weight

> 2026-09-11 私有身體層實測：BodySlide 在 wine 下 Preset 下拉永遠空的，繞法是把預設值寫進 .osp 的 slider 預設屬性；NPC_ 的 NAM6 是身高、NAM7 才是體重；私有身體共用一套 ARMA/ARMO 就夠（三種族身體 TXST 同一張 dds＋FaceGenTextures）（原 type: memory）

2026-09-11 Kurone 46560 私有身體（3BA 烤模）實測：

- **BodySlide（wine／Proton，從 staging 直接跑）Preset 下拉永遠空**，連 CBBE 官方預設也讀不到。繞法：把 46560 預設的 slider 值直接寫進 `.osp` 專案檔的 slider 預設屬性，再 Batch Build。
- **NPC_ 欄位**：`NAM6`＝身高、`NAM7`＝體重（交接書曾把 NAM6 寫成體重，是筆誤）。
- 體重滑條（0-100）改的是兩個雕好形狀之間的逐頂點內插，不是整體縮放：同一 mod 兩個體重檔案深度差 17.94%、寬度只差 1.15%、高度 −0.11%；要調角色「整個人大小」改 NAM6（身高），體重調到滿格不會把人變大（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-09/body/REPORT.md:17-27`）。
- **私有身體不必每人一套 ARMO**：原版 `SkinBodyFemale_1`／`DarkElf`／`WoodElf` 三個 TXST Diffuse 都是同一張 `FemaleBody_1.dds` 且帶 FaceGenTextures（膚色由 facegen tint 執行期給），共用一套 3 ARMA＋1 ARMO＋私有 nif 路徑即可，NPC_ 只改 WNAM。
- 換私有身體前先查 ARMA 第三人稱模型指的是全域還是私有路徑：指向**全域** `FemaleBody_1.nif` 時不需重烤 BodySlide，做一支小 ESL 把該 ARMA 的 `WorldModel[1].File` 改指向已烤好的私有 nif 即可，0 筆 NPC_ 改動（2026-10-23，`agentctl/handoffs/done/2026-10/home-2026-10-10/batch4a-kurone/REPORT.md`）。
- **交叉風險**：私有身體層的 NPC_ 覆寫會壓過換臉層；換臉層之後再改，必須把新贏家 forward 回身體層（或身體層載在前面、換臉層帶 WNAM）。
- 實機看身材要先 `<ref>.unequipall`，或直接用 Outfit Studio 開 nif 看形狀不用開遊戲。
- 交接書寫死的單一欄位值可能依記錄的其他維度（種族/型別）而不同：「MorphRace 補回去用 013748」其實依種族有四個值，照字面手改成單一值五筆裡四筆會拿到錯的種族臉形；有疑慮優先用整筆 forward 自權威來源取代手改單一值，不要信交接書的字面值（2026-10-23，`agentctl/handoffs/done/2026-09/home-2026-09-09/body/REPORT.md:69-78`）。

**How to apply:** 烤身體別指望 GUI 選預設；改 NPC 體重動 NAM7、整體大小動 NAM6；多層覆寫同一個 NPC_ 時最後載入的那層要 forward 全部欄位。
相關：[[look-layer-must-carry-hdpt-flst-clfm]]、[[look-transplant-workflow-and-picker]]

## daegon-2212-midsave-upgrade

> Daegon 2.0.5→2.2.1.2 中途升級成功；Legacy(112097/112191) 與 2.x 不可並存；NifSwap 要四路徑同 md5；Elven Princess v1.3 對 2.2（原 type: memory）

2026-09-19 使用者實機確認：Daegon and Kaeserius 2.0.5→2.2.1.2 在現有存檔升級成功（profiles `b9b13f4`），跳過「先 dismiss」步驟也沒事，
臉／名字／髮辮切換都對。組成：`Daegon-2.2.1.2`＋`Daegon-CHS-171488-2.2.1.2-ZH-2026-09-18`（171488 拓撲同版，forward 自家名詞 8 個＋補 201 欄）
＋`Daegon-ElvenPrincess-1.3`（有角）＋`Goam-Elven-Ears-Fair-1.0`。

**Why:** 2.2.1.2 只增不改（FormID 不重編、masters 不變、非 ESL），DLL 同 NG 模板。
**How to apply:**
- `Daegon Kaekiri 112097`／`Daegon Legacy 112191` 是 Legacy 本體，plugin 同名 `k101Daegon.esp` 但 FormID 體系不同，**不是美化、不能跟 2.x 並存**。
- 本體 DLL `NifSwap()` 在室內外切髮型時用 CopyFileW 在 `facegeom/k101Daegon.esp/00005900{,Stock}.nif` 與 `facegeom/temp/` 之間互換：換臉層四個路徑都要放同 md5，否則切一次髮辮就變回原臉。
- 角與 Goam 耳是烤進 facegen 的無 HDPT 多餘 shape，引擎容忍（作者出貨方式就是這樣）；補 HDPT 的備案工具在 `agentctl/handoffs/home-2026-09-18/dgn2/tools/`。
- 升級後開機的 alias 綁不到／None 錯誤是舊存檔過渡一次性雜訊。
相關：[[daegon-itemfinding-script-ctd]]、[[facegen-headpart-count-mismatch-discards-facegen]]


## facegen-reference-path-and-tint-binding-pitfalls

> 兩種「改了設定但舊參照沒跟著變」的坑：覆寫既有 NPC 的 esp 附帶的 facegen 要放在**原始定義** plugin 的資料夾下，放覆寫 esp 自己名字的資料夾形同沒裝；合併/改名 plugin 後，facegen nif 內寫死的舊 facetint 路徑不會自動更新。

- 覆寫 esp 把 facegen 放自己名字資料夾，引擎只認原始定義 plugin（如 `Skyrim.esm`）的資料夾，形同沒裝。
- facegen nif 內嵌 facetint 路徑寫死舊 plugin 名；facetint 是引擎依 plugin 名另行載入，跟 nif 路徑欄位沒同步機制。
（2026-10-10，`agentctl/handoffs/done/2026-10/home-2026-10-10/tradingposts/REPORT.md`、`.../nell/REPORT.md`）

**Why:** 路徑看起來對，但引擎用的是另一條固定規則找資料夾/路徑，不是存在性問題。

**How to apply:** 驗收覆寫既有 NPC 外觀要查 facegen 是否放在**原始定義 plugin** 的 `FaceGeom`/`FaceTint` 下；改名或合併含 facegen 記錄的施工要額外核對 nif 內嵌 facetint 路徑，對不上列入實機驗收。相關：[[face-bugs-check-real-actor-and-upstream-fomod]]、[[hdpt-edid-must-match-facegen-shape-names]]。

OBody NG 4.4.3 的 preset 黑名單（2026-10-23）：逐字串精確比對，不支援萬用字元/子字串（黑名單裡的「Zeroed Sliders」擋不住「CT77 Zeroed Sliders - Zap Panties」）；且只擋「之後」的新分配，已套到 NPC 身上、存進 cosave 的 preset 不會自動清除（走 ORefit 換裝路徑，只讀 cosave 不查黑名單）。建黑名單前先掃出全部啟用中的實際 preset 名稱逐一核對；加黑名單後對已中過的角色要額外手動重置或清 skee morph cache（`agentctl/handoffs/done/2026-10/home-2026-10-04/aniya/REPORT-fix.md`）。

整個 modlist 一次性 facegen 一致化重烤的參考流程（2026-10-23，第三方快照未實測）：Synthesis NPCs-Face-Data patcher 補 master → 產出 NPCsWithFaces.esp 設 Active File → CK 依 RAM 分段 Ctrl+F4（低於 32GB 要按種族區間分 5 批）→ 排除小孩（TRI 結構特殊會生成失敗）與 Astrid（會燒焦全部 NPC 臉）→ CAO BSA Packer 打包時 Maximum Size 須鎖 1.96，超過不會被遊戲載入（`modpack-design/sources/animonculory-modding-resources-2026-09-02/facegen-regeneration-ck.md`）。此上限也適用任何用 CAO 打包 facegen 進 BSA 的場景。
