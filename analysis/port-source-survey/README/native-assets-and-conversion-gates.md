# 零轉換：直接是 Skyrim 原生格式

[返回入口](../README.md)

## 零轉換：直接是 Skyrim 原生格式

不是「移植」，是**直接用**——同一個 Skyrim SE 引擎/ESM/BSA/NIF 格式，今天就能拿 xEdit/Creation Kit 打開，完全不用碰任何轉檔管線。省力程度是所有候選裡最高的一層，代價是這不是全新 IP，是別人已經在 Skyrim 生態內做好的東西（個人本機用沒有格式障礙，公開發佈才需要照各 mod 頁面的授權條款）。

| 候選 | 是什麼 | 亮點 |
|---|---|---|
| **Enderal**（SureAI） | 完整全轉換 mod，跑在 Skyrim SE 引擎上 | Vyn 大陸、Ark/Riverville/Kartago 等城鎮，完整原創種族/NPC/任務線，量體等同一款獨立 RPG |
| **Beyond Skyrim: Bruma** | Skyblivion 已發佈的 Cyrodiil 布魯馬區域 | 已經是別人做完 Oblivion→Skyrim 轉換的成果，直接繼承 |
| **Wyrmstooth / Beyond Reach / Falskaar** | 新增大型 worldspace 的知名 quest mod | 各自獨立設計的新大陸，城鎮/地牢佈局可直接拆解參考 |
| **Vigilant** | 大型原創 quest mod（sofia-patch 已經在碰的世界觀） | 已經是你現有專案在用的素材，順手可以再深挖 |

## 四道關卡（2026-08-11 桌面查證）

初版總表用單一「省力程度」排序，但那把四件難度不同的事壓成一個數字。從 [darksouls-port/extractor](../../../projects/darksouls-port/extractor/README.md) 實際在做的四段回推，任何候選都要分別過四關：

| 關卡 | DS1R 的作法 | 為什麼是獨立的一關 |
|---|---|---|
| **① 開容器** | SoulsFormatsNEXT 讀 DCX/BND3/BXF3 | 加密或格式未逆向就整條斷；這關最容易查（拿通用工具開一下就知道） |
| **② 網格** | FLVER2 → glTF（SharpGLTF） | 有工具就過，多數引擎都有社群解包器 |
| **③ 佈局** | MSB1 → JSON（position/rotation/scale **＋ part 型別**） | **最被低估的一關**。沒有它，抽出來的是散裝資產不是城鎮 |
| **④ 碰撞** | hkx → `soulstruct-havok` → `collision_hulls.py` 凸分解 | 唯一可全部重生的一關——`collision_hulls.py` 吃通用三角網格、與來源引擎無關，最壞情況從網格重算 |

③ 的重要性有實例：`p1/P1-INGAME-FINDINGS.md` 的 MSB dump 能說明 `ConnectCollision` 是地圖連接語意，也能揭露 `h0054B1` / `h0099B1` 同時被註冊為普通 `Collision` 與 `ConnectCollision`。這正是單靠散裝網格看不到的資訊；但因為兩種 part 共用同一 model 與 transform，實作上也不能盲目按型別整類排除，仍要與視覺幾何的距離證據交叉判斷。

### 重評結果

重評結果的記錄已抽到 [native-assets-and-conversion-gates-candidate-reassessment.json](native-assets-and-conversion-gates-candidate-reassessment.json)（5 列）。

候選：保留原表「候選」欄內容。

① 容器：保留原表「① 容器」欄內容。

② 網格：保留原表「② 網格」欄內容。

③ 佈局：保留原表「③ 佈局」欄內容。

④ 碰撞：保留原表「④ 碰撞」欄內容。

修正後判斷：保留原表「修正後判斷」欄內容。

統計：共 5 筆記錄、6 欄。

### 三處更正

**1. Bethesda 系不是「零轉檔」。** NIF 版本實際不同：Morrowind `4.0.0.2`、Oblivion `20.0.0.5`、Skyrim `20.2.0.7`，而且**手動改版號無效**——UESP 明載用新版 NifSkope 存 Morrowind 檔會讓 mesh 在遊戲裡直接不顯示。好消息是有現成轉換器 [Ormin/skyblivion-NIFConverter](https://github.com/Ormin/skyblivion-NIFConverter)（Skyblivion/Skywind 在用）。**結論不變（仍最省力），但省掉的是 glTF 那一段，不是整條管線**；仍需一個 NIF→NIF 轉換步驟。

**2. DS3/Sekiro 從 ★★★★☆ 降級——「同棧」的說法不成立。** extractor README 自陳「只在 DSR v1.04 `m18` 實測過；其他地圖／其他 FromSoft 遊戲（用 MSB3/FLVER0 等）未驗」。具體差在：③ DS3 用 MSB3、Sekiro 用 MSBS，現有解析器釘死 `MSB1`；④ havok 版本不同，現在靠 `soulstruct-havok` 讀 DSR 的 2015 tagfile，而 `HKLib` 只支援 2018（艾爾登）——**中間這代沒有現成 Python 讀取器**，這正是初版標給艾爾登法環的那道牆，DS3/Sekiro 同樣要面對。[Smithbox](https://github.com/vawser/Smithbox) 確實支援 DS3/Sekiro 的 Map Editor 與 Model Editor，但它是 GUI 編輯器，不等於現成的批次抽取管線。

**3. BG3 上修，且初版有一處分類錯誤。** 下方「全新戰場」段把 BG3 歸進 Unity 系，與總表的「Larian 自研（LSX/LSF）」矛盾——**以總表為準，BG3 不是 Unity**。查證後三件事：官方 Toolkit **不含 level editor**（只能唯讀載入關卡看 entity 配置），但這不重要，因為 `Levels/` 目錄下每張圖的 `.lsf` 記的就是 Characters/Items 等物件與其擺放，LSLib 可轉成 `.lsx` XML **直接當文字讀**——功能上等價於 MSB，也就是最難的 ③ 這關 BG3 是通的。網格側 `.gr2` 需要在 LSLib 的 `Tools/` 放一份相容的 `granny2.dll`，否則匯入匯出直接報 `Granny2.dll not found`。

### 關卡 ③ 的通用查法

比查文件準的一招，按引擎家族分：

- **UE4/5**：FModel 可把 `.umap` 匯出成 JSON，再用 [umodel_tools](https://skarndev.github.io/umodel_tools/) 的 Blender addon 重建。**限制是只吃靜態資料**（static mesh、燈光擺放）；UE 裡常有物件是 blueprint 或 C++ 在執行期生成的，那部分不會出現在匯出裡。所以 UE 候選要先問「這遊戲的場景有多少是靜態擺的」。UE5 另需 `mappings.usmap`。
- **Unity**：**別用 AssetStudio 做這關**。AssetStudio 適合確認有沒有加密、匯出單體模型；要完整場景層級（GameObject、transform、父子關係、prefab 結構）該用 [AssetRipper](https://assetripper.org/)，它重建的是近乎原始的場景佈局。

### 已完成移植的旁路（韓文站候選回饋，2026-08-11）

`korean-policy-porting-2026-08-07-b2b` 的三筆候選已逐筆對照本機保留的 `meta.json` 與原始 `page.html`。先前把它們籠統稱為「地圖 porting 類」是分類錯誤；三者都是裝備或道具，沒有一筆包含地圖或場景佈局。

| 候選 | 頁面實際內容 | 對本調查的證據力 |
|---|---|---|
| BDO Arethel & Heled | 兩套服裝，CBBE 3BA / HDT-SMP | 只證明特定角色裝備的網格、材質與物理已有 Skyrim 成品 |
| Dark Souls 3 Silver Knight | 兩套盔甲及劍、槍、盾、弓箭 | 只證明單體角色資產可移植；不證明 MSB3 佈局或地圖 havok 已解 |
| Bloodborne Lantern HDT | 紅／藍提燈的道具版與武器版 | 只證明單一道具的網格、材質與物理已有 Skyrim 成品 |

**結論**：這三筆不會推翻四道關卡對「自己抽地圖」的判斷，也不能用來上修 BDO、DS3 或 Bloodborne 的地圖候選排名。它們證明的是另一條路：若只要單體物件，可直接使用別人已轉成 Skyrim 格式的成品，因而繞過來源遊戲的容器、佈局與碰撞解析。這條「成品移植旁路」要另外處理來源、版本相容性與授權；本調查仍只允許本機個人使用，不把下載連結存活視為可再發佈的證明。

