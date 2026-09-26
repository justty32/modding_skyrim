# 臉、隨從、身體與動畫（2/4）

[lessons 索引](README.md)｜同主題：[faces-followers-bodies](faces-followers-bodies.md)、[faces-followers-bodies-3](faces-followers-bodies-3.md)、[faces-followers-bodies-4](faces-followers-bodies-4.md)

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
