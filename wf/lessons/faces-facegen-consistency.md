# 臉：facegen 與頭部件一致性規則

[lessons 索引](README.md)

換臉流程與工具在 [faces-look-transplant](faces-look-transplant.md)；排錯見 [faces-troubleshooting](faces-troubleshooting.md)；RaceMenu 匯出頭見 [faces-racemenu-runtime](faces-racemenu-runtime.md)。

## facegen-verify-size-md5-not-existence

> 2026-09-09 Vilja「大媽臉」真因——工人把素材 HDPT 的基礎頭 femalehead.nif 當 FaceGeom 抄進去；驗 facegen 要看逐對大小／md5 各不相同，不能只看檔案存在

2026-09-09 使用者看到 Vilja「臉是大媽臉」。真因：Kurone 包十個角色共用的 HDPT 基礎頭 `femalehead.nif`（沒捏過的素臉）被當成 FaceGeom 複製到 `facegeom/<esp>/<formid>.nif`。素臉檔存在、路徑對、ESL 旗標對，靜態 gate 全綠，畫面仍是錯的。

**How to apply:**
- 換臉／重烤 facegen 的驗收要加：**每顆 facegen nif 大小與 md5 逐對列出，且彼此不同、且不等於素材 HDPT 基礎頭的 md5**；捏過的臉通常 0.7–2.5 MB，素頭固定 ~322 KB。
- 順帶：`strings` 讀 nif 內嵌貼圖路徑，證明頭身貼圖同源；髮型 shape 名要在 nif 裡。
- 同類坑：[[oar-copy-folder-bypasses-gates]]（複製繞過閘門）、[[housecarl-merge-facegen-backslash-filename]]。

## facegen-headpart-count-mismatch-discards-facegen
<a id="look-layer-must-carry-hdpt-flst-clfm"></a>
<a id="hdpt-edid-must-match-facegen-shape-names"></a>

> 引擎拿 NPC 實際頭部件集合（PNAM＋ExtraParts＋種族預設補的嘴／眼／眉／臉）的 HDPT EDID 對 facegen nif 的 shape 名，筆數或名字一塊對不上就整顆預烤 facegen 作廢、執行期重生＝素臉（大媽臉）／黑臉；換臉層要帶齊素材的 HDPT／FLST／CLFM，EDID 要等於 shape 名

規則（Face Discoloration Fix 說明也有寫）：**head parts 與 facegen nif 對不上，整顆預烤臉作廢、執行期重生且不載入上色資料**。NPC_ 沒有 NAM9／NAMA／tint layers 時（Kurone 素材 tint layers 是 0，妝烤在 facetint 裡）→ 素臉；有 Face Discoloration Fix（FaceGenFixes.dll）時是成人素頭，FDF 關＝黑臉。層開著時連本體那顆 facegen 也被拒，所以「藏檔零變化」不能推成「引擎不讀路徑」。

三種對不上的方式（都是大媽臉）：
- **少帶記錄**（2026-09-09 Yoana）：換臉層只帶 TXST＋NPC_，沒帶素材的 HDPT（頭部零件）／FLST（適用種族清單）／CLFM（髮色）。正確前例：Livia（HDPT 6＋FLST 1）。
- **EDID 被改名**（2026-09-12 Ashe，使用者親看）：`Ashe-Look-From-A2-Dev-2026-09-07` 五筆私有 HDPT 的 EDID 被 transplant 流程改掉，nif 裡 shape 仍是素材原名（`AAA_Hairline`、`AAA_Scalp`、`AAA_Hair`、`AAA_GirlHeads`、`AAA_FemaleBrows`）。只比數量與檔案的離線檢查全過。
- **種族補的部件**（2026-09-11 Yoana，已修）：nif 7 塊 shape 含嘴 `FemaleMouthHumanoidDefault`，PNAM 只寫 4 塊，引擎用自訂種族 `BB02YoanaRace` 的預設嘴 `BB02YoanaMouth` 補上 → 名字不符。修法層 `Yoana-FaceGen-Match-Dev-2026-09-11`：PNAM 補 `05150F FemaleMouthHumanoidDefault`，並把她的種族加進該 HDPT 的 ValidRaces FLST（純加法）。

**How to apply（換臉層驗收）：**
1. 用 nif 內 shape 清單（BSFaceGen 下每塊的名字）對 NPC_ **實際會用到的完整頭部件集合**逐塊對名；目標是自訂種族時特別容易漏「嘴」。對不上就明寫進 PNAM（用素材同一塊），或改 nif 的 shape 名。
2. 層內 HDPT 筆數 ≥ 素材 PNAM 筆數、每個 HDPT 的 ValidRaces FLST 含目標種族、CLFM 帶齊。
3. 症狀：頭髮／臉型對但**無妝慘白**＝facegen 被作廢；看到成人素臉先查記錄層一致性，不要先怪貼圖或目錄。
4. 二分實驗：先「PNAM 換本體＋藏層 facegen」看本體臉回不回來，一輪就能把元兇圈進頭部件閉包。

工具：transplant.py 保留 donor EDID，gate 5 已把 Race `HeadData` 預設件納入、與 shape 名做大小寫敏感 multiset 等值（fail closed，`agentctl/tools/look_transplant/README.md:103-107`）；`--verify <層目錄>` 驗既有層。audit 見 `agentctl/handoffs/home-2026-09-13/tpfix/data/layer-audit.md`（當時 Noela／Noemie／Yoana／Yvanni 四層 FAIL 未修）；已換臉角色的掃描清單見 `agentctl/handoffs/home-2026-09-12/ashe3/REPORT.md`。

MO2 在 wine 下的 VFS 對目錄大小寫不敏感，facegen 目錄大小寫不一致（如 `bb02yoanafollower.esp/` vs `BB02YoanaFollower.esp/`）不是真因——全機 488 條大小寫不一致的路徑裡有好幾個正常運作的層。判準：一個「真因」若在其他正常案例裡也成立，它就不是真因。例外：同一個 mod 裡兩份大小寫不同、**內容也不同**的 facegen 並存時，哪一份生效不確定（2026-10-26 `FOL-Recorder-Bugfix`，見 [[mo2-silent-collision-failure-modes]]）。

同機制：[[rs-children-missing-esp]]（RS Children 少裝 RSChildren.esp，小孩全成大媽臉）。相關：[[outfit-hair-slot-hides-headparts]]、[[custom-race-blocks-facegen-load]]、[[facegen-verify-size-md5-not-existence]]

## nif-positions-topology-and-tri-are-separate-evidence

> 比較身形要分開驗 positions、頂點索引與三角連接；同頂點數、檔案大小或 slider 名稱不構成 TRI 相容證據。

2026-11-02。NIF 同頂點數、同三角數，甚至 NiSkinPartition vertex map 相同，三角連接仍可能不同。位置 hash 能證明座標陣列相同／不同；同索引 RMS 位移沒有解剖標誌對照時，只是陣列差異。bbox 能證幾何範圍差異，不能換算成視覺好壞。OSP 的 small／big 值是輸入，省略不等於已烘焙的零，也不能據此認定成品就是某個公開 preset。包內附 `.tri` 只證存在，不能推成可接另一身體。

**How to apply:** 分別驗證位置與三角連接（排除三角列次序／繞序差異），標明索引對應是否已證；TRI 未驗就保持未證，不直接移接。不要以 NIF 大小推形狀，也不要以內嵌貼圖路徑代替 ARMA／TXST 的皮膚解析。

來源：private `agentctl/handoffs/home-2026-11-02/kurone-intake/REPORT.md:28–40`（既有 NIF、OSP、TRI 與 record 離線比較）。

## facegen-not-recoverable-from-npc-record-alone

> NPC 記錄轉成 jslot，不等於還原作者的臉。

現象：Chloe 無 NAM9／NAMA；只轉 headParts 與記錄值，得到普通圓耳臉而非 FaceGen 的 Chloe。

真因／邊界：FaceGen 與 HDPT 頭同拓撲 3832 點，但位移平均 0.42、最大 2.26；UV 也不同。本機 33 支 Kurone 女性 HDPT 頭相同。132 個已提供 TRI morph 擬合仍殘差 38%，且需超範圍權重。因此現有記錄／滑桿不能還原。**「用未發佈底模烤成」僅是可能製作來源，資料不足以證明作者流程或有一顆未發佈底模**；可證的是外觀差異保留在 FaceGen。

驗法：沿 NPC PNAM、HDPT 模型與 FaceGeom 分別解析，對齊座標空間，核拓撲、頂點差與 UV；不要只看 NAM9 有沒有值。

避法：保留原 FaceGen 為外觀依據；同拓撲且座標／體重確認後才做 FaceGen-HDPT sculpt 差值。頂點差不會自動搬 UV、材質或皮膚。

出處：`agentctl/handoffs/home-2026-11-25/miku-face/offline-render/O-DETAILS.md:28`、`:30`、`:32`（agentctl `4d98b502`）；`REPORT.md:19`（`44c11491`）。
