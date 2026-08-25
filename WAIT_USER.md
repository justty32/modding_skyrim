# WAIT_USER — 等待使用者的事

只列需要使用者親自做/驗證才能繼續的 open 項。完成即移除，不留完成清單。

> 2026-08-20 起，MO2 只保留一個 profile（2026-08-23 更名為 `modpack-main`），遊玩、開發與驗收
> 狀態改由 profile Git repo 分支管理。
> 下文保留的 `Play-KR`／`Modpack-KR-Dev`／`QA` 舊名稱只描述當時的部署或驗證環境，不代表現在
> 仍有這些 profile 可以切換。

常見類型：

- 實機或 UI 手動驗證
- 外部帳號、權限、下載、授權
- 本機環境變數或工具安裝
- 不能由 agent 代跑的指令
- 高風險操作的確認

## Open

- **YouTube候選的 SOURCE-HOLD若要升級，需回到有 Nexus API key／houseCARL與 archives的環境**
  （2026-08-25）：35支有候選影片已完成 owner-level routing，公司端沒有可連線瀏覽器，Nexus HTML受
  Cloudflare阻擋，Windows／WSL也沒有可用 API key，因此未證 current metadata／archive的項目全部 fail
  closed成具體 HOLD。日後只在要升某一件時依[coverage](modpack-design/content-plan/youtube-candidate-final-coverage-audit-2026-08-25.md)
  的 reopen procedure一次查一件；未重提就不需要額外操作，也不得把 HOLD直接改成 GO。

- **三個 subproject 的完整離線測試需在可補依賴的環境重跑**（2026-08-24）：公司端依照「不下載、
  產物不能帶回家」限制只做既有環境驗證。`projects/scene-capture-bridge` 缺
  `x64-mingw-static` 的 nlohmann-json triplet；`projects/darksouls-port` 的 35 項測試中 29 項可跑、
  6 項因正式必要依賴 `scipy`／`shapely` 未安裝而 ERROR（不是可合理 skip 的 optional dependency）；
  `projects/model-converter` 缺 `pytest`。回到可建立 repo-local venv／補 vcpkg triplet 的環境後，依各
  repo README 重跑即可；本輪沒有連網安裝，也沒有改測試來掩蓋缺依賴。

- **DMK 1.5.0 人工校對版需在家中 Linux 重建、部署與 UI 驗收**（2026-08-24）：66 個字串已逐條
  審完（38 個人工覆寫、28 個確認沿用），builder／ledger 的靜態一致性 PASS；公司端沒有官方與 CHS
  archives／7z／OpenCC，且公司下載或產物不能帶回家，所以沒有假裝完成 archive replay。回家後用既有
  exact archives 執行 [`build_dmk_cht_layer.py`](mod-library/l10n/tools/build_dmk_cht_layer.py)，確認新
  offline gate 為 `human_reviewed_zh_tw`、66 reviewed、38 override、0 unresolved，再把新的單檔
  `Data/Viny Mods/DMK/Language.json` layer 部署到唯一 profile。最後肉眼抽查一般設定、相機、PC／手把
  按鍵與 OAR converter 警告，並做 DMK 移動 smoke；目前已部署的 `Machine-Private.7z` 仍是
  2026-08-21 未校對機翻包。完整邊界見
  [安裝結果](agentctl/logs/mcm-helper-dmk-cht-install-2026-08-21.md)。

- **EnaiRim Batch 0：回到家後逐件取得 5 個 Nexus archives**（2026-08-24）：使用者已完成最終選型，
  並要求公司網路一次只能查一件；本輪沒有開互動瀏覽器或下載。後續在有既有 Nexus 登入 session 的
  Linux 環境，依 [`nexus-intake`](wf/workflows/nexus-intake/README.md) 用 headful Chrome＋CDP **一次一檔**
  取得：① Mannaz 3.0.1 本體（mod 87219，MAIN file id **406689**——原本寫的 `372921` 是錯的，那是 `OLD_VERSION` 的 Mannaz 1.1.0）、② Mannaz CHS 3.0.1
  （mod 98760 main）、③ Freyr 1.2.0 本體（mod 88043 main）、④ Freyr CHS 1.2.0
  （mod 98756 main）、⑤ Audugan 1.0.0 本體（mod 169621 main）。Valravn 2.2.0 原包已在 catalog，
  不需重抓。每檔必須逐件核對原始檔名／API version／bytes／SHA-256／manifest 後入庫；不輸入憑證、
  不過 CAPTCHA、不改 Nexus 帳號狀態。五件的精確 `file_id`／檔名／bytes／VirusTotal hash 見
  [Batch 0 目標表](agentctl/logs/enairim-batch0-target-table-2026-08-24/README.md)（2026-08-24 查核）。
  完整現況與 rollback snapshot 見
  [Batch 0 preflight](agentctl/logs/simonrim-to-enairim-final-selection-2026-08-24/batch-0-preflight.md)。

- **EnaiRim Batch 7：完整終態的人眼 blocking 驗收**（等 Batch 1–6 實際施工後）：逐批自動／靜態 gate
  不能代替畫面與手感。Promotion 前需確認 Audugan／Valravn private CHT 與其他新文字層無方框、亂碼、
  截斷或錯誤術語；shrine／standing stone／High Hrothgar candidates 無穿插且可互動；Valravn 搭 BFCO／
  Precision／TDM／TK Dodge／WYT 的輸入、多人節奏、武器速度、耐力與命中手感可接受；並抽查代表性
  race／faith／spell／enchantment／shout UI。完整固定範圍與 non-blocking 長玩邊界見
  [Batch 7 計畫](agentctl/logs/simonrim-to-enairim-final-selection-2026-08-24/batch-7-integration-promotion-plan.md)。

- **Modpack-KR Batch 6 最終 gameplay 驗收**：自動 lane 已於 2026-08-21 以 21/21 PASS、
  `load_epoch 1 → 2`、0 new crash 收束，但不得冒充真人 gameplay PASS。仍需真人做真正新遊戲、
  城市/NPC 外觀巡查、BFCO 戰鬥與移動手感、Mysticism/Adamant、CT77/AVE 換裝、隨從招募與
  RDO/Recorder/Sofia 對話、Altano 的 VIGILANT 正常入口／字幕／語音，以及自然跨入新增 worldspace。
  VIGILANT 已於 2026-08-21 升到本體／英語語音／正體／book overlay 精確同版 1.8.2；同一輪真人
  驗收再抽看 MCM 是否無方框／亂碼、兩三本有 description overlay 的書，以及字幕與語音語意即可。
  Silent Voice 缺口是已接受狀態，不需生成 TTS。逐項判準、agent 已完成的邊界與畫面見
  [Batch 6 final smoke 結果](agentctl/logs/modpack-kr-final-smoke-2026-08-21/RESULT.md)。

- **四個中文層剛修好排序，第一次真的會顯示中文，需要抽查**（2026-08-23）：
  這四個層先前裝在本體**下方**而完全失效——檔案在、mod 也啟用著，但英文原版贏走每個衝突檔案。
  2026-08-23 已上移並晉升 main，所以**它們是第一次真的生效，從來沒有人看過顯示結果**。

  | mod | 看哪裡 |
  |---|---|
  | Timing is Everything SE 2.2 | MCM 的任務觸發設定頁 |
  | The Choice is Yours 2.7 | 任務起始的接受／拒絕對話選項 |
  | At Your Own Pace（8 個 ESP）| 主線／學院／盜賊公會等各線的推進選項 |
  | SkyParkour 3.6.2 | UI 字串（走 `Interface/Translations`，不是 ESP）|

  抽查重點是**方框、mojibake、截斷、空白**——靜態稽核只能證明勝出者對了，證明不了字有沒有正常畫出來。
  排序稽核隨時可重跑：`python3 mod-library/l10n/tools/audit_layer_priority.py`。

- **RDO Final 正體中文仍需真人 runtime 驗收**（2026-08-16）：已在
  [`mod-library/l10n/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/`](mod-library/l10n/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/README.md)
  建立並部署獨立最高優先級 layer，只覆寫同名 ESP 與六個 follower 通知 PEX；部署時期只套用於
  當時的 Dev profile，未納入當時的一般遊玩環境（兩者已於 2026-08-20 併入唯一 profile，2026-08-23 更名為 `modpack-main`）。
  離線 gate 證明 9,766-record topology／全部非文字 payload 相同，4,071 個 ESP zstrings 與六個 PEX
  display slots 改為正體；PEX declaration／properties／bytecode tails 逐 byte 相同。另修正 seed 唯一
  `<BribeCost>` → 官方 `<bribecost>` token-case 漂移。load order／FormLink／抽樣 PEX winner 通過；
  script-binding gate 只重報官方 RDO 既有 VMAD findings。請抽查一般關係對話、選項／字幕、任務／
  通知、賄賂金額替換，以及 Gelebor／Isran／Valerica 的等待／離隊通知，確認沒有方框、mojibake、
  空白、未替換 token、截斷或新 crash。部署當時的門檻是未通過前不進入一般遊玩環境；profile
  合併不改變此項仍待驗的結論。

- **Recorder Follower 3.0 正體中文需真人對話抽查**（2026-08-20）：已在
  [`mod-library/l10n/mods/Recorder-Follower-Traditional-Chinese-3.0/`](mod-library/l10n/mods/Recorder-Follower-Traditional-Chinese-3.0/README.md)
  從官方 3.0 baseline 與同版 CHT seed 重建獨立同名 ESP 覆寫；部署時期只套用於當時的 Dev
  profile，未納入當時的一般遊玩環境（兩者已於 2026-08-20 併入唯一 profile，2026-08-23 更名為 `modpack-main`）。離線 gate
  證明 1,380-record topology／全部非文字 payload 相同，只有 1,429 個
  玩家可見 zstring 改為正體；scoped houseCARL after-gate 全 PASS。固定 baseline runtime smoke
  3/3 PASS，精確 ESS／SKSE pair 與 state fingerprint 匹配、load epoch `0 → 1`，遊戲確實載入
  `Recorder Follower Base.esp`，且已完成 teardown。請日後抽查 Recorder 的招募／一般對話、字幕、
  任務日誌、書籍與通知，確認沒有方框、mojibake、空白、截斷或新 crash；英語配音本來就保留。

- **Sofia Follower 2.51 正體中文 v2 需真人對話／MCM 抽查**（2026-08-20）：已在
  [`mod-library/l10n/mods/Sofia-Follower-Traditional-Chinese-2.51-v2/`](mod-library/l10n/mods/Sofia-Follower-Traditional-Chinese-2.51-v2/README.md)
  從官方 2.51 baseline 與 Nexus 183562 的 Traditional Chinese Localization Patch v2 重建獨立
  ESP＋8 PEX 覆寫；部署時期只套用於當時的 Dev profile，未納入當時的一般遊玩環境（兩者已於
  2026-08-20 併入唯一 `Modpack-KR`）。離線 gate 證明 1,742-record
  topology 與全部非文字 payload 相同，只有 1,665 個 ESP 顯示文字欄位及 105 個既有 PEX
  string-table slots 改為正體；所有 PEX declaration／properties／control-flow／bytecode tails 逐 byte
  相同。固定 baseline runtime smoke 3/3 PASS，精確 ESS／SKSE pair 與 state fingerprint 匹配、
  `load_epoch 0 → 1`，遊戲確實載入 `SofiaFollower.esp`，且已完成 teardown。請日後抽查 Sofia 的
  招募／一般對話、字幕、任務日誌、MCM、關係狀態與左上角通知，確認沒有方框、mojibake、空白、
  截斷或新 crash；英語配音本來就保留。

- **VIGILANT 1.8.2 正體中文需真人主線／顯示抽查**（2026-08-20 提出，2026-08-23 更新版本）：已取得 Nexus 158886
  保留的 exact-version `VIGILANT SE (CHT)` 1.8.1；部署時期只套用於當時 Dev profile 的最高
  優先級，未納入當時的一般遊玩環境（兩者已於 2026-08-20 併入唯一 profile，2026-08-23 更名為 `modpack-main`）。官方英文與
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
  日語配音保留是預期行為；作者檔與私人修正都不納入公開成品或對外重發。
  **2026-08-23 更新**：上面那句「1.8.2 來源準備尚未取代現役 1.8.1 layer」寫於 2026-08-21 01:16，
  已被同日稍晚的 `1fc1a97`（VIGILANT exact-version 群組升級到 1.8.2，通過 parity 驗證）推翻。
  現役啟用的是 `VIGILANT SE Traditional Chinese 1.8.2`，1.8.1 layer 已停用。
  **真人抽查本身仍未做**，只是對象改成 1.8.2；上述 45 筆 `BOOK.DESC` 私人修正同樣已升到 1.8.2。

- **Scene ghost rendered-camera ray：15 條實機驗收**（2026-08-21 提出，2026-08-23 更新）：
  **攝影機語意已於 2026-08-22 裁決 = 選項 3（rendered-camera ray）**，理由是連續放置與畫面
  瞄準最自然；**實作也已完成並推送**（`scene-capture-bridge` 的
  `feat/ghost-camera-ray-2026-08-22@a17e460 fix: aim placements from rendered camera`）。
  原本這條在問「請決定三選一」，已經沒有要決定的事了。

  **剩下的是人眼驗收，而且必須涵蓋三種情境**——第一人稱、vanilla 第三人稱、SmoothCam，
  **不可只驗第三人稱就宣告通過**。固定 15 條清單在
  [`agentctl/logs/scene-ghost-camera-ray-2026-08-22.md`](agentctl/logs/scene-ghost-camera-ray-2026-08-22.md#runtime-驗收清單固定-15-條)。

  > 2026-08-23 一次嘗試中斷：DLL 已部署、環境已備妥，但 log 證據只支持 2 條，
  > 其中三條的關鍵字出現 0 次。**上次沒過，要重跑，不要當作已完成 13 條。**

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
  [wuxin-character-overhaul-se-ae-compatibility.md](wf/workflows/investigation/findings/wuxin-character-overhaul-se-ae-compatibility.md)。

- **BG3 場景佈局實檔驗證**（2026-08-11）：桌面研究已確認 LSLib 可把 BG3
  `Levels/` 下的 `.lsf` 轉成可讀 `.lsx`，但尚未用使用者持有的遊戲資料驗證 placement
  欄位能否無損對映 ModForge `placements`（位置、旋轉、尺度、base/resource identity）。下次
  有 BG3 安裝或合法抽取素材時，挑一個小型 level 做 `.lsf` → `.lsx`，記錄欄位與一組實例，
  再決定是否開 converter/spec 工作；沒有實檔前不宣稱 port pipeline 可行。評估框架與候選
  比較見 [port-source-survey](analysis/port-source-survey/README.md)。

- **`~/Downloads/_已入庫-2026-08-23/` 的 52 個確認重複壓縮檔要不要刪**（2026-08-23）：
  這 55 個項目共 **5.7GB**，是 Downloads 歸檔時逐檔開壓縮檔比對後確認**內容已在
  `~/skyrim_mods/` 裡**的重複件（同 SHA-256，或瀏覽器重複下載留下的 `X.7z`／`X (1).7z` 對）。
  沒有刪，原樣搬到這個資料夾等你決定。刪掉沒有風險——庫裡有同內容的檔，MongoDB 也已建索引；
  但這是不可逆操作，所以不自行執行。要刪就直接 `rm -rf` 整個資料夾。

- **L4 剩下 146 個舊命名壓縮檔只能人工辨識**（2026-08-23）：全庫 `naming_pattern=legacy`
  的 174 筆已用 Nexus `md5_search` 從**檔案內容**還原來源，28 筆查到（結果進 Mongo 的
  `nexus_md5*` 欄位）。**剩下 146 筆 Nexus 查無此 md5**——來源是對岸站台、被解壓重打包過、
  或本來就不是 Nexus 的東西，自動化到此為止。清單（含大小與壓縮檔內的 plugin 名當線索）在
  [l4-md5-resolution.md](mod-library/audits/l4-md5-resolution.md#仍需人工辨識146-筆)，
  最大的幾筆是 `BDOR Complete Collection`（2.63 GiB）、`Snezhinka.Sentinel.Girls2`（1.39 GiB）、
  `JH_NPC整合包SSE.zip`（1.29 GiB）。你只需判斷「想留／想裝／沒興趣」，不必逐行填表。
