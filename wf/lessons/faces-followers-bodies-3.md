# 臉、隨從、身體與動畫（3/4）

[lessons 索引](README.md)｜同主題：[faces-followers-bodies](faces-followers-bodies.md)、[faces-followers-bodies-2](faces-followers-bodies-2.md)、[faces-followers-bodies-4](faces-followers-bodies-4.md)

## custom-race-blocks-facegen-load

> 2026-09-11 Yoana 十輪終局真因：某些自訂種族（BB02YoanaRace）會讓引擎對該 NPC 完全不讀 facegeom／facetint（塞外來頭零變化），執行期用頭部件模板重生＝原版五官素臉；記錄層把 RNAM 改成素材的原版種族一次修好；換臉目標是自訂種族時，先做「外來頭塞路徑」實驗判斷（原 type: memory）

2026-09-11 Yoana 大媽臉，10 輪、約 2.5M token 才收。最終真因：**她的自訂種族 `BB02YoanaRace` 讓引擎完全不載入預烤 facegen**（facegeom＋facetint 都不讀）。

決定性實驗（lead-yoana9）：
- B1 把 Vilja 層的 Lili 臉 nif/dds 改名塞進她的 facegen 路徑 → **零變化**（連貼圖都沒換）→ 整條路徑對她是死的，跟 nif 內容無關。
- B2 記錄層（不是 setrace 指令）把 NPC_ RNAM 改成 `013744 ImperialRace`（素材沙耶的種族）→ **五官立刻變沙耶**。
- 兩種族 RACE DATA flags 只差 Playable 位元；Playable 層做了但使用者裁示直接改種族，沒驗。
- 執行期 `setrace` 指令**不能**當種族實驗（會單向毀掉預烤頭，換回也救不回）。

修法：層 `Yoana-Race-Imperial-Dev-2026-09-11`（NPC_ RNAM=013744，其餘 forward 贏家）。代價：失去該自訂種族的 spells／抗性／技能加成（使用者：隨從強度不是考量）；對話 GetIsRace 全序 0 筆。順帶留下：`Yoana-Outfit-NoWig`（披風假髮）、`Yoana-FaceGen-Match`（補嘴）兩層仍在。

**How to apply：**
1. 換臉目標若是**自訂種族**，第一步不是改層，是做 B1「外來頭塞路徑」：零變化＝種族閘門，直接評估改 RNAM；有變化才去比 nif／PNAM。
2. 種族實驗一律用記錄層＋新局，禁用 setrace。
3. 判準看**五官形狀**（大眼／下巴／嘴寬）與素材本尊同框，不看頭髮、不看妝。
4. 相機：yoana6 REPORT 第 4 節校準配方＋`tai` 定住；不要 tfc。
相關：[[outfit-hair-slot-hides-headparts]]、[[facegen-headpart-count-mismatch-discards-facegen]]、[[look-transplant-workflow-and-picker]]

## face-bugs-check-real-actor-and-upstream-fomod

> 2026-09-10 三張臉同晚壞的三種真因：placeatme 複本正常但真身壞＝存檔臉快取（disable/enable 刷新）；上游 FOMOD 可能漏裝某人的 facegen nif（Chronicon Pack II 2.2.5 的 Ryoko）；facegen nif 指到不存在的 detail 貼圖＝粉紫臉（原 type: memory）

2026-09-10 lead-ryoko 一晚查清三張臉，三種不同真因，都不是換臉層本身：

1. **Yoana「大媽臉」**：層資料 18 條全對、facegen md5 是素材真臉。`placeatme` 的複本正常、真身壞
   → **存檔快取了舊臉**（存檔 09-09 中午建，層 09-09 晚才重建）。修法：遊戲內對真身 `disable` → `enable`（或 setnpcweight）強制重載，不改任何檔。
2. **Ryoko Ukita（Chronicon Pack II 2.2.5）**：上游 FOMOD 把她的臉 nif 放在 `02 Hair Style/Ryoko/<髮型>/`，
   但 ModuleConfig.xml 沒有 Ryoko 的髮型 group → 照 XML 安裝永遠沒有她的臉。1.8.6 舊版臉在 Core，09-07 升版才壞。
   修法：從壓縮檔抽對應髮型資料夾做成獨立層（沒有 esp）。
3. **Frea／Annekke 粉紫臉**：JH NPC Beauty 的 facegen nif tex[3] 指到全機不存在的 `femaleheaddetail_frekles2.dds`（525 顆臉只有這兩顆）。
   粉紫＝缺貼圖。修法：修正層改 nif 貼圖路徑。

**How to apply:**
- 使用者說某人臉壞，先問症狀：大媽臉（素頭）／黑臉／粉紫（缺貼圖）／花掉，各對應不同層。
- 驗臉**看真身不看複本**；複本好真身壞＝存檔快取，先刷新再重建層。
- 裝隨從包後逐人核對 `facegeom/<esp>/<id>.nif` 存在（不能只信 FOMOD 選單）。
- 領隊收線一定要放 `game.lock`（lead-chair 沒放，下一隊空等 10 分鐘）。
相關：[[look-layer-must-carry-hdpt-flst-clfm]]、[[facegen-verify-size-md5-not-existence]]、[[rs-children-missing-esp]]

## outfit-hair-slot-hides-headparts

> 2026-09-11 Yoana 大媽臉五輪才抓到的真因：NPC 預設服裝的披風佔 biped slot 31（Hair）且 NIF 內縫假髮，引擎藏掉真頭髮；換頭部件／facegen／種族怎麼改都看不出來。臉壞先查裝備 slot 30/31/41/43/130 與 unequipall 對照（原 type: memory）

2026-09-11 lead-yoana×5 累計約 1.4M token 才抓到：Yoana the Wanderer 的預設 outfit「小紅帽 - 披風」ARMO 佔 **slot 31（Hair）**，NIF 裡縫了 11 塊假髮（短黑鮑伯）。引擎規則：穿著佔 Hair slot 的裝備會隱藏頭髮 head part → 換臉層寫的 Saya 髮型永遠看不到，但同一筆 NPC_ 的身高有效（getscale 量尺），facegen 檔藏掉也零變化，placeatme 複製體同樣壞（穿同一套 outfit）。

前四輪浪費在：存檔快取、Face Discoloration Fix、ESL、facegen 路徑、自訂種族 HeadData、HDPT ValidRaces FLST、ACHR 覆寫、SkyPatcher／SPID／alias script。

**How to apply（臉／髮壞的第一步）：**
1. 遊戲內先 `<ref>.unequipall` 再看一次；變好＝裝備問題，直接去查 outfit 的 ARMO/ARMA biped slots（30 頭、31 髮、41 長髮、43 耳、130 頭飾等）。
2. 離線：讀 NPC_ 的 DOFT（default outfit）→ OTFT → 每件 ARMO 的 BOD2 slots；任何佔 31／41 的都會蓋髮型。
3. 修法：outfit 層去掉那件，或把 ARMA 的 slot 改掉／NIF 切掉假髮。
4. 「複製體也壞」不代表不是 per-ref；複製體穿同一套 outfit。判斷前先脫裝備。
相關：[[face-bugs-check-real-actor-and-upstream-fomod]]、[[look-layer-must-carry-hdpt-flst-clfm]]

## bodyslide-wine-preset-empty-nam7-weight

> 2026-09-11 私有身體層實測：BodySlide 在 wine 下 Preset 下拉永遠空的，繞法是把預設值寫進 .osp 的 slider 預設屬性；NPC_ 的 NAM6 是身高、NAM7 才是體重；私有身體共用一套 ARMA/ARMO 就夠（三種族身體 TXST 同一張 dds＋FaceGenTextures）（原 type: memory）

2026-09-11 lead-body 做 Kurone 46560 私有身體（3BA 烤模、只給七位）實測：

- **BodySlide（wine／Proton，從 staging 直接跑）Preset 下拉永遠空**，連 CBBE 官方預設也讀不到。繞法：把 46560 預設的 slider 值直接寫進 `.osp` 專案檔的 slider 預設屬性，再 Batch Build。
- **NPC_ 欄位**：`NAM6`＝身高、`NAM7`＝體重。交接書寫 NAM6 當體重是筆誤，第一次驗收讀到 1.0／0.95 才發現。
- **私有身體不必每人一套 ARMO**：原版 `SkinBodyFemale_1`／`DarkElf`／`WoodElf` 三個 TXST Diffuse 都是同一張 `FemaleBody_1.dds` 且帶 FaceGenTextures（膚色由 facegen tint 執行期給），共用一套 3 ARMA＋1 ARMO＋私有 nif 路徑即可，NPC_ 只改 WNAM。
- **交叉風險**：私有身體層的 NPC_ 覆寫會壓過換臉層；換臉層之後再改，必須把新贏家 forward 回身體層（或身體層載在前面、換臉層帶 WNAM）。
- 實機看身材要先 `<ref>.unequipall`，或直接用 Outfit Studio 開 nif 看形狀不用開遊戲。

**How to apply:** 烤身體別指望 GUI 選預設；改 NPC 體重動 NAM7；多層覆寫同一個 NPC_ 時最後載入的那層要 forward 全部欄位。
相關：[[look-layer-must-carry-hdpt-flst-clfm]]、[[look-transplant-workflow-and-picker]]
