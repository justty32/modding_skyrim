# racemenu／author — 需求凍結與合成（純數值法）

[racemenu](README.md)｜[WORKFLOWS](../../WORKFLOWS.md)

段 1–2：把「臉再瘦一點」這類話變成一份份候選 `.jslot`。全程離線，不碰 `instance/`。這一段**看不到結果**，只負責產生數值合理、結構正確、改動可追溯的候選。看圖要靠 [loop](loop.md)，那一段還沒做好。

## 工具

`agentctl/tools/jslot/cli.py`（stdlib；測試在同目錄 `test_jslot.py`）：

| 子命令 | 用途 |
|---|---|
| `show A.jslot [--json]` | 列出 NAM9 18 個滑桿（含代號）、NAMA 部件編號、headParts、可見 tint 層、custom、sculpt、依賴 plugin |
| `lint A.jslot …` | 驗結構；有 error 就 exit 1 |
| `set A.jslot -o OUT.jslot '<修改>' …` | 白名單修改，只寫新檔；OUT 已存在或等於來源就拒絕 |
| `diff A.jslot B.jslot [--json]` | 欄位級比較，NAM9 帶 Δ |
| `fields` | 列出可改與唯讀的欄位，以及唯讀的理由 |

修改語法：`nam9.<代號或 0-17>=V`、`+=D`、`-=D`（結果必須落在 ±1）、`preset.nose|eyes|mouth=N`、`weight=V`、`tint.<index>.color=#RRGGBB`、`tint.<index>.alpha=0-255`、`custom.<既有名稱>=V`。headParts、髮色、sculpt、transforms、overrides 等欄位唯讀，理由用 `fields` 查。

寫出的檔和 RaceMenu（JsonCpp StyledWriter）的格式逐位元組相同。本機 8 份真檔都驗過原樣讀寫不變，所以 `git diff` 或文字 diff 只會出現真的改到的那幾行。

## 1. 需求凍結

寫一張需求卡（放任務證據夾），內容：

1. **目標 actor**：主角或某個 NPC（EDID／FormID，用 `instance/tools/whichmod.py` 查定義與贏家）。主角目前是男性 Imperial。
2. **基底**：哪份 jslot（本機現有的見調查線 `racemenu-components.json`），或「NPC 現有的臉」。後者要先做 NPC→jslot 反向轉換，這支工具**還沒做**，見 [計畫](../plans/racemenu-face/README.md)。
3. **基底和目標要同性別、同種族**。tint 的 `index` 和 headParts 都綁種族，跨種族的基底只能取 NAM9 數值。
4. **特徵清單**：使用者的原話逐條列出，每條對到下面 §2 的一列。
5. **依賴**：`show` 印出的「依賴 plugin」都要在現役 profile 裡（`instance/tools/profile_query.py`）。

Done when：需求卡存在，且每條原話都標了「對到哪列」或「做不到＋原因」。

## 2. 合成：文字需求→滑桿

兩份資料檔（契約見 [data-files](../common/data-files.md)，查法見那份的工具段）：

- [sliders.json](sliders.json)（47 列）：每個可調欄位一列。欄位如下：
  - `id`：工具用的代號。
  - `field`：jslot 路徑。
  - `kind`：NAM9、NAMA、tint 或唯讀。
  - `zh`：中文說明。
  - `range`：取值範圍。
  - `neg_pole`、`pos_pole`：負值、正值各對到 chargen tri 的哪個 morph。
  - `effect`：視覺效果。
  - `phrases`：常見說法。
  - `step`：建議步幅。
  - `editable`：工具能不能改。
  - `source`：出處。
  - `confidence`：實證或推論。
- [intents.json](intents.json)（22 列）：常見說法→要動哪幾個欄位、往哪一端、動多少。欄位是 `intent`、`adjust`、`note`、`confidence`。`adjust` 用「欄位→目標端 幅度」寫，例如 `nam9.Jaw_NarrowWide→JawNarrow 0.1`。要轉成正負號，查 sliders.json 那列的 `neg_pole`／`pos_pole`。

做法：

1. 每條特徵先找 intents.json；沒有就找 sliders.json 的 `phrases`、`zh`；兩邊都對不到，就在回報表寫「無對應滑桿」，不要硬湊。
2. **每輪幅度**：每條需求對主軸動「小 0.1」；使用者說「很多／明顯」才用「中 0.2」；單一軸單輪不超過 0.3。tint 的 alpha 每輪 ±32，RGB 每通道 ±16。
3. **離散欄位**（`preset.eyes`／`nose`／`mouth`）沒有「大一點」這種方向，相鄰編號也不代表外觀相近。每個編號各出一份候選，最多 3 份，要等看圖才能選。
4. **候選數**：同一輪最多 3 份。命名 `<基底>_r<輪>_<a|b|c>.jslot`。每份都跑 `lint`，並對基底跑 `diff`。
5. 原版**沒有**連續的「眼睛大小」滑桿；能用的只有 `preset.eyes` 和眼睛深淺。裝了 ECE／EFM 後才會有 custom 滑桿，目前本機沒裝。
6. 身形需求（胸、腰、臀、整體身材）不在這裡改，轉交 [bodyslide](../bodyslide/README.md)。

Done when：每份候選 `lint` exit 0；`diff` 對基底列出的欄位和需求卡的對應完全一致，沒有多出來的欄位。

## 3. 方向還沒校準

欄位對應已有實證：NAM9 19 格的順序來自 xEdit `wbDefinitionsTES5.pas:8435-8455` 與 CommonLibSSE `TESNPC.h` `FaceData::Morphs`；每軸對到哪兩個 tri morph，來自 `femaleheadchargen.tri` 的 morph 名稱。

**還沒實證的是「負值是 A 端還是 B 端」**。sliders.json 先依 xEdit 欄名的順序假設負值對 A 端（例如 `Nose Long/Short`：負值＝NoseLong）。在 [loop](loop.md) 的出圖或截圖做好之前：

- 回報時一律寫成「往 JawNarrow 端 0.1（假設為負值，方向未校準）」。
- 校準後只改 sliders.json 的 `neg_pole`／`pos_pole` 和 `confidence`。intents.json 不用動，因為它只寫目標端，不寫正負號。

## 4. 回報格式

每輪給使用者一張表（候選 × 改動），並附一句結論：

| 候選 | 需求原話 | 改了什麼（欄位：舊→新） | 依據 | 看過圖嗎 |
|---|---|---|---|---|
| `Hatak_r1_a` | 臉瘦一點 | `nam9.Jaw_NarrowWide`：-0.30→-0.40（往 JawNarrow，方向未校準） | intents「臉瘦一點」 | 否（純數值） |

「看過圖嗎」在段 3／4 做好之前一律填「否」。**不可**寫「效果如預期」。
