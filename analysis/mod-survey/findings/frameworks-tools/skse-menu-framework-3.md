# SKSE Menu Framework 3（遊戲內嵌 Dear ImGui 選單框架；native C++ SKSE plugin）

← [survey index](../../index.md)

**作者**：QTR-Modding（Thiago099）
**出處**（皆開源，讀 source）：
- 框架：https://github.com/QTR-Modding/SKSE-Menu-Framework-3
- 官方範例：https://github.com/QTR-Modding/SKSE-Menu-Framework-3-Example

| 項目 | 值 |
| --- | --- |
| 類型 | **框架型**：給 modder 用的**遊戲內 GUI 選單框架**，本體是 native `SKSEMenuFramework.dll`（CommonLibSSE-NG SKSE plugin，v3.4 / vcpkg 2.1.1）|
| 渲染 | **Dear ImGui**（bundled，含 `imgui_impl_win32` + `imgui_impl_dx11`）疊在遊戲 D3D11 上 |
| Plugin | **無 ESP**（純 SKSE DLL + loose 資產：fonts / themes / ini）|
| 消費者介面 | **純 C++ header API**（`resources/SKSEMenuFramework.h`）——消費者 mod **必須自己寫一支 SKSE plugin**。**無 Papyrus API、無資料驅動註冊** |
| 敘事價值 | 無 |

<!-- wf-nav -->
- [architecture-and-api](skse-menu-framework-3/architecture-and-api.md)
- [modforge-evaluation-and-integration](skse-menu-framework-3/modforge-evaluation-and-integration.md)
