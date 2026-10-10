# 10-10 檢查清單：隨從與人物

[回總頁](2026-10-10-play-checklist.md)｜〔〕是 `agentctl/handoffs/2026-10-10/` 下的報告目錄。崩潰的處理方式一律照總頁 1e。

外觀共通檢查（下面寫「外觀」的都指這一套）：臉不黑、不灰，不是素頭（大媽臉）；對她用 `<ref>.unequipall` 看身形是 Kurone 預設、脖子與手腳接縫正常。臉不對時先試 `disable`／`enable`，再回報。

## Saya

- [ ] **外觀**，另外看身體膚色和頭部是否一致（可能有細微色差）；頭髮染色跟著 Hair Colour Sync NG 走，物理髮會動。〔batch4a-kurone〕
- [ ] **和 Yoana 並排比**（Yoana 是用舊版 Saya 換的臉），看像不像你要的。〔batch4a-kurone〕

## Liz 與 Karin

- [ ] **Liz**：劫匪峽谷洞穴裡被綁著，救出後對話是繁中；**頭髮不粉紫**（補過貼圖）；外觀。之後她會去 Moorside Inn；黑境研究所旁的 Golden Mushroom 站在地板上，不卡在牆裡。〔batch4a-kurone〕
- [ ] **Karin**（雪漫醉獵人酒館）：外觀。〔batch4a-kurone〕

## Nell（冬堡學院暗門後）

- [ ] **跟隨與解散**：招募、一路跟隨、解散後她自己走回基地（走的就是暗門）。對話與名字是繁中，她叫你「學弟妹」。〔nell〕
- [ ] **外觀**；臉色異常先回報（facegen 裡有一條舊路徑，預期不影響）。穿她的鞋時腳不陷地（RaceMenu High Heels）。〔nell〕

## 靈魂石冢的 NPC

- [ ] **Lilith、Chaos、沉睡巨人旅店的 Emma** 等女性 NPC：外觀；OBody 不會再套隨機身形。Clash 保持她自帶的身體。〔soultomb〕

## 瓦蕾莉卡（VDAO）

- [ ] **名字**是「瓦蕾莉卡」（之前被 Kurone 層蓋成英文），臉仍是 Kurone 版，不是大媽臉、黑臉或原版臉。〔batch3、vdao〕
- [ ] **招募**：完成〈Beyond Death〉、拿到上古卷軸後，在靈魂石冢跟她說 **No**（「我不能认同。你不能留在这里。」）。選單裡如果同時有原版或 NFF 的「跟我來」，選帶「（VDAO）」字樣的那條。〔vdao〕
- [ ] **召喚**：在 Volkihar 實驗室用法術「召唤瓦蕾莉卡」，說明文字是「将瓦蕾莉卡召唤到你身边。」，**不是 Lyra**（出現 Lyra 代表 esp 裝錯版本）。〔vdao〕
- [ ] **母女對話**：帶 Serana 和她一起進城（兩人在 500 單位內）會觸發閒聊，字幕簡中。〔vdao〕
- [ ] **NFF 名單裡沒有她**；用「（VDAO）是时候分道扬镳了。」解散，她要回城堡，不能卡在跟隨狀態。舊存檔若已跑過 RDO 的 Valerica 任務，可能要用 VDAO 的「Follower Reset - Dismiss First」重設。〔vdao〕

## Ashe 與 Serana

- [ ] **兩人同隊**時偶爾互相聊天，字幕中文；Ashe 看書那段對話不會一直重播。一直沒觸發的話，主控台 `set MM_AsheranaBanterGV to 2`。〔tradingposts〕

## 其他人物

- [ ] **帝國士兵的臉**：交易站改過一名原版帝國士兵；看到臉和脖子顏色明顯不同（黑臉）就回報，已知可能是 facegen 放錯資料夾。〔tradingposts〕
- [ ] **衛兵隨從**：Become a Guard 升階後，在營房（Elrich）、喬瓦斯卡（Runa）、旗幟母馬（Jorvald）能招衛兵隨從；週薪通知「你領到了本週薪水 N 金幣。」〔artisans-guard〕
