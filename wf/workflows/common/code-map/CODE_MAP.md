# CODE_MAP — 原始碼導航

本母 repo 主要保存分析與工作流文件；可建置的原始碼位於 `projects/` 的獨立
repo/submodule。修改前先從下表進目標專案，遵守該專案自己的 README、AGENTS 與
CODE_MAP。不存在的根層 source tree 不另造索引。

## 專案入口

| 專案 | 程式碼／文件入口 |
|------|------------------|
| ModForge | [`projects/ModForge/workflows/common/code-map/CODE_MAP.md`](../../../../projects/ModForge/workflows/common/code-map/CODE_MAP.md) — generator domain、CLI、schema、tests 的完整分域索引 |
| agent-bridge | [`projects/agent-bridge/README.md`](../../../../projects/agent-bridge/README.md) — SKSE HTTP runtime；[`client/README.md`](../../../../projects/agent-bridge/client/README.md) — Linux client/MCP；[`QA-SCHEMA.md`](../../../../projects/agent-bridge/client/QA-SCHEMA.md) — qa.json contract |
| scene-capture-bridge | [`projects/scene-capture-bridge/README.md`](../../../../projects/scene-capture-bridge/README.md) — SKSE runtime；`src/CatalogFile.*` + `tests/CatalogFileTests.cpp` 是不依賴 SKSE 的 ModForge scene-catalog v1 parser/FormKey index/provenance+runtime global-source-order gate/metadata merge；`tests/RunModForgeCatalogContract.cmake` 另以真實 ModForge CLI 串 full/light plugin→catalog exporter bytes→consumer 的 MinGW CTest，`tests/CatalogCompatibilityProbe.cpp` 可把真實 catalog／resolved path list 餵進同一 consumer gate；`Catalog.cpp` 由 `TESDataHandler::files` 取得 full/light 全域 loaded sequence，kDataLoaded 後把合格離線 EditorID/name 補進 Browser |
| godot-worldspace-editor | [`projects/godot-worldspace-editor/README.md`](../../../../projects/godot-worldspace-editor/README.md) — `godot/placements_io.gd` 是 placements producer；`tests/test_placements_contract.py` 以 Godot headless 真實 exporter→ModForge CLI→ESP REFR 讀回；`godot/model_fetch.gd` 優先遵守 `MODFORGE_NIF2GLTF_BIN` executable hook 並 fail-closed 管理 `.gltf + .bin` cache，`tests/test_model_fetch_contract.py` 以 synthetic NIF→production converter→Godot `GLTFDocument` 驗 mesh/座標與壞輸出清理重試 |
| model-converter | [`projects/model-converter/README.md`](../../../../projects/model-converter/README.md) — `PROTOCOL.md` 定義 nif2gltf/gltf2nif 黑盒 CLI；前者由 Godot ModelFetch live contract 消費，後者由 darksouls-port production batch live contract 消費 |
| skyrim-voicegen | [`projects/skyrim-voicegen/README.md`](../../../../projects/skyrim-voicegen/README.md) — `voicegen.py` 是 ModForge TTS 黑盒 producer；`tests/fake_fish_engine.py` 只作 live contract 最末端 fixture，ModForge `VoiceLiveContractTests.cs` 真跨 process 驗完整 args、合法 WAV 與 failure cleanup |
| game-data | [`projects/game-data/README.md`](../../../../projects/game-data/README.md) — `extract.sh` 先做全 batch stem collision preflight，再以 sibling staging + paired backup/rollback 原子發布 gamedata/questnodes；`tests/test_extract.py` 用會真寫檔的 fake dotnet 驗 known-good 保留與零半成品 |
| darksouls-port | [`projects/darksouls-port/README.md`](../../../../projects/darksouls-port/README.md) — `tools/p1_batch.py` 以同目錄 staging 呼 sibling production gltf2nif，失敗撤下 stale packageable target；`tests/test_model_converter_contract.py` 再用 model-converter production reader 驗 BSTriShape、材質、座標及 bhk hull |
| sofia-patch | [`projects/sofia-patch/README.md`](../../../../projects/sofia-patch/README.md) |
| my_skyrim_plugin_1 | [`projects/my_skyrim_plugin_1/README.md`](../../../../projects/my_skyrim_plugin_1/README.md) — DaylightDungeon SKSE plugin；打包與離線測試在 `scripts/`，**PowerShell 與 POSIX 各一套、彼此獨立**：`pack.ps1`／`pack.sh` 打包，`test_packaging.ps1`／`test_packaging.sh` 驗打包契約（synthetic CMake cache/DLL、zip 內 MO2 layout、`--output-dir` 防護、CLI exit code），`test_quest_prf.ps1`／`test_quest_prf.sh` 驗 quest PRF primitives（純 stdlib g++，不需 SKSE／CommonLib） |
| houseCARL | [`projects/houseCARL/README.md`](../../../../projects/houseCARL/README.md)；Linux 適配結論在 [`linux-manjaro-mo2-runbook.md`](../../../../analysis/houseCARL/answers/linux-manjaro-mo2-runbook.md) |

## agent-bridge semantic QA 快速圖

| 類別 | 檔案 | 職責 |
|------|------|------|
| Runtime | `projects/agent-bridge/src/GameActions.*`, `MessageBox.*`, `StateActors.*`, `State.*`, `Routes.*` | game-thread actor/dialogue/MessageBox actions、structured state、HTTP contract |
| Linux client | `projects/agent-bridge/client/bridge.py`, `qa_runner.py`, `qa_mcp.py` | HTTP calls、declarative QA steps、MCP semantic tools |
| Tests | `projects/agent-bridge/client/test_bridge.py`, `test_qa_runner.py`, `test_qa_mcp.py` | request shape、retry/validation、MCP routing |
| Docs | `projects/agent-bridge/README.md`, `client/README.md`, `client/QA-SCHEMA.md` | runtime API、client entry、qa.json contract |

新增／刪除原始碼檔案或改變職責時，先更新目標 repo 的 CODE_MAP；目標 repo 沒有
細分 CODE_MAP 時，才維護本頁的快速圖或 README 入口。

## 母 repo 本機工具

| 檔案 | 職責 |
|---|---|
| `tools/check_markdown_links.py` | 掃描母 repo 與非 `projects/` 工作區 submodules 的 tracked Markdown links；驗證檔案與 GitHub-style heading／explicit HTML anchors，理解 canonical symlink 位置，並支援 CI 的 `--skip-symlinks` 邊界 |
| `tools/test_check_markdown_links.py` | Markdown link checker 的相對路徑、broken file／anchor、重複與 Setext heading、closed ATX heading、標題內含 inline link、fence（連結側與 anchor 側各一條）、CLI 與 symlink 行為；失敗訊息要指名缺哪個 anchor；Windows 缺 file-symlink privilege 時只 skip symlink-only cases |
| `tools/check_submodule_pins.py` | pre-push 核心：只檢查本次 push ref 相對 remote tip 有變動的 gitlink；本機存在但任何 remote-tracking ref 都不可達時 fetch 後 fail closed |
| `tools/test_check_submodule_pins.py` | 以臨時 bare remote、母 repo 與真實 submodule 驗未變／已推／未推 pin、未初始化／本機缺 commit 與刪分支邊界 |
| `tools/check_code_map_coverage.py` | 檢查每一支工具腳本是否在某份索引頁被指名；**走訪各 submodule 自己的 git**，不靠母 repo 的 `git ls-files`（它到 gitlink 就停，正是 `check_markdown_links.py` 出過的洞）。已知缺口以 `code_map_coverage_baseline.txt` 當 ratchet：清單內靜默、清單外一律非零 exit；baseline 指到已刪除的檔案也 fail closed，清單不會腐化成永久藉口 |
| `tools/code_map_coverage_baseline.txt` | ratchet 的豁免清單，**目前是空的**（2026-08-26 盤點時 36 支未索引，同日全部補進本頁）。留著是為了下一次真的有不該進索引的腳本時寫上路徑與理由；**是債不是豁免**，且 stale 行會 fail closed |
| `tools/test_check_code_map_coverage.py` | 以真實巢狀 submodule 的合成工作區驗已索引／未索引／submodule 內可達／baseline 靜默／baseline 不通殺／stale baseline／未追蹤檔不算數；7 條全部經突變測試證明能變紅 |
| `instance/tools/resolve_load_order.py` | 把唯一 profile（`modpack-main`）的 enabled `loadorder.txt` 解析成真實 plugin paths；provider precedence 是 shared `overwrite` → `modlist.txt` 最高優先 enabled mod → game `Data`，任何 enabled missing plugin 以非零 exit fail closed |
| `instance/tools/test_resolve_load_order.py` | synthetic MO2 tree 驗 overwrite winner、named-mod priority、implicit master 與 disabled／missing plugin 行為 |
| `mod-library/l10n/tools/build_vigilant_book_desc_overlay.py` | 以指定版本的 VIGILANT 正體 plugin 同時作結構 seed 與術語來源，只補齊精確 45 筆仍為英文的 `BOOK.DESC`；筆數、record topology 與所有非目標 payload 都 fail closed，並輸出逐筆 ledger |
| `instance/tools/build_profile_checkpoint.py` | 唯讀 MO2 profile 快照：`modlist.txt` 行序即 priority，逐 mod 算排除 `meta.ini` 的 payload `tree_sha256`，並對 `profiles/manifest.json` 標記 issue（安裝目錄缺、manifest 無此筆、`source_path` 缺或不存在、source 落在 `/tmp`）。**刻意預設 exit 0**——checkpoint 本來就要能記錄壞掉的狀態；要當閘門必須加 `--fail-on-issues`（2026-08-26 補，之前是恆真） |
| `instance/tools/reconcile_profile_sources.py` | 對 checkpoint 裡 enabled 但無 manifest 紀錄者解析 `meta.ini` 的 `installationFile`：`Z:/` 轉 POSIX → 絕對路徑直用 → MO2 `downloads` 相對路徑 → fallback roots 遞迴比對 basename，且**只有唯一命中才採用**（多命中標 ambiguous）。永遠 exit 0，只寫報告不動檔案 |
| `instance/tools/audit_profile_recovery.py` | 吃 checkpoint，只驗 enabled mod 的還原來源：archive 比對宣告的 SHA-256；directory 要求根目錄有 `MANIFEST.sha256`、逐檔驗 hash 並拒絕逃出根目錄的相對路徑。任何一項不是 `*_pass`（含「沒有 MANIFEST」的 `directory_unverified`）即非零 exit，fail closed |
| `instance/tools/backfill_profile_manifest.py` | 把 reconcile 報告中「有精確 archive 但 manifest 未收錄」者補成 manifest 記錄；`fomod_choices` 一律寫 `unrecorded`，明示「有原始 archive，但不宣稱可重現安裝選項」。**永遠 exit 0，不是閘門**；寫到 `--output` 而非原地覆寫 |
| `instance/tools/audit_overwrite.py` | 對 shared `overwrite` 做不可變快照：全樹逐檔 SHA-256 加一個 `treeSha256`，按固定規則分類成 creation_club／racemenu_export／generated_behavior／runtime_state／qa_cache／user_config／unclassified；遇 symlink 直接 raise 拒絕快照。**預設即使有 unclassified 也 exit 0**，閘門要加 `--fail-unclassified` |
| `instance/profiles/tools/check_profiles.py` | 現役 profile 的結構稽核。**2026-08-23（`241522d`）起會讀 `ModOrganizer.ini` 的 `selected_profile=` 比對 `CANONICAL_PROFILE`**——在那之前它只看 profile 目錄，ini 停在一個不存在的 profile 名也照樣 PASS，是本工作區記錄的第一個恆真檢查 |
| `instance/profiles/tools/profile_workflow.py` | profile repo 的分支模型（`main → feat/* → release/* → main`）操作輔助 |
| `mod-library/db/cleanup_report.py` | 清理分級的唯一判準實作：L1 同 SHA-256 多路徑／L2 同 `(nexus_mod_id, grouping_key)` 組內舊版／L3 含不相容 SKSE dll 且無 esp、bsa／L4 legacy 命名且不在 `mine/`（只標記不動）。**三條例外優先於判準**：已安裝那版、有對應版本漢化包的版本、Nexus 上 gone/hidden 或 `never_delete` 者一律 keep。預設唯讀；`--write-decisions` 才寫 Mongo，且寫前整庫 dump、不覆寫人工決策 |
| `mod-library/db/quarantine.py` | 清理的執行端，**整條管線不呼叫 rm**：候選被 move 進隔離區並保留相對路徑，每次移動寫回 Mongo 供 `restore` 原地還原。選擇器是寫死的具名 query，刻意不提供自由查詢；`move` 需同時給 `--reason` 與 `--yes` |
| `mod-library/db/nexus_intake_check.py` | Nexus 入庫前的檔案比對閘門（`test_nexus_intake_check.py` 的受測對象）：list-files／verify-download／dedupe／parity／scan-report 各自 fail closed，ingest 預設 dry-run |
| `mod-library/db/scan_mod_library.py` | 掃庫與 Mongo bootstrap；`quarantine.py` 與 `agentctl/tools/check_dll_runtime.py` 都從它 import `connect` |
| `mod-library/db/fetch_nexus_status.py` | 唯一會打 Nexus v1 API 的富化工具。`NEXUS_API_KEY` 未設就直接 exit（明文拒絕退化成爬 HTML）；`--interval` 低於 1.0 秒拒絕啟動；429／5xx 指數退避，連續失敗以 exit 2 保留可續跑點；配額低於門檻主動停止。判為 gone/hidden 會**寫入 `never_delete=True`**。**注意**：resume 提示印的仍是 2026-08-23 拆分前的舊路徑 |
| `mod-library/db/report_upstream_status.py` | 把 enabled MO2 層對上 Nexus 富化結果，產出可用性與版本漂移報告。版本比較刻意保守：MO2 日期 placeholder 與含 qualifier 的版本一律判 `unclear` 而非 different。`--require-fetch-complete` 擋下「富化沒跑完就出報告」。**注意**：四個預設路徑指向不存在的 `mod-library/qa/reports/` 與 `mod-library/logs/`，不給參數直接跑會炸 |
| `mod-library/db/l4_review.py` | 把 L4 用純檔名／路徑 regex 分成 11 桶並給建議動作，**分桶順序即優先權**。只是輔助清單：不移動、不刪除、不隔離、不寫 Mongo，永遠 exit 0 |
| `mod-library/db/resolve_legacy_md5.py` | legacy MD5 命名的回溯解析 |
| `mod-library/db/ingest_candidates.py` | 把候選 fixture 灌進 `candidates`：`_id` = 正規化 `source_url` 的 SHA-256。**已被 rejected 的文件永遠跳過不覆寫**；人工欄位只走 `$setOnInsert`。有任何失敗筆數以 exit 1 收尾 |
| `mod-library/db/review_candidates.py` | `candidates` 的人工審閱狀態機。目標解析到多筆即視為 ambiguous；**只要有任一目標無法唯一解析就整批中止、一筆都不改**並 exit 1 |
| `mod-library/db/test_default_paths.py` | 釘住 2026-08-23 repo 化之後的路徑契約：整庫 dump 與 log 必須落在 repo 外，報告類必須落在 repo 內 `audits/`，兩個環境變數覆寫要被三支都吃到。以 stub 掉 `bson` 的方式載入，不需 pymongo 也不需 DB。5 pass |
| `mod-library/db/test_nexus_intake_check.py` | `nexus_intake_check.py` 的行為契約：欄位不符要指名是哪個欄位、stale file_id 要被標出、同名不同內容只標 review 不靜默放行、過程不碰 library 任何檔案。28 pass |
| `mod-library/l10n/tools/inline_translation_overlay.py` | 漢化層的底層引擎（只被 import）：以 **record identity（signature + raw FormID）+ tag + 同 tag 出現序**把譯文 seed 對上官方 ESP，官方 ESP 永遠是唯一結構母本。`verify_overlay` 事後驗 record 數／identity／group path／subrecord topology 全等且只有目標 payload 變動。**兩處是靜默略過而非 fail closed**：解碼失敗的 zstring 回 `None` 後整欄跳過；非手動列的 control-token 與換行數不符只 `continue` |
| `mod-library/l10n/tools/enairim_cht_common.py` | EnaiRim 系的共用層，**比 overlay 嚴一級**：`exact_zip` 同時驗 archive basename、SHA-256、zip CRC 與成員清單完全相等；`inline_rows` 走字典直譯，六種情況（來源不在字典／target 空或未變或含 U+FFFD／control token 多重集不符／換行數不符／總筆數不符／字典有未用到的來源）**全部 `SystemExit`**。與 overlay 的嚴格度落差是選層時最該知道的一件事：同樣叫「control token 不符」，overlay 是 `continue`、common 是 `SystemExit` |
| `mod-library/l10n/tools/project_adamant_translation.py` | 版本升級用的譯文投影器，**不翻譯也不產 plugin**：只在「精確 FormKey/type/field/occurrence 的來源文字仍逐位元相同」或「新來源在舊審過列中有唯一對應」時才沿用，其餘標 NEEDS REVIEW 並 exit 1。設計意圖是擋住「用舊漢化 plugin 蓋掉上游 gameplay 修正」 |
| `mod-library/l10n/tools/build_audugan_100_cht_layer.py` | `enairim_cht_common` 消費者。archive／ESP／BSA 三個 SHA-256 全部釘死，字典直譯 9 組 (record, tag) 共 412 欄位，BSA 不覆蓋 |
| `mod-library/l10n/tools/build_valravn_220_cht_layer.py` | `enairim_cht_common` 消費者，比 Audugan 多一層：直接改寫一個 QUST 的 **VMAD 字串屬性**，gate 端要求非目標 VMAD payload 完全相同、record 數 388、BSA 逐位元相同 |
| `mod-library/l10n/tools/build_ai_overhaul_195_cht_layer.py` | 官方與 CHS 兩個 archive 三重釘死，非 plugin 成員必須逐位元相同。**前代官方繁中 NPC 名只在 record identity 與英文來源都仍相同時才沿用**，其餘顯式標成 `MACHINE_CONVERTED_UNREVIEWED` 並出高風險複審 ledger。輸出打包後重打一次比對是否位元相同 |
| `mod-library/l10n/tools/build_dmk_cht_layer.py` | 非 ESP：對 `Language.json` 做 key 順序與葉節點型別全等檢查（必須恰好 66 個字串葉），OpenCC 後套 token 還原表與人工審閱覆寫表；覆寫的 key 不在官方來源即 `SystemExit`。gate 是 `human_reviewed_zh_tw`，**不會**在資料缺失時預設通過 |
| `mod-library/l10n/tools/build_vokriinator_black_6153_vmad_fix.py` | **不是漢化**：修一筆 MGEF 綁到 `MP_ILL__InfluenceFear`（相依集提供的是 `IMP_ILL__InfluenceFear`）。只改那一個 VMAD 長度前綴字串，要求 record 數 824、改動 record 與 payload 各恰為 1。**單一版本專用（6.15.3）**；另有 latent bug：`MANIFEST.sha256` 把從不產生的 `README.md` 列入計算 |
| `mod-library/l10n/tools/build_party_sheet_31_cht_layer.py` | 非 ESP：INI 翻譯表與兩個 tweenoptions JSON，閘門是 section／key 拓撲一致與 `printf` placeholder 不漂移。**全機器轉換未審閱**。**一次性／歷史**：無 argparse，來源 archive 與輸出根目錄全硬寫，且來源 archive 已不在該路徑 |
| `mod-library/l10n/tools/build_new_content_cht_layers.py` | **一次性／歷史**：2026-08-21 那批（AYOP 九模組、Biggie Traits、Additional Traits、WICTS、SkyParkour）的批次腳本，所有 archive 路徑硬寫 |
| `mod-library/l10n/tools/build_biggie_traits_cht_completion.py` | **一次性／歷史**：從 MO2 已安裝目錄（非 archive）讀 ESP 補齊 61 個仍為英文的欄位。只新建兩個 disabled 的 mod 資料夾，不改 profile 也不改既有 mod 目錄；輸出已存在就拒跑 |
| `mod-library/l10n/tools/audit_layer_priority.py` | 稽核每個漢化層有沒有真的贏過它覆蓋的檔案。**2026-08-26 修掉一個恆真路徑**：原本 `errors="replace"` 讀 modlist（在判斷成敗的路徑上），編碼故障→U+FFFD→查無目錄→`WARN … continue`→`PASS`。現在嚴格解碼，exit 2＝稽核跑不起來、exit 1＝真的有層在輸，兩者分開 |
| `mod-library/l10n/tools/match_translations.py` | 譯文與來源的比對配對 |
| `agentctl/tools/runtime_log_window.py` | 單次 smoke 的 CrashLogger／Papyrus 視窗：`start` 存指紋，`finish` 只認 marker 之後寫入的 Papyrus、以及**名稱相同但 hash 變了也算新**的 crash log。三段式 exit：新 crash log = 2（優先於一切），沒有新鮮 Papyrus 或有可疑行 = 1，乾淨 = 0。從不編輯或輪替遊戲 log |
| `agentctl/tools/skse_log_window.py` | 單一 SKSE plugin log 的「這次真的有寫」證明：要求 mtime 晚於 marker **且** hash 或 mtime 與 before 不同才算 fresh，再逐條比對 `--expect` 的 regex |
| `agentctl/tools/test_runtime_log_window.py` | 驗 runtime 視窗的判定邊界：不得把歷史 log 當新的、可疑行需複審、新 crash 優先於乾淨 Papyrus、同名但內容變更算新、log 輪替時只看新的那個 |
| `agentctl/tools/test_skse_log_window.py` | 驗 fresh 與 expect 兩個條件各自失效：未變動的歷史 log 不算 fresh，新鮮但缺預期行仍 fail |
| `agentctl/tools/check_enairim_offline_gates.py` | Batch 1-6 離線 gate 證據的 fail-closed 匯總器：逐 batch 驗 header／每條 check 值／artifact 數下限，並對每個 artifact 驗 sha256 格式、實體存在、byte 數與 hash 相符，且**路徑不得逃出證據目錄**。三態 exit：PASS=0、FAIL=1、**缺檔的 HOLD=2**（刻意與 FAIL 分開） |
| `agentctl/tools/test_enairim_offline_gates.py` | 驗上面那支的四個失效面，含「缺 batch 檔要是 HOLD 而不是 FAIL」與 artifact 路徑逃逸 |
| `agentctl/tools/mechanical_runtime_capture.py` | 機械式 WAIT_USER 驗收的證據採集：**不啟動遊戲、不送任何會改變狀態的指令**，只讀 agent-bridge 的結構化端點或對存檔目錄做指紋。預期 FormID 寫死在腳本裡當比對基準 |
| `agentctl/tools/check_dll_runtime.py` | `runtime_ok_1_6_1170` 的唯一產生者，也是 L3 分級依據，**刻意偏向保留**：只有在 archive 確實含 loader-scoped SKSE plugin 且沒有任何一個能載入時才判不相容。手工走 PE export table 讀 `SKSEPlugin_Version`，**從不載入或執行 DLL**；靜態讀不到的舊式 plugin 回 `unknown` 而非不相容。**目前壞的**：`from scan_mod_library import connect`，但那支在 `mod-library/db/`，同目錄沒有，import 即失敗 |
| `agentctl/tools/check_links.py` | `candidates.source_url` 的存活檢查：先 HEAD，特定情況回退 GET。**永遠 exit 0**，全掛也不會讓呼叫端失敗——拿它當 gate 就是恆真檢查。需要 Mongo，會連外網 |
| `agentctl/tools/build_gallery.py` | 把 `candidates` 連同截圖渲染成單一本機 HTML 走查頁。輸出寫進 `agentctl/docs/`，但截圖路徑是相對於 mod library 根目錄算的——兩者不同 repo，連結能不能開取決於本機佈局 |
| `agentctl/tools/triage_crash.py` | crash log 分流 |
| `agentctl/tools/agent_inbox/inbox_send.sh` | Codex 工作線以固定 frontmatter／STATUS 契約原子發布完成、阻塞或進度訊息到執行期 inbox |
| `agentctl/tools/agent_inbox/inbox_read.sh` | 無副作用、空 inbox 完全靜默的未讀訊息摘要，供調度者與 `UserPromptSubmit` hook 使用 |
| `agentctl/tools/agent_inbox/notify_watch.sh` | 每 20 秒靜默輪詢新訊息與受監看 tmux session，對新信、消失 session 及兩輪確認的孤兒狀態各通知一次 |
