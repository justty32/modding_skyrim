# Verification

2026-08-16 靜態驗證結果：PASS。

- 最終外掛可由固定 SHA-256 的英文來源 patch 與 TSV 逐 byte 重建。
- masters 保持 `Skyrim.esm`、`Update.esm`、`ConstellationsNewSkills.esp`。
- 45 筆檔案記錄（TES4 + 44 PERK）的 GRUP、record、subrecord 拓撲一致。
- 除 TES4 localized flag、44 個 `FULL` 與 44 個 `DESC` 的 string ID 外，所有 header 與非文字 payload 完全一致。
- `_English`／`_Chinese` 字串檔 byte-identical；44 個名稱、44 個說明均為有效 UTF-8，數字 token 保留，無 replacement marker 或常見簡體字形。
- houseCARL raw-file parser 可讀取最終外掛，辨識為 44 筆 PERK 並正確保留 rank chain。houseCARL 的 raw 顯示層目前會把 localized UTF-8 當 cp1252 呈現，因此繁中文字面值以本包的 UTF-8 decoder gate 為準。

重跑完整 gate：

```bash
python tools/verify_translation.py \
  --source '/path/to/Constellations Perk Nodes Traditional Chinese 1.0.2 Source.esp'
```

尚需實機確認：三棵自訂技能樹的節點名稱與說明皆顯示繁中，包含多 rank 節點；點選與升級行為不變。
