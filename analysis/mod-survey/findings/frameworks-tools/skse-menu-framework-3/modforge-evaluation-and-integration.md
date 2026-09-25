# 對 ModForge：純參考（非可生成）— idea #7 / #24 定位

← [原文入口](../skse-menu-framework-3.md)

## 對 ModForge：純參考（非可生成）— idea #7 / #24 定位

⚠️ **界線（比照 [proteus.md](../../skills-survival/proteus.md) 對閉源 native 的判定，只是這個是開源）**：ModForge 是 **build-time JSON→esp 生成器**，產物是 Bethesda record（+ 附帶 `.pex`/loose 資產）。SKSE Menu Framework 是 **runtime C++ GUI 框架**，它的「選單」是**編譯進消費者 DLL 的 ImGui C++ 程式碼**，**沒有任何 record、沒有資料驅動註冊面**。因此：

<!-- wf-nav -->
- **ModForge 無可生成成分**：生不出 ImGui 視窗（那是 C++ 不是 record/JSON），也沒有像 MCM `config.json` 那樣的中介宣告可讓 ModForge 產出。連消費者的註冊都是 `SKSEPluginLoad` 裡的 C++ 呼叫。
- **idea #7（遊戲內嵌互動 UI）**：這**正是** #7 缺的那塊「原生即時 GUI 畫布」——但只能當**技術選型參考**。若 #7 要走 ImGui 路線，等於 ModForge 得**隨產物附一支預建/需消費者自寫的 SKSE plugin**（同 Tundra/Honed Metal controller `.pex` 的「須附 native code」判定，只是這裡是 DLL 不是 Papyrus）。ModForge 本身不生 GUI。
- **idea #24（遊戲內編輯器需要 GUI：擺物/選 record/存快照面板）**：**它能當 #24 的 UI 層——但代價是 native**。這框架的能力**天生對得上 #24 需求**：range 3D 世界的即時控件、`RE::` 直接讀寫遊戲物件、FormID 查找（範例已示範查 form + 操作）、非暫停 overlay（邊擺物邊看世界）、table/tree 選 record、按鈕存快照。**技術上它就是 #24 面板該用的東西**。但 ModForge **不能「生成」這個編輯器**——得**手寫一支專用 SKSE plugin**（用此框架畫 UI，把「擺物/選 record/存快照」邏輯寫成 C++，快照再吐回 ModForge 的 JSON→esp 管線）。即：**#24 的 GUI 層 = 一個獨立 native 子專案（消費此框架），不是 ModForge 生成目標**。與 AnnoRim 筆記裡「#24 快照該吐 placement 產物格式」呼應——此框架負責「在遊戲內採集」，ModForge 負責「把採集結果生成 esp」。

**對 Sofia**：無關。

## 結論

開源、可讀 source 的**遊戲內 Dear ImGui 選單框架**（D3D11 hook + WndProc 攔輸入 + freezeTime 暫停），消費者以純 C++ header（GetProcAddress shim）註冊選單/視窗/HUD/輸入 hook，**無 ESP、無 Papyrus、無資料驅動**。對 ModForge：**純參考**（生成器域外）。**價值＝它是 idea #7/#24「遊戲內原生互動 GUI／編輯器面板」在技術上最現成的答案**，但落地路徑是「**寫一支消費此框架的 SKSE plugin**」而非 ModForge 生成——ModForge 端最多只在旁邊接「編輯器快照 JSON → esp」的既有管線。

---

## 為何不是 `sse-imgui`（2026-07-10 實測排除）

[ryobg/sse-imgui](https://github.com/ryobg/sse-imgui) 看起來是同類東西，**在 AE 上不能用**：

- 它的功能靠相依鏈 `sse-imgui → sse-gui → sse-hooks`（DLL 內字串 `Accepted SSEGUI interface v`、`.refptr.ssegui`，執行期經 SKSE messaging 取 SSE-GUI 介面）。三者都停在 2020 年、鎖 SE 1.5.97。
- `sse-imgui.dll` 只匯出舊式 `SKSEPlugin_Query` / `SKSEPlugin_Load`，**沒有 `SKSEPlugin_Version`**；import `msvcrt.dll`、字串含 `Mingw-w64 runtime failure`。本機 runtime 是 SKSE **1.6.1170（AE）**。
- 對照：`SKSEMenuFramework.dll` 匯出 `SKSEPlugin_Version`（v3.12.0），CommonLibSSE-NG 建置，upstream 2026-07 仍在動。

## 落地（2026-07-10）：`scene-capture-bridge` 就是它的消費者 plugin

本 finding 原本的結論是「#24 的 GUI 層＝一個獨立 native 子專案」。**不必獨立**——[`../scene-capture-bridge`](../../../../../projects/scene-capture-bridge/README.md) 已經是一支編得過、實機驗過的 CommonLibSSE-NG SKSE plugin，面板直接長在它上面（`src/UI.cpp`）。

- 消費者 header `resources/SKSEMenuFramework.h` vendored 到 `extern/SKSEMenuFramework/`（LGPL-2.1；**離線機必須能 build**，故不用 `file(DOWNLOAD)`）。header 自足，只要 `windows.h` + std。
- **軟相依**：`IsInstalled()` 是 `GetModuleHandleW(L"SKSEMenuFramework")` 探測。編出來的 DLL import 表仍只有 5 個系統 DLL、無此框架的 import name → 沒裝框架的玩家照樣拿到 F10 hotkey，且動態連結符合 LGPL。
