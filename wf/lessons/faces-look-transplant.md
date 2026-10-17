# 臉：換臉流程與 facegen 規則

[lessons 索引](README.md)

## voiced-follower-makeover-project

> 2026-09-01 使用者定調的新 project：語音隨從改造（對話/劇情/語音棒但外表/動畫不滿意的隨從，逐個做外觀+動畫+能力值+裝備 overlay）（原 type: project）

2026-09-01 使用者定調：Sofia 的動畫與美化只是概念起點，本質是一個新 project——「語音隨從改造」。判準：隨從的對話、劇情、語音很棒，但外表和動畫不滿意，就做修改；未來擴及能力值與裝備。Sofia 是首個 pilot。設計文件由 hvfm 隊落在 modpack-design。

**Why:** 這是長期方向不是單次施工；之後使用者點名其他語音隨從時直接走此 pipeline。

**How to apply:** 相關施工照 pipeline 模板（每隨從一個 overlay mod 資料夾）；技術基礎見 hbfco（OAR per-NPC 綁定、Sofia 零 faction 只能按個體綁）與 hnpc（頭模 copy_npc_appearance 可行、身模 per-NPC 先緩）兩份報告。相關：[[dont-inflate-light-preferences]]（但此案是使用者明說的方向，不是輕量偏好）。

## look-transplant-workflow-and-picker

> 換臉（外表移植）已有工作流與工具：agentctl/tools/look_transplant/transplant.py（一般種族）、race 線手寫路線（自訂種族素材）、挑選頁 artifact 產「【換臉變更單 LOOKS v1】」；素材端自訂種族才是硬擋，跨種族只是警告（原 type: project）

2026-09-07 晚一次做了 14＋7 對。工具鏈：`agentctl/tools/housecarl_call.py`（腳本呼叫 houseCARL MCP）＋`tools/look_transplant/transplant.py`（pairs.csv → staging overlay，ESL patch、facegen 改名、VERIFY.txt）；自訂種族素材（Chronicon／Diana／YoRHa A2）工具拒收，改走 `handoffs/home-2026-09-07/race/` 的手寫覆蓋（複製 HDPT 加目標種族、facegen 整包搬）。使用者用 artifact「換臉挑選」<https://claude.ai/code/artifact/5856df2c-5b95-4ff3-a912-e9ee39a40b67> 改主意，貼變更單即可；流程 `agentctl/docs/look-swap-runbook.md`。

**Why:** 使用者一晚改了七次主意，逐條口頭轉達成本高；頁面＋變更單把「選」和「做」分開。

**How to apply:** 收到「【換臉變更單 LOOKS v1】」走 wf `look-transplant`；素材若是自訂種族走 race 路線；素材 mod 更新會改 FormID（Chronicon II 2.2.5 全改號、Shiori 新號＝Mion 舊號），更新後 patch 要重做。Sofia 本體身體貼圖是 UNP 系，跟 CBBE 網格不相容，脖縫只能讓頭改吃全域膚色。相關：[[oar-copy-folder-bypasses-gates]]、[[housecarl-merge-facegen-backslash-filename]]。

**2026-09-08 補**：transplant.py 與 race 路線都會**連 RACE 一起搬**（Auri 木精靈→高精靈），身高與種族天賦跟著變；使用者若在意要另出「只搬 HDPT／facegen、不動 RNAM」的選項。頭身脖縫兩種真因：貼圖不同源（頭吃素材私有皮、身吃全域皮 → 一支 ESL 把頭 TXST 指回全域皮，如 Vilja←Yuuko）與頭 nif 本身（貼圖已同源仍裂 → 重烤 facegen，如 Sofia）；先比頭四張／身四張 md5 再決定走哪條。Chronicon 私有 `textures/Chron/body/FemaleHead*.dds` 是全包共用路徑，多個層各帶副本，不能直接覆蓋。名冊 artifact <https://claude.ai/code/artifact/81af4627-99c9-4772-9f4a-2381b9234c04> 與挑選頁都有可重跑建置腳本：`agentctl/handoffs/home-2026-09-08/art/tools/build_pick.py`／`build_roster.py`（先 pick 後 roster）。

## hide-donor-after-look-transplant

> 2026-09-11 使用者定：換臉用過的素材角色（donor）要在其所屬 mod 裡隱藏掉（ACHR initially disabled 或等效），不能讓同一張臉在世界裡出現兩次；每次換臉收線都要帶這一步並列入驗收（原 type: feedback）

2026-09-11 使用者原話：「已經被拿去換臉的角色，在其所屬的 mod 中，要記得隱藏掉」。

**Why：** 換臉層只把素材的頭／身體搬到目標 NPC，素材本人仍在世界裡，同一張臉會出現兩次；使用者不要這樣。

**How to apply：**
1. 每個 `<Target>-Look-From-<Donor>` 層收線時，同批要有 `DonorFollowers-Disabled-*` 層把素材 ACHR 設 initially disabled（`0xC00`）或等效隱藏（不是刪 NPC_，避免存檔壞）。
2. 驗收條目：素材 mod 的每個放置點（ACHR）都查到停用；素材在多個 cell 有分身也要全列。
3. 換臉層作廢／停用時，對應素材要不要解除隱藏一併裁。
相關：[[look-transplant-workflow-and-picker]]、[[look-layer-must-carry-hdpt-flst-clfm]]

## facegen-verify-size-md5-not-existence

> 2026-09-09 Vilja「大媽臉」真因——工人把素材 HDPT 的基礎頭 femalehead.nif 當 FaceGeom 抄進去；驗 facegen 要看逐對大小／md5 各不相同，不能只看檔案存在（原 type: feedback）

2026-09-09 lead-looks 套 9 對換臉後，使用者看到 Vilja「臉是大媽臉」。真因：codex 工人把 Kurone 包裡
十個角色共用的 HDPT 基礎頭 `femalehead.nif`（322,300 bytes、md5 全同、沒捏過的素臉）當成 FaceGeom
複製到目標的 `facegeom/<esp>/<formid>.nif`。Vilja／Katana／KatanaShade／Yoana 四顆都中，esp 本身沒錯。

**Why:** 交接書的驗收寫「facegen nif＋dds 在目標 FormKey 路徑」——「存在」就過了。素臉檔存在、路徑對、
ESL 旗標對，所有靜態 gate 全綠，但畫面是錯的。

**How to apply:**
- 換臉／重烤 facegen 的驗收要加：**每顆 facegen nif 大小與 md5 逐對列出，且彼此不同、且不等於素材
  HDPT 基礎頭的 md5**；捏過的臉通常 0.7–2.5 MB，素頭固定 ~322 KB。
- 順帶：`strings` 讀 nif 內嵌貼圖路徑，證明頭身貼圖同源；髮型 shape 名要在 nif 裡。
- 同類坑：[[oar-copy-folder-bypasses-gates]]（複製繞過閘門）、[[housecarl-merge-facegen-backslash-filename]]。

## look-layer-must-carry-hdpt-flst-clfm

> 2026-09-09 Yoana 大媽臉真因——換臉層只帶 TXST＋NPC_、沒帶素材的 HDPT／FLST／CLFM 記錄；Face Discoloration Fix 偵測 PNAM 與 facegen 不符就執行期重生成素頭。另：MO2（wine）VFS 對目錄大小寫不敏感，大小寫不一致不是問題（原 type: feedback）

2026-09-09 lead-looks 的三個工人層（cx-looks-b 做的三對）只複製了 TXST 與 NPC_ 覆寫，
**沒把素材的 HDPT（頭部零件）／FLST（適用種族清單）／CLFM（髮色）記錄帶進層裡**；
Yoana 原本 HeadParts 就是空的，所以最先爆成成人素頭（`Face Discoloration Fix`／FaceGenFixes.dll
偵測 NPC 的 PNAM 與 facegen nif 的 shape 對不上就在執行期重生成）。對照會動的前例
（Livia：HDPT 6＋FLST 1）與 `tools/look_transplant/transplant.py`（每對 HDPT 5–6 筆）。

**先前誤判要記住**：我一度把真因寫成「facegen 目錄大小寫撞車（bb02yoanafollower.esp/ vs
BB02YoanaFollower.esp/）」——**錯的**。全機 488 條大小寫不一致的路徑裡包含好幾個正常運作的層，
MO2 在 wine 下的 VFS 對大小寫不敏感。判準：一個「真因」若在其他正常案例裡也成立，它就不是真因。

**How to apply:**
- 換臉層驗收必加：層內 HDPT 筆數 ≥ 素材 PNAM 筆數、每個 HDPT 的 ValidRaces FLST 含目標種族、
  CLFM 帶齊；`strings` 讀 facegen nif 的 shape 名要與目標 PNAM 的 HDPT EditorID 一一對上。
- 有 Face Discoloration Fix 的載入序，任何 PNAM／facegen 不一致都會變「素頭」而不是黑臉——
  看到成人素臉先查記錄層一致性，不要先怪貼圖或目錄。
- 同機制：[[rs-children-missing-esp]]（RS Children 少裝 RSChildren.esp，小孩全成大媽臉）。
  相關 [[facegen-verify-size-md5-not-existence]]。

## hdpt-edid-must-match-facegen-shape-names

> 換臉層私有 HDPT 的 EDID 若跟 facegen nif 內 shape 名不一致，引擎整顆 facegen 作廢（連本體那顆也不採用）→ 大媽臉；Ashe 09-12 真因（原 type: memory）

2026-09-12 Ashe 大媽臉真因（cx-ashe3 三輪單因二分，使用者親看）：換臉層 `Ashe-Look-From-A2-Dev-2026-09-07` 裡五筆私有 HDPT（hairline／scalp／hair／head／brows）被 transplant 流程改了 EDID，而 facegen nif 裡每塊 shape 的名字還是素材原名（`AAA_Hairline`、`AAA_Scalp`、`AAA_Hair`、`AAA_GirlHeads`、`AAA_FemaleBrows`）。引擎拿 HDPT EDID 對 nif shape 名，對不上就整顆 facegen 丟掉改即時算臉。

**Why:** 09-11 兩隊十一項離線檢查（層是贏家、facegen 同素材位元組、nif 合法、頭部件數 7/7、種族原版）全過卻仍大媽臉，因為都只比「數量」與「檔案」，沒比「名字」。而且層開著時本體 facegen 也被拒（PNAM 換回本體＋藏層 facegen 才回本體臉），所以「藏檔零變化」不能推成「引擎不讀路徑」。

**How to apply:**
1. 換臉層驗收新增一條：層裡每筆 HDPT 的 EDID 必須等於 facegen nif 內對應 shape 名（或反過來改 nif 的 shape 名）；transplant.py 已於 2026-09-13（cx-tpfix，agentctl commit 78694267）改成保留 donor EDID＋fail-closed gate 5，另有 `--verify <層目錄>` 可驗既有層；audit 見 `agentctl/handoffs/home-2026-09-13/tpfix/data/layer-audit.md`（Noela／Noemie／Yoana／Yvanni 四層 FAIL 未修）。
2. 二分實驗的正確順序：先「PNAM 換本體＋藏層 facegen」看本體臉回不回來，一輪就能把元兇圈進頭部件閉包。
3. 已換臉的其他角色要回頭掃同樣的坑（cx-ashe3 REPORT 有清單，見 `agentctl/handoffs/home-2026-09-12/ashe3/REPORT.md`）。
相關：[[facegen-headpart-count-mismatch-discards-facegen]]、[[look-layer-must-carry-hdpt-flst-clfm]]、[[custom-race-blocks-facegen-load]]

## facegen-headpart-count-mismatch-discards-facegen

> 2026-09-11 Yoana 七輪的臉真因：預烤 facegen nif 的 shape（含嘴 FemaleMouthHumanoidDefault）與 NPC_ 實際頭部件集合（含種族預設補上的嘴）只要一塊對不上，引擎整顆 facegen 作廢改執行期重生＝素臉／黑臉；換臉層 PNAM 要把「種族會補的部件」也明寫成與 nif 一致（原 type: memory）

2026-09-11 lead-yoana7 修好 Yoana 大媽臉。真因：
- 換臉層 facegen `00000800.nif`（＝沙耶預烤頭）內含 **7 塊 shape**：髮、2 髮際線、眉、眼、臉、**嘴 `FemaleMouthHumanoidDefault`**。
- 換臉層／贏家 NPC_ 的 PNAM 只寫 4 塊（髮眉眼臉），沒寫嘴 → 引擎用她**自訂種族 `BB02YoanaRace` 的預設嘴 `BB02YoanaMouth`** 補上 → 與 nif 內的嘴名字不符。
- 引擎規則（Face Discoloration Fix 說明也有寫）：**head parts 與 facegen nif 對不上，整顆預烤臉作廢、執行期重生且不載入上色資料**。NPC_ 沒有 NAM9／NAMA／tint layers（Kurone 素材本身 tint layers 也是 0，妝烤在 facetint 裡）→ 素臉；FDF 關＝黑臉。
- 修法：層 `Yoana-FaceGen-Match-Dev-2026-09-11`——PNAM 補進 `05150F FemaleMouthHumanoidDefault`，並把她的種族加進該 HDPT 的 ValidRaces FLST（純加法）。實機同框有妝有暖膚色。

**How to apply（換臉層驗收新增一條）：**
1. 用 nif 內 shape 清單（BSFaceGen 下每塊的名字）對 NPC_ **實際會用到的完整頭部件集合**（PNAM＋ExtraParts＋**種族 HeadData 會補的預設部件：嘴、眼、眉、臉**）逐塊對名。目標是自訂種族時特別容易漏「嘴」。
2. 對不上就明寫進 PNAM（用素材同一塊）並確認該 HDPT ValidRaces 含目標種族。
3. 症狀對照：頭髮／臉型對但**無妝慘白**＝facegen 被作廢；FDF 關掉變黑臉可確認。
4. transplant.py 應把「種族補的部件」納入 PNAM 生成（待改）。
相關：[[outfit-hair-slot-hides-headparts]]、[[look-layer-must-carry-hdpt-flst-clfm]]、[[facegen-verify-size-md5-not-existence]]
