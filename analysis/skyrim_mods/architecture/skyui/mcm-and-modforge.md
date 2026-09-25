# SkyUI SE — mcm-and-modforge

[返回入口](../skyui.md)

## MCM 機制概述

> 以下為一般性說明（公開知識 / SkyUI SDK 慣例），非從本機源碼解碼——BSA 未解包。

mod 作者要做的事：

1. 寫一個 quest script，宣告 `Scriptname MyMod_MCM extends SKI_ConfigBase`。
2. 覆寫生命週期回呼建構頁面：
   - `OnConfigInit()` —— 設定頁名、分頁數等一次性初始化；
   - `OnPageReset(string page)` —— 每次開啟該頁時呼叫，用 `AddToggleOption` / `AddSliderOption` / `AddMenuOption` / `AddTextOption` 等逐一加控制項；
   - `OnOptionSelect` / `OnOptionSliderAccept` 等 —— 玩家操作時的回呼，把值寫回 mod 的狀態（通常是 GlobalVariable 或 script property）。
3. 把這個 script 掛到一個 **Start Game Enabled quest** 上。

剩下的由 SkyUI 自動完成：`SKI_ConfigManager`（`[000802]`）在啟動時掃描所有 `SKI_ConfigBase` 子類、把它們列進 MCM 左欄，玩家點選時分發到對應實例，再由 `SKI_ConfigMenu`（`[000820]`）渲染。作者**完全不需碰 Flash**，只寫 Papyrus。

**連結回 Sofia 分析**：Sofia 的 `JJSofiaMCM "Sofia Config Menu"` quest（`[00C55D]`，掛 `SofiaMCMscript` 26 prop，見 `sofia-follower.md:53`）就是這套機制的一個實例——它在 MCM 裡提供 catch-up 距離、評論頻率、戰鬥風格切換等開關，玩家在選單調整後寫回 `SofiaCatchUpEnabled` / `SofiaCommentFrequency` 等 GlobalVariable（`sofia-follower.md:127`）。Sofia 同時用 `JJSofiaGetHasSKSE` 在 runtime 探測 SKSE 是否存在、缺了就降級停用 MCM——印證了「**MCM 是選配，核心功能不該硬依賴它**」。

## 對 ModForge 的意義

ModForge（`projects/ModForge`，程式化生成 plugin）目前的設定儲存是 **GLOB（GlobalVariable）**（見 `src/ModForge.Core/Spec.Globals.cs`、`Generator.Build.Globals.cs`，以及 ModForge CLAUDE.md「已落地功能 → GlobalVariable」），**但沒有任何遊戲內設定 UI**——使用者只能靠 console 或外部工具改 GLOB 值。

### 要生成 MCM 設定頁需要什麼

若想讓 ModForge 生成的 mod 有設定選單，本質上要產出一個「`extends SKI_ConfigBase` 的 quest + script」，拆成三個能力需求：

本表彙整「mcm-requirements」的原始記錄。已抽到 [mcm-and-modforge-mcm-requirements.json](mcm-and-modforge-mcm-requirements.json)（3 列）。

需求：原表「需求」欄值。

ModForge 現況：原表「ModForge 現況」欄值。

缺口：原表「缺口」欄值。

統計：3 列，3 欄。

### 可行性結論（務實）

<!-- wf-nav -->
- **技術上可行，且門檻不高**：ModForge 既有的「生成 `extends X` 的 Papyrus + 掛到 quest + 編譯」管線，與生成一個 MCM config script 是**同型工作**，差別主要在 base class 名稱、回呼樣板（`OnPageReset` 的 `AddToggleOption`/`AddSliderOption`）與一張「GLOB ↔ 控制項」的映射表（可從現有的 `GlobalSpec` 自動推導：short/bool → toggle，float → slider）。
- **但不該預設依賴 SkyUI**：這會把一個 native/UI 框架塞進每個產物的依賴鏈，違反 ModForge「預設零外部依賴」的取向（與 `jcontainers.md` 的結論一致——JFormDB 也被定位為「進階選項，不該預設」）。Sofia 的做法（核心零 SKSE、MCM 選配並 runtime 降級）是正確範式。
- **建議定位為 opt-in 進階功能**：在 spec 增設一個明確的 `mcm` 區塊（例如列出要暴露的 GLOB 與對應控制項型別），只有作者顯式啟用時才生成 config script、加上 SkyUI master/依賴標記，並在文件提醒終端使用者需裝 SkyUI + SKSE。預設仍維持「GLOB + 無 UI」。
- **優先級判斷**：對隨從/內容類 mod 而言，MCM 是「使用者可調設定」的標準缺口（見 `sofia-follower.md` 結論點出這是該品類最大缺口）。若 ModForge 要瞄準隨從這類品類，MCM 生成的投資報酬率高於 native 資料結構（JContainers）持久化。
