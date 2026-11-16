# Kurone Soul Tomb Picker Template

Done when: the single-file template and this note exist, the fixed data placeholder is preserved, all requested selection and JSON workflows are implemented, and the lead receives both absolute output paths. Implemented a Traditional Chinese offline picker using embedded CSS and native JavaScript, with female targets shown by default, all specified filters, grouped donor choices, body descriptions, all five live warning types, global duplicate summaries, reference tables, localStorage restore/save, confirmed clearing, JSON preview/download/copy, and partial-success JSON import. Counts come from the supplied arrays, not the sample metadata totals. Targets and exported picks retain the input target order. No external assets, requests, frameworks, game access, or mod changes are used. Only files under this workspace's out directory were written; this file also serves as the task notes and handoff because the brief prohibits writing elsewhere.

## Integration

Replace the sole `__PICK_DATA__` token with the complete JSON object. Keep the surrounding application/json script element intact. The template deliberately does not embed the sample data. Escape literal less-than characters in serialized data as `\u003c` before HTML injection so record text cannot terminate the data script element. Runtime DOM content uses textContent rather than HTML interpolation. With the placeholder unchanged, the page displays a data-loading explanation and disables the controls instead of throwing an uncaught parsing error.

## Export Fields

- `format`: fixed `kurone-soultomb-pick/1` format identifier.
- `generated_at`: UTC ISO 8601 time when the current JSON preview is regenerated on initialization or a selection change, import, or clear. Download and copy use exactly that preview snapshot.
- `data_extracted`: unchanged `meta.extracted` value from the injected data.
- `profile`: unchanged `meta.profile` value.
- `remove_donor`: always `false`; the original donor NPC is never removed.
- `picks`: only targets with a donor selected or a body other than `none`, ordered as in the main table, independent of filters.
- `picks[].target.formkey`, `edid`, `name`, `mod`, `sex`: the target's exact source values; no identifiers are synthesized.
- `picks[].donor`: `null` when no face is selected; otherwise an object containing the donor's unchanged `formkey`, `edid`, `name_zh`, `name_en`, `race`, and boolean `custom_race` fields.
- `picks[].parts`: `head` when a donor exists, otherwise `null`.
- `picks[].body`: always an object with `id` and `label` copied from the selected body; the no-change selection is the supplied `none` body with label meaning no change.
- `picks[].warnings`: the row's current warning strings without colors, including duplicate names when applicable. Warnings are recomputed from current data and selections, not trusted from imported JSON.

## Persistence And Import

The localStorage key is exactly `kurone-soultomb-pick/v1`. Its value is an object mapping each selected target ID to `{donor_id, body_id}`. Unselected targets are omitted; a body-only selection uses an empty donor ID. Invalid or missing saved IDs are reported and downgraded to no change where possible. Blocked storage does not prevent selection or export.

Import accepts the exported envelope and replaces the current selection set. Targets and donors match by trimmed, case-insensitive FormKey, with the original input values preserved in subsequent exports. Unknown target FormKeys are listed and skipped; unknown donor FormKeys are listed and that row keeps any valid body selection. Unknown body IDs become `none` with a message. Duplicate entries for the same target use the last entry. Profile differences and donor-removal flags produce messages; removal is never enabled. Invalid JSON or an invalid envelope leaves existing selections intact. The five warning rules use the complete selection set, even when targets are hidden by filters.

## Follow-up: Donor Sex Filter And Dynamic Counts

Added the unchecked toolbar control labeled 素材顯示全部性別. By default each target's donor dropdown includes only donors with the same sex as that target, plus its currently selected donor even if that donor has a different sex. Enabling the control lists all donor sexes for every target; disabling it rebuilds each dropdown without changing selection state, localStorage, export content, or warnings. The retained cross-sex donor remains within its normal optgroup, and the existing sex-mismatch warning still appears. This also applies to cross-sex selections restored from localStorage or imported JSON. Switching away from a retained cross-sex donor removes that former option while the control is unchecked. The toggle is a display control, not a persisted choice; it starts unchecked when the page is opened. The target sex filter still defaults to female.

All totals remain computed from the current data arrays, including target and donor totals, excluded totals, body totals, per-mod counts, visible rows, selected rows, duplicates, and warning messages. Neither the old nor the updated real-data target count is hardcoded as a row total. The template accepts the updated dataset without changing these calculations. Source review covers the new control, selection-preserving dropdown rebuild, import/restore path, and dynamic count expressions; runtime interaction remains for the lead to verify.

## Validation And Limitations

Performed a source review of data parsing, source-field mappings, selection events, warning calculation, global summaries, serialization, FormKey-based import, localStorage handling, clipboard fallback, and dynamic filtering. A text search found no external web addresses, external asset attributes, fetch calls, CSS imports, or external CSS resources. The exact data script line is present once. All generated reference text and identifiers come from the supplied schema.

No shell, Node runtime, or browser execution tool is available to this worker. JavaScript syntax checking, screenshot inspection, the complete real target dataset, duplicate-selection interaction, round-trip import, and actual clipboard/download/storage behavior have therefore NOT been executed or verified. These acceptance checks remain with the lead. File-origin localStorage and clipboard support vary by browser; both have visible failure messages, and copy attempts the required hidden-textarea execCommand fallback. Fonts are local-only fallbacks. The download filename uses local time; the export timestamp uses UTC. The summary warning count counts warning messages across rows, not unique warning categories.

## Handoff

Done: `out/page-template.html` and `out/NOTES.md` are written; fixed JSON envelope, exact placeholder, offline behavior, and requested controls are implemented. Not done: runtime acceptance tests, real-data injection, or deployment outside the workspace. Next step: the lead injects the real JSON with safe script escaping, runs the Node syntax check and Firefox acceptance tests, and checks duplicate warnings plus export/import round-tripping. Also verify same-sex donor defaults, all-sex toggling, preserved cross-sex selections and warnings (including imported/restored choices), and totals calculated from the updated dataset. No permission or product decision is requested.
