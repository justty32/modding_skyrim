# dev-env — 開發環境入口

記錄不同機器/環境能做什麼、不能做什麼，以及 fresh clone 後要做的事。

開始前寫 `Done when: <環境能力/缺口/下一步已記錄，必要時 WAIT_USER 已更新>`。

## 環境矩陣

| 環境 | 有什麼 | 能做 | 不能做 |
|------|--------|------|--------|
| 家用 Manjaro（2026-08-12 實測） | Git、Python 3.14、.NET SDK 10、CMake、Ninja、Wine；部分 repo 自有 venv | 母 repo 維護、ModForge/Python 離線 suite、可取得 submodule 的 build/test | 目前 PATH 無 Godot/Pwsh；感官與遊戲內結果仍需人工驗收 |
| 公司 Windows 離線工作區（2026-08-12 finding） | .NET SDK 10、Git Bash、Godot 4.6、model-converter venv；無 Skyrim | ModForge 與四條 correctness contract 的離線測試 | Skyrim/MO2 runtime、真實遊戲資料與模型驗收 |
| GitHub／各子 repo CI | 母 repo 文件 gate；每個子 repo 自己的 workflow 與依賴 | 母 repo link/unit gate；子 repo 宣告的 build/test/package gate | 不跨 repo 建置，也不能取代實機驗收 |

這是**開發能力**矩陣，不是部署現況。MO2 instance/profile/load order、已安裝 mod 與實機
驗收一律由 `instance/`（部署狀態）與 `agentctl/`（實機驗收證據）管；本檔不複製那份狀態。
（2026-08-23 前這些歸 `~/notes/projects/modding/skyrim/`，現在那裡只剩不進版控的截圖與 MongoDB 快照。）

## Fresh Clone

母 repo 沒有統一依賴或 build；先取回 gitlinks，再進目標子 repo 讀它的 README／AGENTS：

```bash
git clone --recurse-submodules git@github.com:justty32/modding_skyrim.git
cd modding_skyrim
git submodule status
```

若 clone 時略過 submodule，之後補：

```bash
git submodule update --init --recursive
```

截至 2026-08-12，最新母 repo 仍引用三個尚未發布的子模組 commit，因此上述 recursive
步驟會失敗；精確 SHA 與正確修復順序見 [../WAIT_USER.md](../../WAIT_USER.md)。不要把母 repo
gitlink 倒退，也不要把本機舊 checkout 當成已同步。

同步成功後，依 [testing.md](testing.md) 選目標 repo 的離線測試。依賴只裝在該子 repo
自己的環境；母 repo 根目錄不建立共用 venv、NuGet cache 或 build tree。

## 常用環境變數

母 repo 本身沒有必要環境變數。常見變數屬於 producer/consumer 契約，設定與 fallback 以
各子 repo 文件為準：

| 變數 | 所屬邊界 | 先讀 |
|------|----------|------|
| `MODFORGE_TTS_BIN` | ModForge → skyrim-voicegen | `projects/skyrim-voicegen/PROTOCOL.md` |
| `MODFORGE_NIF2GLTF_BIN` | Godot editor → model-converter | `projects/model-converter/PROTOCOL.md` |
| `MODFORGE_REPO`、`MODFORGE_SKYRIM_DATA`、`MODFORGE_MODS_UNZIP` | game-data extractor | `projects/game-data/README.md` |
| `GODOT_BIN`、`MODEL_CONVERTER_DIR` | Godot contract tests | `projects/godot-worldspace-editor/README.md` |

不要把本機絕對路徑、憑證或私有素材位置寫進母 repo。

## 出貨/打包

母 repo 不產生單一 release，也不代替子 repo 打包。流程是：

1. 在來源子 repo 依它自己的 README/build workflow 產生並驗證 artifact。
2. 要交付的新成品放到 [`../mod-library/`](../../mod-library/README.md) 的對應分類，並附 `SOURCE.md`。
3. 部署到 MO2 前先讀 notes 側現況；部署結果也只回寫 notes。

歷史成品仍留在 `~/skyrim_mods/mine/`，不因整理環境而搬動。不得在遊戲執行時覆寫已
載入的 DLL；具體安全部署命令由產出該 DLL 的子 repo 維護。

## 何時不用

- 只是一次性跑 build/test，走 testing 或原工作流。
- 是外部工具細節，走 tooling。
