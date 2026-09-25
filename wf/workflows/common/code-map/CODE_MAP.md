# CODE_MAP — 原始碼導航

本母 repo 主要保存分析與工作流文件；可建置的原始碼位於 `projects/` 的獨立
repo/submodule。修改前先從下表進目標專案，遵守該專案自己的 README、AGENTS 與
CODE_MAP。不存在的根層 source tree 不另造索引。

## 專案入口

內容見 [projects.md](projects.md)。

## agent-bridge semantic QA 快速圖

| 類別 | 檔案 | 職責 |
|------|------|------|
| Runtime | `projects/agent-bridge/src/GameActions.*`, `MessageBox.*`, `StateActors.*`, `State.*`, `Routes.*` | game-thread actor/dialogue/MessageBox actions、structured state、HTTP contract |
| Linux client | `projects/agent-bridge/client/bridge.py`, `qa_runner.py`, `qa_mcp.py` | HTTP calls、declarative QA steps、MCP semantic tools |
| Tests | `projects/agent-bridge/client/test_bridge.py`, `test_qa_runner.py`, `test_qa_mcp.py` | request shape、retry/validation、MCP routing |
| Docs | `projects/agent-bridge/README.md`, `client/README.md`, `client/QA-SCHEMA.md` | runtime API、client entry、qa.json contract |

新增／刪除原始碼檔案或改變職責時，先更新目標 repo 的 CODE_MAP；目標 repo 沒有
細分 CODE_MAP 時，才維護本頁的快速圖或 README 入口。

## 母 repo 本機工具

<!-- wf-nav -->
| 檔案 | 職責 |
|---|---|
| `tools/check_markdown_links.py` | 掃描母 repo 與非 `projects/` 工作區 submodules 的 tracked Markdown links；驗證檔案與 GitHub-style heading／explicit HTML anchors，理解 canonical symlink 位置，並支援 CI 的 `--skip-symlinks` 與 `--skip-uninitialized-submodules` 邊界（後者明報未初始化 gitlink 的未檢查目標，預設仍嚴格） |
| `tools/markdown_links/parsing.py` | 解析本機連結與 heading anchors，驗證連結目標。 |
| `tools/markdown_links/__init__.py` | Markdown 連結解析與驗證輔助套件入口。 |
| `tools/test_check_markdown_links.py` | Markdown link checker 的相對路徑、broken file／anchor、重複與 Setext heading、closed ATX heading、標題內含 inline link、fence（連結側與 anchor 側各一條）、CLI 與 symlink 行為；失敗訊息要指名缺哪個 anchor；Windows 缺 file-symlink privilege 時只 skip symlink-only cases |
| `tools/test_check_markdown_links_anchors.py` | 驗證 Unicode、Setext、重複標題、HTML 與 fenced code 的 anchor 行為。 |
| `tools/test_check_markdown_links_cli.py` | 驗證 CLI 錯誤、未初始化 submodule、來源排除與 symlink 選項。 |
| `tools/markdown_links_testlib.py` | 提供暫存目錄、symlink 權限處理與假 gitlink 的共用測試 fixture。 |
| `tools/check_submodule_pins.py` | pre-push 核心：只檢查本次 push ref 相對 remote tip 有變動的 gitlink；本機存在但任何 remote-tracking ref 都不可達時 fetch 後 fail closed |
| `tools/submodule_pins/pins.py` | 解析 push updates，計算變動 gitlink 與新分支 pins。 |
| `tools/submodule_pins/__init__.py` | gitlink pin 計算與 remote 可達性檢查套件入口。 |
| `tools/submodule_pins/branches.py` | 檢查 remote 可達性、推導 push 目標分支並警告側分支依賴。 |
| `tools/submodule_pins/guard.py` | 檢查變動 submodule pins，依遞迴推送模式回報推送指引。 |
| `tools/test_check_submodule_pins.py` | 以臨時 bare remote、母 repo 與真實 submodule 驗未變／已推／未推 pin、未初始化／本機缺 commit 與刪分支邊界 |
| `tools/test_check_submodule_pins_recurse.py` | 驗證 on-demand／only／check 遞迴推送模式的 pin 阻擋與側分支警告。 |
| `tools/submodule_pins_testlib.py` | 提供帶真實 submodule 與暫存 remotes 的共用 pin guard 測試 fixture。 |
| `tools/check_code_map_coverage.py` | 檢查每一支工具腳本是否在某份索引頁被指名；**走訪各 submodule 自己的 git**，不靠母 repo 的 `git ls-files`（它到 gitlink 就停，正是 `check_markdown_links.py` 出過的洞）。已知缺口以 `code_map_coverage_baseline.txt` 當 ratchet：清單內靜默、清單外一律非零 exit；baseline 指到已刪除的檔案也 fail closed，清單不會腐化成永久藉口 |
| `tools/code_map_coverage_baseline.txt` | ratchet 的豁免清單，**目前是空的**（2026-08-26 盤點時 36 支未索引，同日全部補進本頁）。留著是為了下一次真的有不該進索引的腳本時寫上路徑與理由；**是債不是豁免**，且 stale 行會 fail closed |
| `tools/test_check_code_map_coverage.py` | 以真實巢狀 submodule 的合成工作區驗已索引／未索引／submodule 內可達／baseline 靜默／baseline 不通殺／stale baseline／未追蹤檔不算數；7 條全部經突變測試證明能變紅 |
| `mod-library/db/*`、`mod-library/l10n/tools/*` | **索引不放這裡**——`mod-library` 是 private （含他人 mod 的完整 ESP 複本），連腳本清單都不進 public 母 repo。逐支職責見該 repo 內的 `db/README.md` 與 `l10n/tools/README.md` |
| `instance/tools/*`、`instance/profiles/tools/*` | **索引不放這裡**——母 repo 是 public，該 repo 是 private，逐支職責見該 repo 的 `tools/README.md` 與 `profiles/tools/README.md` |
| `agentctl/tools/*` | **索引不放這裡**——母 repo 是 public，該 repo 是 private，逐支職責見該 repo 的 `tools/README.md`（含 `agent_inbox/`） |
