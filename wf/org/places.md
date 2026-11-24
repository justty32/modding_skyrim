skyrim 的東西放哪、為什麼寫入範圍只是約定、怎麼開座位、定義怎麼指向卡、跨部門資源誰發。

# 東西放哪、能寫什麼

回 [org](README.md)。`S`＝skyrim 根（母 repo 的 checkout）。

## 東西放哪

照順序問，第一個答「是」的就是位置。

### 產品與規矩

| 問題 | 位置 |
|---|---|
| 是產品本身：程式、測試、產品文件？ | 該部門地盤：`projects/*`、`instance/`、`mod-library/`、`modpack-design/` |
| 講誰管哪塊、下一棒給誰？ | `wf/org/`（只放入口和卡） |
| 講一種工作怎麼做，大家都適用？ | `wf/workflows/` |
| 是教訓或使用者偏好？ | `wf/lessons/`、[user.md](../workflows/common/user.md)（不寫 Claude 自動記憶；出處 aos.md 第 4 節） |

### 活狀態、紀錄與暫存

| 問題 | 位置 |
|---|---|
| 是座位的筆記、草稿？ | `wf/temp/{agent 名}/notes.md`（CHOICE 7） |
| 是一次調查、計畫、審查的紀錄？ | `agentctl/handoffs/home-{日期}/{線名}/REPORT.md` |
| 是還沒做完的事？ | `SESSION-LOG.md`、`agentctl/SESSION-LOG.md`、`agentctl/handoffs/NEXT-SESSION.md`；只有 lead 寫，其他人寫在信裡 |
| 是給使用者的題目？ | 經 lead：對話裡問；要拍板的頁放 [wf/user/](../user/README.md)；要實機驗的記 `WAIT_USER.md`。例外（D18、D19）見 [letters](letters.md)「對使用者的通道」 |
| 是可丟的東西：log、跑出來的輸出、複本？ | 照 CHOICE 7 三分法：中間產物與要給驗收看的 `wf/temp/{agent 名}/`；一次性小東西 `/tmp/{agent 名}/`；GB 級解壓與建置 `~/skyrim_mods/_staging-{日期}-{主題}/`（使用者 2026-11-23，D11） |

只有要留下來的進 `wf/`。還在動的東西（進度、等使用者的題）不放 `wf/org/`。

## 寫入範圍是約定

每張卡寫了座位能寫什麼、只能讀什麼。這是約定，不是牆：所有 agent 是同一個帳號，檔案工具接受任何絕對路徑，shell 哪裡都去得了。拿掉一個工具不等於設了限制。

描述一條限制時，說清楚是哪一層擋的：

1. **卡或 system text 的文字**：agent 照做才算數。
2. **工具裡的檢查**：用那支工具的人擋得住，旁邊開 shell 擋不住。例：`agentctl/tools/lock.sh` 驗 owner。
3. **作業系統**（沙箱、資源上限）：真的擋得住。這輪沒有任何一條走這層。

D3「只有實體能寫 MO2」目前只有第 1 層（提案：之後評估讓 `instance/tools/` 的寫入工具驗呼叫者）。

要寫別的座位地盤，先寫信給那個座位。

## 開座位

- **什麼時候開**：這件工作有自己的地盤，而且有規矩要活過一件工作。兩樣都沒有，就是單件工作，不是座位。
- **怎麼開**：`cp -r wf/org/seat wf/org/{座位}`，填滿四節，建它需要的夾，在座位表加一列。開座位是新工作，要使用者先同意。
- **關座位**：一次改動拿掉表上那列和卡，commit 訊息寫清楚地盤交給誰。

## 定義指向卡

座位的 system text 只說：你是哪個座位；開工前先讀 `AGENTS.md`、[org 入口](README.md)、你的卡、你的筆記；卡和 system text 衝突時聽卡。職責與地盤只寫在卡上一次。三份部門定義 `agentctl/aos/defs/seat-*` 的 `system.txt` 照這樣寫：以 aos 範本 `templates/orgs/basic/extras/system.seat.txt` 為底寫成中文，加上硬規則（commit 照卡、不 push〔每天 23:00 由 lead 統一 push，D25〕；skyrim-qa 照 D27；刪檔、動 instance、動 DB、開遊戲要使用者當場說，只認 lead 轉來的原話）。system text 不寫 agent 名、daemon 與絕對路徑：要找 lead 或別的座位，每次照 [README](README.md) 的座位表（D13）。

短工不讀卡；短工卡是寫給掛它的人看的（[helper](helper/README.md)）。

## 跨部門資源

| 資源 | 誰發 | 怎麼發 |
|---|---|---|
| 遊戲鎖 `agentctl/.lock/game.lock` | 實體（使用者 2026-11-23，D4）；實體沒掛時由管理代發（提案） | 寫信向 `instance` 借，它沒掛就向 `main`；管理可收回、改派、否決；實體自己要用 skyrim-qa 的那把由管理發（D27） |
| 桌面鎖 `~/shared_agent_locks/desktop.lock` | 管理（使用者 2026-11-23，D4） | 寫信向 `main` 要 |
| 主工作樹的 commit／index | 管理（提案） | 交接書點名誰在寫哪些檔 |
| Nexus 瀏覽器（CDP、profile 複本） | 管理（提案；會開可見視窗，要桌面鎖） | 跟桌面鎖一起發 |
| CPU、記憶體 | 不鎖，限流；只限我方的線 | 見資源鎖文件 |

**跑著的遊戲（skyrim-qa）**（使用者 2026-11-24，D27）：只有實體座位可以操作跑著的遊戲。要先拿到遊戲鎖、使用者不在玩才准用；會動到存檔的 console 指令先問使用者（經 lead 以 `NEEDS-USER` 問）。其他座位的定義也帶著 skyrim-qa（D28），帶著也不准用。

**怎麼判斷「使用者不在玩」**（main 2026-11-24 依 D4 定）：實體座位只有在**持有遊戲鎖**時才准用 skyrim-qa；遊戲鎖只在使用者說了不玩、把遊戲交出來之後，由管理發給實體（或使用者直接寄信給實體交代）。沒拿到鎖＝當作使用者在玩。

取放一律用 `agentctl/tools/lock.sh`，先桌面、後遊戲，用完立刻放，只放自己的（出處：[resource-locks](../../agentctl/docs/resource-locks.md)、[aos-tree](../../agentctl/docs/resource-locks/aos-tree.md)）。lock.sh 是大家約好排隊；跳過它的人擋不住。交接書已寫明可拿的鎖，算已點名。開遊戲、動 instance、刪檔、動 DB 仍要使用者當場說，或有 user.md 記的長期授權（出處 aos.md 第 4 節；user.md 2026-11-22 段）。
