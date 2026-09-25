# tundra-defense — scope-records

← [調查入口](../tundra-defense.md)

## Scope / sources

Scope / sources的逐列資料。

已抽到 [tundra-defense-sources.json](tundra-defense-sources.json)（7 列）

項目：原表「項目」欄。

值：原表「值」欄。

統計：7 列記錄；2 欄。

抽 `.pex`：用 repo 內 `../../../projects/sofia-patch/vigilant-reconstruction-redo/_tools/bsa_reader.py`（7z 開不了此 BSA）+ 自寫 Skyrim `.pex` 字串表 parser（magic `0xFA57C0DE`，big-endian）。記憶體鐵律遵守（只走 CLI lazy overlay，未整載任何主檔）。

## 1. Classification

<!-- wf-nav -->
- **類型**：**自建聚落／據點經營＋波次守城（base-building + tower-defense）**——玩家從零放下一個 Water Well「核心」，自由擺放建物/城牆/陷阱/守衛，再手動或隨機觸發一波波敵人來襲。**不是內容型（無地點/角色弧），是純系統型 sandbox。**
- **Plugin**：是，單一 ESP，Skyrim.esm-only。**SKSE 依賴**：`aaaFortPlayerQuestScript` 內有 `iGetKeyPressed` / `aiDXScanCode` / `BindKey`（自製 keybinder）**(pex-strings)** → **需 SKSE**（DXScanCode 鍵盤輪詢是 SKSE-only）；建造輸入另用 4 個自製 Voice/Concentration Spell（見 §3）作為不依賴 SKSE 的後備確認鍵。
- **敘事價值**：**無**（generic 募兵/管理選單對白 + 3 段 SpecialPlans 語音，無角色弧）。
- **系統價值（對 idea #22）**：**最高**。`settlement-npc-expansions` / `populated-skyrim-family` / `cutting-room-floor` 都只解「**住滿既有聚落**」；**Tundra Defense 是唯一一個把「玩家**從無到有蓋出**據點 + 經營 + 防守」整套做出來的範本**，正是 #22 「漂泊開拓慢活」的核心動詞（build/manage/defend），也是 `settlements:` Phase-2 的活樣本。

## 2. Record shape（`dump` tally，未整載）

2. Record shape（`dump` tally，未整載）的逐列資料。

已抽到 [tundra-defense-records.json](tundra-defense-records.json)（19 列）

record：原表「record」欄。

count：原表「count」欄。

角色：原表「角色」欄。

統計：19 列記錄；3 欄。

讀法：**核心三件套 = 109 Ingestible（建材瓶）↔ 113 MagicEffect（"Construct X"）↔ 108 Activator（建物本體）**，幾乎一一對應。87 MESG = 整個 UI 層。0 GLOB = 狀態全活在 quest script 上。

