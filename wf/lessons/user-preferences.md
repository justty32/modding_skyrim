# 使用者偏好與邊界

[lessons 索引](README.md)｜偏好的現行表在 [common/user.md](../workflows/common/user.md)，本檔收原話與怎麼照做；怎麼讀他的話與施工節奏見 [user-intent-and-pacing](user-intent-and-pacing.md)。

## send-screenshots-to-session

> 使用者常遠端連線看 session：截圖用 SendUserFile 傳進來、要審批的計畫做成 Artifact 頁，不要只留路徑

2026-09-03 使用者出門中從另一裝置說：「截圖之後可以直接傳到這個 session 讓我看到」；同日補充「我現在是透過 claude code 遠端連線這電腦」，並要求覆核完「產個 artifact 給我審批」。他不在電腦前也會看對話，留在 repo 路徑的截圖他看不到。

**How to apply:**
- 實機驗證產出 png 後，用 `SendUserFile`（status=proactive、display=render）送關鍵幾張，不一次塞全部；同一畫面有明顯變化才重送。
- 需要他拍板的大計畫（如 LoreRim 借用清單）做成 Artifact 審批頁（先載 artifact-design skill），資料用團隊的 summary.json／csv，不在對話裡貼長表。在 aos 樹裡，要他裁的題寄使用者專區（[aos.md](../workflows/aos.md) 第 4 節）。
- 相關：[[user-present-screen-is-still-usable]]、[[verify-game-alive-via-qa-not-ps]]

## notes-agent-minimal-contact

> 2026-09-11 使用者指示：跟同機的 notes agent（Steam 下載那條）沒事別頻繁交流、省 token；聯絡走本機 session 訊息不走 inbox

2026-09-11 使用者原話：「沒事不要跟 notes agent 太頻繁的交流，省點 token」；稍早也說「不用 inbox，直接 message 過去就好」。每則跨 session 訊息兩邊都吃 context。

**How to apply:**
- 只在真的要協調資源時才傳：他要重啟 Steam 而遊戲鎖有人、Steam 跳 Skyrim 更新提示、磁碟／網路快撞上。
- 規矩一次講清楚（Skyrim 489830 不碰、desktop.lock 互斥、game.lock 空才能重啟 Steam），之後不再重申；他的預告／確認類訊息不用回。
- 聯絡用 SendMessage 到本機 session（ListAgents 找名字），不放 `~/notes/inbox/`。相關：[[driving-other-cli-agents]]

## dont-clutter-home-with-agent-output

> 別在 ~/ 亂放東西；真正的交付物進 repo，暫存不落家目錄

2026-08-22 使用者說：「不要在 ~/ 亂放東西=_=」。家目錄是使用者每天在看的地方，不是 agent 的暫存區；線只會照交接書做，規則沒寫進交接書就不會被遵守。

**How to apply:**
1. 交接書預設寫明：報告與交付物進 repo（`agentctl/handoffs/…` 等）；暫存照 [CHOICES](../org/CHOICES.md) 第 7 題三分法放；`~/notes/projects/modding/skyrim/` 只留不進版控的截圖與 MongoDB 快照（[dev-env](../workflows/dev-env.md)）。
2. 要求每條線收工前清掉可重建的中間產物（解包副本、ESP 中間檔、BSA 解出物）；有 build script 加鎖定來源 SHA 的，要隨時重跑得出來。
3. 我自己的暫存一律用 scratchpad，不落到 `~/`。
4. 清理是使用者的決定：刪之前先看、先問。2026-08-22 提清理方案時使用者說「算了，先不動，下次再說」——要主動再提，但仍先問再刪。

相關：[[workspace-layout-and-duties]]、[[im-dispatcher-codex-implements]]、[[push-and-remote-actions]]

## check-clock-dont-estimate-time

> 寫 STATE／交接書的時刻要用 date 查，不要用估的；2026-09-05 憑感覺估的時刻標快 1.5～2 小時，給各線的硬停與等候上限全是虛的

憑感覺推的時刻會偏（2026-09-05 標快約兩小時）。時刻錯了，各線硬停與「等到 13:40 為止」這種上限就失真，領隊會照字面空等或提早收線，事後也對不上紀錄。

**How to apply:** 每次寫時刻前跑 `date '+%H:%M'`；硬停與等候上限用「現在＋N 分鐘」算出來再寫；對帳以檔名或紀錄上的時間戳為準（如 inbox 檔名 `20260905T1219-…`），不以手寫時刻為準。相關：[[codex-tmux-operational-notes]]。

## artifact-republish-needs-read-first

> compact 之後或換了檔案路徑重發既有 artifact，平台會拒絕直到本 session 用 action:read 抓過線上版；大頁 read 一次很貴，重發前先估成本

2026-09-11：Artifact 工具要求本 session 看過線上版才准用 `url` 覆蓋；compact 後這狀態會掉，同 session 內產頁腳本輸出到新目錄也不算「同路徑重發」。沒 read 就重發會被拒、重試多燒 token。成本量級：小頁（名冊 65KB）要 Read 存檔全文約 25k token；大頁（1.9MB 單行 JSON）不必逐行 Read，但 read 一次約 60k token。

**How to apply：**
1. 產頁腳本固定輸出到同一個檔案路徑（例如 `agentctl/handoffs/home-2026-09-08/art/PICK-LOOKS.html`），別每天換目錄；同 session 同路徑重發不用 read。
2. 非同路徑／compact 後重發：先 `action:read url`，小頁再 Read 存檔全文；大頁 read 一次即可，先估 token。
3. 大頁的內嵌資料（縮圖 base64）考慮拆到獨立 assets 或降低內嵌量。

## reply-in-traditional-chinese

> 使用者要求對話回覆用繁體中文；這跟 mod 內容的繁簡偏好是兩回事

2026-08-24 明確要求。回覆、交接書、commit message 主體用繁體中文；技術專名（FormID、submodule、SHA-256、mod／檔名、指令）留原文。現行表見 [user.md](../workflows/common/user.md)「語言」列。

**不要混淆**：這條管我怎麼回話；mod 中文層繁簡都可接受（[[no-cht-chs-preference]]），不要拿這條去堅持 mod 一定要正體。

## top-level-explain-in-plain-words

> 頂層對使用者：使用者很聰明，預設不必翻譯；順手能白話就白話（私心偏好，不是硬規則）；只有他說「今天很累不想動腦」才開助手翻，翻譯太貴時改指出該先看哪些檔案

2026-08-30 使用者定的頂層溝通規則（對應 agentctl/docs/team-model.md 頂層那節），原話（以這句為準）：「使用者也挺聰明，除非他說今天很累不想動腦，不然也不需要翻譯。但私心啦，能順便翻譯成白話還是最好。」

**How to apply**：預設不開翻譯助手、不刻意翻。初見的詞順手給一句白話（成本近零才做，別為此多開 agent 或多花一輪）。使用者明說累了／不想動腦，才開助手（Sonnet）翻；產出大到翻譯本身很貴時，改列「先看 A、再看 B，各看什麼」。這是輕量偏好，照 [[dont-inflate-light-preferences]] 別放大成流程。相關：[[model-tiers-and-headcount]]、[[answer-should-we-with-a-threshold]]、[[reply-in-traditional-chinese]]
