# 調度、模型分級與交接書（2/9）

[lessons 索引](README.md)｜同主題：[dispatch-and-agents](dispatch-and-agents.md)、[dispatch-and-agents-3](dispatch-and-agents-3.md)、[dispatch-and-agents-4](dispatch-and-agents-4.md)、[dispatch-and-agents-5](dispatch-and-agents-5.md)、[dispatch-and-agents-6](dispatch-and-agents-6.md)、[dispatch-and-agents-7](dispatch-and-agents-7.md)、[dispatch-and-agents-8](dispatch-and-agents-8.md)、[dispatch-and-agents-9](dispatch-and-agents-9.md)

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
