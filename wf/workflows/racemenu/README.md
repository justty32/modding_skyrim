# racemenu — 捏臉：RaceMenu preset 的合成、確認與固化

[WORKFLOWS](../../WORKFLOWS.md)｜[INDEX](../../INDEX.md)

讓 agent 依文字需求調整 RaceMenu preset（`.jslot`），先看結果，再交付。**臉的最終產物是 NPC 的 patch 層**（ESP 裡的 NPC_ 臉部欄位，加上 FaceGen 頭 NIF 與 tint），不能只停在存檔或 JCUser 裡。主角的臉則收成 preset 層。

**何時用**：「幫我捏臉」「改某 NPC 的臉」「臉再瘦一點／眼睛大一點」「把這個 preset 套到 X」「把我主角的臉給 X」「RaceMenu 出問題」。
**何時不用**：
- 把 NPC A 的整張臉換給 NPC B → [look-swap runbook](../../../agentctl/docs/look-swap-runbook.md)（`look_transplant`），不必繞 jslot。
- 身形，包括胸、腰、臀、BodySlide preset、OBody 指派、`.tri` → [bodyslide](../bodyslide/README.md)；逐 NPC 指定身形走 [換身體](../bodyslide/body-swap.md)。
- 裝或下載 RaceMenu 附屬件 → [nexus-intake](../nexus-intake/README.md)、[profile-change](../profile-change/README.md)。

## 現況：哪些段已可用

| 段 | 檔 | 內容 | 狀態 |
|---|---|---|---|
| 1 需求凍結 | [author.md](author.md#1-需求凍結) | 目標 actor、基底 preset、要改的特徵 | **可用**（純文件流程） |
| 2 合成 | [author.md](author.md#2-合成文字需求滑桿) | 文字需求→滑桿；用 `jslot` 工具產生候選、lint、diff | **可用**（離線、純數值，看不到圖） |
| 3 離線預覽 | [loop.md](loop.md#3-離線預覽) | 正面、側面幾何圖 | **未實作** |
| 4 遊戲內確認 | [loop.md](loop.md#4-遊戲內確認) | 套 preset＋AgentBridge 截圖 | **未實作、未實機** |
| 5 使用者選定 | [loop.md](loop.md#5-使用者選定) | 挑選頁 | 沿用既有 `wf/user/` 頁面模式 |
| 6 固化 | [bake.md](bake.md) | preset→NPC patch 層 | record／上架／組層**可用**；匯出頭**未實機** |
| 7 部署驗收 | [bake.md](bake.md#7-部署與驗收) | `layer_apply`＋實機看臉 | manifest 自動產出；**未實機**，試點待授權 |

下一階段工具與授權清單見計畫 [racemenu-face](../plans/racemenu-face/README.md)。

## Done when

依本輪走到哪段而定，開工時寫明：

- 段 1–2：每份候選 `.jslot` 都存在於本輪工作目錄，`python3 agentctl/tools/jslot/cli.py lint <檔>` exit 0，對基底的 `diff` 只出現本輪宣告要改的欄位；回報表依 [author.md](author.md#4-回報格式) 填滿。
- 段 3 之後：各段 Done when 寫在該段，那幾段目前都還不能宣稱完成。

## 授權邊界

| 動作 | 需要 |
|---|---|
| 讀 jslot、離線產生候選、寫進 `wf/temp/<線>/` 或任務證據夾 | 不用問 |
| 開遊戲、取 desktop／game 鎖 | 使用者當場授權（[runtime-qa](../runtime-qa/README.md)）；使用者在玩不能暫停的連線遊戲時禁止 |
| 把 jslot 放進 VFS 的 `CharGen/Presets/`、或刪掉它 | 算動 `instance/`，要當場授權 |
| 在遊戲裡對 baseline 存檔開 `showracemenu`、`ExportHead` | 同上；**不存檔** |
| 暫放匯出觸發 ESP／pex（`npc_face/trigger/`）並在事後收回 | 同上；清單見 trigger README |
| 安裝 Python 套件（離線出圖） | 要問 |
| 部署 patch 層 | profile-change 授權流程 |

## 已知限制

- **主角是男性 Imperial、原版男體**：可以捏臉，捏身形目前做不到（男體方案由 `male-body-survey` 調查）。
- 私人 preset `Hatak`、`Prisoner` 都是**女性**臉，套到男主角時 tint 與頭型會錯位，只能當數值參考。
- **NPC 臉固化缺一場實機匯出**（`ExportHead` 從沒產出過）；CK 已裝（Steam 1946180）但 Proton 下未驗證，列備援 D1；PROTEUS「清除 NPC 編輯」禁用。見 [bake](bake.md#禁區)。
- 身體滑桿 plugin `RaceMenuMorphsCBBE` 未裝，要裝用 3BA 30174 v2.48 包那份（CBBE 1.8.1 包那份缺 40 個滑桿）；屬身形，歸 bodyslide。
- OBody 預設先清空 actor 的所有 morph 再套 preset，和 RaceMenu 的身體 morph 是**後寫者贏**；臉部欄位不受影響。
- 臉部滑桿正負方向未實機校準（[author §3](author.md#3-方向還沒校準)）；自訂種族部分滑桿無效、也不讀預烤 facegen。

## 交接

- 段 2 的成品（候選 jslot、diff、回報表）放任務證據夾 `agentctl/handoffs/<場>/<線>/`。
- 要人眼判斷美醜的，記到 [WAIT_USER](../../../WAIT_USER.md)，不可自行宣稱通過。
- 依據：調查 REPORT `agentctl/handoffs/home-2026-11-22/racemenu-survey/REPORT.md`（§6）。
