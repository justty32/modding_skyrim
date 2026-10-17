# 10-10 檢查清單：野外與地點——據點與住宅

[回野外入口](../2026-10-10-play-checklist-wild.md)｜[回總頁](../2026-10-10-play-checklist.md)｜〔〕是 `agentctl/handoffs/done/2026-10/home-2026-10-10/` 下的報告目錄。崩潰的處理方式一律照總頁 1e。

## 交易站（Trading Posts）

- [ ] **Wayfinder（雪漫平原）與 Pale 兩站**：建築、商人、守衛都在，物件不浮空、不陷地，守衛不走進牆裡。〔tradingposts〕
  - **agent 10-10 實機**：agent 部分驗過：Wayfinder 載入正常，商人與守衛在場、名字中文；浮空看不清，Pale 兩站留給你。〔ingame-test〕
- [ ] **Granite Hill、Ryn's Lost Valley、Bleakwind 一帶**：沒有建築互相穿模。其他 5 站各看一眼，商人能交易、名字是中文。〔tradingposts〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 獸人據點（Orc Strongholds AIO）

- [ ] **四座各巡一次**（Largashbur、Dushnikh Yal、Mor Khazgur、Narzulbur）：建築不浮空、不穿模，門能進，NPC 沒卡在牆裡；Largashbur 長屋與地窖的光照不變、名稱是中文。附近的遭遇事件點如果和新建築疊在一起，截圖。〔batch4b〕
  - **agent 10-10 實機**：**使用者肉眼確認 OK（10-10）**；agent 確認四座載入不崩。〔ingame-test〕

## 野松會所（The Nasty Pine，風盔城東）

- [ ] **室外**：Hollyfrost／Hlaalu 農場一帶的建築、圍欄、路沒有和地形打架；Hlaalu 農場那一格 NPC 走路有沒有卡住（已知和 Pride of the Niben 有一塊 navmesh 衝突）。〔batch4b〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **室內**：租床、桑拿自動脫衣的提示是中文；女侍、吟遊詩人的服裝在脖子、手腕、腳踝、腰帶處沒有破洞。〔batch4b〕
  - **agent 10-10 實機**：agent 部分驗過：室內載入正常，截圖看不出服裝破洞；中文提示留給你。〔ingame-test〕

## 亨德拉海姆與其他 CC 住宅

### 亨德拉海姆：任務與大門

- [ ] **Eydvina 的信**：完成同伴團「白銀之手」（加入內環）之前不該收到；完成後換一次地點，信使就會送來。〔batch3〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **新建築大門**：任務前門是鎖的（顯示需要鑰匙、不能撬）；打敗 Eydvina 拿到鑰匙後能開，任務標記指在這扇新門上。門一直打不開的話，停用 `CT15-Hendraheim-DoorLock-Dev-2026-10-10`。〔batch3〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
### 亨德拉海姆：屋外與隨從

- [ ] **屋外與隨從**：屋外一圈加上西邊 Lost Valley、北邊龍塚，看有沒有浮空、埋地或 NPC 卡路；名冊「召集」後四名隨從出現（弗雷爾會召喚野豬古利），名字與說明都是中文。〔batch3〕
  - **agent 10-10 實機**：agent 部分驗過：屋外載入不崩，Papyrus 有 4 行武器架腳本錯誤（來源待查）；浮空和名冊召集留給你。〔ingame-test〕
### 其他 CC 住宅

- [ ] **Bloodchill Manor** 要等黎明守衛「血脈」完成後才收到邀請；**Gallows Hall** 大門在「召喚儀式法術」任務完成前是鎖的，完成後進入就自動解鎖。〔batch3〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 靈魂石冢（Soul Tomb，河木外）

- [ ] **傳送畫框**看得到、能傳送、撞上去有碰撞；Boss 戰後的金幣堆能拾取；在人偶、鐘、雕像、屍堆旁近戰 1～2 分鐘不會崩。崩了先照總頁 1e，再看 callstack 有沒有 `hkpCompressedMeshShape`。〔soultomb〕
  - **agent 10-10 實機**：agent 部分驗過：石冢內部載入、待了幾分鐘沒崩；畫框、Boss、近戰留給你。〔ingame-test〕
- [ ] **NPC 不互殺**：入口與沉睡巨人旅店附近誤傷中立 NPC，不會立刻全員敵對；石冢內 NPC 之間不互打。書與通知是中文。〔soultomb〕
  - **agent 10-10 實機**：agent 部分驗過：石冢內約 30 名 NPC 都不敵對，名字中文；誤傷測試留給你。〔ingame-test〕

## 風暴斗篷軍營（IDE Stormcloaks）

- [ ] **每個軍營多 3 名士兵**，和他們的新對話是簡中字幕。口音像土匪或平民的士兵，內戰台詞要有聲音（Nord 士兵的聲線）；仍然只有字幕的話，記下那句字幕。〔batch3〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **Gray-Mane 與 Galmar**：「失蹤」任務救出 Thorald 後的新流程能走；Galmar 的新對話和原本 RDO／AI Overhaul 的行為並存。〔batch3〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 任務板（Missives）

- [ ] 不會派「找車夫／船夫」的信；Tyranus 與 Vigilant Carcette 也仍在禁派清單上。〔batch2〕
  - **agent 10-10 實機**：agent 驗不了，留給你（另見 AutoSEQ：MissivesExpansion 沒有 SEQ 檔）。〔ingame-test〕
