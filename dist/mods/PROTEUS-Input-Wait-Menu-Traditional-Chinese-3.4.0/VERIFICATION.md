# Verification — PROTEUS Input Wait Menu Traditional Chinese 3.4.0

## Commands run

```bash
python tools/build_translation.py
python tools/verify_translation.py --source "/home/lorkhan/games/mod-organizer-2-skyrimspecialedition/modorganizer2/mods/PROTEUS/Interface/translations/Input Wait Menu_english.txt"
sha256sum -c MANIFEST.sha256
```

## Result

- Source SHA-256 matched `1230b4f0e891c73a4761b2f7d952907555b6d93d7f4948ea268a89b414991cbc`.
- Verifier confirmed the full 80-key set and source ordering, exact `{}` placeholder sequence, and all numeric tokens.
- Generated game asset has UTF-16LE BOM, CRLF-only line endings, no final newline, and one Tab per record.
- `MANIFEST.sha256` covers the game asset, documents, TSV, and both tools. No MOD Organizer 2 deployment, GUI use, or game launch was performed.
