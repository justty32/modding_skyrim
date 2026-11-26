# 臉：facegen 沒生效——存檔快取、漏裝、自訂種族、資料夾路徑與升級

[lessons 索引](README.md)

頭部件與 facegen 對名的規則在 [faces-facegen-consistency](faces-facegen-consistency.md)；裝備／身體類排錯見 [faces-troubleshooting](faces-troubleshooting.md)。

## face-bugs-check-real-actor-and-upstream-fomod

> 2026-09-10 三張臉壞的三種真因：placeatme 複本正常但真身壞＝存檔臉快取（disable/enable 刷新）；上游 FOMOD 可能漏裝某人的 facegen nif；facegen nif 指到不存在的 detail 貼圖＝粉紫臉

三種真因都不是換臉層本身（2026-09-10）：
1. **存檔快取舊臉**（Yoana）：層資料全對、facegen md5 是素材真臉，`placeatme` 複本正常、真身壞（存檔比層重建早）。修法：遊戲內對真身 `disable` → `enable`（或 setnpcweight）強制重載，不改檔。
2. **上游 FOMOD 漏裝 facegen**：臉 nif 放在可選髮型資料夾，但 `ModuleConfig.xml` 沒有對應選項，照 XML 裝仍漏臉。修法：核對壓縮檔，抽出對應髮型資料夾做成獨立層（沒有 esp）。
3. **粉紫臉**（Frea／Annekke）：JH NPC Beauty 的 facegen nif tex[3] 指到全機不存在的 `femaleheaddetail_frekles2.dds`。粉紫＝缺貼圖，修正層改 nif 貼圖路徑。

**How to apply:**
- 使用者說某人臉壞，先問症狀：大媽臉（素頭）／黑臉／粉紫（缺貼圖）／花掉，各對應不同層。
- 驗臉**看真身不看複本**；複本好真身壞＝存檔快取，先刷新再重建層。
- 裝隨從包後逐人核對 `facegeom/<esp>/<id>.nif` 存在（不能只信 FOMOD 選單）。
- 裝新外觀／頭髮類 mod 時，對全 VFS（啟用 mod 的 loose＋BSA）逐支查新 nif 引用的貼圖是否存在，安裝階段就抓粉紫風險：缺 diffuse／alpha 會粉紫要補，只缺法線圖不會粉紫可不管（2026-10-23，`agentctl/handoffs/done/2026-10/home-2026-10-10/batch4a-kurone/REPORT.md`）。

相關：[[look-layer-must-carry-hdpt-flst-clfm]]、[[facegen-verify-size-md5-not-existence]]、[[rs-children-missing-esp]]

## custom-race-blocks-facegen-load

> 2026-09-11 Yoana 終局真因：某些自訂種族（BB02YoanaRace）會讓引擎對該 NPC 完全不讀 facegeom／facetint（塞外來頭零變化），執行期用頭部件模板重生＝原版五官素臉；記錄層把 RNAM 改成素材的原版種族一次修好；換臉目標是自訂種族時，先做「外來頭塞路徑」實驗判斷

2026-09-11：自訂種族 `BB02YoanaRace` 讓引擎對 Yoana 完全不載入預烤 facegen（facegeom＋facetint 都不讀）。
- 把別人的臉 nif/dds 改名塞進她的 facegen 路徑 → **零變化**（連貼圖都沒換）＝整條路徑對她是死的，跟 nif 內容無關。
- 記錄層（不是 setrace 指令）把 NPC_ RNAM 改成 `013744 ImperialRace`（素材的種族）→ 五官立刻對。兩種族 RACE DATA flags 只差 Playable 位元；只補 Playable 是否夠沒驗過。
- 執行期 `setrace` 指令**不能**當種族實驗（會單向毀掉預烤頭，換回也救不回）。

修法：層 `Yoana-Race-Imperial-Dev-2026-09-11`（NPC_ RNAM=013744，其餘 forward 贏家）。代價：失去該自訂種族的 spells／抗性／技能加成（使用者：隨從強度不是考量）；對話 GetIsRace 全序 0 筆。`Yoana-Outfit-NoWig`（披風假髮）、`Yoana-FaceGen-Match`（補嘴）兩層也要開：2026-11-25 使用者「yoana那塊確實需要這個拿掉假髮的」，換了髮型就要拿掉假髮（裁示 37「披風穿回」作廢）。

**How to apply：**
1. 換臉目標若是**自訂種族**，第一步不是改層，是做「外來頭塞路徑」：零變化＝種族閘門，直接評估改 RNAM；有變化才去比 nif／PNAM。
2. 種族實驗一律用記錄層＋新局，禁用 setrace。
3. 判準看**五官形狀**（大眼／下巴／嘴寬）與素材本尊同框，不看頭髮、不看妝。
4. 相機：yoana6 REPORT 第 4 節校準配方＋`tai` 定住；不要 tfc。

玩家在 RaceMenu 選不到自訂種族、部件不可選是另一道門，見 [[custom-race-playable-and-valid-headparts]]。相關：[[outfit-hair-slot-hides-headparts]]、[[facegen-headpart-count-mismatch-discards-facegen]]、[[look-transplant-workflow-and-picker]]

## facegen-reference-path-and-tint-binding-pitfalls

> 兩種「改了設定但舊參照沒跟著變」的坑：覆寫既有 NPC 的 esp 附帶的 facegen 要放在**原始定義** plugin 的資料夾下，放覆寫 esp 自己名字的資料夾形同沒裝；合併/改名 plugin 後，facegen nif 內寫死的舊 facetint 路徑不會自動更新。

2026-10-10（`agentctl/handoffs/done/2026-10/home-2026-10-10/tradingposts/REPORT.md`、`.../nell/REPORT.md`）：
- 引擎只認原始定義 plugin（如 `Skyrim.esm`）的 `FaceGeom`／`FaceTint` 資料夾；覆寫 esp 放自己名字的資料夾形同沒裝。路徑看起來對，但不是存在性問題。
- facegen nif 內嵌的 facetint 路徑寫死舊 plugin 名；facetint 是引擎依 plugin 名另行載入，跟 nif 路徑欄位沒同步機制。

**How to apply:** 驗收覆寫既有 NPC 外觀要查 facegen 是否放在**原始定義 plugin** 下；改名或合併含 facegen 記錄的施工要額外核對 nif 內嵌 facetint 路徑，對不上列入實機驗收。

整個 modlist 一次性 facegen 一致化重烤的參考流程（2026-10-23，第三方快照未實測，`modpack-design/sources/animonculory-modding-resources-2026-09-02/facegen-regeneration-ck.md`）：Synthesis NPCs-Face-Data patcher 補 master → 產出 NPCsWithFaces.esp 設 Active File → CK 依 RAM 分段 Ctrl+F4（低於 32GB 要按種族區間分 5 批）→ 排除小孩（TRI 結構特殊會生成失敗）與 Astrid（會燒焦全部 NPC 臉）→ CAO BSA Packer 打包。**任何用 CAO 打包 facegen 進 BSA，Maximum Size 須鎖 1.96，超過不會被遊戲載入。**

相關：[[face-bugs-check-real-actor-and-upstream-fomod]]、[[hdpt-edid-must-match-facegen-shape-names]]。

## daegon-2212-midsave-upgrade

> Daegon 2.0.5→2.2.1.2 中途升級成功；Legacy(112097/112191) 與 2.x 不可並存；NifSwap 要四路徑同 md5；Elven Princess v1.3 對 2.2

2026-09-19 使用者實機確認：Daegon and Kaeserius 2.0.5→2.2.1.2 在現有存檔升級成功（profiles `b9b13f4`），不必先 dismiss。組成：`Daegon-2.2.1.2`＋`Daegon-CHS-171488-2.2.1.2-ZH-2026-09-18`（171488 拓撲同版，forward 自家名詞 8 個＋補 201 欄）＋`Daegon-ElvenPrincess-1.3`（有角）＋`Goam-Elven-Ears-Fair-1.0`。2.2.1.2 只增不改（FormID 不重編、masters 不變、非 ESL），DLL 同 NG 模板。

**How to apply:**
- `Daegon Kaekiri 112097`／`Daegon Legacy 112191` 是 Legacy 本體，plugin 同名 `k101Daegon.esp` 但 FormID 體系不同，**不是美化、不能跟 2.x 並存**。
- 本體 DLL `NifSwap()` 在室內外切髮型時用 CopyFileW 在 `facegeom/k101Daegon.esp/00005900{,Stock}.nif` 與 `facegeom/temp/` 之間互換：換臉層四個路徑都要放同 md5，否則切一次髮辮就變回原臉。
- 角與 Goam 耳是烤進 facegen 的無 HDPT 多餘 shape，引擎容忍（作者出貨方式就是這樣）；補 HDPT 的備案工具在 `agentctl/handoffs/home-2026-09-18/dgn2/tools/`。
- 升級後開機的 alias 綁不到／None 錯誤是舊存檔過渡一次性雜訊。

相關：[[daegon-itemfinding-script-ctd]]、[[facegen-headpart-count-mismatch-discards-facegen]]
