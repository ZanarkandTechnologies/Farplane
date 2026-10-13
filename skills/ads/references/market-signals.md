---
title: Ads Market Signals
owner: ads
status: active
kind: skill-reference
---

# Ads Market Signals

Load in N2 when the thesis needs a demand signal or angle families and the
operator has not supplied them. Both recipes are read-only data pulls, adapted
from published treg and Monid workflows. Quote the price first (treg
`catalog_get` or `monid inspect`), stay inside the operator's weekly spend
cap, and log the spend. The gateway per job is the winner recorded in the tool
loadout note in `~/.farplane/memory/`.

## 1. Keyword Demand To Ad Budget

Use when the offer's search demand or the budget split is unknown.

1. Expand the seed offer into about 100 related terms
   (`treg.google.keywords.ideas`).
2. Price the terms in one batch: volume, CPC, competition and 12 months of
   history (`google.keywords.volume`, up to 1,000 terms a call).
3. Read Google Trends for the top 5 terms.
4. Split the test budget by volume share; drop terms whose CPC breaks the
   offer's allowed cost per lead.

Out: term table, trend direction, budget split, the demand line for the
thesis. Published receipt: $0.11 for 50 keywords.

## 2. Competitor Ads As An Angle Pack

Use before writing angle families, and to re-check a live test monthly.

1. Count each competitor's active Meta ads first (`onlyTotal: true`), then
   pull them with a cap: format, CTA, opening line, start date.
2. Pull Google Ads Transparency creatives for each competitor's root domain.
3. Group the openings into angle families; an ad running 30+ days is a
   likely winner, a burst of new variants is a live test.
4. Hand the families to N2 as hypotheses, never as copy to reuse.

Cheapest Meta Ad Library listings seen 2026-10-12: about $0.0017-0.005 an ad;
Google Ads Transparency about $0.011-0.015 a hit.

Never copy a competitor's wording, imagery or brand; record the mechanism.
Source workflows: treg `/workflows/keyword-demand-to-ad-budget` and
`/workflows/mine-competitor-meta-ads-as-creative-pack`; mapped in
`~/.farplane/memory/projects/farplane/2026-10-12-treg-workflows.md`.
