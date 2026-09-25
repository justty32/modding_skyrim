## Asset converter 一鍵靜態模型整包（2026-09-10）

公司 WSL 已完成一般模型、DDS 貼圖與自動 box／convex／convex-mesh 碰撞的一鍵輸出，離線測試不能證明 Skyrim 中的外觀與站立結果。

回到有 Skyrim 的機器後，用一件有 diffuse／normal 的簡單箱子或石頭，照 [轉換說明](../../projects/model-converter/PACKAGE.md) 產生整包，再在測試 cell 放置：確認大小與方向正確、貼圖可見、透明／發光設定合理，並確認角色無法穿過模型、可站上頂面。各驗一次 `box` 與 `convex`；測試素材與產物雜湊由 `converter-package.json` 記錄。

另用已分成左右柱與橫樑的門框測 `convex-mesh`：中央可通行、柱子與橫樑可阻擋。對照同一模型的 `convex` 會填滿開口。帶法線貼圖的素材再比較強度 0／0.5／2，確認表面凹凸變化合理。

新增 UV 驗收：依 [真實模型試轉](../../projects/model-converter/REAL-ASSETS.md) 重建 Lantern 與 LanternUV，比較貼圖重複／位移與法線照明；公司已逐頂點驗 NIF UV，但尚未看遊戲畫面。再依 [SheenChair 回家驗收](../../projects/model-converter/HOME-VALIDATION.md) 產出兩版與安裝測試記錄，檢查布紋／木紋的比例、陰影、法線與極細面接縫；可比較 `--bake-size 1024` 與 `2048`。Sheen／材質 variants 不算等價支援。Lantern／Avocado 來源自帶切線資料，轉換器已補直通保留；回家同樣確認 normal 凹凸與鏡射後的打光方向，公司有實際 NIF／DDS 方向測試。 SheenChair 沒有來源 TANGENT，轉換器另補鏡射 UV 接縫拆點與逐角點法線重烘；請使用最新重建批次比較，舊包不包含這次方向修正。

頂點色驗收：PLY 頂點／面顏色已補保留，NIF 的顏色資料與 shader 標記也依格式定義修正；舊的彩色 NIF 請重新轉換，再確認紅／藍分面與顏色接縫。SheenChair 來源沒有頂點色，既有驗收批次可沿用。

透明裁切驗收：MASK 的 alpha test flags 已依格式定義修正；舊版 MASK 模型需重轉，再看葉片／鐵網等貼圖透明區是否正確挖空。SheenChair 所有來源材質均為 OPAQUE，不能用它代替裁切驗收，也不需因此重建最新椅子包。

進度（2026-09-10 22:2x，lead-chair）：SheenChair 兩包已裝進現役 `modpack-main` 並實機看到——`AssetTest-SheenChair-1024`／`-2048`／`-ESP-Dev-2026-09-10`（ESL 測試 esp，2 筆 STAT `ACSheenChair1024` 000800／`ACSheenChair2048` 000801，無 REFR）。`player.placeatme FE3BE800`／`FE3BE801` 在河木鎮外空地各擺一張，兩張都正常顯示橘色布面＋木腳、椅腳朝下、貼地。碰撞外框實測 0.826×0.570×0.686 m（期望 0.827×0.570×0.686），底面 Z=0；BSX=Havok、havok layer 1 OL_STATIC、4 個分件凸包。**尚待使用者肉眼判定**：布紋／木紋比例、法線凹凸方向、接縫黑線、遠看接縫，以及走過去是否真的被擋。截圖 `agentctl/handoffs/home-2026-09-10/chair/data/shots/`。

2026-09-14 追加特效材質回家驗收：公司 WSL 已修正 `BSEffectShaderProperty` 的檔頭格式（converter `4631547`，完整離線測試 503 passed）；[格式證據與回歸](../../projects/model-converter/EFFECT-SHADER-CTD.md)不能取代遊戲載入驗收。回家需用修正版重新產生兩種光柱（`A19_BG_shaft[Dn]_Add.mtd`、`A16_light_shaft[Dn]_Add.mtd`），在獨立測試包確認進場不 CTD、光柱可見、透明與發光正常，再決定恢復 DS 管線中的兩筆 `skip`。這輪不恢復 `skip`、不部署。原始事故與避開方式見 [dsp6 進場崩潰紀錄](../../agentctl/handoffs/home-2026-09-13/dsp6/pack/REPORT.md#進-cell-ctd-與修法)；修正結果以 [converter 進度](../../projects/model-converter/SESSION-LOG.md) 為準。

2026-09-14 公司 WSL 未部署至 MO2、未動現役 profile；上段 09-10 家中部署紀錄仍有效。True PBR、蒙皮與動畫不屬這次一般靜態模型驗收。


