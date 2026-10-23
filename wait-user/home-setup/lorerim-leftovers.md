## LoreRim 借用後續：只剩三題（2026-09-05 核對後縮小）

2026-09-03 已入庫 439 件／8.966 GB，借用段 359 件、42 個中文層與 16 個框架／解鎖件已上線。
原本六題，**四題已在 09-03／09-04 落地或裁示**（搬到本檔末尾的已完成節），剩下這三題還等你：

<!-- wf-nav -->
1. **21 件中文層拓撲 FAIL 是否全改自製。** 09-03 `lrzh` 契約寫死不碰，至今沒動；
   `lrrev` 已逐件記 `fail_reason`。證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-03/lrzh/REPORT.md:128`
   （「沒做：FAIL 21 件」）、同檔 `:155`。
2. **五件 `NO-PEX-UPSTREAM` 借用件（CFTO 以外）留著還是停用。** 三處（archive／Nexus／BSA）都沒有 `.pex`，
   Papyrus `Cannot open store` 剩的 5 筆正是它們。逐件表：
   `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-03/lrzh/REPORT.md:56-60`
   （LR-0267 CFTO、LR-0292、LR-0302、LR-0206、LR-0085）。
3. **要不要全圖補跑地形 LOD（xLODGen）。** 2026-10-23 改寫：原題「找不找得到來源」**已失效**——
   09-20 `bcfix` 線已從 sheson 的 GitHub release v132 下載解開，實讀就在
   `~/skyrim_mods/tools/xLODGen-132-bcfix/xLODGen/xLODGenx64.exe`，**從未執行、沒註冊進 MO2**；
   只有「不在 Nexus」那半句還對。真問題是要不要為遠景地表開一次 50–120 分鐘的 GUI 工序，
   而**你 10-08 已往反方向裁過一次**：照「整個停掉 DynDOLOD，不重跑」整組停用
   （`modlist.txt:195`-`:197`、`:2410`-`:2411` 全 `-`，profiles `2cdbf1a`），遠景已退回原版 object LOD。
   10-03「只在補 Bloodchill／Rigmor 地形 LOD 時才跑、目視接縫再補」的條件式裁示，兩個觸發點也沒了
   （Rigmor 整族 10-08 停用；Bloodchill 補丁 10-03 已部署且只改 LAND，`:336`）。**預設答案＝不跑**：
   **A＝維持不跑**（建議）；**B＝實機看到接縫才補**，照 `bcfix/LOD-RUNBOOK.md` 跑 Tamriel 四級 Specific Chunk，
   **不能無人值守**；**C＝連 DynDOLOD 一起恢復重跑**（另加約 1.5 小時，等於推翻 10-08 那條裁示）。
   證據（`…`＝`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/`）：
   `…/2026-09/home-2026-09-20/bcfix/REPORT.md:156`／`:176`、同線 `LOD-RUNBOOK.md:7`、
   `…/2026-10/home-2026-10-03/worldfix/data/lod/ASSESS.md:4`／`:9`／`:32`、
   `…/2026-10/home-2026-10-08/newsave/BRIEF-build.md:10`、`REPORT-build.md:13`／`:75`。

> **2026-09-05 追加的上位裁示**：使用者當日 14:00 說「LoreRim 裡面的東西我全都要」，範圍＝371 件
> （BORROW 176＋ASK 195，621 件 SKIP 不碰），已由 `lead-lr` 解析對版、依賴閉包與下載入庫，安裝計畫 B0–B8 已 push。
> 證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-05/STATE.md:73`／`:84`、
> modpack-design commit `c064897`。**那是新的一批，不取代上面這三題。**
> **19:20 後續更正**：使用者已改選 LoreRim 清單，371 件全收計畫不再是現行下載範圍；目前等待使用者貼回
> localStorage 選單，下載暫停。原 14:00 裁示留在上段作歷史，不可再當執行指令。
> 證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-05/STATE.md:97`。
