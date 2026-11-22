# 11-22 agent 替你代驗 WAIT_USER 的結果

你出門時 agent 開遊戲跑了 4 場（S0–S3），全程不存檔。第 5 場（S4）剛開就因額度到上限中止；S4–S7 沒跑。**你的存檔沒被動到**：每場前後 91 個存檔逐檔雜湊相同，三個 ini 也相同。詳細證據見[代驗報告](../../agentctl/handoffs/home-2026-11-22/waituser-runtime/REPORT.md)；截圖在 `agentctl/handoffs/home-2026-11-22/waituser-runtime/shots/`（只在本機）。

## 傍晚補跑（runtime-3，S4–S7＋補做項）

agent 又跑了 6 場（B1–B6），一樣全程不存檔；**91 個存檔逐檔雜湊、三個 ini 每場前後都相同**。證據見[報告](../../agentctl/handoffs/home-2026-11-22/runtime-3/REPORT.md)，截圖在 `agentctl/handoffs/home-2026-11-22/runtime-3/shots/`（只在本機）。

- **新問題｜Baan Malur 渡船**：船夫對話、扣 30 金、抵達 `BaanMalur15` 都對，沒被彈回；**但抵達約 1.5 分鐘後遊戲崩潰**（崩在 `EngineFixes.dll` 的記憶體配置器）。請你自己搭一次，看抵達後會不會崩。**現況（傍晚 ferry-repro）**：分析判定不是 EngineFixes 的錯（它是受害者，兇手是某段把堆疊弄歪的程式，log 太短查不出），和「EngineFixes 三選一」無關；agent 同條件重走 3 次、各停 5～7 分鐘，**都沒崩**，目前算偶發。你玩時若卡死，先按 `Ctrl+Shift+F12` 再關遊戲（[報告](../../agentctl/handoffs/home-2026-11-22/ferry-repro/REPORT.md)）。
- **請看一眼｜10-18 貼圖巡點**：6 個室內點沒看到紫色／缺圖（`B2-*`）；Boethiah 神龕、Volkihar 外塔沒拍到。
- **請看一眼｜kurone 23 人**：穿衣全身、卸裝正面／側面、頸部近照（`B6-*`；Jordis、Megara 叫不來）。身形要 Reset 後才準。
- **請看一眼｜CRS 口才**：agent 用真按鍵（E）選了 3 個新話題，CRS 的按鍵處理有跑、log 錯 0；但**你的 CRS 設定是「不顯示訊息」**，所以本來就不會跳提示。要提示就到 MCM 打開。
- **ESL 旗標／RaceMenu**：RaceMenu 開得起來、滑桿能動（換臉那場一口氣調了 100 格）；容器快捷鍵、換裝戒指沒測。
- **無法判定**：VIGILANT 開場任務（日誌裡還沒有，未觸發）；Headhunter 逃犯／竊賊對話（主控台起任務找不到目標人物）。
- **仍沒做**：S8（MCM／日誌截圖場）、S9（Scene ghost）；所有身形類要等你 OBody Reset。

## 已替你結案（中午 S0–S3）

- **NPC Spell Variance KID ini**：log 裡那 8 條規則（含 5 條 Apocalypse）全部生效、0 警告，已從清單刪掉。
- **Headhunter 告示推進**的第 1、2 步：冬堡「殺死強盜」告示殺掉目標後推進到「割下強盜首級」。這項只剩「逃犯／竊賊對話選項」那一步。

## 請看一眼（agent 看到了，結案要你點頭）

- **Apocalypse 四法術**：烈焰冲击／霜冻球／启示录有特效（`S0-30`、`S0-32`、`S0-33`），**火山看不到效果**（`S0-31`、`S0-41`），請實戰放一次火山。
- **RDO**：旅店與衛兵對話中文、賞金數字正常（`S1-crs-dagur-關於-1`、`S1-14-guard-b`）。
- **cow 學院指南牌**：內容中文，但樓層寫「一楼／二楼」，和清單寫的「楼上／一楼／地下层」不同（`S1/signs.json`）。
- **VIGILANT／GLENMORIL 女裝 5 件**：穿上都看得到、名稱對（`S2-faralda-*-front`）。貼身與否要 Reset 後看。
- **Radiant Bow**：書名、弓、箭名中文，召得出來（`S3-bow-summoned`）。
- **Falkreath Shop**：讀檔不崩，索拉夫對話中文（`S3-solaf-1b`）。
- **VIGILANT 阿爾塔諾**：對話正體（`S3-altano-1b`）。他在**晨星城**風岳客棧，不是 Morthal。

## 有問題

- 沒有確定的 FAIL。待確認的有兩件：火山沒有可見效果；VIGILANT 開場任務在 37 級仍停在 stage 0、日誌看不到。

## 仍要你本人

- **CRS 口才提示**：傍晚已用真按鍵代驗按鍵處理有跑；提示被你的 MCM「不顯示訊息」關掉（見上）。
- 要開選單的部分（MCM、日誌、技能選單、Estates 畫面、書翻頁、水晶球）。
- 所有身形類項目：要先做 OBody Reset。
- 新的取捨：**EngineFixes 三選一**。男體上線後主角也可能遇到滑桿失效，見[日後決定](../../wait-user/later-decisions.md)。**現況**：「拉一兩次就失效」是 EngineFixes 6.x 時代的說法，現行 7.0.20 還沒驗證；agent 排的 1 分鐘滑桿實測因你回來、鍵鼠交還而沒做。建議仍是先 (a) 不改，等實測。
- 一句話就能結案的 5 項，見報告「待你一句話確認」。
