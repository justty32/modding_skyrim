# 環境事實與設計決策

> 屬於 [AI 全自動 mod QA 迴圈](README.md)。

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
| 既有 QA 素材 | `projects/scene-capture-bridge/`：SKSE C++23 DLL，已有 console 指令系統、cell placed-ref 走訪、scene.json 匯出 | 該子專案 README |
| Linux cross-compile | `my_skyrim_plugin_1` 的 `release-clang-cl-linux` preset（clang-cl + lld-link + xwin）**實測產出過可用 DLL**：`build/release-clang-cl-linux/DaylightDungeon.dll`（PE32+ DLL，1.1M，2026-06-06） | `file` 輸出 |

**兩個對不上的地方（未處理，留給 notes 側）**：
- 自製產物已集中到 private 的 `mod-library/`（`l10n/mods/`、`plugins/`、`artifacts/`）；歷史散布位置仍是 `~/skyrim_mods/mine/`。
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
