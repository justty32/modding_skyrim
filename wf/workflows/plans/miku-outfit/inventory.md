# 現況盤點：初音那套現在有什麼、缺什麼

[計畫入口](README.md)

依據是 11-25 的原型：素材盤點 [OUTFIT.md](../../../../agentctl/handoffs/home-2026-11-25/miku-face/gpt-nomouse/OUTFIT.md)、試色 [outfit/README](../../../../agentctl/handoffs/home-2026-11-25/miku-face/outfit/README.md)、溢色量測 [COLOR.md](../../../../agentctl/handoffs/home-2026-11-25/miku-face/outfit/COLOR.md)、雙尾與衣服交叉 [hair/phase2](../../../../agentctl/handoffs/home-2026-11-25/miku-face/hair/phase2/README.md)。本檔只整理，不重量。

## 一句話

五件現成服裝能分槽組合，離線試色也做過；但它還不是經典初音。缺無袖剪裁、領帶、成對的紅黑方形髮飾，裙子的短百褶輪廓也沒驗過；而且全都沒在遊戲裡穿過。

## 逐件

已抽到 [pieces.json](data/pieces.json)（11 列：現有 5、缺 3、待驗 1、本計畫補列的缺件 2）。欄位：

- `id`／`part`／`kind`：代號、部位、現有／缺／待驗。
- `editorid`、`armo`、`arma`：ARMO 與 ARMA 的 FormKey（local FormID:plugin）。ARMA 是 `preview.py` 實際讀的那筆。
- `slots`：ARMO 槽位，另記 ARMA 的覆蓋槽。
- `fit`：網格屬於哪種體型（UNP 線索、CBBE 等）。
- `race`：種族涵蓋。
- `color_trial`：試色結果。
- `gaps`：已知缺口。
- `candidates`：備案或補件來源。
- `evidence_path`：出處。

統計：現有五件槽位是 32＋49＋33＋37＋42，ARMO 不重複；缺件兩件找不到現成（領帶、方形髮飾），無袖只能改網格；耳機和左臂 01 是本計畫依官方設定圖補列的，原型文件沒列，要不要做是 D16。

## 種族涵蓋

Chloe 是女性 KuroneNord（`00052A:KuroneSoulTomb.esp`），它的 armor race 是 DefaultRace。五件的人形 ARMA 主種族也都是 DefaultRace，`preview.py` 讀記錄時逐件核過，不合就報錯。所以這五件給 Chloe 穿不靠額外種族清單。沒做的是 `race_gear` 的完整檢查，以及 Ribbon21 同一顆 ARMO 裡的亞龍、虎人分支（它們佔 31／41／43，會碰頭髮）。階段 A 的記錄補丁要過 `race_gear`，見 [recolor.md](recolor.md)。

## 身體與體型

Chloe 的身體是私有 Kurone7 網格，體重 60，沒有 BODYTRI。所以這五件都不會跟著 RaceMenu 身體滑桿變形，OBody 重新指派也會清掉手捏的 morph。上衣自帶 UNP 嵌身 `0HWUNP0` 接替軀幹，Nell 袖套自帶手。離線預覽用 Chloe 皮膚貼圖接縫，遊戲裡的皮膚替換還沒驗。貼合 Kurone7 是階段 M 的工作（[mesh.md](mesh.md)）。

## 試色的結論

- **可以照帶染**：束腰 Corset、裙、靴，帶外都是 0% 或 0.27%。上衣布片 touka 0.36%，也在門檻內。
- **不能照帶染**：Nell 袖套。它的 UV 跟遠端金屬面幾乎全共用（6,709／6,717 texel），定稿只好保留金屬原色。
- **要修過才能染**：Ribbon21 髮帶。初版溢 75.82%，排除共用 texel 後正面帶外歸零，選區保住 71%。
- **共用貼圖不能覆蓋**：袖套借的是原版 `DwarvenShield.dds`，Nell 的袖、鞋、衣也共用它。換色一律寫新路徑，不蓋原檔。

## 跟雙尾的交叉

修正版雙尾（第二輪保留綁點）對五件的非共面三角交叉對：髮帶 367、裙 232、上衣 touka 146、嵌身 80、Corset 25，袖與靴 0。外移 5 單位的試驗能把 touka 降到 8、裙降到 120，但正面輪廓外拱，所以主要候選還是修正版。要歸零得改衣服網格（階段 M4）或接受。這些數字只是表面交叉，不包括動作、物理和透明遮罩。

## 沒驗的

遊戲裡穿著、動作穿模、布料物理、Recorder 靴的 `cynthia_nilfgaard_s.dds` 是否缺件、上衣嵌身缺的 `FemaleBody_0_msn.dds`。這些都排進階段 A 的家裡步驟。
