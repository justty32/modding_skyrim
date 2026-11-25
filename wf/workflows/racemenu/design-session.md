# racemenu／design-session — 捏人試驗場：設計線、支援組織、實體代拍、離線工具

[racemenu](README.md)｜[WORKFLOWS](../../WORKFLOWS.md)

使用者說「派一條線試試看捏 X」（臉、髮、身形，再往後是衣裝）時，頂層怎麼在一晚內組起設計線、支援線、實體座位與 fsm gpt 工人，借遊戲、還遊戲。單份 preset 怎麼做仍照 [author](author.md)、[loop](loop.md)、[bake](bake.md)；本檔只管組織與時間。試點是 2026-11-25 的 Chloe 版初音（[REPORT](../../../agentctl/handoffs/home-2026-11-25/miku-face/REPORT.md)）。

**何時用**：要強模型自己探索造型、途中會冒出工具需求、可能借遊戲拍圖。
**何時不用**：已有 jslot 只改幾個滑桿 → [author](author.md)；把 NPC A 的臉整張搬給 B → [look-swap runbook](../../../agentctl/docs/look-swap-runbook.md)；只做身形 → [bodyslide](../bodyslide/README.md)。

## Done when

寫進設計線 BRIEF 的驗收：REPORT 第一段白話寫像不像、卡在哪；入選 preset 與實拍或離線圖都在線夾；借過遊戲的話，下面收場清單逐項有證據；本場若冒出新的人工步驟，末段資料檔補一列。

## 角色

| 角色 | 誰 | 只做 | 不做 |
|---|---|---|---|
| 頂層 | `main` | 對使用者、轉介、放行、定死線、收場複查 | 實作、代判美醜 |
| 設計線 | 強模型，可開子 agent（試點是使用者點名的 codex astra ultra，D20 的例外） | 設計、判圖、寫請求 | 碰遊戲、MO2、profile |
| 支援線 | Claude Opus | 做工具、做測試補丁（只放 staging） | 安裝、開遊戲 |
| 實體座位 | `instance`，唯一碰遊戲（D27），持 game.lock | 裝拆補丁、代拍、F5 匯出、只描述所見 | 推論 mesh 成因 |
| fsm gpt 工人 | sol／astra | 互不相干的旁支：調查、文件、圖鑑、黃金證據 | 設計決策 |

## 開工十分鐘內

1. **三問一次問完**：① 今晚能不能借遊戲拍圖，使用者幾點離開、幾點回來（他要用鍵鼠時就不能拍）；② 自訂種族要不要做臨時測試補丁（只在測試時裝，收工拆）；③ 身形捏不捏。
2. 照範本寫 [設計線 BRIEF](../../../agentctl/templates/BRIEF-design.md) 與 [支援線 BRIEF](../../../agentctl/templates/BRIEF-support.md)，`brief_lint --strict` 過了才派。
3. **可預見的前置同時開工，別等設計線開口**：測試種族補丁、NPC→jslot 基底、看圖工具選種族、離線出圖。試點的 S1–S3 與設計線同時起跑，省掉一輪往返。
4. 每份 BRIEF 都寫上「其他線並行改動是正常的，不用停下來問」，以及「成品圖要搬進線夾」。

## 時間線範本

| 時刻 | 事 | 試點 |
|---|---|---|
| T0 | 使用者開口，頂層問三題 | 19:0x |
| T0＋10 分 | 設計線、支援線同時開工 | 19:0x |
| 前置就緒 | 測試補丁交實體裝 | 19:13 |
| 窗口開 | 第一個 `shoot` | 19:15 |
| 換補丁最後時刻 | 收場前約 15 分 | 定 20:05，19:40 換了 v2 |
| 收場 | 使用者回來前 10 分 | 定 20:20，19:50 還場 |
| 額度重置後 | 收尾、交 REPORT | 21:00 重置，21:30 收尾，21:50 交 |

## 請求協定

- 設計線寫線夾 `REQUESTS.md`，每則一個標題 `## R<n> <HH:MM> shoot|tool|question`。`shoot` 附清單檔絕對路徑、mode、種族、角度、輸出位置；清單裡每份先 lint。
- 回覆寫 `REPLIES*.md`、同編號。**一開始就每個主筆一個回覆檔**（`REPLIES-main.md`、`REPLIES-instance.md`、支援線一份）；共寫一份很快破 8 KB，還會被別人的 commit 連帶收進去。
- 第一個 `shoot` 由頂層轉介，之後實體直接盯 `REQUESTS.md`。替代清單要寫明「還沒開拍才替換，已開拍就照原清單收完」。
- 中途改需求：寫 `ADDENDUM-N.md`（[範本](../../../agentctl/templates/ADDENDUM.md)），再用 tmux 對設計線說一句。用 Agent 工具開的子 agent 線跑起來後收不到訊息，要中間成果就事先約定 commit 標題含 `… ready`，頂層盯 `git log`。

## 借遊戲的窗口

使用者交出遊戲時，頂層當場定兩條死線並寫進回覆檔：**換補丁的最後時刻**，以及**收場時刻**（比使用者回來早 10 分鐘）。實體收場清單，逐項留證據：

1. 看圖工具 stop，存檔與 INI 比對通過。
2. 關遊戲、關 MO2。
3. revert 測試層；MO2 回寫造成差異時先比正規化 diff（[lesson](../../lessons/mo2-profiles.md#mo2-revert-check-normalized-diff)）。
4. profile 四檔回到裝前 sha256，mods 夾沒有測試層，check_masters 的 `present=no` 為 0。
5. overwrite 裡遊戲寫的 `CharGen/Head_*` 匯出搬到暫存，不留在 overwrite。
6. 放鎖：先放 game、再放 desktop。

頂層到點自己用 `qa_status` 與 `git status` 再查一次，不只看回報。

## 閘門

批次拍照前，先載一份基準、在 Sculpt 頁按 F5 匯出真頭，核 shape 名與頂點數。試點靠 996 對 3832 抓到頭根本沒換成。`getisrace` 只證明種族、不證明頭；「髮色變了」「lint 過」也都不算（[lesson](../../lessons/faces-racemenu-runtime.md#racemenu-export-head-parts-not-applied)）。

## 離線優先與額度

- 設計線先用 `head_render` 離線出圖篩候選，遊戲只做最後確認。滑鼠歸使用者時 face_loop 不能用。
- GPT 週額度有重置時刻。重置前讓 fsm gpt 工人一直有活（kernel 同時 2 個 slot，sol 全樹最多 1 隻），設計線子 agent 上限放寬；重置後就收。

## 交付物

設計線：REPORT（第一段白話）、入選 1–3 份 preset、實拍與 F5 頭。支援線：工具與測試、INSTALL（layer_apply manifest 與還原）。實體：回覆檔裡的收場證據。頂層：STATE 一段、教訓收進 lessons。

## 常見坑

- 寫時刻前先 `date`；試點把 19 點寫成 20 點，事後發更正（[lesson](../../lessons/user-preferences.md#check-clock-dont-estimate-time)）。
- zsh 的 `set -- $var` 不拆字，結果掛出名字含空白的工人；用陣列或 `${=var}`。
- 子 agent 看到別線改了工作樹會停下來問，所以 BRIEF 要先寫明那是正常的。
- 圖片被 `.gitignore` 擋（[handoffs 版控政策](../../../agentctl/handoffs/README.md#什麼能進版控)），只能留在本機；`/tmp` 重開機就清，BRIEF 要寫明搬進線夾。
- 臉的領域坑：[自訂種族可選與部件可選](../../lessons/faces-racemenu-runtime.md#custom-race-playable-and-valid-headparts)、[眼雕要配對的頭](../../lessons/faces-racemenu-runtime.md#eye-sculpt-requires-matching-head)、[FaceGen 不能由記錄還原](../../lessons/faces-facegen-consistency.md#facegen-not-recoverable-from-npc-record-alone)、[WornArmor 也是外觀](../../lessons/faces-troubleshooting.md#npc-wornarmor-is-part-of-appearance)。

## 已工具化／仍人工

逐步對照（22 列：狀態、工具、缺口、值不值得做成程序、優先序、依據）已抽到 [design-session-steps.json](design-session-steps.json)。各類程序候選的總表見 [PROCEDURE-CANDIDATES](../../../agentctl/handoffs/home-2026-11-24/PROCEDURE-CANDIDATES.md)（本場是追加的第 8–11 類）。統計：已工具化 6、半工具化 10、仍人工 6。給工具線的優先序：

- **P0**：收場複查腳本（第 13 列）、F5 真頭閘門 CLI（第 12 列）。
- **P1**：測試種族補丁產生器、臨時測試層租約、無滑鼠代拍實機試驗、jslot 直接離線出圖。
- **P2**：挑基底圖鑑、請求協定 CLI、滑桿校準寫回、髮型變形、成品搬檔。
- **P3** 與「不值得」：其餘，理由寫在資料檔。
