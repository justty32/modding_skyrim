# 10-10 檢查清單：野外與地點

[回總頁](2026-10-10-play-checklist.md)｜〔〕是 `agentctl/handoffs/2026-10-10/` 下的報告目錄。崩潰的處理方式一律照總頁 1e。

## 露營：Dovah 馬車與營地

- [ ] **第一次上車、啟用馬車前先存檔**。上游有一則 2.1.5 啟用馬車時 `XAudio2_7.dll` 崩潰的回報，Proton 下會不會發生不確定。崩了照總頁 1e 處理。〔camp-hunt-install〕
- [ ] **MCM**：`Dovah Rider` 頁有出現；自動拾取、自動採集預設是關的，確認一下就好。紮營時跳「也要清理树木吗？」選**否**。〔camp-hunt-install〕
- [ ] **中文**：馬車、營地、料理、手冊是簡中；待售告示名、車廂內部地名和多數通知列提示是英文（已知、翻不到）。〔camp-hunt-install〕

## 露營：吃東西與烤火（生存模式開著時）

- [ ] **Dovah 料理會回飽食**：有點餓時吃一份烤肉（大份）或一杯茶（極小份），飢餓值要回升；同一份食物只回一次，不會回兩次。戴著娜米拉戒指時一般食物不回飽（Taste of Death 的設計）。〔smi〕
- [ ] **營火取暖**：在雪地紮 Dovah 營地、生火，站在火旁約 8 公尺內，寒冷值要回升。〔smi〕
- [ ] **快速旅行**：生存模式開著時，從地圖快速旅行仍然可用。〔smi〕

## 狩獵：SHO 與 DAK

- [ ] **剝皮**：殺一隻鹿或狼，一般「搜刮」就能剝皮並推進時間（提示「…过去了…」）；`Shift＋E` 可以扛屍體；把獵物賣給商人要有對白。〔camp-hunt-install〕
- [ ] **Deepborn 的 Shift 互動照常**（DAK 換成 DLL 版的連帶影響）。〔camp-hunt-install〕

## 灌木叢（Hide in Bushes）

- [ ] **站進大片灌木叢**（例如河木一帶的松灌木），主動效果欄出現「藏身灌木叢」／「強化潛行」，蹲下時眼睛指示要比在空地上更晚張開；走出去 1～2 秒內效果消失。〔hide-in-bushes、artisans-guard〕
- [ ] **蹲著貼矮灌木**（雪莓、薰衣草、薊）會有效果，站起來就消失；貼著松樹幹或樹樁也有小幅效果。完全沒反應的話，看 SKSE 目錄下的 `ObjectImpactFramework.log` 與 `FormListManipulator.log`。〔hide-in-bushes〕

## 交易站（Trading Posts）

- [ ] **Wayfinder（雪漫平原）與 Pale 兩站**：建築、商人、守衛都在，物件不浮空、不陷地，守衛不走進牆裡。〔tradingposts〕
- [ ] **Granite Hill、Ryn's Lost Valley、Bleakwind 一帶**：沒有建築互相穿模。其他 5 站各看一眼，商人能交易、名字是中文。〔tradingposts〕

## 獸人據點（Orc Strongholds AIO）

- [ ] **四座各巡一次**（Largashbur、Dushnikh Yal、Mor Khazgur、Narzulbur）：建築不浮空、不穿模，門能進，NPC 沒卡在牆裡；Largashbur 長屋與地窖的光照不變、名稱是中文。附近的遭遇事件點如果和新建築疊在一起，截圖。〔batch4b〕

## 野松會所（The Nasty Pine，風盔城東）

- [ ] **室外**：Hollyfrost／Hlaalu 農場一帶的建築、圍欄、路沒有和地形打架；Hlaalu 農場那一格 NPC 走路有沒有卡住（已知和 Pride of the Niben 有一塊 navmesh 衝突）。〔batch4b〕
- [ ] **室內**：租床、桑拿自動脫衣的提示是中文；女侍、吟遊詩人的服裝在脖子、手腕、腳踝、腰帶處沒有破洞。〔batch4b〕

## 亨德拉海姆與其他 CC 住宅

- [ ] **Eydvina 的信**：完成同伴團「白銀之手」（加入內環）之前不該收到；完成後換一次地點，信使就會送來。〔batch3〕
- [ ] **新建築大門**：任務前門是鎖的（顯示需要鑰匙、不能撬）；打敗 Eydvina 拿到鑰匙後能開，任務標記指在這扇新門上。門一直打不開的話，停用 `CT15-Hendraheim-DoorLock-Dev-2026-10-10`。〔batch3〕
- [ ] **屋外與隨從**：屋外一圈加上西邊 Lost Valley、北邊龍塚，看有沒有浮空、埋地或 NPC 卡路；名冊「召集」後四名隨從出現（弗雷爾會召喚野豬古利），名字與說明都是中文。〔batch3〕
- [ ] **Bloodchill Manor** 要等黎明守衛「血脈」完成後才收到邀請；**Gallows Hall** 大門在「召喚儀式法術」任務完成前是鎖的，完成後進入就自動解鎖。〔batch3〕

## 靈魂石冢（Soul Tomb，河木外）

- [ ] **傳送畫框**看得到、能傳送、撞上去有碰撞；Boss 戰後的金幣堆能拾取；在人偶、鐘、雕像、屍堆旁近戰 1～2 分鐘不會崩。崩了先照總頁 1e，再看 callstack 有沒有 `hkpCompressedMeshShape`。〔soultomb〕
- [ ] **NPC 不互殺**：入口與沉睡巨人旅店附近誤傷中立 NPC，不會立刻全員敵對；石冢內 NPC 之間不互打。書與通知是中文。〔soultomb〕

## 風暴斗篷軍營（IDE Stormcloaks）

- [ ] **每個軍營多 3 名士兵**，和他們的新對話是簡中字幕。口音像土匪或平民的士兵，內戰台詞要有聲音（Nord 士兵的聲線）；仍然只有字幕的話，記下那句字幕。〔batch3〕
- [ ] **Gray-Mane 與 Galmar**：「失蹤」任務救出 Thorald 後的新流程能走；Galmar 的新對話和原本 RDO／AI Overhaul 的行為並存。〔batch3〕

## 任務板（Missives）

- [ ] 不會派「找車夫／船夫」的信；Tyranus 與 Vigilant Carcette 也仍在禁派清單上。〔batch2〕
