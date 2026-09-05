# WAIT_USER — 等待使用者的事

只列需要使用者親自操作、實機驗收、外部環境或素材才能繼續的 open 項；判定已完成的移到各子檔末尾的
「已完成（封存）」節並附證據路徑，**不從檔案裡刪掉**。

> 唯一現役 MO2 profile 是 `modpack-main`。子文件中的舊 profile 名稱只描述歷史證據，不能切換或
> 當成現行操作指令。

> **數字重算／逐 hunk 稽核日期：2026-09-05**（`cx-tidy-b-close` 對照 09-04／09-05 的 logs、inbox、handoff 與實體產物重算）。
> 對照基準：`instance/profiles` 的 `modpack-main` 內容基準 `5f47044`（repo HEAD `85d71da` 只新增 `dsport-dev`）、
> `modlist.txt` 1379 行／啟用 1278、`plugins.txt` 874 行／啟用 851。
> 更即時的一頁式現況見 [`agentctl/status/STATUS.html`](agentctl/status/STATUS.html)（每次 `python3 agentctl/status/build_status.py` 重跑現抓）。

| 類別 | open | 前次 | 清單 |
|---|---:|---:|---|
| 回家下載／重建 | 3 | 6 | [`wait-user/home-setup.md`](wait-user/home-setup.md) |
| 今晚裁決簡報（2026-09-02） | 0 | 0 | [wait-user/decision-briefs-2026-09-02.md](wait-user/decision-briefs-2026-09-02.md)（15 題全部已裁示並落地） |
| 整包 UI／中文／任務驗收 | 9 | 12 | [`wait-user/integrated-runtime.md`](wait-user/integrated-runtime.md) |
| 獨立功能驗收 | 5 | 5 | [`wait-user/feature-runtime.md`](wait-user/feature-runtime.md) |
| 日後素材／清理決定 | 4 | 5 | [`wait-user/later-decisions.md`](wait-user/later-decisions.md) |
| 版本控制收線 | 0 | 0 | [本檔下節](#push-排程) |

**2026-09-05 這輪判定為「其實已完成／已裁示」而移進封存節的十項**（每項在子檔內都附證據路徑）：
AE DLC 授權確認與 CC 第二輪、Mihail 自然核心首批、DMK 1.5.0 人工校對版（以上在 `home-setup.md`）；
EnaiRim Batch 7 終態 gate（抽查對象 Audugan／Valravn 已不在載入序）、modlist 優先度修復的實機驗收
與 Missives 兩條裁示衝突（以上在 `integrated-runtime.md`）；Dev0A 基線存檔規則（`later-decisions.md`）；
另有三項原本就標「不計 open」但仍混在 open 區的，一併歸位。

**縮小範圍但仍 open 的四項**：LoreRim 借用後續 6 題→3 題、GO19 剩餘 5 項→2 項、
四個首次生效中文層→只剩 2 個（At Your Own Pace 全套已停用、The Choice is Yours 繁中層已停用）、
staging 清理 4 條路徑→3 條已自行消失。

**注意：`wait-user/feature-runtime.md` 的 Simonrim Batch 4E／4A／4M/P 三節經逐個實讀後全部仍有效**
（Thaumaturgy 1.5、Apothecary 1.3.9、Mysticism 2.4.2、Adamant 5.9.2 都還在啟用清單），
過期的只有行號與框架名（BFCO→MCO），已就地更正，不是整批作廢。

歷史導流：[`decision-briefs-2026-09-01.md`](wait-user/decision-briefs-2026-09-01.md) 的 10 題均已裁示；
[`home-runbook-2026-09-01.md`](wait-user/home-runbook-2026-09-01.md) 是當日執行快照，未完事項已由上表現役清單承接，兩檔均不另計數。

## Push 排程

2026-09-03 14:50 使用者已放行 promote 與 push，profiles main 已 promote，當日各 repo push 已執行；現況見
[`agentctl/handoffs/home-2026-09-03/STATE.md`](agentctl/handoffs/home-2026-09-03/STATE.md)。

歷史：2026-09-01 的一次性 push 排程已完成。

`wf-lint.sh` 兩個缺陷已由使用者裁示**現在就修**，並已派 `cx-kern1` 承接（交接書
`agentctl/handoffs/kern-2026-08-30/HANDOFF-cx-kern1.md`）；不再列為等待使用者項目。
