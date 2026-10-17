# wait-user — 等使用者項目的子檔

[WAIT_USER.md](../WAIT_USER.md) 是 hub，只放計數表；各類 open 項的內容在本目錄。

## 規則

- 只收需要使用者親自操作、實機驗收、外部環境或素材才能繼續的 open 項。
- 判定已完成的項目從 md 移到同名 `*-closed.json`（契約 `wf-table/1`），附關閉日期與證據路徑，**不直接刪掉**。
- hub 的計數變動與敘述（新增／結案／重算說明）寫進 `hub-notes-closed.json`，hub 本身不寫敘述。
- 唯一現役 MO2 profile 是 `modpack-main`；子檔中的舊 profile 名稱只描述歷史證據，不能切換或當成現行操作指令。
- 已全部裁示、只剩歷史價值的整份文件移進 [archive/](archive/README.md)，活文件不連進去。

## 子檔

<!-- wf-nav -->
| 檔案 | 內容 | 已完成項 |
|---|---|---|
| [home-setup.md](home-setup.md) | 回家下載／重建 | `home-setup-closed.json` |
| [integrated-runtime.md](integrated-runtime.md) | 整包 UI／中文／任務驗收（細節在 `integrated-runtime/`） | `integrated-runtime-closed.json` |
| [feature-runtime.md](feature-runtime.md) | 獨立功能驗收（細節在 `feature-runtime/`） | 檔內「已完成（封存）」節 |
| [later-decisions.md](later-decisions.md) | 日後素材／清理決定 | `later-decisions-closed.json` |
| [hub-notes-closed.json](hub-notes-closed.json) | hub 的增減紀錄與 2026-09-05 重算說明 | — |
