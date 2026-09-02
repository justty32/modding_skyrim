# 日後素材／清理決定

## 夜貓－無心 3.1.0（可選精確替換）

目前 JH People 1.1.3＋NPC Plugin Chooser 2 的 536 NPC patch 已滿足方向，不阻塞整包。若仍要精確
3.1.0，只提供作者百度網盤中名稱含「人物美化」與「頭模替換」的 archive，放入既有
`/home/lorkhan/skyrim_mods/`；未取得完整資產許可不得公開重打包。見
[`相容性調查`](../wf/workflows/investigation/findings/wuxin-character-overhaul-se-ae-compatibility.md)。

## ~~Beyond Reach 兩件灰色地帶要不要算排除區~~（已裁示，不計 open）

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

## ~~profiles 的 baseline save pair 被誤刪，要復原還是改規則~~（已裁示並執行，不計 open）

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

## ~~53 件停用 mod 要不要刪~~（已裁示，不計 open）

`lead-disabled` 2026-08-30 21:05 問：**「你之後還會不會重跑 NPC 外觀生成？」**
**裁示：不會 → 刪。** 記於同日 22:2x 的 `agentctl/handoffs/opus-ops-2026-08-30/STATE.md:26-27`
（該節標題「使用者今天的裁示（既定事實，不要拿回去再問）」），2026-09-01 約 22:00 使用者於主 session 口頭重申。

執行範圍與逐件驗證在 `agentctl/handoffs/hwrap-2026-09-01/DELETE-PLAN.json`：
刪 9 件共 2.75 GiB（2 個 donor ＋ 7 件雜項）；
**`AgentBridge` 排除**——`instance/profiles/modpack-main/modlist.txt:316` 現為 `+AgentBridge`（啟用中），
刪啟用中的 mod 會弄壞 profile。

還原代價：兩個 donor 的原始壓縮檔仍在 `~/skyrim_mods/hdd/manually/character-beauty-2026-08-15/`，
**但目錄內是 CAO 轉換後資產、壓縮檔是轉換前的**，還原需重跑 CAO（540＋549 個 NIF）——這正是裁示已接受的代價。

## BG3 場景佈局實檔驗證

有合法遊戲資料時，以小型 `Levels/*.lsf` 做 `.lsf → .lsx`，記錄位置／旋轉／尺度／resource identity
能否無損對映 ModForge placements，再決定是否開 converter/spec；沒有實檔前不宣稱 pipeline 可行。
見 [`port-source-survey`](../analysis/port-source-survey/README.md)。

## 中文層五個裁示（2026-09-01 已裁示，不計 open）

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

## 2026-08-29 調查線留下的裁示

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
