# 程式碼慣例 + CODE_MAP 維護鏈

碰原始碼的工作流共用這套規矩：feature-dev、refactor、specs、plans。純文檔或調查類工作流按需參考。

## 程式碼慣例

- 遵守專案既有風格，不為小改動引入新架構。
- 大檔按職責拆分；建議 `src/` 單檔超過 300 行就檢視。
- 生成檔、schema、examples、fixtures 若會影響行為，視為源碼同步維護。
- breaking change 前先搜尋既有 examples、docs、tests，受影響者同一批更新。
- 新增公開 spec/API/config 欄位時，同步更新 schema、example、文件。

## CODE_MAP 維護鏈

程式碼導航 index 在 [code-map/CODE_MAP.md](code-map/CODE_MAP.md)。

維護鏈：

```text
程式碼（含 examples/assets/fixtures）→ CODE_MAP → 文檔
```

優先級：

```text
code/tests > schema/examples/fixtures > CODE_MAP > docs > generated/html
```

規則：

1. 修改前先讀 CODE_MAP，找到相關領域，只讀該領域列出的檔案。
2. 新增/刪除原始碼檔案，或檔案職責顯著改變時，同步更新 CODE_MAP。
3. CODE_MAP 與程式碼衝突時，以程式碼為準，立即修正 CODE_MAP。
4. 原始碼檔案本身不加「對應 CODE_MAP」註釋；反向查找直接搜尋 CODE_MAP。

## 多 Agent 並行

- 並行前先分互斥檔案或領域。
- 每個 agent 必須有自己的 `Done when:`。
- 共享 open 狀態寫 session-log。
- 整合者負責讀產物、解衝突、跑測試、同步 CODE_MAP/文檔。
