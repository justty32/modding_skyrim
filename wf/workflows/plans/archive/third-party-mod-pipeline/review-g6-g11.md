# 重審補漏 G6–G11 與 D5 簡化

> 屬於 [第三方 mod 取得–安裝–驗證流水線](README.md)。

## 七、重審補漏（2026-08-04，動工前對抗式複查）（續）


### G6 — 要版控的不是三個檔，是整個 profile 資料夾（D3 修正）

實查 profile 內容：`modlist.txt`、`plugins.txt`、`loadorder.txt`、**`archives.txt`**、`lockedorder.txt`、`initweaks.ini`、`settings.ini`、`skyrim.ini`、`skyrimcustom.ini`、`skyrimprefs.ini`。

D3 原文寫「profile 三檔」是錯的。ini 類也必須版控——有些 mod 要求 ini 修改，那些改動同樣需要能回滾。另外 `.mo2ctl-backups/` 要進 `.gitignore`；`modlist.txt.bak-before-agentbridge`（上游 0.3 留下的）是殘骸，可清。

### G7 — 下載工作單缺「對照已裝」這一步（D5 修正）

109 個 mod 已涵蓋大多數常見前置（SkyUI、MCM Helper、po3 全套、PapyrusUtil、JContainers、RaceMenu、XPMSE、FNIS…）。工作單若不 diff 已裝清單，會叫使用者重下已經有的東西——而**重裝框架就是 G4 的觸發路徑**。

工作單必須對每個依賴標記三態：已裝且版本足夠（跳過）／已裝但版本不足（升級，且標明風險）／未裝（下載）。查法用 `housecarl_load_order_status(lookup=...)` + `housecarl_skse_inventory(filter=...)`。

### G8 — AgentBridge 現在就在玩家 load order 裡

`modlist.txt:3` 是 `+AgentBridge`，`skse_inventory` 確認 `AgentBridge.dll` v0.3.0 已啟用。也就是**每次正常玩遊戲都開著 5099 這個會執行任意 console 指令的 port**。這與它自己的設計意圖相反（上游 1.1：「測試治具，每次 QA 跑完就卸，絕不能進玩家 load order」）。已補為 P0.5。

（`SceneCaptureBridge` 同樣在啟用中，但那是作者工具、使用者自己在用，不同性質，不動。）

### G9 — SkyLinkAI 已經是第二套遊戲內 MCP

`skse_inventory` 查到 `SkyrimMCPPlugin.dll` + `SkyLinkAI_Server\{SkyrimMCP,ModelContextProtocol,ModelContextProtocol.Core}.dll`（mod 名 `SkyLinkAI`）。

兩個待確認：(a) 在為 D4 延後的「技能／法術清單」動手改 `State.cpp` 之前，**先看 SkyLinkAI 是否已經暴露那些欄位**，可能省掉整個 C++ 改動；(b) 兩套 in-game server 是否搶 port 或 hook——AgentBridge 固定 5099，SkyLinkAI 用什麼未查。

### G10 — 沒有衝突解決 patch 這一步

實查確認 load order 裡**沒有** bashed／smashed／merged patch（所以「加 mod 要重生 bashed patch」這條不適用，是好消息）。

但反面是：目前純靠排序決定衝突勝負，兩個 mod 都要改同一筆記錄時只能二選一。houseCARL 有 `housecarl_forward_record` / `housecarl_bulk_apply` / `housecarl_cross_plugin_query` 正是做這個的，而本計畫沒有「必要時產 patch plugin」這一步。暫不列入 Done when（會讓範圍膨脹），但要記著這是排序解不了的那一類問題的出口。

### G11 — baseline 只有一份 level-1 空手存檔

上游 D2 記「baseline 組合不預先擴充」是使用者決定，成立。但第三方 mod 會比 no-op plugin 更快撞到這面牆：level 1、無 perk、無裝備 → 等級門檻、perk 門檻、前置任務都測不到。**預期 P4 就會需要第二份 baseline**，屆時再開，但別當意外。

### 對 D5 的簡化（2026-08-04）

多來源分工收斂為單一原則：**AI 讀公開頁面與翻譯，不代抓需登入的站或匿名檔案空間的二進位檔**。
