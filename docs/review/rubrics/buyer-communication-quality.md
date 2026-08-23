# Buyer Communication Quality

Use for dossiers, landing pages, proposals, and any UI whose reader must make a
business decision. It judges the page's argument; `unslop` only removes generic
phrasing after this family passes.

Required TAS: `TAS-A`

## Required checks

1. One named reader and decision are explicit.
2. Outcome appears before mechanics; headings alone tell a coherent story.
3. Every material claim has adjacent proof or is clearly labelled hypothesis.
4. Evidence states what it means for the buyer, not only how it was produced.
5. The page answers the strongest relevant objection and gives one clear action.
6. A reader can scan the 10-second, 60-second, and 5-minute paths without
   developer jargon or architecture becoming the main narrative.

## Evidence and verdict

- Use the copy-complete `design.md`, current capture, and claim sources.
- `TAS-A`: every required check is evidenced and the argument is buyer-readable.
- `TAS-B`: useful but a reader, proof, objection, or action is repairably weak.
- `TAS-C`: absent reader/decision, incoherent story, unsupported claim, or no
  actionable next step.

## Calibration

**TAS-A / pass:** “Cut weekly account research from 6 hours to 45 minutes,”
followed by the operated comparison, interpretation, limitation, and review
CTA.

**TAS-B / revise:** “Cut weekly account research from 6 hours to 45 minutes,”
with a named operations lead and CTA, but only an unlabelled internal estimate
instead of inspectable proof. Repair the proof and interpretation; do not let
prose cleanup pass it.

**TAS-C / fail:** “RAG-powered multi-agent enrichment pipeline,” followed by
component details and no buyer outcome, proof interpretation, or next decision.
