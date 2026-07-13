---
title: Dogfood report prototype comparison
kind: prototype-comparison
status: complete
created_at: 2026-07-13T21:40:00+08:00
source_sha256: 5b1fa2ff3f2df3717d90d9a383daa414ccd2c593e9c8ff32d3999c974749c7f0
---

# Dogfood report prototype comparison

## Result

The prototype reduces the primary reading path from 1,990 to 549 words and
from 14 to 7 headings while retaining the source decision, material risks,
next action, and exact no-execution proof. That is a 72% word reduction and a
50% heading reduction. The source report remains unchanged; structured proof
moved to a linked JSON receipt rather than being deleted.

## Before and after

| Measure | Source | Prototype | Change |
| --- | ---: | ---: | ---: |
| Human-report words | 1,990 | 549 | -72% |
| Headings | 14 | 7 | -50% |
| Primary decision appears | Summary paragraph + bullets | Title + first section | earlier |
| Diagram | none | one situation map | added |
| Machine receipt | repeated as report prose | linked structured JSON | moved |
| Empty-state ledgers | three tables with `none` rows | one plain decision sentence | compressed |

Counts use `wc -w` and Markdown heading lines. The source SHA-256 is recorded in
frontmatter so later checks can prove it was not rewritten.

## Coverage map

| Source claim | Prototype destination |
| --- | --- |
| No active or pending experiment WIP; one immediate slot | Decision; material finding 1 |
| Completion-learning proof is strong but Dogfood consumption/dedupe is unproved | Situation map; material findings 2–3 |
| Select one Dogfood completion-learning fixture | Decision; next action |
| Create no duplicate ticket-identity recovery because `TASK-0338` owns it | Decision; material finding 4 |
| Future Reward rows are Pulse check-ins | Material finding 5 |
| Feature/system continue-adjust decisions | Material finding 6 |
| Human-feedback candidate rejected | Risks: missing export; no unsupported admission |
| Paperclip candidate deferred | Risks: defer until a bounded gap and proof route exist |
| Six declared source gaps | Four grouped risk bullets; none omitted |
| Candidate hypothesis, guard, proof, stop, and admission owner | Next action |
| Authority, zero writes, action/mutation state, capacity/order guards, exact stop receipt | `dogfood-receipt.json` |
| Exhaustive ticket/feature evidence and BAU examples | Linked unchanged source report |

## Content disposition

Kept in the human reading path:

- the portfolio decision and reason;
- only findings that alter admission, ownership, or behavior;
- gaps that constrain confidence or candidate choice;
- one owner, action, proof route, and stop condition.

Moved to supporting evidence:

- authority, mutation counts, eight ordering/capacity guards, and the exact
  no-execution string;
- exhaustive ticket-by-ticket proof, raw capacity arithmetic, and source
  observations.

Removed as duplicate or instructional prose:

- allowed-state definitions and candidate authoring requirements;
- empty experiment, active-portfolio, and due-check-in table rows;
- repeated explanations of WIP policy, delayed caps, and report-only behavior;
- second statements of facts already present in the decision or receipt.

Nothing removed above is unique decision evidence. The unchanged source report
remains available for audit and is the canonical record.

## Prototype boundary

This comparison proves readability for one representative report. It does not
prove generality across all 37 report-family skills and does not change
`skills/dogfood-review/`, its live template, report generation, or downstream
state.
