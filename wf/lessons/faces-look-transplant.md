# 臉：換臉流程與工具

[lessons 索引](README.md)

facegen 與頭部件一致性的規則（大媽臉／素臉的真因）在 [faces-facegen-consistency](faces-facegen-consistency.md)。

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

## look-transplant-wnam-and-skin-checks

> 換臉/換種族常漏兩個欄位：`copy_npc_appearance` 會把 donor 的 WNAM 一起搬過去蓋掉目標原本皮膚（可能有 quest 依賴）；換種族時若 WNAM 指的私有皮膚 ARMA 只涵蓋舊種族，新種族脫光或穿無手套/靴子衣服時缺甲部位直接消失。

copy_npc_appearance 連 HDPT／HairColor／TintLayers／WNAM 整組都搬，donor 髮型 HDPT 若指向本機沒有的 provider 會變禿頭（2026-09-01，`agentctl/handoffs/done/2026-09-01/hnpc-2026-09-01/MIXMATCH.md:14-27`）。換種族層改了 RNAM 卻沒動 WNAM 時，私有皮膚 ARMA 只涵蓋舊種族（2026-10-04，`agentctl/handoffs/done/2026-10/home-2026-10-04/aniya/REPORT.md`）；不只皮膚，假髮與私有衣服的 ARMA 也一樣：Varinia 的偽裝腳本跨領地會發一頂佔 slot 31／41 的假髮，假髮 ARMA 只列 Imperial，換成 WoodElf 後假髮把頭髮藏掉、自己又畫不出來＝光頭，同理預設洋裝一直隱形（2026-10-26，`agentctl/handoffs/home-2026-10-26/face3/REPORT.md` 第 0 節；全隨從掃描 `agentctl/handoffs/home-2026-10-26/aniya/REPORT.md`）。

**Why:** WNAM 跟 HDPT/facegen 是分開系統，換臉工具預設動 WNAM、換種族工具預設不查 WNAM，兩邊各漏一半。

**How to apply:** 換臉後查目標 WNAM 是否被 quest/腳本依賴；換種族後跑 `python3 agentctl/tools/look_transplant/race_gear.py check --layer <層名>`（exit 1＝有回歸）：它連 skin、outfit、inventory、定義 plugin 的私有裝備一起比 ARMA 種族清單，抓得到 2026-10-26 Varinia 型（假髮藏頭髮又畫不出來、衣服隱形）；它掃不到別的 plugin 用腳本或劇情發的衣服；皮膚回歸可改回原版 `000D64 SkinNaked`，其餘補 ARMA 種族。私有身體層（如 `Kurone7-PrivateBody`）改了誰的 WNAM 也要跑同一個檢查：`--layer` 給完整 mod 名稱時不限 `*-Look-From-*` 層（2026-10-26，`agentctl/handoffs/home-2026-10-26/bodyswap2/REPORT.md` §1c）。相關：[[look-transplant-workflow-and-picker]]、[[hide-donor-after-look-transplant]]。
