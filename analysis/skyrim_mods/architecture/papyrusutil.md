# PapyrusUtil SE/AE (v4.6)

## 定位

SKSE plugin，與 JContainers 同類——都是「為 Papyrus 補資料儲存與工具函式」的依賴 library，本身**沒有任何遊戲內容**。但兩者走的是不同路線：

- **JContainers**：容器物件（JArray/JMap/JFormMap…）+ 路徑字串定址 + 容器生命週期管理。功能強、概念重，使用者要理解 root/temporary 容器與 GC。
- **PapyrusUtil**：**輕量、扁平的 KV**。不需要建立或管理任何容器物件——直接以 `(Form, key 字串)` 或 `(json 檔名, key 字串)` 為複合鍵存取 int/float/form/string 與 list。入門成本極低。

readme 一句話定位（`Readme - PapyrusUtilSE.txt` Description 段）：

> SKSE plugin that allows you to save any amount of int, float, form and string values on any form or globally from papyrus scripts. Also supports lists. These values can be accessed from any mod allowing easy dynamic compatibility.

「any mod can access」是它的設計哲學：所有 mod 共用同一個全域命名空間，靠 key 前綴（如 `rnd_hungervalue`）避免撞名，達成**零硬依賴的跨 mod 相容**（`StorageUtil.psc:37-58` 的註解詳述此用法）。

三大支柱：

| 支柱 | 鍵的形態 | 持久化位置 |
|---|---|---|
| **StorageUtil** | `(Form, key)` 或全域 `(none, key)` | 存檔內（co-save） |
| **JsonUtil** | `(json 檔名, key)` | **外部 .json 檔**（獨立於存檔，可遊戲外編輯） |
| **PapyrusUtil** | 無狀態 | 純陣列/字串/數值工具，無持久化 |

<!-- wf-nav -->
- [檔案結構](papyrusutil/files-and-storage-api.md)
- [PapyrusUtil —— 版本檢查 + 純陣列/字串/數值工具](papyrusutil/utility-api-and-design.md)
