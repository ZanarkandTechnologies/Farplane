---
title: Agent Skills eval comparison decision matrix
created_at: 2026-06-30
target: Farplane skill system compared with Agent Skills eval and authoring practices
status: draft
scoring: 1-5 for value/evidence/transferability/cost/risk/synergy
---

# Decision Matrix: Farplane skill system compared with Agent Skills eval and authoring practices

| Feature | Scores | Decision | Reason | Implementation note |
| --- | --- | --- | --- | --- |
| With-skill versus baseline output evals | V5/E5/T4/C3/R4/S5 | adapt | Strong proof pattern, but Farplane should express it through `skills/eval` and ticket-scoped artifacts rather than importing the external workspace layout verbatim. | Add a baseline-comparison mode or guidance to `eval`/`skill-maintenance`; store evidence under skill or ticket artifacts. |
| Richer skill-local eval cases and assertions | V5/E5/T5/C3/R4/S5 | adopt | Farplane already has `eval_task.json`; the missing value is better assertion/evidence discipline and coverage quality. | Extend authoring guidance and runner schema only as much as needed for prompt, expected behavior, files, assertions, grading evidence. |
| Description trigger-rate evals | V5/E5/T4/C3/R3/S5 | adopt | This is the clearest gap: Farplane validates description length/shape but does not yet measure whether descriptions select the right skill. | Introduce `trigger_eval` rows or a mode in `eval` that runs labeled should/should-not trigger prompts and records rates. |
| Train/validation split for description optimization | V4/E5/T4/C4/R4/S4 | adapt | Useful for material description rewrites, but too heavy for every typo-sized edit. | Require for high-heat or ambiguous skill-routing changes; keep optional for tiny local edits. |
| Trace-based simplification | V5/E5/T5/C4/R5/S5 | adopt | Matches Farplane's hardcase/correction culture and improves both quality and context cost. | Add trace findings as accepted evidence for `skill-signals` maintenance burden and `skill-maintenance.refine_skill`. |
| Real-expertise source material | V4/E5/T5/C5/R5/S4 | adopt | Already aligned with Farplane tickets/docs/history/proof truth, worth making explicit in skill-maintenance scoring. | Prefer skill changes backed by task logs, tickets, reviews, specs, corrections, and git diffs over generic best-practice prose. |
| Context budget and progressive disclosure | V5/E5/T5/C5/R5/S5 | adopt | Farplane already has a stronger local version: first-load contract plus optional capped budget. | Keep current Farplane shape; use Agent Skills as validation, not a reason to loosen. |
| Imperative, user-intent descriptions | V4/E5/T4/C5/R4/S4 | adapt | Agent Skills optimizes for selection; Farplane optimizes for lean generated registry. The principle transfers, the 1024-char limit does not. | Update examples/guidance to prefer imperative user-intent wording inside the 220-char cap. |
| Live HTML optimization report | V3/E3/T3/C2/R3/S3 | defer | Useful eventually, but data contracts and runner behavior should come first. | Revisit after trigger/output eval artifacts are stable and repeated enough to need a viewer. |

Decision values: `adopt`, `adapt`, `reject`, `defer`.
