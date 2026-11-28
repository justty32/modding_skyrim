# 整包 UI／中文／任務驗收

## Auri＋現役 VIGILANT 有限解凍整合

內容見 [new-game-followers.md](integrated-runtime/new-game-followers.md)。

## DMK 中文層 smoke 以標準 baseline save 重跑

內容見 [dmk-gameplay.md](integrated-runtime/dmk-gameplay.md)。

## 四個首次生效中文層 → 現在只剩兩個（2026-09-05 核對）

內容見 [localization-checks.md](integrated-runtime/localization-checks.md)。

## 2026-08-20 任務內容批

內容見 [quests-npc-text.md](integrated-runtime/quests-npc-text.md)。

## 四 mod 與 Ambriel 外觀的自然遊玩驗證（2026-11-01 立）

自然遊玩時抽查 Eilgird／Lenora 隨從對話、Paths 實際技能樹，以及原存檔 Ambriel 外觀快取與自然劇情人形／龍變身往返。Paths 技能效果、解鎖條件及自動施展說明請確認換行、右邊不超框、下方不重疊；r4 已部署但尚未實機驗收，見 Paths 斷詞部署紀錄（已刪：`agentctl/handoffs/home-2026-11-01/paths-wrap/REPORT.md`）。兩個新生人形膚色、Paths 空面板中文、Estates 中文 UI 與反射 UI 已驗收；這些不代表上述自然遊玩項已通過。見 部署驗證（已刪：`agentctl/handoffs/home-2026-11-01/wanted/INSTALL-QA.md`）。

## 冬堡學院：Midden01 的 Summerset Isle Assault 通道（2026-11-23）

只有靜態證據：Summerset Isle Assault 在 Midden01 停用原版牆開的通道，被組合補丁蓋回 JK's 版本、JK's 在同座標有自己的牆，等於封回去；它的 navmesh 改動也被組合補丁蓋掉。要實機看傳送門走不走得到（玩家與隨從，有沒有穿牆或擋路）。真的被擋才談修（要動 profile、要使用者同意）。見 [REPORT](../agentctl/handoffs/home-2026-11-23/winterhold-conflicts/REPORT.md)。

## 冬堡學院：Midden 調查書是不是紫色（2026-11-23）

只有靜態證據：Finding Velehk Sain 把 `dunMiddenInvestigationBook` 的模型換成 `BCSSEJournal.nif`，它要的 `JournalAdmonition.dds` 與 `_n.dds` 全機找不到。要實機看 Midden 那本書的貼圖。見 [REPORT](../agentctl/handoffs/home-2026-11-23/winterhold-conflicts/REPORT.md)。

- 代驗 2026-11-28：無法代驗——書頁（閱讀畫面）中文正常，但世界裡那本書的 3D 模型拍不到（第三人稱鏡頭與隨從擋住，送不了視角輸入）（見 agentctl/handoffs/home-2026-11-28/rt-proxy/REPORT.md）

## 冬堡學院：外景冰柱、冰板的貼圖（2026-11-23）

只有靜態證據：Icy Mesh Remaster 要的 `textures/landscape/ENV_I.dds`、`ENV_G.dds` 全機找不到，影響不只學院。要實機看學院外景冰柱、冰板。見 [REPORT](../agentctl/handoffs/home-2026-11-23/winterhold-conflicts/REPORT.md)。

- 代驗 2026-11-28：PASS（冰柱）——學院中庭截圖可見的冰柱、冰簷正常白色、沒有紫色；冰板沒特別找到（見 agentctl/handoffs/home-2026-11-28/rt-proxy/REPORT.md）

## Vaelyra 中文抽查（2026-11-26）

找 Vaelyra 對話，確認問候、跟隨選項和閒聊字幕沒有方框、截斷或亂碼；請她唸一本書並選「繼續」數輪，確認字幕中文。物品欄打開《雪中燈火》看書頁；MCM 的「隨從／女巫面相／書籍」三頁都要有內容，舊存檔選單名稱仍為英文是預期。不對請回報句子或頁面與截圖。[REPORT](../agentctl/handoffs/home-2026-11-26/vaelyra-zh/REPORT.md)

- 代驗 2026-11-28：PASS（部分）——問候、閒聊字幕與隨從選單 7 項繁中、無方框無截斷，《雪中燈火》物品名中文；唸書（好感門檻未到）、書頁、MCM 三頁無法代驗（見 agentctl/handoffs/home-2026-11-28/rt-proxy/REPORT.md）

## Vaelyra 相容修正實機抽查（2026-11-26）

到金丘農場看工棚名稱「金丘農場工棚」、農舍名稱「金丘農園」及光照；到沉睡巨人旅店確認沒有多出的灰塵光束。Feris 的 OBody 項另見換臉清單。不對請回報地點及截圖。[REPORT](../agentctl/handoffs/home-2026-11-26/vaelyra-fix/REPORT.md)

- 代驗 2026-11-28：PASS（部分）——旅店灰塵光束那筆 GetDisabled=1（對照組薇萊拉=0），工棚、農舍室內光照截圖正常；門上名稱拍不到（鏡頭被隨從擋），無法代驗（見 agentctl/handoffs/home-2026-11-28/rt-proxy/REPORT.md）

## OBody 全域重置（2026-11-26）

先保留重置前存檔，因舊分配值只能從該存檔找回。到空室內開 OBody MCM，關閉 ORefit 和兩個 randomization，執行 `Reset all distributed presets`；男女都會重置，約 930 名男性舊隨機 HIMBO 值也會清成零形。另存新檔、退出遊戲重開並讀新檔，看卡蘿塔等路人女 NPC 是否回到 BSO Neutral；Sofia、Lydia 若仍不對，再選中個別執行 `Reset this actor`。不對請回報人物與重置後畫面。[REPORT](../agentctl/handoffs/home-2026-11-26/obody-ct77fix/REPORT.md)

## Frozen in Time 0.30 實機抽查（2026-11-27）

野外遭死靈術士「奪體者」襲擊後，撿《賈納夫的日記》，看任務日誌、目標及手寫書是否中文且無方框；在黑境營地看《人造雪精靈配方》內頁、召喚法陣與身體部位名稱。復活雪精靈後選命名對話，確認文字框顯示中文、可輸入英文名，召喚法術名為「召喚＋名字」；字幕應對得上語音。《普尼艾備忘錄》第一頁法莫符文保留原文、第二頁中文。看鍛莫機巧盒／儲藏盒說明是否中文無亂碼，並到索瑟海姆默斯靈峰北邊遺跡外圍看 ULP 與 FiT 物件有無重疊。不要用 AFT／NFF 收她，使用她自己的對話系統。異常回報場景及截圖。[REPORT](../agentctl/handoffs/home-2026-11-27/fit-030/REPORT.md)

- 代驗 2026-11-28：PASS（部分）——《人造雪精靈配方》內頁手寫中文無方框，四本書物品名中文；劇情（奪體者、命名、日誌、法陣、ULP 重疊）沒到，其餘無法代驗（見 agentctl/handoffs/home-2026-11-28/rt-proxy/REPORT.md）

## Taeka 1.2.1 實機抽查（2026-11-27）

在冬堡冻炉客栈找迭卡，確認衣服沒有穿模。對話字幕、玩家選項應為簡中且不截斷；試「叫我……」稱呼請求，配方及帽子效果通知應為中文。物品欄打開《奶奶的来信》《66号订单》看手寫中文無方框，晚餐任務日誌與目標也應中文。第一輪以外的通知要等 r2 裝好才翻譯；異常回報文字、場景及截圖。[REPORT](../agentctl/handoffs/home-2026-11-27/taeka/REPORT.md)

- 代驗 2026-11-28：PASS（部分）——開場 6 輪與隨從選單 16 項簡中不截斷，《奶奶的来信》《66号订单》手寫中文無方框，「叫我的名字吧」通知中文；衣服穿模無法代驗（舊存檔一張截圖疑似只戴帽子，見 REPORT），配方／帽子通知、晚餐日誌沒到（見 agentctl/handoffs/home-2026-11-28/rt-proxy/REPORT.md）

## Taeka r2 通知與技能抽查（2026-11-27）

r2 報告只到 staging，待部署後再驗。跟迭卡說「叫我的名字吧」選杰森等名字，看右上中文通知無方框或截斷；晚餐任務攪鍋、採蜂蜜、拿胡蘿蔔、打水時看通知中文。喝愛情藥水或慢燉燉菜後，確認通知中文且口才／毀滅／幻術技能照樣 +1。不對回報動作、通知及技能變化。[REPORT](../agentctl/handoffs/home-2026-11-27/taeka-pex2/REPORT.md)

- 代驗 2026-11-28：PASS（部分）——「叫我的名字吧」選杰森，左上通知「迭卡会记住的。」（r2 的 lwbJasonON.pex 譯文）無方框無截斷；晚餐任務四個動作、愛情藥水／燉菜的技能 +1 沒做到，無法代驗（見 agentctl/handoffs/home-2026-11-28/rt-proxy/REPORT.md）
