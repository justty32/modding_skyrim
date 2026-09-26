# 調度、模型分級與交接書（3/9）

[lessons 索引](README.md)｜同主題：[dispatch-and-agents](dispatch-and-agents.md)、[dispatch-and-agents-2](dispatch-and-agents-2.md)、[dispatch-and-agents-4](dispatch-and-agents-4.md)、[dispatch-and-agents-5](dispatch-and-agents-5.md)、[dispatch-and-agents-6](dispatch-and-agents-6.md)、[dispatch-and-agents-7](dispatch-and-agents-7.md)、[dispatch-and-agents-8](dispatch-and-agents-8.md)、[dispatch-and-agents-9](dispatch-and-agents-9.md)

## fable-top-opus-middle-management

> 主 session 是 Fable 只做頂層決策＋鎖＋瀏覽器＋對使用者；中層管理線用 Fable subagent，它預設指揮 codex gpt-sol 做實作、重要部分改指揮 Opus、Sonnet 不限（原 type: memory）

2026-08-27 使用者定調三層結構：

> 你是 fable，耗 token 很快。那些 codex 回報的時候是走 inbox，你會被喚醒去讀信。
> 我是覺得你不要親自去讀信，你應該讓 opus 去管理這些 codex 和 inbox，然後匯報給你，
> 你就做最終頂層決策者就好。

**Why**：Fable 每次被 inbox 訊息喚醒去讀信、巡線、收線，燒的都是最貴的 context。
Opus 中層便宜得多，而且線管理是照契約辦事（驗收條數寫死、七步收線），不需要頂層判斷。

**How to apply**：
- 結構：**Fable（頂層決策／鎖／瀏覽器／對使用者）→ Opus 管理線（讀 inbox、盯 tmux、
  寫 orders、核驗收、收線、接力派線、歸檔 new/→read/）→ codex gpt-sol（執行，auto-compact
  自理，可自開 terra subagent）**。
- Fable **不掛 inbox 醒鐘**、不逐則讀信；只在管理線上呈五類事時醒：待下載清單就緒、
  需使用者決定、需鎖或瀏覽器、管理線要交棒、全部收工戰報。
- 管理線的 context 也有限：吃緊時寫 STATE.md 交棒，由 Fable 開繼任者——不硬撐。
- 這條疊在 [[im-dispatcher-codex-implements]] 之上：那條說「實作歸 codex」，這條再把
  「管理」也從 Fable 剝出去。
- 歸檔訊息（new/→read/）是管理線職責，順帶讓 Fable 的 UserPromptSubmit hook 輸出瘦身。

相關：[[delegate-simple-work-to-sonnet]]、[[driving-other-cli-agents]]、[[trust-gpt-sol-more]]

**2026-08-30 修正**：使用者改口「可以改成用 fable，然後讓 fable 去指揮 opus」——中層管理線
改用 **Fable subagent**（`Agent` 工具 `model: fable`），它再開 Opus subagent 做實作；Opus 不再直接
當管理線。三層變成 **Fable 主 session（頂層）→ Fable 管理線（拆工、派 Opus、核驗收、回報）→ Opus／codex（實作）**。
主 session 的角色不變：仍只做決策、鎖、瀏覽器、對使用者。交接書照舊寫給管理線，由它自行切給 Opus。
同日再補「大家都可以用 sonnet」：管理線派工人時 **Sonnet 是預設**（機械性：表格抽資料檔、對帳、連結修正、盤點），
需要語意判斷的（散文拆段、封存判定、A/B 分類）才用 Opus。

**2026-08-30 再修（之後的派工模型）**：Fable 管理線的實作工人**預設是 codex gpt-sol**（走 agentctl 的
driving-codex 流程：tmux、交接書、固定驗收條數），**重要部分**（判斷密集、改壞了代價高的）改指揮 **Opus**；
**Sonnet 不限制**（機械活隨便用）。gpt-sol 可以隨意指派 gpt terra／luna 當它自己的 subagent，管理線不管那一層。
使用者隨即要求「先跟管理線說，讓他們之後新派的都用這套，不然 token 消耗有點快」——所以正在跑的管理線也要當場切換，不是等下一輪。

**2026-08-30 晚**：使用者臨時指定「請 opus agent 去指揮 gpt-sol」——管理線用 Opus 也行，看使用者當下怎麼說；工人仍預設 gpt-sol。別把「管理線一定是 Fable」當死規則。

**2026-09-05 家中場**：使用者原話「我允許你帶領十個團隊，每個團隊由 opus 領導，組員可以有兩個 opus，兩個 gpt-sol，兩個 sonnet，context 由 opus 領導管理。而 opus 領導的 context 由你管理。記得每隔一些大任務後，若下個大任務差別很大或 context 達到上限的一半，那就記得 compact 他們，opus 領導對底下的組員也是。可以分一半事情給 gpt-sol 做，但順手的話還是 opus/sonnet 比較好，因爲溝通比較順暢。」——所以：領隊＝Opus（`Agent` model opus），headcount 上限 10 隊×(2 Opus＋2 gpt-sol＋2 Sonnet)；gpt-sol 拿一半量可以，但溝通順暢優先 Opus／Sonnet；compact 判準＝大題目切換或 context 過半，領隊對成員也照做。同日另一句：對使用者說話與給他看的文件都要大白話（比 [[top-level-explain-in-plain-words]] 更強：不是「順手」，是「一律」）。
