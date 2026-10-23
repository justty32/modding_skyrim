# skyrim_engine —— 引擎/SKSE modding 知識庫

Skyrim SE 引擎逆向分析知識庫,以 **CommonLibSSE-NG**(C++/SKSE plugin 開發)為主軸,兼及 NIF/Papyrus/record 層。2026-04-15 從舊 `project_analysis` 遷入。

> 與隔壁 `analysis/skyrim_mods/`(七個**參考 mod** 的拆解,服務 ModForge spec 設計)不同:本目錄是**引擎本身怎麼運作、SKSE plugin 怎麼寫**的通用知識,不綁定特定 mod。

> **另有一份副本**：`projects/my_skyrim_plugin_1/skyrim_mod/`（該 repo 的隨身手冊，入口是它的 `INDEX.md`）。**本目錄是正本**。2026-10-23 逐份比對：168 組配對裡 163 組 sha256 完全相同（資料見 `agentctl/handoffs/home-2026-10-23/kbdiff/pair-classification.json`）。**改這裡的共有檔案時，先評估另一邊是否要同步**——同一批連結已經被兩邊各自修過一次（analysis 2026-08-12、projects 2026-10-17），索引也各建了一份。

## 目錄結構

篇數為 2026-10-23 實數（`ls <dir>/*.md` 扣掉各自的 README）。

<!-- wf-nav -->

| 目錄 | 篇數 | 性質 |
|---|---|---|
| [`architecture/`](architecture/README.md) | 39 | 子系統深潛(骨骼/Biped/NIF/Shader/VFX/對話儲存架構…) |
| [`tutorial/`](tutorial/README.md) | 59 ＋ [`Ultimate_Town_Challenge/`](tutorial/Ultimate_Town_Challenge/README.md) 9 | 實作教學(從單一小技巧到完整系統實裝) |
| [`answers/`](answers/README.md) | 48(另 24 篇在同名子資料夾) | 具體問題的分析解答 |
| [`others/`](others/README.md) | 6 | RE 命名空間 API 總覽(Events/UI/Magic/Inventory/Papyrus/Input) |
| [`details/commonlibsee-ng/`](details/commonlibsee-ng/README.md) | 2 ＋ RE 7 ＋ examples 3 | CommonLibSSE-NG 專案結構與 RE 層細節、examples |
| [`archive/`](archive/README.md) | — | 已封存、不在維護鏈的文件 |

## 檔名慣例

`<分類>_<主題>.md`,分類前綴:`3D_Graphics` / `Dialogue_Quest` / `Items` / `Magic` / `NPC` / `Save_Data` / `Systems` / `World`。tutorial 內帶編號者(如 `Magic_05_...`)是小顆粒單題教學,帶 `Tutorial_` 者是完整系統教學。各目錄索引即照這組前綴分節。

## 常用入口

- FormID 二進位結構:[`architecture/Systems_TESForm_Detailed.md`](architecture/Systems_TESForm_Detailed.md)(AGENTS.md 有引用)
- RE 層 API 快查:[`others/README.md`](others/README.md)
- CommonLibSSE-NG 專案總覽:[`details/commonlibsee-ng/00_overview.md`](details/commonlibsee-ng/00_overview.md)
- AI 框架(SkyrimNet/Mantella/MinAI/IntelEngine)拆解:[answers 索引的「AI 框架拆解」節](answers/README.md)共 9 份;綜合借鏡結論見 [`answers/ai-frameworks-modforge-relevance.md`](answers/ai-frameworks-modforge-relevance.md)
