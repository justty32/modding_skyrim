# 臉：RaceMenu 實機匯出與遊戲內取景

[lessons 索引](README.md)

## racemenu-export-head-parts-not-applied

> 2026-11-22 runtime-pilot 四場實機：用 Papyrus（`CharGen.LoadPreset`、`CharGen.LoadCharacter`）對主角套 preset 再 `ExportHead`，tint／髮色／體重會套上，**頭部件不會換**——匯出 NIF 仍是原主角（或新角色種族預設）的部件，存檔主角與 `coc` 新角色都一樣；匯出物要先看 shape 名再談上架。根因已查明：主控台 `setrace`／`sexchange` 後頭 3D 不重建，解法是在 RaceMenu UI 點種族

事實（證據：`agentctl/handoffs/home-2026-11-22/runtime-pilot/REPORT.md`）：
- skee `SKSETaskExportHead::Run` 直接複製主角**當下的** face node（`NifUtils.cpp:235` 起），所以匯出 NIF 的 shape 名＝畫面上真的掛著的部件；`SaveExternalCharacter` 寫的 jslot `headParts` 是 ActorBase（有 overlay 時讀 overlay，`PresetInterface.cpp:744`）。
- 場 2：console `sexchange`＋`setrace BretonRace`＋`LoadPreset` → 部件仍是 `MaleHeadImperial`、`HumanBeard31`…，只多一個 `FemaleMouthHumanoidDefault`；頭的 texture set 卻是女頭貼圖，畫面上看起來「像套上了」（灰髮、刀疤、戰紋都在），近看有鬍渣。
- 場 3：先 `Game.ForceThirdPerson()`（camera state 9）再套，結果相同——不是第一人稱沒重建的問題。
- 場 4：改走 `LoadCharacter(player, BretonRace, src)`（skee `ApplyPreset`：SetRace、清 `overlayRace`、不篩直接 `ChangeHeadPart`）→ 部件仍不變。
- 場 5：主選單 `coc QASmoke` 開新角色（Nord 男）再跑一樣流程 → 部件是 Nord 男預設件＋女嘴＋女眉，Hatak 的 6 件一件都沒上。當場真因未定位。

**根因（2026-11-22 face-pilot-2 查明，證據：`agentctl/handoffs/home-2026-11-22/face-pilot-2/REPORT.md` §B）**：用主控台 `setrace`／`sexchange` 改主角後，**頭 3D 不重建**；之後不論 Papyrus 或 RaceMenu UI 載 preset，匯出都是舊部件。
- S1–S2：console 改成 Breton 女，再在 UI 載 Hatak → 畫面像換了，匯出仍是原主角 9 件。
- S3：在 RaceMenu 內用 Sculpt F5 匯出 → 仍是舊件，否定「關選單時才重建」。
- S3 續：**在 UI 的 Sliders 分頁點種族（Imperial→Breton，先點別的再點回）**，頭重建；UI 載 Hatak、Sculpt F5 匯出 → 部件正確。關選單後再用觸發 ESP 匯出，結果相同。
- 副作用：UI 換種族時，RaceMenu 把女性 Facial Hair 類 HDPT 滑桿設成第一件，Goam 精靈耳就掛上去（多一個 `GoamElvenEarsBreton` shape）。UI 拿不掉（只有耳朵各款和 `00`，S4），改離線用 `build_layer.py`／`facegen_install.py --drop-shape <shape名>` 刪。
- Papyrus 路線（`LoadPreset`／`LoadCharacter`）不換部件的觀察保留：場 2–4 都先用過主控台 `sexchange`（場 2–3 另加 `setrace`），與上述根因一致；Papyrus 單獨在沒被主控台改過的主角上會不會換，沒有另外驗。

**How to apply：**
- 換種族一律在 RaceMenu UI 點種族，**不要用主控台 `setrace` 代替 UI**；主控台 `sexchange` 可以先用來換性別，但之後一定要在 UI 點一次種族讓頭重建（runtime-3 A3：`player.sexchange` → UI 點 Breton → 匯出部件正確）；做法見 [racemenu/bake-export](../workflows/racemenu/bake-export.md)。
- 匯出後**先**讀 NIF shape 名（`npc_face/nifio.py`）或 `Exported/<名>.jslot` 的 `headParts`，對 preset 的部件；少了就是這個坑，不要拿去上架（`facegen_install` gate a 會 FAIL，這是對的）；多了（耳朵）就用 `--drop-shape`。
- 畫面截圖不能當「部件已換」的證據：tint、髮色、頭貼圖都會變，部件沒變也很像。

實機操作配方（同場驗證有效）：
- 臉部取景：主角在第一人稱看不到自己。`tfc` 凍住相機 → `player.setpos` 把主角放到相機前 70–90 單位、`setangle z` 轉 180° 面向相機 → `fov 45`、`tm` 關 HUD → spectacle 截圖；側面再轉 90°。NPC 同理：`placeatme <base>` 出複本、用 AgentBridge `/console` 帶 `ref` 對複本 `setpos`／`setangle`，`tai` 定住 AI，拍完 `disable`＋`markfordelete`。
- AgentBridge 0.11.0 `input_tap` 在焦點正常時仍回 `environment_blocked`；`xdotool key`（Skyrim 是 XWayland 視窗）可用，滾輪 `click 5` 可拉遠到第三人稱。
- console `setrace` 會跳 crossbow 模組的 MessageBox（「changed race in 1st person」），用 `select_message_box(index=0)` 關；`coc` 新角色會跳 `Done Writing`。
- Papyrus 字串常數不分大小寫地共用字串表：腳本寫 `"OK"`，log 印出 `ok`（`DONE status=ok`）。比對 log 時不分大小寫。
**2026-11-25 補強（miku-face，F5 真頭是開拍整批前的閘門）**：
現象：玩家已是 KuroneNord，畫面也有尖耳，F5 卻是 FemaleHeadNord 996 點／原版眉 102 點；眼 176 點、嘴 141 點已吃到 Chloe 雕刻，尖耳另來自 Goam。

真因／邊界：HDPT 可玩性及種族預設配置未符合預期，但不能斷言「record header NonPlayable 單獨造成回退」。原 HDPT header 0x04、DATA 0x04；S1v2 成功時 DATA 已為 0x05、女性種族預設已換，**header 仍是 0x04**。多因素同改沒有隔離單一旗標因果。

驗法：先載一份基準，Sculpt F5 匯出 NIF，核 shape 名、拓撲及點數。本案 H1 才確認 AAA_HPH 3832／眉 371／Ocean 176，並用 Goam 空白耳 000850 排除耳殼。jslot 的 headParts 是記錄層，不可替代 live NIF；996／3832 是本案指紋，不是通用頭模常數。

避法：旗標、RNAM、預設、載入後 3D 分層排錯；真頭過關再批次拍照。不要把「髮色變了」「lint 過」「getisrace 正確」當作換頭成功。

出處：`agentctl/handoffs/home-2026-11-25/miku-face/` 下 `REPLIES-2.md:5`、`:7`、`:29`（agentctl `21355dee`）；`REPORT.md:21`（`44c11491`）。
相關：[[custom-race-blocks-facegen-load]]、[[face-bugs-check-real-actor-and-upstream-fomod]]

## facegen-neck-seam-export-weight

> 2026-11-22 runtime-3：RaceMenu 匯出的頭，脖子是照**匯出當下主角的體型（weight）**烤的；NPC 最終體重（NAM7）和它不同，脖子底部就有一圈縫（脫衣也在，看得到後面的頭髮）。匯出前在 Sliders 把「體型」調到 NPC 最終 weight÷100

事實（證據：`agentctl/handoffs/home-2026-11-22/runtime-3/`，A1–A4 截圖與 `data/`）：
- A1：face-pilot-2 的 Muiri 層（主角載 Hatak 後體型 0 時匯出，`--keep-weight` 保留 Muiri 100）→ 臉、部件、貼圖都對，脖縫明顯。
- A2：主控台 `setnpcweight` 試 100／0／50，只有 0 時縫消失 → 縫由體型差造成，不是貼圖或部件。
- A3–A4：RaceMenu 內把「體型」從 0 調到 1.00（Right 每格 0.01）再 F5 匯出、重建層 → 脖縫消失，正面／側面／背面／裸頸都正常，體重保持 100。

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
- 出處：`agentctl/handoffs/home-2026-11-25/miku-face/support/REPORT.md:18`、`:23`（agentctl `18953859`）；`REPLIES-2.md:5`（`21355dee`）。

## eye-sculpt-requires-matching-head

> 黑眼窩先查部件與相對位置，不先改貼圖或把所有眼雕刪光。

- 現象：早期完整眼雕出現黑眼窩；關眼雕的對照能看見虹膜。
- 真因／邊界：眼部件已移動、頭仍為錯誤的 Nord 部件，造成相對幾何不匹配。這支持眼雕與頭的組合有問題，不能單憑當時照片判定 Chloe 眼雕本身壞掉，也不能當作「任何整顆眼睛位移必黑」的定律。最後在正確頭眉上局部改上瞼可成功。
- 驗法：先過 live 頭部件 gate，再固定頭、貼圖、燈光，分別開關頭雕／眼雕；核眼球、眼瞼與虹膜位置。定稿上瞼只動頭 154 點、眼件 54 點，F5 最大位移 0.237133，離線預期 0.237130。
- 避法：不要把整顆眼球平移當作開瞼；使用局部遮罩，保留眼球與下瞼，最後用 F5 與正側照一起驗。
- 出處：`agentctl/handoffs/home-2026-11-25/miku-face/REPLIES-instance.md:5`（agentctl `a43517d9`，R7 對照）；`REPLIES-2.md:5`（`21355dee`）；`REPORT.md:21`（`44c11491`）。
