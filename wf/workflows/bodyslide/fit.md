# 專屬身體擬合成 preset

[入口](README.md)｜[換身體](body-swap.md)｜[部署](deploy.md)

自帶專屬身體的 NPC，裸身是作者烤好的私有 mesh，共用裝備卻是基準形（`CBBE Vanilla`）。本頁把私有身體反推成「基準身體＋滑桿值」的 preset，再走 [逐 NPC 指定身形](body-swap-npc.md)，讓裝備跟上她的身形。

**何時用**：新裝了自帶身體的隨從或換身體 mod、盤點發現某些 NPC 穿甲不合身。
**何時不用**：NPC 用全域身體（直接改 `npc_presets`）；UNP 系、原版系或拓樸不同的身體（要先換身體）。

## Done when

- `bodyslide_fit.py batch` exit 0；每套身體都有判定（可用／勉強／不可擬合／不必指定）與殘差。
- 正控通過：已知等於某 preset 的身體，擬合誤差近 0（現役正控是 Aela＝`Kurone Big Change Body`，見 `tools/test_bodyslide_fit.py`）。
- 「可用」者已加進 `obody.npc_presets`，`bodyslide_rebuild.py obody` 的 `problems` 為空。

## 原理

BodySlide 建置是線性疊加：頂點＝基準頂點＋Σ 滑桿值／100 × 該滑桿的 diff（`invert` 滑桿用 1−值／100；`_0` 用 small 值、`_1` 用 big 值）。diff 取自 ShapeData 的 `.osd`。所以「這套身體是哪組滑桿值」是帶界限的最小平方問題，stdlib 解得動：法方程只有滑桿數（約 150）見方，一套身體約 0.3 秒。模型與 BodySlide 實際建置逐頂點差 3e-5，見 2026-11-22 body-fit 的 REPORT。

## 怎麼跑

**列出誰用哪套身體**：從 NPC_ 的皮膚（或種族皮膚）走到 slot 32 的 ARMA，再解 VFS 贏家，依 `_0`／`_1` 的 sha256 去重。種族不在 ARMA 清單時改用種族的 armor race；ACBS 的 template 旗標在 offset 18。

**選滑桿集**（依頂點數）：CBBE（13,554 點）用 `CBBE.osp` 的 `CBBE Body`；3BA v2（18,436／1,905／201）用 30174 包 `SE 3BBB Amazing.osp` 的 `CBBE 3BBB Body Amazing`；3BA v1（shape `3BBB`，13,651／599／3,960）包內只剩舊 NIF 與舊 OSD，用 v2 的滑桿名改指舊 OSD 的 `3BBB<名>` 衍生一份 OSP。

**擬合**：`bodyslide_fit.py batch`，spec 列滑桿集、`base_preset`（量「現在差多少」）與每套身體的 `_0`／`_1`；單套用 `fit`。

**處理裸身**：差量會經 RaceMenu 推到 NIF 的 BODYTRI 所指的 tri，裸身已是目標形就不能再推一次。沒有 BODYTRI、或指向不存在的 tri，不用處理。指向私有 tri，就把該路徑列進 `obody.neutralize_tri`（放空 tri）。指向全域 `femalebody.tri` 時，shape 名不是 `CBBE` 對不上、不用處理；是 `CBBE` 就用 `retarget-bodytri` 複製 NIF、改指空 tri，經 `obody.extra_files` 放進 OBody 層。

**加表重產**：可用者逐 NPC 加進 `obody.npc_presets`（`plugin` 用定義該 NPC 的 plugin），擬合 preset 的 XML 目錄加進 `presets_dirs`，換 `obody.revision`，跑 `bodyslide_rebuild.py obody`；部署走 [部署](deploy.md)。

## 判定門檻

以基準身體高度 H 為尺度（H 約 100～120 單位，1 單位約 1.43 cm）：

| 判定 | 條件 | 意思 |
|---|---|---|
| 可用 | RMS ≤ 0.002H 且 p99 ≤ 0.006H | 誤差在 3 mm／1 cm 內，比裝備離皮膚的距離（0.3～1 單位）小 |
| 勉強 | RMS ≤ 0.005H 且 p99 ≤ 0.0125H | 輪廓跟得上，局部可能穿模 |
| 不可擬合 | 其餘，或拓樸對不上 | 手修過或別的拓樸，裝備跟不上 |
| 不必指定 | 基準 preset 本身就達「可用」 | 現在就合身 |

最大誤差只回報、不入判定：少數縫線與生殖器頂點會拉高它。

## 人工判斷點

- **勉強**的身體要不要指定：看資料檔的誤差集中部位；在胸、臀以外可接受。
- **擬合撞到界限**（`at_bound`）：通常是共線滑桿互相抵銷，殘差小就無妨；殘差大要人看。
- **3BA 專屬滑桿**（生殖器、乳頭細節共 22 個）不影響 CBBE 裝備；CBBE 裝備只吃兩者共有的 137 個。
- **共用同一 mesh 的 NPC** 要一起指定：空 tri 與改指的 BODYTRI 會影響所有用這個 mesh 的人。
- **實機外觀**（甲貼不貼、裸身有沒有被推兩次、存檔殘留 morph）只能由使用者在遊戲裡看；已在存檔中的 NPC 要 OBody Reset 才吃新指定。
