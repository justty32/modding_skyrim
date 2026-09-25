# SkyUI SE — files-and-records

[返回入口](../skyui.md)

## 檔案結構

來源：`~/skyrim_mods/SkyUI/`

| 檔案 | 大小 | 內容 |
|---|---|---|
| `SkyUI_SE.esp` | 2.4 KB | 只有 **7 個 record，全是 Quest**；master = `[Skyrim.esm]` |
| `SkyUI_SE.bsa` | 2.9 MB | Flash UI（`.swf`）+ 編譯後的 `SKI_*.pex` Papyrus 腳本 |

關鍵的結構觀察：**邏輯在 ESP 的 7 個 quest-script，視覺與程式碼本體在 BSA**。

- ESP 之所以只有 quest，是因為 SkyUI 的本體是 **Papyrus（行為）+ Flash（畫面）**，兩者都不是遊戲世界資料 record。ESP 在這裡退化成一張極薄的「腳本掛載清單」：每個 quest 唯一的作用就是當一個**常駐單例**，把對應的 `SKI_*` script 實例化並掛上去。
- BSA 內含 SWF 與 `SKI_*.psc/.pex`，本機**無工具解包**，故以下 record 解剖聚焦 ESP 暴露的 quest + script 名稱，腳本內部行為以公開知識補述（已標註）。
- 安裝結構為 MO2 標準平鋪（`.esp` + `.bsa` 同名成對放在 `Data/` 根；BSA 靠同名 ESP 自動載入）。

## record 解剖

來源：`dotnet run --project src/ModForge.Cli -- dump ~/skyrim_mods/SkyUI/SkyUI_SE.esp`（已重跑驗證）

七個 quest 一律是「**用 quest 當常駐單例 script 容器**」的慣用法——quest 本身沒有 stage 邏輯、沒有 alias、priority=0，存在的唯一目的是承載一個 SkyUI 子系統的 Papyrus 物件，並靠 quest flags 讓它在開新遊戲時自動常駐。

本表彙整「quest-records」的原始記錄。已抽到 [files-and-records-quest-records.json](files-and-records-quest-records.json)（7 列）。

FormID：原表「FormID」欄值。

EditorID：原表「EditorID」欄值。

掛載 script：原表「掛載 script」欄值。

職責（script 名稱 + 公開知識）：原表「職責（script 名稱 + 公開知識）」欄值。

統計：7 列，4 欄。

子系統可分成三組：

- **MCM 框架**：`SKI_ConfigManager`（註冊與分發）+ `SKI_ConfigMenu`（渲染）—— 對 ModForge 唯一有意義的部分。
- **HUD widget 框架**：`SKI_WidgetManager` + `SKI_ActiveEffectsWidget`。
- **啟動 / 設定 / 收藏**：`SKI_Main`、`SKI_SettingsManager`、`SKI_FavoritesManager`。

### quest flags = 常駐單例

dump 顯示 flags 並非隨意：

- `SKI_ConfigManagerInstance` flags = **281**，其餘六個 flags = **273**。
- 兩者都含 **Start Game Enabled** 位（quest 在新遊戲一開始就執行、整局常駐），這正是「把 quest 當常駐單例腳本容器」的前提。
- 差別在 ConfigManager 多了一個位：它是唯一帶有 `stage[1]`（空 log）的 quest，需要 stage table 存在（281 = 273 + 額外旗標），用以驅動它的初始化/掃描流程；其餘子系統不需要 stage。

> 慣例提煉：**Start Game Enabled quest + 掛一個 script（0 個 alias、priority 0）= 一個全域常駐的 Papyrus 單例**。這是 Skyrim 框架類 mod 共通的招式（Sofia 的 `JJSofiaMCM`、`SofiaFollowerScript` 等也是把狀態塞在常駐 quest 的 script property 上，見 `sofia-follower.md`）。

