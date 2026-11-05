# CHIM — headless plugin/save 工具研究

> 專案暫緩（2026-11-05），本夾凍結不更新；研究保留為知識正本。

研究對象是 [mojibake-dev/chim](https://github.com/mojibake-dev/chim)，不是同名 AI NPC 專案。它提供 Python library、MCP 與 Bethesda plugin/save 的位元組操作；本次只評估對 ModForge 的借鑑，不啟動整合或功能開發。

Done when: 已釘來源版本、以實作區分已有能力與缺口，列出可驗收的最小切片及不採納的範圍。

研究於 2026-11-02 完成，CHIM 固定在 [`461af0f`](https://github.com/mojibake-dev/chim/tree/461af0f7ac82032997a7ae4f50c7769b0c1447fe)，ModForge 對照版本為 `b60741b09a0301ee425532269a54513993a5d961`。方法是公開原始碼與測試的靜態閱讀，沒有安裝、執行 CHIM 或操作遊戲／存檔；提到既有測試不代表本輪重新執行。

主結論見 [對 ModForge 的借鑑](answers/modforge-fit.md)：獨立結構驗證、驗收後發布、出貨 manifest。一般 ModForge 出貨路徑與已完成的單模型 wrapper 分開判斷，避免重做後者。

## 原始碼與授權邊界

HEAD 的 [server.py](https://github.com/mojibake-dev/chim/blob/461af0f7ac82032997a7ae4f50c7769b0c1447fe/chim/server.py#L45-L87) 包含 Skyrim plugin/save 以外的 TES3/OpenMW/TES3MP 路線；README 不能當完整能力清單。plugin 操作透過 [ops.py](https://github.com/mojibake-dev/chim/blob/461af0f7ac82032997a7ae4f50c7769b0c1447fe/chim/esp/ops.py#L100-L129) 接外部 esplib；結構驗證仍保留另一套 reader，細節與限制見正文。

CHIM 的 [pyproject.toml:11](https://github.com/mojibake-dev/chim/blob/461af0f7ac82032997a7ae4f50c7769b0c1447fe/pyproject.toml#L11) 宣告 MIT，但該 commit 的 `git ls-files '*LICENSE*' '*COPYING*'` 無結果，未附獨立完整授權／copyright notice。它在 [pyproject.toml:41](https://github.com/mojibake-dev/chim/blob/461af0f7ac82032997a7ae4f50c7769b0c1447fe/pyproject.toml#L41) 釘選 `BadDogSkyrim/esplib@fb4e2759dac816453fff12e73d88c7101088006a`，該版本 [宣告 MPL-2.0](https://github.com/BadDogSkyrim/esplib/blob/fb4e2759dac816453fff12e73d88c7101088006a/pyproject.toml#L8)。概念參考與直接搬程式碼分開；不能把 CHIM 與其 backend 全視為 MIT。工作區 `agentctl/tools/esplib/` 是另一個同名工具，不能混為同一依賴。

回到 [analysis 導航](../README.md)。
