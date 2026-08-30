# 已知環境條件

[testing](../testing.md)

這台機器上會影響測試結果判讀的既有條件：

- 這台未安裝 Godot；兩個 Godot contract 的 source gate 會通過，runtime class 會明示 skip。
- `darksouls-port` 用 repo 自帶的 `venv/` 是 35/35 全過（2026-08-26 實測）。用系統 Python 會變成
  2 error / 19 skip（缺 numpy）——**那不是 repo 壞了，是跑錯直譯器**。
- ModForge 離線 suite 目前會輸出既有 nullable/xUnit analyzer warnings，但 1190 項全過。
