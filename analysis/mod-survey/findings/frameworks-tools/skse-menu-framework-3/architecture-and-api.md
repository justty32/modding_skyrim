# 是什麼（別望文生義）

← [原文入口](../skse-menu-framework-3.md)

## 是什麼（別望文生義）

**不是** MCM 那種設定選單產生器，而是一個**通用遊戲內即時 GUI 畫布**：讓別的 mod 在遊戲畫面上疊自己的 ImGui 視窗／控件（按鈕、slider、input、table、tree、圖片、字型、圖示…整套 ImGui widget）。預設熱鍵 **F1** 開一個「Mod Control Panel」主視窗，各消費者 mod 把自己的頁面掛進去；也能開獨立浮動視窗、螢幕 HUD overlay。定位＝Skyrim 版的「按 F1 叫出開發者/工具面板」。

## 架構（讀 `framework/src/`）

<!-- wf-nav -->
- **渲染後端**：`Hooks.cpp` hook `IDXGISwapChain::Present`（vtable）+ `SetWindowLongPtrA` 換 `WndProc`（`WndProcHook::thunk`）攔輸入；ImGui 用官方 win32+dx11 backend。純疊加，不碰 Scaleform。
- **註冊一個選單**（消費者端，見下「介面」）：`SetSection` → `AddSectionItem(名稱, RenderFn)` 掛頁面；`AddWindow(RenderFn, pauseGame)` 開獨立視窗；`AddHudElement` 掛 overlay；`AddInputEvent` 攔按鍵。Render 函式是 `void __stdcall()`，每幀被呼叫，內部直接呼 ImGui。
- **控件型別**：**整套 Dear ImGui**（`ImGuiMCP::` 命名空間轉發）——Button/InputText/SliderInt/ColorEdit4/PlotLines/BeginTable/BeginChild/Image/MenuBar… 無自訂控件抽象層，就是 raw ImGui。
- **input/焦點**：WndProc 攔截；`AddInputEvent` callback 回傳 `bool` 決定是否吞掉該輸入（block）。`IsAnyBlockingWindowOpened()` 判斷玩家是否正被選單佔用。
- **開關熱鍵**：`SKSEMenuFramework.ini [General] ToggleKey`（預設 f1）+ `ToggleMode`（SinglePress/DoublePress）+ gamepad 熱鍵；`SetHotkeyEnabled(bool)` API 動態開關。
- **暫停/游標互動**：`GameLock.cpp` 用 `RE::Main::freezeTime` 凍結時間；ini `FreezeTimeOnMenu` / `BlurBackgroundOnMenu` 可調；**non-blocking 視窗**（`AddWindow(fn,false)` 或 `BlockUserInput=false`）不暫停遊戲、玩家仍可操作（overlay/HUD 用途）。
- **其他**：主題（`SKSEMenuFrameworkThemes/*.json` 熱插拔）、字型（`SKSE/Plugins/Fonts/*.ttf|otf` + 同名 `.json` 配大中小三尺寸，`PushFont`）、Font Awesome 圖示、多語系字型範圍（中/日/韓/西里爾/泰/土耳其 ini 開關 + 翻譯檔）、`LoadTexture`（SVG/DDS/PNG…）貼圖、開關選單 `Event`（kOpenMenu/kCloseMenu/kBeforeRender/kAfterRender）。

## 給消費者 mod 的介面（重點：純 C++，非資料驅動）

消費者**不連結** DLL，而是 include 一份 header shim：`GetModuleHandleW(L"SKSEMenuFramework")` + `GetProcAddress` 動態取每個 export（`AddSectionItem`/`AddWindow`/`LoadTexture`…），`IsInstalled()` 檢查 DLL 存在即 graceful skip。**最小註冊流程**（`example/src/UI.cpp` + `plugin.cpp`）：

```cpp
// plugin.cpp — 標準 CommonLibSSE-NG SKSE 進入點
SKSEPluginLoad(const SKSE::LoadInterface* skse) {
    SKSE::Init(skse);
    UI::Register();
    return true;
}
// UI.cpp
void UI::Register() {
    if (!SKSEMenuFramework::IsInstalled()) return;   // 沒裝就跳過
    SKSEMenuFramework::SetSection(MOD_NAME);          // 用 mod 名當分區
    SKSEMenuFramework::AddSectionItem("Add Item", Example1::Render); // 掛一頁
}
void __stdcall UI::Example1::Render() {              // 每幀呼叫，內部直接寫 ImGui
    ImGuiMCP::InputScalar("form id", ...);
    if (ImGuiMCP::Button("Search")) LookupForm();
    // 可直接呼 RE:: 遊戲 API，例如 player->AddObjectToContainer(...)
}
```

Render 函式裡能直接呼 CommonLib `RE::` 遊戲 API（範例：查 FormID → 加物品進玩家背包），所以它是「GUI + 直接操控遊戲物件」的組合。**沒有 JSON/ini 註冊選單這條路**——所有選單邏輯都是編譯進消費者 DLL 的 C++。

## 依賴 / 前置

- **本體**：SKSE64、CommonLibSSE-NG（`alandtse/CommonLibVR` ng 分支，同時涵蓋 SE/AE/VR）、Address Library、D3D11。vcpkg 拉 imgui 生態 + spdlog/simpleini/nanosvg/directxtk/nlohmann-json 等。
- **消費者 mod**：需 SKSE + CommonLibSSE-NG **自建 build 環境**（vcpkg + CMake + MSVC）寫 native plugin；runtime 只軟依賴本框架 DLL（沒裝就 `IsInstalled()` 跳過）。
- 與其他 QTR 元件無強耦合；本體自包含。

## 與其他 UI 路線對比

| 路線 | 技術 | 定位 |
| --- | --- | --- |
| **SKSE Menu Framework** | 原生 **Dear ImGui**（D3D11 hook）| 開發者/工具面板、即時控件、debug/editor 型 GUI；modder 寫 C++ |
| SkyUI / MCM（+ MCM Helper）| Flash / Scaleform `.swf` | 設定選單、貼合原生 UI 風格；MCM Helper 可 JSON 資料驅動 |
| UIExtensions | Scaleform 自訂選單（環選/列表）| 玩家互動選單，仍走 Flash |
| LoreBox | Scaleform loadMovie 注入 | 往既有 SkyUI 選單塞 tooltip |

差異核心：**ImGui = 程式碼即介面（immediate mode，C++）**，開發極快、控件豐富、但外觀非原生風、且**每個消費者都要出一支 DLL**；Scaleform 路線貼原生風、可 Papyrus/資料驅動、但做自訂控件痛苦。

