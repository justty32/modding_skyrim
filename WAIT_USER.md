# WAIT_USER — 等待使用者的事

只列需要使用者親自操作、實機驗收、外部環境或素材才能繼續的 open 項；完成即從所屬清單移除，
不在這裡保存完成歷史。

> 唯一現役 MO2 profile 是 `modpack-main`。子文件中的舊 profile 名稱只描述歷史證據，不能切換或
> 當成現行操作指令。

| 類別 | open | 清單 |
|---|---:|---|
| 回家下載／重建 | 3 | [`wait-user/home-setup.md`](wait-user/home-setup.md) |
| 整包 UI／中文／任務驗收 | 8 | [`wait-user/integrated-runtime.md`](wait-user/integrated-runtime.md) |
| 獨立功能驗收 | 6 | [`wait-user/feature-runtime.md`](wait-user/feature-runtime.md) |
| 日後素材／清理決定 | 12 | [`wait-user/later-decisions.md`](wait-user/later-decisions.md) |
| 版本控制收線 | 1 | [本檔下節](#push-排程) |

## Push 排程

1. **裁示：等全部收線後一次推。** `modpack` 還在裝、`dl` 還在抓、`dsport3` 還在改，現在 commit
   會抓到中間狀態；三隊收線後由 `dispatcher` 整理成乾淨的 commit 再推，母 repo 的 gitlink 一次對齊。
   **未推清單**：`projects/darksouls-port` ahead 2、`projects/ModForge` ahead 2、`mod-library` 有 9 個
   新漢化層未 commit、`instance` 有 100＋件新裝 mod 未 commit。

`wf-lint.sh` 兩個缺陷已由使用者裁示**現在就修**，並已派 `cx-kern1` 承接（交接書
`agentctl/handoffs/kern-2026-08-30/HANDOFF-cx-kern1.md`）；不再列為等待使用者項目。
