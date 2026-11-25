# 已知環境條件

[testing](../testing.md)

家裡那台機器上會影響測試結果判讀的既有條件；工具是否存在要在執行當下重查，通過數以目標 repo 的
README／測試輸出為準：

- 這台未安裝 Godot；兩個 Godot contract 的 source gate 會通過，runtime class 會明示 skip。
- `darksouls-port` 必須用 repo 自帶的 `venv/`；用系統 Python 缺 numpy 時不是產品回歸。
- ModForge 離線 suite 的命令與當下 warnings／通過數只看該 repo README 與本次輸出，不沿用歷史數字。

## 公司 WSL 那台（2026-11-25 查）

場地的差別見 [sites](../../org/sites.md)。這台跑離線測試時，下面幾種紅燈是環境造成的，不是產品回歸：

- **CRLF**：每個 repo 都在 local 設了 `core.autocrlf=true`，沒有 `*.sh text eol=lf` 的 repo，`.sh` 在工作樹是 CRLF，bash 會報 `bash\r` 或 `set: pipefail\r`。11-25 已替 10 個 `projects/*`、`instance/`、`mod-library/` 補上。直接執行的 `.py` 還沒有規則。補規則後要把工作樹的 `.sh` 刪掉重新 checkout。manifest hash 也會全紅，見 [tidy 的 Windows 坑](../tidy/gotchas-windows.md)。
- **缺套件**：Pillow 11-25 已用 apt 裝（`python3-pil`；公司網路偶爾連不到 archive，重試即可）；沒有 `dotnet`，ModForge 離線 suite 與 houseCARL 的 build 跑不了。
- **缺建置目錄**：沒有 `darksouls-port/venv/`，也沒有 `scene-capture-bridge/build/tests-native/`。
- **負載下的時序**：`agent-bridge` 的 `test_post_deadline_is_unknown_and_bounded` 在整批低優先序一起跑時紅過一次（`rejected` != `unknown`），單獨重跑 3 次都過。
- **Godot**：沒有，兩個 contract 跟家裡一樣明示 skip。
