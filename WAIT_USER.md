# WAIT_USER — 等待使用者的事

只列需要使用者親自操作、實機驗收、外部環境或素材才能繼續的 open 項；完成即從所屬清單移除，
不在這裡保存完成歷史。

> 唯一現役 MO2 profile 是 `modpack-main`。子文件中的舊 profile 名稱只描述歷史證據，不能切換或
> 當成現行操作指令。

| 類別 | open | 清單 |
|---|---:|---|
| 回家下載／重建 | 9 | [`wait-user/home-setup.md`](wait-user/home-setup.md) |
| 今晚裁決簡報（2026-09-02） | 15 | [wait-user/decision-briefs-2026-09-02.md](wait-user/decision-briefs-2026-09-02.md) |
| 整包 UI／中文／任務驗收 | 11 | [`wait-user/integrated-runtime.md`](wait-user/integrated-runtime.md) |
| 獨立功能驗收 | 5 | [`wait-user/feature-runtime.md`](wait-user/feature-runtime.md) |
| 日後素材／清理決定 | 2 | [`wait-user/later-decisions.md`](wait-user/later-decisions.md) |
| 版本控制收線 | 0 | [本檔下節](#push-排程) |

## Push 排程

1. ~~**裁示：等全部現役線真正收完後一次推。** 先由 `dispatcher` 對帳各子 repo 的 commit、dirty
   worktree 與母 repo gitlink；對帳完成後，再請使用者當場確認是否 push。~~ **已完成（2026-09-01）**。

`wf-lint.sh` 兩個缺陷已由使用者裁示**現在就修**，並已派 `cx-kern1` 承接（交接書
`agentctl/handoffs/kern-2026-08-30/HANDOFF-cx-kern1.md`）；不再列為等待使用者項目。
