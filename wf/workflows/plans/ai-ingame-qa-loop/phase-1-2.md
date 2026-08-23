# Phase 1–2 — DLL 與 Linux client

> 屬於 [AI 全自動 mod QA 迴圈](README.md)。

## 四、分階段任務（續）


### Phase 1 — Agent Bridge DLL v1

| # | 任務 | 驗證 |
|---|---|---|
| 1.1 | **✅ 已定案（2026-08-02，使用者決定）：開 sibling 子專案；現已抽離為 `projects/agent-bridge/` 獨立 repo/submodule。** 理由：兩者生命週期相反——`scene-capture-bridge` 是人用熱鍵驅動的**創作**工具、與內容一起出貨；`agent-bridge` 是**測試治具**，每次 QA 跑完就卸，絕不能進玩家 load order。把會執行 console 指令的監聽 port 併進創作工具，等於每次做內容都開著那個 port。程式碼複用往反方向走：需要時把 cell 走訪那段搬進 agent-bridge | 子專案已建立並編出 DLL，見 0.1 |
| 1.2 | **✅ PASS（2026-08-02）** `GET /state` 完整欄位，分成「永遠回傳」與「選配」兩層 | 見下方「1.2 實測結果」 |
| 1.3 | **✅ 執行面 PASS，輸出面部分達成（2026-08-02）** `POST /console` 執行任意指令 | 見下方「1.3 實測結果」 |
| 1.4 | **⏸ 延後（D6）** `POST /screenshot`：抓 D3D11 backbuffer 寫 PNG。只有「使用者出門、AI 自己多試幾次留圖」才需要 | Linux 端讀得到 PNG 且內容正確 |
| 1.5 | **✅ PASS（2026-08-02），如預期是 1.3 的附帶結果**：`POST /console {"cmd":"load <存檔stem>"}` 從主選單直接載入 baseline，不需要啟動參數也不需要 bridge 開機動作 | 主選單下發指令，6 秒後 `/state` 回 `WhiterunExterior15` |
| 1.6 | **⏸ 延後（D6）** `POST /input`：送合成輸入事件。使用者在場時自己按更快更可靠 | 能從遊戲中開到 Inventory / MCM 指定分頁 |

### Phase 2 — Linux 端 client

| # | 任務 | 驗證 |
|---|---|---|
| 2.1 | **✅ PASS（2026-08-02）** `mo2ctl`：`install` / `uninstall` / `enable` / `disable` / `launch` / `kill` / `status`，落在 `agent-bridge/client/mo2ctl.py`（純 stdlib） | 見下方「2.1 實測結果」 |
| 2.2 | **✅ PASS（2026-08-02；0.3.0 semantic tools 於 2026-08-10 實測）** `client/qa_mcp.py`，已在 `~/.claude.json` 與 houseCARL 並列註冊。現行 tool 清單見子專案 README | 見下方「2.2 實測結果」與子專案 0.6.0 acceptance |

#### 2.1 實測結果（2026-08-02）— 全程免 GUI 的裝-跑-卸

落點：`agent-bridge/client/mo2ctl.py`。與 DLL 同一個子專案，因為 port 號、`/state` 欄位名、讀它的 client 是同一份合約，兩側要能一次 commit。純 stdlib：QA 治具自己還要先裝環境才能跑，就會沒人用。

**完整迴圈（對真實 109-mod load order，全程沒開 MO2 GUI）**：

1. `install ModForge/out/ModForgeNavmeshNoop.esp --name QaNoop`
2. `launch` → `protontricks-launch --appid 489830 <MO2>/ModOrganizer.exe moshortcut://:SKSE`，30 秒後 `/ping` 回應
3. `GET /state?include=plugins` → `{"name":"ModForgeNavmeshNoop.esp","index":26}` ← **驗收條件達成**
4. `POST /console {"cmd":"load <baseline>"}` → `/state` 回 `WhiterunExterior15`
5. `kill --mo2`、`uninstall QaNoop`
6. `modlist.txt` / `plugins.txt` / `loadorder.txt` 三份**與安裝前 byte-identical**

第 6 步才是關鍵：會在 profile 裡留殘渣的迴圈只能跑一次。

**新增 `/state?include=plugins`（AgentBridge 0.4.0）**。原計畫寫「用 `/state` 驗證 plugin 生效」但 `/state` 當時沒有任何 plugin 欄位，驗收條件無法成立，所以補上。回的是**引擎實際解析出來的 load order**——`plugins.txt` 說的是要求，這個說的是結果（MO2 的 VFS、缺 master、esl 佔位都會改變它）。`index` 就是 FormID 實際帶的那個 byte（full `0x00`–`0xFD`、light `0xFE000`+）。實作走 `GetLoadedMods()`／`GetLoadedLightMods()` 存取器而非直接寫 `compiledFileCollection`：後者在 NG 多 runtime build 下藏在 runtime-specific layout 後面，寫了不能編。

**三個計畫沒寫、實作時才撞到的環境事實**：

- **profile 三個檔的換行符不一致**：`modlist.txt`／`loadorder.txt` 是 CRLF，`plugins.txt` 是 LF。同一個目錄、同一支程式寫的。統一normalize 不是無害操作，而先前手動改 modlist 時 `sed 's|^+AgentBridge$|...|'` 對 CRLF 內容靜默匹配不到、看起來成功其實沒改，就是同一個坑。`mo2ctl` 每次讀檔都把該檔自己的換行符帶著走。
- **MO2 執行中改 profile 會被靜默回滾**（詳見上面五、風險那條）。原計畫只把「遊戲在跑」列為互斥條件,實際上 MO2 才是真正會咬人的那個。
- **進程比對必須認 `argv[0]`，不能全命令列 substring**：`protontricks-launch --appid 489830 .../ModOrganizer.exe moshortcut://:SKSE` 的參數裡就有 MO2 的路徑,substring 比對會把 launcher、它的 wrapper、它的 python 父程序都算成 MO2——實測一個 MO2 被數成五個。反方向也錯:`SkyrimSELauncher.exe` 那條 Steam/Proton 鏈整個 session 都活著,比對太鬆會讓遊戲看起來永遠在跑、互斥鎖永遠打不開。另外全程讀 `/proc` 不用 `pkill -f`——本專案已經被自己的 pattern 殺掉過兩次 shell。

#### 2.2 實測結果（2026-08-02）— MCP server

`client/qa_mcp.py`，手寫 JSON-RPC over stdio（不引 `mcp` 套件，維持 client/ 全 stdlib）。已寫進 `~/.claude.json` 的 `mcpServers`，與 `housecarl` 並列，`env` 帶 `MO2_ROOT` / `MO2_PROFILE`。**要下一個 session 才會生效**——MCP server 是啟動時連的。

**暴露語意讀寫工具，刻意不暴露生命週期操作。** 初版四個是 `qa_status` /
`qa_state` / `qa_console` / `qa_run`；0.3.0 再加入 `qa_actor` / `qa_dialogue` /
`qa_global` / `qa_wait`。仍然**不給 `install` / `uninstall` / `launch` / `kill`**：
這四個各自只是一行 Bash、一個 session 用不到幾次，而真正頻繁、真正值得走
MCP 的是 state 與 semantic action。讓模型能用一次 tool call 就終結使用者的遊戲
session，是比「要它自己打指令」更差的人機介面。`qa_run` 仍然會做完整套，但那
是從一份使用者可以先讀過的 qa.json 來的。

**stdio 的唯一鐵律：stdout 只能有協議流量。** 一個誤觸的 `print()` 就會汙染串流，client 端只會看到連線莫名斷掉。兩個由此而來的實作決定：`qa_run` 強制 `interactive=False`（runner 在這裡卡在 `input()` 會讓 server 整個吊死且沒人回得了）；notification（沒有 `id` 的訊息，例如 `notifications/initialized`）一律不回應——對 notification 回應是協議違規，有些 client 會直接斷線。

驗證：腳本化 handshake 跑過 initialize / tools/list / ping / 四個 tool / 未知 tool / 未知 method / 壞 JSON，每一行 stdout 都是合法 JSON-RPC、stderr 全乾淨；再用註冊檔裡那條命令原封不動從 `/` 這個無關 cwd 跑一次確認（`qa_run` 的相對路徑是相對 script 目錄解析的，所以照樣通）。
