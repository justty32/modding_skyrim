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

各子 repo（上表四條線與 `projects/` 下的軟體 repo）根目錄都有自己的 `AGENTS.md` 與 `wf/` 工作流骨架（2026-10-26 導入）；進子 repo 工作先讀它的 `AGENTS.md`。例外：`projects/houseCARL` 尚未導入，`projects/model-converter` 的 `wf/` 暫在 `wf-import` 分支。

## 你來找什麼?

<!-- wf-nav -->
| 你要找的 | 去哪裡 |
|---|---|
| 做好的 mod、plugin、翻譯或修正 esp | [`mod-library/`](mod-library/)：`l10n/mods/` 是翻譯層、`plugins/` 是 SKSE DLL、`artifacts/` 是修正 esp；每個成品資料夾有 `SOURCE.md` 或 `README.md` 記來源。歷史自製成品在 `~/skyrim_mods/mine/`（DSPort*/ModForge*/MF* 系列），依使用者決定留在原地。 |
| 現在裝了什麼、load order 是什麼 | [`instance/`](instance/) |
| 整合包要做什麼、技術債與選型 | [`modpack-design/`](modpack-design/) |
| 叫 AI 下載、操作遊戲或做驗收 | [`agentctl/`](agentctl/) |
| 今天或最近一場從哪裡接著做 | [`agentctl/handoffs/NEXT-SESSION.md`](agentctl/handoffs/NEXT-SESSION.md) |
| 使用者想要、尚待調查的 mod | [`modpack-design/sources/`](modpack-design/sources/README.md) 的 `mod-want-review-*`（審查結果）；根目錄的 `mods-user-want.md`、`play-notes.md` 是使用者私人貼板，已不進版控 |
| 開發中的原始碼 | [`projects/`](projects/README.md) |
| 引擎、SKSE、mod 與工具的研究筆記 | [`analysis/`](analysis/README.md) |
| 外部框架原始碼 | [`external/`](external/README.md)；他人的 mod、框架與參考素材實體在 `~/skyrim_mods/`（依使用者決定留在原地，體積以 `du -sh` 為準）。 |

## `projects/` 裡有什麼

所有開發 repo 的用途、彼此的協議關係，以及 submodule 更新和一次 push 的設定，都在 [`projects/README.md`](projects/README.md)。

## 不進版控的東西

| 東西 | 位置 | 原因 |
|---|---|---|
| mod 下載庫 | `~/skyrim_mods/`（百 GB 級，以 `du -sh` 為準） | 體積 |
| 舊場次實機截圖 | `~/notes/projects/modding/skyrim/logs/`（88 MB） | 歷史證據；近期截圖在 `agentctl/handoffs/**/runtime/`，同樣不進版控 |
| 歷史 MongoDB 快照 | `~/notes/projects/modding/skyrim/backups/`（86 MB） | 歷史備份；現役部署狀態已歸 [`instance/`](instance/) |
| QA baseline 存檔 | `~/games/skyrim-qa-baselines`（3.1 MB） | 刻意放在 repo 外，作為唯讀主檔 |
| houseCARL MCP 建置產物 | `~/tools/housecarl/server/` | 由 [`projects/houseCARL`](projects/houseCARL/README.md) publish，不是原始碼 |

## 頂層還有什麼

`wf/`（工作流骨架，wf-kernel v0.6+794d6d2，骨架來自 `~/repo/workflows` 模板）、`tools/`、`wait-user/`、`patches/`、`.github/` 等其餘頂層目錄與檔案的逐列說明見 [`wf/INDEX.md`](wf/INDEX.md)——本檔只當入口，佈局細目以 INDEX 為準。

## 要在這裡動手做事?

先讀 [AGENTS.md](AGENTS.md) 的工作規則與工作流路由。
