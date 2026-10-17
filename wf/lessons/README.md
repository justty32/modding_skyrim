# lessons — 從 Claude 記憶搬來的教訓庫

每個 `##` 小節是一條教訓（標題＝原記憶檔名 slug，引言行＝原 description，內文保留日期與 Why／How to apply）。lessons 是知識庫不是流程文件，單檔可超過 8 KB；同主題放同一檔，超過 16 KB 才按子主題分檔（檔名語意化，不用 `-N` 編號）。

## 搬家狀態

- 2026-09-26 memmig 把記憶目錄的 md 以腳本原文轉成小節（腳本已封存到 `wf/workflows/common/archive/`）；2026-10-17 WP-05 把 `-2`…`-9` 分檔合併成下表（內容逐行保留，無重複小節）。
- **未搬**：`interactive-grep-is-ugrep`、`pgrep-self-match-beyond-brackets`（原定進 `this-machine.md`，未建）；`overnight-agent-fleet-2026-08-20`、`aetheria-agent-coexistence`（原定判過期，未定案）；2026-09-26 之後新增的記憶條目也還沒搬。
- **記憶目錄**：原檔全部仍在，`MEMORY.md` 尚未改成指向本目錄的指標——記憶目錄改寫由頂層處理；在那之前兩邊並存，記憶目錄較新。

## 分類表

<!-- wf-nav -->
| 檔案 | 主題 | 條數 |
|---|---|---|
| [user-preferences](user-preferences.md) | 使用者偏好與邊界 | 10 |
| [dispatch-roles](dispatch-roles.md) | 調度：頂層角色與誰來做 | 4 |
| [dispatch-delegation](dispatch-delegation.md) | 調度：模型分級、委派與領隊 | 7 |
| [dispatch-handoffs](dispatch-handoffs.md) | 調度：交接書與查證 | 3 |
| [dispatch-cli-agents](dispatch-cli-agents.md) | 調度：驅動 codex／tmux 與行程 | 5 |
| [locks-screen-and-game](locks-screen-and-game.md) | 鎖、螢幕與開遊戲 | 7 |
| [repos-layout-and-remotes](repos-layout-and-remotes.md) | 版控：repo 佈局、remote 與 push | 5 |
| [git-commit-hygiene](git-commit-hygiene.md) | 版控：commit、工作樹與產物衛生 | 5 |
| [docs-organization](docs-organization.md) | 文件整理與 wf kernel | 4 |
| [mo2-profiles](mo2-profiles.md) | MO2 與 profile | 10 |
| [housecarl-and-tools](housecarl-and-tools.md) | houseCARL、xEdit、DynDOLOD 等工具坑 | 9 |
| [faces-look-transplant](faces-look-transplant.md) | 臉：換臉流程與 facegen 規則 | 7 |
| [faces-troubleshooting](faces-troubleshooting.md) | 臉與身體：排錯與升級 | 5 |
| [animation-oar](animation-oar.md) | 動畫與 OAR | 3 |
| [crash-dll-and-scripts](crash-dll-and-scripts.md) | CTD：SKSE DLL 與腳本 | 5 |
| [crash-data-and-assets](crash-data-and-assets.md) | CTD：資料層與素材 | 4 |
| [translation-and-zh](translation-and-zh.md) | 翻譯與中文層 | 7 |
| [project-decisions](project-decisions.md) | 專案裁示與地圖／內容限制 | 4 |

## 新增規則

新教訓寫進對應主題檔的一個 `##` 小節：標題／日期／事實／Why／How to apply。主題檔超過 16 KB 時按子主題拆成語意化檔名，並更新上表。
