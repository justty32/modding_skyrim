# 日後素材／清理決定

## 夜貓－無心 3.1.0（可選精確替換）

目前 JH People 1.1.3＋NPC Plugin Chooser 2 的 536 NPC patch 已滿足方向，不阻塞整包。若仍要精確
3.1.0，只提供作者百度網盤中名稱含「人物美化」與「頭模替換」的 archive，放入既有
`/home/lorkhan/skyrim_mods/`；未取得完整資產許可不得公開重打包。見
[`相容性調查`](../wf/workflows/investigation/findings/wuxin-character-overhaul-se-ae-compatibility.md)。

**2026-09-05 核對：仍 open，但這題現在跟「外表移植」專案綁在一起看比較划算。**
09-05 使用者開了 `look-transplant` 子專案（8 位女性目標×84 個素材、17 組建議配對），
選臉是審美裁決、agent 不代選；若那批配對能滿足需求，這條「精確 3.1.0」就不必再追。
入口：`/home/lorkhan/repo/moddings/skyrim/modpack-design/content-plan/followers/voiced-follower-overhaul/look-transplant/`
（挑選頁 `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-05/hd/DECISION.html`）。
證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-05/STATE.md:37`／`:52`／`:56`、
modpack-design commit `652ed91`／`dd009b8`。

## BG3 場景佈局實檔驗證

有合法遊戲資料時，以小型 `Levels/*.lsf` 做 `.lsf → .lsx`，記錄位置／旋轉／尺度／resource identity
能否無損對映 ModForge placements，再決定是否開 converter/spec；沒有實檔前不宣稱 pipeline 可行。
見 [`port-source-survey`](../analysis/port-source-survey/README.md)。

**2026-09-05 核對：仍 open（擋在「有沒有合法 BG3 遊戲資料」，那是你的題，agent 跨不過）。**
相鄰進展：09-05 的 `lead-mc` 線已完成 `model-converter` 通用格式→NIF 轉換
（any2nif：OBJ／GLB／FBX／DAE／STL／PLY、tex2dds、材質映射）並交付 REPORT。
它**不涵蓋 `.lsf → .lsx`**（那是 BG3 專屬容器），所以不取代本項，但之後真要做 BG3 匯入時是同一條管線的下游。
證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/done/2026-09/home-2026-09-05/mc/REPORT.md`。

## 已裁示／已完成（封存）

> 以下各項不再等你動作，從 open 清單移到這裡保存歷史。「Dev0A 基線存檔」是 2026-09-05 這輪新判定的，
> 「wf kernel v0.5.1」是 2026-10-23 搬進來的（09-25 23:30 就已結案，條目卻漏在 open 區）。
> 每項附證據絕對路徑或 commit hash。

已抽到 [later-decisions-closed.json](later-decisions-closed.json)（13 列）。

項目：原本的三級標題。

關閉日期：文中的關閉或裁示日期。

證據路徑：原文所列的證據。

內容：標題下的完整原文。

統計：13 項（第 10 列為 2026-09-25 自 staging 項移入的 todo-04／todo-09 暫存刪除；
第 12 列為 2026-10-23 使用者裁示全刪並執行完畢的 staging／暫存清理題；
第 13 列為同日 MO2 關閉後自行收斂的 profiles 暫態（16:10 envsnap 實測 dirty=0），開了又當天結案；
第 11 列為 2026-10-23 移入的 wf kernel v0.5.1／v0.6 升級）。

2026-09-25 22:25 推進（wf kernel v0.5.1）：cx-wu-kern 試做純覆蓋升級，發現本地 `wf/tools` 已含上游 v0.5.1 之後的規則（母 repo kernel 測試 15 項中 3 項專測這些，覆蓋後轉紅），dispatcher 裁定**不降版並撤回 commit**；下次升級要對齊上游 v0.6 或更新、用 diff 合併。對照報告 `agentctl/handoffs/done/2026-09/home-2026-09-25/wu/kern/REPORT.md`。此項改為「等上游 v0.6」，不再是可直接套的維護。

2026-09-25 23:30 **wf kernel 升級結案**：`cx-wu-kern2` 三載點對齊上游 main `794d6d2`（v0.6＋lint 修正），tools 整包、kernel 段換新、本地段保留；lint 持平、上游 15 項測試綠；各 repo 已 push。此項關閉。
