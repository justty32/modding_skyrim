# lessons — 從 Claude 記憶搬來的教訓庫

每個 `##` 小節是一條教訓：標題＝原記憶檔名 slug（記憶與其他文件以 slug 引用，**不改**），引言行＝一句 description，內文只留日期、事實、Why、How to apply 與使用者原話。lessons 是知識庫不是流程文件，單檔可超過 8 KB；同主題放同一檔，超過 16 KB 才按子主題分檔（檔名語意化，不用 `-N` 編號）。

**內容精簡**：2026-10-26 使用者裁示 lessons 也套內容精簡（[tidy 原則 5](../workflows/tidy/content-trim.md)）。事故經過的流水帳、改版經過、被推翻的舊說法（含刪除線段）直接刪，只留現行結論；刪掉的靠 `git log -p -- <檔>` 找。技術結論的來源位置（`path:line`、URL）照 AGENTS 鐵律 6 保留。

## 來源

小節來自 Claude 記憶目錄（`~/.claude/projects/-home-lorkhan-repo-moddings-skyrim/memory/`），之後新教訓直接寫進本目錄。**記憶目錄**：原檔全部仍在，`MEMORY.md` 尚未改成指向本目錄的指標——記憶目錄改寫由頂層處理；在那之前兩邊並存，記憶目錄較新。

## 分類表

<!-- wf-nav -->
| 檔案 | 主題 | 條數 |
|---|---|---|
| [user-preferences](user-preferences.md) | 使用者偏好與邊界 | 10 |
| [dispatch-roles](dispatch-roles.md) | 調度：頂層角色與誰來做 | 4 |
| [dispatch-delegation](dispatch-delegation.md) | 調度：模型分級與委派給誰 | 6 |
| [dispatch-leads-and-line-discipline](dispatch-leads-and-line-discipline.md) | 調度：領隊與線的運作紀律 | 5 |
| [dispatch-handoffs](dispatch-handoffs.md) | 調度：交接書與查證 | 6 |
| [dispatch-cli-agents](dispatch-cli-agents.md) | 調度：驅動 codex／tmux | 5 |
| [process-throttling](process-throttling.md) | 行程限流與別線行程的分寸 | 2 |
| [locks-screen-and-game](locks-screen-and-game.md) | 鎖、螢幕與開遊戲 | 7 |
| [repos-layout-and-remotes](repos-layout-and-remotes.md) | 版控：repo 佈局、remote 與 push | 5 |
| [git-commit-hygiene](git-commit-hygiene.md) | 版控：commit、pathspec 與工作樹 | 5 |
| [artifact-hygiene-and-ignores](artifact-hygiene-and-ignores.md) | 版控：產物衛生、.gitignore 與刪除前的掃描 | 4 |
| [docs-organization](docs-organization.md) | 文件整理：封存、拆檔與頁面歸屬 | 5 |
| [wf-kernel](wf-kernel.md) | wf 骨架（kernel）與工具形態 | 2 |
| [mo2-profiles](mo2-profiles.md) | MO2 profile 三檔：還原、並行編輯與遊戲改寫 | 5 |
| [mo2-behavior-quirks](mo2-behavior-quirks.md) | MO2 本體行為坑（首次啟動、幽靈 profile、靜默失效） | 6 |
| [mod-install-audit](mod-install-audit.md) | 裝／拔 mod 的稽核（裝前評估、安裝包對帳、FOMOD、同概念兄弟、LOD master、照抄選項的軟依賴） | 6 |
| [mod-library-bookkeeping](mod-library-bookkeeping.md) | mod 庫帳務、暫存與清理安全（身分辨識、欄位可信度、破壞性動作） | 5 |
| [asset-and-engine-loading](asset-and-engine-loading.md) | 素材存在性診斷與引擎載檔／runtime 狀態機制 | 3 |
| [housecarl-and-tools](housecarl-and-tools.md) | houseCARL 本體與其 Nexus／bridge 端點的坑 | 6 |
| [housecarl-on-linux](housecarl-on-linux.md) | houseCARL 在 Linux 的平台坑（路徑、環境變數、鏡像、靜默錯答） | 4 |
| [xedit-dyndolod-and-lod](xedit-dyndolod-and-lod.md) | xEdit、DynDOLOD 與 LOD 前置 | 3 |
| [plugin-bsa-and-script-formats](plugin-bsa-and-script-formats.md) | plugin／BSA／腳本的格式事實與量測陷阱 | 5 |
| [tool-portability](tool-portability.md) | 自製工具：repo 根推導、乾淨 clone 驗證、合法輸入不喊錯 | 2 |
| [this-machine](this-machine.md) | 本機環境特性（shell、行程、工具差異） | 3 |
| [faces-look-transplant](faces-look-transplant.md) | 臉：換臉流程與工具 | 4 |
| [faces-facegen-consistency](faces-facegen-consistency.md) | 臉：facegen 與頭部件一致性規則（大媽臉／素臉真因） | 4 |
| [faces-troubleshooting](faces-troubleshooting.md) | 臉與身體：排錯與升級 | 6 |
| [animation-oar](animation-oar.md) | 動畫與 OAR | 6 |
| [crash-dll-and-scripts](crash-dll-and-scripts.md) | CTD：SKSE DLL 與腳本 | 7 |
| [crash-data-and-assets](crash-data-and-assets.md) | CTD：資料層與素材 | 6 |
| [gameplay-bugs](gameplay-bugs.md) | 遊戲行為異常（非崩潰）的歸因 | 5 |
| [translation-and-zh](translation-and-zh.md) | 中文層部署 gate 與引擎的字串機制 | 6 |
| [zh-policy-and-naming](zh-policy-and-naming.md) | 中文層政策：翻不翻、繁簡與命名 | 4 |
| [zh-tooling-and-scans](zh-tooling-and-scans.md) | 中文層工具與掃描（zhport、靜態掃描、QA checker） | 5 |
| [project-decisions](project-decisions.md) | 專案裁示與開發／驗證流程的嚴謹度 | 6 |
| [map-port-and-world-conflicts](map-port-and-world-conflicts.md) | 地圖移植的引擎限制與世界／內容衝突 | 5 |
| [nexus-download-ops](nexus-download-ops.md) | Nexus 下載自動化（profile 複本、CDP、file_id、並行） | 4 |
| [porting-and-modforge](porting-and-modforge.md) | 資產移植與 ModForge 能力邊界 | 3 |

## 新增規則

新教訓寫進對應主題檔的一個 `##` 小節：標題／日期／事實／Why／How to apply；寫結論不寫經過。就地更正舊說法時直接改成現行結論，不留刪除線。主題檔超過 16 KB 時按子主題拆成語意化檔名，並更新上表。
