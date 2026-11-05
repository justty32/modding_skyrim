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

## PoE 星盤：提供施法速度參考 mod（2026-11-03）

你 11-03 對星盤機制的裁示說「施法速度我之後找個mod給你參考」。在你提供之前，施法速度的節點照舊轉成毀滅增傷＋減耗，不做真的施法速度。給 mod 名稱或 Nexus 連結即可，agent 再評估落地方式。見
[`poe-skyrim-mapping` mechanics](../wf/workflows/plans/poe-skyrim-mapping/mechanics.md#要做的機制與切片)。

## PoE 星盤：延後的 10 個 keystone 逐個討論（2026-11-03）

你說「這些自創規則啥的，我們可以後續慢慢更新加上，不急著做」。9 個自創案、Supreme Ego（待重新設計）與 Vaal Pact 的「吸血鬼之約」備案，等你有空時逐個討論；在那之前用 5 份通用加成佔位，不擋施工。見
[`poe-skyrim-mapping` keystones](../wf/workflows/plans/poe-skyrim-mapping/keystones.md#延後的-10-個)。

## 八職業×三子類：24設計樣板與新參數過目（2026-11-04）

依你明確選定的24型範圍，[完整過目頁](../wf/user/2026-11-04-all-classes.md)已補齊240規則、真圖與正負情境，原刻印／浪潮／守衛契約保留。新強度、成本與期限尚待你過目；可先挑想調整或優先驗可行性的子型。本項是新增完整24型設計交付的過目，不重開已完成的浪潮命名／前場看稿，也不把看稿當source或部署授權。

## MEMORY.md 改成指向 wf/lessons/ 的指標（2026-10-24 積壓，2026-11-05 從 agentctl SESSION-LOG 移入）

使用者 2026-10-24「這些都記下來，我下次做」留下的積壓：`MEMORY.md` 改成指向 `wf/lessons/` 的指標——memmig 搬家本體已做完（183 個小節、原檔全在），唯一剩的就是這個動作，`wf/lessons/README.md` 已寫明由頂層處理；在那之前兩邊並存、記憶目錄較新。
