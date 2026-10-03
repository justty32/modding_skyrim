# movesets — 招式配置：從挑招到進遊戲生效

[WORKFLOWS](../../WORKFLOWS.md)｜[INDEX](../../INDEX.md)

把使用者在姿態配置頁挑的招（或貼的變更單）套進 MCOI 姿態格／DAR 覆蓋層，模擬驗證、部署、煙霧，最後重發配置頁。工具在 agentctl 的 `tools/movesets/`（private，索引見該目錄 README），MO2 與煙霧共用腳本在 `instance/tools/`。

**何時用**：「我在配置頁挑好了／貼變更單」「這格換成 X」「要專屬裝備的招強制發動」「按方向攻擊被別套搶走」。
**何時不用**：裝新的招式 mod 本體 → [nexus-intake](../nexus-intake/README.md) 再接 [profile-change](../profile-change/README.md)；招式動畫 T 字／CTD 查因 → [investigation](../investigation/README.md)（先看 OAR log 與 crash log）。

## Done when

下表每列都填滿，且數字等於基準：

| 驗收 | 基準 | 出處 |
|---|---|---|
| 其他格主招變動 | 0 | `winner_diff.py --cells <這輪的格>` exit 0 |
| 方向搶格（主招兩檔跨套） | 0 | `ktsim.py` 的 `cross-mod` |
| 入侵 | 16（持盾衝刺 INTRUSION:LEFT-PARTIAL） | `intrusion_scan.py` |
| 模擬＝實套 | 逐位元組相同 | 套用後重掃的 scan 對 `--simulate` 輸出 |
| MO2 開關一輪 | `selected_profile=modpack-main`、指定 plugin 有 `*` | `instance/tools/mo2_cycle_verify.sh` 全 PASS |
| 主選單煙霧 | OAR [E] 0／caching 0／[W] 255，無新 crash log | `instance/tools/skse_smoke.sh` 全 PASS |
| 配置頁 | 新版已發布、db picks 已同步 | Artifact 版號＋db 文件版號寫進 REPORT |

## 流程

### 1. 讀變更單

`apply_change_order.py <單> --dry-run` 分出 swap／add／clear／stale；stale（單上的舊值≠現況）先回報，不硬套。只挑招沒附單時，直接列成「格 → nn-nexusid」。

### 2. 掃現況

`movecond.py`（會先跑 `oar_scan.py`＋`intrusion_scan.py`）產 scan／home／intr／movecond 四檔到 `$MOVECOND_TMP`。快取 `$ESPDB_CACHE` 過期就刪掉重建。

### 3. 閘門判斷

`force_gates.py --scan … --mod <nn-id>` 看來源每個子資料夾要不要專屬裝備（拆什麼、拆完 level）。判準：玩家、無姿態、拿同類一般武器就會動＝過；只認特定物品＝閘門。level 為 `ok` 的直接套；`unconvertible`（DAR 轉不了 OAR）不自動套，列進 REPORT。

### 4. 模擬

來源本來就不綁裝備的一般換招，照 meleecond 各輪做法換 MCOI 格的攻擊類 hkx（條件不動；目前沒有通用腳本，可借 `apply_force.py` 的 plan／simulate 只放 base）。要強制發動的寫進 `force_picks.json`（新的一輪加 `round` 與 rounds 一列），`apply_force.py --scan … --simulate --round <rN> --out after.json`。

`winner_diff.py before.json after.json --cells …`：其他格必須 0 變；這幾格的缺檔回退列在 diff 裡，寫進 REPORT。

`ktsim.py <TMP>`（主招兩檔）看 `cross-mod`；`intrusion_scan.py after.json` 看入侵仍 16。

### 5. 搶格排除（cross-mod > 0 才做）

`iterate_exclusions.py <TMP>` 反覆推規則到 0，再 `apply_exclusions.py`（dry-run）確認清單。只排除「被搶格的右手武器」，不動其他格。

### 6. 套用

取鎖（先 desktop 再 game）、MO2／遊戲關著、`profiles/` 已 commit。`apply_force.py --apply --round <rN>`／`apply_exclusions.py --apply`；兩者都先備份並寫 manifest。套完重掃，scan 要等於模擬輸出。

### 7. MO2 循環驗證

先 `mo2_cycle_verify.sh --snapshot base.json`，再跑一輪開關 MO2 比對（MO2 首開會掉新 plugin 的 `*`，關掉後一定要重驗）。

### 8. 主選單煙霧

`skse_smoke.sh`（`launch-mo2.sh --skse` 開到主選單、收 log、關遊戲）。崩了先跑 `agentctl/tools/snapshot_skse_logs.sh` 再開 MO2。

### 9. 頁面

`patch_pick_page.py <scan> <r8.json>` 更新 `PICK-STANCES.html` 的 DATA；需要時 `build_movesets_all.py` 重產總覽頁。重發前先 Artifact **read** 線上版（不然會被拒），再 publish 到同一個 URL；db 的 `picks/<武器>` 文件同步改成新選擇。

### 10. 還原方式寫進 REPORT

force 是 `revert.sh r2 --apply` 再 `r1`（從最後一輪往回退）；排除層是 `apply_exclusions.py --revert`；stances-plan 隨 manifest 一起還原；配置頁退版＝git 還原 html 後重發。

### 11. commit

agentctl、instance/profiles、母 repo 各自 commit，只 `git add` 明確路徑；跑 `agentctl/tools/hygiene_check.py staged`；不 push。

## 交接

- 需要使用者實機揮刀驗收 → [WAIT_USER](../../../WAIT_USER.md) 一行（逐格列「應該出現／不該出現」的招）；跨 session → [SESSION-LOG](../../../SESSION-LOG.md)。
- 動到 profile（加 mod、勾 plugin）的部分照 [profile-change](../profile-change/README.md)；實機測試照 [runtime-qa](../runtime-qa/README.md)。
