# 調度：頂層角色與誰來做

[lessons 索引](README.md)

## im-dispatcher-codex-implements

> 我是調度者，實作交給 codex gpt-sol；不要自己把整條線的查證與改碼做完（原 type: feedback）

使用者原話：

- 2026-08-21：「記住，你只是調度者，實際事情由 codex gpt sol 去做。」（當時頂層自己做完兩個上游缺陷的根因分析、改 Papyrus、寫報告、提交，全部沒有開線。）
- 2026-08-29：「beyond reach 那些，與相關的，都要下載」——頂層先自己 grep 決策文件、翻庫存、比對版本才寫交接書，使用者當場糾正：「**你不要自己調查，你直接委託 agent 團隊**」。

**Why:** 主 context 是稀缺資源。深潛實作會把大量工具輸出灌進主對話，
一條線就吃掉三成 context；而 codex 線是獨立 context，跑完只回報結論。
調度者的價值在拆任務、寫死驗收、判斷回報可不可信，不在親手做。
盤點本身就是線的工作：線有獨立 context，查得比頂層全；頂層先查一輪不但重複，還會把不完整的事實寫死進交接書，反而框住線。

**How to apply:**
- 拿到「去搞定 X」這種任務時，先想「這該開幾條線」，不是「我先查一下」。這條**覆蓋** [[delegate-simple-work-to-sonnet]]
  裡「判斷與改碼自己來」那句。交接書寫法見 [[codex-tmux-operational-notes]]、
  信任程度見 [[trust-gpt-sol-more]]。
- **瑣碎不是自己動手的理由**（2026-08-22，「刪 5 個檔＋修斷鏈＋git commit」也算）：只要是**改檔案、跑 git、裝 mod、驗證檔案雜湊、寫報告**，一律開線。
  頂層自己只做：讀狀態、判斷、寫交接書、轉述使用者回報、把關誠實界線。
- 交接書只寫「使用者要什麼、什麼算範圍內（範圍、判準、禁區、驗收）、遇到分歧怎麼選」；事實由線用 houseCARL 自己查，
  連「庫裡已經有哪些版本」都交給線去比。頂層的最小查證只剩：鎖狀態、現役線有沒有衝突、路徑存不存在。

## dispatcher-must-use-own-assistants

> 2026-08-30 使用者指出頂層做太多事;頂層有權開自己的助手(默認兩個)卻一個都沒開,機械工作要外包（原 type: feedback）

2026-08-30 使用者在同時跑七個團隊的那一輪說：

> 我覺得你作為頂層 agent，**做太多事情了**。

同日他三次說同一件事：

- 「盡量把工作量都押給 codex gpt，sol／terra／luna 都可以。」
- 「記住，盡量把事情都押給 codex gpt。」
- 「盡量把工作都交給 codex。」

2026-08-31 再次申誡：「你盡量不要做事」。

**Why:** `agentctl/docs/team-model.md` 寫了「頂層**通常也會被允許有自己的輔助者 agent**
（例如開 Sonnet 去查資料、盤點），不必事事經過團隊領導……數量使用者通常會指定，
**沒指定就默認兩個**」。問題不是手癢，是忘了自己有外包的權限。**重申＝做得不夠、預設沒改，不是他忘了說過。**

**越界的標尺**（2026-08-30 頂層自己做了的）：資料檔合併（寫合併腳本、審查 md、回填來源 md）、逐隊驗收（驗證腳本、重跑 unittest、查 git ahead/behind）、調查型 diff、一整批文件撰寫。

**How to apply:**
**開場就開助手**，不要等到自己開始寫腳本才想起來。沒指定數量就開兩個。

**助手優先用 codex 線**（不編團隊，終局直接進 `inbox/new/`），需要頻繁來回才用 Claude subagent。

**外包**：資料檔合併、驗收腳本、跑測試、查 git 狀態、把已定結論落成文字、文件格式與連結修補；交接書撰寫、tmux 發射驅動、巡線放行、inbox 轉信也外包給常駐助手 cx-ops（standing 契約在 `agentctl/handoffs/ops-2026-08-31/STANDING.md`）。

**留給自己**：仲裁兩隊互相矛盾的宣告、資源／鎖的分配、範圍裁定、對使用者說話、管領導 context。
（即使仲裁需要地面真相，探測也可以叫助手跑完回報，我只做判斷。）

別過度修正成「什麼都不碰」——[[dont-inflate-light-preferences]]。判準是
**「這件事需要我的判斷，還是只需要有人動手」**。

**預設是「開一條 codex 線掛在 dispatcher 底下」**（如 `cx-ops1`／`cx-diag1`；同期純 codex 線做得跟 Opus 領隊一樣好，`cx-diag1` 定位出當天崩潰根因）：
寫交接書 → `tmux new-session` ＋ `send-keys 'codex'` → 它自己跑 → `inbox_send.sh` 回報。
**不編團隊、不配 Opus 領導。**

**只有同時滿足這兩條才開 Opus 領導**：① 真的需要 **3 條以上並行線同時被監看**；
② 判斷內容是非機械的（要仲裁、要改判、要跨線調和）。
單一有界任務（改文件、查一個 mod、跑一支工具、產一份報告）**一律 codex 線**。開團隊的門檻是「要不要有人替我監看與核驗多條線」，不是「這件事重不重要」。

使用者說「開團隊」時，**那是指「別自己做」，不是指「一定要配 Opus」**——
codex 線也是團隊的一種。若他要的是多線並行，再開領導。

相關：[[im-dispatcher-codex-implements]]（那條講不要深潛實作；這條補上「而且你有助手可以用」）、[[model-tiers-and-headcount]]、[[trust-gpt-sol-more]]。

## fable-top-handles-only-hardest

> 2026-09-09 使用者裁示「你只負責最困難的任務」——Fable 頂層除了調度，只親自做最難的那一件；其餘一律派 Opus／Sonnet／gpt-sol（原 type: feedback）

2026-09-09 使用者在 /goal 之後補一句原話：「你只負責最困難的任務」。

**Why:** Fable 是最貴也最聰明的一級（見 [[model-tiers-and-headcount]]）。頂層 context 是最稀缺的資源，
拿來做普通事等於用最貴的人做雜工；他要的是 Fable 的判斷力留給真正卡住、別的模型解不開的問題。

**How to apply:**
- 頂層預設只做：調度、鎖、對使用者說話、artifact 發布——和**唯一一件最難的任務**（例如別隊卡死的真因診斷、跨隊衝突仲裁）。
- 開場先把待辦按難度排，最難的一件留給自己（或在別隊卡住時接手），其餘全派出去：普通→Opus 領隊、簡單→Sonnet、量大呆板→codex gpt-sol（可自開 terra／luna）。
- 「最難」的判準：需要跨多個 mod／層／工具鏈的推理、前一輪已經失敗過一次以上、或後果不可逆。不是「我順手就能做」。
- 這條**加強**而不是取代 [[im-dispatcher-codex-implements]] 與 [[dispatcher-must-use-own-assistants]]。

## fable-top-opus-middle-management

> 主 session 是 Fable 只做頂層決策＋鎖＋瀏覽器＋對使用者；中層管理線用 Fable subagent，它預設指揮 codex gpt-sol 做實作、重要部分改指揮 Opus、Sonnet 不限（原 type: memory）

使用者原話（依時間）：

- 2026-08-27 定三層結構：

  > 你是 fable，耗 token 很快。那些 codex 回報的時候是走 inbox，你會被喚醒去讀信。
  > 我是覺得你不要親自去讀信，你應該讓 opus 去管理這些 codex 和 inbox，然後匯報給你，
  > 你就做最終頂層決策者就好。

- 2026-08-30：「可以改成用 fable，然後讓 fable 去指揮 opus」；同日「大家都可以用 sonnet」；派工模型改定後要求「先跟管理線說，讓他們之後新派的都用這套，不然 token 消耗有點快」；同日晚「請 opus agent 去指揮 gpt-sol」。
- 2026-09-05 家中場：「我允許你帶領十個團隊，每個團隊由 opus 領導，組員可以有兩個 opus，兩個 gpt-sol，兩個 sonnet，context 由 opus 領導管理。而 opus 領導的 context 由你管理。記得每隔一些大任務後，若下個大任務差別很大或 context 達到上限的一半，那就記得 compact 他們，opus 領導對底下的組員也是。可以分一半事情給 gpt-sol 做，但順手的話還是 opus/sonnet 比較好，因爲溝通比較順暢。」

**Why**：Fable 每次被 inbox 訊息喚醒去讀信、巡線、收線，燒的都是最貴的 context；線管理是照契約辦事（驗收條數寫死、七步收線），不需要頂層判斷。

**How to apply**：
結構：**主 session（頂層決策／鎖／瀏覽器／對使用者）→ 管理線／領隊（讀 inbox、盯 tmux、
寫 orders、拆工、核驗收、收線、接力派線、歸檔 new/→read/）→ 工人（執行）**。交接書寫給管理線，由它自行切給工人。

管理線用哪個模型看使用者當下怎麼說（Fable subagent `Agent` 工具 `model: fable`，或 Opus），別把「管理線一定是 Fable」當死規則；2026-09-05 起領隊＝Opus（`Agent` model opus），headcount 上限 10 隊×(2 Opus＋2 gpt-sol＋2 Sonnet)。

工人：**預設 codex gpt-sol**（走 agentctl 的 driving-codex 流程：tmux、交接書、固定驗收條數；auto-compact 自理），**重要部分**（判斷密集、改壞了代價高的）用 **Opus**；
**Sonnet 不限制**（機械性：表格抽資料檔、對帳、連結修正、盤點），需要語意判斷的（散文拆段、封存判定、A/B 分類）用 Opus。gpt-sol 可以隨意指派 gpt terra／luna 當它自己的 subagent，管理線不管那一層。gpt-sol 拿一半量可以，但溝通順暢優先 Opus／Sonnet。

派工模型一改，正在跑的管理線也要當場切換，不是等下一輪。

compact 判準＝大題目切換或 context 過半；頂層對領隊、領隊對成員都照做。

Fable **不掛 inbox 醒鐘**、不逐則讀信；只在管理線上呈五類事時醒：待下載清單就緒、
需使用者決定、需鎖或瀏覽器、管理線要交棒、全部收工戰報。

管理線的 context 也有限：吃緊時寫 STATE.md 交棒，由頂層開繼任者——不硬撐。

這條疊在 [[im-dispatcher-codex-implements]] 之上：那條說「實作歸 codex」，這條再把
「管理」也從頂層剝出去。

歸檔訊息（new/→read/）是管理線職責，順帶讓頂層的 UserPromptSubmit hook 輸出瘦身。

對使用者說話與給他看的文件一律大白話（2026-09-05；比 [[top-level-explain-in-plain-words]] 更強：不是「順手」，是「一律」）。

相關：[[delegate-simple-work-to-sonnet]]、[[driving-other-cli-agents]]、[[trust-gpt-sol-more]]
