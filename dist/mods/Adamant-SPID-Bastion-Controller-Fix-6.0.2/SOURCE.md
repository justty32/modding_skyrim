# Source

- Upstream: [Adamant - A Perk Overhaul](https://www.nexusmods.com/skyrimspecialedition/mods/30191)
- Upstream MAIN version: `6.0.2`, uploaded 2026-08-15
- Upstream archive SHA-256: `116f715a9608a4f0b8b07fe017bc05c8f6ff0926bbdffb51dfdbf0233dc95afc`
- Upstream `Adamant_DISTR.ini` SHA-256: `03f2e3951ade9d25c11d0c65e456f7672a7159d608d6c7cab8d7c8dcd3d92074`
- Built: 2026-08-16

Evidence:

- SPID 7.3.0.16 runtime log: `[Adamant_DISTR.ini] (MAG_BastionNPC) FAIL - editorID doesn't exist`.
- Official `Adamant.esp` 6.0.2 contains `MAG_BastionControllerPerkNPC` and does not contain
  `MAG_BastionNPC`.
- The corrected record appears at `23284B:Adamant.esp`; with runtime full-plugin index `0x29`,
  SPID reports it as `PERK:2923284B`.

