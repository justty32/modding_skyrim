# 階段 E 特效：邊光、光源、武器附魔、發光貼圖

[計畫入口](README.md)

特效分兩類。**記錄層**的只寫 ESL，不動網格：EffectShader 邊光、魔法效果的光源、武器附魔光效。**網格層**的要複製 NIF 改 shader：發光貼圖。推薦先做記錄層（D14）。

## 先查的事（E0）

公司看不到遊戲目錄。modlist 裡有 Light and Shade SE 和「No ENB Lights」版的 Strange Runes，像是沒裝 ENB，但沒查證；Community Shaders 有沒有裝也不知道。這兩樣會影響發光與光源看起來的樣子，家裡先查遊戲目錄與 modlist，結論寫回本檔。

## 各項做法

**E2 青綠邊光**：做一個 EFSH（EffectShader），邊緣色青綠、填充透明，掛在一個常駐能力上（SPEL 類型 Ability，裡面一個 MGEF，它的 hit shader 指向這個 EFSH），再把能力給 Chloe。只寫記錄，不動網格。風險是常駐能力讀檔後會不會掉，以及別的 mod 會不會清掉它。

**E3 青綠光源**：MGEF 有光源欄，原版的燭光術就是這樣做的。做法同 E2，不用動網格。要看夜間亮度與半徑。

**E4 武器附魔光效**：給蔥做一個 ENCH，裡面的 MGEF 用青綠附魔 shader。現役有 Equip Enchantment Fix，附魔裝備的光效應該會正常顯示，實機確認。依賴 W4（蔥的 WEAP 先做好）。

**E5 發光貼圖**：讓衣服的青綠邊自己發光。要複製 NIF，在 BSLightingShaderProperty 開 glow map 旗標，第 3 槽（索引 2）放 `_g.dds`，再設 emissive 色。houseCARL `nif_set` 現在只能改節點旗標、縮放、分區、alpha、貼圖路徑，**不能改 shader 旗標與 emissive**，要先擴。`_g.dds` 可以從階段 A 的選區遮罩直接產。這項跟網格階段一起做最省事，因為那時本來就要複製 NIF。

## 要什麼工具

記錄層四種記錄（EFSH、MGEF、SPEL、ENCH）現有寫入器沒有。建在共用庫 `agentctl/tools/lib/espwrite`（[tools-lib-refactor](../tools-lib-refactor/README.md) B4 之後；使用者 2026-11-26 答 Q9 照推薦），不擴 esplib（它只讀），不另起一份。這是 E1，公司就能做，用合成 plugin 先紅後綠。

E5 要擴 houseCARL `nif_set`（C#）加 shader 旗標與 emissive 色兩個操作，照它現有 `set_path` 的寫法與回讀檢查。

## 要使用者授權的

全部只在家：裝層、開遊戲，每次當場說。不用下載，也不用安裝。

## 家裡與公司

| 步驟 | 公司 | 家 |
|---|---|---|
| E0 查 ENB／Community Shaders | 不能 | 能 |
| E1 記錄寫入器 | 能 | — |
| E5 擴 nif_set | 能（合成 NIF） | 真 NIF 跑 |
| E2–E5 做層與實機 | 不能 | 能 |

## 閘門與驗收

1. **離線**：ESL 讀回每筆記錄的欄位（EFSH 顏色、MGEF 的 shader 與光源、SPEL 類型、ENCH 效果）；`check_masters` 沒缺。E5 再用 `nif_inspect` 讀回旗標與第 3 槽。
2. **實機**：
   - E2：截圖看得到邊光；脫戰、讀檔後還在；別的 NPC 沒受影響。
   - E3：夜間截圖有光、不閃。
   - E4：拔出武器有光、收起消失。
   - E5：青綠邊在暗處發光，其他部位不發光。
3. **效能**：同一場景開關特效各看一次 FPS，掉太多就退回。

## 工作量與依賴

E0 半小時；E1 約 1 天；E2 半天；E3、E4 各 2 小時；E5 1–1.5 天。合計約 3 天，加實機。依賴：E2 要 E1 與 I2（Chloe 先穿上）；E4 要 W4；E5 要 E0 與階段 A 的遮罩。task 在 [tasks-later.json](data/tasks-later.json)。

## 不做的

音符粒子、舞台燈這類要做粒子 NIF 的，不在本計畫。要的話另開一題。
