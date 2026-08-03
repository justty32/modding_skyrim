# skyrim_engine —— 引擎/SKSE modding 知識庫

Skyrim SE 引擎逆向分析知識庫,以 **CommonLibSSE-NG**(C++/SKSE plugin 開發)為主軸,兼及 NIF/Papyrus/record 層。2026-04-15 從舊 `project_analysis` 遷入(見 `session_log.md`)。

> 與隔壁 `analysis/skyrim_mods/`(七個**參考 mod** 的拆解,服務 ModForge spec 設計)不同:本目錄是**引擎本身怎麼運作、SKSE plugin 怎麼寫**的通用知識,不綁定特定 mod。

## 目錄結構

| 目錄 | 篇數 | 性質 |
|---|---|---|
| `architecture/` | 39 | 子系統深潛(骨骼/Biped/NIF/Shader/VFX/對話儲存架構…) |
| `tutorial/` | 60 | 實作教學(從單一小技巧到完整系統實裝) |
| `answers/` | 39 | 具體問題的分析解答 |
| `others/` | 6+README | RE 命名空間 API 總覽(Events/UI/Magic/Inventory/Papyrus/Input) |
| `details/commonlibsee-ng/` | — | CommonLibSSE-NG 專案結構與 RE 層細節、examples |

## 檔名慣例

`<分類>_<主題>.md`,分類前綴:`3D_Graphics` / `Dialogue_Quest` / `Items` / `Magic` / `NPC` / `Systems` / `World`。tutorial 內帶編號者(如 `Magic_05_...`)是小顆粒單題教學,帶 `Tutorial_` 者是完整系統教學。

## 常用入口

- FormID 二進位結構:`architecture/Systems_TESForm_Detailed.md`(AGENTS.md 有引用)
- RE 層 API 快查:`others/README.md`
- CommonLibSSE-NG 專案總覽:`details/commonlibsee-ng/00_overview.md`
- AI 框架(SkyrimNet/Mantella/MinAI/IntelEngine)拆解:`answers/*-analysis.md` 四份;綜合借鏡結論見 `answers/ai-frameworks-modforge-relevance.md`
