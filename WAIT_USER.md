# WAIT_USER — 等待使用者的事

只列需要使用者親自做/驗證才能繼續的 open 項。完成即移除，不留完成清單。

常見類型：

- 實機或 UI 手動驗證
- 外部帳號、權限、下載、授權
- 本機環境變數或工具安裝
- 不能由 agent 代跑的指令
- 高風險操作的確認

## Open

- **無心人物美化 SE/AE 1.6.1170 適配缺合法來源檔**（2026-08-13）：本機 `/home/lorkhan/skyrim_mods`
  與 MO2 mods 都沒有無心、`Decent Women` 或 `Women's faces` archive，houseCARL 只能讀 Nexus
  metadata、不能下載。使用者需先選一條並透過官方 Nexus 取得檔案：

  - 要**經典無心人物**：下載使用者合法持有的無心人物模組，或 LE `Decent Women` 所需原檔
    （Nexus Skyrim id `14443`）。這條才保留經典外觀，但需 LE→SE 資產／plugin 轉換；作者權限
    限制轉換、修改及資產使用，未取得許可不得把移植版或未授權第三方資產公開重打包。
  - 接受**不同臉的現成 SSE 替代品**：從 Nexus SSE id `5630` 用 mod-manager 下載英文
    `NPS_Female_SE_Eng`。它是自包含的純資料 mod，原則上可在 1.6.1170 使用，但不是經典
    `Decent Women` 原樣，而且不改 companions。

  將 archive 放進既有 `/home/lorkhan/skyrim_mods/` 後通知 agent。後續在 `Modpack-KR-Dev`
  驗證 archive、Form 44／BSA／FaceGen，再依 `AI Overhaul → 外觀 → conflict patch` 建 patch 並做
  實機黑臉／頸縫／AI 驗收。完整調查見
  [wuxin-character-overhaul-se-ae-compatibility.md](workflows/investigation/findings/wuxin-character-overhaul-se-ae-compatibility.md)。

- **母 repo 最新 commit 引用了三個尚未 push 的子模組 commit**（2026-08-12，家用 Manjaro
  實證）：`main` 已快轉到 `b95ee0d`，但 `git pull` 的遞迴子模組 fetch 會報
  `upload-pack: not our ref`。GitHub 與本機都沒有以下三個被母 repo gitlink 指定的 commit：

  | submodule | 母 repo 要求 | GitHub `main` 目前 | 首次被母 repo 引用 |
  |---|---|---|---|
  | `my_skyrim_plugin_1` | `ea6bfeb` | `e257642` | `e4a95e8`（15:56） |
  | `scene-capture-bridge` | `1e44326` | `298566a` | `e4a95e8`（15:56） |
  | `sofia-patch` | `fc25fc1` | `c1c6f80` | `b90b1fb` → `3692362`（13:30–14:25） |

  請在仍持有這三個 commit 的電腦，逐 repo 將包含目標 commit 的 branch push 到各自 GitHub
  remote；上表母 repo commits 均由公司電腦的 `guanyu.lu` 於 2026-08-12 建立，可依時間與
  parent commit 訊息定位原 session。先確認 `git branch --contains <sha>` 與欲推 branch，再
  push，**不要在這台把母 repo
  指標倒退到舊 `main`**，否則會丟掉本批已落地內容。之後在母 repo 執行
  `git submodule update --init --recursive`，三者都能 checkout 才算完成。這台其餘子模組已
  對齊；目前只有上述三個仍顯示 gitlink mismatch。

- **scene-capture-bridge 離線 catalog Browser 實機驗收**（2026-08-12 開條，**2026-08-13 家用機大幅修正**）：

  **⚠️ 真正的阻礙不是 toolchain，是那顆 commit 沒推。** 原本這條寫「公司機沒有 Linux
  clang-cl+xwin toolchain」——家用機**有，而且 2026-08-13 實測整條 build path 是活的**
  （`rm -rf build/release-clang-cl-linux` → `cmake --preset build-release-clang-cl-linux`
  → build 29/29 通過；import 表只有 KERNEL32/ole32/VERSION/USER32/SHELL32，靜態 CRT 乾淨；
  `scripts/deploy.sh` 已部署，crc32 `7e94ad30`）。真正卡住的是：**DLL 消費端程式碼在母 repo
  gitlink 指的 `1e44326`，那顆不在家用機也不在 GitHub**（`git cat-file` 確認），還躺在公司機。
  本機 HEAD `298566a` 的 `Catalog.cpp` 只有 **runtime-only** 版，沒有 json 讀檔/merge/
  provenance/global-source-order gate。**在那顆被 push 上來之前，離線 catalog 的實機驗收做不了**
  ——見本檔上面「母 repo 最新 commit 引用了三個尚未 push 的子模組 commit」條目，那三顆裡就有它。

  **產生端（ModForge）已在家用機對真實完整 load order 跑通**（2026-08-13）：

  | | 結果 |
  |---|---|
  | resolved load order | 59 個實體檔（8 esm + 9 esl + 42 esp），full+light 混合 |
  | `catalog build` | 59 sources / 1,408,820 records / 12.8s |
  | `catalog export-json` | 1,338,046 winners（70,774 筆被 override）/ 4.6s / **468 MB** |

  重建方式：`scripts/resolve_load_order.py Play-KR > lo.txt`（把 MO2 profile 的 load order 依
  mod 優先序解成實體路徑；Linux 沒有活的 usvfs 可讀，只能自己解），再
  `dotnet run --project src/ModForge.Cli -c Release -- catalog build <db> $(< lo.txt)`。
  ⚠️ `catalog build` 的 plugin 參數順序**就是** load order index，別打亂。

  **三個發現（都已量化，不是推測）：**

  1. **468 MB 裡約 97% 是 DLL 永遠用不到的。** `PlacedObject` 一種型別佔 1,015,529 筆（72%）
     ——那是世界裡的 REFR 實例，而 Browser 是 Object Window，只列 base object。
     `catalog export-json` **沒有型別過濾**。照 DLL 的 21 個 `kTypes` 過濾後實測：
     **468 MB → 11 MB**，同 schema v1、同 59 sources、33,737 筆，EditorID 覆蓋率
     33,736/33,737。這直接關係到本條原本要求的「不造成數 GB 啟動延遲」——**建議把型別過濾
     做進 `export-json`（例如 `--placeable`），不要指望 DLL 端 parse 完 468 MB 再丟掉**。
  2. **過濾軸必須是 record_type，不能是 model_path。** ARMO 的模型掛在 ARMA 上，Mutagen 的
     `IModeledGetter.Model` 對它是 null；拿 model_path 當條件會把 4,944 件護甲整批砍掉。
  3. **`Catalog.cpp` 的 `kTypes` 裡 `Armor` 是死條目。** CommonLibSSE 標頭確認
     `TESObjectARMO` 繼承鏈裡沒有 `TESModel`（走 `TESBipedModelForm`），所以緊接著那道
     `base->As<RE::TESModel>()` gate 會把**所有護甲**濾掉——列在可瀏覽型別裡但一筆都進不了
     Browser。`StaticCollection` 預測同樣掛零（待實機確認）。

  **還沒做完的：runtime-only Browser 實機驗收。** DLL 已部署、遊戲已由
  `mo2ctl launch --no-wait` 啟動（Play-KR profile），但**沒人進去點過**。接手的 agent：請使用者
  F1 → `Scene Capture Bridge` → Browser 頁（首開觸發全 form-array 掃描，注意頓不頓），然後讀
  `<Proton prefix>/drive_c/users/steamuser/Documents/My Games/Skyrim Special Edition/SKSE/SceneCaptureBridge.log`
  的 `Catalog:` 那行對帳。**離線算出來的預測值**：placeable bases **27,246**、
  from **33** plugin(s)、**19** type(s)（不是 21）、skipped **6,491** model-less（其中 4,944 是護甲）。
  type 下拉選單裡**應該找不到 Armor**——找不到就是發現 3 實錘；找得到就是判斷錯，
  `TESObjectARMO` 在 runtime 另有取得 model 的路徑。兩種結果都要記回來。

  **`1e44326` 到手之後才輪得到的**：確認 `TESDataHandler::files` 過濾出的 loaded sequence 與實際
  override precedence 一致，驗 Browser loaded/match、EditorID 搜尋/顯示與 preview/place；再各測
  缺一個、多一個、反轉順序、壞 JSON 時皆退回 runtime-only。另需確認 MO2 process 內
  `Data/<plugin>` 可讀/hash，才能設計 SHA gate；現階段 UI 會明示 SHA 尚未驗證。
  ⚠️ 注意 `loadorder.txt` 有三個 CC plugin（`ccbgssse068-bloodfall`、`ccbgssse069-contest`、
  `ccvsvsse004-beafarmer`）**磁碟上根本不存在**，遊戲直接跳過；任何 resolver 與「缺一個」測試都得
  先把這個既有的洞算進去，別誤判成 bug。

- **BG3 場景佈局實檔驗證**（2026-08-11）：桌面研究已確認 LSLib 可把 BG3
  `Levels/` 下的 `.lsf` 轉成可讀 `.lsx`，但尚未用使用者持有的遊戲資料驗證 placement
  欄位能否無損對映 ModForge `placements`（位置、旋轉、尺度、base/resource identity）。下次
  有 BG3 安裝或合法抽取素材時，挑一個小型 level 做 `.lsf` → `.lsx`，記錄欄位與一組實例，
  再決定是否開 converter/spec 工作；沒有實檔前不宣稱 port pipeline 可行。評估框架與候選
  比較見 [port-source-survey](analysis/port-source-survey/README.md)。

- **darksouls-port 門洞仍卡，參數已備好但未套用**（2026-08-06，**使用者決定先收現狀**；2026-08-11 補上前置條件與備援）：症狀是使用者實走回報「只有過門會卡，過道上走基本沒問題」——根因是平面內填洞，有門洞的牆其凸包把門洞填實。`--ghost-tol` 是**每顆 hull** 的容許量，一個門洞切成好幾顆、每顆合法填 0.24 m²，加起來就把門框內縮到卡人。

  **⚠️ 動手前的前置條件**：`tools/collision_hulls.py` 的相依全是 lazy import，跑起來才會炸。**目前哪個 venv 都不齊**（`model-converter/.venv` 只有 numpy + pygltflib）。**權威 setup 在 `tools/collision_hulls.py` 檔頭 docstring**（2026-08-11 核對程式碼）：專屬 venv + `soulstruct` / `soulstruct-havok` 從 GitHub 源碼裝（`pip install -e ./soulstruct && pip install --no-deps -e ./soulstruct-havok`——PyPI 的 soulstruct 只到 2.3.2 < havok 要求的 2.4.0，且**必須 editable**，否則漏 package-data JSON 會 `FileNotFoundError`），再 `pip install numpy scipy colorama networkx vhacdx trimesh shapely`。

  兩個容易踩的點（`p1/P1-INGAME-FINDINGS.md`「工具現況」節已於 2026-08-11 同步修正，含逐項核對表）：

  - **`shapely` 是必要的，且正好在本任務的關鍵路徑上**——`_ghost_area()`（line 141 import shapely）由 `_split_by_ghost()` line 223 呼叫，那就是 `--ghost-tol` 的核心機制。漏裝會在要跑的那一步失敗。
  - **`vhacdx` 不需要**——只在 `_vhacd()` 內 import，而 `--method` 預設是 `components` 而非 `vhacd`。

  執行步驟：

  1. 照 `tools/collision_hulls.py` 檔頭建好 venv 與相依。
  2. `--ghost-tol` 預設 0.25 → **0.02**（h0006 實測：hull 233 → 302，總憑空面積 2.0 → 0.1 m²，**+30% hull 換 20 倍改善**）。
  3. 全量重跑 47 個 hkx。全量代價估計：載體 NIF 341 → 約 440 塊。
  4. `rm -rf out/DSPortP1` 後重新打包 → `mo2ctl install --force` 重裝 → 進場走一次門。

  **若 0.02 還是卡**：下一個懷疑對象是門框側壁（reveal）自成 patch 後的**厚度**，那要調 `--planar-thresh`（現行預設 **0.15**），**不是繼續降 `--ghost-tol`**。（兩個預設值均於 2026-08-11 對 `tools/collision_hulls.py` 核對：`--ghost-tol` 0.25 於 line 327、`--planar-thresh` 0.15 於檔頭說明。）

  **`DSPortP1` 目前仍裝在 MO2 裡**（新版碰撞、332 個載體），故意留著讓下次能直接進場。技術細節見 [P1-INGAME-FINDINGS.md](projects/darksouls-port/p1/P1-INGAME-FINDINGS.md)。
