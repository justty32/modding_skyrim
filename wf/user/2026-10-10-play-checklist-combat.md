# 10-10 檢查清單：戰鬥與系統

[回總頁](2026-10-10-play-checklist.md)｜〔〕是 `agentctl/handoffs/2026-10-10/` 下的報告目錄。崩潰的處理方式一律照總頁 1e。

## 敵人數量（Dynamic Enemy Spawns）

- [ ] **帶 2 個隨從**進一個有敵人的洞穴（例如 Embershard Mine），敵人大約多 50%；**單人**進同類地點，敵人數和原本一樣。離開再回來，複製出來的敵人都會消失。〔hide-in-bushes〕
  - **agent 10-10 實機**：agent 驗不了，留給你（log 顯示 followerMultiplier=1.25，和「約多 50%」一致）。〔ingame-test〕
- [ ] **屍體**：複製敵人的屍體可以搜刮，**不要往裡面放東西**（放了那具屍體會永久寫進存檔）。F1 選單裡有 `Dynamic Enemy Spawns SKSE` 頁；自訂隨從沒被算進去時，在 Force Counted Followers 加上名字。〔hide-in-bushes〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 敵人打法（SkyTactics、NPC Spell Variance）

- [ ] **強盜營地與屍鬼墓各打一輪**：同一種敵人的不同個體打法不同（有人貼身壓迫、有人退後拉弓、Boss 換風格）。平常帶的隨從打法應該不變（用 NFF 收的普通 NPC 擋不到，例外）。〔batch4b〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **打一場有法師的仗**（死靈法師據點、法師巢）：法師會換招、補血、上結界或斗篷。崩潰且 crash log 點名 `NPCSpellVariance.dll` 或 `spellcastingreworked.dll` 時，停用 `NPC Spell Variance-132097-2.7.2`。〔batch4b〕
  - **agent 10-10 實機**：agent 驗不了，留給你（NPCSpellVariance 載入正常）。〔ingame-test〕

## 結界（Perfectly Valid Wards）

- [ ] **架結界各擋一次**：近戰（含強力攻擊，應該把攻擊者彈開）、箭、龍吼。擋近戰或箭時 HUD 有結界能量條，也會給恢復系經驗。擋完看 skse64.log 和 PVW 自己的 log，確認沒有新的 crash log。〔batch2〕
  - **agent 10-10 實機**：agent 驗不了，留給你（PVW log 的 hook 都裝上了）。〔ingame-test〕
- [ ] **法術反彈已關**：敵方法師開結界時，你的法術不會被彈回；你的結界也不會反彈敵人的法術。〔batch2〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 硬直與閃避

- [ ] **Modern Stagger Lock**：打人形敵人（強盜），硬直動畫正常、**不會卡在原地**，連擊可以接硬直。屍鬼和法爾默不受 MSL 影響（Pandora 的限制，預期如此）。〔batch-uc-has-bcd〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **Dynamic Dodge Shot**：拉弓時往左、右、後移動再按右鍵。弓術 45 以下是 Kratos 式閃避（不能射）；45 以上、沒穿重甲是原版閃避射擊；穿重甲且條件達標是 Infinity 式閃避。原地或往前按右鍵是瞄準縮放。出現 T-pose 的話先看 OAR log 再回報。〔batch2〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 飛刀（Glenmoril）

- [ ] 飛刀名稱是中文；左右手都能裝、各有投擲動作；寒冷飛刀多一個冰霜效果，萎靡之毒多一個毒傷。〔batch2〕
  - **agent 10-10 實機**：agent 部分驗過：四種飛刀名稱都是中文；投擲和效果留給你。〔ingame-test〕

## 熔煉、訓練、撿雜物

- [ ] **熔爐**：多出很多「熔回錠／原料」的配方，身上正裝備的物品不會出現在清單裡。熔煉也會給鍛造經驗，留意練功速度。Smelting Plus 的說明信台詞是中文，信件內文與任務目標是英文（已知）。〔batch2〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **訓練不限次數**：同一個等級內找同一位訓練師連續訓練超過 5 次；主控台 `getgs iTrainingNumAllowedPerLevel` 應回 1800。〔unlimited-training〕
  - **agent 10-10 實機**：agent 已驗 OK：`getgs iTrainingNumAllowedPerLevel` 回 1800；連續訓練留給你。〔ingame-test〕
- [ ] **Unlootable Clutter**：同一種雜物撿過一個，第二個就沒有「拿取」提示；銀器和矮人器每件都撿得到。Shift+K 切換開關（右上角顯示 ON／OFF）；和別的鍵衝突就告訴線改熱鍵。〔batch-uc-has-bcd〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 家裡自動整理（Home Auto Sort）與 F1 選單

- [ ] **F1 → Home Auto Sort 頁**：容器名、地名等中文不是方塊字，其他頁照常。〔batch-uc-has-bcd〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕
- [ ] **SkyPrompt**：第一次進遊戲會跳教學；設好主箱子後看著它，會出現 T（收納）／G（補給）提示，長按有效。〔batch-uc-has-bcd〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## 車夫與船夫（Better Carriage Destinations）

- [ ] **CFTO 車站與渡船**（例如 Heljarchen、Dawnstar 渡船）：都改成 BCD 的對話與車資，CFTO 原本的目的地清單不再出現（設計如此）。**冬堡車站**和**龍橋渡船**也要能選目的地。MCM 的「更好的运输目的地」頁是中文。〔batch-uc-has-bcd〕
  - **agent 10-10 實機**：agent 部分驗過：白漫車夫只剩 BCD 那條對話；其他車站和 MCM 留給你。〔ingame-test〕
- [ ] **Granite Hill 自宅車夫**：原本的搭車選單被 BCD 取代，改用地圖選 Granite Hill，要能到達。到不了就回報（這是已接受的風險）。〔batch-uc-has-bcd〕
  - **agent 10-10 實機**：agent 驗不了，留給你。〔ingame-test〕

## Unslaad 武器的新動作（Animated Armoury Unslaad Patch）

- [ ] **Unslaad 的太刀、薙刀、長槍類武器換成新動作**：拿到其中任何一把裝備起來看揮法（物品欄顯示的是簡中名）。阿卡维尔大太刀、阿卡维尔剑、刀锋卫士之剑、戴尔芬的誓剑→太刀揮法；阿卡维尔薙刀、白霜之镰→戟的揮法；阿尔凯瑞之矛、短穆特拉、银钥匙剑→細劍揮法；阿尔凯瑞巨矛、穆特拉、银钥匙巨剑、贵族巨剑→長槍揮法。名稱不是方塊字。揮法沒變就回報。〔m159159〕
- [ ] **注意**：阿爾凱瑞之矛（單手）、短穆特拉原本算「錘」，現在算「劍」；雙手版（阿尔凯瑞巨矛、穆特拉）原本算「戰錘」，現在算「巨劍」。吃的天賦會跟著換（例如錘的破甲變成劍的流血、戰錘的破甲變成巨劍的暴擊），這是補丁設計如此。〔m159159〕
