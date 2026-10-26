# 工具可攜性與輸入容錯：repo 根推導、乾淨 clone 驗證、合法輸入不喊錯

[lessons 索引](README.md)

## tools-must-derive-repo-root-explicitly

> 工具用「自身相對位置」推 repo 根，在獨立 clone／搬目錄後會推錯——真樹永遠綠、乾淨 checkout 才現形的假綠燈（2026-10-23）

同根因兩案（2026-10-23）：

- `agentctl/tools/brief_lint.py` 用 `Path(__file__).resolve().parents[2]` 推母 repo 根：submodule 佈局下恰好是母 repo，獨立 clone 時是 clone 的上層目錄，點名 `agentctl/tools/…` 的合格交接書全被判「工具路徑不存在」——乾淨 clone 假紅，真工作樹永遠綠。
- 用 `../../../../` 相對層數定位 repo 根的工具（`reverify.py` 等），handoffs 場次夾月結搬進 `done/<月>/` 後層數多一層，整支靜默壞掉。

**Why:** 「自身位置推根」隱性綁死目錄佈局，而佈局會變（submodule vs 獨立 clone、場次夾月結搬移、worktree）。壞的時候不是報錯，是**解析到不存在的路徑然後給出錯誤結論**；在開發機真樹上永遠測不到，只有乾淨 checkout 才現形。

**How to apply（正解階梯，由上而下 fallback）：**

1. **明確參數優先**：CLI 提供 `--root`／`--repo`，測試一律用它。
2. **問 git，不要數層**：自身 repo 根用 `git -C "$(dirname "$0")" rev-parse --show-toplevel`；需要**母 repo 根**時用 `git rev-parse --show-superproject-working-tree`（submodule 佈局回母根、獨立 clone 回空字串——空字串就是「沒有母根」的明確訊號，進入下一層 fallback，不要當錯誤吞掉）。
3. **前綴剝除 fallback**：解析「相對母根」的路徑（如 `agentctl/tools/x.py`）時，母根不可得就以自身 repo 根＋剝掉自己的前綴再試一次（brief_lint 的做法）。
4. 環境變數覆蓋（如有）排在參數之後、推導之前。

**收線條件（新工具必做，寫進交接書驗收）：在乾淨 clone 上驗過一次**——`git clone --depth 1` 到臨時目錄，跑 `python3 -m unittest discover` 確認①新測試檔**有被 discover 抓到**（缺 `__init__.py` 之類會靜默跳過：2026-10-23 `repo_hooks/__init__.py` 漏 commit，真樹測試在跑、乾淨 checkout 一條都不跑）、②整套綠。「工具報綠」不等於「真的驗過」，discover 抓不到的測試與推錯根的路徑檢查都是同一類靜默假綠燈。

## tools-handle-legal-input-quietly-fail-loudly-on-missing-sources

> 工具遇到「不認識但完全合法」的輸入，預設行為是靜默跳過並計數，不是喊錯；「預期來源消失」才大聲失敗。同一天四案證明這是系統性傾向不是巧合（2026-10-23）

同族四案（2026-10-23），全部是「工具在正常輸入上輸出假訊號」：

- **假綠燈**：`fomod_audit_all.py` 吃的 manifest 廢止後靜默回空結果＋exit 0，覆蓋率不足還報綠。
- **假紅燈**：`brief_lint.py` 推錯母 repo 根，乾淨 clone 上合格交接書全判「工具路徑不存在」（見上一節）。
- **假 PASS**：gitignore 一致化的 `verify_ignore.sh` 在特定情境回 PASS 但實際沒驗到（gitignore 線 REPORT）。
- **假 fatal**：`precommit_gate.py` 碰到 staged gitlink（mode 160000，pin submodule 的常態）走 `cat-file` 失敗，印 `fatal`＋「合併衝突？」的猜測——本工作區幾乎每次收線都 pin gitlink，等於常態噪音，而噪音會讓真 fatal 被忽略。

**Why:** 這四個都不是輸入壞掉，是**工具沒把「合法但非目標」與「出錯」分開**。假綠燈比沒工具糟（信了就不查）；假警報比安靜糟（狼來了之後真警報被無視）。

**How to apply（判準三條）：**

1. **合法但不認識／非目標的輸入**（gitlink 不是 blob、範本檔滿是佔位、別線 staged 的檔）→ **靜默跳過＋計數**，needed 時輸出一行總數；不印 fatal、不猜原因（「合併衝突？」這種猜測性字串永遠不要出現在工具輸出）。
2. **預期的資料來源消失或讀不到**（manifest 被廢止、checklist 基線不存在）→ **大聲失敗（exit 2＋ERROR）**，不准回空結果＋exit 0。
3. 新工具收線前跑一次「奇怪但合法」輸入清單：staged gitlink、空目錄、CRLF、並行刪檔（stat race）、來源檔不存在——前四種要安靜，最後一種要響。

符合判準的現成範例：`hygiene_audit.py`（stat race 接 OSError→跳過）、`profile_query.py`（缺 profile 檔進 `missing_files` 欄位不報錯）、`lock.sh`（殘鎖無 owner 檔→明確拒絕不猜測）。
