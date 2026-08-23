# 執行紀錄

> 屬於 [mod 下載庫建檔與清理（MongoDB）](README.md)。

## 六、執行紀錄

程式在 [`mod-library/db/`](../../../../mod-library/db)（2026-08-23 統整前在 `~/notes/projects/modding/skyrim/tools/`）：`scan_mod_library.py`（1.1–1.2）、`cleanup_report.py`（1.5/1.7）、`quarantine.py`（1.6）；`check_dll_runtime.py`（1.3）因屬 runtime 診斷歸到 [`agentctl/tools/`](../../../../agentctl/tools)。schema 文件在 [`mod-library/db/mongodb-schema.md`](../../../../mod-library/db/mongodb-schema.md)。

**2026-08-11 · P1.5/P1.7 重驗完成**

`cleanup_report.py --self-test` 的 13 項 fixture 全數通過，包含 L2 的已安裝版本、漢化版本對應、Nexus gone/hidden 三條例外；對 systemd 管理的實庫（`127.0.0.1:27017`）跑唯讀 `--verify` 時 6 項 invariants 全數通過，含兩次分類結果一致。寫入路徑在 `--write-decisions` 前會先產生整庫 pymongo JSON dump。

**2026-08-04 · L3 隔離已執行**

移入 `~/skyrim_mods/.quarantine/2026-08-04/`，共 3 檔 1.61 MiB，理由是移除框架版本地雷（非回收容量）：

| 檔案 | 鎖定 runtime | 庫內保留的相容版 |
|---|---|---|
| `Fuz Ro D'oh-15109-2-3` | 1.6.640 | `Fuz Ro D'oh-15109-2-5` |
| `JContainers SE-16495-4-2-3` | 1.6.640 | `JContainers SE-16495-4-2-9` |
| `PapyrusUtil AE SE-13048-4-4` | 1.6.640 | `PapyrusUtil AE SE-13048-4-6` |

移動前自動 dump 了整份 catalogue（`backups/skyrim-mongo-2026-08-04-222103-pre-quarantine.json`）。**restore 往返已實測**：還原一個 → 確認回到原路徑且 mtime 保留 → 再次隔離 → 狀態一致。沒有驗過 restore 的隔離區只是慢動作刪除，所以這個往返測試是驗收條件而不是加分項。

**實作時撞到、值得記下的兩件事**

1. **`compatibleVersions` 陣列在宣告 AddrLib 的 plugin 裡是垃圾。** 實測 `APoseFix`、`AnimationMotionRevolution` 讀出 16 個一模一樣的 `0x01000000`（解成「1.0.0」，不是任何 Skyrim runtime）——SKSE 在版本獨立位元有設時根本不讀這個陣列，作者自然不初始化它。修法：只在 `addr_lib=false` 時採信該陣列，並過濾掉不在 1.4–1.6 範圍的值。原始值另存 `raw_compatible_versions` 供稽核。
2. **「讀不出意圖」必須判為保留，不能判為不相容。** query-only 的舊 plugin 是在 `SKSEPlugin_Query` 裡動態設定 metadata，靜態讀不到。`judge()` 只在「每個 loader-scoped plugin 都宣告了可用的 runtime 清單、且都不含 1.6.1170」時才回 False。26 個「無法判定」就是這條規則保下來的。
