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

## 一、環境事實（2026-08-01 實查，規劃基於這些前提）

| 項目 | 事實 | 來源 |
|---|---|---|
| Skyrim SE | `~/.local/share/Steam/steamapps/common/Skyrim Special Edition`（AE，appid 489830） | `appmanifest_489830.acf` |
| 執行層 | **Proton 9.0-203** | `~/.local/share/Steam/steamapps/compatdata/489830/version` |
| SKSE | `skse64_loader.exe` + `skse64_1_6_1170.dll`，runtime 鎖 **1.6.1170** | 遊戲根目錄 `find` |
| MO2 | `~/games/mod-organizer-2-skyrimspecialedition/modorganizer2/ModOrganizer.exe`，**跑在遊戲自己的 Proton 9 prefix 內**（`compatdata/489830/pfx`），與 Skyrim 共用同一個 wine session（usvfs 要求如此） | 2026-08-02 重查，見下方「MO2 啟動鏈」 |
| MO2 啟動鏈 | `mo2installer`（`~/dev/mo2installer`，furglitch/modorganizer2-linux-installer）把遊戲目錄的 `SkyrimSELauncher.exe` **換成 redirector**（253752 bytes，原檔備份為 `_SkyrimSELauncher.exe`），redirector 讀同目錄的 `modorganizer2/instance_path.txt` 轉呼叫 `ModOrganizer.exe`。所以日常啟動就是 Steam 的 Play 鈕 / `steam steam://rungameid/489830`，沒有獨立 wrapper script | 檔案大小比對 + `instance_path.txt` + `.desktop` 的 `Exec=` |
| 系統 wine-11.13 | **與 Skyrim/MO2 無關**（pacman 套件，prefix `~/.wine`，`find` 該 prefix 無任何 skyrim/modorganizer 命中）。先前計畫誤記為「MO2 跑在這套上」，2026-08-02 更正 | `pacman -Qi wine`、`find ~/.wine/drive_c` |
| 在遊戲 runtime 內跑測試 exe | `protontricks-launch --appid 489830 <exe>`（protontricks 已安裝於 `/usr/bin`）；等效手動式見 0.1a。**不可**用系統 `wine <exe>`，那會落在無關的 `~/.wine` | agent 調查 |
| MO2 現況 | 單一 profile `Default`，111 個 mod 資料夾，`plugins.txt` 44 行、42 個 active | 現場 `ls` / `grep -c` |
| 顯示 session | **Wayland**（`XDG_SESSION_TYPE=wayland`） | 現場 |
| 截圖工具 | grim / scrot / maim **都沒裝**；ffmpeg 有 | 現場 |
| 輸入工具 | xdotool 有（Wayland 下對非 XWayland 視窗基本無效）；ydotool / wmctrl 沒裝 | 現場 |
| .NET | SDK 10.0.110、8.0.129 | `dotnet --list-sdks` |
| 既有 QA 素材 | `projects/ModForge/sub_projs/scene-capture-bridge/`：SKSE C++23 DLL，已有 console 指令系統、cell placed-ref 走訪、scene.json 匯出 | 該子專案 README |
| Linux cross-compile | `my_skyrim_plugin_1` 的 `release-clang-cl-linux` preset（clang-cl + lld-link + xwin）**實測產出過可用 DLL**：`build/release-clang-cl-linux/DaylightDungeon.dll`（PE32+ DLL，1.1M，2026-06-06） | `file` 輸出 |

**兩個對不上的地方（未處理，留給 notes 側）**：
- `dist/mods`、`dist/plugins` 皆為空，實際產物散在 `~/skyrim_mods/mine/`。
- `~/notes/projects/modding/skyrim/` 記的已部署自製 mod 名稱，與 MO2 現場的三個 `*_backup` 資料夾對不上（notes 可能停在 2026-07-17）。部署狀態歸 notes 管，本 repo 不代改。

## 二、已定案的設計決策

### D1：不走 OS 層自動化，把眼睛和手放進遊戲進程

Wayland + 無截圖工具 + xdotool 受限 + Proton 隔離 → 「截螢幕 + 模擬鍵盤」這條路脆弱且不可重現。

改為：**一支 SKSE C++ DLL 當 agent bridge，開 localhost HTTP**。
- 截圖 → DLL 抓 D3D11 backbuffer 寫 PNG（ENB / ScreenshotUtility 的做法），完全繞開 Wayland。
- UI 導航 → DLL 送合成輸入事件給遊戲自己的 input handler，不需要 OS 層。

**基礎已有一半**：`scene-capture-bridge` 已經是 SKSE C++23 DLL，有 console 指令系統、會走訪 cell 的 placed refs 讀 base + world transform + enable state、會匯出 JSON 餵回 ModForge `build`。缺的只是「對外開 socket」與「螢幕擷取」。

### D2：「開新檔」＝ baseline 存檔（使用者 2026-08-01 確認）

真·新遊戲要過 Helgen 開場 + 種族選單，自動化慢且脆。改為**維護一組 baseline 存檔**（過完開場，不同等級/地點各一份），bridge 啟動時自動載入指定存檔。

- **使用者後續會提供 baseline 存檔的組合建議**（要哪些地點/等級/裝備狀態）。在那之前先用單一「過完開場、白漫城外」的存檔開發。
- 真要「純淨新檔」時，另外裝 Alternate Start 類 mod 跳開場，不列入本計畫。

### D3：QA bridge 的 DLL 直接用 Linux cross-compile 出貨（使用者 2026-08-01 確認）

`my_skyrim_plugin_1` 的 preset 註明「compile-verification only，正式 DLL 走 Windows CI」，但**這條路使用者已實測可用**，且 QA bridge 是內部工具、不是給玩家的產物 → **直接用 `release-clang-cl-linux` 產出可用 DLL，不進 Windows CI**。迭代速度優先。

### D4：傳輸走 localhost TCP（HTTP + JSON）

Wine 的 winsock 走 host socket，Proton 的 pressure-vessel 預設共用 network namespace → Linux 進程連得到遊戲裡的 loopback。Mantella 在 Linux 上就是這樣跑的（協定形狀見 `analysis/skyrim_engine/answers/mantella-analysis.md`、`src/http/routes/mantella_route.py:65-102`）。

**這是整條路的地基假設，Phase 0 第一件事就是實測它。** 若不通，備援是共享目錄的檔案投遞通道（透過 Wine 的 `Z:` drive），但延遲與複雜度都會上升。

### D5：MO2 不開 GUI

裝 mod ＝ 複製資料夾進 `mods/` + 寫 `meta.ini` + 改 `profiles/Default/modlist.txt` 與 `plugins.txt`。啟動遊戲 ＝ `ModOrganizer.exe "moshortcut://:SKSE"`。Phase 0 驗證這條可行。

### D6：截圖與合成輸入降級為「使用者不在場」才需要的功能（使用者 2026-08-02 決定）

原計畫把「視覺驗證」與「UI 手感驗證」當成兩個要建的能力（1.4 截圖、1.6 合成輸入、4.1 連拍比對、4.2 導航後交棒）。使用者指出這個前提站不住：**做 mod 的時候人基本上都在電腦前**，AI 直接叫他看就好，不需要 AI 代拍代看；要導航到某個 UI 頁面，他自己按比 AI 送合成事件快也可靠。

截圖真正有用的只有兩種情境，而且**都以「使用者出門」為前提**：

1. 出門時 AI 自己多做嘗試，把各次結果拍下來，回家後一次看幾張。
2. 餵給多模態 AI 判斷——但使用者認為目前的多模態 AI 還不夠成熟，而且這同樣只有出門時才需要。

**影響**：
- **1.4（截圖）、1.6（合成輸入）、4.1、4.2 全部降到最後**，等「離場模式」真的要做時再回頭。不是取消，是排序後移。
- 表格第一節那個「三類驗證分流」仍然成立，但**第一、二類（視覺、UI 手感）的實作方式改成「AI 停下來通知使用者，使用者自己看/自己按」**，不需要任何新能力——`/state` 加上一則通知就夠了。
- **接下來的重心是 Phase 2 與 Phase 3**：`mo2ctl` 與 MCP server 讓迴圈可用，`qa.json` runner 讓它可重複。這兩件事才是「AI 能自己跑完一輪」的瓶頸。

## 三、架構

```
Claude (Linux)
  ├─ ModForge CLI ─────────── spec.json → .esp + mod 資料夾（已有）
  ├─ mo2ctl（新）──────────── 裝 mod / 改 profile / 啟動 / 關閉遊戲
  └─ qa-client（新）────────── bridge.py / qa_runner.py → 127.0.0.1:5099（MCP 包裝待做＝2.2）
                                       │
                      ┌────────────────┴────────────────┐
                      │  Skyrim.exe (Proton 9.0-203)    │
                      │   agent-bridge.dll               │
                      │    GET  /state                   │
                      │    POST /console                 │
                      │    POST /input                   │
                      │    POST /screenshot              │
                      └──────────────────────────────────┘
```

`agent-bridge` 已定案為 `scene-capture-bridge` 的 **sibling 子專案**（1.1，理由見該列）。上圖的 `/input`、`/screenshot` 依 D6 延後，目前實作的是 `/ping`、`/state`、`/console`。

## 四、分階段任務

### Phase 0 — 地基驗證（先做這個；三項任一不通，後面的形狀就要改）

| # | 任務 | 驗證 |
|---|---|---|
| 0.1a | **✅ PASS（2026-08-02）** 先與 SKSE 脫鉤單驗 D4：獨立 Win64 console exe（mingw-w64 GCC 16.1.0 + winsock2）bind `127.0.0.1:5099` | 見下方「0.1a 實測結果」 |
| 0.1 | **✅ PASS（2026-08-02）** 用 `release-clang-cl-linux` preset 編出 `agent-bridge/build/release-clang-cl-linux/AgentBridge.dll`（PE32+ x86-64，1.1M，`SKSEPlugin_Load`/`_Query`/`_Version` 匯出齊全），含 `GET /ping` 與 `GET /state` 最小 stub | 見下方「0.1–0.3 實測結果」 |
| 0.2 | **✅ PASS（2026-08-02）** SKSE 載入 cross-compile 出來的 DLL，遊戲進程內成功 bind | 同上 |
| 0.3 | **✅ PASS（2026-08-02）** 全程沒開 MO2 GUI：建 `mods/AgentBridge/` + `meta.ini` + `modlist.txt` 插一行 | 同上 |
| 0.4 | **✅ 完成（2026-08-02）** 使用者產出第一份 baseline，唯讀主檔放 `~/games/skyrim-qa-baselines/`（444，含 README） | 見下方「0.4 baseline 存檔」 |

#### 0.1a 實測結果（2026-08-02）— D4 loopback 成立

探針原始碼與產物：`<scratchpad>/loopback-probe/probe.{c,exe}`（Phase 1.1 決定 agent-bridge 落點後搬進該子專案）。
編譯：`x86_64-w64-mingw32-gcc -O2 -o probe.exe probe.c -lws2_32`（刻意 bind `INADDR_LOOPBACK` 而非 `INADDR_ANY`，要驗的就是 loopback 這條路）。

| 執行層 | 指令 | 結果 |
|---|---|---|
| 系統 wine-11.13（＝MO2 用的那套版本） | `WINEPREFIX=<scratch> wine ./probe.exe 5099` | **PASS**，Linux 端 `curl 127.0.0.1:5099` → `{"ok":true,"who":"windows-probe"}` |
| Proton 9.0-203 + SteamLinuxRuntime_sniper（pressure-vessel 容器） | `STEAM_COMPAT_CLIENT_INSTALL_PATH=~/.local/share/Steam STEAM_COMPAT_DATA_PATH=<scratch>/protoncompat <sniper>/run-in-sniper -- "<Proton 9.0 (Beta)>/proton" run probe.exe 5099` | **PASS**，同上 |

Proton 那組的關鍵佐證（排除「其實是前一個 wine 探針在回話」）：`ss -ltnp` 顯示監聽者是 `Proton 9.0 (Beta)/files/bin/wineserver`，祖先鏈 `wineserver ← pv-adverb ← srt-bwrap`，確實在容器內；容器外的 curl 仍拿得到回應。

**結論**：pressure-vessel 預設共用 network namespace 的假設成立，`agent-bridge` 可以走 HTTP over localhost，五節風險表的「最大單點風險」解除。備援（`Z:` 共享目錄檔案投遞）不需要了。

**尚未驗的部分**：上述是 console exe 自己 bind；SKSE DLL 在 Skyrim 進程內 bind 是否同樣通，要等 0.1/0.2。理論上同一個 wineserver、同一條路，但 Skyrim 進程的 winsock 初始化時機與 ENB/其他 SKSE plugin 的干擾未測。→ **0.2 已補驗，通。**

#### 0.1–0.3 實測結果（2026-08-02）— 一次全過

安裝方式（＝0.3 的驗證）：全程沒開 MO2 GUI，只做三件事——`mods/AgentBridge/SKSE/Plugins/AgentBridge.dll`、`mods/AgentBridge/meta.ini`、`profiles/Default/modlist.txt` 第 2 行插 `+AgentBridge`（第 1 行是 MO2 的標頭註解，必須留著；modlist 是「上面＝高優先權」）。純 SKSE plugin 沒有 esp，**不用動 `plugins.txt`**。備份留在 `modlist.txt.bak-before-agentbridge`。

使用者從 Steam 啟動（走 redirector → MO2 → SKSE），停在主選單。Linux 端：

```
$ curl -s 127.0.0.1:5099/ping
{"ok":true,"plugin":"AgentBridge","version":"0.1.0"}
$ curl -s 127.0.0.1:5099/state
{"ok":true,"player":{"cell":"","cell_form_id":0,"level":1,"name":"Prisoner","position":{"x":2048.0,"y":2048.0,"z":0.0}}}
```

`AgentBridge.log`（Proton prefix 內 `.../My Games/Skyrim Special Edition/SKSE/`）：
```
[08:22:32] AgentBridge loaded
[08:22:41] AgentBridge: listening on 127.0.0.1:5099 (2 route(s))
```

**三件事同時得證**：
1. clang-cl + xwin cross-compile 出來的 DLL，SKSE 在 Proton 底下載得起來 → **D3 成立**，不需要 Windows CI。
2. 遊戲進程內 bind 的 loopback，容器外的 Linux 連得到 → D4 從「探針等級」升級到「真正的 Skyrim 進程等級」。
3. `/state` 回得出東西，代表 **`GameThread::Run` 的主執行緒 marshalling 在遊戲內真的運作**，不只是 socket 活著。主選單狀態下 task queue 就會排空（回的是 dummy player「Prisoner」、等級 1、無 parent cell），這正是預期行為。

#### 0.4 baseline 存檔（2026-08-02）

主檔路徑 `~/games/skyrim-qa-baselines/`（**唯讀 444**，對應五節「存檔汙染」風險：runner 只能主檔→Saves 單向複製，絕不反向）。

| 檔名 stem | 角色 | 位置 | 遊戲時間 |
|---|---|---|---|
| `Save3_474D5830_0_507269736F6E6572_Tamriel_000008_20260802003106_1_1` | Prisoner（Nord） | Tamriel 外景，白漫城外荒野 | 000.08.27 |

`.ess` 與 `.skse` **必須成對**複製——`.skse` 是 co-save，缺了它 SKSE plugin 的持久狀態會掉。

遊戲 Saves 目錄在 Proton prefix 內：`~/.local/share/Steam/steamapps/compatdata/489830/pfx/drive_c/users/steamuser/Documents/My Games/Skyrim Special Edition/Saves/`。

**對 1.5 的影響**：自動載入不需要另外做啟動參數——`POST /console` 一旦通了，`load <存檔檔名>` 就是載入動作，1.5 幾乎是 1.3 的附帶結果。

### Phase 1 — Agent Bridge DLL v1

| # | 任務 | 驗證 |
|---|---|---|
| 1.1 | **✅ 已定案（2026-08-02，使用者決定）：開 sibling 子專案 `projects/ModForge/sub_projs/agent-bridge/`。** 理由：兩者生命週期相反——`scene-capture-bridge` 是人用熱鍵驅動的**創作**工具、與內容一起出貨；`agent-bridge` 是**測試治具**，每次 QA 跑完就卸，絕不能進玩家 load order。把會執行 console 指令的監聽 port 併進創作工具，等於每次做內容都開著那個 port。程式碼複用往反方向走：需要時把 cell 走訪那段搬進 agent-bridge | 子專案已建立並編出 DLL，見 0.1 |
| 1.2 | **✅ PASS（2026-08-02）** `GET /state` 完整欄位，分成「永遠回傳」與「選配」兩層 | 見下方「1.2 實測結果」 |
| 1.3 | **✅ 執行面 PASS，輸出面部分達成（2026-08-02）** `POST /console` 執行任意指令 | 見下方「1.3 實測結果」 |
| 1.4 | **⏸ 延後（D6）** `POST /screenshot`：抓 D3D11 backbuffer 寫 PNG。只有「使用者出門、AI 自己多試幾次留圖」才需要 | Linux 端讀得到 PNG 且內容正確 |
| 1.5 | **✅ PASS（2026-08-02），如預期是 1.3 的附帶結果**：`POST /console {"cmd":"load <存檔stem>"}` 從主選單直接載入 baseline，不需要啟動參數也不需要 bridge 開機動作 | 主選單下發指令，6 秒後 `/state` 回 `WhiterunExterior15` |
| 1.6 | **⏸ 延後（D6）** `POST /input`：送合成輸入事件。使用者在場時自己按更快更可靠 | 能從遊戲中開到 Inventory / MCM 指定分頁 |

### Phase 2 — Linux 端 client

| # | 任務 | 驗證 |
|---|---|---|
| 2.1 | **✅ PASS（2026-08-02）** `mo2ctl`：`install` / `uninstall` / `enable` / `disable` / `launch` / `kill` / `status`，落在 `agent-bridge/client/mo2ctl.py`（純 stdlib） | 見下方「2.1 實測結果」 |
| 2.2 | **✅ PASS（2026-08-02）** `client/qa_mcp.py`，已在 `~/.claude.json` 與 houseCARL 並列註冊。暴露 `qa_status` / `qa_state` / `qa_console` / `qa_run` | 見下方「2.2 實測結果」 |

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

**暴露四個，刻意不暴露另外四個。** 給的是 `qa_status` / `qa_state` / `qa_console` / `qa_run`。**不給 `install` / `uninstall` / `launch` / `kill`**：這四個各自只是一行 Bash、一個 session 用不到幾次，而真正頻繁、真正值得走 MCP 的是 `state` 與 `console`。讓模型能用一次 tool call 就終結使用者的遊戲 session，是比「要它自己打指令」更差的人機介面。`qa_run` 仍然會做完整套，但那是從一份使用者可以先讀過的 qa.json 來的。

**stdio 的唯一鐵律：stdout 只能有協議流量。** 一個誤觸的 `print()` 就會汙染串流，client 端只會看到連線莫名斷掉。兩個由此而來的實作決定：`qa_run` 強制 `interactive=False`（runner 在這裡卡在 `input()` 會讓 server 整個吊死且沒人回得了）；notification（沒有 `id` 的訊息，例如 `notifications/initialized`）一律不回應——對 notification 回應是協議違規，有些 client 會直接斷線。

驗證：腳本化 handshake 跑過 initialize / tools/list / ping / 四個 tool / 未知 tool / 未知 method / 壞 JSON，每一行 stdout 都是合法 JSON-RPC、stderr 全乾淨；再用註冊檔裡那條命令原封不動從 `/` 這個無關 cwd 跑一次確認（`qa_run` 的相對路徑是相對 script 目錄解析的，所以照樣通）。

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

### Phase 4 — 人工關卡

| # | 任務 | 驗證 |
|---|---|---|
| 4.1 | **⏸ 延後（D6）** 視覺驗證連拍與 before/after 對照。使用者在場時直接叫他看即可 | 使用者收到成組可比對的圖 |
| 4.2 | **簡化（D6）** `handoff_user` step 保留,但**拿掉「AI 導航到指定頁面」那半**——只要停住並通知使用者,使用者自己操作。不依賴 1.6 | 走通一次通知→使用者回覆→AI 收尾 |

#### 1.3 實測結果（2026-08-02）

執行機制：`IFormFactory` 造 `RE::Script` → `SetCommand` → `CompileAndRun(target)`，走 `GameThread::Run`（timeout 10s）。`ref` 參數是 console 的「selected reference」，給 `player.additem` 這類點號指令用的。

| 測試 | 結果 |
|---|---|
| `load <baseline stem>`（主選單） | ✅ 載入成功，6 秒後 `/state` 從空 cell 變 `WhiterunExterior15` @ (14732, -14913, -4784) |
| `coc WhiterunBanneredMare` | ✅ `/state` 變 `WhiterunBanneredMare` (0x1601E) @ (2.9, -399.9, 70.2) |
| `player.getav health` | ✅ 輸出 `GetActorValue: Health >> 100.00` |
| `getgs fMoveCharWalkBase` | ✅ 輸出 `GameSetting fMoveCharWalkBase >> 100.00` |
| 亂指令 | ✅ 輸出 `Script command "thisisnotacommand" not found.` |
| 壞 ref `0xDEADBEEF` | ✅ 400 + `no reference with form id 0xDEADBEEF` |
| 空 body | ✅ 400 + `missing "cmd"` |

**輸出擷取只有部分達成，而且踩了兩個坑（都記在子專案 README 的 Pitfall 段）**：

1. **`ConsoleLog::VPrint` 的 5-byte detour 會讓遊戲開場即 crash**（access violation，跳進不可讀位址）。這個 load order 裡 `MoreInformativeConsole.dll` 與 `ConsoleUtilSSE.dll` 都在 console 輸出路徑上，兩個 plugin patch 同一段序言，後者蓋掉前者，前者保存的「原始位元組」就變成別人 `jmp` 的一半。**通則：在真實的百來個 mod load order 裡，對熱門引擎函式做序言 detour 本來就不安全。**
2. 改讀 `ConsoleLog::lastMessage`（純結構成員存取，零衝突風險）後，發現 **before/after 比對會抓到別人插隊寫的行**——`load` 與 `coc` 明明不印東西，卻分別回了 `GetInFaction >> 0.00`、`IsShieldOut >> 0.00`。某個 mod 顯然在高頻透過 ConsoleUtil 查詢。0.2.2 改成**先印哨兵 `__agentbridge_N__` 再比對**：沒人印東西時哨兵還在，就正確回空。

**殘留限制（0.3.0 實測後定案，設計上接受，不再投入）**：
- **只拿得到最後一行**。`sqs`、`help` 這類多行輸出會被截成末行。
- **哨兵只對「執行很快的指令」有效**。實測：`player.additem`、`player.setav` 回正確的空 `output`；但 `load`、`coc` 仍分別漏出 `GetInFaction >> 0.00`、`GetNumericPackageData >> 360.00`。規律是**指令的同步執行span 越長，別的 mod 越有機會插隊寫 `lastMessage`**，而 span 長度由指令本身決定，縮不了。
- **因此 runner 的 `assert_state` 一律對 `/state` 斷言，不要對 console 輸出斷言。** console 輸出只當診斷資訊，不當事實來源。`output_captured: true` 不代表那行是這條指令印的。

#### 1.2 實測結果（2026-08-02，AgentBridge 0.3.0）

**沒有照原計畫「裁剪自 Mantella / MinAI 欄位清單」**——那兩份的取向是「把數值轉成人看得懂的描述」（MinAI 的 21 級時間描述、~60+ 地點關鍵字），對 LLM 對話有用，對 QA 斷言沒用。QA 要的是**機器可斷言的事實**，所以欄位重新設計過。

**兩層設計**（`GET /state[?include=nearby,inventory,quests][&radius=][&limit=]`）：

- **永遠回傳**：`player`（name/level/position/angle_z/cell/worldspace/interior/health-magicka-stamina 的 current+max/carry_weight/in_combat-sneaking-weapon_drawn-dead/左右手裝備）、`game`（遊戲時間、`menus_open`、`dialogue` 的 topic/quest/speaker）。
- **選配**：`nearby_actors`（走引擎自己的 `ProcessLists::highActorHandles`，比走遍 cell 的 placed ref 便宜得多，依距離排序）、`inventory`、`quests`（active + `currentStage`）。

分層的理由：只想確認「cell 有沒有變」的 QA step，不該付整包背包和全 quest 掃描的代價。每個集合都有 `limit`（預設 32），免得一個壞請求讓主執行緒去組 900 筆陣列。

實測（白漫勇者之家內）：`nearby_actors` 依距離抓到 Jon Battle-Born(136)/Mikael(170)/Uthgerd(366)/Hulda(541)/Saadia(615)；`inventory` 抓到金幣與 `worn:true` 的礦工衣；`quests` 抓到 Live Another Life stage 200。狀態變更確實反映：`player.additem f 500` → 金幣 113→613；`player.setav health 250` → current 與 max 都變 250。

**兩個要知道的行為，不是 bug**：
- `equipped.right` / `left` 只涵蓋**雙手**（武器/法術）。盔甲不在手部 slot，空手時是 `null`——身上穿的要看 `inventory` 的 `worn: true`。
- 主選單狀態下 `/state` 可能回 **503**（task queue 沒排空）。0.1.0 時期在主選單拿得到 dummy player，但那是遊戲已完全靜止時；剛啟動還在初始化就會逾時。runner 要把「主選單 /state 逾時」當正常，靠 `/ping` 判斷進程活著。

## 五、風險

- ~~**D4 的 loopback 假設不成立** → 最大單點風險~~ → **2026-08-02 已用獨立 Win64 探針證活**（wine 與 Proton/pressure-vessel 兩條都通，見 Phase 0.1a）。備援 `Z:` 共享目錄檔案投遞不需要了。殘留的小風險只剩「在 Skyrim 進程內 bind」與「console exe 自己 bind」的差異。
- **Proton / Wine 不穩**：反覆冷啟動遊戲容易累積 crash。runner 要有 timeout + 強制 kill + 重試。
- **存檔汙染**：baseline 存檔必須唯讀複製後使用，絕不讓自動化流程覆寫原檔。
- ~~**MO2 被同時修改**：遊戲執行中不得改 `mods/` 或 profile 檔；`mo2ctl` 要有互斥檢查。~~ **已處理，且比原本設想的嚴重**：真正的加害者不是遊戲而是 **MO2 本身**——MO2 把 profile 存在記憶體裡，退出／切 profile 時整份寫回，所以在 MO2 執行中改 `modlist.txt` 不會衝突，會在幾分鐘後被**靜默回滾**，無錯誤訊息，症狀只表現為「裝了卻沒載入」。`mo2ctl` 所有寫入類子指令對 **MO2 或遊戲任一在跑**都拒絕執行。
- **無法 headless**：遊戲需要顯示輸出，這條迴圈只能在使用者的桌面 session 跑，不能背景常駐。
- **cross-compile 的 DLL 與 MSVC 產物行為差異**：D3 已接受此風險（內部工具，非出貨物）。

## 六、結案（2026-08-02）

**Phase 0 / 1 / 2 / 3 全過，Phase 4 依 D6 只剩 handoff 而那已隨 3.2 落地。本計畫無 open 項。**

程式碼與文檔的家：`projects/agent-bridge/`（子專案 README 有 Pitfall 段；`client/QA-SCHEMA.md` 是 qa.json 的權威）。原始結案 commits 為 `50cebe6` / `fb94931` / `a7c5863` / `a1e5f31`；後續已抽成獨立 repo 並 push。

**MCP server 四個 tool 實機驗完**（`qa_status` / `qa_state` / `qa_console` / `qa_run`，註冊在 `~/.claude.json`，註冊當下那個 session 不生效、下一個才生效）。一輪完整 `qa_run` ≈ 30 秒（含冷啟動 19 秒），收尾後 profile 零殘留。

**首跑抓到的那個 ModForge bug 已修，而且是被這條迴圈自己驗證的**（commit `eb0bb6c`）：`CopyCellEnv` 從來沒複製 `EditorID` → CELL override 讓 vanilla cell 變無名。用修好的產生器重 build `ModForgeNavmeshNoop.esp`，跑一份把 `player.cell == "WhiterunBanneredMare"` 加回斷言的 smoke 變體（即首跑失敗的那條），`pass` 8/8。**但 schema 的建議不變：production spec 仍用 `cell_form_id`**——修的是我們的產生器，任何別人的 mod 漏帶 EDID 都能重演同一件事。

**baseline 存檔組合不預先擴充**（使用者決定）：各 mod 要的測試環境不同，先猜組合是浪費。白漫城外荒野那份（`~/games/skyrim-qa-baselines/`，444）夠用，要新的等實際需要再開。

下次要動這條迴圈，從子專案 README 進去，不用重讀本計畫。
