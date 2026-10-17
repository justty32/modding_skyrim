# 使用者偏好與邊界

[lessons 索引](README.md)

## send-screenshots-to-session

> 使用者常遠端連線看 session：截圖用 SendUserFile 傳進來、要審批的計畫做成 Artifact 頁，不要只留路徑（原 type: feedback）

2026-09-03 早上使用者出門中從另一裝置跟 session 說：「截圖之後可以直接傳到這個 session 讓我看到」。

**Why:** 他不在電腦前也會看這個對話；截圖留在 repo 路徑他看不到，傳進來才有用。

**How to apply:**
- 實機驗證（rt 隊）產出 png 後，用 `SendUserFile`（status=proactive、display=render）送關鍵幾張（天賦樹、對話、新 mod），不要一次塞全部。
- 同一畫面只送一次；有明顯變化才重送。
- 2026-09-03 09:15 使用者補充「我現在是透過 claude code 遠端連線這電腦」並要求覆核完「產個 artifact 給我審批」：需要他拍板的大計畫（如 LoreRim 借用清單）做成 Artifact 審批頁（先載 artifact-design skill），資料來源用團隊的 summary.json／csv，不要在對話裡貼長表。
- 相關：[[user-present-screen-is-still-usable]]、[[verify-game-alive-via-qa-not-ps]]

## notes-agent-minimal-contact

> 2026-09-11 使用者指示：跟同機的 notes agent（Steam 下載那條）沒事別頻繁交流、省 token；聯絡走本機 session 訊息不走 inbox（原 type: memory）

2026-09-11 使用者原話：「沒事不要跟 notes agent 太頻繁的交流，省點 token」；稍早也說「不用 inbox，直接 message 過去就好」。

**Why:** 每則跨 session 訊息兩邊都要吃 context；禮貌性回覆、重複確認都是浪費。

**How to apply:**
- 只在**真的要協調資源**時才傳：他要重啟 Steam 而我們遊戲鎖有人、Steam 跳 Skyrim 更新提示、磁碟／網路快撞上。
- 規矩一次講清楚（Skyrim 489830 不碰、desktop.lock 互斥、game.lock 空才能重啟 Steam），之後不再重申。
- 收到他的預告／確認類訊息**不用回**。
- 聯絡方式：SendMessage 到本機 session（ListAgents 找名字），不放 `~/notes/inbox/`。
相關：[[driving-other-cli-agents]]、[[aetheria-agent-coexistence]]

## dont-clutter-home-with-agent-output

> 別在 ~/ 亂放東西；codex 線的產出會失控膨脹，真正的交付物要進 ~/notes（原 type: feedback）

2026-08-22 使用者說：「不要在 ~/ 亂放東西=_=」。

當天我一口氣派了七八條 codex 線，每條都讓它把報告、解包出來的 archive、
ESP 工作副本、runtime 截圖全堆在自己的 `~/skyrim_agent_out/codex-*/` 裡，
而且沒有要求收工清理。結果 `~/skyrim_agent_out` 長到 **1.6 GB**、一天動 1,452 個檔案、
底下攤著 19 個 `codex-*` 目錄。

**Why**：家目錄是使用者每天在看的地方，不是 agent 的暫存區。
而且這個 repo 早就有既有慣例——報告與交付物歸 `~/notes/projects/modding/skyrim/`
（`logs/`、`artifacts/`、`qa/`、`docs/`）。那天八條線只有 `codex-pandora`
一條做對，把報告寫進 `notes/.../logs/` 並 push。是我沒把規則寫進交接書。

**How to apply**：
1. 交接書預設就要求：**報告與決策文件寫進 `~/notes/...`**，
   `~/skyrim_agent_out/codex-*/` 只留 handoff 與小的證據檔
2. 要求每條線**收工前自己清掉可重建的中間產物**——
   解包副本、ESP 中間檔、BSA 解出來的東西。
   有 build script 加鎖定來源 SHA 的，要用隨時重跑得出來
3. 我自己的暫存一律用 scratchpad，不要落到 `~/`
4. 清理是使用者的決定：**刪之前先看、先問**。
   2026-08-22 我提了清理方案，使用者說「算了，先不動，下次再說」——
   下次要主動提起，但仍然先問再刪

相關：[[workspace-layout-and-duties]]、[[im-dispatcher-codex-implements]]、
[[push-and-remote-actions]]

## check-clock-dont-estimate-time

> 寫 STATE／交接書的時刻要用 date 查，不要用估的；2026-09-05 我連續兩小時把時間標快 1.5～2 小時，導致給各線的硬停與等候上限全是虛的（原 type: feedback）

2026-09-05 家中場：我在 STATE.md 與交接書裡寫的「13:05、13:20、14:30」全是憑感覺推的，實際 `date` 只到 12:28；inbox 檔名的時間戳（`20260905T1219-…`）才是對的。

**Why:** 時刻錯了，各線硬停（14:30／15:30）與「等到 13:40 為止」這種上限就失真，領隊會照字面時間空等或提早收線；事後對帳也對不上 inbox。
**How to apply:** 每次寫時刻前跑 `date '+%H:%M'`；硬停與等候上限用「現在＋N 分鐘」算出來再寫；對帳一律以 inbox 檔名為準。相關：[[codex-tmux-operational-notes]]。

## artifact-republish-needs-read-first

> 2026-09-11 實測：compact 之後或換了檔案路徑重發既有 artifact，平台會拒絕直到本 session 用 action:read 抓過線上版；小頁還要 Read 完存下來的全文（名冊 65KB≈25k token），換臉挑選頁 1.9MB 的單行 JSON 不必逐行 Read 但 read 一次就要 ~60k token。重發前先估成本。（原 type: feedback）

2026-09-11 晚上重發換臉挑選頁（1.9MB）與隨從名冊（65KB）各被拒兩次才成功，多燒約 80k token。

**Why：** Artifact 工具要求「本 session 看過線上版」才准用 `url` 覆蓋；compact 後這個狀態會掉，而且同一 session 內若產頁腳本輸出到**新目錄**，就不算「同檔案路徑重發」。

**How to apply：**
1. 產頁腳本固定輸出到**同一個檔案路徑**（例如 `agentctl/handoffs/home-2026-09-08/art/PICK-LOOKS.html`），別每天換目錄；同 session 同路徑重發不用 read。
2. 非同路徑／compact 後要重發：先 `action:read url`，小頁再 Read 存檔全文；大頁（單行 JSON）read 一次即可，但要先估 token。
3. 大頁的資料（縮圖 base64）考慮拆到獨立 assets 或降低內嵌量，讓 read 成本降下來。

## reply-in-traditional-chinese

> 使用者要求對話回覆用繁體中文；這跟 mod 內容的繁簡偏好是兩回事（原 type: feedback）

跟使用者對話一律用**繁體中文**回覆（2026-08-24 明確要求）。

**Why:** 他讀中文比較快，而且這條線的文件（`AGENTS.md`、`WAIT_USER.md`、交接書、
session-log）本來就全是中文寫的，回覆換成英文等於每次都要他做一次語言切換。

**How to apply:** 回覆、交接書、commit message 主體都用繁體中文。技術專名
（FormID、submodule、SHA-256、mod／檔名、指令）維持原文不要硬翻。

**注意不要混淆**：這條講的是**我怎麼回話**。[[no-cht-chs-preference]] 講的是
**mod 中文層**——那邊繁簡都可接受，不要拿這條去推翻它、去堅持 mod 一定要正體。

## top-level-explain-in-plain-words

> 頂層對使用者：使用者很聰明，預設不必翻譯；順手能白話就白話（私心偏好，不是硬規則）；只有他說「今天很累不想動腦」才開助手翻，翻譯太貴時改指出該先看哪些檔案（原 type: feedback）

2026-08-30 使用者定的頂層溝通規則（對應 agentctl/docs/team-model.md 頂層那節）：

- 頂層 agent 直接跟使用者對接，說的東西要**適合使用者理解**；**使用者初次見識的東西最好先用白話說明**，別直接丟術語與內部代號。
- 頂層通常很貴，所以**可以開助手 agent（Sonnet）把技術產出翻譯成使用者聽得懂的話**——這也是頂層「私人助手」的正當用途之一。
- 但要分情況：**有時光是翻譯就會吃掉一大堆 context，反而更貴**。這時候不翻，改成**直接跟使用者指出「應該先去看哪些檔案」**，讓他自己讀。

**Why**：頂層是使用者的唯一介面；聽不懂＝白花一輪；但翻譯是 token 密集的活，硬翻大產出會把頂層的 context 燒掉。

**同日修正**：「使用者也挺聰明，除非他說今天很累不想動腦，不然也不需要翻譯。但私心啦，能順便翻譯成白話還是最好。」

**How to apply**：預設**不開翻譯助手、不刻意翻**——使用者讀得懂技術產出。初見的詞順手給一句白話（成本近零就做，別為此多開 agent 或多花一輪）。只有使用者明說累了／不想動腦，才啟動助手翻譯；那時若產出大到翻譯本身很貴，改列「先看 A、再看 B，各看什麼」。這是輕量偏好，照 [[dont-inflate-light-preferences]] 別放大成流程。相關：[[model-tiers-and-headcount]]、[[answer-should-we-with-a-threshold]]、[[reply-in-traditional-chinese]]

## dont-inflate-light-preferences

> 使用者的輕量偏好不要膨脹成設計指令;他說「不要懲罰我喝藥」是排除條件,不是「圍繞鍊金建 build」（原 type: feedback）

2026-08-21 同一天犯了兩次同樣的錯：**把使用者的一句輕量偏好，放大成一條全面的設計原則。**

**案例一**：他說「像這種非遊玩內容，**如果很難做**漢化那就不用做，英文我也是看得懂的」。
我解讀成「非遊玩內容一律維持英文」。他隨後補「做了就做了，沒關係，中文選單也是很舒服」——
才發現重點在**成本**不在類別。

**案例二**：他說「我想要狂喝藥」。我把它當成 build 方向，寫了五條設計約束（Apothecary 變成
build 核心、天賦系統改用鍊金樹當選擇依據、推薦一堆喝藥 QoL mod、附魔立石偏向鍊金路線）。
他澄清：「呃，沒關係的，我的意思只是希望**不要懲罰我喝藥**就好」——那只是一條**排除條件**。

**Why:** 他講話是隨口的、資訊量小的。我把它當成需求規格去展開，結果是**替他做了他沒做的決定**，
而且會讓 agent 往錯的方向花時間。放大偏好比忽略偏好更糟，因為它看起來像在服務他。

**How to apply:**
- 一句輕描淡寫的話，預設是**一條約束**或**一個偏好**，不是一個方向。
- 要展開成設計決策前，先問自己：**這是他說的，還是我推論的？** 推論的部分要標明是推論，
  或直接問他一句。
- 特別警覺這兩種放大：**「不要 X」→「要最大化反 X」**、**「X 很難就算了」→「X 一律不做」**。
- 他澄清時不要辯解，直接縮回並把已經派出去的指令修正掉。

相關：[[translation-layer-cost-threshold]]、[[trust-gpt-sol-more]]

## answer-should-we-with-a-threshold

> 使用者問「看要不要做 X」時，別只回「不必」；給可執行的判準讓他挑（原 type: feedback）

2026-08-23：使用者問「工作流這邊，看要不要做重構，整個做整理拆檔」。我評估後回
「**沒有拆檔**——最大的檔 34K，是詳細實作計畫的正常尺寸」。他下一句就是
「做拆檔重構，wf 中的檔案若超過 8kb 就拆」。

**Why:** 他會問「要不要」，通常是**已經覺得不對勁**，只是還沒定出線在哪。回一句
「不必」等於把判準留在我腦裡，他沒東西可以反駁或修改，只好直接下命令——白花一輪。
注意這跟 [[dont-inflate-light-preferences]] 不衝突：那條講的是**別把隨口一句放大成方向**；
這條講的是**他直接問我的時候，要給他可以挑的東西**。

**How to apply:** 回答「要不要做 X」時，附上具體判準與它會造成的結果，讓他改數字就好。
例如「以 8KB 為線的話會拆 5 份、以 20KB 為線只拆 2 份，我傾向不拆因為…」。
真心認為不必做，也要說清楚**什麼條件下就該做**。不要只給結論。

## investigate-all-then-install-once

> 大流程是「各類 mod 全部調查完 → 總結成一份安裝清單 → 才開始施工」，不要每查完一個小 mod 就裝一次（原 type: memory）

2026-08-27 使用者定調整個 modding 流程的節奏：

> 先調查完各類 mod、並總結出需要安裝的東西後，再來開始。不然每調查完一個小 mod
> 就開始安裝測試，那個上下文切換很麻煩。

**Why**：下載／安裝／實機驗證本身是**被允許的**（使用者同時放行了下載、安裝、碰 MO2、實機），
所以擋住施工的不是權限，是**節奏**。逐件施工會逼使用者在「查資料」與「顧遊戲」之間反覆切換，
那個成本落在他身上，不是落在 agent 身上。

**How to apply**：
- 調查線可以一直開，但**產出一律是清單與判定，不是施工動作**。
- 施工要攢成一次：等各類調查都收斂，合併成**單一份**安裝／驗收計畫再動手。
- 別把「已授權」誤讀成「現在就可以做」——[[dont-inflate-light-preferences]] 的反面同樣成立：
  授權是解除禁令，不是下達指令。
- 驗收清單也要合併，不要每條線各開一份（見 [[im-dispatcher-codex-implements]] 的分工）。

相關：[[launch-skyrim-via-steam]]（真的要實機時的啟動方式）、[[answer-should-we-with-a-threshold]]
