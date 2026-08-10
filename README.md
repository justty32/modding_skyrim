# ~/repo/moddings/skyrim —— Skyrim modding 總資料夾

Skyrim SE modding 的開發、分析、產物集中地。本工作區是 public 母 git repo；`projects/` 下各開發專案保持獨立版控，其中 10 個由母 repo 以 submodule 管理。

## 你來找什麼?

| 你要找的 | 去哪裡 |
|---|---|
| **做好的 mod / plugin 成品**(拿去部署、安裝) | [`dist/`](dist/README.md) —— `mods/`(mod 包)、`plugins/`(SKSE DLL)、`libs/`、`docs/`;每個成品資料夾內有 `SOURCE.md` 記來源。**歷史自製成品目前在 `~/skyrim_mods/mine/`**(DSPort*/ModForge*/MF* 系列,使用者決定留原地),新成品才進 dist/ |
| 開發中的原始碼 | `projects/` —— 見下表;各自是獨立 git repo |
| 引擎/SKSE 知識、分析文件 | `analysis/` —— `skyrim_engine/`(CommonLibSSE-NG 引擎手冊)、`skyrim_mods/`(七個參考 mod 拆解)、`houseCARL/`(Linux 適配 runbook)、`mod-survey/`(136 份他人 mod 結構化調查)、`tool-survey/`(製作工具調查)、`followers-patch/`(8 份隨從人設 brief)、`port-source-survey/`(移植素材來源候選調查) |
| 他人的 mod、框架、參考素材 | 實體在 **`~/skyrim_mods/`**(97G 下載庫:`hdd/`、`aa/`、根目錄壓縮檔;解壓素材在 `unzip/`;使用者決定留原地不遷)。[`external/`](external/README.md) 是未來新進素材的預定落點 |

## `projects/` 裡有什麼

各自獨立 git repo,彼此**靠協議/CLI 對接、不整合**。多數跨 repo 連結假設它們**同層 clone 在 `projects/` 下**。

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
| `agent-bridge` | AI 全自動 mod QA 迴圈:遊戲內 HTTP DLL + Linux 端 mo2ctl/runner/MCP | console + runtime state；可列 cell/loaded actors、跨 cell 移到 NPC、開／讀／依文字或 FormID 選對話、等待狀態收斂 |
| `game-data` | 全遊戲文本/清單抽取(vanilla+DLC+CC+mod),給 agent 唯讀取用 | 消費 CLI `gamedata` |

**內容專案**(用 ModForge 做出實際的 mod)

| repo | 是什麼 |
|---|---|
| `sofia-patch` | Sofia 隨從擴充 × VIGILANT 支援:人設解碼、演出設計、四幕對白劇本 |
| `darksouls-port` | DS Remastered 地圖移植成 Skyrim worldspace(**資產僅本機、不發佈**)|

**其他**

| repo | 是什麼 |
|---|---|
| `houseCARL` | Skyrim MCP 工具 fork(資料層讀寫 load order) |
| `my_skyrim_plugin_1` | SKSE C++ plugin 樣板 + 建置骨架(CMake/vcpkg/CI/靜態 CRT) |

> 除了 ModForge／houseCARL／my_skyrim_plugin_1,其餘八個都是 **2026-08-02 從 ModForge `sub_projs/` 抽出來的**(未帶舊 commit 歷史);ModForge 原位置各留一份 stub 導引,它們的契約/spec/計畫文檔仍在 ModForge。**remote 狀態**:godot-worldspace-editor / scene-capture-bridge / model-converter / agent-bridge / skyrim-voicegen 已推上 GitHub(`justty32/skyrim_*`,public);**darksouls-port、sofia-patch、game-data 三個還沒有 remote**——前兩者含他人 mod 的台詞原文與資產抽取器,要開也該開 private。

## 部署注意

- **本機部署狀態(MO2 instance、load order、已裝 mod 清單)不在本資料夾**——歸 `~/notes/projects/modding/skyrim/` 管。部署前去那邊看現況、部署後回那邊記錄。
- 本資料夾只負責:開發(projects)、分析(analysis)、產物(dist)、參考素材(external)。

## 要在這裡動手做事?

先讀 [AGENTS.md](AGENTS.md)(工作規則、工作流路由)。
