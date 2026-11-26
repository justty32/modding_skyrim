# 階段 M 網格：無袖、貼身、修穿模、髮飾、領帶

[計畫入口](README.md)｜工具調查 [offline-survey](../../../../agentctl/handoffs/home-2026-11-25/miku-face/offline-survey/REPORT.md)｜生成式 AI 調查 [ai-3d-survey](../../../../agentctl/handoffs/home-2026-11-26/ai-3d-survey/REPORT.md)

換色只能改顏色。無袖剪裁、領帶、方形髮飾、貼合 Chloe 身體、修掉跟雙尾的穿模，都要動網格。

## 要什麼工具

**階段 1：Outfit Studio 6.2 的 MCP**。Outfit Studio 從 6.1.0 起內建給 AI 用的 MCP server，不用滑鼠就能匯入 NIF／OBJ、刪頂點、conform 到參考身體、改權重、量穿模、存回 NIF。現役是 5.8.2，沒有這個功能。要升 6.2.0，Nexus 只給 nxm 下載。工具的 schema 兩個月出了三版，可能還會變。

驅動它的 `agentctl/tools/os_runner/` 現在只是骨架：只印計畫，加 `--execute` 也會被拒，等授權後才 pilot。要補的是 loopback 與 Mesa llvmpipe GLX（現有 BodySlide 沙箱關網路也關 GLX），以及 Wine 行程的收尾。估約 1 天（offline-survey 的 P7）。

**階段 2：Blender＋自編 PyNifly**。從零建模才需要：麥克風架、耳機、重做襯衫。PyNifly 官方只支援 Windows，Linux 版是 2026-11-20 開、還沒合併的 PR #453。兩樣都是 GPL-3.0，自用沒問題，程式碼不搬進 repo。

**生成式 AI（2026-11-26 調查，使用者「可以併入」）**：開源文字／圖片轉 3D 出的是幾十萬面三角網格，要減面、重展 UV、再烘焙才能進遊戲，所以領帶、方形髮飾、麥克風架改用 agent 寫 Blender 腳本（`blender -b --python`）程序化建模；無袖、蔥是改現有網格，AI 用不上。AI 只用在兩處：耳機麥克風的草模（TripoSG，MIT，約 8 GB VRAM，有 CLI 可限面數），以及在我們自己的 UV 上畫紋理（StableGen，本地，8 GB 起，可沿用既有 UV；TRELLIS.2 texturing 要 24 GB；Meshy Retexture 是雲端付費備援）。PBR 轉 Skyrim：albedo→`_d`，normal→`_n` RGB，roughness 反相進 `_n` alpha。Blender 有官方 MCP（Blender Lab，GPL，可無頭）。AI 綁骨套不了 Skyrim 骨架，權重照舊從身體複製。Hunyuan3D 授權排除 EU、英國、南韓，而且上紋理會重展 UV，不用。各件路線見調查的 `parts.json`，工具比較見 `tools.json`（40 列）。回家先查顯卡 VRAM 與原版 normal 綠通道方向。

**量測**：`hair/phase2/surface_audit.py` 已能量雙尾×衣服的三角交叉。衣服×身體還沒有現成模式，要擴（M3）。

## 要使用者授權的

- **D1**：家裡下載 Outfit Studio 6.2，放在 MO2 外的沙箱，跑它的 MCP，並改沙箱 runner 開 loopback 與 GLX。公司已答先不要。
- **D2**：家裡 pacman 裝 Blender，clone 並編譯未合併的 PyNifly 分支。推薦等階段 1 做完再准。
- 要用 AI 那兩處時：下載 TripoSG、StableGen（含 ComfyUI）的模型權重，各要使用者點頭；雲端備援要帳號＋付費。
- 做出來的 NIF 要裝進 MO2、要開遊戲，照舊每次當場說。

## 各件做法

**M2 無袖**：複製 RecorderShirt 的 NIF，用 MCP 刪掉 touka 的袖子頂點，修邊。嵌身 `0HWUNP0` 的肩臂要露出來，會碰到 UNP 與 Kurone7 皮膚貼圖接縫，正背出圖看。

**M3 貼合 Kurone7**：以 Chloe 的私有 Kurone7 體重 0／100 身體當參考，五件逐件 conform，兩端都要存。Kurone7 沒有 BODYTRI，衣服做完也不會跟著 RaceMenu 身體滑桿變，這是現況，不是新問題。

**M4 修雙尾穿模**：盤點表的交叉對（髮帶 367、裙 232、touka 146、嵌身 80、Corset 25）。改衣服，不改已實拍的雙尾。要不要做到 0，或看圖接受，由使用者決定。

**M5 方形髮飾**：官方設定是左右各一個紅黑方塊。幾何就是兩個方塊，可以用程式產 OBJ，交給 Outfit Studio 匯入、綁頭骨、存 NIF，不必等 Blender。它要新 ARMO，佔一個現役沒衝突的槽（避開頭髮 31 與髮帶 42，從 44–48 挑），施工前先查載入序。

**M6 領帶**：扁平幾何，綁 Neck／Spine2，做法同 M5。要跟著胸口動，權重比髮飾難，做不好就等階段 2。

**M8 新建模**：麥克風架（[weapons.md](weapons.md) 的 WP5，Blender 程序化建模）、耳機（D16，TripoSG 草模→減面→上色）、重做襯衫。每件都照 M3 的量測與 A6 的實機流程驗。

## 家裡與公司

| 步驟 | 公司 | 家 |
|---|---|---|
| os_runner 補完、mock 測試 | 能 | — |
| os_runner pilot、跑 Outfit Studio | 不能（不安裝） | D1 准了才能 |
| surface_audit 加衣物×身體 | 能，合成網格測試 | 真網格跑 |
| 方塊、領帶 OBJ 產生器 | 能 | — |
| Blender、PyNifly | 不能 | D2 准了才能 |

## 閘門與驗收

1. **pilot**：`health` 回 OK、`render_view` 出一張圖、`stop` 後沒有殘留行程。沒過就停在這裡，不換別的方法繞。
2. **每件 NIF**：shape 名、頂點數、權重骨、貼圖路徑用 `nif_inspect` 讀回；正背出圖沒有破洞。
3. **穿模**：中立姿衣物×身體、雙尾×衣物交叉對降到 0，或降到使用者看圖接受的值。
4. **實機**：同階段 A6，另外看走、跑、坐下時的穿模。

## 工作量與依賴

M1 約 1 天；M2 1 天；M3 2–3 天；M4 1 天；M5、M6 各 1 天。合計約 7–8 天，加實機。M8 每件 1–3 天，另計。依賴：M1 要 D1；M2–M6 要 M1；M4 要 M3；M8 要 D2。task 在 [tasks-later.json](data/tasks-later.json)。

## 風險

- Outfit Studio 存回 NIF 時，原件的分區、shader、額外資料會不會被改動，還沒驗（offline-survey 只標了 FaceGen 頭的同類風險）。存回後一律 `nif_inspect` 對照原件。
- 改了衣服網格，階段 A 的 UV 帶高度（z_bands）可能要重量。
- 新網格的授權：改作現成 mod 的網格只供自用；要公開發布得另查各 mod 的 Permissions。
