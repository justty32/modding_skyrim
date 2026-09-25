# Phase 0 — 地基驗證

> 屬於 [AI 全自動 mod QA 迴圈](README.md)。

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

**0.2 已驗證通過**：SKSE DLL 在 Skyrim 進程內 bind 同樣可通；這也覆蓋了 console exe 探針未涵蓋的 winsock 初始化時機與 ENB／其他 SKSE plugin 干擾風險。

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
