# user — 使用者偏好與確認邊界

[common/README](README.md)

agent 不用重猜的事。always-on 鐵律在 `AGENTS.md`，這裡是**這位使用者**的偏好——改了改這裡，不改鐵律。

| 項目 | 設定 |
|------|------|
| 語言 | 回覆與文件一律**繁體中文**；技術專名（mod 名、API、指令、欄位）留原文。**mod 層繁簡皆可**——要的是有中文，不是正體；缺字破版才是硬 gate |
| 分支慣例 | 直接 commit `main`，不開 branch 走 PR；**push 要使用者當場確認**（依鐵律 2）|
| 直接做、不用問 | 改文件、跑唯讀指令（`git status`／`grep`／`find`／查 Nexus）、跑測試與 lint |
| 一定先問 | push、刪檔、動 `instance/`（MO2 profile／load order／已裝 mod）、動 DB（mod-library 的 MongoDB）、安裝依賴、開新的大型工作 |
| 回覆風格 | 短、先結論。使用者問「**要不要**」時不要只回「不必」，附上可執行的判準（門檻數字）與後果，讓他能改數字 |
| 時區 | Asia/Taipei |

領域詞彙常猜錯 → 開 `glossary.md`（見 [common/README](README.md)）。
