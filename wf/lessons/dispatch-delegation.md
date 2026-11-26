# 調度：模型分級、委派與領隊

[lessons 索引](README.md)

現行分工與子 agent 規則只依 [team-model](../../agentctl/docs/team-model.md)（codex 2026-11-24 退役，D20；fsm gpt 端點分工 D29，[decisions-2026-11b](../org/decisions-2026-11b.md)）；下列原話裡的「codex gpt-sol」照現行選型讀成 fsm gpt 的 sol 端點或 Claude 系工人。

## model-tiers-and-headcount

> 使用者定的模型分級、角色三層、選人判準、context 管理、信箱分層與執行速度，全文已收進 team-model；本條只留指標與使用者原話

2026-08-30 使用者定調「依用途分配團隊與角色」，並說**不用上網查方案**。現行全文：角色三層 [team-model/roles.md](../../agentctl/docs/team-model/roles.md)、聰明度分級 [intelligence-tiers.md](../../agentctl/docs/team-model/intelligence-tiers.md)、消耗速度與選人判準 [team-model.md](../../agentctl/docs/team-model.md) 第三、四節（gpt-sol 是 A 級腦、C 級消耗的「性價比之神」）、context 管理 [context.md](../../agentctl/docs/team-model/context.md)、執行速度與逐模型指揮心得 [speed-and-driving.md](../../agentctl/docs/team-model/speed-and-driving.md)（使用者有時要求「幾小時內完成」，排時程依各模型速度）、方案 [plans.md](../../agentctl/docs/team-model/plans.md)。

2026-09-25 使用者當場說的「隊伍無上限」只限那一輪，並明說不要記成通則；今日子 agent 數量依每線 BRIEF 上限，配額往下不倍增。

信箱分層（2026-08-30）：頂層平常不盯信箱，但團隊裡有外部 agent（別台機器、樹外 session）要直接跟頂層交流時，頂層也要盯自己的信箱。

相關：[[fable-top-opus-middle-management]]、[[trust-gpt-sol-more]]、[[delegate-simple-work-to-sonnet]]

## prefer-gpt-sol-for-all-tasks

> 領隊只切工、合併、覆核，實作／掃描／翻譯／腳本一律派給工人，領隊自己動手＝違反；派誰依現行選型（Claude 系或 fsm gpt，端點分工照 D29）

使用者原話：
- 2026-09-11：「可以的話，之後的任務都盡量用 codex gpt-sol」。
- 2026-09-12：「盡量讓所有agent都指揮gpt-sol去做事。至於漢化這塊，則可以讓gpt-sol去指揮更低階更便宜的gpt-terra/luna」。
- 2026-09-16（頂層親手改 profile 裝 patch、關 MO2、開遊戲之後被糾正）：「你盡量不要自己做事。要麼gpt-sol，要麼opus, sonnet」。

**Why:** 省 Claude token；GPT 端點便宜，量大呆板的事再往下交更便宜的端點。

**How to apply:**
1. 交接書寫死「領隊只分派／合併／覆核，不自己跑掃描或寫產物」；量小的事也派一個工人。
2. 中文層：量大翻譯、搬字串交 terra／luna 這類便宜端點，sol 只做切工與 gate。額度或 API 不穩時 Claude 系與 fsm gpt 互為備援，恢復後換回。
3. 頂層同 [[im-dispatcher-codex-implements]]：連「一行 profile 編輯」「裝一支 esp」「開遊戲煙霧」都派線；crash log 初判可以自己看，修法派線。
4. 例外：要拿遊戲鎖的實機段、工人沒有的 MCP（houseCARL／qa）步驟，由領隊代跑，但只跑那一步。

相關：[[trust-gpt-sol-more]]、[[model-tiers-and-headcount]]

## delegate-simple-work-to-sonnet

> 使用者要我把簡單/機械性的工作丟給 sonnet subagent，不要自己全做

簡單的工作可以交給 sonnet agent（2026-08-03 使用者主動提出）。適用：查版本/日期/相容性這類有明確答案的事實查證、grep/盤點、抓 CI log、讀多檔做摘要。

**Why:** 這類工作不需要主 context，丟出去可以並行，也不會把大量原始輸出灌進主對話。

**How to apply:** `Agent` + `model: "sonnet"`，背景跑，同時繼續做需要判斷的部分。指派時寫清楚「不要改檔案、回傳簡潔事實 + 出處」——sonnet 會照做。動到程式碼與整條線的實作也派工人線，不是自己來（2026-08-21，見 [[im-dispatcher-codex-implements]]）。數量依每線 BRIEF 上限，配額往下不倍增。相關：[[push-and-remote-actions]]

## trust-gpt-sol-more

> gpt-sol 是僅次於 opus 的一線模型，要給大任務、少複查；把它當 sonnet 微管理會燒光 Claude 的 token

2026-08-20 夜間，使用者看到我短時間燒掉大量 token 時說：

> 你這是把 codex gpt 當成是 sonnet 在用。不是的，你應該多信任他們一些，gpt-sol 是僅次於 opus 的
> 一線模型，除了會彎彎繞繞之外沒啥問題。

**Why:** gpt-sol 能自己完成整條工作線並自我驗證，重複驗證它已附證據的東西是純浪費；Claude 該做的是規劃、分工、跨線協調，以及它做不到或不該自己決定的事（產品取捨、破壞既有契約的選項、跨 repo 順序）。

**How to apply:**
- 一次給**整條線**，讓它連續跑完多個 batch，不要拆成一批一批等我派。
- **不要重算它已附證據的 hash／數字**，抽驗一次建立信任即可；不要每幾十秒看一次畫面或信箱；交接書寫護欄與驗收清單就好，不必上百行寫死每一步。
- 讓它自己 commit（push 由頂層每天 23:00 統一，D25）。
- 工人每步寫 PROGRESS、頂層 ≤20 分鐘巡檢一次就夠。
- 唯一要壓住的是「為了保險亂跑驗證／彎彎繞繞」：寫「驗收就這幾條，做完就停」。
- 判斷密集、產出是資料表或程式的線，固定配一條不讀實作的獨立覆核線自己重跑驗收——它抓得到領導驗收漏掉的真問題，成本遠低於交出錯數字（2026-10-23，`agentctl/handoffs/done/2026-09-02/spike-2026-09-02/REPORT.md:126-143`）。

相關：[[codex-tmux-operational-notes]]、[[delegate-simple-work-to-sonnet]]

## delegate-mod-evaluation-to-agents

> 2026-10-10 使用者原話「關於調查mod，建議你都開agent去調查」；使用者貼 Nexus 連結問「這個如何」時，頂層不自己查 houseCARL/modlist，派 agent 評估

使用者原話（2026-10-10，他連貼 Nexus 連結問「這個如何」、頂層一直自己查時）：「關於調查mod，建議你都開agent去調查」；同日再定：「一個mod開一個評估agent。你這邊就負責跟我報告」；稍晚：「你可以開無上限個agent，事情也盡量都交給agent做」。

**Why:** 頂層 context 被 mod 描述灌爆；評估是可外包的機械工作。

**How to apply:** 收到 mod 連結就派評估 agent，**一個 mod 一個 agent**（別用常駐線排隊）；評估要含：做什麼、本機前置是否已有、同概念 mod 撞車（[[rule-out-a-concept-scan-same-batch-siblings]]）、中文層、穩定度、給判準的建議（[[answer-should-we-with-a-threshold]]）。頂層只轉述白話結論與待裁示項、出選項、排 profile 寫入順序。今日 agent 數量依每線 BRIEF 上限，配額往下不倍增。相關：[[im-dispatcher-codex-implements]]

## line-agents-refuse-relayed-delete-approval

> 2026-10-17 line 子代理依 AGENTS.md 鐵律 2 不接受頂層轉述的刪除授權；刪除由頂層在使用者面板確認後親自跑

line 子代理會把清單和刪除腳本（purge.py，含 dry-run 與閘門）都備妥，但拒絕實刪：轉述的授權不算使用者本人確認（2026-10-17 ~/ 清理）。

**Why:** 鐵律 2 要求使用者當場確認或親自登記；子代理看不到主 session 的 AskUserQuestion 回答。

**How to apply:**
- 破壞性步驟讓子代理產出「可審的腳本＋目標清單＋dry-run」，頂層用 AskUserQuestion 取得確認後自己跑 `--yes`，別再把刪除指令轉派一輪。
- 大批刪除／搬移前先建固定欄位的刪除帳本（來源路徑、大小、憑證、可否重下、處置方式），帳本列數＝授權筆數的 gate 全過才動手；預設 `mv` 到暫存 trash，只有使用者單獨明確授權「永久刪除」才用 `rm`，容量或任何一筆對不上就整批停手（2026-10-23，`agentctl/handoffs/done/2026-08-31/clean-2026-08-31/HANDOFF.md:51-101`）。

相關：[[dont-clutter-home-with-agent-output]]
