# UIExtensions (v1.2.0, Nexus #17561) — files-and-menu-records

[返回入口](../uiextensions.md)

## 檔案結構

來源：`~/skyrim_mods/UIExtensions/`

```
UIExtensions/
├── UIExtensions.esp   (1.1 KB) ← 純邏輯註冊：9 record
└── UIExtensions.bsa   (467 KB) ← 視覺 (SWF) + 腳本 (PEX/PSC)
```

**強調 `master(s)=[]`：完全自包含的獨立 plugin**（驗證：`dump UIExtensions.esp` 輸出 `master(s)=[]`）。它不 override、不引用 Skyrim.esm 的任何 record，9 個 record 全是新增的 menu 註冊容器與一個結果傳遞用 FormList。因此它可以放在 load order 任意位置、不挑前置，這正是 library 型 plugin 該有的形態。

邏輯與資產的分工：

- **邏輯在 ESP 的 9 record**：8 個常駐 quest 當 menu 的單例腳本容器 + 1 個 FormList 當選取結果的傳遞通道。
- **視覺/實作在 BSA**：每個 menu 一個 Flash `.swf`（畫面與動畫）+ 對應 `.pex`（編譯後 Papyrus）。

BSA 內可辨識的資產（來源：`strings UIExtensions.bsa`）：

| 類別 | 內容 |
|---|---|
| menu SWF | `listmenu.swf` / `selectionmenu.swf` / `wheelmenu.swf` / `textentrymenu.swf` / `magicmenuext.swf` / `statssheetmenu.swf` / `cosmeticmenu.swf` / `dyemenu.swf` / `followermenu.swf` |
| 輔助 SWF | `messagebox.swf` / `meter.swf` / `bottombar.swf` / `buttonart.swf` |
| 圖示 SWF | `icons_category_psychosteve.swf` / `skyui_icons_psychosteve.swf` |
| menu 腳本 (.pex/.psc) | 對應 8 個 ESP menu，外加輔助 `UIExtensions` / `UIMenuBase` / `UIMenuLoad`（基底/載入器，不掛 quest，被各 menu 共用） |

> 註：`followermenu.swf` 存在於 BSA，但 ESP 沒有對應的常駐 quest record，研判為內部/未公開或由其他 menu 共用的資產。BSA **無工具解包**，SWF 與 .pex 的內部細節不在本分析範圍，以下聚焦 ESP record + 公開知識。

## record 解剖

### 8 個 menu quest（單例容器慣用法）

8 個 record 全是 **Quest**，各掛一個（CosmeticMenu 掛兩個）UI menu 腳本，`flags=273`、`priority=0`：

本表彙整「menu-quests」的原始記錄。已抽到 [files-and-menu-records-menu-quests.json](files-and-menu-records-menu-quests.json)（8 列）。

FormID：原表「FormID」欄值。

Quest / 掛載腳本：原表「Quest / 掛載腳本」欄值。

用途：原表「用途」欄值。

統計：8 列，3 欄。

**單例容器慣用法**：8 個 quest 都用「常駐 quest 當 script 容器」這個 SkyUI/SKSE 生態的標準手法——`flags=273` 含 **Start Game Enabled** bit，遊戲一開始就把這些 quest 啟動並常駐，掛在上面的 menu 腳本因此始終存在、可被任何 mod 透過 `Quest.GetScript()` 或直接 cast 取得單例。quest 本身沒有 stage/objective/alias 等任務語意，純粹借用「常駐物件」的生命週期當腳本宿主。

### FormList SelectedForms `[002852]`

`[002852:UIExtensions.esp] FormList SelectedForms` 是**菜單與呼叫端之間的結果傳遞通道**。當 menu（特別是涉及 Form 選擇的 SelectionMenu）讓玩家勾選了一個或多個遊戲物件（Form）時，把結果寫進這個共用 FormList，呼叫端在 menu 關閉後讀取它即可取得「玩家選了哪些 form」。FormList 在此扮演 Papyrus 跨腳本傳遞「一組 Form」的便捷共享變數（避免逐一 SetPropertyValue 的麻煩）。

