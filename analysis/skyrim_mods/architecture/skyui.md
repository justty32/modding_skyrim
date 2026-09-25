# SkyUI SE

## 定位

SkyUI 有兩個截然不同的身分，分析時必須分開看：

- **(a) 玩家面 —— UI 替換**：替換 vanilla 的物品欄、魔法、地圖、收藏等 Flash（Scaleform）介面，提供搜尋、排序、分欄等現代化操作。這部分的本體是 BSA 內的 `.swf`，**不是傳統 record**，從 ESP 層看不到，只能靠公開知識描述。
- **(b) mod 開發者面 —— MCM（Mod Configuration Menu）框架**：SkyUI 在系統選單裡掛出一個「Mod Configuration」分頁，任何 mod 只要寫一個 `extends SKI_ConfigBase` 的 quest script，就能在裡面註冊一個專屬設定頁（toggle / slider / 下拉等控制項）。整個 Skyrim modding 生態的「遊戲內設定 UI」幾乎都建立在這套機制上。

對 ModForge 而言，**(b) 才是重點**：它是「程式化生成的 mod 要不要有設定選單」這個問題的標準答案。(a) 是純美術與 Flash 工程，與 record 生成器無關。

與既有分析的對照：SkyUI 像 JContainers 一樣是「被別的 mod 依賴的基礎設施」（見 `jcontainers.md`），但 JContainers 是 native 資料結構 library，SkyUI 提供的是 **UI 服務面**。而 Sofia（見 `sofia-follower.md`）正是消費 SkyUI 的下游實例——它的 `JJSofiaMCM` quest 就是一個 MCM 設定頁。

<!-- wf-nav -->
- [檔案結構](skyui/files-and-records.md)
- [MCM 機制概述](skyui/mcm-and-modforge.md)
