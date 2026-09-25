# trade-and-barter — modforge-roadmap

← [調查入口](../trade-and-barter.md)

## 3. Relevance to ModForge

**Yes — ModForge could already generate most of a T&B-style tweak mod**, because T&B's core
mechanism is precisely what ModForge's perk pipeline does. Verified against the code:

<!-- wf-nav -->
- ✅ **`ModBuyPrices` / `ModSellPrices` EntryPoint perks are already supported.** Both are in
  ModForge's entry-type tab-count map (`src/ModForge.Core/Generator.Build.Perks.EntryPoints.cs`
  lines 31 & 55) — the two price entry points T&B is built on.
- ✅ **Conditioned perks.** ModForge perks support both **perk-level and effect-level CTDA
  conditions** via the shared `ConditionSpec` (`src/ModForge.Core/Spec.Perks.cs`, `Conditions`
  on both perk and effect; `Generator.Build.Conditions.cs`). That's exactly T&B's "carefully
  conditioned perks" model — faction-rank / location / race-keyword / skill-value gates map to
  ModForge condition functions.
- ✅ **MCM generation.** ModForge already emits MCM config (`Spec.Mcm.cs`, `McmGen.cs`,
  `Generator.Build.Mcm.cs`) — per the MEMORY recipe it's the MCM-Helper path (config.json +
  generated QUST/alias), which is a *different* MCM tech than T&B's hand-scripted SkyUI menu,
  but functionally covers "ship a config menu."
- ✅ **Vendor factions** (Vendor flag + VendorValues + sellBuyList + merchant container) and
  the new **`settlements:` population macro** exist (`Generator.Build.Vendor.cs`,
  `Spec.Settlement.cs`) — so the merchant-side scaffolding a price mod attaches to is present.
- ✅ **SPID/KID distribution** exists if one wanted to distribute the price perks onto the
  player or merchants instead of hand-placing them.

So the pitch **"could ModForge generate a merchant-economy tweak mod like this?"** → **largely
yes**: a spec of conditioned `ModBuyPrices`/`ModSellPrices` perks (Thane discount, skill-based
pricing, race/kin bonus) + an MCM to toggle them is expressible **today**.

**Gaps for a faithful reproduction:**

- ❌ **No GMST / game-setting editing in ModForge.** Confirmed: `grep -ri gmst/gamesetting`
  over `src/` returns **nothing** (only survey docs mention it). If a faithful T&B port needs
  to touch `fBarterMin`/`fBarterMax` or other GMSTs, ModForge **cannot express that today**.
  (May or may not be needed — see §2 uncertainty — but the capability is absent regardless.)
- ⚠️ **MCM-driven runtime values.** T&B's MCM writes GLOBs that its perk conditions read so
  options are live-toggleable. UNVERIFIED whether ModForge's MCM generator can wire an MCM
  slider/toggle → GLOBAL → perk-condition value end-to-end. Needs a code pass on
  `Generator.Build.Mcm.cs` ↔ globals before claiming parity.
- ⚠️ **Merchant-gold / inventory-respawn knobs.** If T&B does these via Faction VendorValues
  edits or LVLI respawn flags, confirm ModForge can *edit* those on vanilla records (override),
  not just create new merchant factions. UNVERIFIED.

**Out of scope / not worth replicating:** the USSEP-merchant compat fixes and the
`DLC2DremoraPrices` patch are vanilla-bug-fix glue, not a generatable feature pattern.

## 4. Roadmap implications (actionable)

<!-- wf-nav -->
1. **GMST / game-setting editing is the one hard gap.** ModForge has *no* GMST story
   (verified absent in `src/`). Add a `gameSettings:` (or `gmst:`) spec block that emits GMST
   override records (float/int/string). Even if T&B itself leans on perks, GMST editing is a
   broad economy/balance primitive (`fBarterMin`, `fXPPerSkillRank`, etc.) many tweak mods need.
2. **Confirm MCM-toggle → GLOBAL → perk-condition wiring.** This is the difference between
   "ModForge can ship an MCM" and "ModForge can ship a *configurable* mechanics mod like T&B."
   Verify/close on `Generator.Build.Mcm.cs` + globals; if missing, it's a concrete feature:
   bind an MCM option to a generated GLOB that a perk's CTDA reads.
3. **Verify override-editing of vanilla Faction VendorValues / LVLI respawn** (merchant gold,
   stock refresh). If ModForge can only create new vendor factions, add override support.
4. **No new perk-type work needed** — `ModBuyPrices`/`ModSellPrices` already land. Good signal
   that the EntryPoint perk surface is broad enough for economy mods.
5. **(Validation TODO, not a gap)** To remove the §2 UNVERIFIED flags, open the actual T&B esp
   in Mutagen and confirm: does it edit GMSTs? does it edit VendorValues? is it ESL? This
   survey is secondary-source only because Nexus/Step/Fandom 403'd the fetch.

## Sources (actually fetched/searched)

- Nexus SE 23081 (description not fetchable — 403): https://www.nexusmods.com/skyrimspecialedition/mods/23081
- Nexus LE 34612: https://www.nexusmods.com/skyrim/mods/34612
- Settings Loader companion (Nexus 57926): https://www.nexusmods.com/skyrimspecialedition/mods/57926
- Nolvus economy guide (fetched): https://www.nolvus.net/guide/ultra/gameplay/economy
- StepModifications T&B topics (403, search-summarized): https://stepmodifications.org/forum/topic/1996-trade-and-barter-by-kryptopyr/
- TES Mods Fandom wiki (403, search-summarized): https://tes-mods.fandom.com/wiki/Trade_and_Barter
- Patreon T&B SE post (search-summarized): https://www.patreon.com/posts/trade-barter-se-24395210

ModForge code checked: `src/ModForge.Core/Generator.Build.Perks.EntryPoints.cs` (ModBuyPrices
L31 / ModSellPrices L55), `src/ModForge.Core/Spec.Perks.cs` (perk + effect Conditions),
`Spec.Mcm.cs` / `McmGen.cs` / `Generator.Build.Mcm.cs`, `Generator.Build.Vendor.cs`,
`Spec.Settlement.cs`; GMST absent from `src/` (grep).
