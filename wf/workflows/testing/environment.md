# 已知環境條件

[testing](../testing.md)

這台機器上會影響測試結果判讀的既有條件；工具是否存在要在執行當下重查，通過數以目標 repo 的
README／測試輸出為準：

- 這台未安裝 Godot；兩個 Godot contract 的 source gate 會通過，runtime class 會明示 skip。
- `darksouls-port` 必須用 repo 自帶的 `venv/`；用系統 Python 缺 numpy 時不是產品回歸。
- ModForge 離線 suite 的命令與當下 warnings／通過數只看該 repo README 與本次輸出，不沿用歷史數字。
