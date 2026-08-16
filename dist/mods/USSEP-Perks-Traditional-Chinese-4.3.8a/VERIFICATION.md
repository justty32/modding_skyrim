# Verification

2026-08-16 靜態驗證與 scope 內 runtime 結果：PASS。

- 固定來源 SHA-256 與 USSEP 4.3.8a 契約一致；最終 ESP SHA-256 為
  `85e0fea84c13aebb313ef1b8a8efc286a84254204939d43cb96ed3a5f010257b`。
- 最終外掛可由固定來源 ESP 與 `translation-source.tsv` 逐 byte 重建。
- masters 為 USSEP 原本十個 masters，再加 USSEP 本身；houseCARL 在 Dev active order 掃描為
  0 dangling FormLink、0 missing master、0 parse failure。
- 100 筆檔案記錄（TES4 + 99 PERK）的 GRUP、record、subrecord 拓撲一致。
- 除 TES4 localized flag、99 個 `FULL` 與 99 個 `DESC` 的 string ID 外，所有 header 與非文字
  payload 完全一致；FormID、EditorID、效果、條件與 rank chain 均未改。
- `_English`／`_Chinese` 字串檔 byte-identical；99 個名稱與 99 個說明均為有效 UTF-8，數字 token
  保留，無 replacement marker、控制換行、殘留英文（允許術語 `NPC`）或常見簡體字形。
- 198 個欄位的 provenance 數量固定為 186 個 record mapping、8 個 USSEP adaptation、4 個 custom。
- houseCARL raw-file parser 可讀取最終外掛，辨識為單一類型的 99 筆 PERK；其 raw 顯示層目前會把
  localized UTF-8 當 cp1252 呈現，因此繁中文字面值以本包的 UTF-8 decoder gate 為準。
- Dev VFS 的四個 STRINGS／DLSTRINGS winner 均為本模組。scoped static report：
  `~/notes/projects/modding/skyrim/qa/reports/2026-08-16-ussep-perks-cht-static.json`。

重跑完整 gate：

```bash
python tools/verify_translation.py \
  --source '/path/to/unofficial skyrim special edition patch.esp'
```

以 `ModpackKRDev0A` 實機載入後，使用者確認其他技能系與全部天賦樹節點均為中文。唯一仍為英文的
`Destruction` 是技能分類標題，不屬於本包的 PERK `FULL`／`DESC` 範圍；使用者明確接受現況，故
不再擴大為 AVIF／介面字串 patch。
