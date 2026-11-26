# 資產移植與 ModForge 工具評估

[lessons 索引](README.md)｜地圖移植的引擎限制見 [map-port-and-world-conflicts](map-port-and-world-conflicts.md)

把外部遊戲資產／工具搬進 Skyrim、或評估 ModForge 能否生成某功能時反覆踩到的方法論與邊界。

## asset-porting-feasibility-checklist

> 判斷能否移植某遊戲資產進 Skyrim 要過四道獨立關卡（容器解密／網格轉換／場景佈局／碰撞），佈局最容易低估；判加密要用工具快速實測不查文件；鐵律僅本機個人使用；移植管線除靜態擺放檔也要讀事件腳本才抓得到開場初始狀態

2026-08-11 判準：四關（容器/網格/佈局/碰撞）各自查證，單一難度分數會過於樂觀；佈局最容易被低估（沒有它只抽到散裝資產），碰撞是唯一可用通用演算法重生的一關；「已完成移植」案例若全是單體裝備、沒有地圖佈局，不能當佈局管線已解的佐證。判加密直接拿 AssetStudio（Unity）／FModel（UE4/5）開安裝目錄，要完整場景重建才上 AssetRipper。移植鐵律：僅本機個人使用絕不發佈，現行營運網路遊戲（anti-cheat/EULA 禁反向工程）一律排除或降到最後。

**事件腳本（EMEVD 初始狀態）**：DS 原引擎用「同座標放兩份（完整版／破壞版），開場靠 EMEVD 關掉其中一份」表達可破壞物與劇情狀態；只讀 MSB 會把壞掉前後同時擺出來、把短暫碰撞擺成永久幽靈碰撞，或漏掉開場 `Constructor()` 關閉的物件（例：`o8510` 補地板蓋洞口，移植版「一開始就看到本該觸發劇情才出現的塌陷」）。移植前先跑 EMEVD 初始狀態過濾：找同模型同座標重複 entity、找被 Constructor 關掉的 entity（`agentctl/handoffs/done/2026-08-30/dsport2-2026-08-30/FINDING.md:48-62`）。判分支確定性：前向 `SkipLines` 類指令在 `join=i+1+line_count` 與未跳過路徑匯流，只有 `[i+1,join)` 算條件性，join 之後當確定性保留；`ReturnIf*` 沒有 join 點，之後整段降為條件性——漏掉「join 後恢復確定性」會把本該確定關掉的 entity 誤判成條件性（`agentctl/handoffs/done/2026-08-30/dsport3-2026-08-30/HANDOFF-cx-dsp6.md:40-55`）。

**DS→Skyrim 轉檔管線**（2026-10-23）：(a) 自訂 worldspace 進場用 `cow <worldspace名> <x> <y>`＋`player.setpos z <高度值>`，`coc <起點標記>` 結構性不可行。(b) 純觸發／音源類物件（objbnd 無可渲染幾何）轉 NIF 會報 `glTF has no meshes`，不是工具 bug，排除出 placement 清單。(c) `convert_or_reuse()` 以 `cwd=model-converter` 起子程序，一律傳絕對路徑（相對路徑得到 `cannot read source`）。(d) 同時有 `oXXXX` 與 `oXXXX_1` 兩份 FLVER 時，`_1` 通常是「破壞後型態」不是 LOD，先比三角面數再決定轉不轉；MSB 只引用主 stem。(e) 旋轉必須用基底變換 `R_sky = B·R_ds·B⁻¹`，不能用「交換 Euler 軸」的捷徑，要寫共軛恆等式測試釘住（`agentctl/handoffs/done/2026-08-29/dsport/cx-ds3-HANDOFF.md:14-27`、`cx-ds2-HANDOFF.md:26-36,64-68`、`agentctl/handoffs/done/2026-09-05/dsport4-2026-09-05/STATE.md:165-166`）。

**How to apply:** 評估新移植來源先四關各自查證＋鐵律排除；讀取管線除靜態擺放檔外一定連事件腳本一起讀。「已有人移植過」不能當佈局已解的佐證。相關：[[dsport-render-constraints]]

## modforge-external-tool-survey-and-dependency-policy

> 外部工具/library 要補 ModForge 缺口前先查兩件事：授權（GPL 系列只能重新實作概念不能搬碼）與有沒有無頭 CLI/API；ModForge 本身外部依賴策略是 native/SWF library 一律 opt-in、預設零依賴，含用 Quest Conditional bool 做偽 MCM 免裝 SkyUI

tool-survey 盤點：Wrye Bash 的 LeveledListsPatcher 是 GPL-3.0，leveled list 自動合併只能重新實作演算法不能搬碼，且綁死 wx GUI 沒有無頭介面；CKPE 只穩定/加速 CK GUI，沒有 command-line/batch 介面，不能當 facegen 自動化 API；SkyPlace 證明 runtime reference 互動 UX 可行，但沒有 ESP writer（只存存檔 sidecar）也沒有 LICENSE，不能補場景編輯缺口。授權與無頭介面任一缺就只能當設計參考。

依賴策略（盤點 JContainers/PapyrusUtil/powerofthree's Tweaks/SkyUI/UIExtensions 後定）：ModForge 產出的 plugin 不得在功能上依賴這些 native/SWF library；要做開關先用純 `extends Quest` Conditional bool＋`GetVMQuestVariable` 做偽 MCM，只有真的需要玩家選單才 opt-in 生成 SkyUI 依賴。新功能需要外部 library 一律設計成 opt-in 區塊，預設路徑零依賴。

## modforge-record-boundary-and-tooling-gotchas

> 評估 ModForge 能否生成某功能看核心邏輯是 record/JSON/ini 還是編譯進 DLL（不看開源與否）；大規模對話投放也是全靠 condition+FormList+override 不靠複雜 Papyrus；console `coc` 只吃 CELL EditorID 不吃 XMarker；`dump` 不展開 XMRK subrecord 要配 raw-byte grep；本機無 BSA/PEX 工具時自寫 Python parser 比找第三方庫可靠；xLODGen 要另外去官方 GitHub 抓、四個 LOD 級別要各用全新空白輸出目錄

**能力邊界（資料驅動 vs 編譯進二進位）**：ModForge 是 build-time JSON→esp 的 record 生成器；選單/邏輯編譯進消費者 DLL（不論開源閉源）就只能列為前置依賴，只有 config/record/loose 文字檔層級在可生成範圍。對話投放也一樣：參考 mod 投給誰全寫在 condition（尤其 `GetIsVoiceType`）＋FormList 靜態名單＋override 既有 vanilla INFO，要生成的 Papyrus 只有節流計時器／短 fragment／alias clear 三類；ModForge 目前沒有取出 vanilla Quest/DialogTopic/INFO 覆寫的入口，也不支援 `GetIsVoiceType`/`IsInList`，要做對話包優先補這兩項。

**操作坑**：
- console `coc` 只吃 CELL 的 EditorID；要到特定 XMarker 先 `coc` 該 cell 再 `player.setpos`。
- ModForge `dump` 不展開 REFR 的 `XMRK`，驗 map marker 類旗標要對編譯後 ESP 做 `rg -aob` raw-byte grep。
- 沒有官方文件化介面時自己動手：找不到能開 BSA 的工具／庫時自寫 Python 讀 BSA v105 header 就解得出全部檔案；PEX 同理自寫 header/string-table 解析器，不必完整反編譯器。
- xLODGen 不在 SSEEdit/DynDOLOD 工具組內，去 sheson 官方 GitHub release 抓（論壇連結會 403）；已存在的 DDS 會讓它跳過生成，LOD4/8/16/32 各用全新空白 output 目錄。
