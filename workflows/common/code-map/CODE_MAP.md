# CODE_MAP — 程式碼導航 index

> 將本檔改成目標 repo 的實際結構。目標是讓 agent 修改前能快速定位相關檔案，只讀必要範圍。

## 子 index

| 子 index | 涵蓋 |
|----------|------|
| `CODE_MAP.core.md` | 核心 domain / business logic |
| `CODE_MAP.infra.md` | CLI / build / config / I/O / integration |
| `CODE_MAP.ui.md` | frontend / UI / routes / components |
| `CODE_MAP.tests.md` | tests / fixtures / test helpers |

不需要的子 index 可以刪除；領域不同就重命名。

## 修改前規則

1. 先判斷要改的功能屬於哪個領域。
2. 只讀對應子 index 列出的檔案。
3. 若 CODE_MAP 缺資料，以程式碼為準補上。

## 領域索引範本

每個子 index 建議使用這種格式：

```md
# CODE_MAP.<domain>

## Runtime / Production

| 檔案 | 職責 |
|------|------|
| `src/...` | TODO |

## Tests

| 檔案 | 覆蓋 |
|------|------|
| `tests/...` | TODO |

## Docs / Examples

| 檔案 | 用途 |
|------|------|
| `docs/...` | TODO |
```

