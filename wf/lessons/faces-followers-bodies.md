# 臉、隨從、身體與動畫（1/4）

[lessons 索引](README.md)｜同主題：[faces-followers-bodies-2](faces-followers-bodies-2.md)、[faces-followers-bodies-3](faces-followers-bodies-3.md)、[faces-followers-bodies-4](faces-followers-bodies-4.md)

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
