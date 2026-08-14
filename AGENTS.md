# skyrim — Agent 專案備忘

> Skyrim Special Edition modding 分析工作區。這份檔案是最頂層路由器，只放 always-on 規則與入口連結；細節放到各工作流。

## 專案摘要

- 專案一句話：Skyrim SE modding 分析工作區——引擎/mod 逆向分析（CommonLibSSE-NG C++、Papyrus）＋ houseCARL（Skyrim 讀寫用 MCP 工具）的 Linux 適配。
- 主要語言/框架：分析對象為 C++（SKSE plugin / CommonLibSSE-NG）、Papyrus（`.psc`）、C#（houseCARL 用 Mutagen）；本 repo 自身主要是 Markdown 分析文件，另有 Python stdlib 文件驗證腳本，無建置產物。
- 主要 build 指令：無（純分析 repo）。若要重跑 houseCARL 的本機建置，見 `analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md`（`dotnet build housecarl.sln`／self-contained `dotnet publish -r linux-x64`）。
- 主要 test 指令：`python -m unittest discover -s tests -v`、`python scripts/check_markdown_links.py`；各 submodule 測試矩陣見 `workflows/testing.md`。houseCARL 驗證方式見上述 runbook（HTTP 模式啟動 + explicit paths 測試）。

## 先讀哪裡

- 使用者要你動手做某件事 → [WORKFLOWS.md](WORKFLOWS.md)：依意圖派發到對應工作流。
- 任何測試／實機驗證 → [workflows/testing.md](workflows/testing.md)；本機 MO2 細節再依該入口讀 notes 側 testing workflow。
- 想看 repo 結構 → 專案自己的 `INDEX.md` 或 `README.md`。
- 碰原始碼 → 先讀 [workflows/common/conventions.md](workflows/common/conventions.md)，再讀 [CODE_MAP](workflows/common/code-map/CODE_MAP.md)。

## Always-on 鐵律

- 重構/整理必須 behavior-preserving；改完跑對應測試。
- 未經使用者確認，不 push、不開新大型工作。
- 不 revert 使用者或其他 agent 的未確認變更；遇到衝突先停下說明。
- 各工作流的具體流程在自己的 README，不在本檔重複。
- 小事可以跳流程；完整規則見 [PRINCIPLES.md](PRINCIPLES.md)。
- 非微小工作先定義 `Done when:`。
- 需要使用者親自驗證、外部環境、權限、實機、帳號或手動操作時，記到 [WAIT_USER.md](WAIT_USER.md)。
- 跨 session 的 open 狀態記到 [SESSION-LOG.md](SESSION-LOG.md) 或對應工作流的 `session-log.md`。
- 引用外部專案程式碼或技術結論時，盡量附來源位置：`path/to/file:line`、函式名、URL、paper id、或命令輸出摘要。
- 架構圖/流程圖優先用 Mermaid、表格、列點；不要用需要字元對齊的 ASCII 框線圖。

## 分層思想

整個 repo 是分層樹，每一層只指向下一層：

```text
AGENTS.md → WORKFLOWS.md / INDEX.md → 各工作流入口 → 工作流內容 → 子工作流
```

- `README.md` = 初入一個資料夾先讀的入口/導引。
- `INDEX.md` = 描述該資料夾頂層結構的索引。
- 小資料夾可以 README 兼 index；變大後才拆出獨立 INDEX。
- durable 知識歸到它所屬的工作流，不堆在頂層。

## 本地專案規則

把專案專屬規則放這裡，保持精簡；太長就移到對應工作流。

- **目錄佈局**：`analysis/skyrim_engine/`（CommonLibSSE-NG 引擎逆向，SKSE plugin 開發導向，含 Architecture/Tutorial/Answers/Details 全分類）、`analysis/skyrim_mods/`（7 個參考 mod 拆解：JContainers/PapyrusUtil/powerofthree's Tweaks/SkyUI/UIExtensions/Sofia Follower/RDO，服務 ModForge 這個外部程式化生成工具的 spec 設計）、`analysis/houseCARL/`（houseCARL 這個 Skyrim MCP 工具在本機 Manjaro + Proton + MO2 環境的適配分析）、`dist/`（自製產物：mods/plugins/libs/docs，等待部署使用，見其 README）、`external/`（他人 mod 與框架的唯讀參考素材）。
- **根 README.md 是外來 agent 的入口**（設計情境：`~/notes` 側的 agent 被派來「找做好的 mod 去部署」，會先讀 README.md）——它必須永遠答得出「成品在哪」（`dist/`）與「部署狀態歸 `~/notes/projects/modding/skyrim/` 管」。新增產物類型或改佈局時同步更新它。
- **本工作區自 2026-08-03 起是 public 母 git repo**（`justty32/modding_skyrim`），`projects/` 下 11 個獨立 repo 以 submodule 管理：ModForge、my_skyrim_plugin_1、godot-worldspace-editor、scene-capture-bridge、model-converter、agent-bridge、darksouls-port、sofia-patch、skyrim-voicegen、game-data、houseCARL。跨 repo 連結假設各 repo **同層 clone 在 `projects/` 下**。houseCARL 釘在 `justty32/houseCARL` 的 `fix/dialogue-encoding-lint`，只維護自有 fork、不追 upstream；決策見 [fork-maintenance-decision.md](analysis/houseCARL/answers/fork-maintenance-decision.md)。另有三份純文檔子專案在 `analysis/`（mod-survey、tool-survey、followers-patch），不是獨立 repo。
- **FormID 有兩種語境，別混用**：引擎內部二進位 `FormID` 是 32 位，前兩位是插件在 load order 的索引（`0xFF` 開頭＝runtime 動態生成物件），詳見 `analysis/skyrim_engine/architecture/Systems_TESForm_Detailed.md`。houseCARL MCP 工具對外走的是**文字格式** `XXXXXX:Plugin.esp`（6 位十六進位＋定義該記錄的 master 檔名），兩者概念相通但序列化方式不同。
- **houseCARL 的核心心智模型**：讀取一律走「真實 load order winner」＋可選完整 conflict tree；預設寫入落在**新增的 patch plugin**（`houseCARL - <name>`），原始 plugin 不動；in-place 編輯是需一次性同意的 opt-in 車道。查 Nexus Mods 優先用 `mcp__housecarl__housecarl_nexus_search` / `housecarl_nexus_mod`，別開瀏覽器代勞。
- **本機佈署狀況歸 `~/notes/projects/modding/skyrim/` 管**（職責劃分 2026-07-17）：MO2 instance / profile / load order、已部署 mod 清單、houseCARL MCP 的本機註冊指令、實機驗證狀態、部署規劃（Jackify 等）全在那邊維護，本 repo 只管開發與分析，**不重複維護部署資訊**。開發完的 mod 要上機驗證 → 去那邊查現況。
- **houseCARL 讀 MO2 的技術限制**（分析結論，非部署事實）：MO2 的 `ModOrganizer.ini` 記的是 Wine 路徑（`Z:\home\...`），houseCARL 的 `Mo2InstanceDir` 模式讀不動，須改用 explicit `DataDir`/`ModsDir`/`ProfileDir`；本機實際路徑與註冊指令見 notes 側 `housecarl.md`。
- `TODO`: release/package 注意事項（本 repo 目前只做分析，無打包產物）。

## 可選工作模式

若專案需要分析外部 repo、做衍生專案、或打包 patch，可啟用：

- [analysis](workflows/analysis.md)：陌生專案 Level 1-6 分析。
- [create](workflows/create/README.md)：基於分析建立獨立小專案。
- [patch](workflows/patch/README.md)：建立冷啟動 agent 可套用的 patch 包。
- [research](workflows/research/README.md)：paper/長文閱讀、摘要、翻譯、索引。
- [html-guide](workflows/html-guide/README.md)：大量 `.md` 的 HTML 導覽層。
