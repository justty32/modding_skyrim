# 調度、模型分級與交接書（8/9）

[lessons 索引](README.md)｜同主題：[dispatch-and-agents](dispatch-and-agents.md)、[dispatch-and-agents-2](dispatch-and-agents-2.md)、[dispatch-and-agents-3](dispatch-and-agents-3.md)、[dispatch-and-agents-4](dispatch-and-agents-4.md)、[dispatch-and-agents-5](dispatch-and-agents-5.md)、[dispatch-and-agents-6](dispatch-and-agents-6.md)、[dispatch-and-agents-7](dispatch-and-agents-7.md)、[dispatch-and-agents-9](dispatch-and-agents-9.md)

## codex-tmux-operational-notes

> 用 tmux 驅動 codex CLI 的實務細節——送出鍵要分開送、trust prompt、gpt-sol 的行為特性與該寫死的護欄（原 type: feedback）

2026-08-20 夜間一次開三條 codex 線（gpt-5.6-sol）跑 Skyrim modding 工作，累積的操作細節。

**送指令要分兩次呼叫**：`tmux send-keys -t <s> -l '<文字>'` 之後的 `C-m`／`Enter` 如果**寫在同一個
Bash 呼叫裡**，codex TUI 常常只把文字放進 composer 而不送出（pane 上看到 `» <你的文字>` 就是還沒送）。
要另外發一個 `tmux send-keys -t <s> C-m` 才會真的送出。每次送完務必 capture 確認開頭變成 `›` 且出現
`Working (`。

**啟動時會先問 trust**：`codex` 在新目錄第一次啟動會停在「Do you trust the contents of this
directory?」，要送一個 Enter 才會進主畫面。`capture-pane -p -S -30` 在 alt-screen 下抓不到東西，
**不要加 `-S`**。

**偵測 idle**：pane 裡有 `Working (` 就是忙碌，消失即該輪結束。用 Monitor 做 busy→idle 邊緣觸發
通知，比自己輪詢省很多 token。

**gpt-sol 的行為特性**（使用者親口提醒 + 實測）：
- 會為了「更保險」跑一大堆與正事無關的驗證測試。**交接書要寫死「驗收就是這四條，一條不多，
  做完就停」**，實測有效。
- subagent 使用者的界線是：**為了推進正事可以開，為了驗證／複查／風險掃描這種周邊小事不准開**。
  判準寫成「那個 subagent 的產出如果不在驗收清單裡，就不該開它」。
- 護欄遵守度高：叫它「遇到工具錯誤就停下回報」它真的會停——但它把**自己寫錯的 Python 引號**
  也算成工具錯誤而停工。交接書要區分「工具/環境錯誤 → 停」與「你自己的臨時腳本寫錯 → 自己修」。
- 給精確的預期數字（檔案數、bytes、tree SHA）它會照著對，不會含糊帶過。

**多線分工**：一條 MO2 live tree + profiles git、一條 submodule 原始碼、一條唯讀盤點寫 notes。
同一個 git repo 有兩條線要 commit 時，交接書要寫「只准 `git add <明確路徑>`，禁止 `git add -A`，
遇到 `.git/index.lock` 等幾秒重試、絕不刪 lock」。

**遊戲是獨佔資源**：MO2／Skyrim 同時只能一條線持有，而且**不能在另一條線正在搬 `overwrite/`
檔案時啟動**（遊戲會寫入 overwrite）。排程要自己當鎖來管。

**改 `~/.codex/config.toml` 會殺掉所有正在跑的 codex session**（2026-08-20 實測）：22:57:39 用
`sed -i` 改了一行 `HouseCarl__ProfileDir`，22:59:09–10 四個 `tmux-spawn-*.scope` 在同一秒內全部結束，
四條 codex 線同時死光，在途工作（未落檔的交接書、未寫出的腳本）全部丟失；只有已經 commit 的存活。
codex 顯然會監看設定檔並在變更時退出。**要改 codex 設定就先讓所有 session 收工，或接受重開的代價。**
排查時 `journalctl --user | grep 'tmux-spawn.*scope'` 會列出每個 scope 的 wall clock，能用起始時間反推
是哪幾條線。

**houseCARL 在本機的已知壞法**：`Mo2InstanceDir` 模式不可用（MO2 的 `gamePath` 是 Wine 路徑
`Z:\home\...`，houseCARL 不做映射，會推出不存在的 `Z:\home\...\Data`）；正解是 explicit paths
`HouseCarl__DataDir` / `ModsDir` / `ProfileDir`。2026-08-20 單 profile 遷移後，`~/.codex/config.toml`
與 `~/.claude.json` 兩邊的 `ProfileDir` 都還指著已退役的 `profiles/Default`，導致每個 houseCARL 查詢
都回 "No active plugins resolved"。已改成 `profiles/Modpack-KR`（兩邊都有 `.bak-20260820` 備份）。

**任務結束就關掉 session,不要留著等下一批**(2026-08-21 量測後訂的規矩)。每個閒置的 codex
session 持有一個 houseCARL MCP 實例,**實測平均 249 MB**。昨夜開六條線、任務結束後只確認成果
有沒有推上去卻沒收拾 session,結果 codex-b/codex-f 從凌晨閒置到早上;連同其他閒置線共佔
**2,237 MB**,關掉後降到 475 MB,**釋出約 1.8 GB**。

要用時重開只要 30 秒,而交接書都寫在磁碟上(`~/skyrim_agent_out/<線名>/`),不依賴 session 記憶——
這正是把成果寫成報告與交接書的意義。

**附帶教訓**:我一度用「影響接近零」把 MCP 實例洩漏帶過去,那是**沒量就下的結論**。
使用者說過「不要操我的電腦」,這種事該量了再說。

相關：[[driving-other-cli-agents]]、[[delegate-simple-work-to-sonnet]]

**2026-08-30 使用者心得——指揮 gpt-sol 要經常提醒它專注**：「要他專注在真正重要的事情上，無關緊要的小事先別管」，否則它會一直寫測試一直驗證。這是動態手段，跟交接書「寫死驗收條數」（靜態）並列：交接書擋不住的過程漂移，靠 orders／tmux 中途提醒拉回來。各模型有各自的指揮方式，已進 agentctl/docs/team-model/speed-and-driving.md 的逐模型指揮心得表（2026-08-30）。

**2026-09-08 模型別名壞了**：`codex -m gpt-sol` 現在回 `The 'gpt-sol' model is not supported when using Codex with a ChatGPT account`；config 裡的真名是 `gpt-5.6-sol`，直接跑 `codex` 用預設模型即可。交接書寫「gpt-sol」沒問題（是我們的暱稱），但啟動指令別帶 `-m gpt-sol`。另：`housecarl_bsa_list`（BSArch 走 wine）在這台機器讀 BSA 會 `wineserver: bind: Operation not permitted`，髮型「缺檔」判定要改用 python 直接掃 BSA 位元組，否則會假警報。

**2026-09-20 補**：`codex` 預設模型實際是 `gpt-6-astra medium`（不是 gpt-sol），要 gpt-sol 得另外確認別名；
`inbox_send.sh` **沒有 `--body-file` 旗標**，正文檔是第 4 個位置參數，寫成旗標會靜默從 stdin 卡住（lead-fde920 抓到）。
交接書「只看 plugins.txt 帶 `*`」會漏掉隱含載入的 CC 與原版 master（1266 支＝1207 勾選＋59 隱含）。

**2026-09-25 orders 檔不是即時剎車**：cx-wu-kern 在我把「不降版、還原」的 order 追加到 `inbox/orders/cx-wu-kern.md` 三分鐘後照樣 commit 了降版（它只在「每完成一步」才讀 order，最後一步 commit 前沒再讀）。要即時攔一條 codex 線，用 `tmux send-keys -t <線> Escape` 中斷再送新指令＋兩次 Enter，或直接 kill session；order 檔只適合「下一步前要看」的補充指示。事後靠三個 repo 都沒 push，用 `reset --soft HEAD~1`＋`restore --staged --worktree -- wf AGENTS.md`＋刪新檔還原。
