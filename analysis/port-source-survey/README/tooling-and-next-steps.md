# 通用工具驗證技巧（按引擎家族）

[返回入口](../README.md)

## 通用工具驗證技巧（按引擎家族）

- **Unity**：直接拿 **AssetStudio** 開一下遊戲安裝目錄，幾分鐘內就知道有沒有加密。多數 Unity 遊戲預設不加殼，除非開發商特別上了保護（少數大廠會用 Unity 的資產加密外掛）。
- **Unreal Engine 4/5**：拿 **FModel** 開安裝目錄，同樣多數預設不加密（除非上了 pak 加密金鑰）。霍格華茲的傳承這類熱門 UE 遊戲社群已經大量驗證過可行性。

上表「未特別確認加密狀態」的都適用對應這招，比查文件準。

## 與 darksouls-port 技術棧的關係

- **完全複用**：`collision_hulls.py`（連通元件→凸包/V-HACD 後處理）吃通用三角網格 JSON，跟來源引擎無關；glTF 中介格式刻意維持來源原生座標系不做轉換，就是為了「換目標引擎不必重抽」。
- **需要重寫前端解析器**：Elden Ring（MSBE、Oodle）、**DS3（MSB3）/Sekiro（MSBS）——2026-08-11 查證後確認需要，不是「大機率」**；havok 版本亦不同，見上面「三處更正」第 2 點。Bethesda 系列這層需求最小，但仍需 NIF→NIF 版本轉換（第 1 點）。
- **全新戰場**：Unity 系（Pathfinder/PoE 等）要另外接 AssetRipper（**不是 AssetStudio**，見「關卡 ③ 的通用查法」）這類通用 Unity 解包工具，跟 FromSoft 棧完全獨立，是另一條管線。**BG3 不屬於此類**——它是 Larian 自研 LSX/LSF，走 LSLib，是第三條路。

## 待辦（尚未動工）

韓文站候選的桌面回饋已在上節做完；**以下每一條都需要本機有該遊戲**，是實測而非查資料。
- **BG3（自己動手的候選裡建議優先）**：拿 LSLib 解一張小地圖的 `.lsf` → `.lsx`，確認擺放資料的欄位結構是否真能對映到 ModForge spec 的 placements。這是唯一一條能在不寫新解析器的前提下驗證 ③ 的候選。
- **Bethesda 系**：跑一次 `skyblivion-NIFConverter`，確認它產出的 NIF 能被現有 `model-converter` 管線接受，以及碰撞是否需要重生。
- 實測 Pathfinder: Kingmaker、Pillars of Eternity 的 Unity 資產是否加密（AssetStudio 開一下即知），若過關再用 AssetRipper 驗 ③。
- 查證 DS3/Sekiro 的 DCX 壓縮是否已上 Oodle（影響是否要先解決 Elden Ring 那條 Oodle DLL 路徑）。**注意**：即使 Oodle 這關過了，MSB3/MSBS 與 havok 版本兩道仍在，見上。
- 查證 Aion/ArcheAge 的 CryEngine `.cgf` 通用轉檔工具（如 CryEngine Converter）目前是否還維護、能不能吃這兩款的版本。

## 來源

2026-08-11 查證所依據的外部來源：

<!-- wf-nav -->

- [Ormin/skyblivion-NIFConverter](https://github.com/Ormin/skyblivion-NIFConverter) — Oblivion→Skyrim NIF 轉換器
- [UESP: Creating Morrowind Meshes Using New Versions of Blender](https://en.uesp.net/wiki/Morrowind_Mod:Creating_Morrowind_Meshes_Using_New_Versions_of_Blender) — NIF 版本號與「改版號無效」
- [Norbyte/lslib](https://github.com/Norbyte/lslib) — BG3 LSF/LSX/GR2 轉換
- [BG3 Modding Wiki: Getting Started with 3D Modding](https://wiki.bg3.community/Tutorials/Visual/getting-started-with-3d-modding) — `granny2.dll` 需求
- [bg3.wiki: Working with LSX files](https://bg3.wiki/wiki/Modding:Working_with_LSX_files) — `Levels/` 下 `.lsf` 的擺放資料結構
- [BG3 官方 modding 文件](https://docs.baldursgate3.game/) — Toolkit 範圍（無 level editor）
- [vawser/Smithbox](https://github.com/vawser/Smithbox) — DS3/Sekiro 的 Map/Model Editor 支援
- [umodel_tools](https://skarndev.github.io/umodel_tools/usage.html) — UE `.umap` 匯出僅含靜態資料
- [AssetRipper](https://assetripper.org/) — Unity 場景層級重建
