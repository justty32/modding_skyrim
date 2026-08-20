# WAIT_USER — 等待使用者的事

只列需要使用者親自做/驗證才能繼續的 open 項。完成即移除，不留完成清單。

> 2026-08-20 起，MO2 只保留 `Modpack-KR`，遊玩、開發與驗收狀態改由 profile Git repo 分支管理。
> 下文保留的 `Play-KR`／`Modpack-KR-Dev`／`QA` 舊名稱只描述當時的部署或驗證環境，不代表現在
> 仍有這些 profile 可以切換。

常見類型：

- 實機或 UI 手動驗證
- 外部帳號、權限、下載、授權
- 本機環境變數或工具安裝
- 不能由 agent 代跑的指令
- 高風險操作的確認

## Open

- **RDO Final 正體中文仍需真人 runtime 驗收**（2026-08-16）：已在
  [`dist/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/`](dist/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/README.md)
  建立並部署獨立最高優先級 layer，只覆寫同名 ESP 與六個 follower 通知 PEX；部署時期只套用於
  當時的 Dev profile，未納入當時的一般遊玩環境（兩者已於 2026-08-20 併入唯一 `Modpack-KR`）。
  離線 gate 證明 9,766-record topology／全部非文字 payload 相同，4,071 個 ESP zstrings 與六個 PEX
  display slots 改為正體；PEX declaration／properties／bytecode tails 逐 byte 相同。另修正 seed 唯一
  `<BribeCost>` → 官方 `<bribecost>` token-case 漂移。load order／FormLink／抽樣 PEX winner 通過；
  script-binding gate 只重報官方 RDO 既有 VMAD findings。請抽查一般關係對話、選項／字幕、任務／
  通知、賄賂金額替換，以及 Gelebor／Isran／Valerica 的等待／離隊通知，確認沒有方框、mojibake、
  空白、未替換 token、截斷或新 crash。部署當時的門檻是未通過前不進入一般遊玩環境；profile
  合併不改變此項仍待驗的結論。

- **Recorder Follower 3.0 正體中文需真人對話抽查**（2026-08-20）：已在
  [`dist/mods/Recorder-Follower-Traditional-Chinese-3.0/`](dist/mods/Recorder-Follower-Traditional-Chinese-3.0/README.md)
  從官方 3.0 baseline 與同版 CHT seed 重建獨立同名 ESP 覆寫；部署時期只套用於當時的 Dev
  profile，未納入當時的一般遊玩環境（兩者已於 2026-08-20 併入唯一 `Modpack-KR`）。離線 gate
  證明 1,380-record topology／全部非文字 payload 相同，只有 1,429 個
  玩家可見 zstring 改為正體；scoped houseCARL after-gate 全 PASS。固定 baseline runtime smoke
  3/3 PASS，精確 ESS／SKSE pair 與 state fingerprint 匹配、load epoch `0 → 1`，遊戲確實載入
  `Recorder Follower Base.esp`，且已完成 teardown。請日後抽查 Recorder 的招募／一般對話、字幕、
  任務日誌、書籍與通知，確認沒有方框、mojibake、空白、截斷或新 crash；英語配音本來就保留。

- **Sofia Follower 2.51 正體中文 v2 需真人對話／MCM 抽查**（2026-08-20）：已在
  [`dist/mods/Sofia-Follower-Traditional-Chinese-2.51-v2/`](dist/mods/Sofia-Follower-Traditional-Chinese-2.51-v2/README.md)
  從官方 2.51 baseline 與 Nexus 183562 的 Traditional Chinese Localization Patch v2 重建獨立
  ESP＋8 PEX 覆寫；部署時期只套用於當時的 Dev profile，未納入當時的一般遊玩環境（兩者已於
  2026-08-20 併入唯一 `Modpack-KR`）。離線 gate 證明 1,742-record
  topology 與全部非文字 payload 相同，只有 1,665 個 ESP 顯示文字欄位及 105 個既有 PEX
  string-table slots 改為正體；所有 PEX declaration／properties／control-flow／bytecode tails 逐 byte
  相同。固定 baseline runtime smoke 3/3 PASS，精確 ESS／SKSE pair 與 state fingerprint 匹配、
  `load_epoch 0 → 1`，遊戲確實載入 `SofiaFollower.esp`，且已完成 teardown。請日後抽查 Sofia 的
  招募／一般對話、字幕、任務日誌、MCM、關係狀態與左上角通知，確認沒有方框、mojibake、空白、
  截斷或新 crash；英語配音本來就保留。

- **VIGILANT 1.8.1 正體中文需真人主線／顯示抽查**（2026-08-20）：已取得 Nexus 158886
  保留的 exact-version `VIGILANT SE (CHT)` 1.8.1；部署時期只套用於當時 Dev profile 的最高
  優先級，未納入當時的一般遊玩環境（兩者已於 2026-08-20 併入唯一 `Modpack-KR`）。官方英文與
  翻譯 ESM 都有 129,107 records，record identity／header／GRUP／
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
  截至 **2026-08-21 01:16（Asia/Taipei）**，今晚新增的是可重建上述 45 筆私人修正的
  exact-version 產生器；1.8.2 來源準備尚未取代現役 1.8.1 layer，因此本項 1.8.1 真人抽查仍成立。

- **Scene Capture Browser：請決定未 commit ghost 的第三人稱攝影機語意**（2026-08-21）：
  placement drift 的 Armor、Editor commit 與 save/load 修正已由 AgentBridge 座標序列及
  `load_epoch 1 → 2` 通過，不需重做；剩下的是已確認的 camera/player-facing ray 語意選擇，並非
  尚未診斷的漂移。請選一項：**commit 後清 ghost**（最簡單，但會破壞連續放置）、**暫停／恢復
  follow**（保留預覽但增加狀態操作），或 **改用 rendered-camera ray**（體驗最佳、改動與相容性
  驗證最大）。選定前 `feat/placement-drift` 的 ghost 分支維持原狀；完整證據與取捨見 notes
  `projects/modding/skyrim/logs/scene-capture-placement-drift-2026-08-20.md`。

- **2026-08-20 新任務內容批只剩 UI／真人內容抽查**：UNSLAAD 3.0.6b、Missives
  2.03、DAc0da 1.1.0b 與 GLENMORIL 0.96.80b 的本體、英譯、正體、適用擴充及現成語音，在部署
  時期只套用於當時的 Dev profile，未納入當時的一般遊玩環境；兩者已於 2026-08-20 併入唯一
  `Modpack-KR`。2026-08-20 的短自動 runtime smoke 7/7 PASS：受信任 baseline
  配對與新 load epoch 通過，且引擎實際載入 `Unslaad.esm`、`Missives.esp`、`DAc0da.esm`、
  `Glenmoril.esm`；本時窗沒有新 crash，teardown 已關閉 Skyrim／MO2、停用 AgentBridge 並切回
  當時的 `Play-KR` 歷史 profile（該名稱現已不存在）。後續只需拆批抽查 MCM／任務入口、正體
  日誌／對話／字幕、實際語音與跨 worldspace；
  尚未真人走過的任務流程不可稱 gameplay PASS。GLENMORIL 現有有效語音覆蓋為
  3,653／4,792（76.23%），UNSLAAD 現成英語語音只涵蓋 Act 1；剩餘內容使用 Silent Voice 是已接受
  的預期狀態，**不需要生成 TTS，也不應因缺語音判定失敗**。安裝矩陣與回滾 commits 見 notes
  `projects/modding/skyrim/logs/quest-content-batch-2026-08-20.md`。
  截至 **2026-08-21 00:57（Asia/Taipei）**，後續 Batch 6 final automatic lane 另以 101-plugin
  當時快照完成 21 PASS、0 FAIL、3 handoff；它只補強 load／cell／save-reload 證據，不取代本項
  真人任務、語音、UI 與 worldspace 流程抽查。詳見 notes
  `projects/modding/skyrim/logs/modpack-kr-final-smoke-2026-08-21/RESULT.md`。

- **Simonrim Batch 4E 只剩真人附魔功能／手感抽樣**（2026-08-16）：Thaumaturgy 1.5、精確同版繁中、
  Execute XP VMAD fix 與 184-record AVE／Constellations 最終 merge 已在當時的 Dev profile 完成
  靜態與 runtime smoke（該環境已於 2026-08-20 併入唯一 `Modpack-KR`）。固定 baseline QA 6/6；
  本體、fix、AVE、Constellations、merge 都由引擎載入，代表物繁中無
  方框／mojibake，AVE 護手第三人稱模型正常，本次啟動時間窗沒有新 crash。使用者日後只需正常遊玩
  抽樣：附魔分解→學習→製作→裝備／重載／充能、Empowered Strike 的 power-attack proc、slot
  restriction，以及 loot/vendor 中 vanilla／AVE enchanted items 的階級與比例是否自然。完整證據在
  notes 側 `logs/simonrim-batch4-4e-2026-08-16/RESULT.md`；回滾方式也在同一份報告。

- **Simonrim Batch 4A 只剩真人鍊金／經濟／戰鬥手感抽樣**（2026-08-16）：Apothecary 1.3.9、
  Fishing 1.4.1、Saints and Seducers 1.4.0、Rare Curios 1.4.0、四個精確版本繁中層與獨立
  Become Ethereal VMAD fix 已在當時的 Dev profile 完成靜態與 runtime 驗證（該環境已於
  2026-08-20 併入唯一 `Modpack-KR`）。固定 baseline QA 7/7、SPID
  `19/19`；`隱秘藥劑` 的繁中名稱／說明、15 秒開始／結束效果及修補後 Papyrus 增量都已由 agent
  驗證，代表性本體與三個 CC 物品也無方框／mojibake／新 crash，不需重跑這些。使用者日後遊玩時
  只需以正常流程抽樣：鍊金台混合 vanilla／Fishing／Saints／Rare Curios 原料、在戰鬥中正常塗抹
  一種毒劑、觀察 vendor 庫存／價格與 early-game 供應，以及較長 session 的平衡與存讀檔手感。
  完整證據在 notes 側 `logs/simonrim-batch4-4a-2026-08-16/RESULT.md`；不阻塞獨立 Batch 4E。

- **Simonrim Batch 4M/P 只剩真人功能／手感抽樣**（更新 2026-08-20）：Mysticism 2.5.0、Adamant
  6.0.4、精確版本繁中、Adamant Scrambled Bugs 設定與 `MAG_BastionControllerPerkNPC` SPID 單行
  修正於部署時期只安裝在當時的 Dev profile（該環境已於 2026-08-20 併入唯一 `Modpack-KR`）。
  6.0.4 的 load order／VFS／靜態完整性與實機存讀檔皆通過；引擎實際
  載入 `Adamant.esp`，使用者確認技能樹名稱與說明繁中正常，第二次載入後無新 crash 或 Adamant
  錯誤。恢復系天賦樹與 Mysticism 2.5 新法術「強效火焰弱化」的既有驗證也不需重跑。
  使用者日後遊玩時只需抽樣：正常向 vendor 買書→讀書→施放 novice／apprentice 法術、點代表性
  Adamant 天賦並感受效果，以及 BFCO 輕／重／方向／sprint attack 搭配武器天賦是否自然；長期平衡
  與存讀檔手感也屬真人範圍。完整證據在 notes 側
  `logs/simonrim-batch4-4mp-2026-08-16/RESULT.md`。不阻塞接續 Batch 4A；回滾只需停用該報告列出的
  五個部署 layer（部署當時稱為 Dev layer，現由唯一 profile 的 Git 分支狀態管理）。

- **Expanded Skyrim Weaponry Batch 3A 只剩真人動態驗收**（2026-08-15）：agent 已完成中文名稱、
  inventory preview、第一／第三人稱、地面模型、鍛造配方與 runtime leveled-list distribution 驗證；
  三件代表武器無方框／mojibake／紫模／缺 mesh，`LItemWeaponBattleAxe` 100 次解析也精確產生
  21 鐵製戰戟、23 鐵製雙鋒巨斧與 56 原版戰斧。使用者回家後只需以真人遊玩或錄影確認鐵製戰戟
  與鋼製雙刃巨劍的拔收、BFCO 普攻及動作銜接正常；單張截圖不能替代時間軸結論。完成後移除此條。
  回滾只需停用 merge patch、CHT 與 NPC 原包，原始 USSEP／ESW 檔均未被改寫。

- **精確換成無心 3.1.0 仍需使用者日後提供原包**（2026-08-15 更新）：目前已用官方 Nexus
  JH People `1.1.3` + NPC Plugin Chooser 2 在當時的 Dev profile 做成可於 1.6.1170 運作的 536 NPC
  外觀 patch（該環境已於 2026-08-20 併入唯一 `Modpack-KR`），並完成靜態與遊戲內黑臉檢查；這已
  滿足本輪「經典韓系 NPC 美化」，不阻塞整合包。但它不是
  夜貓－無心 3.1.0 的完整 1138 NPC「人物美化＋頭模替換」，不能冒充相同內容。

  若日後仍要**精確換成無心 3.1.0**，請從作者頁所列百度網盤只下載名稱含「人物美化」與
  「頭模替換」的 archive，不需下載遊戲本體、環境或功能包；放進既有
  `/home/lorkhan/skyrim_mods/` 後通知 agent。到時以新獨立批次驗證來源、轉換 LE 資產／plugin，
  重建 NPC coverage 與 winner patch，再取代目前 JH output；未取得完整資產許可不得公開重打包。
  原相容性調查見
  [wuxin-character-overhaul-se-ae-compatibility.md](workflows/investigation/findings/wuxin-character-overhaul-se-ae-compatibility.md)。

- **BG3 場景佈局實檔驗證**（2026-08-11）：桌面研究已確認 LSLib 可把 BG3
  `Levels/` 下的 `.lsf` 轉成可讀 `.lsx`，但尚未用使用者持有的遊戲資料驗證 placement
  欄位能否無損對映 ModForge `placements`（位置、旋轉、尺度、base/resource identity）。下次
  有 BG3 安裝或合法抽取素材時，挑一個小型 level 做 `.lsf` → `.lsx`，記錄欄位與一組實例，
  再決定是否開 converter/spec 工作；沒有實檔前不宣稱 port pipeline 可行。評估框架與候選
  比較見 [port-source-survey](analysis/port-source-survey/README.md)。

- **darksouls-port ghost-tol 0.02 門洞仍需真人實走**（更新至 **2026-08-21 01:16，
  Asia/Taipei**）：舊版「參數未套用／venv 未齊／待全量重跑」已被今晚工作取代。專用環境與
  `--ghost-tol 0.02` 已完成 47 件碰撞全量重建；21,226 hulls 經既有 MSB/orphan 過濾後輸出
  389 個載體 NIF，638-file ZIP 的 SHA-256 是
  `8166b7c80018d9443676d942d0dfc2361a6eab69c9d866a4491521c91e22f97c`，離線 15/15 tests、archive
  test 與 ModForge validate/dump 均通過。

  01:00 後曾把新版安裝為 `DSPortP1` runtime candidate；resolver 為 102/102、0 missing。但給足
  600 秒仍未啟動 Skyrim，沒有 load epoch、before/after position 或實體 `W` 輸入，所以這次結果是
  **inconclusive，不是門洞 FAIL，也不是 PASS**。teardown 已停用 `DSPortP1` 與 AgentBridge，
  MO2 payload 保留，下一次**不需重建或重下載**。請在可實際進遊戲的時窗啟用候選並走過原先會卡的
  門洞一次；若 0.02 仍卡，下一個調查方向才是門框側壁 thickness／`--planar-thresh` 0.15，
  不再下降 `--ghost-tol`。完整時序與證據見
  [P1-INGAME-FINDINGS.md](projects/darksouls-port/p1/P1-INGAME-FINDINGS.md)。
