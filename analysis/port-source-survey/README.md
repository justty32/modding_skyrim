# port-source-survey — 移植素材來源候選調查

← [README.md](../../README.md)

調查「除了 Dark Souls Remastered 之外，還有哪些遊戲適合抽資產移植進 Skyrim」的候選清單。起點是 [darksouls-port](../../projects/darksouls-port/) 的技術棧（SoulsFormatsNEXT 解 FromSoft 容器格式、`collision_hulls.py` 做引擎無關的碰撞後處理、glTF 當中介格式刻意不做座標轉換以利換引擎）。

**性質**：純討論記錄，非實測結論。下面標「不確定」的地方動手前務必先驗證，不要當定論引用。

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

## 候選總表（按省力程度排序）

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
- **需要重寫前端解析器**：Elden Ring（MSBE、Oodle）、DS3/Sekiro（大機率同樣需要，未驗）；Bethesda 系列反而可能完全不需要這層，因為目標格式（NIF）本來就相容。
- **全新戰場**：Unity 系（Pathfinder/PoE/BG3 等）要另外接 AssetStudio/UABE 這類通用 Unity 解包工具，跟 FromSoft 棧完全獨立，是另一條管線。

## 待辦（尚未動工）

- 實測 Pathfinder: Kingmaker、Pillars of Eternity 的 Unity 資產是否加密（AssetStudio 直接開）。
- 查證 DS3/Sekiro 的 DCX 壓縮是否已上 Oodle（影響是否要先解決 Elden Ring 那條 Oodle DLL 路徑）。
- 查證 Aion/ArcheAge 的 CryEngine `.cgf` 通用轉檔工具（如 CryEngine Converter）目前是否還維護、能不能吃這兩款的版本。
