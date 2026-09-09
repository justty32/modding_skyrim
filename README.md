# Skyrim modding 工作區

這裡集中放 Skyrim SE modding 的開發、分析、部署與產物。母 repo 是 public；各條工作線各自獨立版控，母 repo 用 submodule 連進來。

## 四條主線

2026-08-23 統整後，日常工作分成四條獨立 repo：

| 線 | 管什麼 | 可見性 |
|---|---|---|
| [`instance/`](instance/) | 本機部署狀態：MO2 instance、現役 profile `modpack-main`、load order、已裝 mod 與 profile 稽核工具 | private |
| [`mod-library/`](mod-library/) | 本地 mod 庫：MongoDB 索引、自製繁中翻譯層、自製插件與修正 esp、庫稽核 | private |
| [`modpack-design/`](modpack-design/) | 整合包設計：Gameplay 遷移批次、技術債與選型調查 | private（暫時） |
| [`agentctl/`](agentctl/) | AI 操控 Skyrim 的總控：工作流、插件編排、agent 交接、QA harness 與執行證據 | private（暫時） |

`mod-library` 必須永遠 private，因為翻譯層有他人 mod 的完整原始 ESP 複本。`modpack-design` 和 `agentctl` 暫時也是 private，等逐檔審查後再決定能否公開。不要從這個 public 母 repo 推論子 repo 的公開範圍。

## 你來找什麼?

<!-- wf-nav -->
| 你要找的 | 去哪裡 |
|---|---|
| 做好的 mod、plugin、翻譯或修正 esp | [`mod-library/`](mod-library/)：`l10n/mods/` 是翻譯層、`plugins/` 是 SKSE DLL、`artifacts/` 是修正 esp；每個成品資料夾有 `SOURCE.md` 記來源。歷史自製成品在 `~/skyrim_mods/mine/`（DSPort*/ModForge*/MF* 系列），依使用者決定留在原地。 |
| 現在裝了什麼、load order 是什麼 | [`instance/`](instance/) |
| 整合包要做什麼、技術債與選型 | [`modpack-design/`](modpack-design/) |
| 叫 AI 下載、操作遊戲或做驗收 | [`agentctl/`](agentctl/) |
| 今天或最近一場從哪裡接著做 | [`agentctl/handoffs/NEXT-SESSION.md`](agentctl/handoffs/NEXT-SESSION.md) |
| 使用者想要、尚待調查的 mod | [`mods-user-want.md`](mods-user-want.md) |
| 開發中的原始碼 | [`projects/`](projects/README.md) |
| 引擎、SKSE、mod 與工具的研究筆記 | [`analysis/`](analysis/README.md) |
| 外部框架原始碼 | [`external/`](external/README.md)；他人的 mod、框架與參考素材實體在 `~/skyrim_mods/`（125 GB，依使用者決定留在原地）。 |

## `projects/` 裡有什麼

所有開發 repo 的用途、彼此的協議關係，以及 submodule 更新和一次 push 的設定，都在 [`projects/README.md`](projects/README.md)。

## 不進版控的東西

| 東西 | 位置 | 原因 |
|---|---|---|
| mod 下載庫 | `~/skyrim_mods/`（125 GB） | 體積 |
| 舊場次實機截圖 | `~/notes/projects/modding/skyrim/logs/`（88 MB） | 歷史證據；近期截圖在 `agentctl/handoffs/**/runtime/`，同樣不進版控 |
| 歷史 MongoDB 快照 | `~/notes/projects/modding/skyrim/backups/`（86 MB） | 歷史備份；現役部署狀態已歸 [`instance/`](instance/) |
| QA baseline 存檔 | `~/games/skyrim-qa-baselines`（3.1 MB） | 刻意放在 repo 外，作為唯讀主檔 |
| houseCARL MCP 建置產物 | `~/tools/housecarl/server/` | 由 [`projects/houseCARL`](projects/houseCARL/README.md) publish，不是原始碼 |

## 頂層還有什麼

<!-- wf-nav -->

- [`wf/`](wf/) 是工作流骨架（wf-kernel v0.5）：從 [`WORKFLOWS`](wf/WORKFLOWS.md) 派發工作、用 [`INDEX`](wf/INDEX.md) 找結構、用 [`STRUCTURE`](wf/STRUCTURE.md) 整理資料夾；文件工具在 [`wf/tools/`](wf/tools/)。
- [`tools/`](tools/) 有母 repo 的連結、submodule pin 與 code-map 檢查；完整連結檢查：`python3 tools/check_markdown_links.py`。
- [SESSION-LOG.md](SESSION-LOG.md) 只記母 repo 的跨 session 活狀態；Skyrim 工作線的主線在 [`agentctl/SESSION-LOG.md`](agentctl/SESSION-LOG.md)，當場現況與各隊報告放在 `agentctl/handoffs/`。
- [WAIT_USER.md](WAIT_USER.md) 列需要使用者親自驗證、實機操作或外部素材的項目。
- [`patches/`](patches/README.md) 放可套用到他人 mod 的獨立修補。

`wf/` 的命名與職責對齊 `tome4` 和 `elin`；骨架來自 `~/repo/workflows` 模板（kernel v0.5，2026-08-30）。

## 要在這裡動手做事?

先讀 [AGENTS.md](AGENTS.md) 的工作規則與工作流路由。
