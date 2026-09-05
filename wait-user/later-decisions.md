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

**已裁示、但本次零刪除**（2026-09-05 19:38）：todo-04 選 B，`_grow-2026-08-31` 與
`_grow-2026-08-31-backed-out` 兩份都刪；todo-09 選 A，`_mco2bfco-2026-08-30` 與
`_mco2bfco-trash` 兩份都刪。本線只記錄裁示，四個目錄目前仍存在，交由有權執行線處理。
證據：`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-05/STATE.md:102`。

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

### Dev0A 基線存檔：使用者刻意刪了，規則要不要跟著改（2026-09-02 晚）

**判定：已裁示並執行（2026-09-04），不再等你。**
使用者 2026-09-04 對第 10 題裁 **A**：baseline pair **留著，但搬到 `instance/profiles/baselines/`**
——等於選了本節建議的 ①（留著），只是換了存放位置，避免它一直出現在遊戲的存檔清單裡。
2026-09-05 實讀：`/home/lorkhan/repo/moddings/skyrim/instance/profiles/baselines/ModpackKRDev0A.ess`（2.9 MB）與
`.../ModpackKRDev0A.skse`（6.2 KB）皆在。
證據：`instance/profiles` commit `0f64c20`（「Dev0A 基線存檔搬到 baselines/，規則與 git 保護全留」）、
母 repo commit `afb530d`（wf baseline save pair 路徑改指 `instance/profiles/baselines`）、
agentctl commit `b009076`、
`/home/lorkhan/repo/moddings/skyrim/agentctl/handoffs/home-2026-09-03/SESSION-LOG.md`（「09-04 使用者裁示」節第 10 題）。
**注意**：`check_profiles.py` 的 `BASELINE_SAVES`、`.gitignore` 白名單、`instance/profiles/README.md` 規則 4、
`wf/workflows/runtime-qa/README.md` 第 2 節這四處**沒有拿掉規則**（裁的是 ①，本來就不用拿掉），只有路徑跟著改。
另：`NEXT-SESSION.md` 的注意事項寫「`ModpackKRDev0A.ess/.skse` 已留在 `modpack-main/saves/`（git 不追蹤，正本在 `baselines/`）」
——那是遊戲啟動前要就位的執行複本，與正本不衝突。

使用者 2026-09-02 22:30 說「dev0a 存檔基線我確實刪掉了」（實機驗收期間在遊戲內刪）。dispatcher 因
`instance/profiles/tools/check_profiles.py` 把它當必要檔（缺了 promote 直接 FAIL）且 QA harness／agent 開遊戲都載它
（當晚 dsview 傳送就是 `load ModpackKRDev0A`），先從 git 覆回（`9e188e2` 之前，sha 同 README 常數），**沒有改規則**。
要問：① 留著（維持現狀，遊戲存檔清單裡會一直看到它）；② 拿掉——要一併改 `check_profiles.py` 的 `BASELINE_SAVES`、
`.gitignore` 白名單、`instance/profiles/README.md` 規則 4、`wf/workflows/runtime-qa/README.md` 第 2 節，並替 agent QA 另定基線存檔。
建議 ①。

### ~~LoreRim 打底：80 件待裁決＋借用盤點 11 題~~（2026-09-02 全部已裁示，不計 open）

**判定：2026-09-02 全部已裁示（本節原本就標 不計 open），2026-09-05 核對無新增待裁。**

LoreRim 3933 件套完三條規則（ENB／高解析度／NPC 美化）後，撞到現役已裝／已定的部分全部寫成問題進
`modpack-design/content-plan/lorerim/data/conflicts-for-ruling.csv`（80 列，`default_action` 一律 `KEEP-OURS`）。
**先答 4 件 `runtime-version` 與 5 件 `gameplay-core`**（AE 1.7.99 vs 釘版 1.6.1170、付費 AE 更新、158 件 1.7.99 DLL、
Stock Game；Requiem vs EnaiRim 凍結、吸血鬼／狼人 overhaul、perk 進程層、魔法組合、Late Loaders 整體平衡），
其餘 71 條才有意義。三隊的結論是**整包換底走不通**，可行的是把 LoreRim 當已排序的候選池，先借
城鎮／建築／地點、對話、音效三段；展開見 `modpack-design/content-plan/lorerim/adoption-draft.md`。
**裁示（2026-09-02 使用者當場，寫入 `conflicts-for-ruling.csv` 的 `ruling` 欄）**：① 維持 1.6.1170 釘版只借選型；
② **買付費 AE 升級**（連帶風險見 `home-setup.md`）；③ DLL 只對要借的件逐件找 1.6.1170 版；④ 不採 Stock Game；
⑤ 不採 Requiem；⑥ 維持不加吸血鬼／狼人 overhaul；⑦ 不換 perk 進程層；⑧ 不整組換魔法；⑨ 不採 Late Loaders。
**高解析度門檻：2K 可、4K 以上排除**（2026-09-02 使用者當場，用於 `exclusions.csv` 的 `GRAY-HIRES` 改判）。其餘 71 件不逐件裁，預設 `KEEP-OURS` 生效；下一段做「借三段」逐件盤點時再問。不併 install-plan 直到盤點完成。
**借用盤點已完成（同日 12:05）**：`modpack-design/content-plan/lorerim/borrow-plan.md` 第六節七題與 `cc-plan.md` 第六節四題待使用者，
**11 題已於同日裁示（全照調度者建議）**：灰區 12 件回家查解析度、UI 音效 2 件不要、已有同名 8 件先保留我們的、
`Lux` 家族借本體、BOS 與 Embers XD 借、Northern Roads 不借、REBUILD 先做第一二批用到的、CC 段排 AE 升級後下一輪、
USCCCP 樞紐順序可以、LoreRim 停用的 4 件 CC 不跟、Survival Mode CC 擱著。降版備援回家確認（使用者記得有）。
另裁示：**一般 retexture 整批先放著**（使用者對畫面要求不高），`exclusions.csv` 的 `GRAY-HIRES` 800 餘件不追、不進借用盤點。
裁示已寫進 `borrow-candidates.csv`／`borrow-patches.csv` 的 `ruling` 欄與兩份計畫的第七節。**本項不再 open。**
**同日 14:35 追加裁示：改走 MCO 體系**（看過 `mco-switch-estimate.md` 後決定，推翻 backlog 的 MCO→BFCO 方向）；
團隊 `mco` 產出回家遷移計畫 `modpack-design/content-plan/gameplay/mco-migration-plan-2026-09-02.md`，執行列回家清單。
**15:40 六題裁示**：Q1 配 SCAR 2（前提 1.6.1170 DLL）；Q2 不走 DXP；Q3 CPR／PGC 開線查 1.6.1170 DLL；Q4 LoreRim 155 件 moveset 全借；
Q5 11 件 `ASK` 開線查；Q6 查不到 1.6.1170 版跳過並記錄。落地在計畫第六節與 `data/mco-{moveset-queue,ask-11,dll-runtime-evidence}.csv`。

### ~~Beyond Reach 兩件灰色地帶要不要算排除區~~（已裁示，不計 open）

**判定：已裁示（兩件都留著、維持啟用、不算排除區），2026-09-05 核對無異動。**

**裁示：兩件都留著，維持啟用，不算排除區。** 2026-09-01 使用者口頭，經 `dispatcher` 轉達：
屬**缺失資產補件**而非美化，故不落排除區。無需任何 profile 變更（兩件本來就啟用中）。

以下為裁示前的原始問題與現況，保留作為判斷依據：

`lead-modpack` 2026-08-30 的三項裁示裡，只有這一項至今**查無任何裁示**
（另兩項「實機開檔」與「SIGMA 第一人稱動畫」已分別由 hdmk smoke 與 lead-grow 落地）。
它判這兩件**不落**排除區並已安裝啟用，但因為名字本身就長得像排除區（貼圖／mesh），請你看一眼：

- `Beyond Reach Missing Textures Pack 2` —— 名字是貼圖包，實際是 Beyond Reach 的**缺失資產補件**，不是美化包。
- `Beyond Reach - Improved Meshes - FOMOD` —— 「Improved Meshes」聽起來就是 mesh 精修。

**現況**：兩件都啟用中，`instance/profiles/modpack-main/modlist.txt` 第 619、662、663 行為 `+`
（662 是同組的簡中層）。**不要的話單獨停用即可，不影響其他 169 件。**
原訊息已歸檔在 [`2026-08-30 DIGEST`](../agentctl/inbox/done/2026-08-30/DIGEST.md)（`lead-modpack` 段）。

### ~~profiles 的 baseline save pair 被誤刪，要復原還是改規則~~（已裁示並執行，不計 open）

**判定：已裁示並執行；且該項已被 2026-09-04 的第 10 題裁示接續（見上面「Dev0A 基線存檔」一節），存檔正本現在在 `instance/profiles/baselines/`。**

**裁示：① 復原。** 2026-09-02 使用者於公司 session 當場裁示，並已在公司這台執行：
`instance/profiles` 自 `2b1546d`（＝`7e70ae2^`）取回
`modpack-main/saves/ModpackKRDev0A.{ess,skse}`。兩檔實測內容 sha256 與
`tools/check_profiles.py` 的 `BASELINE_SAVES` 常數相符（`fcd26d7d…`／`9545b19d…`），
`check_profiles.py` 由 `FAILED: 2 validation error(s)` 轉為 `PASS`，
`profile_workflow.py status` 亦恢復可執行。**改動仍在工作樹，尚未 commit。**

裁定依據是刪除屬意外而非決定：`.gitignore` 白名單例外、驗證器常數、
`instance/profiles/README.md` 與 `wf/workflows/runtime-qa/README.md` 都仍當它們是固定基準；
若為刻意刪除，這些會一併拿掉。兩檔是在 `7e70ae2`（2026-08-31 22:45）被 `commit -a` 掃進去的。

**衍生的 open 項已另立**：2026-09-01 的 DMK smoke 當時磁碟上沒有 baseline save，
用的不是標準基準，須回家以復原後的基準重跑——列於
[`整包 UI／中文／任務驗收`](integrated-runtime.md)。

**歷程**：`lead-hdmk` 2026-09-01 19:47 上報後依鐵律 4 未自行修；`lead-hops` 同日合併
`feat/dmk-cht-20260901` 時亦未碰（`main` 與該分支的 validation 錯誤完全相同，合併未新增退化）。

### ~~53 件停用 mod 要不要刪~~（已裁示，不計 open）

**判定：已裁示（不會重跑 NPC 外觀生成 → 刪），2026-09-05 核對無異動。**

`lead-disabled` 2026-08-30 21:05 問：**「你之後還會不會重跑 NPC 外觀生成？」**
**裁示：不會 → 刪。** 記於同日 22:2x 的 `agentctl/handoffs/opus-ops-2026-08-30/STATE.md:26-27`
（該節標題「使用者今天的裁示（既定事實，不要拿回去再問）」），2026-09-01 約 22:00 使用者於主 session 口頭重申。

執行範圍與逐件驗證在 `agentctl/handoffs/hwrap-2026-09-01/DELETE-PLAN.json`：
刪 9 件共 2.75 GiB（2 個 donor ＋ 7 件雜項）；
**`AgentBridge` 排除**——`instance/profiles/modpack-main/modlist.txt:316` 現為 `+AgentBridge`（啟用中），
刪啟用中的 mod 會弄壞 profile。

還原代價：兩個 donor 的原始壓縮檔仍在 `~/skyrim_mods/hdd/manually/character-beauty-2026-08-15/`，
**但目錄內是 CAO 轉換後資產、壓縮檔是轉換前的**，還原需重跑 CAO（540＋549 個 NIF）——這正是裁示已接受的代價。

### ~~中文層五個裁示（2026-09-01 已裁示，不計 open）~~

**判定：五題 2026-09-01 全部已裁示，2026-09-05 核對無異動。**

來源是 2026-08-28 的續行清單（已封存，只剩這條活著）；
逐項細節在 [`中文層覆蓋總表`](../modpack-design/content-plan/zh-layer/zh-layer-coverage-master-2026-08-28.md)的
「等使用者裁示」節：

1. ~~**Bandolier NPC 層三選一**~~ **裁示：B —— 裝 NPC 層並做小型 forward patch，保留 NPC 分發與中文；
   patch 依 realistic variant forward 83＋23 兩批。**（2026-09-01，使用者當場口頭裁示；見
   [裁示簡報](decision-briefs-2026-09-01.md)第 4 條。）**2026-09-01 撤銷：Bandolier 併入 clothes purge，第 4 節作廢。**
2. ~~**Reforging 綁 SkyPatcher**~~ **裁示：A —— 接受中文層綁定 SkyPatcher，沿用現役 7.0.0 框架。**
   （2026-09-01，使用者當場口頭裁示；見[裁示簡報](decision-briefs-2026-09-01.md)第 5 條。）
3. ~~**AA（Armor Add-on）三個同版中文層選哪個流派**~~ **裁示：A —— 採 `72518` 已驗 DAR 簡中 exact 層。**
   （2026-09-01，使用者當場口頭裁示；見[裁示簡報](decision-briefs-2026-09-01.md)第 6 條。）
4. ~~**`sLanguage` 要不要動**~~ **裁示：A —— 維持 `ENGLISH`，只局部修正 `_chinese.txt` 檔名例外。**
   （2026-09-01，使用者當場口頭裁示；見[裁示簡報](decision-briefs-2026-09-01.md)第 7 條。）
5. ~~**Steam 2.5MB 補丁（TargetBuild 24914197）接不接受**~~ **裁示：A —— 不收補丁，維持
   1.6.1170 釘版與 Steam 離線。**（2026-09-01，使用者當場口頭裁示；見
   [裁示簡報](decision-briefs-2026-09-01.md)第 8 條。）

### ~~2026-08-29 調查線留下的裁示~~

**判定：三條調查線的裁示 2026-09-01 全部落地，2026-09-05 核對無異動。**

各線的完整結論在 [`agentctl DIGEST`](../agentctl/inbox/done/2026-08-29/DIGEST.md)，報告在 `agentctl/handoffs/done/2026-08-29/<線名>/REPORT.md`。

### ~~隨從凍結要不要維持（cx-fdlg）~~（已裁示，不計 open）

Sofia／Recorder／Auri 的 dialogue 生態 GO 2／DEFER 5／NO-GO 13；Auri 技術與中文都可行，只因 follower 凍結判 NO-GO。
**裁示：B —— 有限解凍，例外只開 Auri＋現役 VIGILANT，並採 Sofia Hub 選配式 preflight／No Bump，
不順手引入第二名新 follower。**（2026-09-01，使用者當場口頭裁示；見
[裁示簡報](decision-briefs-2026-09-01.md)第 2 條。）

### ~~Mihail 生物要哪個方向（cx-mihail）~~（已裁示，不計 open）

295 件 Creatures and Mounts 裡挑出 16 件低耦合 standalone，10 件有對版中文層（9 CHS／1 CHT）。
**裁示：A —— 首批採自然核心 4–6 件、原生 hand-placed topology、接受 exact CHS，以最小可回滾批次
先驗生態密度。**（2026-09-01，使用者當場口頭裁示；見
[裁示簡報](decision-briefs-2026-09-01.md)第 3 條。）
