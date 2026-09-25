## GO19 新內容要不要改用新周目正式驗收

ECSS 作者要求全新存檔，Gray Cowl 周年版是大改替換件，Faehaven 也建議新存檔；2026-09-03 用 Dev0A 舊存檔時第一局
79 秒後 crash，第二局正常，且今天新增的 11 個 plugin 沒出現在 crash 現場。A＝現在開新周目，把這三件正式驗收；
B＝繼續舊周目，但接受之後的 crash／任務狀態不能歸咎於部署。證據：`agentctl/handoffs/home-2026-09-03/inst2/REPORT.md`。

## Auri＋現役 VIGILANT 有限解凍整合

**裁示：B —— follower 只有限解凍 Auri＋現役 VIGILANT，並採 Sofia 選配 preflight／No Bump。**
（2026-09-01，使用者當場口頭裁示；見[裁示簡報](../decision-briefs-2026-09-01.md)第 2 條。）回家以 Auri
2.2 本體、exact 2.2 中文、VIGILANT commentary 0.2／tweaks 做 winner preflight 與部署；Auri 不匯入
NFF，Sofia 的 RDO／AI Overhaul／No Bump 選配須重新核對現役 clothing binding fix winner。
**通過**＝離線 winner／版本／中文層無回滾，再實機驗 Auri 招募與跟隨、VIGILANT commentary 條件／
字幕、Sofia 選配及既有 VIGILANT／Sofia 行為都無新衝突；不得藉此加入第二名新 follower。

**狀態（2026-09-05 實讀，本項仍 open 但只剩實機那半）**：檔案層都已到位——
`/home/lorkhan/repo/moddings/skyrim/instance/profiles/modpack-main/modlist.txt:735`＝`+Song Of The Green (Auri Follower) 2.2`（啟用），
中文層 `:732`／`:733`／`:734` 三行皆 `+`；`plugins.txt:734`＝`*018Auri.esp`（啟用）。
VIGILANT 1.8.2 四層仍啟用（`modlist.txt:357`／`:358`／`:360`／`:421`）；
Sofia 的 clothing binding fix winner 仍在（`modlist.txt:417`／`:418`、`plugins.txt:599`＝`*SofiaClothingBindingFixDev.esp`）。
**還沒做的是實機那一段**（Auri 招募／跟隨、VIGILANT commentary 條件與字幕、Sofia 選配無新衝突）。
另註：`/home/lorkhan/repo/moddings/skyrim/agentctl/status/todo/20-Auri到底還做不做.md` 有一份平行筆記，兩處講同一件事。

