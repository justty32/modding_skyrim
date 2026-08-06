# SESSION-LOG — 進度日誌 hub

只放還沒完成的活狀態。完成的不留在這裡；完成後濃縮到對應工作流的 landed/archive、release note、或 git log。

待使用者親自做/驗證的事放 [WAIT_USER.md](WAIT_USER.md)。

建議單一 `session-log.md` 保持短小，只為「下一個 session 接得上」。若超過 50 行，刪舊留新，或按工作流/主題拆檔。

## 最新進度

- **三個 agent 並行：碰撞修正實機複驗、流水線 P1 落地、mod 庫清理**（2026-08-06）：本 session 把三條線同時推進——Claude 做 darksouls-port 碰撞，**codex CLI** 做流水線 P1，**pi + deepseek-v4-pro** 做 mod 庫。三者各據一個獨立 git repo（`projects/darksouls-port` / `projects/agent-bridge` / `~/notes`），不搶 index.lock。
  - **跨 agent 的通道是 tmux，不是 stdin 注入。** 「找到 process 丟 stdin」在這台機器上做不到：互動模式的 stdin 是 tty，寫 `/proc/<pid>/fd/0` 是寫到終端裝置（方向反了），而唯一能塞進 tty 輸入佇列的 `ioctl(TIOCSTI)` 被 `dev.tty.legacy_tiocsti=0` 關掉（kernel 6.2 起預設關）。**tmux 持有 pty master，`send-keys` 是合法寫入**；`capture-pane` 讀回。使用者可隨時 `attach` 插手，實際上也這樣做了。
  - **darksouls-port P2 碰撞修正完成**（commit `1d65760`、`20c6fad`）：`decompose_components()` 改成「近平面 patch 廣度優先成長 → 憑空面積遞迴二分」，V-HACD 從這條路徑移除。**全 47 檔憑空碰撞面積 27,774 m² → 314 m²（降 98.9%）**，hulls 4,893 → 17,706，載體 NIF 116 → 332（過濾後）。實機複驗：玩家 Z 從 19973 降到 **19937**，低的 0.54 m 正是舊版增厚地板的量。使用者實走：**「只有過門會卡，過道基本沒問題」**——根因(b) 幽靈牆消失，根因(a) 門洞填實仍在。細節與下一步參數見 [projects/darksouls-port/p1/P1-INGAME-FINDINGS.md](projects/darksouls-port/p1/P1-INGAME-FINDINGS.md)。
    - **判準必須是「憑空面積」而不是 patch 自己的填充率**：patch 邊界本來就鋸齒狀，凸包蓋到的是隔壁 patch 的真實幾何。填充率版本實測會把平坦的牆切成單一三角形（h0006 47→319 hulls）。同理 fill 只能在 patch **長完之後**檢查，邊長邊檢查等於自我封鎖（47→231）。
    - **剩下的 314 m² 全集中在門洞，是因為 `--ghost-tol` 是逐顆 hull 的容許量**——門洞切成數顆、每顆各填 0.24 m² 就把門框內縮到卡人。掃描出 0.02 是甜蜜點（+30% hull 換 20 倍改善），**使用者決定先收現狀不套用**。
    - **`ModForge package` 會併進既有輸出目錄**，不會清乾淨：被過濾掉的 5 個載體 NIF 就這樣一路混到 MO2。重新打包前先 `rm -rf out/DSPortP1`。`mo2ctl install --force` 本身是真的取代（實測 332 而非 337）。
  - **流水線 P1 完成**（agent-bridge `b0e87ad`，codex 產出，9 個測試綠）：`mo2ctl inspect <archive> [--write-choices]`、`install --priority bottom|top|before:|after:` ＋ `--fomod-choices`、zip-slip 防護、7z/rar 偵測（無工具則 `handoff_user`）、FOMOD 宣告式解析與可重放、`archives.txt` 的 unmanaged BSA 維護、**優先權預設從 top 改為 bottom**、8 個單元測試。解析不了的 FOMOD 變體（`conditionalFileInstalls`、flag 傳遞、step 可見性條件）一律 `handoff_user`，不猜。
  - 🔴 **P0.2「清掉 3 條 stale CC 條目」證實守不住**（profiles repo `ae3cf71`）：`Default/loadorder.txt` mtime 是 2026-08-05 20:37，**玩一次遊戲引擎就把那三條寫回去**，並把 `plugins.txt` header 換成 MO2 版、整檔重輸出成 CRLF。已把現實 commit 成新基準——與其每次產生雜訊 diff，不如讓靜態關卡的輸出保持乾淨。**這條計畫步驟本身是徒勞的，不要再花力氣清它。**
  - **mod 庫 L1+L2 執行完畢**（`~/notes` commit `5eb1239`）：L1 完全重複 33 檔 / 0.47 GiB、L2 舊版本 74 檔 / 5.79 GiB。⚠️ **`.quarantine/2026-08-06/` 在建立後被刪除**，107 筆沒經 restore 就永久消失（ext4、無快照、不在 Trash）。**逐筆查證後實質損失為零**：L1 的孿生副本全在庫內，L2 的 64 組有 62 組留著新版，剩 2 組被刪光但都是使用者當場指定全刪的。真正的代價是**復原路徑沒了**，以及 MongoDB 有 107 筆標著 `quarantined_at` 但檔案不存在的不一致（重掃前要處理）。事故記錄在 `~/notes/projects/modding/skyrim/docs/2026-08-06-deletion-incident.md`。
  - **mod 庫的 MongoDB 不在 systemd 那個服務上**：資料在 `~/data/mongodb`，要手動起 `mongod --dbpath ~/data/mongodb --port 27018`。所有治具要帶 `SKYRIM_MONGO_URI=mongodb://127.0.0.1:27018`。systemd 的 `mongodb.service`（27017）是空的。

- **第三方 mod 流水線 + mod 庫建檔，兩份計畫開工**（2026-08-04）：兩份新計畫 [workflows/plans/third-party-mod-pipeline.md](workflows/plans/third-party-mod-pipeline.md)（取得→安裝→驗證）與 [workflows/plans/mod-library-catalog.md](workflows/plans/mod-library-catalog.md)（`~/skyrim_mods` 建檔與清理）。**程式落 `~/notes/projects/modding/skyrim/`**（使用者授權的例外，與 rimworld 那套同構；設計文件留本 repo，程式不進本 repo）。
  - **建檔完成**：1,692 個壓縮檔 → 去重後 **1,659 筆 / 85.7 GiB** 進 MongoDB（db `skyrim`），檔名解析 99.0%、0 失敗、1 分 46 秒。抄了 rimworld 最貴的教訓：`$set`（磁碟事實）／`$setOnInsert`（養成資料）從第一版就分離。
  - **DLL runtime 檢查完成**：186 個含 dll 的壓縮檔全查（自寫 PE export 解析，不載入 dll），**151 相容 1.6.1170 / 9 不相容 / 26 無法判定 / 0 失敗**；解析器已對 houseCARL 的已裝層讀值校驗通過（同樣抓到那 5 個 version-LOCKED）。
  - **L3 隔離已執行**：3 個鎖 1.6.640 的框架舊副本（JContainers 4.2.3 / PapyrusUtil 4.4 / Fuz Ro D'oh 2.3）移入 `~/skyrim_mods/.quarantine/2026-08-04/`。**價值是移除「重裝框架抓到舊版→109 個 mod 一起壞」的引信，不是回收容量**（僅 1.61 MiB）。restore 往返實測過。
  - **清理的空間上限比預期小得多**：L1 完全重複 0.47 GiB + L2 真·舊版本 4.76 GiB ≈ **5.2 GiB / 85.7 GiB（6%）**。**本任務的價值在盤點與風險移除，不在容量。**
  - **修掉一個會誤刪的判準**：原本按 `nexus_mod_id` 分組判「舊版本」是錯的——一個 mod 頁會出多個不同檔案（實證：`mod 10917` = Beyond Skyrim 的 Assets + Bruma + DLC patch 三個都需要）。分組鍵加上正規化檔名後 115 組 → **65 組**，避免 **2.64 GiB 誤刪**。排序鍵必須用檔名的 10 位 Nexus timestamp（版本字串跨 scheme 不可排序，大小更不可靠）。
  - **L2 無法全自動**：`housecarl_nexus_mod` 只回最新 MAIN 檔版本，不回逐檔清單，所以問不到「這檔是否被 Nexus 歸為舊版」。65 組人工審可行，不值得為此擴 houseCARL。
  - **流水線 P0 完成 4/5**：MO2 profile 走 git（repo 在 `<instance>/profiles/`，`.gitattributes` 設 `* -text` 保 CRLF，3 個 commit）、清掉 3 條 stale CC 條目（plugin 56→53 且全部 resolve）、開 `QA` profile（與 `Default` **只差 AgentBridge 一行**）、**AgentBridge 移出正式 profile**（它先前一直啟用著，等於每次玩遊戲都開著 5099 那個會執行任意 console 指令的 port）。
  - 🔴 **P0.2 受阻**：`housecarl_set_mo2_instance` 在 Linux 下不能用，它沒把 `ModOrganizer.ini` 的 Wine `Z:\` 前綴翻回 Linux 路徑。**第三個同族 Linux 路徑 bug**，見 [WAIT_USER.md](WAIT_USER.md)。影響有限（explicit-paths mode 全程可用，只失去跨 profile 檢查）。
  - **crash triage 建好並實查 20 份既有 log**：`triage_crash.py`（list/show/blame/recurring）。三個平台前提寫進計畫 G5：**Proton 下約 40% 的 log 沒有 call stack**（Wine 的堆疊回溯不完整，所以「crash log 會指名兇手」只有六成成立）、相隔一秒的第二份 log 是 crash handler 自己崩掉的副產物要去重、`Private: 117440444.07 MB` 是 Wine 垃圾值。
  - **2026-08-02 那次 agent-bridge 事故拿到直接證據**：`crash-2026-08-02-08-41-23.log` uptime **6,599ms**（README 記「~6.6s Papyrus VM init」分毫不差），call stack 是 `<unmapped> → AgentBridge.dll+0054404 → ConsoleUtilSSE.dll spdlog::logger::sink_it_`。**README 那條「別跟別的 plugin 搶同一段序言」的通則原是從症狀推論，這份 log 直接指出碰撞對象。** 該 detour 已放棄、AgentBridge 已移出正式 profile，此案結。
  - **順帶發現**：這個 load order **沒有慣性肇事的第三方 plugin**（堆疊頂端幾乎全是引擎與 d3d11/VCRUNTIME）；`MCM-Unlocked.dll` 在 2026-07-05 那次連續佔 frame [2][3][4][5]，是唯一值得留意的第三方線索。另有兩組同址重複的引擎級崩潰（`SkyrimSE.exe+02C3957 lock inc [rax+0x170]`、`SkyrimSE.exe+0146110`），同址重現代表可重製。
  - **下一步（未動工）**：P1.4 Nexus 補值（查在架狀態標 `never_delete`，是 L2 審核的前置）、L1 去重（0.47 GiB，唯一可自動的一級）、流水線 P1 的 archive+FOMOD 解析層（整條流水線目前斷在這裡：`mo2ctl install` 只吃已解壓資料夾，零 archive、零 FOMOD 支援）。

- **工作區納入版控並推上 GitHub**（2026-08-03，**推翻 2026-07-17「這裡不做版控」**）：母 repo＝`git@github.com:justty32/modding_skyrim.git`（**public**），`projects/` 下 **10 個子專案為 submodule**。首版 commit `80c9386`，內容 **2.2 MB / 753 檔全是文字**。
  - 為此新開三個 **private** repo 並推上：`skyrim_darksouls_port`、`skyrim_sofia_patch`、`skyrim_game_data`（先前沒有 remote；內容敏感——DS 資產抽取器、逐字提取的對白）。ModForge 的 `110b0fc` 也推了，否則 submodule 會釘在未 push 的 commit 上。
  - `.gitignore` 排除 **490MB 的他人 clone**：`external/frameworks/`（193M）、`analysis/tool-survey/repos/`（294M）——著作權 + 體積，且各自帶 `.git`；`findings/`、README、`external/mods/` 保留。
  - **驗收＝實跑 `git clone --recurse-submodules` 到暫存區**，10 個 submodule 全抓下來且有內容，不是只看 push 成功。
  - 🔴 **唯一沒納入的：`projects/houseCARL`**——別人 repo 的 fork 且本機 HEAD 在未推上 fork 的 rebase 分支，釘成 submodule 會讓別人 clone 直接失敗。已 gitignore，解法見 [WAIT_USER.md](WAIT_USER.md)。

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
