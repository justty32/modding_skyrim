# trade-and-barter — economy-mechanism

← [調查入口](../trade-and-barter.md)

## 1. What it does

Trade & Barter is a lightweight, fully-MCM-configurable **economy/merchant overhaul**. It
adds many optional factors that shift buy/sell prices and merchant behaviour, each toggleable
or settable to zero. Headline knobs (corroborated across sources):

<!-- wf-nav -->
- **Overall barter rate** + **how much Speech skill affects prices** (adjustable).
- **Merchant gold** scaled by settlement size (big-city merchants richer than small towns);
  separate **Fence gold** option.
- **Location pricing** — goods cheaper in small towns, pricier in large cities; named
  location variables incl. Raven Rock / Solstheim (Dragonborn DLC).
- **Status / faction pricing** — Thane, Guild Member, Guild Leader get % discounts in the
  relevant city/guild; price varies by **faction rank, relationship, and race**.
- **Knowledge-based pricing** — better prices when you're skilled in the goods' domain:
  **Smithing** at blacksmiths, **Alchemy** at apothecaries (a "you-know-its-worth" system).
- **Race/kin pricing** — incl. a non-Orc **Blood-Kin of the Orcs** bonus at Orc strongholds;
  Dawnguard/Volkihar faction members get vendor discounts from their side's merchants.
- **Inventory respawn rate** (how fast merchant stock refreshes) adjustable.
- **Vanilla Speech-perk interaction** — works with the **Investor** and **Haggling** perks
  (it fixes `DLC2DremoraPrices` so the Dremora merchant obeys Haggling, and extends the
  Investor effect to USSEP-added investment merchants: Falion, Filnjar, Lod, Madena, Moth
  gro-Bagol, Zaria, Glover Mallory).

UNVERIFIED: any literal "blood price" or "pay-to-invest-in-shop" mechanic beyond the vanilla
Investor perk — I found no evidence T&B adds a shop-investment *system* of its own; it
extends the *vanilla* Investor perk's reach. Treat "invest in shops" as **vanilla Investor
perk, not a T&B addition** unless verified against the esp.

## 2. Mechanism / how it's implemented

This is the load-bearing finding and it's **well corroborated**:

> "uses a series of carefully conditioned perks to accomplish nearly all of its changes, with
> the only script included being the MCM script that controls the menu options."

<!-- wf-nav -->
- **Perks (the engine).** Nearly everything is **conditioned EntryPoint perks** — i.e.
  `Mod Buy Prices` / `Mod Sell Prices` perk entry-point effects gated by CTDA conditions
  (faction rank, location, race/keyword, skill value, relationship). The MCM toggles drive
  GLOB/condition values that enable/disable each perk path. This is a near-pure record
  overhaul, **not** a Papyrus-driven price engine.
- **Scripts.** Exactly **one** Papyrus script: the **MCM menu script**. No per-frame /
  OnSell scripting. So it is *script-light by design* (the script only writes config).
- **MCM.** Ships a **SkyUI MCM** (its own script, classic SkyUI `SKI_ConfigBase`-style — this
  predates and is independent of MCM-Helper). **Requires SKSE + SkyUI.** Without SkyUI the
  mod still loads but all options stay at default values. There's a separate companion mod,
  **"Trade and Barter - Settings Loader" (Nexus 57926)**, that auto-saves/loads MCM settings
  per new game — i.e. base T&B does **not** persist settings without it.
- **GMST / game settings.** Sources reference vanilla barter GMSTs `fBarterMin` / `fBarterMax`
  (and the Speech-affects-price relationship) as the *concept space*. UNVERIFIED whether T&B
  edits those GMSTs as static records vs. driving everything through perk entry points + GLOBs.
  Given the "conditioned perks do nearly everything" design, the likely answer is **mostly
  perks/GLOBs, minimal-to-no static GMST edits**, but I could not byte-confirm the esp. Do
  **not** assert specific GMST edits without checking the plugin.
- **Factions / VendorValues.** It reads/uses vanilla merchant **job factions** and added
  "merchant job faction" price options; UNVERIFIED whether it rewrites Faction VendorValues
  (gold/radius/hours) records or layers gold via perks/GLOBs. Merchant-gold scaling is
  presented as an MCM option, suggesting GLOB-driven rather than hard VendorValues edits, but
  unconfirmed.
- **No SKSE-plugin (DLL) dependency** beyond SKSE-the-loader (needed for SkyUI/MCM). No KID /
  SPID. UNVERIFIED but consistent with all sources describing it as records + one MCM script.
- **ESL?** UNVERIFIED — do not claim a flag/version. Modern SE builds *may* be ESL-flagged;
  check the actual file.

**No specific FormIDs, GMST values, perk EDIDs, or version numbers are asserted here** — none
were verifiable from secondary sources. The only named vanilla identifiers I'm confident in
are the perk-entry-point *types* `Mod Buy Prices` / `Mod Sell Prices`, the vanilla **Investor**
/ **Haggling** Speech perks, and the `DLC2DremoraPrices` perk T&B patches.

