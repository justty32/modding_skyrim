# 2026-10-10 進遊戲檢查清單

> 整理線彙整 10-10 十七份報告（`agentctl/handoffs/2026-10-10/`）。內容都取自各線 REPORT 的「實機清單」與「順帶看到」，沒有另外推新結論；重複的項目已經合併。全部都還沒進遊戲驗過。
>
> **10-10 17:23–17:51 agent 實機兩輪（沒崩潰）**：結果逐項標在各項底下（OK／問題／留給你）。要先看的三件事：Artisans 選項只在店裡出現、AutoSEQ 報 53 支 SEQ 缺漏、MO2 每開一次都重排 master 區。詳見 [ingame-test REPORT](../../agentctl/handoffs/2026-10-10/ingame-test/REPORT.md)。

今天新裝 37 組 mod（含中文層與自製層，plugins.txt 多了 78 行）。這一頁放「開遊戲前」與總表，實測項目依地點分成四頁：

- [城鎮與室內](2026-10-10-play-checklist-towns.md)：白漫、風盔、裂谷、冬堡、雪漫、配偶搬家
- [野外與地點](2026-10-10-play-checklist-wild.md)：露營狩獵、灌木叢、交易站、獸人據點、野松會所、亨德拉海姆、靈魂石冢、軍營、第二次大戰
- [戰鬥與系統](2026-10-10-play-checklist-combat.md)：敵人、法術、硬直、閃避、鍛造熔煉、撿雜物、生存模式
- [隨從與人物](2026-10-10-play-checklist-followers.md)：Saya、Liz、Karin、Nell、瓦蕾莉卡、Ashe 與 Serana

## 1. 開遊戲前

### 1a. MO2 第一次開過之後（交給下一條線，你不用做）

MO2 第一次啟動會重寫 profile，新 plugin 的 `*` 可能掉、順序可能被改。下一條線要做的事合併成一份資料檔：[2026-10-10-play-checklist-mo2-reverify.json](2026-10-10-play-checklist-mo2-reverify.json)（82 列；10-10 mo2-reorder 後改版，行號以 profiles `68e37bd` 為準）。

欄位：`line`＝profiles `68e37bd` 當下 plugins.txt 的行號；`plugin`＝檔名；`expect_star`＝該不該有 `*`；`order_rule`＝順序要求；`note`＝備註；`report_path`＝出處 REPORT。統計：80 行要有 `*`、2 行（Dodge Shot 另兩支）刻意不勾；有順序要求的 43 行，其餘是 ESL 新記錄、放哪都行。

最容易出事的三處：

- **普通 esp 不能排進 master 區**：TaBg、Kurone 系、Soul Tomb、Nell、VDAO 以前排在 USSEP 前面，但 USSEP 帶 ESM 旗標，MO2 和引擎都會把普通 esp 移到 master 類後面，所以每次開 MO2 都會「重排」。10-10 mo2-reorder 已把 record 改成合法順序（TaBg 現在在第 134 行），因 USSEP 先載而翻掉的 8 筆由 `EngineOrder Forward 2026-10-10.esp` 補回。**不要再把它們拉回 USSEP 前**；reverify 的 PARTITION gate 會抓（[mo2-reorder REPORT](../../agentctl/handoffs/2026-10-10/mo2-reorder/REPORT.md)）。
- **第 1300～1304 行**（亨德拉海姆五支）要在 WorldFix AFull（第 1305 行）之前；**最後一行**必須是 `EngineOrder Forward 2026-10-10.esp`，倒數第二行是 `ZH HallOfAttainment Name Fix`。
- MO2 關閉時常見的暫態回寫：把新 BSA 寫進 archives.txt（預期行為）。三條停用條目（Animated Ice Floes／Bergs、Varinia 補完 esp）的檔案不在 VFS，已在 mo2-reorder 從 record 刪掉，不會再被 MO2 丟出差異。

### 1b. 你自己要做的：DAc0da

- [ ] **先不要升到 15 級。** 讀檔後在主控台打 `getglobalvalue zDcdGStartLevel`，要回 25；如果是 15，打 `set zDcdGStartLevel to 25` 再查一次。預期 15 級時天上不出現 Numidium，25 級才開始。〔batch2〕
  - **agent 10-10 實機**：agent 驗出問題：存檔裡目前是 **15**，還沒改，要你自己 `set zDcdGStartLevel to 25`。〔ingame-test〕

### 1c. 你自己要做的：生存模式

- [ ] **Sleep to Level Up 手動改成 Always Disabled**：MCM → Survival Control Panel → Main。現有存檔一定要手動設一次（新開檔會自動讀 `Data/Survival.json`）。驗證方式：升級後不睡覺，也能直接加點。〔smi〕
  - **agent 10-10 實機**：agent 驗不了，留給你（要開 MCM）。〔ingame-test〕
- [ ] **生存模式開關**：設定 → 遊戲性 →「生存模式」。開著時畫面有寒冷／飢餓／疲勞指示；關掉後指示消失、需求停止。新開檔預設是開的。只想關其中一項，就在主控台 `set SMI_ColdShouldBeEnabled to 0`（飢餓用 `SMI_HungerShouldBeEnabled`、疲勞用 `SMI_ExhaustionShouldBeEnabled`），然後存檔、讀檔一次；改回 1 就恢復。〔smi〕
  - **agent 10-10 實機**：agent 已驗 OK（開啟狀態）：四個開關 global 都是 1，寒冷／飢餓的通知是中文；切換開關留給你。〔ingame-test〕

### 1d. 進遊戲先看一眼載入

- [ ] `我的文件/My Games/Skyrim Special Edition/SKSE/skse64.log` 裡，今天新增的這些 DLL 都要寫 loaded correctly：UnlootableClutter、HomeAutoSort、SkyPrompt、BetterCarriageDestinations、ModernStaggerLock、NPCSpellVariance、AutoEnemySpawn、ObjectImpactFramework、SurvivalModeImproved、ArtisansOfSkyrim、DovahRiderNative、DynamicActivationKey、PerfectlyValidWards、HairColourSyncNG、po3_SimpleOffenceSuppression。名字對不上時以 DLL 檔名為準。
  - **agent 10-10 實機**：agent 已驗 OK：15 個全部 loaded correctly（總共 157 個），兩輪都沒崩、沒有新的 crash log。〔ingame-test〕

### 1e. 崩潰時一律這樣處理

先跑 `agentctl/tools/snapshot_skse_logs.sh` 保存 log，再重開 MO2；把 crash log 的檔名交給線。各頁寫的「停用哪個 mod」是**查證後**的退路，不要在拿到 log 之前先停用。

## 2. 今天裝了什麼

總表抽成資料檔：[2026-10-10-play-checklist-installed.json](2026-10-10-play-checklist-installed.json)（39 列）。欄位：`mod`＝mod 名稱、`nexus`＝Nexus 編號、`version`＝版本、`self_layers`＝我方自製的中文層／修正層／設定改動、`report_path`＝施工 REPORT。

自製層大致分三類：中文覆蓋層（約 20 支，都過了方塊字檢查，缺字 0）；相容或合併層（Saya 鼠道、Nell 學院、Hendraheim 任務／門鎖／配偶任務、Missives 禁派清單、Trading Posts USSEP 回補、Smelting Plus 修正）；私有身體層（Kurone3、Soul Tomb、Nell，三組都改指 Kurone7 的身體，沒有動全域 CBBE）。

## 3. 不裝／延後

延後：

- **Campfire 一族**（Campfire、Skills of the Wild 等）：等下一個新周目再說。〔campfire-frostfall〕

今天評估後決定不裝：

- Frostfall（只剩你不要的寒冷系統）〔campfire-frostfall〕、Chocolate Poise（和 B&B、Elden Rim 的硬直來源重疊，4.x 剛重寫）〔chocolate-poise〕、I am not a slow walker（要排最後才生效，但會蓋掉 B&B 的跑速）〔slow-walker〕、Milandriel（和 Mixwater Mill 的 navmesh 硬衝突，另有 60 筆全域髒改）〔batch3〕。
- Valerica Valery、Aphrodelyn、A Secret to Hide、Isekai Hero、Dynamic NPC Scaling、Gilded Road、Dynamic Armor Rating：今天在對話裡裁示不裝，沒有對應的施工報告。

原始報告都在 [agentctl/handoffs/2026-10-10/](../../agentctl/handoffs/2026-10-10/)（各頁的〔〕標記就是子目錄名）。
