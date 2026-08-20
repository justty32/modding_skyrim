# Source

- Upstream: [Adamant - A Perk Overhaul](https://www.nexusmods.com/skyrimspecialedition/mods/30191)
- Upstream MAIN version: `6.0.4`, uploaded 2026-08-19
- Upstream archive SHA-256: `d68f257da48d4e36a6616ed555962d8bc0237c3705cf9507b89804f7833641b7`
- Upstream `Adamant_DISTR.ini` SHA-256: `03f2e3951ade9d25c11d0c65e456f7672a7159d608d6c7cab8d7c8dcd3d92074`
- Built: 2026-08-20

Evidence:

- SPID 7.3.0.16 runtime log: `[Adamant_DISTR.ini] (MAG_BastionNPC) FAIL - editorID doesn't exist`.
- Official `Adamant.esp` 6.0.4 contains `MAG_BastionControllerPerkNPC` and does not contain
  `MAG_BastionNPC`.
- The official 6.0.4 `Adamant_DISTR.ini` is byte-identical to 6.0.2 (SHA-256 above), so the
  one-line correction remains required after the main-file upgrade.
- The corrected record appears at `23284B:Adamant.esp`; with runtime full-plugin index `0x29`,
  SPID reports it as `PERK:2923284B`.
