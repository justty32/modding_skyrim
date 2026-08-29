# Dialogue translation gaps: NFF, Glad You're Here, and USSEP

Date: 2026-08-16

## Finding

The English dialogue seen during the Dev runtime acceptance is not an IFD Lydia or RDO Final
translation failure. It comes from three independently incomplete translation surfaces:

1. `Nether's Follower Framework Traditional Chinese 2.8.6b` translates only
   `Interface/Translations/nwsFollowerFramework_english.txt`. NFF's unlocalized ESP still owns
   player-facing dialogue such as `DIAL 42488F:nwsFollowerFramework.esp`,
   `I'd like to see your additional follower inventory.`
2. `Glad You're Here Traditional Chinese 3.6.0.0` likewise translates only its MCM table. The
   current ESP contains the generic `I'm glad you're here.` topic plus many response, prompt,
   message, and letter strings.
3. Elrindir's `Why the name "Drunken Huntsman"?` (`0C2464:Skyrim.esm`) and
   `Who should I talk to for work?` (`0C368C:Skyrim.esm`) are won by
   `unofficial skyrim special edition patch.esp`. The installed USSEP translation layer covers
   perks only, so USSEP's inline English dialogue overrides the translated Skyrim core strings.

AgentBridge captured the Elrindir options directly from the running game. houseCARL's record
conflict tree independently confirmed USSEP as the winner for both topics and their INFO records.

## Available translation evidence

- Local NFF CHS `2.8.6b` has exactly the same 2,917-record identity/order and subrecord topology as
  the installed NFF ESP. It changes 475 zstring fields; the reported inventory topic is translated
  there. This is a strong seed, but its Simplified Chinese must be converted and reviewed before a
  Traditional Chinese text-only override is built. Its 19 changed PEX files remain a separate
  bytecode audit and must not be copied blindly.
- Local 2021 USSEP CHT contains valid Traditional Chinese for the two Elrindir topics and all six
  associated responses, but it is an old 51,147-record plugin versus current USSEP 4.3.8a's
  58,965 records. It is a translation seed only, never an install candidate.
- Current Nexus candidates are NFF Traditional Chinese `2.8.6b` (mod 67680), Glad You're Here CHS
  `3.2.3` (mod 82669), and USSEP CHS `4.3.6c` (mod 143324). The latter two trail the installed
  gameplay versions and therefore require FormID/field matching and a text-only semantic audit.

## Outcome

The three archives were used only as language seeds; none was installed directly. Version-locked
overrides were rebuilt from the exact active sources and deployed only to `Modpack-KR-Dev`:

- NFF: 2,917 records preserved, 467 ESP display strings translated, and 20 PEX files changed only
  in 297 existing string-table slots. Every declaration/property/bytecode tail is byte-identical.
  Two dialogue fields that displayed raw `$FF_*` keys despite the translation table now use their
  audited CHT table literals.
- Glad You're Here: 1,211 records preserved, 828 stable fields translated, and every nontext
  payload preserved. Three empty current-source fields and unmatched 3.6.0 additions were not
  guessed from the older seed.
- USSEP: 58,965 records preserved, 17,904 stable fields translated, and every nontext payload
  preserved. 562 unsafe cross-version candidates with changed tokens/newlines or empty current
  sources were rejected rather than copied.

Installed payloads match their `mod-library/l10n/mods/` artifacts byte-for-byte. Play-KR's modlist, plugins,
and load order hashes remain unchanged. The Dev profile install commit is `0863778`; the two-key
NFF runtime correction is `66e625e`. Static load
order and parse gates passed; houseCARL also re-reported source-plugin VMAD findings and one USSEP
dangling reference, but the canonical binary audits prove those nontext structures are identical
to the current official sources. Live Dev acceptance passed: Lydia's NFF/GYH options, Elrindir's
  USSEP topics and response subtitles all rendered in Traditional Chinese. Two raw NFF `$FF_*` menu
  keys and AI Overhaul's English NPC-name winner were corrected and passed a fresh-launch retest
  (`Elrindir → 厄倫德`). No new crash log was created.
