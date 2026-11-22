# 11-22 agent 替你代驗 WAIT_USER 的結果

你出門時 agent 開遊戲跑了 4 場（S0–S3），全程不存檔。第 5 場（S4）剛開就因額度到上限中止；S4–S7 沒跑。**你的存檔沒被動到**：每場前後 91 個存檔逐檔雜湊相同，三個 ini 也相同。詳細證據見[代驗報告](../../agentctl/handoffs/home-2026-11-22/waituser-runtime/REPORT.md)；截圖在 `agentctl/handoffs/home-2026-11-22/waituser-runtime/shots/`（只在本機）。

## 已替你結案

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

- **CRS 口才提示**：只有你按 E 或滑鼠左鍵選對話才會觸發，agent 做不到。log 那半已過。
- 要開選單的部分（MCM、日誌、技能選單、Estates 畫面、書翻頁、水晶球）。
- 所有身形類項目：要先做 OBody Reset。
- 沒跑的場：S4（10-18 貼圖巡點）、S5／S6（kurone 23 人，身形類要 Reset 後才準）、S7（Baan Malur 渡船、RaceMenu 開啟）。
- 新的取捨：**EngineFixes 三選一**。男體上線後主角也會遇到滑桿失效，見[日後決定](../../wait-user/later-decisions.md)。
- 一句話就能結案的 5 項，見報告「待你一句話確認」。
