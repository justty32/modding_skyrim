# WAIT_USER — 等待使用者的事

只列需要使用者親自操作、實機驗收、外部環境或素材才能繼續的 open 項；完成即從所屬清單移除，
不在這裡保存完成歷史。

> 唯一現役 MO2 profile 是 `modpack-main`。子文件中的舊 profile 名稱只描述歷史證據，不能切換或
> 當成現行操作指令。

| 類別 | open | 清單 |
|---|---:|---|
| 回家下載／重建 | 6 | [`wait-user/home-setup.md`](wait-user/home-setup.md) |
| 今晚裁決簡報（2026-09-02） | 0 | [wait-user/decision-briefs-2026-09-02.md](wait-user/decision-briefs-2026-09-02.md)（15 題全部已裁示並落地） |
| 整包 UI／中文／任務驗收 | 12 | [`wait-user/integrated-runtime.md`](wait-user/integrated-runtime.md) |
| 獨立功能驗收 | 5 | [`wait-user/feature-runtime.md`](wait-user/feature-runtime.md) |
| 日後素材／清理決定 | 5 | [`wait-user/later-decisions.md`](wait-user/later-decisions.md) |
| 版本控制收線 | 0 | [本檔下節](#push-排程) |

歷史導流：[`decision-briefs-2026-09-01.md`](wait-user/decision-briefs-2026-09-01.md) 的 10 題均已裁示；
[`home-runbook-2026-09-01.md`](wait-user/home-runbook-2026-09-01.md) 是當日執行快照，未完事項已由上表現役清單承接，兩檔均不另計數。

## Push 排程

2026-09-03 14:50 使用者已放行 promote 與 push，profiles main 已 promote，當日各 repo push 已執行；現況見
[`agentctl/handoffs/home-2026-09-03/STATE.md`](agentctl/handoffs/home-2026-09-03/STATE.md)。

歷史：2026-09-01 的一次性 push 排程已完成。

`wf-lint.sh` 兩個缺陷已由使用者裁示**現在就修**，並已派 `cx-kern1` 承接（交接書
`agentctl/handoffs/kern-2026-08-30/HANDOFF-cx-kern1.md`）；不再列為等待使用者項目。
