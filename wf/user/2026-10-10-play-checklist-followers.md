# 10-10 檢查清單：隨從與人物

[回總頁](2026-10-10-play-checklist.md)｜〔〕是 `agentctl/handoffs/2026-10-10/` 下的報告目錄。崩潰的處理方式一律照總頁 1e。

外觀共通檢查（下面寫「外觀」的都指這一套）：臉不黑、不灰，不是素頭（大媽臉）；對她用 `<ref>.unequipall` 看身形是 Kurone 預設、脖子與手腳接縫正常。臉不對時先試 `disable`／`enable`，再回報。

## Saya

- [ ] **外觀**，另外看身體膚色和頭部是否一致（可能有細微色差）；頭髮染色跟著 Hair Colour Sync NG 走，物理髮會動。〔batch4a-kurone〕
  - **agent 10-10 實機**：**使用者肉眼確認 OK（10-10 17:3x）**；臉被她自帶的面具遮住；髮色同步和物理髮留給你。〔ingame-test〕
- [ ] **和 Yoana 並排比**（Yoana 是用舊版 Saya 換的臉），看像不像你要的。〔batch4a-kurone〕
  - **agent 10-10 實機**：agent 驗不了，留給你（Yoana 本人外觀你已經確認 OK）。〔ingame-test〕

## Liz 與 Karin

- [ ] **Liz**：劫匪峽谷洞穴裡被綁著，救出後對話是繁中；**頭髮不粉紫**（補過貼圖）；外觀。之後她會去 Moorside Inn；黑境研究所旁的 Golden Mushroom 站在地板上，不卡在牆裡。〔batch4a-kurone〕
  - **agent 10-10 實機**：**使用者肉眼確認 OK（10-10 17:3x）**；agent：頭髮黑色、不是粉紫，對話繁中；救援、搬去 Moorside、Golden Mushroom 留給你。〔ingame-test〕
- [ ] **Karin**（雪漫醉獵人酒館）：外觀。〔batch4a-kurone〕
  - **agent 10-10 實機**：**使用者肉眼確認 OK（10-10 17:3x）**。〔ingame-test〕

## Nell（冬堡學院暗門後）

- [ ] **跟隨與解散**：招募、一路跟隨、解散後她自己走回基地（走的就是暗門）。對話與名字是繁中，她叫你「學弟妹」。〔nell〕
  - **agent 10-10 實機**：agent 部分驗過：對話繁中；招募、解散留給你（AutoSEQ 報 KuroneNellSecretBase 的 SEQ 過期，招募對話可能出不來）。〔ingame-test〕
- [ ] **外觀**；臉色異常先回報（facegen 裡有一條舊路徑，預期不影響）。穿她的鞋時腳不陷地（RaceMenu High Heels）。〔nell〕
  - **agent 10-10 實機**：**使用者肉眼確認 OK（10-10 17:3x）**；高跟鞋留給你。〔ingame-test〕

## 靈魂石冢的 NPC

- [ ] **Lilith、Chaos、沉睡巨人旅店的 Emma** 等女性 NPC：外觀；OBody 不會再套隨機身形。Clash 保持她自帶的身體。〔soultomb〕
  - **agent 10-10 實機**：**使用者肉眼確認 OK（Lilith、Chaos，10-10 17:3x）**；Emma 和 OBody 留給你。〔ingame-test〕

## 瓦蕾莉卡（VDAO）

<!-- wf-nav -->
- [ ] **名字**是「瓦蕾莉卡」（之前被 Kurone 層蓋成英文），臉仍是 Kurone 版，不是大媽臉、黑臉或原版臉。〔batch3、vdao〕
  - **agent 10-10 實機**：**使用者肉眼確認 OK（10-10 17:3x）**；agent：名字是瓦蕾莉卡、臉是 Kurone 版。〔ingame-test〕
- [ ] **招募**：完成〈Beyond Death〉、拿到上古卷軸後，在靈魂石冢跟她說 **No**（「我不能认同。你不能留在这里。」）。選單裡如果同時有原版或 NFF 的「跟我來」，選帶「（VDAO）」字樣的那條。〔vdao〕
  - **agent 10-10 實機**：agent 驗不了，留給你（VDAO 的選項有出現）。〔ingame-test〕
- [ ] **召喚**：在 Volkihar 實驗室用法術「召唤瓦蕾莉卡」，說明文字是「将瓦蕾莉卡召唤到你身边。」，**不是 Lyra**（出現 Lyra 代表 esp 裝錯版本）。〔vdao〕
  - **agent 10-10 實機**：agent 部分驗過（離線查）：法術名是「召唤瓦蕾莉卡」，不是 Lyra；實際召喚留給你。〔ingame-test〕
- [ ] **母女對話**：帶 Serana 和她一起進城（兩人在 500 單位內）會觸發閒聊，字幕簡中。〔vdao〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **NFF 名單裡沒有她**；用「（VDAO）是时候分道扬镳了。」解散，她要回城堡，不能卡在跟隨狀態。舊存檔若已跑過 RDO 的 Valerica 任務，可能要用 VDAO 的「Follower Reset - Dismiss First」重設。〔vdao〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## Ashe 與 Serana

- [ ] **兩人同隊**時偶爾互相聊天，字幕中文；Ashe 看書那段對話不會一直重播。一直沒觸發的話，主控台 `set MM_AsheranaBanterGV to 2`。〔tradingposts〕
  - **agent 10-10 實機**：agent 驗不了，留給你（`MM_AsheranaBanterGV` 目前是 0）。〔ingame-test〕

## 其他人物

- [ ] **帝國士兵的臉**：交易站改過一名原版帝國士兵；看到臉和脖子顏色明顯不同（黑臉）就回報，已知可能是 facegen 放錯資料夾。〔tradingposts〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **衛兵隨從**：Become a Guard 升階後，在營房（Elrich）、喬瓦斯卡（Runa）、旗幟母馬（Jorvald）能招衛兵隨從；週薪通知「你領到了本週薪水 N 金幣。」〔artisans-guard〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 隨從閒聊（Dynamic Follower Banter）

只有**用原版配音的隨從**（Lydia、Jenassa、Marcurio、Aela、Mjoll 等原版隨從；Serana 不支援）會參加；Kurone、Sofia、Auri 這類自訂配音隨從不會開口。至少要帶兩個原版配音隨從（NFF 多人跟隨）。〔m194158〕

- [ ] **會聊天、字幕是中文（簡中）**：帶兩個以上原版配音隨從走一段路，會互相要東西吃、吵武器防具、聊天氣、戰後互相問候。剛裝時可能連著觸發好幾段。完全沒聲音就存檔再讀檔一次（作者建議）。〔m194158〕
- [ ] **通知是繁中**：隨從吃東西、買東西、生病時左上角會跳「〈名字〉剛吃了點雞肉。」這類通知；英文就回報。MCM 選單是英文（框架介面，依慣例不翻）。〔m194158〕
- [ ] **不搶話**：和 Chatty NPCs（同作者）或 RDO 的隨從評論同時出現時，看會不會兩段疊在一起講。太吵就在 MCM 把觸發機率（預設 100）調低，或關掉不想要的類別。〔m194158〕
- [ ] **假疾病**：被熊、狼、夏魯斯等打到後隨從可能「生病」（只扣隨從自己的回血，玩家不受影響）。不想要就在 MCM 關掉整個疾病系統。〔m194158〕
- [ ] **屍體評論**：隊友倒下後其他人會評論（NFF 用的 Notice Corpse patch 已裝）。〔m194158〕
- [ ] **吃喝沒有聲音**：隨從吃東西、喝酒時只有動作，沒有咀嚼／吞嚥音效（已裝靜音 patch）；其他閒聊語音照常有聲音。〔m194158〕
