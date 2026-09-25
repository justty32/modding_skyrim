## 5. Mihail 自然核心首批 4–6 件 preflight

**前置條件。** 先從自然核心候選 Pigeons、Frogs、House Cats、Ring-necked Pheasants、Crows and Ravens、Swans
凍結本晚 4–6 件；六件的 base／exact 中文版本列在
`agentctl/handoffs/done/2026-08-29/cx-mihail/REPORT.md:92`、`:93`、`:94`、`:95`、`:96`、`:97`。
具體要哪 4–6 件 repo 內尚未記錄，回家現場確認；手上必須同時有每件 base／中文 archives，以及可讀
CELL／worldspace、asset 與 records 的工具環境（`wait-user/home-setup.md:14`；`:15`）。

**實際動作。** 一次只做一件：記錄 base／中文 archive 身分並分開解壓；確認 exact 中文對版；掃
CELL／worldspace placement、asset winner 與 records；再逐一檢查新增 ingredient／food、actor stats／ability／
combat style 對 Apothecary 與現役 EnaiRim 的接觸面。每件都寫出獨立回滾單位與 winner／patch 結論
（`wait-user/home-setup.md:15`；`:16`；`:17`）。本案 xEdit／asset 掃描的具體命令 repo 內未記錄，回家現場確認；
repo 只明確要求施工前對選中子集做 xEdit／asset preflight
（`agentctl/handoffs/done/2026-08-29/cx-mihail/REPORT.md:76`）。不得加入全域 SkyPatcher 分布；它會把 hand-placed
spawns 改成另一個 topology（`wait-user/home-setup.md:16`；
`agentctl/handoffs/done/2026-08-29/cx-mihail/REPORT.md:59`；`:63`）。

**通過條件。** 每件都有可回滾單位、exact 中文對版與明列的 winner／patch 結論，CELL／asset／record 衝突及
Apothecary／Enai 接觸面全數有處置，才能排入施工（`wait-user/home-setup.md:17`；`:18`）。

**失敗退路。** 單件未過即從首批排除，不把它排入施工；若剩餘通過者仍有 4–6 件，可只交付該合格批，少於 4 件則
整批停在 preflight，不用 SkyPatcher 補數（批次範圍與 topology 邊界見 `wait-user/home-setup.md:14`、`:16`、`:18`）。

**預估時間。** 2–4 小時（本單估算）；依據是 4–6 件都要逐件做 placement／asset／record 與兩套 gameplay 語意面，
不能把一件 PASS 外推到其餘候選（`wait-user/home-setup.md:14`；`:15`；`:16`；`:17`）。

## 今晚如果只做得完一件

做 **DMK 1.5.0 人工校對版**。理由是 exact archives 的離線重建已 PASS、成品與 gate 都在 repo，寫死的
66／38／0 也已逐項對上；目前真正剩下的是替換未校對機翻層並做指定 UI／移動 smoke，完成路徑最短且能直接消除
現役 machine translation（`agentctl/handoffs/rtqa-2026-08-31/reports/dmk.md:46`；`:50`；`:60`；`:70`；`:71`；`:72`；
`agentctl/logs/mcm-helper-dmk-cht-install-2026-08-21.md:22`；`:24`；`:25`；`:26`）。
