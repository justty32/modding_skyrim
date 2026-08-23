# Phase 3 — 測試腳本化

> 屬於 [AI 全自動 mod QA 迴圈](README.md)。

## 四、分階段任務（續）


### Phase 3 — 測試腳本化

| # | 任務 | 驗證 |
|---|---|---|
| 3.1 | **✅ PASS（2026-08-02）** 定義 `qa.json`：step 型別 `install` / `uninstall` / `enable` / `disable` / `launch` / `kill` / `load_baseline` / `console` / `wait` / `assert_state` / `handoff_user`（`screenshot` 依 D6 不做） | `client/QA-SCHEMA.md` + `client/examples/smoke.qa.json` |
| 3.2 | **✅ PASS（2026-08-02）** `client/qa_runner.py`：每步 pass/fail 報告（D6 之後不含截圖集） | 見下方「3.x 實測結果」 |

#### 3.x 實測結果（2026-08-02）— runner 首跑就抓到真 bug

`client/qa_runner.py` + `client/QA-SCHEMA.md` + `client/examples/smoke.qa.json`。smoke 全程 **31 秒**：kill → install → launch → 斷言 plugin 已載入 → load baseline → 斷言位置 → `coc` → 斷言酒館內容 → handoff_user → teardown（kill + uninstall），profile 三檔零殘留。

**離場語意（D6 的落地形式）**：`handoff_user` 在 tty 下會停住等人回覆（打字＝失敗原因）；非 tty（agent 呼叫）則記錄訊息、標成 `handoff`、繼續跑完。全綠但有 handoff → 整體 `needs_human`，exit code 2。runner 完全不嘗試自己判斷畫面。

**三個實作時撞到、且都值得寫進 schema 的教訓**：

1. **`/ping` 有回應 ≠ 遊戲可查詢。** `/ping` 跑在 socket thread、載入畫面期間照樣回（這是刻意設計，用來區分「進程活著但忙」與「進程死了」）。launch 之後第一個 `/state` **必定** 503 `game thread did not respond in time`。這讓 smoke 紅了一輪。修正：runner 的 launch step 除了 `/ping` 還要等 `/state`；`mo2ctl launch` 維持只等 `/ping`（它是進程控制工具，這個層級是對的）。
2. **斷言必須可重試。** 遊戲對 console 指令的反應幾乎全是非同步的——`coc` 在 cell 載完前就回、actor value 要隔一幀才生效。單次斷言會把「對了但還沒到」判成失敗。`assert_state` 預設重試到 `retry_for` 秒為止，回報最後一次的實際值。
3. **斷言 `cell_form_id`，不要斷言 `cell`。** 詳見下面那條——這是 runner 首跑抓到的真 bug。

**首跑抓到的真 bug：ModForge 寫 CELL override 不保留 EDID。**

smoke 前兩輪都掛在 `player.cell == "WhiterunBanneredMare"` 回 `""`，但同一次快照裡 `interior: true`、`nearby_actors` 有 Hulda、`cell_form_id: 90206` 全對。手動 probe 完全複現不出來（2 秒就解析出名字）。

變因是**測試 mod 本身**：`ModForgeNavmeshNoop.esp` override 了 `CELL 0x0001605E`（＝90206＝戰友蜜酒館；中途一次進位換算失誤讓我先誤判「這 plugin 沒碰這個 cell」），而且**沒寫 EDID subrecord**。runtime 的 cell 物件取的是勝出記錄的 EditorID，於是名字空了、其他欄位全對。

兩個結論：
- **schema 層面**：load order 裡任何一個 plugin 只要 override 記錄時沒把 `EDID` 帶過去，就能把 EditorID 抹掉。FormID 是引擎身分，抹不掉。所以斷言用 FormID。
- **ModForge 層面**：這是**產生器的缺陷**，不是治具的。純 navmesh 的修改不該讓 cell 掉名字。已另開工作追。

值得直說：這就是 QA 迴圈在第一次真跑時做了它該做的事——受測 mod 改動了沒人打算改的可觀察狀態，而治具抓到了。
