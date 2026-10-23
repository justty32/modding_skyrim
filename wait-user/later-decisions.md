# 日後素材／清理決定

## staging、coredump 與各線暫存要不要清（2026-10-23 重新實查後改寫）

**這題仍 open，等你裁。** 2026-10-23 逐條 `ls`／`du` 重查，原文列的數字與路徑有一半已經不準，先把現況換上去；
**本線沒有刪任何東西，也沒有替你決定**。

**coredump 已經不是問題，不必再為它開 sudo**：`/var/lib/systemd/coredump` 實測 **77 MB**
（原文寫 3.1 GB、更早寫 4.6 GB，`systemd-coredump` 自己輪替掉了）。

**原文列的「還在、仍未裁示」八個目錄，今天只剩四個**：

| 目錄（`/home/lorkhan/skyrim_mods/` 下） | 2026-10-23 現況 | 大小 |
|---|---|---:|
| `_lrfw-staging-2026-09-03` | **已不存在** | — |
| `_inst5-staging` | **已不存在** | — |
| `_lod-staging-2026-09-04` | **已不存在** | — |
| `_staging-2026-09-05` | **已不存在** | — |
| `_cc-staging-2026-09-04` | 還在 | 119 MB |
| `_lod-dangling-backup-2026-09-04` | 還在 | 150 MB |
| `_lod-vanilla-master-backup-2026-09-04` | 還在 | 47 MB |
| `_dl-2026-09-05` | 還在 | 1.5 GB |

這四個消失的目錄是哪一輪清掉的，我沒有在 handoffs 裡找到明確紀錄，**只能說「現在不在了」**；
原文對 `_staging-2026-09-05` 寫的「裁決未完成前不能清」已經沒有對象，如果那批 Rigmor Nyx／
Sofia-Head-From-Thora／六隨從停用腳本／fx 合併層還需要，要重做而不是重找。

**順帶：真正佔空間的其實是 `_dl-*` 下載區，不是 staging。** `~/skyrim_mods/_*` 全部合計 **13 GB**，
其中 `_dl-2026-09-06` 3.8 GB、`_dl-2026-09-08` 3.5 GB、`_dl-2026-09-05` 1.5 GB、`_dl-2026-10-10` 479 MB
就佔掉 9.2 GB；`_staging-*` 五個加起來只有約 485 MB。這些在 2026-10-10 收工時也記過
（`agentctl/handoffs/done/2026-10/home-2026-10-10/STATE.md:13`：9 月與 10-03 的舊暫存未清，當天只授權清 10-10 的）。

**要你裁的還是同兩個選項**：A＝確認不再回滾後清掉換空間；B＝保留作除錯／回滾，繼續佔容量。
這組字母與 status todo-04／09 各自的選項編號無關；**未取得明確刪除授權前一律不動**，
而且依既定規則，刪除授權要你本人給，轉述的不算。

**不要一次全清，這兩個有特殊理由**：
- `_lod-vanilla-master-backup-2026-09-04`（47 MB）是清理過的原版 master 備份，Steam Verify 會還原、
  LOD 得重跑，**這是唯一的回填來源**，強烈建議留著。
- `_dl-2026-09-05`（1.5 GB）底下有 `lead-lib/mongo-backup-20260905T1217/`（Mongo 聚合前備份）。

`grow` 暫存 33 GB 這一項另有一份平行筆記
`/home/lorkhan/repo/moddings/skyrim/agentctl/status/todo/04-grow暫存33G要不要刪.md`。

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

已抽到 [later-decisions-closed.json](later-decisions-closed.json)（11 列）。

項目：原本的三級標題。

關閉日期：文中的關閉或裁示日期。

證據路徑：原文所列的證據。

內容：標題下的完整原文。

統計：11 項（第 10 列為 2026-09-25 自 staging 項移入的 todo-04／todo-09 暫存刪除；
第 11 列為 2026-10-23 移入的 wf kernel v0.5.1／v0.6 升級）。

2026-09-25 22:25 推進（wf kernel v0.5.1）：cx-wu-kern 試做純覆蓋升級，發現本地 `wf/tools` 已含上游 v0.5.1 之後的規則（母 repo kernel 測試 15 項中 3 項專測這些，覆蓋後轉紅），dispatcher 裁定**不降版並撤回 commit**；下次升級要對齊上游 v0.6 或更新、用 diff 合併。對照報告 `agentctl/handoffs/done/2026-09/home-2026-09-25/wu/kern/REPORT.md`。此項改為「等上游 v0.6」，不再是可直接套的維護。

2026-09-25 23:30 **wf kernel 升級結案**：`cx-wu-kern2` 三載點對齊上游 main `794d6d2`（v0.6＋lint 修正），tools 整包、kernel 段換新、本地段保留；lint 持平、上游 15 項測試綠；各 repo 已 push。此項關閉。
