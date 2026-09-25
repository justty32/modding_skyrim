# API：StorageUtil（存取/列表）+ JsonUtil

← [papyrusutil](papyrusutil.md)

## 二、完整 API 表

### 2.1 StorageUtil — 儲存 / 讀取 scalar 值

本表整理「2.1 StorageUtil — 儲存 / 讀取 scalar 值」的逐項記錄。

已抽到 [papyrusutil-api-storage-json-scalar-storage.json](papyrusutil-api-storage-json-scalar-storage.json)（22 列）。

欄位「Function」：保留原表的Function。

欄位「簽名」：保留原表的簽名。

欄位「說明」：保留原表的說明。

統計：22 筆記錄，3 個欄位。


### 2.2 StorageUtil — 列表操作

所有列表函數都有 int / float / string / Form 四個型別版本，下表以「XList」代表四種。

本表整理「2.2 StorageUtil — 列表操作」的逐項記錄。

已抽到 [papyrusutil-api-storage-json-list-storage.json](papyrusutil-api-storage-json-list-storage.json)（23 列）。

欄位「Function」：保留原表的Function。

欄位「簽名（簡）」：保留原表的簽名（簡）。

欄位「說明」：保留原表的說明。

統計：23 筆記錄，3 個欄位。


**Prefix 計數 / 清除（跨物件）**：

| Function | 說明 |
|---|---|
| `CountIntValuePrefix(string PrefixKey)` | 計算所有物件上 key 前綴符合的 int value 數量 |
| `CountAllPrefix(string PrefixKey)` | 所有型別全部計 |
| `ClearIntValuePrefix(string PrefixKey)` | 清除所有物件上 key 前綴符合的 int value |
| `ClearAllPrefix(string PrefixKey)` | 所有型別全部清 |
| `CountObjXxxPrefix(Form, string)` | 限定物件的版本 |
| `ClearObjXxxPrefix(Form, string)` | 限定物件的版本 |

### 2.3 JsonUtil — 外部 JSON 檔案讀寫

基礎路徑：`data/skse/plugins/StorageUtilData/`。路徑中 `../` 表示向上一層。

| Function | 說明 |
|---|---|
| `Load(string FileName) → bool` | 手動載入（通常不需要，自動） |
| `Save(string FileName, bool minify=false) → bool` | 手動儲存 |
| `Unload(string FileName, bool saveChanges=true, bool minify=false) → bool` | 卸載並選擇是否存檔 |
| `IsPendingSave(string FileName) → bool` | 是否有未儲存的修改 |
| `IsGood(string FileName) → bool` | 檔案是否載入成功無錯誤 |
| `GetErrors(string FileName) → string` | 取得 JSON 解析錯誤訊息 |
| `JsonInFolder(string folderPath) → string[]` | 列出目錄中所有 .json 檔名 |
| `JsonExists(string FileName) → bool` | 檔案是否存在 |

scalar 讀寫（與 StorageUtil 相同模式，但第一個參數是 `string FileName`）：  
`SetIntValue / GetIntValue / HasIntValue / UnsetIntValue / AdjustIntValue`  
（同理 Float / String / Form 四種型別）

列表操作（同 StorageUtil 列表模式，第一個參數改為 `string FileName`）：  
`IntListAdd / IntListGet / IntListSet / IntListRemove / IntListRemoveAt / IntListInsertAt / IntListClear / IntListCount / IntListFind / IntListHas / IntListSlice / IntListResize / IntListCopy / IntListToArray / IntListRandom / IntListAdjust / IntListCountValue`  
（同理 Float / String / Form 四種型別）

**Path API（實驗性 JSON 路徑解析）**：

本表整理「2.3 JsonUtil — 外部 JSON 檔案讀寫」的逐項記錄。

已抽到 [papyrusutil-api-storage-json-json-path-functions.json](papyrusutil-api-storage-json-json-path-functions.json)（13 列）。

欄位「Function」：保留原表的Function。

欄位「說明」：保留原表的說明。

統計：13 筆記錄，2 個欄位。


