# WAIT_USER — 等待使用者的事

只列需要使用者親自做／驗證才能繼續的 open 項；完成即移除，不留完成清單。

> 2026-08-20 起 MO2 只保留一個 profile；2026-08-23 更名為 `modpack-main`。下文的舊 profile 名稱只描述歷史部署或驗證環境，不代表現在仍可切換。

## 回家下載／重建

- **YouTube 候選 SOURCE-HOLD 逐件升級（可選）**：35 支候選影片已完成 owner-level routing；公司端沒有瀏覽器、Nexus HTML 受 Cloudflare 阻擋且無 API key，所以未重查的 current metadata／archive 全部保持具體 HOLD。只有要升級某一件時，回到有 Nexus API key／houseCARL／archives 的環境，依 [coverage 的 reopen procedure](modpack-design/content-plan/youtube-candidate-final-coverage-audit-2026-08-25.md) 一次查一件；不得把 HOLD 直接改成 GO。

- **三個 subproject 完整離線測試**：可補依賴／工具的環境重跑。`projects/scene-capture-bridge` portable MinGW CTest **2/2 PASS**，但完整 `x64-mingw-static` nlohmann-json triplet 仍缺；`projects/darksouls-port` 仍為 **29/35**，6 項因正式必要的 `scipy`／`shapely` 未安裝而 ERROR；`projects/ModForge` 在公司 Windows 沒有 `dotnet`，WSL 只有 `/bin/sh`、沒有 `bash`，且 repo 路徑未掛載，因此 **1123 offline suite 尚未重跑**。不下載或改測試掩蓋缺依賴；回到可補依賴的環境後依各 repo README 重跑。

- **DMK 1.5.0 人工校對版**：在家用 exact official／CHS archives、7z、OpenCC 執行 [`build_dmk_cht_layer.py`](mod-library/l10n/tools/build_dmk_cht_layer.py)，確認 offline gate `human_reviewed_zh_tw`、66 reviewed、38 override、0 unresolved；將單檔 `Data/Viny Mods/DMK/Language.json` layer 部署至唯一 profile。肉眼抽查一般設定、相機、PC／手把按鍵、OAR converter 警告並做移動 smoke。現在的 `Machine-Private.7z` 仍是 2026-08-21 未校對機翻包。證據：[安裝結果](agentctl/logs/mcm-helper-dmk-cht-install-2026-08-21.md)。

- **EnaiRim Batch 0：五個 Nexus archives**：有既有登入 session 的 Linux 環境依 [nexus-intake](wf/workflows/nexus-intake/README.md)，headful Chrome＋CDP 一次一檔取得並逐件核對原始檔名／API version／bytes／SHA-256／manifest：Mannaz 3.0.1（mod 87219，main file id **406689**；`372921` 是錯的 1.1.0 old version）、Mannaz CHS 3.0.1（98760 main）、Freyr 1.2.0（88043 main）、Freyr CHS 1.2.0（98756 main）、Audugan 1.0.0（169621 main）。Valravn 2.2.0 已在 catalog，不需重抓。不得輸入憑證或處理 CAPTCHA。精確檔案資料：[Batch 0 target table](agentctl/logs/enairim-batch0-target-table-2026-08-24/README.md)；前置與 rollback：[Batch 0 preflight](agentctl/logs/simonrim-to-enairim-final-selection-2026-08-24/batch-0-preflight.md)。

## 一次整包 UI／中文／任務驗收

- **EnaiRim Batch 7 終態人眼 gate**（等 Batch 1–6 施工後）：確認 Audugan／Valravn private CHT 與其他新文字層無方框、亂碼、截斷、錯誤術語；shrine／standing stone／High Hrothgar candidates 無穿插且可互動；Valravn 搭 BFCO／Precision／TDM／TK Dodge／WYT 的輸入、多人節奏、武器速度、耐力、命中手感可接受；抽查 race／faith／spell／enchantment／shout UI。固定範圍：[Batch 7 計畫](agentctl/logs/simonrim-to-enairim-final-selection-2026-08-24/batch-7-integration-promotion-plan.md)。

- **Modpack-KR Batch 6 final gameplay**：自動 lane 21/21 PASS、`load_epoch 1 → 2`、0 new crash 不能代替真人。需新遊戲、城市／NPC 外觀、BFCO 戰鬥與移動手感、Mysticism／Adamant、CT77／AVE 換裝、隨從招募及 RDO／Recorder／Sofia 對話、Altano 的 VIGILANT 正常入口／字幕／語音、自然跨入新增 worldspace；另抽看 MCM 方框／亂碼、兩三本 description overlay 書、字幕／語意。VIGILANT 本體／英語語音／正體／book overlay 必須精確同版 **1.8.2**；Silent Voice 缺口已接受、不需 TTS。證據：[Batch 6 RESULT](agentctl/logs/modpack-kr-final-smoke-2026-08-21/RESULT.md)。

- **四個首次生效中文層**：抽查 Timing is Everything SE **2.2** MCM、The Choice is Yours **2.7** 接受／拒絕對話、At Your Own Pace **8 ESP** 各線推進選項、SkyParkour **3.6.2** `Interface/Translations` UI；確認無方框、mojibake、截斷、空白。排序稽核可重跑 `python3 mod-library/l10n/tools/audit_layer_priority.py`。

- **RDO Final 正體中文**：[layer README](mod-library/l10n/mods/Relationship-Dialogue-Overhaul-Traditional-Chinese-Final/README.md)。已完成 9,766-record topology、4,071 ESP zstrings、六個 follower PEX display slots 及 script-binding gates；真人仍須抽查關係對話／選項／字幕、任務／通知、賄賂金額、Gelebor／Isran／Valerica 等待／離隊通知，確認無方框、亂碼、空白、未替換 token、截斷、新 crash。

- **Recorder Follower 3.0 正體中文**：[layer README](mod-library/l10n/mods/Recorder-Follower-Traditional-Chinese-3.0/README.md)。離線 gate 與固定 baseline smoke 3/3 PASS；真人抽查招募／一般對話、字幕、任務日誌、書籍、通知，確認無方框、亂碼、空白、截斷、新 crash；英語配音保留是預期。

- **Sofia Follower 2.51 v2 正體中文**：[layer README](mod-library/l10n/mods/Sofia-Follower-Traditional-Chinese-2.51-v2/README.md)。離線 gate 與固定 baseline smoke 3/3 PASS；真人抽查招募／一般對話、字幕、任務日誌、MCM、關係狀態、左上通知，確認無方框、亂碼、空白、截斷、新 crash；英語配音保留是預期。

- **VIGILANT SE Traditional Chinese 1.8.2**：現役已是 exact **1.8.2**（1.8.1 已停用），45 筆召喚書／石之碎片 `BOOK.DESC` 私人 text-only layer 亦已升版；真人在晨星城風岳旅店找 Altano，抽查主線開場、對話／字幕、日誌／目標、書籍、物品／效果、MCM，至少打開一件「石之碎片」確認描述為正體，確認無方框、亂碼、空白、截斷、新 crash。英／日配音保留；作者檔與私人修正不公開重發。

- **2026-08-20 新任務內容批**：UNSLAAD **3.0.6b**、Missives **2.03**、DAc0da **1.1.0b**、GLENMORIL **0.96.80b** 的 MCM／任務入口、正體日誌／對話／字幕、實際語音、跨 worldspace 仍需拆批真人抽查；尚未走過流程不可稱 gameplay PASS。GLENMORIL 語音覆蓋 3,653/4,792（76.23%），UNSLAAD 英語語音只涵蓋 Act 1；Silent Voice 是接受狀態，不需 TTS。自動 smoke 7/7 及後續 21 PASS 只證 load／cell／save-reload。證據：[quest batch log](agentctl/logs/quest-content-batch-2026-08-20.md)、[final smoke RESULT](agentctl/logs/modpack-kr-final-smoke-2026-08-21/RESULT.md)。

## 獨立功能驗收

- **Scene ghost rendered-camera ray**：實作已完成（`scene-capture-bridge` `a17e460`），只剩固定 15 條真人驗收；必須涵蓋第一人稱、vanilla 第三人稱、SmoothCam，不可只驗第三人稱。上次 log 只支持 2 條且三條關鍵字為 0，需重跑，不得當作 13/15 通過。清單：[固定 15 條](agentctl/logs/scene-ghost-camera-ray-2026-08-22.md#runtime-驗收清單固定-15-條)。

- **Simonrim Batch 4E**：Thaumaturgy **1.5**、精確同版繁中、Execute XP VMAD fix、184-record AVE／Constellations merge 的靜態與 smoke 已過；真人抽樣附魔分解→學習→製作→裝備／重載／充能、Empowered Strike power-attack proc、slot restriction、vanilla／AVE loot/vendor 階級比例與自然度。證據：[Batch 4E RESULT](agentctl/logs/simonrim-batch4-4e-2026-08-16/RESULT.md)。

- **Simonrim Batch 4A**：Apothecary **1.3.9**、Fishing **1.4.1**、Saints and Seducers **1.4.0**、Rare Curios **1.4.0** 及四個精確版繁中層的真人鍊金／經濟／戰鬥抽樣：混合各來源原料、戰鬥塗毒、vendor 庫存／價格／early-game 供應、長 session 平衡與存讀檔手感。既有 gate 7/7、SPID 19/19 不需重跑。證據：[Batch 4A RESULT](agentctl/logs/simonrim-batch4-4a-2026-08-16/RESULT.md)。

- **Simonrim Batch 4M/P**：Mysticism **2.5.0**、Adamant **6.0.4**、精確版繁中、Scrambled Bugs 設定與 SPID 修正的真人功能／手感抽樣：vendor 買書→讀書→施放 novice／apprentice 法術、Adamant 天賦效果、BFCO 輕／重／方向／sprint attack 與武器天賦、長期平衡及存讀檔。既有 load／VFS／完整性與存讀檔驗證不需重跑。證據：[Batch 4M/P RESULT](agentctl/logs/simonrim-batch4-4mp-2026-08-16/RESULT.md)。

- **Expanded Skyrim Weaponry Batch 3A**：靜態與 runtime distribution 已過；真人／錄影確認鐵製戰戟、鋼製雙刃巨劍拔收、BFCO 普攻及動作銜接正常；單張截圖不能替代時間軸結論。完成後移除此項。

## 日後素材／清理決定

- **夜貓－無心 3.1.0（可選精確替換）**：目前 JH People **1.1.3**＋NPC Plugin Chooser 2 的 536 NPC patch 已滿足經典韓系 NPC 美化，不阻塞整包。若仍要精確 3.1.0，使用者只提供作者百度網盤中名稱含「人物美化」與「頭模替換」的 archive，放入既有 `/home/lorkhan/skyrim_mods/`；未取得完整資產許可不得公開重打包。相容性：[調查](wf/workflows/investigation/findings/wuxin-character-overhaul-se-ae-compatibility.md)。

- **BG3 場景佈局實檔驗證**：有合法遊戲資料時，以一個小型 `Levels/*.lsf` 做 `.lsf → .lsx`，記錄 placement 的位置／旋轉／尺度／base/resource identity 是否能無損對映 ModForge `placements`，再決定是否開 converter/spec；沒有實檔前不宣稱 pipeline 可行。評估：[port-source-survey](analysis/port-source-survey/README.md)。

- **`~/Downloads/_已入庫-2026-08-23/` 52 個確認重複壓縮檔**：55 項共 5.7GB，內容已在 `~/skyrim_mods/`、同 SHA-256 或瀏覽器重複件；使用者決定是否刪除，agent 不自行執行不可逆刪除。

- **L4 146 個 legacy 命名壓縮檔**：174 筆中 28 筆已用 Nexus `md5_search` 還原，剩 146 筆查無 md5，需使用者判斷想留／想裝／沒興趣，不必逐行填表。清單（大小與 plugin 線索）：[l4-md5-resolution](mod-library/audits/l4-md5-resolution.md#仍需人工辨識146-筆)。
