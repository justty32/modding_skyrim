# 調度：模型分級、委派與領隊

[lessons 索引](README.md)

## model-tiers-and-headcount

> 使用者定的模型分級（S/A/B/C/D、GPT 消耗下移兩級）、角色三層、選人判準；2026-09-25 起 GPT 沒退，A 級是 Opus 5.5／gpt-6-astra／gpt-6-sol（原 type: user）

2026-08-30 使用者定調「依用途分配團隊與角色」的模型，正式文件在 agentctl/docs/（team-model.md 第二／五／七節、team-model/plans.md、team-model/speed-and-driving.md）。使用者說**不用上網查方案**。

**現役模型**（2026-09-25 使用者更新）：Opus 5.5、gpt-6-astra、gpt-6-sol 與 Sonnet 都可用，GPT **沒有退**。codex 模型代號 `-m gpt-6-astra`（09-20 起 config 預設）／`-m gpt-6-sol`／`-m gpt-6-luna`；astra 與 sol 的用途細分待實測，暫定 astra 給需要判斷的線、sol 給量大呆板的。

**預設路由**（2026-09-08 使用者 /goal，取代下面分級表當預設路由）：普通任務交 Opus，簡單任務交 Sonnet，量大且呆板的任務開 codex gpt-sol（gpt-sol 可自行呼叫更便宜的 gpt-terra／luna 處理）；對使用者說話與給他看的東西一律大白話。頂層只做調度、裁示轉達、artifact 發布。

**headcount 逐次由使用者給**，不要自己膨脹——2026-09-25 當天說的「隊伍無上限」只限那一輪，使用者明說不要記成規則。剩下的唯一上限是「領導監看得過來」。

**角色三層**：頂層 agent（接指令、開團隊、傳達、協調使用者也會用的資源——HID／螢幕／CPU／硬碟／網路；資源使用權源頭是使用者）**通常 Opus 就夠**，某些情況 Sonnet 也行——頂層只轉達調度，比領導笨是正常的；頂層**可以有自己的輔助者 agent**（例如 Sonnet 查資料／盤點／事實查證），不經團隊領導、不算團隊 headcount，數量使用者指定，沒指定默認兩個。團隊領導＝計畫制定者，依難度用 **Fable 或 Opus**，**不建議 gpt-sol**（另一套體系、跟頂層溝通不便）；領導負擔重（計畫＋指揮＋匯報）所以 Opus 是最低標準，但若「制定計畫」分給某個成員，領導 Sonnet 也可；**領導永遠是 Claude 系**。工人依難度、內容、**使用者給的 headcount** 開，便宜 AI（gpt-sol／terra／luna）在這層大量用，但要算溝通成本（inbox 協議也有摩擦）與**領導的管理上限**（開太多管不動）；gpt-sol 開多少 terra/luna 我們管不著，只告訴它可用資源、頂多建議兩三個。

**聰明度（總分，之後會按用途細分）**：S＝Fable；A＝Opus（軟體工程）、gpt-sol（各方面，軟體工程算 B+）；B＝Opus（軟體工程之外）；C＝gpt-terra、Sonnet；D＝gpt-luna。分級以 Claude 收費為基準，往下補 E/F 很正常（terra/luna 消耗 E/F；DeepSeek 更低）。
**消耗速度**：Claude 系列與聰明度成正比；GPT 系列整體下移兩級——gpt-sol A 級腦、C 級消耗，「性價比之神」。

**context 管理**（2026-08-30）：每個 agent 管自己下級的 context，一大段任務結束就 compact；計畫制定者要在計畫裡預定大段任務間的 compact 間隙；頂層的 compact 與使用者商量；gpt-sol 的 `/compact` 從 stdin（tmux）送；Claude subagent 沒外部 compact 入口就一段一條線接力。目的是清雜訊、提升決策品質。

**信箱分層**（2026-08-30）：頂層平常不盯 inbox，但**若團隊裡有外部 agent（codex／別台機器）要直接跟頂層交流，頂層也要盯自己的信箱**。方向是**大家都可以有自己的信箱，團隊內部信箱與 agent 個人信箱都算**。個人 `mail/<session>/` 與 `topics/` 已有；缺「團隊信箱成一級概念（開團隊配一格、成員預設訂閱）」與「頂層自己那格的位址＋醒鐘策略」，寫在 team-model.md 第七節與 agentctl backlog，未實作。

**執行速度與時程**（2026-08-30）：使用者有時要求「幾小時內完成」，**計畫制定者要依各模型執行速度排時程**。速度三因素：① token 產出速度——通常越聰明越慢但不一概而論、廠商也有影響；體感上分兩檔：**B 級以上比以下慢 1.5 倍**；② 聰明度——笨的要多繞幾圈，聰明的一次搞定（所以慢模型未必總時間長）；③ **模型癖好**——gpt-sol 每做一小事就驗證，硬把時間拉長 1–2 倍（交接書要寫死驗收條數壓這個）。

相關：[[fable-top-opus-middle-management]]、[[trust-gpt-sol-more]]、[[delegate-simple-work-to-sonnet]]

## prefer-gpt-sol-for-all-tasks

> 2026-09-11 使用者原話「可以的話，之後的任務都盡量用 codex gpt-sol」；Opus 領隊只切工、合併、覆核，實作／掃描／翻譯／腳本一律交 gpt-sol（可自開 terra/luna），領隊自己動手＝違反（原 type: feedback）

使用者原話：
- 2026-09-11：「可以的話，之後的任務都盡量用 codex gpt-sol」。
- 2026-09-12：「盡量讓所有agent都指揮gpt-sol去做事。至於漢化這塊，則可以讓gpt-sol去指揮更低階更便宜的gpt-terra/luna」。
- 2026-09-16（頂層親手改 profile 裝 patch、關 MO2、開遊戲之後被糾正）：「你盡量不要自己做事。要麼gpt-sol，要麼opus, sonnet」。

**Why：** 省 Claude token；gpt-sol 便宜且可自開 terra/luna 做呆板量大的事。

**How to apply：**
1. 交接書寫死「領隊只分派／合併／覆核，不自己跑掃描或寫產物」；量小的事也丟一條 gpt-sol（`cx-<隊>-a`）。Opus 領隊的實作工人一律 codex gpt-sol。
2. 中文層交接書明寫 gpt-sol 可自開 terra／luna 做量大翻譯搬字串，gpt-sol 只做切工與 gate。額度用盡時暫改 Sonnet，重置後換回。
3. 頂層也一樣：查資料／整理表／產頁腳本能交就交，不自己寫。連「一行 profile 編輯」「裝一支 esp」「開遊戲煙霧」都要派線；自己只留：寫交接書、驗收、鎖仲裁、對使用者說話。crash log 初判可以自己看，但修法要派線。
4. 例外：拿遊戲鎖的實機段、需要 MCP（houseCARL／qa）的步驟，gpt-sol 沒有 MCP 時由領隊代跑，但只跑那一步。

相關：[[im-dispatcher-codex-implements]]、[[trust-gpt-sol-more]]、[[model-tiers-and-headcount]]

## delegate-simple-work-to-sonnet

> 使用者要我把簡單/機械性的工作丟給 sonnet subagent，不要自己全做（原 type: memory）

簡單的工作可以交給 sonnet agent（2026-08-03 使用者主動提出）。適用：查版本/日期/相容性這類有明確答案的事實查證、grep/盤點、抓 CI log、讀多檔做摘要。

**Why:** 這類工作不需要主 context，丟出去可以並行，也不會把大量原始輸出灌進主對話。

**How to apply:** `Agent` + `model: "sonnet"`，背景跑，同時我繼續做需要判斷的部分。指派時把「不要改檔案、回傳簡潔事實 + 出處」寫清楚——sonnet 會照做。動到程式碼與整條線的實作要開 codex gpt-sol 線，不是自己來（2026-08-21），見 [[im-dispatcher-codex-implements]]。注意本專案的預設是「未經使用者要求不開 subagent」，這條 feedback 就是那個要求。相關：[[push-and-remote-actions]]

## trust-gpt-sol-more

> gpt-sol 是僅次於 opus 的一線模型,要給大任務、少複查;把它當 sonnet 微管理會燒光 Claude 的 token（原 type: feedback）

2026-08-20 夜間，使用者看到我短時間燒掉大量 token 時說：

> 你這是把 codex gpt 當成是 sonnet 在用。不是的，你應該多信任他們一些，gpt-sol 是僅次於 opus 的
> 一線模型，除了會彎彎繞繞之外沒啥問題。

要避免的浪費模式：把 codex 報告過的每個 SHA-256 自己再算一遍、每幾十秒 `capture-pane` 一次、交接書寫到上百行、每一批做完都要我收成果再派下一批。

**Why:** gpt-sol 的能力足以自己完成整條工作線並自我驗證。重複驗證它已經給出證據的東西是純浪費；真正該由 Claude 做的是**規劃、分工、跨線協調、以及它做不到或不該自己決定的事**（例如產品取捨、會破壞既有契約的選項、跨 repo 的順序）。

**How to apply:**
- 一次給**整條線**的任務，不要拆成一批一批等我派工。讓它連續跑完多個 batch。
- **不要重算它已經附證據的 hash／數字**。抽驗一次建立信任即可，之後看報告。
- 讓它自己 commit **並 push**（使用者當次授權 push 的前提下），把 Claude 從迴圈裡拿掉。
- 靠 Monitor 的 busy→idle 邊緣觸發通知，**不要主動輪詢 pane**。
- 交接書寫護欄與驗收清單就好，不用把每個步驟都寫死——它自己會設計做法。
- 它唯一需要被壓住的是「為了保險亂跑驗證／彎彎繞繞」，那用「驗收就這幾條，做完就停」解決。
- 判斷密集、產出是資料表或程式的線，固定配一條不讀實作的獨立覆核線自己重跑驗收——它抓得到領導自己的驗收沒抓到的真問題，成本遠低於把錯數字交出去（2026-10-23，`agentctl/handoffs/done/2026-09-02/spike-2026-09-02/REPORT.md:126-143`）。

相關：[[codex-tmux-operational-notes]]、[[driving-other-cli-agents]]、[[delegate-simple-work-to-sonnet]]

## delegate-mod-evaluation-to-agents

> 2026-10-10 使用者原話「關於調查mod，建議你都開agent去調查」；使用者貼 Nexus 連結問「這個如何」時，頂層不自己查 houseCARL/modlist，派 agent 評估

使用者原話（2026-10-10，他連貼 Nexus 連結問「這個如何」、頂層一直自己查時）：「關於調查mod，建議你都開agent去調查」；同日再定：「一個mod開一個評估agent。你這邊就負責跟我報告」；稍晚：「你可以開無上限個agent，事情也盡量都交給agent做」。

**Why:** 頂層 context 被 mod 描述灌爆；評估是可外包的機械工作（[[im-dispatcher-codex-implements]]、[[prefer-gpt-sol-for-all-tasks]]）。

**How to apply:** 收到 mod 連結就派評估 agent，**一個 mod 一個 agent**（別用常駐線排隊）；評估要含：做什麼、本機前置是否已有、同概念 mod 撞車（[[rule-out-a-concept-scan-same-batch-siblings]]）、中文層、穩定度、給判準的建議（[[answer-should-we-with-a-threshold]]）。頂層只轉述白話結論與待裁示項。agent 數不設上限，施工與評估都派線，頂層只轉述、出選項、排 profile 寫入順序。

## line-agents-refuse-relayed-delete-approval

> 2026-10-17 line 子代理依 AGENTS.md 鐵律 2 不接受頂層轉述的刪除授權；刪除由頂層在使用者面板確認後親自跑

line 子代理會把清單和刪除腳本（purge.py，含 dry-run 與閘門）都備妥，但拒絕實刪：轉述的授權不算使用者本人確認（2026-10-17 ~/ 清理）。

**Why:** 鐵律 2 要求使用者當場確認或親自登記；子代理看不到主 session 的 AskUserQuestion 回答。

**How to apply:**
- 破壞性步驟要讓子代理產出「可審的腳本＋目標清單＋dry-run」，頂層用 AskUserQuestion 取得確認後自己跑 `--yes`，別再把刪除指令轉派一輪。
- 大批刪除／搬移前先建一份固定欄位的刪除帳本（來源路徑、大小、憑證、可否重下、處置方式），帳本列數＝授權筆數的 gate 全過才動手；預設 `mv` 到暫存 trash，只有使用者單獨明確授權「永久刪除」才用 `rm`，容量或任何一筆對不上就整批停手（2026-10-23，`agentctl/handoffs/done/2026-08-31/clean-2026-08-31/HANDOFF.md:51-101`）。

相關：[[dont-clutter-home-with-agent-output]]
