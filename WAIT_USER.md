# WAIT_USER — 等待使用者的事

只列需要使用者親自做/驗證才能繼續的 open 項。完成即移除，不留完成清單。

常見類型：

- 實機或 UI 手動驗證
- 外部帳號、權限、下載、授權
- 本機環境變數或工具安裝
- 不能由 agent 代跑的指令
- 高風險操作的確認

## Open

- **RDO Final 正體中文需 Dev-only runtime 驗收**（2026-08-16）：已在
  [`dist/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/`](dist/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/README.md)
  建立並部署獨立最高優先級 layer，只覆寫同名 ESP 與六個 follower 通知 PEX；Play profile 未變。
  離線 gate 證明 9,766-record topology／全部非文字 payload 相同，4,071 個 ESP zstrings 與六個 PEX
  display slots 改為正體；PEX declaration／properties／bytecode tails 逐 byte 相同。另修正 seed 唯一
  `<BribeCost>` → 官方 `<bribecost>` token-case 漂移。load order／FormLink／抽樣 PEX winner 通過；
  script-binding gate 只重報官方 RDO 既有 VMAD findings。請抽查一般關係對話、選項／字幕、任務／
  通知、賄賂金額替換，以及 Gelebor／Isran／Valerica 的等待／離隊通知，確認沒有方框、mojibake、
  空白、未替換 token、截斷或新 crash。未通過前不部署到 Play profile。

- **Recorder Follower 3.0 正體中文需真人對話抽查**（2026-08-20）：已在
  [`dist/mods/Recorder-Follower-Traditional-Chinese-3.0/`](dist/mods/Recorder-Follower-Traditional-Chinese-3.0/README.md)
  從官方 3.0 baseline 與同版 CHT seed 重建獨立同名 ESP 覆寫，並只部署到 `Modpack-KR-Dev`；
  Play profile 未變。離線 gate 證明 1,380-record topology／全部非文字 payload 相同，只有 1,429 個
  玩家可見 zstring 改為正體；scoped houseCARL after-gate 全 PASS。固定 baseline runtime smoke
  3/3 PASS，精確 ESS／SKSE pair 與 state fingerprint 匹配、load epoch `0 → 1`，遊戲確實載入
  `Recorder Follower Base.esp`，且已完成 teardown。請日後抽查 Recorder 的招募／一般對話、字幕、
  任務日誌、書籍與通知，確認沒有方框、mojibake、空白、截斷或新 crash；英語配音本來就保留。

- **Sofia Follower 2.51 正體中文 v2 需真人對話／MCM 抽查**（2026-08-20）：已在
  [`dist/mods/Sofia-Follower-Traditional-Chinese-2.51-v2/`](dist/mods/Sofia-Follower-Traditional-Chinese-2.51-v2/README.md)
  從官方 2.51 baseline 與 Nexus 183562 的 Traditional Chinese Localization Patch v2 重建獨立
  ESP＋8 PEX 覆寫，並只部署到 `Modpack-KR-Dev`；Play profile 未變。離線 gate 證明 1,742-record
  topology 與全部非文字 payload 相同，只有 1,665 個 ESP 顯示文字欄位及 105 個既有 PEX
  string-table slots 改為正體；所有 PEX declaration／properties／control-flow／bytecode tails 逐 byte
  相同。固定 baseline runtime smoke 3/3 PASS，精確 ESS／SKSE pair 與 state fingerprint 匹配、
  `load_epoch 0 → 1`，遊戲確實載入 `SofiaFollower.esp`，且已完成 teardown。請日後抽查 Sofia 的
  招募／一般對話、字幕、任務日誌、MCM、關係狀態與左上角通知，確認沒有方框、mojibake、空白、
  截斷或新 crash；英語配音本來就保留。

- **VIGILANT 1.8.1 正體中文需真人主線／顯示抽查**（2026-08-20）：已取得 Nexus 158886
  保留的 exact-version `VIGILANT SE (CHT)` 1.8.1，並只部署到 `Modpack-KR-Dev` 的最高優先級；
  Play profile 未變。官方英文與翻譯 ESM 都有 129,107 records，record identity／header／GRUP／
  subrecord topology 完全一致；7,250 個差異全部落在可本地化文字 payload，非文字差異為零。
  以現役英文 ESM 作 before baseline 的 houseCARL after-gate 4/4 PASS；固定 baseline runtime smoke
  3/3 PASS，精確 ESS／SKSE pair 與 state fingerprint 匹配、`load_epoch 0 → 1`，遊戲確實載入
  `Vigilant.esm`，且已完成 teardown。請日後在晨星城風岳旅店找 Altano，抽查任務開場、對話／字幕、
  日誌／目標、書籍、物品／效果與 MCM，確認沒有方框、mojibake、空白、截斷或新 crash。後續稽核
  發現官方 1.8.1 與 1.8.2 正體包都原樣留下同一批 45 個召喚書／石之碎片 `BOOK.DESC` 英文行；已另
  建私人最高優先級 text-only layer，沿用同一筆 `BOOK.FULL` 的既有正體專名補齊，45-record gate 與
  houseCARL before/after 4/4 PASS；修正後固定 baseline runtime 亦 3/3 PASS。抽查時請至少打開一件
  「石之碎片」確認描述行也是正體。現有英／
  日語配音保留是預期行為；作者檔與私人修正都不納入公開 `dist/` 成品或對外重發。

- **2026-08-20 新任務內容批只剩 Dev-only UI／真人內容抽查**：UNSLAAD 3.0.6b、Missives
  2.03、DAc0da 1.1.0b 與 GLENMORIL 0.96.80b 的本體、英譯、正體、適用擴充及現成語音已只部署到
  `Modpack-KR-Dev`；`Play-KR` 未變。2026-08-20 的短自動 runtime smoke 7/7 PASS：受信任 baseline
  配對與新 load epoch 通過，且引擎實際載入 `Unslaad.esm`、`Missives.esp`、`DAc0da.esm`、
  `Glenmoril.esm`；本時窗沒有新 crash，teardown 已關閉 Skyrim／MO2、停用 AgentBridge 並切回
  `Play-KR`。後續只需拆批抽查 MCM／任務入口、正體日誌／對話／字幕、實際語音與跨 worldspace；
  尚未真人走過的任務流程不可稱 gameplay PASS。GLENMORIL 現有有效語音覆蓋為
  3,653／4,792（76.23%），UNSLAAD 現成英語語音只涵蓋 Act 1；剩餘內容使用 Silent Voice 是已接受
  的預期狀態，**不需要生成 TTS，也不應因缺語音判定失敗**。安裝矩陣與回滾 commits 見 notes
  `projects/modding/skyrim/logs/quest-content-batch-2026-08-20.md`。

- **Simonrim Batch 4E 只剩真人附魔功能／手感抽樣**（2026-08-16）：Thaumaturgy 1.5、精確同版繁中、
  Execute XP VMAD fix 與 184-record AVE／Constellations 最終 merge 已完成 Dev-only 靜態與 runtime
  smoke。固定 baseline QA 6/6；本體、fix、AVE、Constellations、merge 都由引擎載入，代表物繁中無
  方框／mojibake，AVE 護手第三人稱模型正常，本次啟動時間窗沒有新 crash。使用者日後只需正常遊玩
  抽樣：附魔分解→學習→製作→裝備／重載／充能、Empowered Strike 的 power-attack proc、slot
  restriction，以及 loot/vendor 中 vanilla／AVE enchanted items 的階級與比例是否自然。完整證據在
  notes 側 `logs/simonrim-batch4-4e-2026-08-16/RESULT.md`；回滾方式也在同一份報告。

- **Simonrim Batch 4A 只剩真人鍊金／經濟／戰鬥手感抽樣**（2026-08-16）：Apothecary 1.3.9、
  Fishing 1.4.1、Saints and Seducers 1.4.0、Rare Curios 1.4.0、四個精確版本繁中層與獨立
  Become Ethereal VMAD fix 已完成 Dev-only 靜態與 runtime 驗證。固定 baseline QA 7/7、SPID
  `19/19`；`隱秘藥劑` 的繁中名稱／說明、15 秒開始／結束效果及修補後 Papyrus 增量都已由 agent
  驗證，代表性本體與三個 CC 物品也無方框／mojibake／新 crash，不需重跑這些。使用者日後遊玩時
  只需以正常流程抽樣：鍊金台混合 vanilla／Fishing／Saints／Rare Curios 原料、在戰鬥中正常塗抹
  一種毒劑、觀察 vendor 庫存／價格與 early-game 供應，以及較長 session 的平衡與存讀檔手感。
  完整證據在 notes 側 `logs/simonrim-batch4-4a-2026-08-16/RESULT.md`；不阻塞獨立 Batch 4E。

- **Simonrim Batch 4M/P 只剩真人功能／手感抽樣**（2026-08-16）：Mysticism 2.5.0、Adamant 6.0.2、
  精確版本繁中、Adamant Scrambled Bugs 設定與 `MAG_BastionControllerPerkNPC` SPID 單行修正已完成
  Dev-only 安裝；load order／VFS／baseline runtime 4/4、SPID `16/16`、恢復系天賦樹與 2.5 新法術
  「強效火焰弱化」的繁中靜態畫面都已由 agent 驗證，無方框／mojibake／新 crash，不需重跑這些。
  使用者日後遊玩時只需抽樣：正常向 vendor 買書→讀書→施放 novice／apprentice 法術、點代表性
  Adamant 天賦並感受效果，以及 BFCO 輕／重／方向／sprint attack 搭配武器天賦是否自然；長期平衡
  與存讀檔手感也屬真人範圍。完整證據在 notes 側
  `logs/simonrim-batch4-4mp-2026-08-16/RESULT.md`。不阻塞接續 Batch 4A；回滾只需停用該報告列出的
  五個 Dev layer。

- **Expanded Skyrim Weaponry Batch 3A 只剩真人動態驗收**（2026-08-15）：agent 已完成中文名稱、
  inventory preview、第一／第三人稱、地面模型、鍛造配方與 runtime leveled-list distribution 驗證；
  三件代表武器無方框／mojibake／紫模／缺 mesh，`LItemWeaponBattleAxe` 100 次解析也精確產生
  21 鐵製戰戟、23 鐵製雙鋒巨斧與 56 原版戰斧。使用者回家後只需以真人遊玩或錄影確認鐵製戰戟
  與鋼製雙刃巨劍的拔收、BFCO 普攻及動作銜接正常；單張截圖不能替代時間軸結論。完成後移除此條。
  回滾只需停用 merge patch、CHT 與 NPC 原包，原始 USSEP／ESW 檔均未被改寫。

- **精確換成無心 3.1.0 仍需使用者日後提供原包**（2026-08-15 更新）：目前已用官方 Nexus
  JH People `1.1.3` + NPC Plugin Chooser 2 做成可在 1.6.1170 運作的 Dev-only 536 NPC 外觀 patch，
  並完成靜態與遊戲內黑臉檢查；這已滿足本輪「經典韓系 NPC 美化」，不阻塞整合包。但它不是
  夜貓－無心 3.1.0 的完整 1138 NPC「人物美化＋頭模替換」，不能冒充相同內容。

  若日後仍要**精確換成無心 3.1.0**，請從作者頁所列百度網盤只下載名稱含「人物美化」與
  「頭模替換」的 archive，不需下載遊戲本體、環境或功能包；放進既有
  `/home/lorkhan/skyrim_mods/` 後通知 agent。到時以新獨立批次驗證來源、轉換 LE 資產／plugin，
  重建 NPC coverage 與 winner patch，再取代目前 JH output；未取得完整資產許可不得公開重打包。
  原相容性調查見
  [wuxin-character-overhaul-se-ae-compatibility.md](workflows/investigation/findings/wuxin-character-overhaul-se-ae-compatibility.md)。

- **scene-capture-bridge 離線 catalog Browser 實機驗收**（2026-08-12 開條，**2026-08-13 家用機大幅修正**，**2026-08-20 阻礙已解除**）：

  **✅ 2026-08-20：那顆 commit 已經推上去了，這條可以開始做。** 公司機（`guanyu.lu`）持有的三顆
  未發布 submodule commit 已全部 fast-forward 到各自 GitHub `main`：`scene-capture-bridge`
  `298566a → 1e44326`、`my_skyrim_plugin_1` `e257642 → ea6bfeb`、`sofia-patch`
  `c1c6f80 → fc25fc1`。母 repo 的遞迴 fetch 不再報 `upload-pack: not our ref`，`git submodule
  status` 三者皆已對齊 remote。**家用機 `git pull` ＋ `git submodule update --init` 之後就拿得到
  DLL 消費端程式碼**，可直接接上下面的實機驗收。（⚠️ `houseCARL` 仍需另外處理——它釘在
  SSH remote `git@github.com:justty32/houseCARL.git` 的自有 fork，公司機沒有 SSH 金鑰，
  與本條無關。）

  原本卡住的是：DLL 消費端程式碼在母 repo gitlink 指的 `1e44326`，那顆不在家用機也不在
  GitHub，還躺在公司機；家用機 HEAD `298566a` 的 `Catalog.cpp` 只有 **runtime-only** 版，
  沒有 json 讀檔/merge/provenance/global-source-order gate。**toolchain 從來不是問題**——家用機
  2026-08-13 實測整條 build path 是活的（`rm -rf build/release-clang-cl-linux` →
  `cmake --preset build-release-clang-cl-linux` → build 29/29 通過；import 表只有
  KERNEL32/ole32/VERSION/USER32/SHELL32，靜態 CRT 乾淨；`scripts/deploy.sh` 已部署，
  crc32 `7e94ad30`）。

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
