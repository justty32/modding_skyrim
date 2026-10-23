# 工具可攜性：repo 根的推導與乾淨 clone 驗證

[lessons 索引](README.md)

## tools-must-derive-repo-root-explicitly

> 工具用「自身相對位置」推 repo 根，在獨立 clone／搬目錄後會推錯——真樹永遠綠、乾淨 checkout 才現形的假綠燈（2026-10-23）

2026-10-23 同一天抓到同根因兩案：

- `agentctl/tools/brief_lint.py` 用 `Path(__file__).resolve().parents[2]` 推母 repo 根。agentctl 以 submodule 佈局活著時 parents[2] 恰好是母 repo；被獨立 clone 到任意位置時 parents[2] 是 clone 的上層目錄，所有點名 `agentctl/tools/…` 的合格交接書全被判「工具路徑不存在」——乾淨 clone 上 7 條測試假紅，真工作樹永遠綠。
- 孤兒工具三支（`reverify.py` 等）用 `../../../../` 相對層數定位 repo 根，handoffs 場次夾月結搬進 `done/<月>/` 後層數多一層，整支靜默壞掉。

**Why:** 「自身位置推根」隱性綁死目錄佈局，而佈局會變（submodule vs 獨立 clone、場次夾月結搬移、worktree）。壞的時候不是報錯，是**解析到不存在的路徑然後給出錯誤結論**；在開發機真樹上永遠測不到，只有乾淨 checkout 才現形。

**How to apply（正解階梯，由上而下 fallback）：**

1. **明確參數優先**：CLI 提供 `--root`／`--repo`，測試一律用它。
2. **問 git，不要數層**：自身 repo 根用 `git -C "$(dirname "$0")" rev-parse --show-toplevel`；需要**母 repo 根**時用 `git rev-parse --show-superproject-working-tree`（submodule 佈局回母根、獨立 clone 回空字串——空字串就是「沒有母根」的明確訊號，進入下一層 fallback，不要當錯誤吞掉）。
3. **前綴剝除 fallback**：解析「相對母根」的路徑（如 `agentctl/tools/x.py`）時，母根不可得就以自身 repo 根＋剝掉自己的前綴再試一次（brief_lint 2026-10-23 的修法，`032ad32f`）。
4. 環境變數覆蓋（如有）排在參數之後、推導之前。

**收線條件（新工具必做，寫進交接書驗收）：在乾淨 clone 上驗過一次**——`git clone --depth 1` 到臨時目錄，跑 `python3 -m unittest discover` 確認①新測試檔**有被 discover 抓到**（缺 `__init__.py` 之類會靜默跳過，見 2026-10-23 `repo_hooks/__init__.py` 漏 commit 一案：真樹 19 條測試在跑、乾淨 checkout 一條都不跑）、②整套綠。「工具報綠」不等於「真的驗過」，discover 抓不到的測試與推錯根的路徑檢查都是同一類靜默假綠燈。
