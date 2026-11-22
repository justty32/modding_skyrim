# racemenu-face — AI 捏臉第二階段起的派線清單

[plans](../README.md)｜工作流 [racemenu](../../racemenu/README.md)

Done when: 下列每項都寫明做什麼、相依、要使用者授權的事、工作量、驗收方式，可以直接抄進 BRIEF 派線。

第一階段（2026-11-22，`racemenu-workflow` 線）已完成：

- 工作流文件。
- `agentctl/tools/jslot/` 離線讀、驗、改、比工具。
- 滑桿語意資料檔。

依據：調查 REPORT `agentctl/handoffs/home-2026-11-22/racemenu-survey/REPORT.md` §6d–6e。

**進度（2026-11-22，`npc-face-tools` 線）**：R5 正向、R4 的觸發元件、R6 的驗證邏輯已做（離線，有測試），工具在 `agentctl/tools/npc_face/`；R1、R2、R3、R7 未動工。各項狀態寫在該節第一行。

建議順序：R1→R2（離線看得到形狀）；R3＋R4 同一次開機做（試點授權頁 [npc-face-pilot](../../../user/2026-11-22-npc-face-pilot.md)）。R6 的 jslot 編輯開放、R7 可隨時插入。

## R1 FRTRI003 解析器＋把 NAM9 套到頂點

- **做什麼**：解析 head chargen／races tri 的 base 頂點、三角形與 morph delta；給一份 jslot，算出套用 NAM9 和 NAMA 之後的頂點。
- **相依**：`agentctl/tools/esplib.bsa` 抽 `femaleheadchargen.tri`（調查線 `wf/temp/racemenu-survey/loop/` 有樣本）。
- **授權**：無（只用 stdlib，不碰遊戲）。
- **工作量**：約 1 天。
- **驗收**：解析出的 morph 名集合等於 `strings` 看到的名稱（NoseLong…LipType30、VampireMorph）；單一 morph 權重 0 時頂點等於 base；有測試。

## R2 離線出圖驅動（段 3）

- **做什麼**：把 R1 的頂點渲染成正面、側面 PNG，候選和基底並排輸出。有兩條路：
  - **甲**：自寫 numpy z-buffer。用 `projects/model-converter/.venv` 現有的 numpy 和 Pillow，不用安裝。
  - **乙**：拆用 Skyrim Universal Viewer 的 NIF 渲染器，見 [planning](../../planning.md) roadmap「離線出圖原型」。
- **相依**：R1。走乙要先完成那一項。
- **授權**：甲無。乙要使用者授權 pip 安裝 PyQt6，並同意執行 SUV 的程式碼（它的授權未宣告，只能自用，不能把程式碼搬進 repo）。
- **工作量**：甲的幾何版 1–2 天，貼圖版另加 2–3 天；乙約半天原型，加上接 R1。
- **驗收**：同一份 jslot 出圖可以重現（相同 hash）；「單軸 +0.5」的差異圖只在該部位有變化。另外用它**校準 NAM9 的正負方向**：結果寫回 `racemenu/sliders.json` 的 `neg_pole`／`pos_pole`，`confidence` 改成「實證（離線）」。

## R3 遊戲內套 preset＋AgentBridge 截圖閉環（段 4）

**狀態**：未動工。`cgf` 主控台路線找不到提供者（`npc-face-patch` REPORT §2），套 preset 改用 R4 的觸發 ESP。

- **做什麼**：包裝 `qa_runner`。包含這些步驟：
  - 暫存 jslot 的放進與收回。
  - 用 `/console` 呼叫 `CharGen.LoadPreset`；`cgf` 不認時改用 ConsoleUtilSSE NG。
  - 用 `/screenshot` 存圖，並統一命名。
  - 不存檔的守門。
  - teardown 稽核。
- **相依**：AgentBridge、runtime-qa、`lock.sh`、`envsnap`。
- **授權**：每次都要使用者當場授權以下各項：
  - (a) 開遊戲並取 desktop／game 鎖。
  - (b) 在 `instance/` 暫時寫入、再刪除 jslot。
  - (c) 對 baseline 存檔開 `showracemenu`。不存檔，但要接受未知的副作用。
- **工作量**：約 1 天，加一次實機。
- **驗收**：`Hatak.jslot` 和改了 3 個值的 `Hatak_t1.jslot` 各一張截圖，兩張看得出差異；之後 `instance/` 沒有殘留；profile 稽核綠燈；鎖目錄是空的。順便用截圖校準方向。

## R4 匯出頭部試驗

**狀態**：觸發元件已建置（`agentctl/tools/npc_face/trigger/`：小 ESP＋Papyrus，`player.addspell` 觸發），runtime 步驟寫成草案，**未實機**；等試點授權。

- **做什麼**：在 R3 那次開機時呼叫 `CharGen.ExportHead("p1test")`，確認會不會產出 NIF 和 tint、檔案落在哪裡、shape 名長什麼樣子。
- **相依**：R3（同一次開機）；`skee64.ini` `bEnableHeadExport=1`（已開）。
- **授權**：同 R3。另外要授權在 `overwrite/` 產生匯出物、事後收回。
- **工作量**：約 1 小時（併在 R3 內）。
- **驗收**：產物存在，並用 `tools/bodyslide_mesh_check.py` 或 houseCARL `nif_inspect` 讀得出 shape 清單；沒產物就記錄原因，改評估 CK 路線。

## R5 jslot→NPC patch 層轉換（段 6）

**狀態**：正向已做——`jslot2npc.py`（record）、`facegen_install.py`（上架，未以真實匯出檔驗證）、`build_layer.py`（一條指令；試點 Hatak→Muiri 停在缺匯出頭檔）。反向 NPC→jslot **未做**。工具改用 esplib 讀贏家＋自帶寫入器，不經 houseCARL `set_field`。

- **做什麼**：產生換臉層，寫入 NAM9、NAMA、PNAM、FTST、TintLayers＋QNAM、NAM7、HCLF（找現成的 CLFM 或新建一筆）；加上上架工具，把 ExportHead 的 NIF 處理成 `facegeom/<plugin>/<id>.nif`（改 shape 名、改 slot、複製 tint、檢查和 PNAM 一致）。也要做反向的 NPC→jslot，給段 1 用「NPC 現有的臉」當基底。
- **相依**：`npc-face-patch` 報告定案的途徑；R4 的結果；houseCARL `set_field`／`nif_set`／`place_asset`；`look_transplant` 的 gate。
- **授權**：部署要走 profile-change 授權。
- **工作量**：2–5 天，視途徑而定。
- **驗收**：層的 ESP 通過 `check_masters`；facegen 的 shape 名和 PNAM 一致；和 `transplant.py --verify` 同等的檢查綠燈；實機不是灰臉。

## R6 headParts 離線驗證

**狀態**：驗證邏輯（性別旗標、valid races FLST、是否在現役載入序）已在 `npc_face/records.py`＋`jslot2npc.py`；jslot 工具的 `headpart` 修改**仍未開放**（待把同一套檢查接進 `jslot/edit.py`）。

- **做什麼**：用 esplib 解析 `formIdentifier` 指到的 HDPT，檢查類型、性別、種族清單是否合法；通過的話，jslot 工具再開放 `headpart` 修改（換髮型、瞳色、眉型）。
- **相依**：esplib、`whichmod`。
- **授權**：無。
- **工作量**：約 1 天。
- **驗收**：有測試；拿本機 8 份 jslot 跑，不合法數為 0。

## R7 jslot↔BodySlide xml 轉換（歸 bodyslide）

- **做什麼**：把 jslot 的 `bodyMorphs`（RaceMenu 身體滑桿）和 BodySlide preset xml 互轉，數值換算為 0–1 對 0–100。
- **相依**：`RaceMenuMorphsCBBE` 裝上之後才會有真的身形 morph；滑桿名稱對照用調查線的 `body-slider-crosswalk.json`。
- **授權**：無。
- **工作量**：約半天。
- **驗收**：互轉一圈後值不變；有測試。
