# Verification

Done when:

- normalized upstream and patched INI differ at exactly one logical line;
- the changed line is only `MAG_BastionNPC` → `MAG_BastionControllerPerkNPC`;
- `Adamant_DISTR.ini` resolves to this Dev-only mod in the MO2 VFS;
- a fresh runtime SPID lookup has no missing-EditorID failure for Adamant, resolves all 13
  Adamant perk rules, and raises the full profile lookup from `15/15` to `16/16` registered perks;
- no new crash log is created, and the Play profile hashes remain unchanged.

Runtime evidence and exact deployment state belong in
`~/notes/projects/modding/skyrim/logs/simonrim-batch4-4mp-2026-08-16/`.

2026-08-16 runtime result: PASS. SPID 7.3.0.16 registered `16/16 Perks` with no
`MAG_BastionNPC` failure, then distributed `MAG_BastionControllerPerkNPC "堡壘"`
(`PERK:2923284B`) to every observed actor. No new crash log was created.
