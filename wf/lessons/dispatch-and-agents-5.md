# 調度、模型分級與交接書（5/9）

[lessons 索引](README.md)｜同主題：[dispatch-and-agents](dispatch-and-agents.md)、[dispatch-and-agents-2](dispatch-and-agents-2.md)、[dispatch-and-agents-3](dispatch-and-agents-3.md)、[dispatch-and-agents-4](dispatch-and-agents-4.md)、[dispatch-and-agents-6](dispatch-and-agents-6.md)、[dispatch-and-agents-7](dispatch-and-agents-7.md)、[dispatch-and-agents-8](dispatch-and-agents-8.md)、[dispatch-and-agents-9](dispatch-and-agents-9.md)

## delegate-simple-work-to-sonnet

> 使用者要我把簡單/機械性的工作丟給 sonnet subagent，不要自己全做（原 type: memory）

簡單的工作可以交給 sonnet agent（2026-08-03 使用者主動提出）。適用：查版本/日期/相容性這類有明確答案的事實查證、grep/盤點、抓 CI log、讀多檔做摘要。

**Why:** 這類工作不需要主 context，丟出去可以並行，也不會把大量原始輸出灌進主對話。

**How to apply:** `Agent` + `model: "sonnet"`，背景跑，同時我繼續做需要判斷的部分。指派時把「不要改檔案、回傳簡潔事實 + 出處」寫清楚——sonnet 會照做。**2026-08-21 更正**：動到程式碼與整條線的實作要開 codex gpt-sol 線，不是自己來，見 [[im-dispatcher-codex-implements]]。注意本專案的預設是「未經使用者要求不開 subagent」，這條 feedback 就是那個要求。相關：[[push-and-remote-actions]]

## trust-gpt-sol-more

> gpt-sol 是僅次於 opus 的一線模型,要給大任務、少複查;把它當 sonnet 微管理會燒光 Claude 的 token（原 type: feedback）

2026-08-20 夜間，使用者看到我幾分鐘內燒掉 60% token，指出原因：

> 你這是把 codex gpt 當成是 sonnet 在用。不是的，你應該多信任他們一些，gpt-sol 是僅次於 opus 的
> 一線模型，除了會彎彎繞繞之外沒啥問題。

我當時的浪費模式：把 codex 報告過的每個 SHA-256 自己再算一遍、每幾十秒 `capture-pane` 一次、
交接書寫到 110–150 行、每一批做完都要我收成果再派下一批。

**Why:** gpt-sol 的能力足以自己完成整條工作線並自我驗證。重複驗證它已經給出證據的東西是純浪費；
真正該由 Claude 做的是**規劃、分工、跨線協調、以及它做不到或不該自己決定的事**（例如產品取捨、
會破壞既有契約的選項、跨 repo 的順序）。

**How to apply:**
- 一次給**整條線**的任務，不要拆成一批一批等我派工。讓它連續跑完多個 batch。
- **不要重算它已經附證據的 hash／數字**。抽驗一次建立信任即可，之後看報告。
- 讓它自己 commit **並 push**（使用者當次授權 push 的前提下），把 Claude 從迴圈裡拿掉。
- 靠 Monitor 的 busy→idle 邊緣觸發通知，**不要主動輪詢 pane**。
- 交接書寫護欄與驗收清單就好，不用把每個步驟都寫死——它自己會設計做法。
- 它唯一需要被壓住的是「為了保險亂跑驗證／彎彎繞繞」，那用「驗收就這幾條，做完就停」解決。

相關：[[codex-tmux-operational-notes]]、[[driving-other-cli-agents]]、[[delegate-simple-work-to-sonnet]]

## rush-mode-parallel-opus-agent-lines

> 2026-09-26 急件模式：一份 COMMON.md 交接＋Agent 工具開 8 條 Opus 平行線，15 分鐘收完八題存檔調查；一條線持遊戲鎖代跑 RT-QUEUE（原 type: memory）

2026-09-26 早使用者 09:07 開場、10:20 關機，說「想開多少線都可以、儘快」。做法：先寫一份 `handoffs/home-<日期>/COMMON.md`（硬停時刻、報告格式、路徑、鎖規則），再用 Agent 工具一次開 8 條 Opus 調查線（每線一個交接段），只有一條線准取 game.lock 並在 09:45 代跑其他線排進 `RT-QUEUE.md` 的 console 查詢；最後開一條整理線把八份 REPORT 濃縮成 `PRE-PLAY-CHECKLIST.md`。09:25 全部收線並 commit。

**Why:** codex tmux 線要送鍵、驗 Enter、盯 Working，起線成本高；Agent 工具的 Opus 線起線零成本、完成有通知、可平行八條，急件時快得多。使用者當天也明說「用啥模型都行」。

**How to apply:** 使用者有硬時限或說「儘快」時，走這條：COMMON.md → 平行 Agent(Opus) → 單線持鎖代跑 RT-QUEUE → 整理線出清單。平常仍依 [[prefer-gpt-sol-for-all-tasks]]。注意子 agent 偶爾寫 REPORT 被 harness 擋，頂層要從完成通知代落檔；MO2 開過後 profile 三檔會漂移，收線派小線 `git checkout` 還原（見 [[mo2-first-launch-drops-new-plugin-star]]、[[mo2-auto-adds-stray-mods-dirs]]）。

## leads-manage-subordinate-context

> 2026-09-18 使用者定：Claude 系 agent 的 context 由其上級管理（頂層管 Opus、Opus 管 Sonnet）；gpt-sol 自帶 auto-compact 不用管；建議開 auto compact（原 type: feedback）

2026-09-18 使用者原話：「你轄下的claude系agent如opus, sonnet，要記得管理他們的context。opus作為隊伍領導，也要管理其轄下的sonnet的context。我建議是設定auto compact會比較舒服。」頂層的 context 由使用者管（他會抓斷點叫 compact）。

**Why:** Opus／Sonnet 領隊吃大輸出（log、截圖、目錄列表）後 context 爆掉會卡線，而且沒人替它們抓斷點；gpt-sol 會自己 auto-compact 所以只有 Claude 系要管。

**How to apply:** 開隊時交接書（COMMON.md）寫死：大輸出交 gpt-sol 落檔、Sonnet 任務單一做完就收、領隊每完成一項先寫 REPORT 再接下一項、Sonnet 回報 ≤10 行只回結論與路徑。本機 auto-compact 是預設開（settings 沒設 autoCompactEnabled=false），但不要依賴它。與 [[fable-top-opus-middle-management]]、[[leads-must-not-end-turn-to-wait]] 並用。

## leads-must-not-end-turn-to-wait

> Opus 領隊用「結束回合＋背景 watcher」當等待會卡死；交接書要寫死「前景 until 迴圈（timeout 540 分段）」，卡住超過 20 分鐘就 TaskStop 換人接手（原 type: memory）

2026-09-06 三個領隊（upd／new10／mcoi）都在等工人或等鎖時「結束回合、掛背景 watcher」；watcher 觸發後領隊有時會醒、有時不會。lead-upd 從 16:52 卡到 18:59 沒套最後一批，最後 `TaskStop` 停掉、開 lead-upd2 用現成的 plan 十分鐘做完。

**Why:** 子代理結束回合後，佇列裡的 SendMessage 只在「下一個 tool round」送達；沒有 tool round 就永遠收不到。背景 Bash 完成的通知也不保證把它叫醒。
**How to apply:** 交接書與 spawn prompt 明寫「等待一律用前景 Bash `until` 迴圈，每輪 `timeout 540`，沒到再跑一輪；別把結束回合當等待」。dispatcher 看到 STATE.md 超過 20 分鐘沒動、鎖空、沒 commit → 直接 TaskStop，開一個小隊接手（料通常都在 staging＋plan json）。相關：[[im-dispatcher-codex-implements]]、[[tmux-working-text-is-not-liveness]]。
