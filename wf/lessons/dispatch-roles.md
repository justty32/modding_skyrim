# 調度：頂層角色與誰來做

[lessons 索引](README.md)

## im-dispatcher-codex-implements

> 我是調度者，實作交給 codex gpt-sol；不要自己把整條線的查證與改碼做完（原 type: feedback）

2026-08-21 使用者明確更正：「記住，你只是調度者，實際事情由 codex gpt sol 去做。」
當時我已經自己做完兩個上游缺陷的完整根因分析、寫 BSA reader、反編譯、改 Papyrus、
編譯、位元組碼比對、寫報告、提交 —— 全部沒有開線。

**Why:** 主 context 是稀缺資源。深潛實作會把大量工具輸出灌進主對話，
一條線就吃掉三成 context；而 codex 線是獨立 context，跑完只回報結論。
調度者的價值在拆任務、寫死驗收、判斷回報可不可信，不在親手做。

**How to apply:** 拿到「去搞定 X」這種任務時，先想「這該開幾條線」，不是「我先查一下」。
探索性的前期查證可以自己做一點，但一旦確定要動手實作就開 codex 線交出去，
把已查明的事實寫進交接書讓它不必重查。這條**覆蓋** [[delegate-simple-work-to-sonnet]]
裡「判斷與改碼自己來」那句。交接書寫法見 [[codex-tmux-operational-notes]]、
信任程度見 [[trust-gpt-sol-more]]。

**2026-08-22 補充——這條比想像中更嚴格。** 使用者第三次糾正時，我正在做的是
「刪 5 個檔＋修斷鏈＋git commit」這種看起來很瑣碎的事。**瑣碎不是自己動手的理由。**

具體觸發：只要是**改檔案、跑 git、裝 mod、驗證檔案雜湊、寫報告**，一律開 codex 線。
我自己只做：讀狀態、判斷、寫交接書、轉述使用者回報、把關誠實界線。
唯一例外是**為了寫好交接書而做的最小查證**（例如確認路徑存在、確認鎖狀態）。

**2026-08-29 再收緊——「為了寫交接書的最小查證」被我撐太大。** 使用者只說了
「beyond reach 那些，與相關的，都要下載」，我卻先自己 grep 決策文件、翻庫存、
比對版本，才寫交接書；使用者當場糾正：「**你不要自己調查，你直接委託 agent 團隊**」。

**盤點本身就是線的工作。** 交接書只要寫清楚**範圍、判準、禁區、驗收**，
事實由線用 houseCARL 自己查——它有獨立 context，查得比我全，也不佔主對話。
我先查一輪不但重複，還會把不完整的事實寫死進交接書，反而框住線。

**修正後的界線**：交接書裡我只給「使用者要什麼、什麼算範圍內、遇到分歧怎麼選」，
連「庫裡已經有哪些版本」都交給線去比。真正的最小查證只剩：鎖狀態、現役線有沒有衝突、
路徑存不存在。

## dispatcher-must-use-own-assistants

> 2026-08-30 使用者指出頂層做太多事;頂層有權開自己的助手(默認兩個)卻一個都沒開,機械工作要外包（原 type: feedback）

2026-08-30 使用者在同時跑七個團隊的那一輪說：

> 我覺得你作為頂層 agent，**做太多事情了**。

**Why:** `agentctl/docs/team-model.md` 早就寫了「頂層**通常也會被允許有自己的輔助者 agent**
（例如開 Sonnet 去查資料、盤點），不必事事經過團隊領導……數量使用者通常會指定，
**沒指定就默認兩個**」。我**一個都沒開**，把機械工作全部自己做了。
根本問題不是手癢，是**忘了自己有外包的權限**。

**那次我越界的具體項目**（拿來當標尺）：
- 三隊 `RESULT.json` 的**合併**——自己寫合併腳本、寫審查 md、回填來源 md
- **逐隊驗收**——自己寫驗證腳本、重跑 unittest、查 git ahead/behind
- **不死院 map ID 調查**——自己 diff 兩版 flver 清單
- **一整批文件撰寫**——housecarl／driving-codex／launch-and-safety／KNOWN-ISSUES／翻譯政策／claims／SESSION-LOG

**How to apply:**
- **開場就開助手**，不要等到自己開始寫腳本才想起來。沒指定數量就開兩個。
- 使用者 2026-08-30 另有裁示「盡量把工作量押給 codex gpt」，所以**助手優先用 codex 線**
  （不編團隊，終局直接進 `inbox/new/`），需要頻繁來回才用 Claude subagent。
- **外包**：資料檔合併、驗收腳本、跑測試、查 git 狀態、把已定結論落成文字、文件格式與連結修補。
- **留給自己**：仲裁兩隊互相矛盾的宣告、資源／鎖的分配、範圍裁定、對使用者說話。
  （即使仲裁需要地面真相，探測也可以叫助手跑完回報，我只做判斷。）
- 別過度修正成「什麼都不碰」——[[dont-inflate-light-preferences]]。判準是
  **「這件事需要我的判斷，還是只需要有人動手」**。

**2026-08-30 使用者又重申一次**：「記住，**盡量把事情都押給 codex gpt**。」——
他在同一天說第二次，代表第一次之後我還是押得不夠。**重申＝我做得不夠，不是他忘了說過。**

還在燒 Claude 的地方，按份量排序：① **每個團隊的 Opus 領導**（今天開了 8 個團隊，
`zh` 那個還因 context 用完換了第二棒）；② 我自己寫 orders 與仲裁。
可以改的：**不是每件事都要開「團隊」**——單一、有界、驗收寫得死的工作
（實機驗收、跑一支工具、產一份報告）**直接開 codex 線掛在 dispatcher 底下就好**，
不必配一個 Opus 領導。開團隊的門檻是「要不要有人替我監看與核驗多條線」，不是「這件事重不重要」。

相關：[[im-dispatcher-codex-implements]]（同一件事的舊版，那條講的是不要深潛實作；
這條補上「而且你有助手可以用」）、[[model-tiers-and-headcount]]、[[trust-gpt-sol-more]]。

### 2026-08-30 他說了**第三次**——所以規則要變成預設值，不是提醒

第一次：「盡量把工作量都押給 codex gpt，sol／terra／luna 都可以。」
第二次：「記住，盡量把事情都押給 codex gpt。」
第三次：「盡量把工作都交給 codex。」

**說三次＝我每次都只改一點點，沒有改預設。** 我的實際行為是：
每接到一個需求就 `Agent(subagent_type=general-purpose, model=opus)` 開一個領導，
一輪下來開了七個 Opus（fix／bikini／purge／disabled／inv2／vig／scrn），
而同期純 codex 線（`cx-ops1`／`cx-kern1`／`cx-diag1`）做得一樣好——
**`cx-diag1` 還是定位出當天崩潰根因的那一條。**

**新預設（從這裡開始照這個做）**：

- **預設就是「開一條 codex 線掛在 dispatcher 底下」**，像 `cx-ops1`／`cx-diag1` 那樣：
  我寫交接書 → `tmux new-session` ＋ `send-keys 'codex'` → 它自己跑 → `inbox_send.sh` 回報。
  **不編團隊、不配 Opus 領導。**
- **只有同時滿足這兩條才開 Opus 領導**：① 真的需要 **3 條以上並行線同時被監看**；
  ② 判斷內容是非機械的（要仲裁、要改判、要跨線調和）。
  單一有界任務（改文件、查一個 mod、跑一支工具、產一份報告）**一律 codex 線**。
- 使用者說「開團隊」時，**那是指「別自己做」，不是指「一定要配 Opus」**——
  codex 線也是團隊的一種。若他要的是多線並行，再開領導。

相關：[[model-tiers-and-headcount]]、[[im-dispatcher-codex-implements]]、[[trust-gpt-sol-more]]。

2026-08-31 再次申誡:「你盡量不要做事」——交接書撰寫、tmux 發射驅動、巡線放行、inbox 轉信全部外包給常駐助手 cx-ops(standing 契約在 agentctl/handoffs/ops-2026-08-31/STANDING.md);頂層只留對話/仲裁/範圍/管領導 context。

## fable-top-handles-only-hardest

> 2026-09-09 使用者裁示「你只負責最困難的任務」——Fable 頂層除了調度，只親自做最難的那一件；其餘一律派 Opus／Sonnet／gpt-sol（原 type: feedback）

2026-09-09 19:1x 使用者在 /goal 之後補一句原話：「你只負責最困難的任務」。

**Why:** Fable 是最貴也最聰明的一級（見 [[model-tiers-and-headcount]]）。頂層 context 是最稀缺的資源，
拿來做普通事等於用最貴的人做雜工；他要的是 Fable 的判斷力留給真正卡住、別的模型解不開的問題。

**How to apply:**
- 頂層預設只做：調度、鎖、對使用者說話、artifact 發布——和**唯一一件最難的任務**（例如別隊卡死的真因診斷、跨隊衝突仲裁）。
- 開場先把待辦按難度排，最難的一件留給自己（或在別隊卡住時接手），其餘全派出去：普通→Opus 領隊、簡單→Sonnet、量大呆板→codex gpt-sol（可自開 terra／luna）。
- 「最難」的判準：需要跨多個 mod／層／工具鏈的推理、前一輪已經失敗過一次以上、或後果不可逆。不是「我順手就能做」。
- 這條**加強**而不是取代 [[im-dispatcher-codex-implements]] 與 [[dispatcher-must-use-own-assistants]]。

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
