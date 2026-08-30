# 綠燈不等於有檢查：四個實例與推論

[testing](../testing.md)｜規則本身（新增或修改一道檢查時要證明它能變紅）在入口。

## 2026-08-23 一天抓到的四個恆真檢查

欄位：`檢查`／`為什麼恆真`。查法（從 `wf/workflows/testing/` 算相對路徑）：

```
python3 ../../../tools/tabledb.py green-light-evidence.json
python3 ../../../tools/tabledb.py green-light-evidence.json get 0
```

共 4 筆。

## 兩個相關的推論

- **檢查器的涵蓋範圍要跟著結構走。** 拆出 submodule、搬走目錄之後，
  要回頭確認檢查器還看得到那些地方。
- **靜態全過不等於畫面上是對的。** 方框、mojibake、截斷、手感只有人眼看得出來；
  這類項目記到 [WAIT_USER.md](../../../WAIT_USER.md)，不要自己宣稱通過。
