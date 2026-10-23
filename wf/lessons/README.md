# lessons — 從 Claude 記憶搬來的教訓庫

每個 `##` 小節是一條教訓（標題＝原記憶檔名 slug，引言行＝原 description，內文保留日期與 Why／How to apply）。lessons 是知識庫不是流程文件，單檔可超過 8 KB；同主題放同一檔，超過 16 KB 才按子主題分檔（檔名語意化，不用 `-N` 編號）。

## 搬家狀態

- 2026-09-26 memmig 把記憶目錄的 md 以腳本原文轉成小節（腳本已封存到 `wf/workflows/common/archive/`）；2026-10-17 WP-05 把 `-2`…`-9` 分檔合併成下表（內容逐行保留，無重複小節）；2026-10-18 `mo2-profiles` 加新條會超過 16 KB，把裝／拔 mod 稽核四條原文搬到 `mod-install-audit`。
- 2026-10-23 tidy E1 補搬 09-26 之後新增的條目與原先點名未搬的 4 條：新增 14 個小節（新建 `this-machine.md`、`gameplay-bugs.md`），就地更新 6 個小節。3 條判過期／流水帳不搬（`aetheria-agent-coexistence`、`overnight-agent-fleet-2026-08-20`、`install-day-2026-10-10`），1 條與既有小節同義未另開。逐條對照表在 `agentctl/handoffs/home-2026-10-23/tidy/E1/REPORT.md`。
- **記憶目錄**：原檔全部仍在，`MEMORY.md` 尚未改成指向本目錄的指標——記憶目錄改寫由頂層處理；在那之前兩邊並存，記憶目錄較新。

## 分類表

<!-- wf-nav -->
| 檔案 | 主題 | 條數 |
|---|---|---|
| [user-preferences](user-preferences.md) | 使用者偏好與邊界 | 10 |
| [dispatch-roles](dispatch-roles.md) | 調度：頂層角色與誰來做 | 4 |
| [dispatch-delegation](dispatch-delegation.md) | 調度：模型分級、委派與領隊 | 10 |
| [dispatch-handoffs](dispatch-handoffs.md) | 調度：交接書與查證 | 3 |
| [dispatch-cli-agents](dispatch-cli-agents.md) | 調度：驅動 codex／tmux 與行程 | 6 |
| [locks-screen-and-game](locks-screen-and-game.md) | 鎖、螢幕與開遊戲 | 7 |
| [repos-layout-and-remotes](repos-layout-and-remotes.md) | 版控：repo 佈局、remote 與 push | 5 |
| [git-commit-hygiene](git-commit-hygiene.md) | 版控：commit、工作樹與產物衛生 | 5 |
| [docs-organization](docs-organization.md) | 文件整理與 wf kernel | 4 |
| [mo2-profiles](mo2-profiles.md) | MO2 與 profile | 7 |
| [mod-install-audit](mod-install-audit.md) | 裝／拔 mod 的稽核（安裝包對帳、FOMOD、同概念兄弟、LOD master、照抄選項的軟依賴、暫存清理的可回復性判準） | 6 |
| [housecarl-and-tools](housecarl-and-tools.md) | houseCARL、xEdit、DynDOLOD 等工具坑 | 9 |
| [this-machine](this-machine.md) | 本機環境特性（shell、行程、工具差異） | 2 |
| [faces-look-transplant](faces-look-transplant.md) | 臉：換臉流程與 facegen 規則 | 7 |
| [faces-troubleshooting](faces-troubleshooting.md) | 臉與身體：排錯與升級 | 5 |
| [animation-oar](animation-oar.md) | 動畫與 OAR | 3 |
| [crash-dll-and-scripts](crash-dll-and-scripts.md) | CTD：SKSE DLL 與腳本 | 5 |
| [crash-data-and-assets](crash-data-and-assets.md) | CTD：資料層與素材 | 4 |
| [gameplay-bugs](gameplay-bugs.md) | 遊戲行為異常（非崩潰）的歸因 | 3 |
| [translation-and-zh](translation-and-zh.md) | 翻譯與中文層 | 8 |
| [project-decisions](project-decisions.md) | 專案裁示與地圖／內容限制 | 7 |

## 新增規則

新教訓寫進對應主題檔的一個 `##` 小節：標題／日期／事實／Why／How to apply。主題檔超過 16 KB 時按子主題拆成語意化檔名，並更新上表。
