# racemenu／loop — 看結果：離線預覽、遊戲內確認、使用者選定

[racemenu](README.md)｜[WORKFLOWS](../../WORKFLOWS.md)

段 3–5。**段 3、4 目前都未實作、未實機**。本檔先寫定介面與邊界，讓下一階段的施工線照著做；工具做好、實機跑過之後再改寫成操作步驟。工具清單、相依與授權在 [racemenu-face 計畫](../plans/racemenu-face/README.md)。

三種迴路的分工（依據：調查 REPORT §6b）：

| 迴路 | 看得到什麼 | 每輪成本 | 定位 |
|---|---|---|---|
| ③ 純數值（[author](author.md)） | 只有數值 | 秒級 | 產生候選、插值 |
| ② 離線出圖（段 3） | 形狀、比例；膚色、妝、髮型和遊戲有落差 | 約 1 秒（推論） | agent 自己先篩 |
| ① 遊戲內截圖（段 4） | 真實畫面 | 冷啟動 3–6 分鐘，之後每輪 10–30 秒（推論） | 最後 1–3 份給使用者看 |

## 3. 離線預覽

**未實作**。要做的事：

1. 讀 head chargen／races tri（FRTRI003）。
2. 把 jslot 的 NAM9 和 presets 套成頂點位移。
3. 渲染正面、側面兩張圖。

渲染器有兩條候選路線：

- 自寫 numpy 光柵器（計畫 R2）。
- 拆用 Skyrim Universal Viewer 的 NIF 渲染器（規劃表裡的「離線出圖原型」；動工要使用者授權 pip 安裝 PyQt6，並同意執行它的程式碼）。

SUV **不解析 `.tri` morph**，所以不管走哪條，套 morph 的程式都得自己寫。

Done when（將來）：每份候選都有 `front.png`、`side.png`；和基底並排的差異圖只在預期部位有變化。

## 4. 遊戲內確認

**部分實機（2026-11-22 runtime-pilot）**：截圖取景已跑通；但 Papyrus 套 preset 不換頭部件，畫面只能確認 tint、髮色、體重，看不到換部件後的真臉（[lessons](../../lessons/faces-racemenu-runtime.md#racemenu-export-head-parts-not-applied)）。依 [runtime-qa](../runtime-qa/README.md)：

1. 用 `envsnap` 確認遊戲和 MO2 都沒在跑，並確認使用者沒在玩連線遊戲。
2. 先取 desktop 鎖，再取 game 鎖（`agentctl/tools/lock.sh`）。
3. 用 `qa_runner` 以 background-active 載入 baseline 存檔。
4. 把候選 jslot 暫時放進 VFS 的 `SKSE/Plugins/CharGen/Presets/`（**動 instance，要當場授權**）。
5. 用 AgentBridge `/console` 呼叫 `CharGen.LoadPreset`（主角）或 `CharGen.LoadCharacterPreset(actor, …)`（NPC）。主控台能不能直接呼叫這些 Global 函式未實機，後備是 ConsoleUtilSSE NG。
6. 存圖用 `spectacle -b -n -f -o`。對臉取景（已實機）：主角在第一人稱看不到自己，先 `tfc` 凍住相機，`player.setpos` 把主角放到相機前 70–90 單位、`setangle z` 轉 180°，`fov 45`、`tm` 關 HUD；側面再轉 90°。拍 NPC 用 `placeatme` 複本＋`/console` 的 `ref` 欄位做同樣的事，`tai` 定住 AI。腳本在 `agentctl/handoffs/home-2026-11-22/runtime-pilot/tools/`。
7. **不存檔**。關遊戲，收回暫存的 jslot，跑 profile 稽核，依反序放鎖。

禁區：

- 不用 `/input` 操作 RaceMenu 介面。
- 不存檔。
- 使用者在玩連線遊戲時不開。

Done when（將來）：每份候選有一張遊戲內截圖；`instance/` 沒有殘留的 jslot；profile 稽核綠燈；兩個鎖目錄都是空的。

## 5. 使用者選定

美醜由使用者判定（runtime-qa：要人眼判斷畫面的是使用者的事）。

- 挑選頁沿用 `wf/user/` 的模式（同 2026-10-26 隨從外觀頁）：每份候選一格，放圖和 author 的回報表那一列。
- 使用者回覆選定前，記一行在 [WAIT_USER](../../../WAIT_USER.md)。

Done when：使用者回覆了選哪一份（或要求再調一輪，回到 [author](author.md#2-合成文字需求滑桿)）。
