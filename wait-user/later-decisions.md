# 日後素材／清理決定

## 夜貓－無心 3.1.0（可選精確替換）

目前 JH People 1.1.3＋NPC Plugin Chooser 2 的 536 NPC patch 已滿足方向，不阻塞整包。若仍要精確
3.1.0，只提供作者百度網盤中名稱含「人物美化」與「頭模替換」的 archive，放入既有
`/home/lorkhan/skyrim_mods/`；未取得完整資產許可不得公開重打包。見
[`相容性調查`](../wf/workflows/investigation/findings/wuxin-character-overhaul-se-ae-compatibility.md)。

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
   [裁示簡報](decision-briefs-2026-09-01.md)第 4 條。）
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
