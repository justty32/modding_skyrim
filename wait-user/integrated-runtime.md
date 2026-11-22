# 整包 UI／中文／任務驗收

## Auri＋現役 VIGILANT 有限解凍整合

內容見 [new-game-followers.md](integrated-runtime/new-game-followers.md)。

## DMK 中文層 smoke 以標準 baseline save 重跑

內容見 [dmk-gameplay.md](integrated-runtime/dmk-gameplay.md)。

## Modpack-KR Batch 6 final gameplay

內容見 [dmk-gameplay.md](integrated-runtime/dmk-gameplay.md)。

## 四個首次生效中文層 → 現在只剩兩個（2026-09-05 核對）

內容見 [localization-checks.md](integrated-runtime/localization-checks.md)。

## RDO 中文層（62500／76474 已落地，待進遊戲抽查）

內容見 [localization-checks.md](integrated-runtime/localization-checks.md)。

## VIGILANT 1.8.2 正體中文

內容見 [quests-npc-text.md](integrated-runtime/quests-npc-text.md)。

## 2026-08-20 任務內容批

內容見 [quests-npc-text.md](integrated-runtime/quests-npc-text.md)。

## cow 中文層人眼抽查（2026-10-26 立）

cow 學院中文層（profiles `93261f4`）已部署、煙霧通過，剩人眼：在學院裡看有沒有方框字、截斷。

1. 成就大厅／智慧大厅／面容之殿門口的「指南」牌：樓層分「楼上／一楼／地下层」，房間名照 Alias 帶出。
2. 首席法師房間水晶球選單：六鈕依序「植物园／议会厅／温泉／办公室／档案室／无」；選「档案室」應真的變成檔案室布置。
3. 《泰姆瑞尔智识：修订版》翻到第 7 頁以後（原本是英文）。

agent 2026-11-22 已觀測：三塊指南牌的內容全是中文（唯一的英文「Alloef」是你的角色名），但樓層寫的是「一楼／二楼」、列的是各樓的人，和上面第 1 點寫的「楼上／一楼／地下层」不一樣；書名「泰姆瑞尔智识：修订版」正常。水晶球 agent 叫不出選單、書 agent 翻不了頁，第 2、3 點仍要你看。牌子全文在 `agentctl/handoffs/home-2026-11-22/waituser-runtime/S1/signs.json`——請看一眼第 1 點算不算過。

內容取自 `agentctl/handoffs/home-2026-10-26/cowzh/REPORT.md`（已刪）「給使用者的人眼抽查」。

## 四 mod 與 Ambriel 外觀的自然遊玩驗證（2026-11-01 立）

自然遊玩時抽查 Eilgird／Lenora 隨從對話、Paths 實際技能樹，以及原存檔 Ambriel 外觀快取與自然劇情人形／龍變身往返。Paths 技能效果、解鎖條件及自動施展說明請確認換行、右邊不超框、下方不重疊；r4 已部署但尚未實機驗收，見 Paths 斷詞部署紀錄（已刪：`agentctl/handoffs/home-2026-11-01/paths-wrap/REPORT.md`）。兩個新生人形膚色、Paths 空面板中文、Estates 中文 UI 與反射 UI 已驗收；這些不代表上述自然遊玩項已通過。見 部署驗證（已刪：`agentctl/handoffs/home-2026-11-01/wanted/INSTALL-QA.md`）。

## Apocalypse 換 10.2.3 中文層後實機驗收（2026-11-22 立）

`modpack-main` 已把 Apocalypse 中文層換成 10.2.3 底版（`Apocalypse-Magic-of-Skyrim-10.2.3-Chinese-Rebuilt-Dev-2026-09-25`），Ordinator 補丁換回 10.0.2；靜態驗證全綠，剩實機。

1. 開遊戲到主選單、讀檔後退出，告訴 agent 一聲；agent 會查 `Papyrus.0.log` 裡 `Cannot open store for class "WB_` 是不是 0 筆（原本每次 69 筆）。
2. 主控台 `player.addspell <前綴>02E0C0`（烈焰冲击）、`<前綴>04733C`（火山）、`<前綴>020A58`（霜冻球）、`<前綴>023316`（启示录），各放一次：要有實際效果，不能只有施法動畫。後六碼是 `Apocalypse - Magic of Skyrim.esp` 的本地 ID；前兩碼是它當下的載入序位置，2026-11-22 是 `6A`（原寫 `69`，當天新增 plugin 後位移），之後再變就用 `whichmod.py <EDID>` 或 `whichmod.py "Apocalypse - Magic of Skyrim.esp"` 查。
3. 讀舊存檔：看技能選單裡原本學過的 Apocalypse 法術還在不在、名字有沒有方框字。9.45 才有的約 465 筆會消失，要重學的請記下來。

agent 2026-11-22 已觀測：第 1 步 log 已過（`WB_` store 錯 0，兩場新窗）；第 2 步 4 支都學得到、中文名正常，用 `player.cast` 對外景空地施放，烈焰冲击／霜冻球／启示录有明顯特效，**火山兩次都看不到效果**，傷害沒量到（靶沒被打中）。截圖 `agentctl/handoffs/home-2026-11-22/waituser-runtime/shots/S0-30…S0-33`、`S0-41`——請看一眼確認，並實戰放一次火山；第 3 步（技能選單）agent 開不了選單，仍要你看。

依據與回退：`agentctl/handoffs/home-2026-11-22/apocalypse-swap/REPORT.md`。

## VIGILANT 開場任務中文抽查（2026-11-22 立）

`modpack-main` 已在 `VIGILANT - Delayed Start-57961-2.3` 上方加了繁中補完層，把被 Delayed Start 蓋回英文的開場任務名與 5 條目標換回中文；靜態驗證全綠，剩人眼。等級到門檻（Delayed Start 設定 25 級）、VIGILANT 開場任務啟動後，打開任務日誌：

1. 任務名要是「斯丹達爾的警戒者」，不是 "Vigilant of Stendarr"。
2. 目標依進度依序是「加入斯丹達爾的警戒者」「跟隨阿爾塔諾或在斯丹達爾神殿與他會合」「與阿爾塔諾交談」「與索隆迪爾交談」；看有沒有方框字或截斷。
3. 任務照常會在 25 級觸發（本層沒動觸發條件，觸發不了就回報，那是別的問題）。

agent 2026-11-22 已觀測：讀 Save342（37 級）時開場任務 `zzzAoMMq00` 已在跑但停在 stage 0，任務日誌裡還看不到它，所以中文字串沒法在遊戲裡看；離線讀到的任務名是「斯丹達爾的警戒者」。37 級還停在 stage 0 是否正常（Delayed Start 可能還有其他條件）未查——你遇到它跳出來時再看日誌。

agent 2026-11-22 下午（runtime-3）用真按鍵打開任務日誌、捲完整個進行中清單：沒有這個任務（同上，還沒觸發），仍無法判定。

依據與回退見[施工報告](../agentctl/handoffs/home-2026-11-22/small-fixes/REPORT.md)。

## Headhunter 的 Missives 討伐告示能推進（2026-11-22 立）

`modpack-main` 已在 `Headhunter - Bounties Redone 1.61-ZH-2026-09-11` 上方補了 `Headhunter - Missives Extension Scripts 1.61`：當初裝 Missives 補丁選項時只裝了 esp、漏了同包的 6 支腳本，所以 Headhunter 加進 Missives 告示板的討伐任務殺了目標也不會推進。靜態驗證全綠，剩實機；舊存檔不用清。

agent 2026-11-22 已代驗通過原本的第 1、2 步（log 的 `_CTB_` store 錯 0；冬堡「殺死強盜」告示任務殺掉目標後 10 秒內推進到「割下強盜首級」），見[代驗報告](../agentctl/handoffs/home-2026-11-22/waituser-runtime/REPORT.md)。只剩：

1. 順路：Headhunter 的逃犯／竊賊對話選項（說服、威嚇、跟我走、開打）選了要有效果。

   agent 2026-11-22 下午（runtime-3）試過：主控台起「追蹤逃犯」任務起不來（別名填不上）；「追蹤竊賊」起得來、設到 stage 20，但沒有任務目標可傳送過去，找不到竊賊本人，無法判定。

依據與回退見[施工報告](../agentctl/handoffs/home-2026-11-22/headhunter-fix/REPORT.md)。
