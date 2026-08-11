# port-source-survey — 移植素材來源候選調查

← [README.md](../../README.md)

調查「除了 Dark Souls Remastered 之外，還有哪些遊戲適合抽資產移植進 Skyrim」的候選清單。起點是 [darksouls-port](../../projects/darksouls-port/) 的技術棧（SoulsFormatsNEXT 解 FromSoft 容器格式、`collision_hulls.py` 做引擎無關的碰撞後處理、glTF 當中介格式刻意不做座標轉換以利換引擎）。

**性質**：下方候選總表仍是**純討論記錄**（2026-08-04），非實測結論。**2026-08-11 新增「四道關卡」一節**，把最高分的幾個候選改用可查證的判準重評，並更正了三處初版過於樂觀的評分——以那節為準，總表的星等視為初版猜測。

**鐵律**（承襲 darksouls-port 的 IP 立場）：所有候選都以**僅本機個人使用、絕不發佈**為前提；凡是現行營運的網路遊戲（有 anti-cheat／EULA 明文禁反向工程）一律排除或降到最後考慮，風險層級跟單機遊戲的成熟 modding 生態不是同一回事。

---

## 零轉換：直接是 Skyrim 原生格式

不是「移植」，是**直接用**——同一個 Skyrim SE 引擎/ESM/BSA/NIF 格式，今天就能拿 xEdit/Creation Kit 打開，完全不用碰任何轉檔管線。省力程度是所有候選裡最高的一層，代價是這不是全新 IP，是別人已經在 Skyrim 生態內做好的東西（個人本機用沒有格式障礙，公開發佈才需要照各 mod 頁面的授權條款）。

| 候選 | 是什麼 | 亮點 |
|---|---|---|
| **Enderal**（SureAI） | 完整全轉換 mod，跑在 Skyrim SE 引擎上 | Vyn 大陸、Ark/Riverville/Kartago 等城鎮，完整原創種族/NPC/任務線，量體等同一款獨立 RPG |
| **Beyond Skyrim: Bruma** | Skyblivion 已發佈的 Cyrodiil 布魯馬區域 | 已經是別人做完 Oblivion→Skyrim 轉換的成果，直接繼承 |
| **Wyrmstooth / Beyond Reach / Falskaar** | 新增大型 worldspace 的知名 quest mod | 各自獨立設計的新大陸，城鎮/地牢佈局可直接拆解參考 |
| **Vigilant** | 大型原創 quest mod（sofia-patch 已經在碰的世界觀） | 已經是你現有專案在用的素材，順手可以再深挖 |

## 四道關卡（2026-08-11 桌面查證）

初版總表用單一「省力程度」排序，但那把四件難度不同的事壓成一個數字。從 [darksouls-port/extractor](../../projects/darksouls-port/extractor/README.md) 實際在做的四段回推，任何候選都要分別過四關：

| 關卡 | DS1R 的作法 | 為什麼是獨立的一關 |
|---|---|---|
| **① 開容器** | SoulsFormatsNEXT 讀 DCX/BND3/BXF3 | 加密或格式未逆向就整條斷；這關最容易查（拿通用工具開一下就知道） |
| **② 網格** | FLVER2 → glTF（SharpGLTF） | 有工具就過，多數引擎都有社群解包器 |
| **③ 佈局** | MSB1 → JSON（position/rotation/scale **＋ part 型別**） | **最被低估的一關**。沒有它，抽出來的是散裝資產不是城鎮 |
| **④ 碰撞** | hkx → `soulstruct-havok` → `collision_hulls.py` 凸分解 | 唯一可全部重生的一關——`collision_hulls.py` 吃通用三角網格、與來源引擎無關，最壞情況從網格重算 |

③ 的重要性有實例：`p1/P1-INGAME-FINDINGS.md` 記著判準必須是「MSB part 型別」而非「離視覺多遠」，`ConnectCollision` 要整類排除。這種資訊只有真正的關卡檔給得出來。

### 重評結果

| 候選 | ① 容器 | ② 網格 | ③ 佈局 | ④ 碰撞 | 修正後判斷 |
|---|---|---|---|---|---|
| **Bethesda 系（Oblivion/Morrowind/FO）** | ✅ BSA，工具遍地 | ✅ 原生 NIF | ✅ 原生 CELL/REFR，xEdit/CK 直接看 | ✅ 原生 havok | **仍是第一名，但不是「零轉檔」**（見下） |
| **BG3** | ✅ LSLib 解 `.pak` | ⚠️ GR2 需自備 `granny2.dll` | ✅ **`Levels/` 下 `.lsf` → `.lsx` 純文字擺放** | ⚠️ 需從網格重算 | **實質最強的非 Bethesda 候選** |
| **DS3 / Sekiro** | ⚠️ 未驗 | ⚠️ 未驗 | ⚠️ MSB3 / MSBS，**非現有 MSB1** | ⚠️ havok 版本不同 | **降級——不是「同棧」**（見下） |
| **UE4/5（霍格華茲、LotF）** | ✅ FModel | ✅ FModel/UModel | ⚠️ **只有靜態** `.umap`，blueprint 動態生成的物件抓不到 | ⚠️ 需從網格重算 | 佈局會缺一塊，缺多少視遊戲而定 |
| **Unity（Pathfinder/PoE）** | ✅ 多數不加密 | ✅ AssetStudio | ⚠️ **要換 AssetRipper**，AssetStudio 導不出完整場景層級 | ⚠️ 需從網格重算 | 可行，但工具選錯就卡在 ③ |

### 三處更正

**1. Bethesda 系不是「零轉檔」。** NIF 版本實際不同：Morrowind `4.0.0.2`、Oblivion `20.0.0.5`、Skyrim `20.2.0.7`，而且**手動改版號無效**——UESP 明載用新版 NifSkope 存 Morrowind 檔會讓 mesh 在遊戲裡直接不顯示。好消息是有現成轉換器 [Ormin/skyblivion-NIFConverter](https://github.com/Ormin/skyblivion-NIFConverter)（Skyblivion/Skywind 在用）。**結論不變（仍最省力），但省掉的是 glTF 那一段，不是整條管線**；仍需一個 NIF→NIF 轉換步驟。

**2. DS3/Sekiro 從 ★★★★☆ 降級——「同棧」的說法不成立。** extractor README 自陳「只在 DSR v1.04 `m18` 實測過；其他地圖／其他 FromSoft 遊戲（用 MSB3/FLVER0 等）未驗」。具體差在：③ DS3 用 MSB3、Sekiro 用 MSBS，現有解析器釘死 `MSB1`；④ havok 版本不同，現在靠 `soulstruct-havok` 讀 DSR 的 2015 tagfile，而 `HKLib` 只支援 2018（艾爾登）——**中間這代沒有現成 Python 讀取器**，這正是初版標給艾爾登法環的那道牆，DS3/Sekiro 同樣要面對。[Smithbox](https://github.com/vawser/Smithbox) 確實支援 DS3/Sekiro 的 Map Editor 與 Model Editor，但它是 GUI 編輯器，不等於現成的批次抽取管線。

**3. BG3 上修，且初版有一處分類錯誤。** 下方「全新戰場」段把 BG3 歸進 Unity 系，與總表的「Larian 自研（LSX/LSF）」矛盾——**以總表為準，BG3 不是 Unity**。查證後三件事：官方 Toolkit **不含 level editor**（只能唯讀載入關卡看 entity 配置），但這不重要，因為 `Levels/` 目錄下每張圖的 `.lsf` 記的就是 Characters/Items 等物件與其擺放，LSLib 可轉成 `.lsx` XML **直接當文字讀**——功能上等價於 MSB，也就是最難的 ③ 這關 BG3 是通的。網格側 `.gr2` 需要在 LSLib 的 `Tools/` 放一份相容的 `granny2.dll`，否則匯入匯出直接報 `Granny2.dll not found`。

### 關卡 ③ 的通用查法

比查文件準的一招，按引擎家族分：

- **UE4/5**：FModel 可把 `.umap` 匯出成 JSON，再用 [umodel_tools](https://skarndev.github.io/umodel_tools/) 的 Blender addon 重建。**限制是只吃靜態資料**（static mesh、燈光擺放）；UE 裡常有物件是 blueprint 或 C++ 在執行期生成的，那部分不會出現在匯出裡。所以 UE 候選要先問「這遊戲的場景有多少是靜態擺的」。UE5 另需 `mappings.usmap`。
- **Unity**：**別用 AssetStudio 做這關**。AssetStudio 適合確認有沒有加密、匯出單體模型；要完整場景層級（GameObject、transform、父子關係、prefab 結構）該用 [AssetRipper](https://assetripper.org/)，它重建的是近乎原始的場景佈局。

## 候選總表（按省力程度排序）

> ⚠️ 以下星等是 2026-08-04 的初版猜測，最高分那幾個已在上一節重評；兩處衝突以上一節為準。

| 候選 | 引擎/格式 | 城鎮/NPC 素材量 | 省力程度 | 美術評價 | 一句話理由 |
|---|---|---|---|---|---|
| **Oblivion / Morrowind / Fallout 3/NV/4** | Gamebryo→Creation（NIF 原生） | 中～高 | ★★★★★ | 中 | 跟 Skyrim 同格式家族，理論上不需要 glTF 轉檔這層；Skywind/Skyblivion 十幾年社群已把坑踩完 |
| **Baldur's Gate 3** | Larian 自研（LSX/LSF） | 極高 | ★★★★★ | 高 | 官方釋出完整 Toolkit，`LSLib` 社群工具成熟（DOS2 時代就在用），手繪質感強的奇幻美術，連光照/材質設定都拿得到 |
| **Dragon Age: Origins** | Eclipse Engine | 高 | ★★★★☆ | 中 | BioWare 官方釋出 Dragon Age Toolset，文件等於現成；畫質較舊，適合借結構不借高精度美術 |
| **Pathfinder: Kingmaker / Wrath of the Righteous** | Unity | 極高 | ★★★★☆ | 中 | Owlcat 官方支援 Unity Mod Manager，代表資產設計上就可被外部工具讀；王國/城鎮系統量體很大 |
| **Pillars of Eternity I/II** | Unity | 高 | ★★★★☆ | 中高 | 社群長期用 AssetStudio 掏過，代表未加密；等距奇幻，城鎮/對話密度高 |
| **Dark Souls 3 / Sekiro** | FromSoft（同 SoulsFormatsNEXT 棧） | 中 | ★★★★☆ | 高 | 跟現有 darksouls-port 同棧，且生態比艾爾登法環更老更成熟（Smithbox 前身就是在 DS3 上打磨的） |
| **Elden Ring** | FromSoft（同家族，格式差一代） | 高 | ★★★☆☆ | 極高——史東薇爾城、王城萊姆萊亞等大型城堡細節 + 地平線構圖的曠野景觀，是全遊戲最被稱讚的部分 | 同作者 library 支援，但 MSB→MSBE 要重寫、DCX 換 Oodle（需自己遊戲本體撈 DLL）、havok 版本也不同 |
| **The Witcher 3：血與酒（陶森特）** | REDengine 3 | 高 | ★★★☆☆ | 極高——博克萊爾宮殿、葡萄園莊園，法式哥德建築，普遍公認美術最強的奇幻 DLC 之一 | `WolvenKit` 成熟（跟 Cyberpunk 2077 共用），CDPR 對 mod 友善，非官方工具、格式較複雜 |
| **霍格華茲的傳承** | Unreal Engine 4 | 中 | ★★★☆☆ | 極高——城堡本體是近年最細緻的哥德式建築範例之一 | `FModel` 社群工具成熟，多數 UE 遊戲預設不加密；社群已大量掏過資產，可行性已驗證 |
| **Neverwinter Nights 1/2** | Aurora（官方 Toolset） | 極高（量體誇張） | ★★★☆☆ | 低 | 20 年社群模組庫量大到近乎作弊，但畫質老舊，適合借「結構/量」不借「美術品質」 |
| **Lords of the Fallen（2023）** | Unreal Engine 5 | 低～中 | ★★★☆☆ | 高——人間/靈界雙重世界對比強烈，氛圍感很強的哥德奇幻場景 | 同用 `FModel`；魂系但非 FromSoft 自家棧，NPC/城鎮量體不如上面幾款 |
| **Solasta: Crown of the Magister** | Unity | 中 | ★★★☆☆ | 中 | 官方支援 mod，格式已知，但量體比 Pathfinder/PoE 小 |
| **Outward** | Unity | 中 | ★★★☆☆ | 中 | 開放世界奇幻，城鎮密度中等，未特別確認加密狀態 |
| **Torment: Tides of Numenera** | Unity | 中 | ★★☆☆☆ | 中高 | 科幻奇幻混合非純奇幻，NPC 對話密度高，城鎮建築細節豐富 |
| **Gothic / Risen 系列** | ZenGin | 中 | ★★☆☆☆ | 中 | 20+ 年社群逆向格式，資料少、不確定成熟度 |

## 排除／高風險

| 候選 | 原因 |
|---|---|
| **黑色沙漠** | Pearl Abyss 自研引擎，`.pak` 加密且格式常變，公開解包工具生態幾乎空白；反萃取做得兇。四款韓系裡難度最高 |
| **天堂二** | 社群（L2J 等）重建的是伺服端邏輯/封包協定，不等於 client 端美術資產解包工具成熟——容易混淆的兩件事 |
| **Aion / ArcheAge** | CryEngine 系（Aion 較早期、ArcheAge 較新），CryEngine 官方發過 SDK 所以理論上有通用 `.cgf`/`.cga` 轉檔工具可用，比 BDO 好走，但仍是現行網遊，風險層級同下一條 |
| **Elder Scrolls Online** | 表面最貼近目標（同宇宙同美術基調），但是現行營運 MMO，anti-cheat + EULA 明文禁止，風險跟黑色沙漠同一層級 |
| **原神 / FF14** | 美術水準都很高（尤其原神場景），但都是現行營運 live service，跟黑色沙漠/ESO 同一風險層級，即便僅本機個人使用也不建議列入候選 |

## 通用工具驗證技巧（按引擎家族）

- **Unity**：直接拿 **AssetStudio** 開一下遊戲安裝目錄，幾分鐘內就知道有沒有加密。多數 Unity 遊戲預設不加殼，除非開發商特別上了保護（少數大廠會用 Unity 的資產加密外掛）。
- **Unreal Engine 4/5**：拿 **FModel** 開安裝目錄，同樣多數預設不加密（除非上了 pak 加密金鑰）。霍格華茲的傳承這類熱門 UE 遊戲社群已經大量驗證過可行性。

上表「未特別確認加密狀態」的都適用對應這招，比查文件準。

## 與 darksouls-port 技術棧的關係

- **完全複用**：`collision_hulls.py`（連通元件→凸包/V-HACD 後處理）吃通用三角網格 JSON，跟來源引擎無關；glTF 中介格式刻意維持來源原生座標系不做轉換，就是為了「換目標引擎不必重抽」。
- **需要重寫前端解析器**：Elden Ring（MSBE、Oodle）、**DS3（MSB3）/Sekiro（MSBS）——2026-08-11 查證後確認需要，不是「大機率」**；havok 版本亦不同，見上面「三處更正」第 2 點。Bethesda 系列這層需求最小，但仍需 NIF→NIF 版本轉換（第 1 點）。
- **全新戰場**：Unity 系（Pathfinder/PoE 等）要另外接 AssetRipper（**不是 AssetStudio**，見「關卡 ③ 的通用查法」）這類通用 Unity 解包工具，跟 FromSoft 棧完全獨立，是另一條管線。**BG3 不屬於此類**——它是 Larian 自研 LSX/LSF，走 LSLib，是第三條路。

## 待辦（尚未動工）

桌面查證能做的已在「四道關卡」做完；**以下每一條都需要本機有該遊戲**，是實測而非查資料。

- **BG3（建議優先）**：拿 LSLib 解一張小地圖的 `.lsf` → `.lsx`，確認擺放資料的欄位結構是否真能對映到 ModForge spec 的 placements。這是唯一一條能在不寫新解析器的前提下驗證 ③ 的候選。
- **Bethesda 系**：跑一次 `skyblivion-NIFConverter`，確認它產出的 NIF 能被現有 `model-converter` 管線接受，以及碰撞是否需要重生。
- 實測 Pathfinder: Kingmaker、Pillars of Eternity 的 Unity 資產是否加密（AssetStudio 開一下即知），若過關再用 AssetRipper 驗 ③。
- 查證 DS3/Sekiro 的 DCX 壓縮是否已上 Oodle（影響是否要先解決 Elden Ring 那條 Oodle DLL 路徑）。**注意**：即使 Oodle 這關過了，MSB3/MSBS 與 havok 版本兩道仍在，見上。
- 查證 Aion/ArcheAge 的 CryEngine `.cgf` 通用轉檔工具（如 CryEngine Converter）目前是否還維護、能不能吃這兩款的版本。

## 來源

2026-08-11 查證所依據的外部來源：

- [Ormin/skyblivion-NIFConverter](https://github.com/Ormin/skyblivion-NIFConverter) — Oblivion→Skyrim NIF 轉換器
- [UESP: Creating Morrowind Meshes Using New Versions of Blender](https://en.uesp.net/wiki/Morrowind_Mod:Creating_Morrowind_Meshes_Using_New_Versions_of_Blender) — NIF 版本號與「改版號無效」
- [Norbyte/lslib](https://github.com/Norbyte/lslib) — BG3 LSF/LSX/GR2 轉換
- [BG3 Modding Wiki: Getting Started with 3D Modding](https://wiki.bg3.community/Tutorials/Visual/getting-started-with-3d-modding) — `granny2.dll` 需求
- [bg3.wiki: Working with LSX files](https://bg3.wiki/wiki/Modding:Working_with_LSX_files) — `Levels/` 下 `.lsf` 的擺放資料結構
- [BG3 官方 modding 文件](https://docs.baldursgate3.game/) — Toolkit 範圍（無 level editor）
- [vawser/Smithbox](https://github.com/vawser/Smithbox) — DS3/Sekiro 的 Map/Model Editor 支援
- [umodel_tools](https://skarndev.github.io/umodel_tools/usage.html) — UE `.umap` 匯出僅含靜態資料
- [AssetRipper](https://assetripper.org/) — Unity 場景層級重建
