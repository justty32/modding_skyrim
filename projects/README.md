# projects — Skyrim mod 開發專案

這裡是純軟體開發 repo。每個專案都是獨立 git repo，彼此靠協議或 CLI 對接，不合成一個專案。多數跨 repo 連結都假設它們同層 clone 在 `projects/` 下；部署、mod 庫、整合包設計與 AI 操控不放在這裡，請從[根目錄](../README.md)進各自工作線。

## 核心

| repo | 是什麼 |
|---|---|
| [`ModForge/`](ModForge/) | JSON spec → Skyrim `.esp` 生成工具（C#，AI agent 友善）。生態核心，下面多數工具都繞著它。 |

## 工具與基石

這些工具靠協議或 CLI 被 ModForge 使用，彼此不整合。

| repo | 是什麼 | 掛勾 |
|---|---|---|
| [`godot-worldspace-editor/`](godot-worldspace-editor/) | Godot 4 離線地形、紋理與物件編輯器，是 CK 地形編輯的替代前端 | heightmap/splatmap PNG + `placements.json` |
| [`scene-capture-bridge/`](scene-capture-bridge/) | SKSE C++ DLL，在遊戲內採集與編輯場景 | `scene.json` → 生 patch esp |
| [`model-converter/`](model-converter/) | Skyrim `.nif` ↔ glTF/FBX/OBJ 雙向轉換（Python） | `MODFORGE_NIF2GLTF_BIN` |
| [`skyrim-voicegen/`](skyrim-voicegen/) | 語音合成：臺詞、情緒、參考嗓音 → `.wav` | `MODFORGE_TTS_BIN` |
| [`agent-bridge/`](agent-bridge/) | AI 自動 mod QA：遊戲內 HTTP DLL，加上 Linux 端 mo2ctl、runner、MCP；也是 [`agentctl/`](../agentctl/) 的核心插件 | console + runtime state |
| [`game-data/`](game-data/) | 抽取整個遊戲的文本與清單（vanilla、DLC、CC、mod），讓 agent 唯讀使用 | 消費 CLI `gamedata` |

## 內容專案

| repo | 是什麼 |
|---|---|
| [`sofia-patch/`](sofia-patch/) | Sofia 隨從擴充 × VIGILANT 支援：人設解碼、演出設計與四幕對白劇本 |
| [`darksouls-port/`](darksouls-port/) | 把 DS Remastered 地圖移植成 Skyrim worldspace；資產只留本機，不發佈 |

## 其他專案

| repo | 是什麼 |
|---|---|
| [`houseCARL/`](houseCARL/) | Skyrim MCP 工具 fork，從資料層讀寫 load order；`Mo2LoadOrder.cs` 是 modlist 排序方向的權威依據 |
| [`my_skyrim_plugin_1/`](my_skyrim_plugin_1/) | DaylightDungeon SKSE 插件＋建置基礎設施（CMake、vcpkg、CI、靜態 CRT）；repo 名沿用舊名 |

除了 ModForge、houseCARL、my_skyrim_plugin_1，其他八個專案都是 2026-08-02 從 ModForge 的 `sub_projs/` 抽出來，沒有帶舊 commit 歷史。ModForge 原位置各留一份 stub 導引；它們的契約、spec 與計畫文件仍在 ModForge。

## 同層 clone 耦合群

下列七個 repo 彼此用 `../<兄弟>` 路徑互指（md 連結、`extract.sh`、`repo_layout.gd`、`MODFORGE_MODEL_CONVERTER_PYTHON` 這類環境變數、symlink），必須同層 clone 在 `projects/` 下。**改名、搬移或單獨 clone 其中任何一個之前，整組都要檢查。**

| 成員 | 依賴誰（→ 指向） |
|---|---|
| ModForge | 契約、spec 與計畫文件仍在這裡，連向其餘六個成員（sub_projs stub） |
| model-converter | → ModForge |
| darksouls-port | → ModForge、model-converter（`.venv-wsl`、`p3/converter-pin.json`） |
| godot-worldspace-editor | → ModForge、model-converter、scene-capture-bridge |
| scene-capture-bridge | → ModForge |
| game-data | → ModForge（`extract.sh`）；被 sofia-patch 以 symlink 引用 |
| sofia-patch | → game-data（`sofia-patch/game-data` symlink，大量引用）、ModForge（含 symlink） |

## houseCARL 與 submodule URL

houseCARL 是上游 `Avick3110/houseCARL` 的 fork：submodule 的 `url` 指 fork `justty32/houseCARL`，`branch = main` 指 fork 的 `main`（含本機三項修正，部署的 MCP dll 建自此）。工作樹裡 `origin` 是上游、`fork` 是我們的 fork，本機 `main` 追的是上游，不是 fork。

`.gitmodules` 的 URL 混用是刻意保留的：`projects/` 下 11 個走 https，`instance`、`mod-library`、`modpack-design`、`agentctl` 四條主線走 ssh。改其中一邊時不必統一。

若遞迴更新出現 `not our ref`，表示母 repo 的 gitlink 指到遠端拿不到的 commit：可能還沒 push，或所在分支已刪除。先進該 submodule 跑 `git fetch --all`，再跑 `git branch -r --contains <pin>`；不要把 gitlink 倒退。push 時 [`../tools/check_submodule_pins.py`](../tools/check_submodule_pins.py) 會檢查遠端拿不到的 pin；它掛在 `../tools/hooks/pre-push`，但無法阻止 pin 推出後所在側分支才被刪除的情況。

## 一次 push 所有變更

建議一開始就設定下列 repo-local Git 設定。它們不進版控：

```bash
git config push.recurseSubmodules on-demand   # 先推有變動的 submodule，再推母 repo
git config submodule.recurse true             # pull/checkout/switch 一併遞迴
git config diff.submodule log                 # diff 顯示 submodule 的 commit 訊息而非裸 hash
git config status.submoduleSummary true       # status 顯示 submodule 改了什麼
```

設了 `on-demand` 後，pre-push 檢查會讓路，因為 Git 會在同一次 push 裡把那些 commit 發布掉；側分支警告仍會出現。
