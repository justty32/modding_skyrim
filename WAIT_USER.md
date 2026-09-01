# WAIT_USER — 等待使用者的事

只列需要使用者親自操作、實機驗收、外部環境或素材才能繼續的 open 項；完成即從所屬清單移除，
不在這裡保存完成歷史。

> 唯一現役 MO2 profile 是 `modpack-main`。子文件中的舊 profile 名稱只描述歷史證據，不能切換或
> 當成現行操作指令。

| 類別 | open | 清單 |
|---|---:|---|
| 回家下載／重建 | 7 | [`wait-user/home-setup.md`](wait-user/home-setup.md) |
| 整包 UI／中文／任務驗收 | 10 | [`wait-user/integrated-runtime.md`](wait-user/integrated-runtime.md) |
| 獨立功能驗收 | 5 | [`wait-user/feature-runtime.md`](wait-user/feature-runtime.md) |
| 日後素材／清理決定 | 3 | [`wait-user/later-decisions.md`](wait-user/later-decisions.md) |
| 版本控制收線 | 0 | [本檔下節](#push-排程) |

## Push 排程

**2026-09-01 `hvfm` 收線待推（3 個 commit，皆 fast-forward，`ahead 1`）**：
`modpack-design` `0e4a19d`、`agentctl` `ad84670`、母 repo gitlink `dd4a5ca`。
內容是「語音隨從改造」project 成立與盤點入檔，零施工。
`dispatcher` 轉達使用者要推，但**轉達不等於使用者本人確認**（鐵律 2 的授權來源），
所以本線只 commit 未 push。工作**沒有遺失風險**——三個 commit 都已落在本機 git。
要推就三行：各 repo `git push origin main`（先兩個子 repo，再母 repo）。


1. ~~**裁示：等全部現役線真正收完後一次推。** 先由 `dispatcher` 對帳各子 repo 的 commit、dirty
   worktree 與母 repo gitlink；對帳完成後，再請使用者當場確認是否 push。~~ **已完成（2026-09-01）**。

`wf-lint.sh` 兩個缺陷已由使用者裁示**現在就修**，並已派 `cx-kern1` 承接（交接書
`agentctl/handoffs/kern-2026-08-30/HANDOFF-cx-kern1.md`）；不再列為等待使用者項目。
