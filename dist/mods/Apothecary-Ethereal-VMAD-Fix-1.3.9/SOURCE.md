# Source and diagnosis

- Upstream: [Apothecary - An Alchemy Overhaul](https://www.nexusmods.com/skyrimspecialedition/mods/52130)
- Target version: 1.3.9, Nexus file id 447818.
- Target record: `0F3879:Apothecary.esp` (`MAG_AlchBecomeEthereal`).

houseCARL's script-property validator found `IntroFX`, `LoopFX`, and `OutroFX` unbound
on `magicImodBeginLoopEnd`. Consuming `MAG_BecomeEthereal01` in a fresh runtime produced
seven matching `Cannot call ... on a None object` Papyrus errors across effect start and
finish.

The same record already carries the complete `magicImodScript` and
`magicSetActorAlphaScript` setup used by the USSEP winner of vanilla
`VoiceMakeEthereal` (`064D68:Skyrim.esm`). USSEP removes the obsolete unbound
`magicImodBeginLoopEnd` attachment from that vanilla record. This patch applies the same
minimal correction to Apothecary's new effect instead of inventing substitute values or
changing the working image-space and alpha behavior.

`tools/source-ApothecaryEtherealVMADFix-unlocalized.esp` was created as a new houseCARL
patch with one structural edit:

```text
Remove VirtualMachineAdapter.Scripts[0] from 0F3879:Apothecary.esp
```

Its inline FULL/DNAM were normalized to the exact English source text before the
deterministic localization pass. SHA-256:
`7577bee1d68629222c5ac9da760fd681a65f451c739d0ba1a7b6f5ba81e61850`.
