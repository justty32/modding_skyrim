# 下一批可離線 correctness 工作（2026-08-12）

狀態：**四項均已落地**；現行實作入口見各目標 repo README，本檔保留當時的缺口與驗收依據。

Done when: 下一批既有功能缺口已按價值排序；每項有可驗證的現況證據、完成條件、
離線前置與明確不包含範圍，可在 compact 後直接派工。

## 結論

建議下一批做四項，依序是 **game-data 原子發布**、**voicegen→ModForge 真實契約**、
**model-converter→Godot 真實契約**、**darksouls-port→model-converter 真實契約**。
它們都在保護已存在的 pipeline，不增加使用者功能；也都不需要 Skyrim、MO2、遊戲素材、
網路或人工驗收。

| 優先 | 工作 | 為什麼現在做 | 主要 repo |
|---|---|---|---|
| P0 | game-data 每個 plugin 原子發布 | 第二段失敗時，第一段正式輸出已可能存在；非零 exit 不能阻止下游誤讀半成品 | `game-data` |
| P1 | production voicegen→ModForge live contract | 兩邊各自測過，但沒有一次真實 process boundary 串接 | `skyrim-voicegen` + `ModForge` |
| P1 | production model-converter→Godot live contract | 真實 consumer 完全無測試，且實作與公開 env-hook 契約漂移 | `model-converter` + `godot-worldspace-editor` |
| P2 | production darksouls batch→gltf2nif live contract | batch 的 converter success 測試目前 mock 掉真正 subprocess/輸出格式 | `darksouls-port` + `model-converter` |

## P0 — game-data 原子發布與整批 preflight

### 現況證據

- `projects/game-data/extract.sh` 的 `run()` 直接先把 `gamedata` 寫進正式
  `mods/<stem>` / `vanilla/<stem>`，再把 `questnodes` 寫進正式 `catalog/quest-nodes/<stem>`。
  第二個命令失敗時只有 `set -e` 停止，沒有 staging、rollback 或 known-good 保留。
- `projects/game-data/tests/test_extract.py` 的 `test_questnodes_failure_is_nonzero` 只驗 exit code
  與呼叫次數，fake dotnet 不寫輸出，因此沒有覆蓋半發布。
- batch 的同 stem collision 是走到檔案時才發現；在碰到 collision 前，較早的 plugin 可能已改寫。

### Done when

- 每個 plugin 的 `gamedata` 與 `questnodes` 都先寫入同檔案系統的 staging；兩者成功且
  必要輸出存在後才發布。
- 任一段失敗：清掉 staging，既有正式輸出保持 byte-for-byte 不變，也不留下新的正式半成品。
- batch 在第一個 extractor 啟動前完成所有輸出 stem collision 檢查。
- tests 用會真的建立目錄/檔案的 fake dotnet 驗成功發布、第一段失敗、第二段失敗、
  known-good 保留、staging 清理與 batch 零副作用。
- README 說清楚原子發布保證；完整 `game-data` unittest 綠。

### 不包含

不重抽真實 Skyrim/game-data，不改 ModForge `gamedata` / `questnodes` 的內容 schema。

## P1 — skyrim-voicegen → ModForge live contract

### 現況證據

- `projects/ModForge/src/ModForge.Core/Voice.cs` 的 `GenerateWav()` 會真的 exec
  `MODFORGE_TTS_BIN`；現有 `VoiceTests.cs` 只測 `BuildTtsArgs()`，未跨 process。
- `projects/skyrim-voicegen/tests/test_voicegen.py` 直接呼叫 `voicegen.main()` 並 mock
  `subprocess.run`；它證明 producer 內部原子發布，沒有證明 ModForge 能呼叫它。
- 因此引數名稱、wrapper 可執行性、路徑含空白、stderr/exit code、WAV bytes 回傳的 drift
  仍可能兩邊各自全綠。

### Done when

- live test 用 production `Voice.GenerateWav()` exec production `voicegen.py`；最末端只用一個
  deterministic fake Fish engine 產生合法短 WAV，不載模型。
- 驗所有 required/optional args（含 emotion/intensity、ref/model/rvc、seed/speed/language）
  穿過兩層且路徑含空白仍正確。
- 驗 producer 成功的 RIFF/WAVE bytes 回到 ModForge；producer 非零、缺檔、header-only/truncated
  都 fail closed，無 temp/stale 誤認。
- Windows 與 POSIX wrapper 都能由測試建立；缺 sibling repo 或必要 runtime 時明示 skip。
- 兩邊原有 test suites 與 live contract 全綠，PROTOCOL/README 測試入口同步。

### 不包含

不載 F5/Fish 模型，不做 xWMA/LIP/FUZ，不做聲音品質或實機驗收。

## P1 — model-converter → Godot ModelFetch live contract

### 現況證據

- `projects/godot-worldspace-editor/godot/model_fetch.gd` 是 production consumer；目前
  `projects/godot-worldspace-editor/tests/` 只有 placements contract，沒有 ModelFetch 測試。
- `model_fetch.gd` 直接推導 sibling `.venv/Scripts/python.exe` / `.venv/bin/python` 並執行
  `python -m nif2gltf`；`projects/model-converter/PROTOCOL.md` 對外宣告的掛勾則是
  `MODFORGE_NIF2GLTF_BIN` 黑盒 executable。文件與 consumer 並非同一契約。
- `model-converter` 的 68 tests 會用 Python loader 讀 glTF，沒有讓 Godot `GLTFDocument`
  消費 production output。

### Done when

- 先定單一呼叫契約並對齊程式與文件：Godot 支援 protocol 的 executable hook，保留 sibling
  checkout 作可預期 fallback；設定優先序有單測/source gate。
- live test 用 model-converter 的 synthetic NIF fixture 經 production CLI 生成 `.gltf + .bin`，
  再由 Godot 4.6 headless 的 production `ModelFetch._load_gltf()` 載入。
- 驗 scene 是 `Node3D`、mesh/primitive/頂點存在，並以非對稱座標檢查軸向與尺度，避免只驗
  「檔案打得開」。缺 `.bin`、壞 glTF、converter 非零均 fail closed 且不污染 repo cache。
- headless 測試在 temporary project copy 執行，避免 `.gd.uid` / `.godot` 污染。
- model-converter 68 tests、Godot placements 3 tests、新 live contract 全綠；README/design/
  parent CODE_MAP 同步。

### 不包含

不跑 `nifexport`（它需要真實 Skyrim BSA），不驗 vanilla NIF，不加入貼圖或蒙皮功能。

## P2 — darksouls-port batch → model-converter live contract

### 現況證據

- `projects/darksouls-port/tools/p1_batch.py` 的 `convert_or_reuse()` 會 shell out 到 sibling
  `python -m gltf2nif`，但 `tests/test_p1_batch.py` 的 success path mock 掉 `run_gltf2nif()`；
  目前只證「回報成功後檔案非空」。
- `model-converter` 自己有 glTF→NIF round-trip tests，但沒有覆蓋 batch 的 interpreter 推導、
  working directory、參數與碰撞 JSON forwarding。

### Done when

- live test 由 production `p1_batch.convert_or_reuse()` 呼叫 sibling production `gltf2nif`，
  分別跑一個 render mesh 與一個 collision carrier fixture。
- 以 model-converter production reader 檢查 NIF，而非只看非空：BSTriShape、材質路徑、
  座標轉換及 bhk hull 數量/頂點皆符合 fixture。
- converter 非零、成功但缺輸出、malformed hull JSON 均 fail closed，沒有可打包 stale output。
- 缺 sibling/venv 時明示 skip；兩 repo 原有 test suites 與 live contract 全綠，README/CODE_MAP 同步。

### 不包含

不抽 DS 遊戲檔、不全量重跑 47 個 HKX、不改 ghost tolerance、不重包或部署 `DSPortP1`。

## 本機離線可行性基線

2026-08-12 在 Windows 工作區實跑：

- `game-data`: 7/7 unittest PASS（Git Bash 可用）。
- `skyrim-voicegen`: 6/6 unittest PASS。
- `model-converter`: 68/68 pytest PASS；`.venv/Scripts/python.exe` 與必要 Python deps 可用。
- `darksouls-port`: 21/21 unittest PASS。
- `godot-worldspace-editor`: Godot 4.6 headless placements contract 3/3 PASS。
- `.NET SDK 10.0.301` 可用；上述工作不需要網路。

## 排除項

- `WAIT_USER.md` 的 scene Browser、Play-KR 聽感/室內、MessageBox、Dark Souls 門洞實走、
  houseCARL fork push 都仍需要外部環境或使用者，不排進本批。
- Sofia 新劇情、BG3 port、model converter 貼圖/蒙皮、ModForge 新 spec 能力都屬新功能，
  不排進本批。
