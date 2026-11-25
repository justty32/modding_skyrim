# user — 使用者偏好與確認邊界

[common/README](README.md)

agent 不用重猜的事。always-on 鐵律在 `AGENTS.md`，這裡是**這位使用者**的偏好——改了改這裡，不改鐵律。

**何時用**：使用者說了偏好、講定了確認邊界（哪些事可以直接做、哪些一定先問）、或講定分支慣例／時區／語言時，記到這裡。
**何時不用**：一次性的小事不必記（例如「這次先不要跑測試」）——那是當下的指示，不是長期偏好；長期知識歸屬層的原則見 [STRUCTURE](../../STRUCTURE.md)。

## Done when

對應的那一列已更新（或新開一列），沒有留下與新偏好矛盾的舊值。

| 項目 | 設定 |
|------|------|
| 語言 | 回覆與文件一律**繁體中文**；技術專名（mod 名、API、指令、欄位）留原文。**mod 層繁簡皆可**——要的是有中文，不是正體；缺字破版才是硬 gate |
| 分支慣例 | 直接 commit `main`，不開 branch 走 PR；**遠端只留 `main`**（2026-11-22「我希望遠端只有main」）；**push 每晚 23:00 統一做**（D25；公司 WSL 16:50，D32）|
| 直接做、不用問 | 改文件、跑唯讀指令（`git status`／`grep`／`find`／查 Nexus）、跑測試與 lint |
| 一定先問 | 臨時 push、刪檔、動 `instance/`（MO2 profile／load order／已裝 mod）、動 DB（mod-library 的 MongoDB）、安裝依賴、開新的大型工作 |
| 回覆風格 | 見 [reply-style](reply-style.md)；短、先結論。使用者問「**要不要**」時不要只回「不必」，附上可執行的判準（門檻數字）與後果，讓他能改數字 |
| 派工人 | Claude 系或 fsm gpt；codex 已退役（D20）|
| 時區 | Asia/Taipei |

2026-10-21 使用者裁示：所有負責實質工作的 agent 必須先親自讀過適用的 `wf/` 規矩，不能只靠領隊摘要；簡單工作或雜活例外。

2026-11-03 使用者裁示：事情盡量交給 agent 做，普通工作交給 `gpt-6.1-sol`，簡單工作與雜活交給 `gpt-6.1-terra`；除簡單工作與雜活外，agent 須先親自讀過適用的 `wf/` 規矩。這取代同日公司端 Opus／Sonnet 的分工偏好；頂層負責與使用者交流，領隊依平台限制與任務需要處理分派，agent 可派子 agent。2026-11-04 使用者再次確認此分工。〔codex 部分 2026-11-24 起失效，見下方 2026-11-24 段〕

2026-11-05 公司端 Claude Code 場使用者裁示：普通工作交給 Opus、簡單工作與雜活交給 Sonnet，頂層只負責與使用者交流；除簡單工作與雜活外，agent 須先親自讀過 `wf/` 規矩才開工。此為 Claude Code 平台的分工，codex 平台仍依上段 gpt-6.1-sol／terra。〔codex 平台 2026-11-24 退役，見下方 2026-11-24 段〕

2026-11-03 本場使用者授權可以隨意 push；此授權以本場為界，平時仍依上表確認。

2026-11-04 家中場使用者再次授權「可以隨意push」，運動約一個半小時期間持續做；本場可直接推送經核對的成果，其他動作邊界不由push授權擴張。

2026-11-07 家中 Claude Code 場使用者裁示：Claude 額度剩 3%（16:00 重置），本場事情盡量交給 codex `gpt-6.1-sol`；若用 Claude agent，普通工作 Opus、簡單工作與雜活 Sonnet；除簡單工作與雜活外 agent 須先讀過 `wf/` 規矩；agent 可依每線 BRIEF 的子 agent 數量上限再派 agent、模型隨意，配額往下不倍增；本場可以隨意 push。後續裁示：家機每隊最多一個外部 codex，與同程序子 agent 分開計數；選人做設計決策／架構規劃時，GPT 的優先級較低，並非禁止使用；每線 BRIEF 必寫子 agent 數量上限，取代同日稍早的無上限寫法。〔codex 部分 2026-11-24 起失效，見下方 2026-11-24 段〕

2026-11-22 家中 Claude Code 場使用者裁示（長期偏好）：技術問題由 agent 自行決定（「反正這些都是技術問題，該怎麼做就怎麼做」）；「每隔一個大段就按照wf/規矩保存進度」＝每完成一大段就照 `wf/` 規矩做階段存檔（STATE、續行點、commit；push 仍看當場授權）；使用者外出時 agent 可自主持續做、可開遊戲／MO2（照 resource-locks 持鎖、不存檔覆蓋使用者進度），並注意 CPU／記憶體（「我出門在外，你自己持續做，可以開遊戲/mo2做事。注意cpu/mem。」）。同場一次性授權（當天可 commit／push、男體選項等）記在當場 STATE，不在此。

2026-11-22 同場稍晚的長期偏好：遠端只留 `main` 已套用於母 repo、agentctl、instance、instance/profiles、mod-library；下載的 mod 壓縮包放 `~/skyrim_mods/` 根目錄保留（「下載的mod壓縮包可以丟到~/skyrim_mods」）；暫存用完可以清（「暫存全都可以清」「能刪就刪」；這是對清暫存的傾向，實際刪除仍照上表「刪檔」先問或有當場授權）。頂層詮釋（非原話）：清暫存不能弄斷可重複的流程——使用者也說「換身體這件事可能會經常做，所以這塊要留下一些口子」——所以長期流程要讀的東西放固定位置，不放 staging／`wf/temp`。

2026-11-23 家中 Claude Code 場使用者裁示：本場普通工作交給 Opus、簡單工作與雜活交給 Sonnet；agent 可以再派 agent、模型隨意；除簡單工作與雜活外 agent 須先讀過 `wf/` 規矩。「可以隨意push」以本場為界，平時仍依上表確認。組織（四部門、團隊）與模型的長期定案在 [wf/org/](../../org/README.md)；暫存三分法在 [wf/org/CHOICES.md](../../org/CHOICES.md) 第 7 題。

2026-11-24 家中 Claude Code 場使用者裁示（長期偏好，D20）：頂層問 `wf/workflows/agent-dispatch/` 要不要退役，使用者答「1.退役，以後都不要用codex了，就用fsm gpt。」從此不派 codex 線；工人用 Claude 系（Opus／Sonnet）或 fsm gpt（aos 的 `agent-fsm` 範本，腦接 llm kernel 的 GPT 端點；掛法在 `agentctl/aos/fsm-gpt/`）。上面 11-03、11-05、11-07 段裡經 codex 跑的部分（codex 平台、家機每隊一個外部 codex）一併失效，GPT 模型改經 fsm gpt 用，選哪個端點見掛法文件；「選人做設計決策／架構規劃時 GPT 優先級較低」與每線 BRIEF 寫子 agent 上限照舊。舊 codex 派線工作流同日先封存到 `wf/archive/agent-dispatch/`，隨後照 D26 刪掉，只剩 git 歷史。

2026-11-24 家中 Claude Code 場第二批使用者裁示（長期偏好，D25–D29）：頂層問五題（今天能不能 push；`wf/archive/` 要不要 `git rm`；skyrim-qa 要不要加規矩；館藏與開發座位要不要也帶 MCP；sol 該做什麼），使用者答「push就是晚上十一點統一push。可以git rm。可以加上規矩。都可以帶mcp。這兩個sol的任務分配都可以，通常是建議普通工作，至於量大呆板的，則看難易度，簡單一點的可以交給terra。」現行：每天 23:00 由頂層統一 push，各線只 commit 不 push（D25，取代上面各段「以本場為界」的逐場授權；D14 原文留在 org）；`wf/archive/` 已刪，封存照 STRUCTURE「過時即刪」（D26）；skyrim-qa 只有實體座位能用，要先拿遊戲鎖、使用者不在玩，動存檔的 console 指令先問（D27）；三個座位都帶 MCP（D28）；fsm gpt 普通工作建議 sol，量大呆板的看難易度，簡單一點的交 terra（D29；11-03 段與 aos.md 舊說法留作歷史）。定案全文在 [wf/org/decisions-2026-11b](../../org/decisions-2026-11b.md)。

2026-11-25 公司端 Claude Code 場使用者裁示（長期，D30–D38）：公司沒有遊戲和 MO2，鍵盤螢幕滑鼠不給 agent；`wf/org` 兩地共用，公司可擴充公司專屬的部分；「公司WSL這邊就是每天四點五十統一push」（16:50，家裡仍 23:00）；平日「能在公司做的就盡量做」，回家再驗（D38，理由是台灣白天避開美國高峰）。原話與做法在 [wf/org/sites](../../org/sites.md)。

領域詞彙常猜錯 → 開 `glossary.md`（見 [common/README](README.md)）。
