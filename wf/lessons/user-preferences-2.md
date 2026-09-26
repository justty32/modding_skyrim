# 使用者偏好與邊界（2/2）

[lessons 索引](README.md)｜同主題：[user-preferences](user-preferences.md)

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
