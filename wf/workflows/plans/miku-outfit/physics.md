# 階段 P 物理：雙尾、裙、緞帶

[計畫入口](README.md)

## 現役裝了什麼

`instance/profiles/modpack-main/modlist.txt` 唯讀查（2026-11-26，公司）：

- **有**：`Faster-HDT-SMP-4.1.1-AVX2`（FSMP，2026-09-05 啟用）、`XP32 Maximum Skeleton Special Extended`、`KS Hairdos SSE 1.10`。
- **沒有**：CBPC。modlist 裡沒有任何 CBPC 或 CBP 開頭的 mod。

舊文件說本機沒有物理框架，例如 voiced-follower-overhaul 的 assets-inventory 與 look-transplant METHOD，那是 2026-09 初的狀態，已經過時。

雙尾用的 Parody 來自 KS Hairdos SSE 1.10，這是靜態版。物理版是另一個 mod：KS Hairdos - HDT SMP（Physics），Nexus 31300。所以現在的雙尾不會飄。Parody 的 NIF 裡有沒有 HDT 物理 block，回家查（P0）。

## 推薦：只用 FSMP，不另裝 CBPC

FSMP 已經在，髮、裙、緞帶都能用它的 XML 骨鏈做。CBPC 主要做身體彈性，跟本題無關，多裝一個只是多一個衝突來源（D13）。

## 各項做法

**P1 雙尾**有兩條路（D12）：

- **(a) 下載 KS Hairdos - HDT SMP（31300）**：先在頁面確認它有沒有 Parody。有的話，比對頂點數是不是同為 9,480、拓撲相同。相同才能沿用我們的 sculpt 位移（雙尾加長、收窄都記在 RaceMenu 的 sculpt host 上，是逐頂點的）。不同就不能用，sculpt 要重做。
- **(b) 自己做**：Outfit Studio 6.2 的 MCP 有 `make_physics_chains`、`write_physics_xml`、`simulate_physics`。在現有 Parody 上加骨鏈與權重，寫 SMP XML。要 D1。

推薦先查 (a)，一頁就能知道答案；不合才走 (b)。

**P2 身體碰撞**：SMP 的頭髮、裙要跟身體碰撞，才不會穿過去。Chloe 的身體是私有 Kurone7，沒有附 SMP 碰撞設定，要在 XML 裡補身體的碰撞形狀（膠囊或球），對齊 XPMSSE 的骨頭。

**P3 裙**：Sela 裙現在只綁身體骨，要加骨鏈與權重，再寫 XML。走、跑、坐下最容易爆，實機要三種姿勢都看。它依賴 M3（先貼合 Kurone7），否則物理會從錯的位置開始算。

**P4 緞帶**：Ribbon21 的尾端加短骨鏈；或改用 Wa Ribbon - SMP（Nexus 21281，和風緞帶，已帶 SMP，授權未查）。方形髮飾是硬的，不加物理。

## 要什麼工具

- **Outfit Studio 6.2 MCP**：(b)、P3、P4 都要，見 [mesh.md](mesh.md)。
- **FSMP 的驗證工具**：FSMP wiki 有 SMP 作者指南與 `smp_report` 驗證頁（github.com/DaymareOn/hdtSMP64/wiki），施工前先讀。
- **量測**：沿用 `surface_audit.py` 量靜態交叉。動態只能實機看。

## 要使用者授權的

- (a)：家裡下載 31300（nxm，要使用者點頭）。
- (b)、P3、P4：D1。
- 每次裝層、開遊戲：當場說。

## 家裡與公司

公司幾乎做不了：看不到 NIF、裝不了 Outfit Studio、沒有遊戲。公司能做的只有讀 FSMP wiki、先寫 XML 範本與它的格式檢查（合成測試）。其餘全在家。

## 閘門與驗收

1. **P0**：SKSE 日誌有 FSMP 初始化；Parody 有沒有 HDT block 寫進本檔。
2. **離線**：XML 解析得回，骨名在 NIF 裡都找得到；靜態交叉對不比階段 M 結束時多。
3. **實機**：站、走、跑、跳、坐下、轉身各看一次。雙尾不爆、不穿肩、不卡進身體，裙不穿腿，讀檔後物理還在。FPS 掉太多就退回靜態。

## 工作量與依賴

P0 半小時；P1 走 (a) 約 1 天，走 (b) 2–3 天；P2 1 天；P3 2 天；P4 半天。合計約 5–7 天，加實機。依賴：P1 要 P0，再加 D1 或下載授權；P2 要 P1；P3 要 M3 與 P2；P4 要 P1。task 在 [tasks-later.json](data/tasks-later.json)。

## 風險

- 換成 SMP 版髮型，HDPT 與 NIF 都會換。已實拍的 H6 外觀要重拍確認。
- FSMP 的 XML 對骨名大小寫敏感。XPMSSE 的骨名要逐一對。
- 物理參數沒有對錯，只有好不好看。阻尼、重力、碰撞半徑要給使用者看實機影片，由使用者挑。
