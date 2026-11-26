# 臉：RaceMenu 實機匯出與遊戲內取景

[lessons 索引](README.md)

## racemenu-export-head-parts-not-applied

> 2026-11-22：對主角套 preset（Papyrus `CharGen.LoadPreset`／`LoadCharacter` 或 RaceMenu UI）再 `ExportHead`，tint／髮色／體重會套上，**頭部件可能不換**——主控台 `setrace`／`sexchange` 後頭 3D 不重建，要在 RaceMenu UI 點種族；匯出物要先看 shape 名再談上架

根因：主控台 `setrace`／`sexchange` 改主角後**頭 3D 不重建**，之後不論 Papyrus（`LoadPreset`／`LoadCharacter`）或 RaceMenu UI 載 preset，匯出都是舊部件；在 UI 的 Sliders 分頁點一次種族（先點別的再點回）頭才重建。各場實驗、「關選單時才重建」的否定與 Goam 耳 `--drop-shape` 已收進 [racemenu/bake-export](../workflows/racemenu/bake-export.md#為什麼以前失敗)。證據：`agentctl/handoffs/home-2026-11-22/runtime-pilot/REPORT.md`（場 2–5）、`agentctl/handoffs/home-2026-11-22/face-pilot-2/REPORT.md` §B（S1–S4）。

- skee `SKSETaskExportHead::Run` 直接複製主角**當下的** face node（`NifUtils.cpp:235` 起），所以匯出 NIF 的 shape 名＝畫面上真的掛著的部件；`SaveExternalCharacter` 寫的 jslot `headParts` 是 ActorBase（有 overlay 時讀 overlay，`PresetInterface.cpp:744`）。
- Papyrus 單獨在沒被主控台改過的主角上會不會換部件，沒有另外驗（場 2–4 都先用過主控台）。

**How to apply：**
- 換種族一律在 RaceMenu UI 點種族，**不要用主控台 `setrace` 代替 UI**；主控台 `sexchange` 可以先用來換性別，但之後一定要在 UI 點一次種族讓頭重建（runtime-3 A3：`player.sexchange` → UI 點 Breton → 匯出部件正確）；做法見 [racemenu/bake-export](../workflows/racemenu/bake-export.md)。
- 匯出後**先**讀 NIF shape 名（`npc_face/nifio.py`）或 `Exported/<名>.jslot` 的 `headParts`，對 preset 的部件；少了就是這個坑，不要拿去上架（`facegen_install` gate a 會 FAIL，這是對的）；多了（耳朵）就用 `--drop-shape`。
- 畫面截圖不能當「部件已換」的證據：tint、髮色、頭貼圖（灰髮、刀疤、戰紋）都會變，畫面上「像套上了」，近看才有原部件痕跡（例：鬍渣）。

實機操作配方（同場驗證有效）：

臉部取景：主角在第一人稱看不到自己。`tfc` 凍住相機 → `player.setpos` 把主角放到相機前 70–90 單位、`setangle z` 轉 180° 面向相機 → `fov 45`、`tm` 關 HUD → spectacle 截圖；側面再轉 90°。NPC 同理：`placeatme <base>` 出複本、用 AgentBridge `/console` 帶 `ref` 對複本 `setpos`／`setangle`，`tai` 定住 AI，拍完 `disable`＋`markfordelete`。

- AgentBridge 0.11.0 `input_tap` 在焦點正常時仍回 `environment_blocked`；`xdotool key`（Skyrim 是 XWayland 視窗）可用，滾輪 `click 5` 可拉遠到第三人稱。
- console `setrace` 會跳 crossbow 模組的 MessageBox（「changed race in 1st person」），用 `select_message_box(index=0)` 關；`coc` 新角色會跳 `Done Writing`。
- Papyrus 字串常數不分大小寫地共用字串表：腳本寫 `"OK"`，log 印出 `ok`。比對 log 時不分大小寫。

**F5 真頭是批次拍照前的閘門**（2026-11-25 miku-face，流程已收進 [racemenu/design-session](../workflows/racemenu/design-session.md)）：玩家已是 KuroneNord、畫面有尖耳，F5 卻是 FemaleHeadNord 996 點；眼、嘴已吃到 Chloe 雕刻，尖耳另來自 Goam。先載一份基準、Sculpt F5 匯出 NIF，核 shape 名、拓撲及點數（本案正確頭 AAA_HPH 3832、眉 371、Ocean 176，用 Goam 空白耳 000850 排除耳殼；996／3832 是本案指紋，不是通用頭模常數）。jslot 的 headParts 是記錄層，不可替代 live NIF。不要把「髮色變了」「lint 過」「getisrace 正確」當作換頭成功；真頭過關再批次拍照。旗標面的邊界見 [[custom-race-playable-and-valid-headparts]]。

出處：`agentctl/handoffs/home-2026-11-25/miku-face/` 下 `REPLIES-2.md:5`、`:7`、`:29`（agentctl `21355dee`）；`REPORT.md:21`（`44c11491`）。
相關：[[custom-race-blocks-facegen-load]]、[[face-bugs-check-real-actor-and-upstream-fomod]]

## facegen-neck-seam-export-weight

> 2026-11-22 runtime-3：RaceMenu 匯出的頭，脖子是照**匯出當下主角的體型（weight）**烤的；NPC 最終體重（NAM7）和它不同，脖子底部就有一圈縫（脫衣也在，看得到後面的頭髮）。匯出前在 Sliders 把「體型」調到 NPC 最終 weight÷100

證據：`agentctl/handoffs/home-2026-11-22/runtime-3/`（A1–A4 截圖與 `data/`）：主角體型 0 時匯出、NPC 保留 NAM7 100 → 臉、部件、貼圖都對但脖縫明顯；主控台 `setnpcweight` 只有 0 時縫消失（縫由體型差造成，不是貼圖或部件）；滑桿調到 1.00 再匯出重建 → 正面／側面／背面／裸頸都正常。

**How to apply：**
- 匯出前先決定 NPC 最終體重：`--keep-weight` 用 NPC 原 NAM7，否則用 preset 的 weight；滑桿調到那個值÷100 再匯出（[bake-export](../workflows/racemenu/bake-export.md) 第 4 步）。
- `build_layer` 帶 `--export-weight <滑桿值×100>`，gate 會擋體型不一致的層；沒帶只有 WARN。
- 頸部一點陰影是光照，和接縫分開看：接縫是一圈斷開、能透看到後方。

## custom-race-playable-and-valid-headparts

> 自訂種族列得出來與頭部件可選，是兩道不同的門。

- 現象：原 Kurone 種族不能直接在 RaceMenu 選；補出種族也不代表 KS 髮、眉、眼可用。
- 真因：RACE 缺 Playable；部件的有效種族 FLST 也要含目標種族。S1 修改兩筆 RACE 的 Playable 與名稱，並在八張贏家 FLST 保留既有成員後追加兩種 Kurone。種族預設頭仍可能是原版 Nord。
- 驗法：讀 RACE／HDPT RNAM／FLST 的實際贏家；遊戲內用 getisrace 確認 actor，不信列表座標或 jslot metadata。載 preset 後另匯出真頭驗部件。
- 避法：把「可選種族」「部件適用種族」「預設及實載部件」分開驗收；覆寫 FLST 要 forward 贏家，不用自己的短清單蓋掉別人。只在獲授權的隔離測試層部署。
- 出處：`agentctl/handoffs/home-2026-11-25/miku-face/support/REPORT.md:18`、`:23`（agentctl `18953859`）；`REPLIES-2.md:5`、`:7`（`21355dee`）。
- NPC 用自訂種族時 facegen 整個不載入是另一回事，見 [[custom-race-blocks-facegen-load]]。

邊界：不能斷言「record header NonPlayable 單獨造成回退」。原 HDPT header 0x04、DATA 0x04；S1v2 成功時 DATA 已為 0x05、女性種族預設已換，**header 仍是 0x04**；多因素同改沒有隔離單一旗標因果。旗標、RNAM、預設、載入後 3D 要分層排錯。

## eye-sculpt-requires-matching-head

> 黑眼窩先查部件與相對位置，不先改貼圖或把所有眼雕刪光。

- 現象：早期完整眼雕出現黑眼窩；關眼雕的對照能看見虹膜。
- 真因／邊界：眼部件已移動、頭仍為錯誤的 Nord 部件，造成相對幾何不匹配。這支持眼雕與頭的組合有問題，不能單憑當時照片判定 Chloe 眼雕本身壞掉，也不能當作「任何整顆眼睛位移必黑」的定律。最後在正確頭眉上局部改上瞼可成功。
- 驗法：先過 live 頭部件 gate，再固定頭、貼圖、燈光，分別開關頭雕／眼雕；核眼球、眼瞼與虹膜位置。定稿上瞼只動頭 154 點、眼件 54 點，F5 最大位移 0.237133，離線預期 0.237130。
- 避法：不要把整顆眼球平移當作開瞼；使用局部遮罩，保留眼球與下瞼，最後用 F5 與正側照一起驗。
- 出處：`agentctl/handoffs/home-2026-11-25/miku-face/REPLIES-instance.md:5`（agentctl `a43517d9`，R7 對照）；`REPLIES-2.md:5`（`21355dee`）；`REPORT.md:21`（`44c11491`）。
