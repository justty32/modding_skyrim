# 工具可攜性與輸入容錯：repo 根推導、乾淨 clone 驗證、合法輸入不喊錯、批次改名規則順序

[lessons 索引](README.md)

## tools-must-derive-repo-root-explicitly

> 工具用「自身相對位置」推 repo 根，在獨立 clone／搬目錄後會推錯——真樹永遠綠、乾淨 checkout 才現形的假綠燈（2026-10-23）

同根因兩案（2026-10-23）：`agentctl/tools/brief_lint.py` 用 `Path(__file__).resolve().parents[2]` 推母 repo 根，submodule 佈局下對、獨立 clone 時推到上層目錄，合格交接書全判「工具路徑不存在」；用 `../../../../` 數層定位的工具（`reverify.py` 等），場次夾月結搬進 `done/<月>/` 後多一層，整支靜默壞掉。

**Why:** 「自身位置推根」綁死目錄佈局（submodule vs 獨立 clone、月結搬移、worktree）；壞的時候不報錯，而是解析到不存在的路徑後給錯結論，在開發機真樹上測不到。

**How to apply（由上而下 fallback）：**

1. 明確參數優先：CLI 提供 `--root`／`--repo`，測試一律用它。
2. 問 git，不要數層：自身 repo 根用 `git -C "$(dirname "$0")" rev-parse --show-toplevel`；母 repo 根用 `git rev-parse --show-superproject-working-tree`（獨立 clone 回空字串＝沒有母根，進下一層 fallback，不當錯誤吞掉）。
3. 前綴剝除：解析相對母根的路徑（如 `agentctl/tools/x.py`）而母根不可得時，以自身 repo 根＋剝掉自己的前綴再試（brief_lint 的做法）。
4. 環境變數覆蓋（如有）排在參數之後、推導之前。

**收線條件（新工具必做，寫進交接書驗收）**：在乾淨 clone 上驗一次——`git clone --depth 1` 到臨時目錄跑 `python3 -m unittest discover`，確認①新測試檔有被 discover 抓到（缺 `__init__.py` 會靜默跳過：2026-10-23 `repo_hooks/__init__.py` 漏 commit，乾淨 checkout 一條都不跑）、②整套綠。

## tools-handle-legal-input-quietly-fail-loudly-on-missing-sources

> 工具遇到「不認識但完全合法」的輸入，預設行為是靜默跳過並計數，不是喊錯；「預期來源消失」才大聲失敗。同一天四案證明這是系統性傾向不是巧合（2026-10-23）

同族四案（2026-10-23），都是工具在正常輸入上輸出假訊號：`fomod_audit_all.py` 吃的 manifest 廢止後回空結果＋exit 0（假綠）；`brief_lint.py` 推錯母根（假紅，見上節）；`verify_ignore.sh` 特定情境回 PASS 但沒驗到（假 PASS）；`precommit_gate.py` 碰到 staged gitlink（mode 160000）走 `cat-file` 失敗印 `fatal`＋「合併衝突？」（假 fatal，收線 pin gitlink 是常態，噪音會讓真 fatal 被忽略）。

**Why:** 工具沒把「合法但非目標」與「出錯」分開。假綠燈讓人不查；假警報讓真警報被無視。

**How to apply：**

1. 合法但不認識／非目標的輸入（gitlink 不是 blob、範本檔滿是佔位、別線 staged 的檔）→ 靜默跳過＋計數，需要時輸出一行總數；不印 fatal、不猜原因（「合併衝突？」這種猜測字串不要出現在工具輸出）。
2. 預期的資料來源消失或讀不到（manifest 被廢止、checklist 基線不存在）→ 大聲失敗（exit 2＋ERROR），不准回空結果＋exit 0。
3. 新工具收線前跑一次「奇怪但合法」輸入：staged gitlink、空目錄、CRLF、並行刪檔（stat race）要安靜；來源檔不存在要響。

現成範例：`hygiene_audit.py`（stat race 接 OSError→跳過）、`profile_query.py`（缺 profile 檔進 `missing_files` 欄位）、`lock.sh`（殘鎖無 owner 檔→明確拒絕不猜測）。

## prefix-rename-rules-need-longest-first-ordering

> 批次改名規則若有前綴包含關係，短規則排在長規則前面會搶先命中、吃掉本該給長規則的字串

2026-08-27 把 `mco_*` 檔名轉 BFCO 命名時，短規則（`mco_powerattack`）排在長規則（`mco_powerattackloop`）前面會提前命中吃掉長字串、產生錯誤改名（`agentctl/handoffs/done/2026-08-27/cx-convert/RESULTS.md:11`）。程式只認第一個命中的規則，不會因為「語意上更精確」自動優先。

**How to apply:** 寫批次改名/替換規則表時，只要規則之間存在字首包含關係，一律把較長（較精確）的規則排在前面；測試 fixture 要刻意把短規則排前做負向對照，證明順序真的會咬到而不是空焗試。
