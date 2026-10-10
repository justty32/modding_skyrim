# 10-10 檢查清單：野外與地點

[回總頁](2026-10-10-play-checklist.md)｜〔〕是 `agentctl/handoffs/2026-10-10/` 下的報告目錄。崩潰的處理方式一律照總頁 1e。

## 露營：Dovah 馬車與營地

- [ ] **第一次上車、啟用馬車前先存檔**。上游有一則 2.1.5 啟用馬車時 `XAudio2_7.dll` 崩潰的回報，Proton 下會不會發生不確定。崩了照總頁 1e 處理。〔camp-hunt-install〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **MCM**：`Dovah Rider` 頁有出現；自動拾取、自動採集預設是關的，確認一下就好。紮營時跳「也要清理树木吗？」選**否**。〔camp-hunt-install〕
  - **agent 10-10 實機**：agent 驗不了，留給你（要開 MCM）。〔ingame-test〕
- [ ] **中文**：馬車、營地、料理、手冊是簡中；待售告示名、車廂內部地名和多數通知列提示是英文（已知、翻不到）。〔camp-hunt-install〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 露營：吃東西與烤火（生存模式開著時）

- [ ] **Dovah 料理會回飽食**：有點餓時吃一份烤肉（大份）或一杯茶（極小份），飢餓值要回升；同一份食物只回一次，不會回兩次。戴著娜米拉戒指時一般食物不回飽（Taste of Death 的設計）。〔smi〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **營火取暖**：在雪地紮 Dovah 營地、生火，站在火旁約 8 公尺內，寒冷值要回升。〔smi〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **快速旅行**：生存模式開著時，從地圖快速旅行仍然可用。〔smi〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 狩獵：SHO 與 DAK

- [ ] **剝皮**：殺一隻鹿或狼，一般「搜刮」就能剝皮並推進時間（提示「…过去了…」）；`Shift＋E` 可以扛屍體；把獵物賣給商人要有對白。〔camp-hunt-install〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **Deepborn 的 Shift 互動照常**（DAK 換成 DLL 版的連帶影響）。〔camp-hunt-install〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 灌木叢（Hide in Bushes）

- [ ] **站進大片灌木叢**（例如河木一帶的松灌木），主動效果欄出現「藏身灌木叢」／「強化潛行」，蹲下時眼睛指示要比在空地上更晚張開；走出去 1～2 秒內效果消失。〔hide-in-bushes、artisans-guard〕
  - **agent 10-10 實機**：agent 驗不了，留給你（log 正常：OIF 規則 7 條、FLM 讀了 HideInBushes_FLM.ini）。〔ingame-test〕
- [ ] **蹲著貼矮灌木**（雪莓、薰衣草、薊）會有效果，站起來就消失；貼著松樹幹或樹樁也有小幅效果。完全沒反應的話，看 SKSE 目錄下的 `ObjectImpactFramework.log` 與 `FormListManipulator.log`。〔hide-in-bushes〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

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

<!-- wf-nav -->
- [ ] **Eydvina 的信**：完成同伴團「白銀之手」（加入內環）之前不該收到；完成後換一次地點，信使就會送來。〔batch3〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **新建築大門**：任務前門是鎖的（顯示需要鑰匙、不能撬）；打敗 Eydvina 拿到鑰匙後能開，任務標記指在這扇新門上。門一直打不開的話，停用 `CT15-Hendraheim-DoorLock-Dev-2026-10-10`。〔batch3〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **屋外與隨從**：屋外一圈加上西邊 Lost Valley、北邊龍塚，看有沒有浮空、埋地或 NPC 卡路；名冊「召集」後四名隨從出現（弗雷爾會召喚野豬古利），名字與說明都是中文。〔batch3〕
  - **agent 10-10 實機**：agent 部分驗過：屋外載入不崩，Papyrus 有 4 行武器架腳本錯誤（來源待查）；浮空和名冊召集留給你。〔ingame-test〕
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

## 第二次大戰（The Second Great War，內戰打完才開始）

內戰結束前這個 mod 幾乎看不到東西；下面多數項目要等內戰打完、收到信之後才驗得了。〔m152315〕

- [ ] **開場**：內戰結束（或 Ulfric／Tullius 死掉）後不久會有信差送信；任務名、信件、對白字幕是中文（簡中為主，少數 1.10.1 新句子用另一份譯本補）。MCM 選單維持英文。〔m152315〕
- [ ] **內戰地圖**：營帳裡的內戰地圖上，戰爭開打後會出現金色／藍色旗子標出各要塞與城鎮歸誰；旗子要插在要塞位置上，不是全擠在地圖中央（插錯位置就是地圖腳本出問題）。〔m152315〕
- [ ] **圍城**：第一場圍城（或任何一場）士兵會從城外湧入、雙方會打；打完不 CTD。城裡有改造的城市（雙倍大白漫、Capital Windhelm、COTN 晨星）特別注意士兵有沒有卡在牆裡或站在空中。〔m152315〕
- [ ] **被梭默佔領的城市**：Talos 神龕換成 Akatosh 神龕、城堡（孤獨城藍宮、風盔王宮、晨星、裂谷米斯特維爾）裡帝國或風暴斗篷的旗幟、床、物品會跟著換，不會新舊兩套疊在一起。〔m152315〕
- [ ] **要塞**：去救俘虜的要塞（尤其 Fort Dunstad 改造版、Fort Greymoor、Fort Sungard）裡，TSGW 加的士兵與門能正常出現；Fort Dunstad 有 6 個連結點兩邊打架只保留了 Fort Dunstad 的，士兵若在原地發呆屬已知小問題。〔m152315〕
- [ ] **野外遭遇**：戰爭期間路上會遇到梭默或帝國／風暴斗篷巡邏、逃難的市民；完全沒遇到過就回報（合併補丁有把 19 個遭遇加回清單）。〔m152315〕

## 兜帽陌生人（A Conversation，七千階梯頂）

- [ ] **他站得好好的**：High Hrothgar 門口階梯上的兜帽陌生人沒有懸空、沒有卡進階梯或 Skyrim Remastered／JK's 改過的石階模型；臉不是灰的；走近時不 CTD。〔eval-154926〕
- [ ] **對話**：選項與字幕是中文（簡中），英文配音正常播放；聊完他會離開。完全不出現就存檔後讀檔一次再看。〔eval-154926〕
  - **agent 10-10 22:00 煙霧**：MO2＋遊戲到主選單 PASS（esp 有 `*`、AutoSEQ 246 OK／0 need、無新 crash log、存檔不變）；站位與對話留給你。〔m186441〕

## 馬薩雷利亞（Masareria，白漫佩拉吉亞農場）

08-30 就裝了 1.3，10-10 升到 1.4（修地面透明、標記看得見、兩個商人箱子斷鏈）並重建中文層，另加「隱形牆拉桿」。〔m186441〕

- [ ] **任務起點**：佩拉吉亞農場屋裡有農夫 Masareru 和他的小說；對話、任務日誌、書名是中文（簡中）；地圖上的區域名（迷宫都市 马萨雷利亚、迷途森林等）是中文。〔m186441〕
- [ ] **異世界城鎮與地底層**：讀書進去之後，地面沒有透明的破洞、看不到地上浮著的標記方塊；配音是英文、字幕中文。〔m186441〕
- [ ] **隱形牆**：清完一層的敵人後牆要自己消失；沒消失時旁邊有一根「拉杆」，拉下去牆就消失、任務往下走。拉桿完全沒出現也不影響正常流程。〔m186441〕
- [ ] **回現實世界**：跟坐在城中央噴泉的作者說話能回去，也能調 Boss 血量（在任務第一階段就要設好）。〔m186441〕
- 若你在 1.3 時期已經進過異世界：1.4 改的是物件腳本屬性與地形，存檔裡已載入過的物件可能還是舊值；只有卡關時才需要回報。〔m186441〕
