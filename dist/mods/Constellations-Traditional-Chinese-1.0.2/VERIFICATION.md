# Verification — Constellations Traditional Chinese 1.0.2

- 驗證日期：2026-08-15
- 結果：PASS
- 遊戲／MO2 啟動：未執行
- 實機部署：未執行

## 來源與範圍檢查

- 上游 `ConstellationsNewSkills_ENGLISH.txt`：UTF-16 LE with BOM、CRLF、6 筆、最後一筆無換行。
- 上游 SHA-256：`69646dc81195b7e4faeb81cc88ddecf76af7a2b1a7467af2d26e45eb3aa0caa4`。
- `Athletics.json`、`HandToHand.json`、`Sorcery.json` 的 `name`／`description` 共引用相同六個 key；本產物逐筆保留名稱與順序。
- 未發現 Constellations 自帶 MCM 檔。
- houseCARL 對 `ConstellationsNewSkills.esp` 的唯讀掃描找到 564 筆 touched records，其中包含大量內嵌英文名稱／說明；這些不是 Interface translation key，故不納入本次 text-only override。

## 產物檢查

執行：

```bash
python tools/verify_translation.py --source "/path/to/Constellations/Interface/Translations/ConstellationsNewSkills_ENGLISH.txt"
sha256sum -c MANIFEST.sha256
```

結果：

```text
PASS reviewable source: UTF-8, 6 unique keys, exact order
PASS game asset: UTF-16 LE BOM, CRLF, no final newline, 6 exact rows, sha256=22d2869cf347a67d58d0d42c58af03e3c5ac71d4355cc0ecbff45f3f4c72bb85
PASS upstream parity: exact source hash and key/order match
PASS manifest: 6 files match
RESULT: PASS
```

`sha256sum -c MANIFEST.sha256` 的六個項目全部為 `OK`。

## Repo 回歸檢查

```text
python -m unittest discover -s tests -v
Ran 6 tests in 0.004s — OK

python scripts/check_markdown_links.py
Markdown links OK: 429 file(s), 580 local link(s)

git diff --check
PASS
```

## 未修改部署端的證據

工作前後對現役 `Modpack-KR-Dev` profile 的三個核心檔案重算 SHA-256，結果相同：

```text
2a4d3184e9ae206170476ab98f5528d8dab7f08d14b05cd2c19dd65d4db94b1e  modlist.txt
51881b3b1f7733ee82e9a3c7a64a31932ad14b8f8096dac4df0de7c112c0d0c6  plugins.txt
f88d26b54c2ec2b9c4b2cbac4d146b2c8ac9daf07c9c74ef52c94b00139f7768  loadorder.txt
```

這只能證明上述三檔未被本工作改動；沒有宣稱遊戲內顯示已經過實機驗收。
