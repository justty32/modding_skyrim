# 臉：換臉流程與 facegen 規則

[lessons 索引](README.md)

## voiced-follower-makeover-project

> 2026-09-01 使用者定調的新 project：語音隨從改造（對話/劇情/語音棒但外表/動畫不滿意的隨從，逐個做外觀+動畫+能力值+裝備 overlay）（原 type: project）

2026-09-01 使用者定調：Sofia 的動畫與美化只是概念起點，本質是一個新 project——「語音隨從改造」。判準：隨從的對話、劇情、語音很棒，但外表和動畫不滿意，就做修改；未來擴及能力值與裝備。Sofia 是首個 pilot。設計文件在 modpack-design。

**Why:** 這是長期方向不是單次施工；之後使用者點名其他語音隨從時直接走此 pipeline。

**How to apply:** 相關施工照 pipeline 模板（每隨從一個 overlay mod 資料夾）；技術基礎見 hbfco（OAR per-NPC 綁定、Sofia 零 faction 只能按個體綁）與 hnpc（頭模 copy_npc_appearance 可行、身模 per-NPC 先緩）兩份報告。相關：[[dont-inflate-light-preferences]]（但此案是使用者明說的方向，不是輕量偏好）。

OAR 的 `IsActorBase` 條件可精確把動畫綁到單一 NPC（faction 為空也適用）：複製一份現役同武器類 OAR submod，在 conditions 加一條 `IsActorBase`（pluginName+formID），priority 設到眾數區以上，MO2 啟用新 mod，不需動 esp、不需跑 Pandora/Nemesis；用遊戲內 OAR 選單核對實際命中的 config 名稱做驗收（`agentctl/handoffs/done/2026-09-01/hbfco-2026-09-01/REPORT.md:110-225`）。

## look-transplant-workflow-and-picker

> 換臉（外表移植）已有工作流與工具：agentctl/tools/look_transplant/transplant.py（一般種族）、race 線手寫路線（自訂種族素材）、挑選頁 artifact 產「【換臉變更單 LOOKS v1】」；素材端自訂種族才是硬擋，跨種族只是警告（原 type: project）

工具鏈（2026-09-07 建）：`agentctl/tools/housecarl_call.py`（腳本呼叫 houseCARL MCP）＋`tools/look_transplant/transplant.py`（pairs.csv → staging overlay，ESL patch、facegen 改名、VERIFY.txt）；自訂種族素材（Chronicon／Diana／YoRHa A2）工具拒收，改走 `handoffs/home-2026-09-07/race/` 的手寫覆蓋（複製 HDPT 加目標種族、facegen 整包搬）。使用者用 artifact「換臉挑選」<https://claude.ai/code/artifact/5856df2c-5b95-4ff3-a912-e9ee39a40b67> 改主意，貼變更單即可；流程 `agentctl/docs/look-swap-runbook.md`。

**Why:** 使用者會反覆改主意（2026-09-07 一晚七次），逐條口頭轉達成本高；頁面＋變更單把「選」和「做」分開。

**How to apply:**
收到「【換臉變更單 LOOKS v1】」走 wf `look-transplant`；素材若是自訂種族走 race 路線。

transplant.py 與 race 路線都會**連 RACE 一起搬**（如 Auri 木精靈→高精靈），身高與種族天賦跟著變；使用者若在意要另出「只搬 HDPT／facegen、不動 RNAM」的選項（2026-09-08）。

頭身脖縫兩種真因：貼圖不同源（頭吃素材私有皮、身吃全域皮 → 一支 ESL 把頭 TXST 指回全域皮，如 Vilja←Yuuko）與頭 nif 本身（貼圖已同源仍裂 → 重烤 facegen，如 Sofia）；先比頭四張／身四張 md5 再決定走哪條。Sofia 本體身體貼圖是 UNP 系，跟 CBBE 網格不相容，脖縫只能讓頭改吃全域膚色。Chronicon 私有 `textures/Chron/body/FemaleHead*.dds` 是全包共用路徑，多個層各帶副本，不能直接覆蓋。

名冊 artifact <https://claude.ai/code/artifact/81af4627-99c9-4772-9f4a-2381b9234c04> 與挑選頁都有可重跑建置腳本：`agentctl/handoffs/home-2026-09-08/art/tools/build_pick.py`／`build_roster.py`（先 pick 後 roster）。2026-10-26 起重產方法（底稿改用線上版、路徑已月結到 `done/2026-09/`）見 [wf/user/2026-10-26-follower-look-pages.md](../user/2026-10-26-follower-look-pages.md)。

facegen 頭模移植跟身模是兩套獨立機制：body mesh/skin texture 掛在 race 的 skin ArmorAddon 上不是 per-NPC；換身體要另做自訂 skin ARMO/ARMA，若 donor 是 UNP/BHUNP 或帶 3BA/SMP 物理而本機沒對應 runtime，會接縫或物理失效。頭模移植工量 1–2 小時，身模半天到一天，收到「換外觀」需求先分清是哪一種（`agentctl/handoffs/done/2026-09-01/hnpc-2026-09-01/MIXMATCH.md:29-41`）。

素材 mod 更新會改 FormID（Chronicon II 2.2.5 全改號），更新後 patch 要重做；改號可能撞號（Shiori 新號 000854＝Mion 舊號），Mion 的換臉 patch 沒跟著更新時遊戲不報錯、安靜地把 Mion 的臉換成 Shiori 的臉。mod 更新改動 FormID 後，所有引用舊 FormID 的 patch 要逐一核對新舊號是否互相撞號，不能只看「舊號還存不存在」（`agentctl/handoffs/done/2026-09/home-2026-09-07/chron/REPORT.md:26`）。

`agentctl/tools/look_transplant/tests` 依賴的 esp fixture 沒進版控（被 .gitignore 排除），乾淨 worktree 跑會 4 errors，只有主樹才會綠；`transplant_lib/common.py` 的預設 staging 路徑在 2026-10-17 清理後可能已不存在。跑測試要在主樹跑，派換臉線前先確認預設 staging 路徑存在（`agentctl/handoffs/home-2026-10-17/patrol/p1-agentctl/REPORT.md`）。

自訂種族把角/耳等特徵直接烤進 facegen、無獨立 HDPT nif 時，可用另一個結構同構（block 排列相同）的既有 HDPT nif 當模板，把 facegen 內該 shape 的 block 叢搬出來重編 ref 做成獨立 nif（Daegon 案例六個 block 只差 3+2+1 個 ref 位元組即可逐位元組對齊）；遇到「烤進 facegen 的特徵想拆成獨立 HDPT」先找同 mod 內結構相同的既有 HDPT nif 當模板比對位元組，不要從零寫 nif（`agentctl/handoffs/done/2026-09/home-2026-09-18/dgn2/REPORT.md:8`）。

新換臉層與既有修正層命中同一張 facegen 但服務不同角色時（kurone Frea 層 vs FreaAnnekke-FaceDetail-Fix 同時蓋 Frea 與 Annekke），不要整層停用舊層——先查舊層是否對其他角色有不可替代的修正，有就把新層疊在上面用優先權壓過，兩個角色各取所需（`agentctl/handoffs/done/2026-09/home-2026-09-11/kurone/REPORT.md:79-82`）。

相關：[[oar-copy-folder-bypasses-gates]]、[[housecarl-merge-facegen-backslash-filename]]。

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

2026-09-09 使用者看到 Vilja「臉是大媽臉」。真因：工人把 Kurone 包裡十個角色共用的 HDPT 基礎頭 `femalehead.nif`（322,300 bytes、md5 全同、沒捏過的素臉）當成 FaceGeom 複製到目標的 `facegeom/<esp>/<formid>.nif`；esp 本身沒錯。

**Why:** 驗收只寫「facegen nif＋dds 在目標 FormKey 路徑」，「存在」就過了。素臉檔存在、路徑對、ESL 旗標對，所有靜態 gate 全綠，但畫面是錯的。

**How to apply:**
- 換臉／重烤 facegen 的驗收要加：**每顆 facegen nif 大小與 md5 逐對列出，且彼此不同、且不等於素材
  HDPT 基礎頭的 md5**；捏過的臉通常 0.7–2.5 MB，素頭固定 ~322 KB。
- 順帶：`strings` 讀 nif 內嵌貼圖路徑，證明頭身貼圖同源；髮型 shape 名要在 nif 裡。
- 同類坑：[[oar-copy-folder-bypasses-gates]]（複製繞過閘門）、[[housecarl-merge-facegen-backslash-filename]]。

## look-layer-must-carry-hdpt-flst-clfm

> 2026-09-09 Yoana 大媽臉真因——換臉層只帶 TXST＋NPC_、沒帶素材的 HDPT／FLST／CLFM 記錄；Face Discoloration Fix 偵測 PNAM 與 facegen 不符就執行期重生成素頭。另：MO2（wine）VFS 對目錄大小寫不敏感，大小寫不一致不是問題（原 type: feedback）

換臉層只複製 TXST 與 NPC_ 覆寫、**沒把素材的 HDPT（頭部零件）／FLST（適用種族清單）／CLFM（髮色）記錄帶進層裡**時，`Face Discoloration Fix`／FaceGenFixes.dll 偵測 NPC 的 PNAM 與 facegen nif 的 shape 對不上，就在執行期重生成成人素頭（2026-09-09 Yoana）。正確的前例：Livia（HDPT 6＋FLST 1）與 `tools/look_transplant/transplant.py`（每對 HDPT 5–6 筆）。

MO2 在 wine 下的 VFS 對目錄大小寫不敏感，facegen 目錄大小寫不一致（如 bb02yoanafollower.esp/ vs BB02YoanaFollower.esp/）不是真因——全機 488 條大小寫不一致的路徑裡包含好幾個正常運作的層。判準：一個「真因」若在其他正常案例裡也成立，它就不是真因。

**How to apply:**
- 換臉層驗收必加：層內 HDPT 筆數 ≥ 素材 PNAM 筆數、每個 HDPT 的 ValidRaces FLST 含目標種族、
  CLFM 帶齊；`strings` 讀 facegen nif 的 shape 名要與目標 PNAM 的 HDPT EditorID 一一對上。
- 有 Face Discoloration Fix 的載入序，任何 PNAM／facegen 不一致都會變「素頭」而不是黑臉——
  看到成人素臉先查記錄層一致性，不要先怪貼圖或目錄。
- 同機制：[[rs-children-missing-esp]]（RS Children 少裝 RSChildren.esp，小孩全成大媽臉）。
  相關 [[facegen-verify-size-md5-not-existence]]。

## hdpt-edid-must-match-facegen-shape-names

> 換臉層私有 HDPT 的 EDID 若跟 facegen nif 內 shape 名不一致，引擎整顆 facegen 作廢（連本體那顆也不採用）→ 大媽臉；Ashe 09-12 真因（原 type: memory）

引擎拿 HDPT EDID 對 facegen nif 的 shape 名，對不上就整顆 facegen 丟掉改即時算臉（2026-09-12 Ashe 大媽臉真因，使用者親看）。案例：換臉層 `Ashe-Look-From-A2-Dev-2026-09-07` 裡五筆私有 HDPT（hairline／scalp／hair／head／brows）被 transplant 流程改了 EDID，而 nif 裡每塊 shape 還是素材原名（`AAA_Hairline`、`AAA_Scalp`、`AAA_Hair`、`AAA_GirlHeads`、`AAA_FemaleBrows`）。

**Why:** 只比「數量」與「檔案」的離線檢查（層是贏家、facegen 同素材位元組、nif 合法、頭部件數 7/7、種族原版）會全過，卻仍大媽臉，因為沒比「名字」。而且層開著時本體 facegen 也被拒（PNAM 換回本體＋藏層 facegen 才回本體臉），所以「藏檔零變化」不能推成「引擎不讀路徑」。

**How to apply:**
1. 換臉層驗收：層裡每筆 HDPT 的 EDID 必須等於 facegen nif 內對應 shape 名（或反過來改 nif 的 shape 名）；transplant.py 現在保留 donor EDID＋fail-closed gate 5，另有 `--verify <層目錄>` 可驗既有層；audit 見 `agentctl/handoffs/home-2026-09-13/tpfix/data/layer-audit.md`（Noela／Noemie／Yoana／Yvanni 四層 FAIL 未修）。
2. 二分實驗的正確順序：先「PNAM 換本體＋藏層 facegen」看本體臉回不回來，一輪就能把元兇圈進頭部件閉包。
3. 已換臉的其他角色要回頭掃同樣的坑（清單見 `agentctl/handoffs/home-2026-09-12/ashe3/REPORT.md`）。
相關：[[facegen-headpart-count-mismatch-discards-facegen]]、[[look-layer-must-carry-hdpt-flst-clfm]]、[[custom-race-blocks-facegen-load]]

## facegen-headpart-count-mismatch-discards-facegen

> 2026-09-11 Yoana 的臉真因：預烤 facegen nif 的 shape（含嘴 FemaleMouthHumanoidDefault）與 NPC_ 實際頭部件集合（含種族預設補上的嘴）只要一塊對不上，引擎整顆 facegen 作廢改執行期重生＝素臉／黑臉；換臉層 PNAM 要把「種族會補的部件」也明寫成與 nif 一致（原 type: memory）

引擎規則（Face Discoloration Fix 說明也有寫）：**head parts 與 facegen nif 對不上，整顆預烤臉作廢、執行期重生且不載入上色資料**。NPC_ 沒有 NAM9／NAMA／tint layers 時（Kurone 素材本身 tint layers 也是 0，妝烤在 facetint 裡）→ 素臉；FDF 關＝黑臉。

案例（2026-09-11 Yoana，已修好）：
- 換臉層 facegen `00000800.nif`（＝沙耶預烤頭）內含 **7 塊 shape**：髮、2 髮際線、眉、眼、臉、**嘴 `FemaleMouthHumanoidDefault`**。
- 換臉層／贏家 NPC_ 的 PNAM 只寫 4 塊（髮眉眼臉），沒寫嘴 → 引擎用她**自訂種族 `BB02YoanaRace` 的預設嘴 `BB02YoanaMouth`** 補上 → 與 nif 內的嘴名字不符。
- 修法：層 `Yoana-FaceGen-Match-Dev-2026-09-11`——PNAM 補進 `05150F FemaleMouthHumanoidDefault`，並把她的種族加進該 HDPT 的 ValidRaces FLST（純加法）。實機同框有妝有暖膚色。

**How to apply（換臉層驗收）：**
1. 用 nif 內 shape 清單（BSFaceGen 下每塊的名字）對 NPC_ **實際會用到的完整頭部件集合**（PNAM＋ExtraParts＋**種族 HeadData 會補的預設部件：嘴、眼、眉、臉**）逐塊對名。目標是自訂種族時特別容易漏「嘴」。
2. 對不上就明寫進 PNAM（用素材同一塊）並確認該 HDPT ValidRaces 含目標種族。
3. 症狀對照：頭髮／臉型對但**無妝慘白**＝facegen 被作廢；FDF 關掉變黑臉可確認。
4. transplant.py 應把「種族補的部件」納入 PNAM 生成（待改）。
相關：[[outfit-hair-slot-hides-headparts]]、[[look-layer-must-carry-hdpt-flst-clfm]]、[[facegen-verify-size-md5-not-existence]]


## look-transplant-wnam-and-skin-checks

> 換臉/換種族常漏兩個欄位：`copy_npc_appearance` 會把 donor 的 WNAM 一起搬過去蓋掉目標原本皮膚（可能有 quest 依賴）；換種族時若 WNAM 指的私有皮膚 ARMA 只涵蓋舊種族，新種族脫光或穿無手套/靴子衣服時缺甲部位直接消失。

copy_npc_appearance 連 HDPT／HairColor／TintLayers／WNAM 整組都搬，donor 髮型 HDPT 若指向本機沒有的 provider 會變禿頭（2026-09-01，`agentctl/handoffs/done/2026-09-01/hnpc-2026-09-01/MIXMATCH.md:14-27`）。換種族層改了 RNAM 卻沒動 WNAM 時，私有皮膚 ARMA 只涵蓋舊種族（2026-10-04，`agentctl/handoffs/done/2026-10/home-2026-10-04/aniya/REPORT.md`）；不只皮膚，假髮與私有衣服的 ARMA 也一樣（2026-10-26 Varinia，`agentctl/handoffs/home-2026-10-26/aniya/REPORT.md`）。

**Why:** WNAM 跟 HDPT/facegen 是分開系統，換臉工具預設動 WNAM、換種族工具預設不查 WNAM，兩邊各漏一半。

**How to apply:** 換臉後查目標 WNAM 是否被 quest/腳本依賴；換種族後跑 `python3 agentctl/tools/look_transplant/race_gear.py check --layer <層名>`（exit 1＝有回歸）：它連 skin、outfit、inventory、定義 plugin 的私有裝備一起比 ARMA 種族清單，抓得到 2026-10-26 Varinia 型（假髮藏不住原髮、衣服隱形）；皮膚回歸可改回原版 `000D64 SkinNaked`，其餘補 ARMA 種族。相關：[[look-transplant-workflow-and-picker]]、[[hide-donor-after-look-transplant]]。
