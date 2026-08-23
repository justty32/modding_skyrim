# plan：AI 全自動 mod QA 迴圈（in-game agent bridge）

出計畫日期 2026-08-01。對應 spec：無（由對話直接進 plan，設計決策記在本檔第二節）。

## 目標

建立一條可重複執行的迴圈：**AI 生 mod → AI 裝進 MO2 → AI 開遊戲載入 baseline 存檔 → AI 操控主角 → 依驗證類型分流**：

| 驗證類型 | 誰驗 | 方式 |
|---|---|---|
| 視覺效果（光照、材質、VFX、機位構圖） | **使用者肉眼** | AI 把遊戲開到定位後**通知使用者自己看**（D6 修正：原為 AI 連拍送圖，只在使用者出門時才需要） |
| UI 操作手感 | **使用者親手** | AI **停住並通知使用者**，使用者自己導航與操作（D6 修正：原為 AI 導航到頁面後交還鍵盤） |
| 對話、物品、NPC、quest stage、位置等狀態 | **AI 自己** | 透過 in-game agent bridge 讀結構化狀態 + 下 console 指令 |

## Done when

- [x] Phase 0 三項地基驗證全部有明確結論（通 / 不通 + 證據）。（2026-08-02 全通）
- [x] `agent-bridge` DLL 能在 Proton 內的 Skyrim 進程起 HTTP server，Linux 端 `curl` 拿得到 `/state` 的 JSON、`/console` 能執行 `coc`。（2026-08-02，0.3.0；`/screenshot` 依 D6 移出本條件）
- [x] **（2026-08-02 達成）** `mo2ctl install <mod資料夾>` 能在**不開 MO2 GUI** 的前提下讓一個 ModForge 產物出現在 MO2 並被 Skyrim 載入（用 `/state?include=plugins` 驗證 plugin 生效）。
- [x] 一份 `qa.json` 能跑完「裝 → 開 → 載 baseline → coc → assert → 交棒人工」全程，產出報告。（2026-08-02，smoke 8/8）
- [x] 至少一個既有 ModForge 產物用這條迴圈完成一次驗證。（2026-08-02，`ModForgeNavmeshNoop.esp`）

**不包含**：真·新遊戲流程（Helgen 開場 + 種族選單）自動化、跨機器/遠端執行、把 bridge 送進 Windows CI 出貨、任何給玩家用的產物。

## 現況摘要（2026-08-10）

本計畫的基礎迴圈於 2026-08-02 結案，後續 semantic control 擴充亦已在
AgentBridge 0.6.0 完成實機驗收。現在除了 console/state 之外，AI 還能：

- 列出 current-cell 與四層 ProcessLists 中的 actors；
- 依精確名稱或 runtime reference FormID 定位 actor，並跨 cell 移到其旁；
- 開啟對話、讀取顯示選項，依文字、index 或 TopicInfo FormID 選擇；
- 讀 TESGlobal，並用 retry／`qa_wait` 等待 cell、actor、dialogue 等非同步狀態收斂。

livingNpcs generic anchor/parley 回歸為 **31/31 PASS**；loaded actor、跨
interior/exterior cell、延遲 actor retry 與兩種結構化 dialogue selector 也已逐項通過。
現行 API 與完整驗收證據以 [`projects/agent-bridge/README.md`](../../../../projects/agent-bridge/README.md)
為準。本計畫保留歷史決策與早期分階段紀錄，不再作為 API 清單。

## 三、架構

```
Agent (Linux)
  ├─ ModForge CLI ─────────── spec.json → .esp + mod 資料夾（已有）
  ├─ mo2ctl（新）──────────── 裝 mod / 改 profile / 啟動 / 關閉遊戲
  └─ qa-client ─────────────── bridge.py / qa_runner.py / qa_mcp.py → 127.0.0.1:5099
                                       │
                      ┌────────────────┴────────────────┐
                      │  Skyrim.exe (Proton 9.0-203)    │
                      │   agent-bridge.dll               │
                      │    GET  /state                   │
                      │    POST /console                 │
                      │    POST /actor/*                 │
                      │    POST /dialogue/*              │
                      └──────────────────────────────────┘
```

`agent-bridge` 已定案為 `scene-capture-bridge` 的 **sibling 子專案**（1.1，理由見該列）。上圖的 `/input`、`/screenshot` 依 D6 延後，目前實作的是 `/ping`、`/state`、`/console`。
現行實作另含 `/global`、`/actor/*` 與 `/dialogue/*`；完整 route table 不在歷史計畫重複維護，見子專案 README。

## 五、風險

- ~~**D4 的 loopback 假設不成立** → 最大單點風險~~ → **2026-08-02 已用獨立 Win64 探針證活**（wine 與 Proton/pressure-vessel 兩條都通，見 Phase 0.1a）。備援 `Z:` 共享目錄檔案投遞不需要了。殘留的小風險只剩「在 Skyrim 進程內 bind」與「console exe 自己 bind」的差異。
- **Proton / Wine 不穩**：反覆冷啟動遊戲容易累積 crash。runner 要有 timeout + 強制 kill + 重試。
- **存檔汙染**：baseline 存檔必須唯讀複製後使用，絕不讓自動化流程覆寫原檔。
- ~~**MO2 被同時修改**：遊戲執行中不得改 `mods/` 或 profile 檔；`mo2ctl` 要有互斥檢查。~~ **已處理，且比原本設想的嚴重**：真正的加害者不是遊戲而是 **MO2 本身**——MO2 把 profile 存在記憶體裡，退出／切 profile 時整份寫回，所以在 MO2 執行中改 `modlist.txt` 不會衝突，會在幾分鐘後被**靜默回滾**，無錯誤訊息，症狀只表現為「裝了卻沒載入」。`mo2ctl` 所有寫入類子指令對 **MO2 或遊戲任一在跑**都拒絕執行。
- **無法 headless**：遊戲需要顯示輸出，這條迴圈只能在使用者的桌面 session 跑，不能背景常駐。
- **cross-compile 的 DLL 與 MSVC 產物行為差異**：D3 已接受此風險（內部工具，非出貨物）。

## 六、原始計畫結案（2026-08-02；後續 0.6.0 見頁首摘要）

**Phase 0 / 1 / 2 / 3 全過，Phase 4 依 D6 只剩 handoff 而那已隨 3.2 落地。本計畫無 open 項。**

程式碼與文檔的家：`projects/agent-bridge/`（子專案 README 有 Pitfall 段；`client/QA-SCHEMA.md` 是 qa.json 的權威）。原始結案 commits 為 `50cebe6` / `fb94931` / `a7c5863` / `a1e5f31`；後續已抽成獨立 repo 並 push。

**MCP server 八個 tool 已實機驗完**（現行清單見子專案 README；註冊在
`~/.claude.json`，tool schema 變更要到下一個 session 才會生效）。初版 smoke 的
完整 `qa_run` 約 30 秒；0.6.0 livingNpcs 回歸為 31/31 PASS，收尾後 profile 零殘留。

**首跑抓到的那個 ModForge bug 已修，而且是被這條迴圈自己驗證的**（commit `eb0bb6c`）：`CopyCellEnv` 從來沒複製 `EditorID` → CELL override 讓 vanilla cell 變無名。用修好的產生器重 build `ModForgeNavmeshNoop.esp`，跑一份把 `player.cell == "WhiterunBanneredMare"` 加回斷言的 smoke 變體（即首跑失敗的那條），`pass` 8/8。**但 schema 的建議不變：production spec 仍用 `cell_form_id`**——修的是我們的產生器，任何別人的 mod 漏帶 EDID 都能重演同一件事。

**baseline 存檔組合不預先擴充**（使用者決定）：各 mod 要的測試環境不同，先猜組合是浪費。白漫城外荒野那份（`~/games/skyrim-qa-baselines/`，444）夠用，要新的等實際需要再開。

下次要動這條迴圈，從子專案 README 進去，不用重讀本計畫。

## 本計畫的其他部分

| 檔案 | 內容 |
|---|---|
| [`context.md`](context.md) | 環境事實與設計決策 |
| [`phase-0.md`](phase-0.md) | Phase 0 — 地基驗證 |
| [`phase-1-2.md`](phase-1-2.md) | Phase 1–2 — DLL 與 Linux client |
| [`phase-3.md`](phase-3.md) | Phase 3 — 測試腳本化 |
| [`phase-4.md`](phase-4.md) | Phase 4 — 人工關卡 |
