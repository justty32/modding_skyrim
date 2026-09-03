# 程式碼慣例 + CODE_MAP 維護鏈

碰原始碼的工作流共用這套規矩：[feature-dev](../feature-dev/README.md)、[refactor](../refactor/README.md)、[planning](../planning.md) 的詳規段。純文檔或調查類工作流按需參考。結構整理原則（被動）見 [STRUCTURE](../../STRUCTURE.md)。

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

規則：

1. 修改前先讀 CODE_MAP，找到相關領域，只讀該領域列出的檔案。
2. 新增/刪除原始碼檔案、檔案職責顯著改變、或測試搬家（Tests 欄）時，同步更新 CODE_MAP；**不因小型內部實作細節變動而更新**。
3. CODE_MAP 與程式碼衝突時，以程式碼為準，立即修正 CODE_MAP。
4. 原始碼檔案本身不加「對應 CODE_MAP」註釋；反向查找直接搜尋 CODE_MAP。

## 真相層優先序

各子專案可以改自己的優先序，但必須明確。預設：

```text
code/tests > schema/examples/fixtures > CODE_MAP > docs > generated/html
```

- 上層與下層衝突時，以上層為準並修正下層。
- generated/html 永遠不是唯一真相。
- research／analysis 的原始來源與摘要衝突時，以原始來源為準。
- CODE_MAP 是導航，不是規格；行為以 code/tests 為準。

## 多 Agent 並行

現行三層角色與模型分級見 [`agentctl/docs/team-model.md`](../../../agentctl/docs/team-model.md)，領地與互斥範圍見
[`agentctl/docs/line-claims.md`](../../../agentctl/docs/line-claims.md)，通訊與上游路由見
[`agentctl/tools/agent_inbox/PROTOCOL.md`](../../../agentctl/tools/agent_inbox/PROTOCOL.md)。
