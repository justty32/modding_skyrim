# Verification contract

The verifier requires all of the following:

- exact source SHA-256 and master list (`Skyrim.esm`, `Update.esm`, `Apothecary.esp`);
- exactly two records (TES4 plus the single MGEF override);
- identical record/subrecord topology and identical non-text payloads between the audited
  source patch and the packaged localized patch;
- exactly two localized fields, with UTF-8 STRINGS/DLSTRINGS and preserved `<dur>` token;
- byte-identical `_English` and `_Chinese` tables for the profile's current language lane;
- a byte-identical rebuild and complete manifest coverage.

Runtime acceptance additionally requires a fresh baseline load, successful potion use and
expiry, no `magicimodbeginloopend` entry in the new Papyrus delta, and no new crash log.
