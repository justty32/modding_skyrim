skyrim 短工（helper）的卡，寫給掛短工的人看：能交給它什麼、不能交什麼、怎麼掛、怎麼收。

# 短工 `helper`

回 [org](../README.md)。

短工為一件事掛上，做完就收。它不佔座位、沒有地盤、不留筆記。它不讀這張卡：它只知道自己的 system text 和交接書。

使用者 2026-11-23：簡單工作與雜活交給 sonnet；這類工作不用先讀 `wf/` 規矩。所以短工的交接書要把該守的規矩寫進去。

## 職責

### 可以交給它

- **查事實**：搜尋、計數、讀檔、整理，每項附來源。不設計、不建議、不改看到的東西。
- **逐點核對**：拿工作跟交接書或計畫比，一項一項。只指出，不修。
- **不用判斷的機械改動**：照表改名、搬檔、套格式；交接書要寫明可寫的路徑。

### 不能交給它

- 寫程式，或任何要理解、要選擇的改動。分不清的話，就是要判斷。
- 設計、結構、決定什麼才對。
- commit、push、刪檔、問使用者、自己再掛 agent。
- 動 MO2 profile、`mods/`、遊戲鎖、遊戲、MO2、Steam。
- 改使用者規範（出處 aos.md 第 4 節：不派 sonnet）。

### 完成條件

答案檔在了，而且掛它的人已逐項對照來源核過。

## 讀寫範圍

約定，不是牆（[places](../places.md)）。

- **能讀**：交接書點名的路徑。
- **能寫**：只有自己的工作夾 `wf/temp/{短工名}/`，或交接書點名的 REPORT 路徑。只有文字這樣說；沒有東西擋它寫到別處。

## 交接

- **掛它的人**（lead 或部門主管）給一份只有一個目標的交接書：讀什麼、寫什麼、交什麼、什麼時候算完、子 agent 上限 → 拿回答案檔或最後一則回覆裡的完整答案 → 對照來源逐項核，不重跑；要留的搬進工作區由自己 commit；收掉短工。
- 掛短工的人替它的結果負責。結果不直接給使用者，也不直接給別的座位。
- 等短工的方法看種類：Claude Code 子 agent 不准用結束回合當等待，用前景迴圈等（出處：[dispatch-leads-and-line-discipline](../../lessons/dispatch-leads-and-line-discipline.md) 的 leads-must-not-end-turn-to-wait）；aos 子 agent 送出交接書後可結束回合，等 `mail_notify` 叫醒（出處：aos 知識庫 `aos/mailbox.md`）。

## 怎麼掛

兩種，先選第一種：

1. **Claude Code 自己的子 agent**（Agent 工具，型別 `line`；要寫 REPORT 時交接書寫明「REPORT 是交付物」）。不佔 aos 名額。
2. **aos 子 agent**：定義 `agentctl/aos/defs/sk-worker-sonnet`（沒有 subagent、def 包，不能 commit、不能掛 agent）。名字 `{上游名}-{角色}-{MMDD}{序}`，不重用（出處 aos.md 第 1 節）。派工用 `mailbox_send`，信裡叫它做完自己收掉（出處：[aos 樹教訓](../../lessons/aos-tree-onboarding-and-leading.md)）。

sol（agent-fsm、沒有 shell）只做蒐集與量大呆板的事，全樹同時最多 1 隻（出處 aos.md 第 4 節）。這輪不取 aos 範本的 `site.txt`，因為短工不是從 kit 做的（見 org-draft 線 REPORT）。

## 模型

- **腦**：sonnet（使用者 2026-11-23：簡單工作與雜活交給 sonnet）。
- **同時幾個**：一份交接書一隻；上限是掛它的人交接書裡寫的子 agent 上限。
- **掛不上時**：掛它的人自己做，或回 `BLOCKED`。
