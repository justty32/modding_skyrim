# 臉：RaceMenu 實機匯出與遊戲內取景

[lessons 索引](README.md)

## racemenu-export-head-parts-not-applied

> 2026-11-22 runtime-pilot 四場實機：用 Papyrus（`CharGen.LoadPreset`、`CharGen.LoadCharacter`）對主角套 preset 再 `ExportHead`，tint／髮色／體重會套上，**頭部件不會換**——匯出 NIF 仍是原主角（或新角色種族預設）的部件，存檔主角與 `coc` 新角色都一樣；匯出物要先看 shape 名再談上架

事實（證據：`agentctl/handoffs/home-2026-11-22/runtime-pilot/REPORT.md`）：
- skee `SKSETaskExportHead::Run` 直接複製主角**當下的** face node（`NifUtils.cpp:235` 起），所以匯出 NIF 的 shape 名＝畫面上真的掛著的部件；`SaveExternalCharacter` 寫的 jslot `headParts` 是 ActorBase（有 overlay 時讀 overlay，`PresetInterface.cpp:744`）。
- 場 2：console `sexchange`＋`setrace BretonRace`＋`LoadPreset` → 部件仍是 `MaleHeadImperial`、`HumanBeard31`…，只多一個 `FemaleMouthHumanoidDefault`；頭的 texture set 卻是女頭貼圖，畫面上看起來「像套上了」（灰髮、刀疤、戰紋都在），近看有鬍渣。
- 場 3：先 `Game.ForceThirdPerson()`（camera state 9）再套，結果相同——不是第一人稱沒重建的問題。
- 場 4：改走 `LoadCharacter(player, BretonRace, src)`（skee `ApplyPreset`：SetRace、清 `overlayRace`、不篩直接 `ChangeHeadPart`）→ 部件仍不變。
- 場 5：主選單 `coc QASmoke` 開新角色（Nord 男）再跑一樣流程 → 部件是 Nord 男預設件＋女嘴＋女眉，Hatak 的 6 件一件都沒上。真因未定位。

**How to apply：**
- 匯出後**先**讀 NIF shape 名（`npc_face/nifio.py`）或 `Exported/<名>.jslot` 的 `headParts`，對 preset 的部件；不符就是這個坑，不要拿去上架（`facegen_install` gate a 會 FAIL，這是對的）。
- 畫面截圖不能當「部件已換」的證據：tint、髮色、頭貼圖都會變，部件沒變也很像。
- 下一步候選（未試）：使用者在 RaceMenu 介面手動載 preset 後由 agent 觸發 `ExportHead`；或 CK Ctrl+F4（備援 D1）。不要再用同一組 Papyrus 呼叫重試。

實機操作配方（同場驗證有效）：
- 臉部取景：主角在第一人稱看不到自己。`tfc` 凍住相機 → `player.setpos` 把主角放到相機前 70–90 單位、`setangle z` 轉 180° 面向相機 → `fov 45`、`tm` 關 HUD → spectacle 截圖；側面再轉 90°。NPC 同理：`placeatme <base>` 出複本、用 AgentBridge `/console` 帶 `ref` 對複本 `setpos`／`setangle`，`tai` 定住 AI，拍完 `disable`＋`markfordelete`。
- AgentBridge 0.11.0 `input_tap` 在焦點正常時仍回 `environment_blocked`；`xdotool key`（Skyrim 是 XWayland 視窗）可用，滾輪 `click 5` 可拉遠到第三人稱。
- console `setrace` 會跳 crossbow 模組的 MessageBox（「changed race in 1st person」），用 `select_message_box(index=0)` 關；`coc` 新角色會跳 `Done Writing`。
- Papyrus 字串常數不分大小寫地共用字串表：腳本寫 `"OK"`，log 印出 `ok`（`DONE status=ok`）。比對 log 時不分大小寫。
相關：[[custom-race-blocks-facegen-load]]、[[face-bugs-check-real-actor-and-upstream-fomod]]
