# 隨從可選工作（2026-11-02）

[使用者頁面索引](README.md)

目前先挑下面五位。這是點名用的候選清單，尚未開始修補，也未新增 WAIT 項目。選定後先重核現役來源、實際生效檔案與後續 Paths 改動，再確認施工範圍。

## 優先五位

- **Secunda**：等級倍率 ×10；可選改 ×1。屬平衡選擇，未證作者寫錯。
- **Cheryl**：作者衣物在背包、預設為學院長袍；先看實穿，再決定是否設成作者衣物。
- **Sela**：作者衣物在背包、預設為農夫衣；同樣先看實穿。
- **Fastred**：作者設定等級上限 40；可選取消上限，屬強化選擇。
- **Rosetta**：可選加入水系法術，配合水系定位；屬主題整合。

依據 [F4 調查](../../agentctl/handoffs/home-2026-10-26/vfstats/REPORT.md) 第 16–22 行。Cheryl、Sela 尚未證實現役實穿錯誤；這五項均不能直接當已確認故障。

## 其他可點名方向

**資產診斷：Recorder**。兩組大小寫同名 facegen 的內容不同；先查來源、雜湊與實際生效檔案，不先刪併。Cheryl 同包另有九張大小寫不同的身體貼圖，選她時可一併唯讀核對，尚未證實皮膚故障。見 [現役狀態](../../agentctl/SESSION-LOG.md) 及 [ESL 調查範圍外發現](../../agentctl/handoffs/home-2026-10-26/eslifierpoc/REPORT.md)。

**既有驗收：Melana、Auri、Eilgird、Lenora、Ambriel**。分別是 reset 讀回／存讀持久性、招募跟隨與 VIGILANT commentary、兩位的自然對話、Ambriel 原存檔外觀快取與自然變身。沒有因此新增施工；Auri 既有驗收範圍不變。見 [Melana 紀錄](../../agentctl/handoffs/home-2026-11-01/melana-style-reset/REPORT.md)、[隨從整合驗收](../../wait-user/integrated-runtime/new-game-followers.md) 與 [自然遊玩驗收](../../wait-user/integrated-runtime.md)。

**定位／平衡次選：Aniya、Morgaine、聖城三位**。Aniya 可選治療 class；Morgaine 可選改成跟玩家等級；維耶魯希娜、莉特莉娜、伊露妮娜先查自訂腳本與來源，再談等級調整。原調查皆建議保留，並非故障。

**外觀偏好：Elli、Luckyirnsvar**。尚未點名換臉，要做需指定素材配對；見 [外觀待選](../../modpack-design/content-plan/followers/OPEN.md)。

**遊戲內給裝備：Ambriel、Altair、Bikhai、Nanak、Sariq、Makara、Malryn**。優先用本人自帶換裝／教學系統，通常不需工程。

## 已結案或本輪暫緩

Remiel 合併層已修、部署且實機確認，另兩件怪事也已裁示不追（[修復](../../agentctl/handoffs/home-2026-10-26/remiel/REPORT.md)、[裁示](../../agentctl/handoffs/home-2026-10-26/decide1026/REPORT.md)）。Varinia 原收拔問題已確認解決，另版 source 候選不代表原症狀未修（[11-02 狀態](../../agentctl/handoffs/home-2026-11-02/STATE.md)）。Camilla 已依後續裁示完成風格指令，本案結束；只有另行選定才確認風格行為／持久性，裝備不是未完成項（[原報末段](../../agentctl/handoffs/home-2026-11-01/camilla-single/REPORT.md)）。

本輪不新增 Sofia 短場景工作，既有驗收範圍不變。Aniya 已完成的身體／裝備與黑名單修補不重開；Rigmor 已停用，不能沿舊表再開工程。

## 資料與舊頁

詳細內容在 [候選及排除資料](2026-11-02-follower-options.json)（29 列；每列是一項選擇或排除狀態，Ambriel 跨類別出現，並非 29 人）。

欄位：`id`／`name` 識別選項；`category` 分類；`finding` 發現；`option` 可選方向；`certainty` 確定度；`home_check` 家中重核需求；`status` 當前狀態；`source_path` 來源連結；`source_locator` 行號或原表姓名。

[59 人能力裝備舊頁](2026-10-26-follower-stats-gear.md) 是 10-26 調查快照，Remiel 卡片仍是修前資料；其他五位以本頁的平衡／偏好／待核界線為準。另有 [外觀頁入口](2026-10-26-follower-look-pages.md)。本頁未更動原審批表或既有驗收項。
