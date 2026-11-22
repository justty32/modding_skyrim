# NPC 換臉試點：把 Hatak 的臉做成 Muiri 的 patch（要你授權）

[wf/user](README.md)｜工作流 [racemenu／bake](../workflows/racemenu/bake.md)｜原始報告 `agentctl/handoffs/home-2026-11-22/npc-face-tools/REPORT.md`、`npc-face-patch/REPORT.md` §4

**一句話**：離線能做的都做好了。現在只差「進一次遊戲，讓主角戴上 Hatak 的臉，把頭匯出成檔案」。這一步要開遊戲、要暫時改 MO2 設定，所以要你點頭。

## 最新現況（2026-11-22 下午，face-pilot-2）

**卡點解開了**：改在 RaceMenu 介面裡換種族、載 Hatak、按「匯出頭」，頭部件就正確了。Muiri 的換臉層已做好、檢查全過（保留原體重），**還沒裝進遊戲、還沒看過**；下一場部署後會拍圖給你看。細節：`agentctl/handoffs/home-2026-11-22/face-pilot-2/REPORT.md`。

## 試點結果（2026-11-22，你出門時 agent 跑的）

**結論：這次沒做成。Muiri 的臉沒有換，換臉層沒產出、沒部署；遊戲裡什麼都沒留下。**

- agent 開了 4 場遊戲做匯出（上限 4 場），每場都**沒存檔**。你的存檔目錄 91 個檔，前後 sha256 逐檔相同。
- 匯出這一步有跑：觸發檔放進去、遊戲吐出頭檔、收回。卡在**遊戲沒有把 Hatak 的頭部件（臉型、髮型、眉眼、疤）真的換上去**。換上去的只有膚色、戰紋、唇色、髮色；頭型、頭髮還是主角原本的。匯出的頭拿去給 Muiri 用會變成錯臉，所以 agent 停手。
- 換了三種做法、外加用全新角色試一次，結果都一樣。細節見 [REPORT](../../agentctl/handoffs/home-2026-11-22/runtime-pilot/REPORT.md)。

| 原本的 Muiri（JH NPC Beauty） | 主角套 Hatak 後（只換到妝與膚色） |
|---|---|
| ![原 Muiri](../../agentctl/handoffs/home-2026-11-22/runtime-pilot/s2/08-muiri-orig-front.jpg) | ![主角套 Hatak](../../agentctl/handoffs/home-2026-11-22/runtime-pilot/s2/06-player-hatak-front.jpg) |

（主角側面：[s2/07](../../agentctl/handoffs/home-2026-11-22/runtime-pilot/s2/07-player-hatak-side.jpg)。原 Muiri 那張是在你存檔場景裡用 `placeatme` 叫出來的暫時複本，拍完刪掉，沒存檔。）

**順帶看到**：Hatak 的眼妝、唇色、戰紋是全黑、不透明，近看很重。套到 NPC 上也會是這樣；若不是你要的，之後改 preset。

### 接下來可以怎麼走（你選）

1. **你手動一次**（約 2 分鐘）：你開遊戲時在 RaceMenu 介面載入 Hatak preset，關掉介面前喊 agent，agent 只負責按「匯出頭」並收檔。這是 RaceMenu 正常的用法，最可能成功。
2. **打通 Creation Kit**：CK 已裝，但 Linux 上沒驗過能不能出臉，要另開小專題。
3. **先不做**。

不論哪條，Muiri 的資料層（髮色、膚色、臉型滑桿）已備好；頂層裁定試點**保留 Muiri 原本體重**，產層時會加 `--keep-weight`。

## 現在已經有的（不用你做事）

- Muiri 的臉部 record patch：`~/skyrim_mods/_staging-2026-11-22-npc-face/Muiri-Look-From-Hatak-Dev-2026-11-22/`。它沿用 Muiri 現在生效的那筆資料（JH NPC Beauty），只換臉的欄位：頭部件、髮色、膚色、臉型滑桿、體重。
- 一顆測試用的小 ESP＋腳本，用來觸發「套 preset → 匯出頭」。目前放在 staging，**沒有裝進遊戲**。
- 一條指令：拿到匯出的頭檔之後，重跑就會產出可以部署的完整換臉層。

**這顆 patch 現在不能單獨裝**：只換資料、不換頭模型的話，Muiri 會變成素頭或錯臉。

## 要你授權的三件事

### 1. 開一次遊戲做匯出（約 20 分鐘，你不能同時在玩）

- **會動到**：
  - agent 取得桌面與遊戲鎖。
  - 用 AgentBridge 開 MO2＋Skyrim，載入 baseline 存檔。
  - 主角暫時被改成**女性 Breton**，戴上 Hatak 的臉。
  - 觸發匯出、截圖，然後**不存檔**直接關遊戲。
- **怎麼收回**：沒有存檔，所以存檔不受影響。關遊戲後跑 profile 稽核，最後放鎖。
- **預期看到**：一張主角戴 Hatak 臉的截圖。Papyrus log 有 `npcface` 完成訊號。`SKSE/Plugins/CharGen/` 底下多出 `npcface_export.nif` 和 `.dds`。

### 2. 暫時放三樣東西進 MO2，用完收回

- **會動到**：
  - 一個暫時的 mod 層，內含觸發 ESP、腳本 pex、`npcface_export.jslot`（Hatak 的複本）。
  - modlist 與 plugins.txt 各加一行。
  - 匯出產物會落在 `overwrite/`。
- **怎麼收回**：
  - 用 `layer_apply --revert` 逐位元組還原三個設定檔，暫時層搬回備份夾（不刪）。
  - `overwrite/` 裡本場新出的 5 個匯出檔先複製到 staging，再刪掉。`saves/` 裡的 baseline 存檔複本也一起刪。最後確認 `overwrite/` 回到原狀。
  - 完整清單見 `agentctl/tools/npc_face/trigger/README.md`。

### 3. 匯出成功後，部署 Muiri 換臉層

- **會動到**：
  - 新增 mod 層 `Muiri-Look-From-Hatak-Dev-2026-11-22`，排在 JH NPC Beauty 之上。
  - plugins.txt 尾端加一顆 ESL patch。
- **怎麼收回**：`layer_apply --revert`，或在 MO2 停用這一層。Muiri 會回到 JH 的臉。
- **預期看到**：
  - Muiri 長得像 Hatak：灰髮、刀疤、Breton 臉型。
  - 體重會變成 Hatak 的 0（原本是 100），身材會變瘦。不想要的話，跟我說「保留體重」。
  - 外觀好不好看由你判斷，agent 不會自己宣稱通過。

第 3 件可以等你看完第 1 件的截圖再決定。

## 失敗時怎麼辦：改走 Creation Kit

出現下面任一種情況，就停下來，改申請「打通 CK」小專題。CK 已經裝在本機，但在 Linux 上能不能匯出頭還沒驗過。

- 匯出後沒有任何 `.nif` 產物。
- 匯出的 NIF 結構不像 FaceGen：頭部件名稱對不上，或缺部件。
- 上架工具的檢查不過，而且用改名也修不好。

record patch 兩條路線共用，不會白做。

## 不會做的事

- 不使用 PROTEUS 的「清除 NPC 編輯」。它會刪掉硬碟上的臉部檔案，可能連已安裝的 mod 一起刪掉。
- 不存檔，不改你的其他存檔。
- 不碰其他 NPC。

## 你只要回一句

例如「1、2 可以，3 等我看圖」，或「全部可以」，或「先不要」。
