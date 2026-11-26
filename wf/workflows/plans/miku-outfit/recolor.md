# 階段 A 換色與記錄補丁、階段 I 整套穿上

[計畫入口](README.md)｜盤點 [inventory.md](inventory.md)

## 用什麼工具

換色與記錄補丁都用 outfit-tools 線在做的 `agentctl/tools/outfit/`（[BRIEF](../../../../agentctl/handoffs/home-2026-11-26/outfit-tools/BRIEF.md)）。本計畫只給規格，不重設計工具。它的輸入是 NIF、原 DDS 加一份選區規格（哪個 shape、UV 帶或遮罩圖、目標色、保護明暗與 alpha），輸出無損 RGBA8 DDS，內建溢色閘門。記錄補丁從配對規格產一顆 ESL：複製 ARMO 與 ARMA 成新 EDID，貼圖改指換色 DDS，WEAP 也走同一套。

貼圖是走 ARMA 替代貼圖（不動 NIF），還是複製 NIF 改路徑，由那條線比較後寫在它的 README。本計畫兩條都能接。不過特效的發光貼圖（E5）和武器（W3）本來就要複製 NIF，所以這兩件不管它選哪條，都要用到「複製 NIF 改路徑」的能力。

## 換色規格草案

已抽到 [recolor.json](data/recolor.json)（7 列，對五件的七個 shape）。欄位：

- `id`／`piece`／`shape`：代號、哪件、NIF 裡的 shape 名。
- `source_dds`、`native`：原貼圖路徑與原解析度。
- `method`：UV 帶、整張、UV 帶＋repair、不染。
- `z_bands`：選區高度帶（原 NIF 綁定空間，體重 60）。
- `target`：目標顏色與可選的主片改色。
- `measured`：11-25 量到的帶內、帶外比例。
- `handling`：溢色風險怎麼處理。
- `decision`：要使用者答的題號。

統計：照帶做 4 個 shape，整張改 1 個（袖套），要 repair 1 個（髮帶），不染 1 個（上衣嵌身皮膚）。

## 顏色怎麼上

沿用原型的做法（`outfit/preview.py:128`）：選區先轉灰階，再映到三點色階——暗 `#083639`、中 `#39C5BB`、亮 `#94EEE0`，中點 132。這樣原貼圖的明暗紋理會留著，alpha 原封不動。D3 若選深一階的 `#278E9A`，三點一起往暗推，比例不變。主片轉灰或轉黑（D4）用同一套映射，只是換一組色階。

## 溢色怎麼處理

判法照 `outfit/audit_color.py`：帶邊向外 0.5 NIF 單位以外才算遠端；RGB 任一 8-bit 色頻差 ≥12 才算顯著變色；每個三角形用 256 個子三角重心取樣，按面積加權。四條規則：

1. **照帶做**：帶外顯著變色 ≤0.5% 就過。現有最高是 touka 的 0.36%。
2. **repair**：選區的 texel 也被遠端面用到時，先在原解析度排除那些 texel，再向外保護 1 個 texel。髮帶一定要走這條。
3. **整張**：UV 幾乎全共用時不要用帶，整張一起改。袖套走這條。
4. **一律寫新路徑**：建議 `textures/miku-outfit/<件>/`。不蓋原檔，因為袖套的 `DwarvenShield.dds` 原版矮人盾也在用。

法線 `_n`、皮膚、`_m`／`_s` 不當主色染。alpha 必須逐像素相等。

## 回家套真素材

公司沒有 mod 檔，只能寫規格、跑合成測試。真素材在家跑，照 outfit-tools 的回家單 `agentctl/handoffs/home-2026-11-26/outfit-tools/HOME-REQUEST.md`（那條線交）：

1. 只寫到 staging，不裝。
2. 出對照圖給使用者答 D3–D6。
3. 答完才產 ESL、裝層、開遊戲。

DDS 先用無損 RGBA8。Corset 原圖 4096²，含 mip 約 85 MiB，實機能不能接受看 D7。

## 記錄補丁

一顆 ESL（名稱看 D17），內含五件 ARMO 與 ARMA 的複本。種族、槽位、模型照原件，只換 EDID 與貼圖。閘門由 outfit-tools 內建：master 都在、FormID 換算對、新貼圖在層裡找得到、ARMA 種族清單涵蓋 KuroneNord。輸入缺、空集合、key 打錯一律報錯。產出 staging 層、`layer_apply` manifest 草稿、INSTALL 草稿，照 custom_race 的做法。

## 階段 I：整套穿上

OTFT 把五件綁成一套；之後換色版、無袖版都只換 OTFT 的內容。給誰穿是 D8：

- **玩家**：`player.additem` 五件，最快能驗。
- **Chloe**：要 forward 她的 NPC 贏家，只改 DOFT。現有 `npc_face` 的 forward 只改臉部欄位，要嘛擴它，要嘛在 outfit-tools 加一個「只改 DOFT」的選項。擴哪一支由施工線先查工具索引決定。

Chloe 的臉與雙尾套回 NPC 是另一件事：她的皮膚 ARMO `000993` 跟 `000D70`、Recorder 共用，要先複製再卸原髮，做法在 [body 說明](../../../../agentctl/handoffs/home-2026-11-25/miku-face/body/README.md)。本計畫只把它列成 I2 的依賴，不重排。

## task 與驗收

A1–A6、I1–I2 在 [tasks-near.json](data/tasks-near.json)。階段 A 的驗收分四關：

1. 七個 shape 的閘門 exit 0。
2. 使用者看過同機位對照圖。
3. 裝層後 profile 三檔只多本層，`check_masters` 沒缺。
4. 實機正背照沒有紫色缺貼圖，且跟離線圖同處同色。
