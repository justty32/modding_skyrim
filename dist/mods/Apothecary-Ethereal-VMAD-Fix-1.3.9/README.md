# Apothecary Ethereal VMAD Fix 1.3.9

Dev-only runtime correction for Apothecary 1.3.9. It overrides only
`MAG_AlchBecomeEthereal` and removes the unbound `magicImodBeginLoopEnd` attachment.
The two working upstream attachments, `magicImodScript` and
`magicSetActorAlphaScript`, remain byte-for-byte intact.

The patch is localized for the current Traditional Chinese lane, so winning the MGEF
record does not replace `虛體變換` or its description with English or mojibake.

Build and verify from the packaged, audited source patch:

```bash
python tools/build_translation.py --source tools/source-ApothecaryEtherealVMADFix-unlocalized.esp
python tools/verify_translation.py --source tools/source-ApothecaryEtherealVMADFix-unlocalized.esp
```

Load after `Apothecary.esp` and its Traditional Chinese layer. This artifact is scoped
to Apothecary 1.3.9 and should be re-audited before use with another version.
