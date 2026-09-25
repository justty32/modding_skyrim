# UIExtensions (v1.2.0, Nexus #17561) — usage-and-modforge

[返回入口](../uiextensions.md)

## 使用模式概述（一般性說明，公開知識）

> 以下為 UIExtensions 公開的通用呼叫慣例，非從 BSA 解出的逐行實作。

典型呼叫端流程：

1. **取得 menu 單例腳本**——對目標 menu quest 取得其掛載腳本（如把 `UIListMenu` quest cast 成 `UIListMenu` 腳本型別）。
2. **設定條目**——呼叫腳本上的方法填入清單條目、圖示、旗標等。
3. **`OpenMenu(...)` 顯示並阻塞等待**——叫出 SWF 畫面，呼叫**阻塞**直到玩家做出選擇或取消。
4. **回傳結果**——回傳被選中的**索引**（清單/輪盤）、**輸入字串**（文字框）或一組 **Form**（經 `SelectedForms` FormList）。

這補完了原生 Papyrus 沒有的「即時、互動、阻塞式」UI 原語——原生只有固定的 `MessageBox`（最多有限按鈕、無捲動、無輸入），UIExtensions 把「任意長清單選擇」「自由文字輸入」「輪盤快捷」這些常見互動變成幾行 Papyrus 就能叫出的元件。

## 對 ModForge 的意義

ModForge（`projects/ModForge`）目前的互動產出集中在**對話分支**（quest/dialogue/scene，見 ModForge CLAUDE.md「已落地功能」）。當生成的內容需要「對話以外的即時玩家選擇/輸入」時，UIExtensions 提供現成元件，省去自寫 SWF 的高成本工作。務實評估：

<!-- wf-nav -->
1. **適用場景**：動態指定目標（從一串候選 NPC/地點選一個）、命名（自訂物品/隨從/據點取名 → `UITextEntryMenu`）、分支選單（比對話框更緊湊的選項清單 → `UIListMenu`）、快捷指令（隨從命令輪盤 → `UIWheelMenu`）。這些用對話 INFO 樹做會很笨重，用 UIExtensions 元件更自然。

2. **使用代價**：ModForge 要用它，得**生成呼叫其 menu 腳本的 Papyrus**（取得單例 → 填條目 → `OpenMenu` → 讀回傳值），並把這段腳本編譯掛到生成的 quest/alias/magic-effect 上——這對既有的 Papyrus 生成管線（dispatcher/controller embed、Wine+CK 編譯）是可行的，但 menu 腳本的 header 需納入編譯時的 source/header 路徑。

3. **native + SWF 依賴**：UIExtensions = SKSE 環境下的 SWF + Papyrus 元件，**它是終端使用者必須額外安裝的前置**。ModForge 若產出依賴它的 plugin，等於要求玩家裝 UIExtensions（與 JContainers 同類的「進階選項，不該是預設」處境，見 `jcontainers.md` 的對照結論）。好處是它**無 master**、相容性極佳，當前置比多數 mod 安全。

4. **定位結論**：UIExtensions 對 ModForge 是「**對話分支以外互動**」的有用補充，而非核心依賴。建議列為**可選增強**——在生成需求明確包含「玩家臨時選擇/輸入」時才引入，並在產出 manifest 標明前置；預設管線仍以對話/scene 為主。
