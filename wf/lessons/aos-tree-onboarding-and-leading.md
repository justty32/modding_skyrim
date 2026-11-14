# aos 樹：接入與帶隊

skyrim 隊 2026-11-14 第一次在 aos 樹裡跑（13:00 開工，14:45 收工）。這裡收下一場照著做會更順的事。規矩本身在 [wf/workflows/aos.md](../workflows/aos.md)，這裡只寫經驗、毛病和繞法。`S`＝skyrim 根。

## aos-tree-pace-gather-then-design

> 蒐集並行、設計快速、先做不會後悔的：第一場 1 小時 45 分走完第 0～2 期

- 事實：流程是這樣跑的。
  - 蒐集：4 隻 sol 加 3 隻 Claude 子 agent，約 30 分。
  - 接著 opus 匯總，fable 出設計，約 5 分。
  - 再來 Argon 審查、opus 細化成計劃。
  - 最後實作第 0～2 期。
- 使用者專區的 4 封 decide 信，他都在幾分鐘內回了，verify 都過。
- 「先做不會後悔的」（鋪 index）跟設計審查同時跑，沒有白做。
- How to apply：沒有爭議的鋪底工作不要等設計定案；要使用者裁的題，集中寫成一封專區信（≤ 7 題）。

## aos-letters-cross-say-as-of

> 信會交錯：每封信寫清楚「截至哪個 commit／哪封信」

- 事實：第一場至少 5 次，對方的 DONE 跟上游的新指示在路上互相越過。
  - 例子：收工那封 pin 指示是在 opus-1 寄 DONE 之前發出的。
- How to apply：
  - 回報開頭寫「截至 commit X／回 letter Y」。
  - 收到新指示時，先對照自己已經做到哪，沒做的才做，不要重做。

## aos-gate-busy-kernelfailed

> 帶 AOS_KERNEL 的工具在 gate 主人忙時回 KernelFailed：等十幾秒重試，頂層縮短回合

- 事實：gate 站掛在主人的 on_clock 上，主人在回合中時站不跑。
  - 下屬的 `mailbox_read`、`self_state` 會在 3 秒後逾時，回 `KernelFailed`。
  - agentctl 主導一場累計 12 次。
  - stock hold 連唯讀查詢也會攔。
- 繞法：
  - 頂層用 `S/agentctl/aos/gate/gate_hold.py` 讓唯讀請求自動過，並刻意把自己的回合縮短。
  - 下屬遇到逾時，等十幾秒重試。
- 出處：`S/agentctl/handoffs/home-2026-11-14/STATE.md`「已知毛病」。

## aos-subagent-forgets-worker

> subagent 工具會把活著的工人從名單忘掉：派工改走 mailbox_send，工人做完自己 self_ctl rm

- 事實：`subagent add` 之後馬上 `ask`，回 `SubagentMissing`，工人還被從名單刪掉，但它其實還活著（第一場 2 次）。
  - 對剛回完信的 eca 下 `subagent stop`，會回 `SessionBad busy answering`，要隔幾分鐘才能 rm。
- 繞法：
  - 派工用 `mailbox_send`，信裡叫工人做完自己 `self_ctl rm`。
  - 工人名字不重用（`…-sonnet-1114a/b/c`）。
- aos 那邊說換樹後會修第一件。

## aos-def-hard-rules-allow-letter-override

> 定義的硬規則別寫死「never commit」：寫「除非來信點名授權」

- 事實：opus-lead 定義的 system text 寫了 never commit。上游信授權 commit 後，隊長還是不敢做，要上游再回一封明講「這封覆蓋定義」。
- How to apply：
  - 寫定義時，commit、push 這類動作寫成「除非來信點名授權（點名檔、點名 repo）」。
  - 刪檔、開遊戲仍然寫死「要使用者在對話裡當場說」。

## aos-eca-tools-read-and-report

> eca 在 dontAsk 下 Read 讀不到工作區外、Claude 子 agent 不准寫 REPORT：定義放行 Read/Glob/Grep，REPORT 由主導代存

- 事實：
  - 必讀清單全在工作區外，eca 的 Read 被拒，只能用 Bash cat 讀。Edit 也因為「沒 Read 過」而失敗，只好用 python 改字。
  - agentctl 在四份 eca 定義的 cli.json 放行 Read／Glob／Grep 後就好了（agentctl `d98eb1b6`）。
  - Agent 工具起的 Claude 子 agent 不能寫 REPORT.md，由主導原樣代存，再加一節「主導的審」。
- How to apply：新定義直接從 `S/agentctl/aos/defs/` 複製，不要從 stock 範本起。

## aos-auto-memory-off-in-defs

> ws 在 S 底下的 eca 會讀寫 Claude 自動記憶：定義的 cli.json 帶 autoMemoryEnabled=false

- 事實：
  - 記憶夾按 `git rev-parse --show-toplevel` 算。ws 在 submodule 根的，用那個 submodule 自己的一份；ws 在 `S/tmp/…` 的，共用 S 的主記憶，也可能寫進去。
  - cli.json 帶 `"settings": {"autoMemoryEnabled": false}` 後，aos 會把它併進 `--settings`。已離線驗過，也在活 agent 上驗過。
- How to apply：教訓寫進本目錄，偏好寫進 `wf/workflows/common/user.md`，不寫自動記憶。

## aos-set-def-not-rm-add

> 換一隻 agent 的定義用 aos-agent ctl set-def，stack 和對話都留著

- 事實：
  - `set-def NAME DEF` 只換定義，history、queue、mailbox 不動。
  - 不帶 `--restart` 的話，下次 start 才生效；agent 可以自己設給自己。
  - 用 `--envs` 加進來的 agent 不能 set-def。
- 出處：`S/tmp/aos-skyrim-agent/p1/swap-runbook.md`。

## aos-sol-gather-limits

> sol（agent-fsm）起步慢、沒有 shell：盤點只到兩層，配給包五分鐘掛四隻

- 事實：
  - sol 要排腦的槽，所以起步慢。
  - `defs/gather` 沒有 shell，glob 兩層就碰到 20000 筆掃描上限，盤點只到兩層。
  - kits/gather 配給包好用。
- How to apply：
  - 全樹同時最多 1 隻 sol。
  - 要深入的盤點，改派有 Bash 的 sonnet。
  - 問使用者的題目交給 eca 寄（fsm 沒有 `user_send`）。

## aos-copy-template-def-fix-readme

> 從 stock 範本複製定義會帶來斷連結的 README：複製後重寫 README，再跑 agent_def check

- 事實：五份定義照抄範本 README，相對連結斷了 76 條。
- How to apply：複製後把 README 縮成幾行、不帶相對連結。`agent_def check` 要回 `problems: []`。

## aos-lock-not-for-live-resources

> aos-lock 只給租約、不判死活：遊戲／桌面鎖照舊用 lock.sh，經 skyrim-agent 點名

- 事實：
  - 持有人消失、租約一到期，B 就拿到鎖，但 A 名下的行程還在跑。
  - 同一個 WS 的別人也能 release。
  - aos-lock 不經 gate。
- 出處：`S/agentctl/handoffs/home-2026-11-14/lock-exp/REPORT.md`，以及 `S/agentctl/docs/resource-locks/aos-tree.md`。

## aos-wrap-pin-and-push-checks

> 收工 pin 與 push 前檢查：wrap.py 只管四個主 repo，projects 要手動；母 repo 用 --recurse-submodules=check

- 事實：
  - `agentctl/tools/wrap.py` 只 pin agentctl、instance、mod-library、modpack-design；`projects/*` 的 gitlink 要自己驗了再 pin。
  - 母 repo 的 `submodule.recurse=true` 會讓 `git grep <rev>` 報 `unable to read tree`，要加 `-c submodule.recurse=false`。
  - config 裡是 `push.recurseSubmodules=on-demand`，推母 repo 時改用 `--recurse-submodules=check`，子 repo 漏推就會擋下來。
- How to apply：
  - pin 前先列「舊 gitlink..新 HEAD」的 commit 清單。
  - public repo 只掃新增的行：帳號名、家目錄絕對路徑、金鑰前綴。
  - 單子照 `S/tmp/aos-skyrim-agent/top/push-plan.md` 的格式寫。

## aos-argon-headless-no-tools

> Argon headless 審查：提示裡寫明「不要用工具」才有產出

- 事實：第一次叫，它想讀檔，被 headless 拒了，沒有產出。第二次在提示裡寫明不要用工具、把材料貼進去，才有產出。
- 出處：`S/tmp/aos-skyrim-agent/opus-1/out/argon-adopt.md`。
