# ~/repo/moddings/skyrim —— Skyrim modding 總資料夾

Skyrim SE modding 的開發、分析、部署與產物集中地。本工作區是 public 母 repo；
底下各條線保持獨立版控，由母 repo 以 submodule 管理。

## 四條主線

2026-08-23 統整後，日常工作分成四條線，各自是獨立 repo：

| 線 | 管什麼 | 可見性 |
|---|---|---|
| [`instance/`](instance/) | **本機部署狀態**：MO2 instance、現役 profile（`modpack-main`）、load order、已裝 mod、profile 稽核工具 | private |
| [`mod-library/`](mod-library/) | **本地 mod 庫**：MongoDB 索引、自製繁中翻譯層、自製插件與修正 esp、庫稽核 | private |
| [`modpack-design/`](modpack-design/) | **整合包設計**：想玩什麼、Gameplay 遷移批次、技術債、選型調查 | private（暫時） |
| [`agentctl/`](agentctl/) | **讓 AI 操控 Skyrim 的總控**：工作流、插件編排、agent 交接、QA harness、執行證據 | private（暫時） |

> **`mod-library` 必須永遠 private**——它的翻譯層內含他人 mod 的完整原始 ESP 複本。
> 另外兩條標「暫時」的是還沒逐檔審查完內容，審完再決定是否公開。
> **不要從這份 public 母 repo 推論各子 repo 的公開範圍。**

## 你來找什麼?

| 你要找的 | 去哪裡 |
|---|---|
| **做好的 mod / plugin 成品**(拿去部署、安裝) | [`mod-library/`](mod-library/) —— `l10n/mods/`(翻譯層)、`plugins/`(SKSE DLL)、`artifacts/`(修正 esp);每個成品資料夾內有 `SOURCE.md` 記來源。**歷史自製成品在 `~/skyrim_mods/mine/`**(DSPort*/ModForge*/MF* 系列,使用者決定留原地) |
| **現在裝了什麼、load order 是什麼** | [`instance/`](instance/) |
| **怎麼叫 AI 去玩 / 去下載 / 去驗證** | [`agentctl/`](agentctl/) |
| 開發中的原始碼 | `projects/` —— 見下表;各自是獨立 git repo |
| 引擎/SKSE 知識、mod 技術拆解、工具調查 | `analysis/` —— `skyrim_engine/`(CommonLibSSE-NG 引擎手冊)、`skyrim_mods/`(七個參考 mod 拆解)、`houseCARL/`(Linux 適配 runbook)、`mod-survey/`(136 份他人 mod 結構化調查)、`tool-survey/`(製作工具調查)、`followers-patch/`(8 份隨從人設 brief)、`port-source-survey/`(移植素材來源候選調查) |
| 他人的 mod、框架、參考素材 | 實體在 **`~/skyrim_mods/`**(125G 下載庫,使用者決定留原地)。[`external/`](external/README.md) 是外部框架原始碼的落點 |

## `projects/` 裡有什麼

**純軟體開發 repo**,各自獨立,彼此**靠協議/CLI 對接、不整合**。多數跨 repo 連結假設它們
**同層 clone 在 `projects/` 下**。狀態與知識類的線不放這裡——那是上面四條主線。

**核心**

| repo | 是什麼 |
|---|---|
| `ModForge` | JSON spec → Skyrim `.esp` 生成工具(C#,AI-agent 友善)。**生態核心**,下面幾乎全部繞著它 |

**工具 / 基石**(靠協議或 CLI 被 ModForge 消費,互不整合)

| repo | 是什麼 | 掛勾 |
|---|---|---|
| `godot-worldspace-editor` | Godot 4 離線地形/紋理/物件編輯器,CK 地形編輯的替代前端 | heightmap/splatmap PNG + `placements.json` |
| `scene-capture-bridge` | SKSE C++ DLL,遊戲內採集/編輯場景 | `scene.json` → 生 patch esp |
| `model-converter` | Skyrim `.nif` ↔ glTF/FBX/OBJ 雙向轉換(Python) | `MODFORGE_NIF2GLTF_BIN` |
| `skyrim-voicegen` | 語音合成:臺詞+情緒+參考嗓音 → `.wav` | `MODFORGE_TTS_BIN` |
| `agent-bridge` | AI 全自動 mod QA 迴圈:遊戲內 HTTP DLL + Linux 端 mo2ctl/runner/MCP。**是 `agentctl/` 的核心插件** | console + runtime state |
| `game-data` | 全遊戲文本/清單抽取(vanilla+DLC+CC+mod),給 agent 唯讀取用 | 消費 CLI `gamedata` |

**內容專案**(用 ModForge 做出實際的 mod)

| repo | 是什麼 |
|---|---|
| `sofia-patch` | Sofia 隨從擴充 × VIGILANT 支援:人設解碼、演出設計、四幕對白劇本 |
| `darksouls-port` | DS Remastered 地圖移植成 Skyrim worldspace(**資產僅本機、不發佈**)|

**其他**

| repo | 是什麼 |
|---|---|
| `houseCARL` | Skyrim MCP 工具 fork(資料層讀寫 load order)。`Mo2LoadOrder.cs` 是 modlist 排序方向的權威依據 |
| `my_skyrim_plugin_1` | SKSE C++ plugin 樣板 + 建置骨架(CMake/vcpkg/CI/靜態 CRT) |

> 除了 ModForge／houseCARL／my_skyrim_plugin_1,其餘八個都是 **2026-08-02 從 ModForge `sub_projs/` 抽出來的**(未帶舊 commit 歷史);ModForge 原位置各留一份 stub 導引,它們的契約/spec/計畫文檔仍在 ModForge。若 recursive update 報 `not our ref`,代表母 repo 的 gitlink 指到一個遠端拿不到的 commit(尚未 push,或它所在的分支已被刪除)。先在該 submodule `git fetch --all` 再看 `git branch -r --contains <pin>`;**不要把 gitlink 倒退**。push 端有 [`tools/check_submodule_pins.py`](tools/check_submodule_pins.py)(掛在 `tools/hooks/pre-push`)擋住推出「遠端拿不到的 pin」,但它擋不住 pin 推出後、它所在的側分支才被刪除的情況。

## 不進版控的東西

| 東西 | 位置 | 為什麼 |
|---|---|---|
| mod 下載庫 | `~/skyrim_mods/`(125GB) | 體積 |
| 實機截圖 | `~/notes/projects/modding/skyrim/logs/`(66MB) | 體積,且只是證據 |
| MongoDB 快照 | `~/notes/projects/modding/skyrim/backups/`(54MB) | 體積 |
| QA baseline 存檔 | `~/games/skyrim-qa-baselines`(3.1MB) | **刻意**設計成 repo 外的唯讀主檔 |
| houseCARL MCP 建置產物 | `~/tools/housecarl/server/` | 由 `projects/houseCARL` publish 出來,不是原始碼 |

## 頂層還有什麼

| 路徑 | 內容 |
|---|---|
| [`wf/`](wf/) | 工作流骨架:7 份骨架 md(PRINCIPLES／WORKFLOWS／DEV-GUIDE／ADOPTION／MAINTENANCE／SYNC／INIT-QUESTIONS)＋ [`wf/workflows/`](wf/workflows/)(各工作流入口、plans、investigation findings、CODE_MAP) |
| [`tools/`](tools/) | 母 repo 的文件驗證:`check_markdown_links.py` 與其測試。跑法 `python3 tools/check_markdown_links.py` |
| [`SESSION-LOG.md`](SESSION-LOG.md) | 母 repo 的跨 session 活狀態。Skyrim 工作線自己的交接主線在 `agentctl/SESSION-LOG.md` |
| [`WAIT_USER.md`](WAIT_USER.md) | 需要使用者親自驗證／實機／外部素材才能完成的項目 |
| `patches/` | 針對他人 mod 的獨立修補 |

> `wf/` 的命名與職責對齊 `~/repo/moddings/tome4` 與 `elin`。

## 要在這裡動手做事?

先讀 [AGENTS.md](AGENTS.md)(工作規則、工作流路由)。
