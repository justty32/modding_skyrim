# 日後素材／清理決定

## staging、coredump 與各線暫存要不要清（2026-09-05 重新實查後改寫）

原本列的四條路徑**已有三條自己消失了**（`/tmp` 是 tmpfs，重開機即清），清單重新以實查結果重列：

**已不存在，不必再裁**（2026-09-05 實查）：
- `/home/lorkhan/skyrim_mods/_inst2-staging` —— 不存在
- `/home/lorkhan/skyrim_mods/_lrinst-staging-2026-09-03/`（原記 18 GB NVMe）—— 不存在
- `/tmp/cx-zm4-objtext-sources`（原記 2 GB，要等 zhmake 收線）—— 不存在；zm4 也已於 2026-09-04 收線
  （agentctl commit `3be7398`、母 repo commit `91912cc`）

**還在、仍未裁示**（2026-09-05 實查大小）：
- `/var/lib/systemd/coredump` —— **3.1 GB**（原記 4.6 GB，已自行縮小）。**需要 `sudo rm`，agent 做不到。**
- `~/skyrim_mods/` 底下累積的施工暫存，實查現存這些：
  `_lrfw-staging-2026-09-03`、`_inst5-staging`、`_cc-staging-2026-09-04`、
  `_lod-staging-2026-09-04`、`_lod-dangling-backup-2026-09-04`、`_lod-vanilla-master-backup-2026-09-04`、
  `_staging-2026-09-05`、`_dl-2026-09-05`。

對上面**仍未裁示**的項目：A＝確認不再回滾後清掉換空間；B＝保留作除錯／回滾，繼續佔容量。
這組字母與 status todo-04／09 各自的選項編號無關；**未取得明確刪除授權前一律不動。**

**不要一次全清，這幾個有特殊理由**：
- `_lod-vanilla-master-backup-2026-09-04` 是清理過的原版 master 備份，Steam Verify 會還原、LOD 得重跑，
  **這是唯一的回填來源**，強烈建議留著。
- `_staging-2026-09-05` 裡有 09-05 備好但依裁示「先不套」的 Rigmor Nyx、Sofia-Head-From-Thora、
  六隨從停用腳本與 fx 3.7 GB 合併層——**裁決未完成前不能清**
  （見 `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/NEXT-SESSION.md` 第 4 節與續行表第 17 項）。
- `_dl-2026-09-05` 底下有 `lead-lib/mongo-backup-20260905T1217/`（Mongo 聚合前備份）。
- 09-05 原先開的 `lead-lr`／`lead-mco2` 狀態已變：`lead-lr` 因 19:20 改選清單而暫停，等使用者貼回
  localStorage 選單；MCO 下載續行改由 `lead-dl` 承接。證據：
  `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/STATE.md:97`／`:99`／`:103`。

`grow` 暫存 33 GB 這一項另有一份平行筆記
`/home/lorkhan/repo/moddings/skyrim/agentctl/status/todo/04-grow暫存33G要不要刪.md`。

## wf kernel v0.5.1 要不要拿（2026-09-02 通知，純重新對齊）

kernel repo（`C:/code/mine/workflows`）2026-09-02 出 v0.5.1。另一個 session 實查後結論：本 repo **沒有缺任何 bug 修正**
（三個檢查器修正都已在、percent-encoding 那條本來就是本 repo 修後回抽），這次只是 `tools/` 拆檔
（`wf-lint-checks.sh`、`tabledb_table.py`、`tabledb_fmt_expand.py`、`fix_moved_links_scan.py`）以符合 kernel 自己的 8 KB 上限，
行為與 API 不變；拆完彼此相依，**要拿就整包拿** `tools/`（`test_*` 除外）。同時 `AGENTS.md` 尾端版本戳仍是 v0.4.1，要一併改 v0.5.1。
**不可覆蓋** `wf/workflows/tidy/gotchas.md`（本 repo 拆出的 `gotchas-windows.md` 會變孤兒；那兩條 kernel 新段本來就是從它回抽的）。
判準與清單在 `C:/code/mine/workflows/docs/CHANGELOG-v0.5.1.md`。**建議**：LoreRim 調查 commit 後、或下個 session 開場時拿，拿完跑一次 strict lint 對數字。

**2026-09-05 實讀更正：仍未拿，但版本戳的描述要修正。**
- 原文寫「`AGENTS.md` 尾端版本戳仍是 v0.4.1」——**已過期**。
  `/home/lorkhan/repo/moddings/skyrim/AGENTS.md:30` 現在是
  `<!-- wf-kernel v0.5 (2026-08-30) -->（上游已出 v0.5.1，純檔案拆分無 bug 修正，尚未套用；見 agentctl/SESSION-LOG.md）`。
  要改的是 **v0.5 → v0.5.1**，不是 v0.4.1。
- **v0.5.1 確定尚未套用**：`/home/lorkhan/repo/moddings/skyrim/wf/tools/` 底下
  **沒有** v0.5.1 拆出的四個檔（`wf-lint-checks.sh`、`tabledb_table.py`、`tabledb_fmt_expand.py`、`fix_moved_links_scan.py`）。
- **待確認**：kernel 上游路徑 `C:/code/mine/workflows` 是 Windows 形式，在這台 Linux 上讀不到，
  我沒有辦法核對 `CHANGELOG-v0.5.1.md` 的實際內容，只能確認本地端「還沒拿」。
- 同一件事另有筆記 `/home/lorkhan/repo/moddings/skyrim/agentctl/status/todo/24-wf骨架版本戳沒對齊.md`。

## 夜貓－無心 3.1.0（可選精確替換）

目前 JH People 1.1.3＋NPC Plugin Chooser 2 的 536 NPC patch 已滿足方向，不阻塞整包。若仍要精確
3.1.0，只提供作者百度網盤中名稱含「人物美化」與「頭模替換」的 archive，放入既有
`/home/lorkhan/skyrim_mods/`；未取得完整資產許可不得公開重打包。見
[`相容性調查`](../wf/workflows/investigation/findings/wuxin-character-overhaul-se-ae-compatibility.md)。

**2026-09-05 核對：仍 open，但這題現在跟「外表移植」專案綁在一起看比較划算。**
09-05 使用者開了 `look-transplant` 子專案（8 位女性目標×84 個素材、17 組建議配對），
選臉是審美裁決、agent 不代選；若那批配對能滿足需求，這條「精確 3.1.0」就不必再追。
入口：`/home/lorkhan/repo/moddings/skyrim/modpack-design/content-plan/followers/voiced-follower-overhaul/look-transplant/`
（挑選頁 `/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/hd/DECISION.html`）。
證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/STATE.md:37`／`:52`／`:56`、
modpack-design commit `652ed91`／`dd009b8`。

## BG3 場景佈局實檔驗證

有合法遊戲資料時，以小型 `Levels/*.lsf` 做 `.lsf → .lsx`，記錄位置／旋轉／尺度／resource identity
能否無損對映 ModForge placements，再決定是否開 converter/spec；沒有實檔前不宣稱 pipeline 可行。
見 [`port-source-survey`](../analysis/port-source-survey/README.md)。

**2026-09-05 核對：仍 open（擋在「有沒有合法 BG3 遊戲資料」，那是你的題，agent 跨不過）。**
相鄰進展：09-05 的 `lead-mc` 線已完成 `model-converter` 通用格式→NIF 轉換
（any2nif：OBJ／GLB／FBX／DAE／STL／PLY、tex2dds、材質映射）並交付 REPORT。
它**不涵蓋 `.lsf → .lsx`**（那是 BG3 專屬容器），所以不取代本項，但之後真要做 BG3 匯入時是同一條管線的下游。
證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/mc/REPORT.md`。

## 已裁示／已完成（封存）

> 以下七項不再等你動作，從 open 清單移到這裡保存歷史。其中「Dev0A 基線存檔」是 2026-09-05 這輪新判定的，
> 其餘六項原本就已標示裁示完畢，只是還混在 open 區裡。每項附證據絕對路徑或 commit hash。

已抽到 [later-decisions-closed.json](later-decisions-closed.json)（10 列）。

項目：原本的三級標題。

關閉日期：文中的關閉或裁示日期。

證據路徑：原文所列的證據。

內容：標題下的完整原文。

統計：10 項（第 10 列為 2026-09-25 自 staging 項移入的 todo-04／todo-09 暫存刪除）。
