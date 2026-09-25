# PapyrusUtil SE/AE (v4.6) — files-and-storage-api

[返回入口](../papyrusutil.md)

## 檔案結構

來源：`~/skyrim_mods/PapyrusUtil/`

| 路徑 | 內容 |
|---|---|
| `SKSE/Plugins/PapyrusUtil.dll` | native 核心（約 1.4 MB） |
| `Scripts/*.pex` | 6 個編譯後腳本（ActorUtil / JsonUtil / MiscUtil / ObjectUtil / PapyrusUtil / StorageUtil） |
| `Scripts/Source/*.psc` | **完整 API 原始碼**（同名 6 份，可讀） |
| `Source/Scripts/*.psc` | 同上的 CK source 路徑複本（v3.41 起複製到 `/source/scripts`） |
| `Readme - PapyrusUtilSE.txt` | 說明文件 |

依賴（readme Requirements 段）：SKSE64 SE/AE 2.2.6+、Skyrim SE/AE 1.6.1170、**Address Library for SKSE Plugins**（Nexus #32444）。

JsonUtil 的外部檔起始目錄是 `data/skse/plugins/StorageUtilData/`，檔名可含相對路徑與省略副檔名（`JsonUtil.psc:12-21`）。

## Papyrus API 面（按函式數排序）

來源：`~/skyrim_mods/PapyrusUtil/Scripts/Source/*.psc`

| 模組 | 函式數 | 職責 |
|---|---|---|
| `StorageUtil.psc` | 286 | 在 form 上或全域存 int/float/form/string 與 list，用 form+key 取回（核心） |
| `JsonUtil.psc` | 138 | 同 StorageUtil 但存到**外部 .json 檔**，可遊戲外編輯、獨立於存檔 |
| `PapyrusUtil.psc` | 101 | 版本檢查 + 陣列/字串/數值工具（無狀態） |
| `MiscUtil.psc` | 23 | TFC 飛行鏡頭、TM 選單開關、cell 掃描、檔案 IO、印 console 等雜項 |
| `ActorUtil.psc` | 6 | actor 的 AI package override 堆疊 |
| `ObjectUtil.psc` | 8 | 替換選定物件的動畫（**SE 已停用**，見下） |

函式數之所以龐大，是因為每個操作都對 int/float/string/Form **四型各一份**，再乘上 value 與 list 兩種形態、以及一系列衍生（Has/Unset/Pluck/Adjust/Count…）。實際「概念」遠少於函式數。

### StorageUtil —— 核心 `(Form, key)` KV

複合鍵的設計集中在前 4 個型別組（`StorageUtil.psc:77-115`）：

```papyrus
int    function SetIntValue(Form ObjKey, string KeyName, int value) global native      ; :77
float  function SetFloatValue(Form ObjKey, string KeyName, float value) global native   ; :78
string function SetStringValue(Form ObjKey, string KeyName, string value) global native ; :79
Form   function SetFormValue(Form ObjKey, string KeyName, Form value) global native     ; :80

int    function GetIntValue(Form ObjKey, string KeyName, int missing = 0) global native ; :112
Form   function GetFormValue(Form ObjKey, string KeyName, Form missing = none) global native ; :115
```

關鍵語意（`StorageUtil.psc:70-114` 註解）：

- `ObjKey` 設 `none` 即「全域」儲存；給任意 `Form` 即「掛在該 form 上」——這就是 per-form 狀態表的入口。
- key（`KeyName`）大小寫不敏感；四個型別各自獨立命名空間（`SetIntValue(none,"abc",1)` 與 `SetFloatValue(none,"abc",2.0)` 互不影響，`:27-35`）。
- `Get*` 帶 `missing` 預設值，缺鍵時回傳它。
- form 被刪除時，掛在其上的值會在下次存檔時清掉（`:11-13`）。

list 版以同樣的 `(Form, key)` 複合鍵指向一個有序串列（`StorageUtil.psc:150-284`）：

```papyrus
int  function FormListAdd(Form ObjKey, string KeyName, Form value, bool allowDuplicate = true) global native ; :153
Form function FormListGet(Form ObjKey, string KeyName, int index) global native                              ; :165
int  function FormListCount(Form ObjKey, string KeyName) global native                                       ; :284
int  function IntListAdd(Form ObjKey, string KeyName, int value, bool allowDuplicate = true) global native   ; :150
```

衍生操作齊全：`Pluck*`（取出即刪，`:124-127`）、`Adjust*`（±現值，`:137-138`）、`*ListShift/*ListPop`（頭尾取出，`:198-211`）、`*ListSort/*ListSlice/*ListToArray`（`:327-388`）、`Count*ValuePrefix` / `Clear*ValuePrefix`（按 key 前綴批次統計或清除，`:424-492`）。另有 `FileXxx` 一整組（`:568-806`）已 **DEPRECATED**，內部全部轉呼 `JsonUtil` 寫到共用的 `../StorageUtil.json`。

### JsonUtil —— 把命名空間換成「外部 json 檔名」

函式表面與 StorageUtil 幾乎一一對應，唯一差別是把首參數從 `Form ObjKey` 換成 `string FileName`（`JsonUtil.psc:7-11` 明說「work in exactly the same way」）：

```papyrus
int  function SetIntValue(string FileName, string KeyName, int value) global native        ; :56
Form function SetFormValue(string FileName, string KeyName, form value) global native       ; :59
int  function GetIntValue(string FileName, string KeyName, int missing = 0) global native   ; :61
int  function FormListAdd(string FileName, string KeyName, Form value, bool allowDuplicate = true) global native ; :79
```

檔案生命週期函式（`JsonUtil.psc:33-53`）：

```papyrus
bool function Load(string FileName) global native                              ; :33
bool function Save(string FileName, bool minify = false) global native         ; :34
bool function Unload(string FileName, bool saveChanges = true, ...) global native ; :35
bool function IsGood(string FileName) global native                            ; :40  (parser 無誤?)
string function GetErrors(string FileName) global native                       ; :42  (格式化錯誤字串)
```

一般情況**不必手動 Load/Save**：玩家存檔時所有被改過的 json 自動寫回（`:23-28`）。

JsonUtil 還有 StorageUtil 沒有的**任意路徑存取**（v3.3 加入，`:175-228`），可讀寫任意 json 結構，適合自訂格式的資料表：

```papyrus
int  function GetPathIntValue(string FileName, string Path, int missing = 0) global native ; :190
function SetPathIntValue(string FileName, string Path, int value) global native            ; :183
int[] function PathIntElements(string FileName, string Path, int invalidType = 0) global native ; :198
```

範例（`:177-180`）：對 `{ "foo": { "bar": [3,10,7] } }` 呼叫 `GetPathIntValue("filename.json", ".foo.bar[1]")` 回傳 `10`。

