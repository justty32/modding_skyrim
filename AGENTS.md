# skyrim — Agent 專案備忘

> Skyrim Special Edition modding 分析工作區。這份檔案是最頂層路由器，只放 always-on 規則與入口連結；細節放到各工作流。

## 專案摘要

- 專案一句話：Skyrim SE modding 工作區。母 repo 管開發（`projects/` 11 個軟體 submodule）與知識（`analysis/`）；部署狀態、mod 庫、整合包設計、AI 操控總控各自獨立成線（`instance/`、`mod-library/`、`modpack-design/`、`agentctl/`，2026-08-23 拆出）。
- 主要語言/框架：分析對象為 C++（SKSE plugin / CommonLibSSE-NG）、Papyrus（`.psc`）、C#（houseCARL 用 Mutagen）；本 repo 自身主要是 Markdown 分析文件，另有 Python stdlib 文件驗證腳本，無建置產物。
- 主要 build 指令：母 repo 無（文件與索引為主，程式在各 submodule）。若要重跑 houseCARL 的本機建置，見 `analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md`（`dotnet build housecarl.sln`／self-contained `dotnet publish -r linux-x64`）。
- 主要 test 指令：`python -m unittest discover -s tools -p "test_*.py" -v`、`python tools/check_markdown_links.py`；各 submodule 測試矩陣見 `wf/workflows/testing.md`。houseCARL 驗證方式見上述 runbook（HTTP 模式啟動 + explicit paths 測試）。

## 先讀哪裡

- 使用者要你動手做某件事 → [WORKFLOWS.md](wf/WORKFLOWS.md)：依意圖派發到對應工作流。
- 想看 repo 結構 → [README.md](README.md)（本 repo 沒有獨立 `INDEX.md`，README 兼索引）；四條主線各自的 README 在 `instance/`、`mod-library/`、`modpack-design/`、`agentctl/`。
- 碰原始碼 → 先讀 [workflows/common/conventions.md](wf/workflows/common/conventions.md)，再讀 [CODE_MAP](wf/workflows/common/code-map/CODE_MAP.md)。

## Always-on 鐵律

- 重構/整理必須 behavior-preserving；改完跑對應測試。
- 未經使用者確認，不 push、不開新大型工作。
- 不 revert 使用者或其他 agent 的未確認變更；遇到衝突先停下說明。
- 各工作流的具體流程在自己的 README，不在本檔重複。
- 小事可以跳流程；完整規則見 [PRINCIPLES.md](wf/PRINCIPLES.md)。
- 非微小工作先定義 `Done when:`。
- 需要使用者親自驗證、外部環境、權限、實機、帳號或手動操作時，記到 [WAIT_USER.md](WAIT_USER.md)。
- 跨 session 的 open 狀態記到 [SESSION-LOG.md](SESSION-LOG.md) 或對應工作流的 `session-log.md`。
- 引用外部專案程式碼或技術結論時，盡量附來源位置：`path/to/file:line`、函式名、URL、paper id、或命令輸出摘要。
- 架構圖/流程圖優先用 Mermaid、表格、列點；不要用需要字元對齊的 ASCII 框線圖。

## 分層思想

整個 repo 是分層樹，每一層只指向下一層：

```text
AGENTS.md → WORKFLOWS.md / README.md → 各工作流入口 → 工作流內容 → 子工作流
```

- `README.md` = 初入一個資料夾先讀的入口/導引。
- `INDEX.md` = 描述該資料夾頂層結構的索引。
- 小資料夾可以 README 兼 index；變大後才拆出獨立 INDEX。
- durable 知識歸到它所屬的工作流，不堆在頂層。

## 本地專案規則

把專案專屬規則放這裡，保持精簡；太長就移到對應工作流。

- **目錄佈局**：工作流骨架整包在 `wf/`（7 份骨架 md ＋ `wf/workflows/`），母 repo 的文件驗證工具在 `tools/`。頂層四條主線各是獨立 repo——`instance/`（本機部署狀態：MO2 instance／現役 profile `modpack-main`／load order／profile 稽核工具）、`mod-library/`（本地 mod 庫：MongoDB 索引、自製繁中翻譯層、自製插件與修正 esp）、`modpack-design/`（整合包設計：Gameplay 遷移批次、技術債、選型調查）、`agentctl/`（AI 操控總控：工作流、agent 交接、QA harness、執行證據）。知識類留在母 repo 的 `analysis/`：`skyrim_engine/`（CommonLibSSE-NG 引擎逆向，SKSE plugin 開發導向，含 Architecture/Tutorial/Answers/Details 全分類）、`skyrim_mods/`（7 個參考 mod 拆解：JContainers／PapyrusUtil／powerofthree's Tweaks／SkyUI／UIExtensions／Sofia Follower／RDO，服務 ModForge 的 spec 設計）、`houseCARL/`（houseCARL 在本機 Manjaro + Proton + MO2 環境的適配分析）、`mod-survey/`（136 份他人 mod 結構化調查）、`tool-survey/`（製作工具調查）；`external/` 是他人框架原始碼的唯讀落點。
- **根 README.md 是外來 agent 的入口**（設計情境：被派來「找做好的 mod 去部署」的 agent 會先讀它）——它必須永遠答得出「成品在哪」（`mod-library/`）與「現在裝了什麼」（`instance/`）。新增產物類型或改佈局時同步更新它。
- **本工作區自 2026-08-03 起是 public 母 git repo**（`justty32/modding_skyrim`），`projects/` 下 11 個獨立 repo 以 submodule 管理：ModForge、my_skyrim_plugin_1、godot-worldspace-editor、scene-capture-bridge、model-converter、agent-bridge、darksouls-port、sofia-patch、skyrim-voicegen、game-data、houseCARL。跨 repo 連結假設各 repo **同層 clone 在 `projects/` 下**。houseCARL 只維護自有 fork（`justty32/houseCARL`）、不追 upstream；決策見 [fork-maintenance-decision.md](analysis/houseCARL/answers/fork-maintenance-decision.md)。另有三份純文檔子專案在 `analysis/`（mod-survey、tool-survey、followers-patch），不是獨立 repo。
- **FormID 有兩種語境，別混用**：引擎內部二進位 `FormID` 是 32 位，前兩位是插件在 load order 的索引（`0xFF` 開頭＝runtime 動態生成物件），詳見 `analysis/skyrim_engine/architecture/Systems_TESForm_Detailed.md`。houseCARL MCP 工具對外走的是**文字格式** `XXXXXX:Plugin.esp`（6 位十六進位＋定義該記錄的 master 檔名），兩者概念相通但序列化方式不同。
- **houseCARL 的核心心智模型**：讀取一律走「真實 load order winner」＋可選完整 conflict tree；預設寫入落在**新增的 patch plugin**（`houseCARL - <name>`），原始 plugin 不動；in-place 編輯是需一次性同意的 opt-in 車道。查 Nexus Mods 優先用 `mcp__housecarl__housecarl_nexus_search` / `housecarl_nexus_mod`，別開瀏覽器代勞。
- **本機部署狀況歸 `instance/` 管**（2026-08-23 統整；此條取代 2026-07-17 的「歸 `~/notes` 管」劃分）：MO2 instance／profile／load order、已部署 mod 清單、實機驗證狀態、部署規劃（Jackify 等）全在 `instance/` 維護。`~/notes/projects/modding/skyrim/` 只留不進版控的實機截圖與 MongoDB 快照。**可見性**：母 repo 是 public，四條主線目前都是 private；`mod-library` 因含他人 mod 的完整 ESP 複本而**必須永遠 private**。
- **houseCARL 讀 MO2 的技術限制**（分析結論，非部署事實）：MO2 的 `ModOrganizer.ini` 記的是 Wine 路徑（`Z:\home\...`），houseCARL 的 `Mo2InstanceDir` 模式讀不動，須改用 explicit `DataDir`/`ModsDir`/`ProfileDir`；本機實際路徑與註冊指令見 `agentctl/docs/housecarl.md`。
- `TODO`: release/package 注意事項（本 repo 目前只做分析，無打包產物）。

## 可選工作模式

若專案需要分析外部 repo、做衍生專案、或打包 patch，可啟用：

- [analysis](wf/workflows/analysis.md)：陌生專案 Level 1-6 分析。
- [create](wf/workflows/create/README.md)：基於分析建立獨立小專案。
- [patch](wf/workflows/patch/README.md)：建立冷啟動 agent 可套用的 patch 包。
- [research](wf/workflows/research/README.md)：paper/長文閱讀、摘要、翻譯、索引。
- [html-guide](wf/workflows/html-guide/README.md)：大量 `.md` 的 HTML 導覽層。
