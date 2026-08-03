# SESSION-LOG — 進度日誌 hub

只放還沒完成的活狀態。完成的不留在這裡；完成後濃縮到對應工作流的 landed/archive、release note、或 git log。

待使用者親自做/驗證的事放 [WAIT_USER.md](WAIT_USER.md)。

建議單一 `session-log.md` 保持短小，只為「下一個 session 接得上」。若超過 50 行，刪舊留新，或按工作流/主題拆檔。

## 最新進度

- **darksouls-port P1 實機驗收通過，進 P2**（2026-08-03）：用 agent-bridge 的 QA 迴圈全程無 GUI 裝入 + 進場（`mo2ctl install/launch` → `POST /console`），使用者實看確認「整個北方不死院都有了」，玩家 Z 穩定 19973–19977 十五秒 → **成形 ✅、地板站得住 ✅**。三個回報事項的根因已全部定位並寫進 [projects/darksouls-port/p1/P1-INGAME-FINDINGS.md](projects/darksouls-port/p1/P1-INGAME-FINDINGS.md)（commit `e0c1f7f`）：
  - **幽靈碰撞**＝`collision_hulls.py --planar-thresh` 預設 **1.5 m** 太寬，連通分量整塊換成凸包 → (a) 有門洞的牆把門洞填實（`h0006` 實測憑空多 **56.9 m²**）(b) 起伏 ≤1.5 m 的曲面/階梯塌成實心塊。修法＝門檻降到 0.05–0.10 m + 對「凸包面積/實際面積」超標的分量另走 V-HACD。
  - **DS-only 擺放物**＝MSB 324 筆裡 **Object 151 + DummyObject 18** 完全沒移植；且 **ConnectCollision 2 筆（`h0054B1`/`h0099B1`）是地圖切換觸發體卻被當實心碰撞進口**——獨立做的距離分析正好抓到 `h0099` 是離視覺 >30 m 的 18 m 方塊，兩條線互相印證。**剔除判準要用 MSB part 型別，不是距離。**
  - **天空盒**（使用者新加需求）：素材已在手（`m9100` 穹頂 5781×3198×5874 m + `m18_sky.dds`/`m18_bg_cloud.dds`）。建議**天空走 Skyrim 原生 WTHR/CLMT**（跟著日夜轉、無 cull 問題、頂點預算為零），**遠山 `m9000` 才走幾何直搬**。
  - ✅ **碰撞管線環境已修好**（2026-08-03，接著上面那條做的）：`darksouls-port/venv/` 的 shebang 還指著搬遷前的舊路徑 `/home/lorkhan/repo/ModForge/sub_projs/darksouls-port/venv/`——**是 8/02 大拆分的殘留，那條管線從搬完就一次都沒跑過**。已 `rm -rf venv` 重建並照 `extractor/README.md` 的配方裝回 soulstruct（editable，clone 在 `extractor/ThirdParty/`）+ scipy/trimesh/vhacdx。**驗證方式＝重跑 `h0006B1A18` 與 repo 既有 `.hulls.json` 逐位元相同**（47 hulls / 100% coverage），所以之後的差異都能歸因到參數改動而非環境漂移。順手也把 `model-converter/.venv` 補上 trimesh/scipy/vhacdx。
  - **下一步（已規劃、未動工）**：① `collision_hulls.py` 的 `--planar-thresh` 1.5m → 0.05–0.10m，且 `len(faces)<6` 那條捷徑要補 deviation 檢查；② 平面內填洞降門檻救不了（有門洞的牆 deviation 本來就 0），要另加「凸包投影面積/三角形實際面積」超標就改走分群的判準——但 V-HACD 吃不動零體積開殼（README 實測 h0501 用 vhacd 覆蓋只有 30%），所以得自己寫按填充率上限的貪婪三角形分群；③ `p1_batch.py` 加兩道過濾：**MSB 沒引用的 3 個碰撞檔**（`h0001B0A18`/`h0012B1A18`/`h0017B1A18`，55 hulls，DS 自己都不載入）＋ 離渲染幾何 >2m 的 hull（h0090/h0092/h0098/h0099 各 2 顆）。
  - ⚠️ **修正先前的判斷**：`ConnectCollision` **不能按型別整檔剔除**——`h0054B1`、`h0099B1` 同時被登記為 `Collision` 與 `ConnectCollision`，h0054 那 144 顆 hull 大多是真實地板（只有 4 顆離群）。改用「MSB 有沒有引用」＋距離兩道判準。
  - ⚠️ **環境現況**：`DSPortP1` **還裝在 MO2 裡**（mods 第 2 順位、index 26），故意留著讓下次能直接進場；遊戲與 MO2 已關。要拆＝`agent-bridge/client/mo2ctl.py uninstall DSPortP1`。

- **ModForge 三個子專案抽成獨立 repo**（2026-08-02）：`godot-worldspace-editor`（Godot 前端）、`scene-capture-bridge`（SKSE 遊戲內編輯 mod）、`model-converter`（nif↔glTF）從 `ModForge/sub_projs/` 移到 `projects/` 同層，各自 `git init`、**不帶舊歷史**（使用者決定）。ModForge 原位置留 stub 導引、連結全修、離線測試 1013 綠並已 commit（`adf7fc9`）。
  - 第二輪（同日）：**能獨立的都獨立**——再抽出 `agent-bridge`、`darksouls-port`、`sofia-patch`、`skyrim-voicegen`、`game-data` 五個成 `projects/` 下的 repo；`mod-survey`、`tool-survey`、`followers-patch` 三份純文檔搬進 `analysis/`（不做 repo）。ModForge `sub_projs/` 只剩 `gemini-research`、`inworld-skill-tree`、`living-adventurers` 三個實體 + 八份 stub。ModForge 已 push 到 `17a5039`。
  - **remote**：五個已開 public 並推上（`justty32/skyrim_godot_worldspace_editor`、`skyrim_scene_capture_bridge`、`skyrim_model_converter`、`skyrim_agent_bridge`、`skyrim_voicegen`）。
  - 🔴 **新 open 項：`skyrim_scene_capture_bridge` 的 CI 首跑就紅**（[run 30747127401](https://github.com/justty32/skyrim_scene_capture_bridge/actions/runs/30747127401)，1m4s 掛在 Configure）。**不是這次搬遷造成的**——那份 workflow 原本埋在 `sub_projs/.../.github/`，GitHub 只認 repo 根，所以**從落地以來一次都沒跑過**，現在到了根才第一次執行、也才第一次暴露問題。
    - 根因（2026-08-03 查證完畢，證據齊）：**MSVC STL 把 `stdext::checked_array_iterator` 整段刪掉了**（[microsoft/STL#5817](https://github.com/microsoft/STL/pull/5817)，2025-11-05 merged；連 `_DEPRECATE_STDEXT_ARR_ITERS` 巨集本身都刪了 → **沒有任何 `-D` 能還原**），而 fmt 9.1.0 `format.h:487` 的 `#if defined(_SECURE_SCL) && _SECURE_SCL` 分支正好用它。vcpkg install 失敗 → 後面「找不到 Ninja」只是 cascade。
      - **只有 debug variant 會炸**：`_SECURE_SCL` 在 release 是 0。主力機 Linux clang-cl 那條之所以一直是綠的，是因為 `cmake/x64-windows-skse-clang.cmake` 設了 `VCPKG_BUILD_TYPE release`（xwin 沒 debug CRT），從沒編過 fmt 的 dbg；CI 的 `x64-windows-skse` triplet 沒設，所以 rel+dbg 都編。
      - fmt 是 CommonLibSSE-NG → spdlog 帶進來的傳遞相依。**fmt 在 10.1.0 移掉那段**（[fmtlib/fmt@9bea6ec](https://github.com/fmtlib/fmt/commit/9bea6ec04a79bb0a342ed654025c4a15d2016226)，2023-07-20；9.1.0/10.0.0 還有，10.1.0+ 沒有）。
    - 方向（**`vcpkg.json` 加 version override 這條走不通**）：baseline `cc288af7` 是 **2022-12-19** 的 commit，該 commit 的 `versions/f-/fmt.json` 最高只到 **fmt 9.1.0**、`spdlog.json` 最高只到 **1.11.0** → override 到 10.x/11.x 會「registry 裡找不到該版本」。剩兩條：
      1. **把 default-registry baseline 拉到近期 commit**（一次帶到 fmt 11.x + spdlog 1.15.x，是互相測過的一組；spdlog 相容性：1.11 不吃外部 fmt 10.x、1.12 起吃 10.x、1.14.x 配 fmt 11 會炸、**1.15.0 起才吃 fmt 11.x**）。待驗＝commonlibsse-ng-fork 能不能配 fmt 11。
      2. **自帶 fmt overlay port**（繞過 versioning）。⚠️ 但 `CMakePresets.json` 的 `vcpkg`（MSVC/CI）preset **沒有設 `VCPKG_OVERLAY_PORTS`**，只有 `vcpkg-clang-linux` 有 → 現在 CI 跟本機根本吃不同來源的 `commonlibsse-ng-fork`/`directxtk`，這個分歧本身也該一併修。
    - **不擋開發**：主力機 Linux clang-cl 交叉編譯照樣出 DLL，純粹是 Windows CI 這條路徑的問題。
  - ⚠️ **唯一活狀態**：**`darksouls-port`、`sofia-patch`、`game-data` 還沒有 remote**。前兩者建議 private——sofia-patch 追蹤了從 `SofiaFollower.esp` 逐字提取的 1464 行對白 + 繁中全譯，與 85 檔保留 VIGILANT topic/INFO 原文的重建稿；darksouls-port 是 DS 資產抽取器。
  - 未動到的：所有契約/spec/計畫/驗收文檔與全部生成端 C# 都還在 ModForge。跨 repo 連結與執行期路徑假設**各 repo 同層 clone 在 `projects/` 下**（Godot 前端可用 `godot/texconfig.json`、game-data 可用 `MODFORGE_REPO` 覆寫）。

- **my_skyrim_plugin_1 分支整理**（2026-08-02）：**已結案，無 open 項。** 七條分支逐條交叉編譯實測後，值得留的撈上 `main`（12 份 research 分析、quest-engine spec 換成 court-wizard 的超集版、設計文件進 `archive/`、三條 spike 原始碼進 `vendor/` 不參與建置），推上 remote，**再**刪掉五條已無價值的分支。現存分支只剩 `main` 與 `feature/court-wizard`（後者是活著的平行產品線，程式碼只在那邊）。全部細節在該 repo 的 `BRANCHES.md`。

- **AI 全自動 mod QA 迴圈**：**已結案**（2026-08-02）。Phase 0/1/2/3 全過、MCP 四個 tool 實機驗完、runner 首跑抓到的 ModForge bug 也修掉並用迴圈自己驗證過。**無 open 項**（那 5 個 commit 使用者已自行 push，`origin/master` 含 `17a5039`）。
  - 結論、實測數據、踩坑全在計畫 [workflows/plans/ai-ingame-qa-loop.md](workflows/plans/ai-ingame-qa-loop.md)「六、結案」；要動程式碼從 `projects/agent-bridge/` 的 README 進去。

## 各工作流 session-log

| 工作流 | session-log | open 摘要 |
|--------|-------------|----------|
| feature-dev | [workflows/feature-dev/session-log.md](workflows/feature-dev/session-log.md) | 無 |
| refactor | [workflows/refactor/session-log.md](workflows/refactor/session-log.md) | 無 |
| investigation | [workflows/investigation/session-log.md](workflows/investigation/session-log.md) | 無 |

## 不屬任何工作流的進度

- 無。
