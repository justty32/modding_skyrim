# AI Overhaul 1.9 NPC 名稱正體中文覆寫

這是 `AI Overhaul.esp` 1.9.0.0 的精確版本、Dev-first 名稱覆寫。AI Overhaul 覆寫原版 NPC
record 時把 `FULL` 名稱寫成英文，會蓋過目前 `Skyrim Traditional Chinese 8.20 Core and Fonts`
的 localized strings；本包把能由同一份現役正體核心字串可靠還原的 423 個名稱寫回同名 ESP。

只包含：

```text
AI Overhaul.esp
```

不改 AI package、scene、dialogue、combat、inventory、appearance、VMAD、FormLink 或其他資料。
一個來自 Fishing master 的 NPC 沒有本機權威正體 strings，刻意保留英文而不猜譯。

## 重建與驗證

```bash
python tools/name_translation_pipeline.py verify \
  --source "/path/to/AI Overhaul.esp" \
  --game-data "/path/to/Skyrim Special Edition/Data" \
  --cht-strings "/path/to/Skyrim Traditional Chinese 8.20 Core and Fonts/Strings"
sha256sum -c MANIFEST.sha256
```

來源與 gate 見 [SOURCE.md](SOURCE.md) 與 [VERIFICATION.md](VERIFICATION.md)。
