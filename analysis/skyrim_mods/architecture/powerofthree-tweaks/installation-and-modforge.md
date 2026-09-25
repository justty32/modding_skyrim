# powerofthree's Tweaks (v1.15.1) — installation-and-modforge

[返回入口](../powerofthree-tweaks.md)

## FOMOD 安裝流程

讀 `fomod/ModuleConfig.xml` 後可確認其安裝邏輯。它**不能**像 JContainers 那樣直接平鋪，因為 SE 與 AE 的 DLL 互斥——若兩顆都丟進 `Data/SKSE/Plugins/` 會撞檔，且裝錯版本會直接 CTD。FOMOD 就是用來在安裝期做這個二選一。

流程分兩段：

1. **必裝部分**（`requiredInstallFiles`）：把 `Required/` 整個資料夾複製到 `Data/` 根（`destination=""`），即共用的 `po3_Tweaks.pex` + `.psc`。這段無條件執行，因為 Papyrus 介面對兩版本相同。

2. **單一安裝步驟「Main」→ 群組「DLL」**（`installStep name="Main"`，`group type="SelectExactlyOne"`）：強制玩家**恰好選一個**：
   - **SSE v1.6.629+ (Anniversary Edition)** → 安裝 `AE/SKSE/Plugins` 到 `SKSE/Plugins`
   - **SSE v1.5.97 (Special Edition)** → 安裝 `SE/SKSE/Plugins` 到 `SKSE/Plugins`

   每個選項帶 `typeDescriptor` / `dependencyType`，會偵測 `gameDependency version`：
   - 偵測到遊戲為 **1.6** → AE 選項標記為 `Recommended`、SE 標記為 `Optional`；
   - 偵測到 **1.5** → 反過來，SE 為 `Recommended`、AE 為 `Optional`。

   也就是 FOMOD 會根據實際遊戲版本**預先推薦**正確的那顆 DLL，但仍由玩家最終確認（`SelectExactlyOne` 保證不會漏選或多選）。

**可選 tweak 開關？沒有。** ModuleConfig 只有「SE/AE 二選一」這一個分支，並未把 45 項 tweak 拆成可勾選的 FOMOD 選項。所有 tweak 是否啟用，是由 DLL 旁邊的 INI 設定檔（runtime 讀取，不在此 installer 包內）控制，而非安裝期決定。安裝期的唯一決策就是引擎版本對應的 DLL。

## 對 ModForge 的意義

ModForge（`projects/ModForge`）是程式化生成 Skyrim plugin 的工具，產出 quest / dialogue / scene / NPC / weapon 等各式 record。powerofthree's Tweaks 修掉的多是**引擎層 bug**，與 ModForge 生成的內容有幾個務實的交集點。

### (a) 可假設玩家裝了哪些常見修正——但僅止於「假設」，不是「依賴」

po3 Tweaks 是 SE/AE 社群的**準標配**之一（與 SKSE、Address Library、USSEP 同級的普及度）。其中幾項剛好覆蓋 ModForge 生成內容的踩坑區：

- **Projectile Range Fix**：ModForge 已能生成自訂 PROJ/EXPL（CLAUDE.md「已落地功能 → Projectile (PROJ) + Explosion (EXPL)」）。自訂投射物的射程行為若遇上 vanilla 的計算錯誤，這項修正會讓表現更接近預期。ModForge 仍應以 vanilla 未修正的行為為基準設計，把 po3 當作「裝了會更好」而非「裝了才對」。
- **Distant Ref Load Crash**：ModForge 在自訂 worldspace 放置大量 reference（placements / 自訂 cell）時，遠距載入正是高風險區。這項修正能降低終端使用者載入崩潰的機率，但 ModForge 不能因此放鬆對 placement 數量與分佈的節制。
- **Cast Added Spells / No-Death-Dispel Spells on Load**：若 ModForge 生成的內容依賴常駐 buff（ability/常駐法術），這兩項修正能緩解「載入存檔後 buff 消失」的經典問題。

結論：ModForge 生成時可以在文檔/README 層級**建議**玩家裝 po3 Tweaks 以獲得更穩定的體驗，但**生成的 plugin 本身不得在功能上預設它存在**。

### (b) Load EditorIDs 對 ModForge debug 流程有實質幫助

ModForge 的開發循環高度依賴主控台診斷（CLAUDE.md 列出的 `smtree` / `scnscan` / `packagediag` / `lightdiag` 等 diag 指令，以及 in-game 測試 workflow）。Skyrim 引擎在 runtime **預設丟棄 EditorID**，主控台只能用 FormID 定址生成出來的 record——但 ModForge 生成時是以 EditorID 命名 record 的，FormID 要在 build 後才能對上。

**Load EditorIDs** 這項 tweak 讓 EditorID 在 runtime 保留，主控台可直接 `help "<EditorID>"` 或用 EditorID 引用物件。對 ModForge 的 in-game 驗證流程（package → zip → 進遊戲測）來說，這把「我生成的那個 quest/NPC 的 FormID 是多少」這個反覆出現的查找步驟大幅簡化。**這是開發者機器上值得常駐的工具，但屬於 debug 便利，不影響成品行為。**

### (c) 這是 native DLL 依賴，ModForge 不該強制依賴它

po3 Tweaks 的修補全在 DLL 裡，且 SE/AE 各一份、綁特定遊戲版本（見上節 FOMOD 邏輯）。ModForge 若讓生成的 plugin 在 record 層級依賴某項 po3 行為（例如假設 Projectile Range 已修正才能正常運作），就等於：

1. 強迫終端使用者裝對版本的 native DLL；
2. 把 plugin 的正確性綁到一個 ModForge 無法驗證、會隨遊戲更新失效的外部 binary 上。

這與 ModForge 對 JContainers 的態度一致（見 `jcontainers.md`「對 ModForge 的意義」）：native 依賴屬於**進階/可選**層，不該進入預設生成路徑。

務實定位：**po3 Tweaks 對 ModForge 開發者是好用的環境（尤其 Load EditorIDs），對 ModForge 產出物則是「相容即可、不依賴」的外部修補層。**
