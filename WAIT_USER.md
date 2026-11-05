# WAIT_USER — 等待使用者的事

只列需要使用者親自操作、實機驗收、外部環境或素材才能繼續的 open 項；子檔規則見 [wait-user/README.md](wait-user/README.md)（結案項直接刪）；增減後跑 `tools/waituser_count.py --check` 核對。唯一現役 MO2 profile 是 `modpack-main`。

| 類別 | open | 清單 |
|---|---:|---|
| 回家下載／重建 | 8 | [`wait-user/home-setup.md`](wait-user/home-setup.md) |
| 整包 UI／中文／任務驗收 | 12 | [`wait-user/integrated-runtime.md`](wait-user/integrated-runtime.md) |
| 獨立功能驗收 | 13 | [`wait-user/feature-runtime.md`](wait-user/feature-runtime.md) |
| 日後素材／清理決定 | 5 | [`wait-user/later-decisions.md`](wait-user/later-decisions.md) |
| 版本控制收線 | 0 | [本檔下節](#push-排程) |

## Push 排程

目前沒有等使用者放行的 push 排程。2026-10-21 使用者已放行母 repo 與 DSP／houseCARL／agentctl 三個修復分支；範圍與結果見 [離線成果與收尾](wf/user/2026-10-21-offline-fixes.md#收尾與下次續接)。
