# Verification

## 已完成的離線 gate

`tools/verify_translation.py` 對精確官方 English source 執行以下 fail-closed 檢查：

1. source ESP SHA-256 與 master 順序完全吻合；
2. TSV 恰為 70 筆：12 筆 8.20 exact FormID seed + 58 筆 CT77 custom；
3. source／output 都有 433 records，GRUP nesting、record 順序、record type、raw FormID、record flags
   （只忽略 TES4 localized bit）、version bytes 與 subrecord tag 順序完全相同；
4. 除 `FULL`／空 `DESC` 外，每一個 subrecord payload 逐 byte 相同；
5. 70 個 `FULL` 全部改為可解析的 `STRINGS` id，69 個空 `DESC` 全部改為值仍為空的
   `DLSTRINGS` id；沒有新增、刪除或搬移 record；
6. English／Chinese 的 `STRINGS` 與 `DLSTRINGS` 各自逐 byte 相同，嚴格 UTF-8 解碼通過，沒有
   U+FFFD、`???` 或常見簡體殘字；
7. fresh in-memory rebuild 與包內 ESP／四個 string tables 逐 byte 相同；
8. manifest 覆蓋所有 release 檔案（manifest 自身除外）。

已鎖定的主要輸出：

| 檔案 | bytes | SHA-256 |
|---|---:|---|
| `Remodeled Armor - Vanilla Replacer.esp` | 219679 | `55035bc7d457df0821af6a4723eaf396eb3154e9d2e62eea6e5ad68340ffda1c` |
| `*_English.STRINGS`／`*_Chinese.STRINGS` | 2201 | `8b2f6632ec77e01c025e4147b6376a29b97d4944a8c8f98d53830f4a42493dec` |
| `*_English.DLSTRINGS`／`*_Chinese.DLSTRINGS` | 905 | `c2a9bf689faebff7864db841da5a2bf0f6c904e03abc81c40c3d3a08be37f5af` |

## 明確允許的 binary 差異

- TES4 header 增加 `Localized` flag (`0x80`)；原本的 ESL flag 與其他 flags 不變。
- 70 個 inline `FULL` zstring 改成 4-byte string id。
- 69 個 inline 空 `DESC` 改成 4-byte string id；其 table value 仍是空字串。
- 上述 payload 長度改變所必須連帶更新的 record data size 與所有祖先 GRUP size。

其他 binary payload 一律不在允許清單，發生任何一 byte 差異都會 fail。

## 尚未完成

- 尚未安裝到 `Modpack-KR-Dev`，也未檢查 MO2 VFS winner／load order。
- 尚未在 `sLanguage=ENGLISH` 的遊戲內抽查 inventory、crafting、container、商店與裝備名稱。
- 尚未做啟用／停用翻譯層的 runtime rollback 對照。

這些項目不影響離線 text-only 結論，但在實機 gate 通過前不能宣稱已部署或 runtime 驗收完成。

