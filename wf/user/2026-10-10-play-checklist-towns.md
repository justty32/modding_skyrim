# 10-10 檢查清單：城鎮與室內

[回總頁](2026-10-10-play-checklist.md)｜〔〕是 `agentctl/handoffs/2026-10-10/` 下的報告目錄。崩潰的處理方式一律照總頁 1e。

## 白漫：馬廄與車夫

- [ ] **馬廄看一眼**：Dovah 的待售告示與馬車、CFTO 的車夫跟車、Cut Content 的馬廄場景，彼此不該穿模或擋路；馬廄柵門預設是開的（Dovah 刻意的）。〔camp-hunt-install〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **白漫車夫**：對話「我想雇你的马车。」→ 開地圖選點 → 先跳「这会花费 N 金钱，继续吗？」→ 選是才傳送。不能點了就直接傳送。〔batch-uc-has-bcd〕
  - **agent 10-10 實機**：agent 部分驗過：Bjorlam 只剩「我想雇你的马车。」一條（BCD），CFTO 的清單沒出現；地圖選點和車資確認留給你。〔ingame-test〕

## 白漫：鐵匠、附魔、鍊金（Artisans）

<!-- wf-nav -->
- [ ] **鐵匠對話並存**：找 Adrianne 或 Eorlund，Honed Metal 的「我需要你的服务。」和 Artisans 的「你能帮我制作东西吗？」「你能帮我升级装备吗？」都要出現。Adrianne 仍站在鍛爐旁工作（Smelting Plus 的移位已清掉）。〔artisans-guard、batch2〕
  - **agent 10-10 實機**：agent 驗出問題：Adrianne 站在戶外鍛爐時只有 HM 的選項，**沒有** Artisans 的兩條；同一個 NPC 在 Warmaiden's 店內時三條都有。先到店裡問，原因待查。〔ingame-test〕
- [ ] **訂單**：下一張鍛造單，等遊戲內 1～3 天（匕首 1 天、一般 2 天、雙手／重甲 3 天）再回去，用「我是來領我訂的東西的」領貨。途中會收到信使的信，信的內文可能是英文（DLL 寫死）。〔artisans-guard〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **清單內容**：mod 加的裝備有出現，價格與強化後的數值合理。附魔師（Farengar）有白銀祝福、狂戰士之魂等自訂附魔（專家 3000、大師 6000 金）；鍊金師（Arcadia）有持續恢復藥水。〔artisans-guard〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 白漫：衛兵（Become a Guard）

- [ ] **入伍**：問白漫衛兵「你們現在還收新衛兵嗎？」→ 龍霄宮總管 Proventus → 衛兵隊長，會跳通知「歡迎加入衛兵，雛兵。」「今晚 10 點來報到值班。」。字幕是繁中，配音是英文。〔artisans-guard〕
  - **agent 10-10 實機**：agent 部分驗過：白漫衛兵有「你們現在還收新衛兵嗎？」（繁中）；後續流程留給你。〔ingame-test〕
- [ ] **夜巡 22:00～04:00**：通知「巡邏開始了。」→ 隨機事件 →「巡邏結束了。」→ 回報隊長。留意事件點附近 KhajiitWillFollow 的 NPC 有沒有被捲進戰鬥。〔artisans-guard〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **營房、喬瓦斯卡、旗幟母馬**：打光、音樂、中文地名都和裝之前一樣。如果變了，多半是 TaBg 被 MO2 挪了位置，見總頁 1a。〔artisans-guard〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 風盔：碼頭倉庫（Saya）

- [ ] **開場**：倉庫裡找到 Saya、Jii、Yasubei，對話與名字是簡中；進倉庫不該觸發擅闖。白天 8～22 點 Yasubei 站在倉庫門邊，晚上 Saya 和 Jii 在地下室睡。〔batch4a-kurone〕
  - **agent 10-10 實機**：agent 部分驗過：倉庫能載入，安兵卫在場並用簡中搭話；擅闖和 Saya／Jii 作息留給你。〔ingame-test〕

## 裂谷：鼠道

- [ ] **Saya 的圓形艙門**能進出，**帶隨從走一次**，看隨從會不會跟到門口。〔batch4a-kurone〕
  - **agent 10-10 實機**：agent 已驗 OK：艙門雙向傳送正常；帶隨從走一次留給你。〔ingame-test〕
- [ ] **往 Shadowfoot Sanctum 的門**傳送位置正常；鼠道的打光與中文地名「鼠道」不變。〔batch4a-kurone〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 冬堡學院：達成之廳

- [ ] **名稱**：門口與地圖顯示「成就大厅」，不是 Hall of Attainment。〔batch3〕
  - **agent 10-10 實機**：agent 已驗 OK（離線查現役贏家的 CELL 名＝成就大厅）。〔ingame-test〕
- [ ] **一樓 NPC**：平常巡走、進出兩扇大門正常，沒有卡在北側地板暗門（JK 地毯旁）附近。〔nell〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **暗門**：地板暗門能進 Nell 的秘密基地，基地的門能傳回大廳暗門的位置；**帶隨從走一次**，隨從要一起傳送。〔nell〕
  - **agent 10-10 實機**：agent 已驗 OK：雙向傳送正常，Nell 本人在基地；帶隨從留給你。〔ingame-test〕

## 雪漫：醉獵人酒館

- [ ] **Karin**：在酒館裡，對話是簡中，商人功能可用；外觀檢查見[隨從與人物](2026-10-10-play-checklist-followers.md)。〔batch4a-kurone〕
  - **agent 10-10 實機**：agent 已驗 OK：人在酒館，對話簡中，有買賣選項。〔ingame-test〕

## 配偶搬家（結婚後）

- [ ] **原版五城的房子**：配偶搬過去後，作息要帶有 AI Overhaul 的行為。〔batch3〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **Hearthfire 三棟**（湖景、晨星、窗景）：要能選、配偶要能住進去。這三棟之前可能是壞的，現在應該恢復了。〔batch3〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **CC 房子與亨德拉海姆**：CC 房子要能選、能搬；亨德拉海姆的配偶在新建築裡睡覺、吃早餐、到露台、大廳、吃晚餐。任務目標文字是「拜访你配偶的房子」。〔batch3〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
