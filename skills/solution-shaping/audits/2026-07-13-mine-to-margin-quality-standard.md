---
skill: solution-shaping
date: 2026-07-13
change_type: behavior
status: pass
---

# Mine-To-Margin Quality Standard

## Behavior Delta

- Before: the skill already recognized mine-to-margin as an allocation loop and
  required realistic scenarios, but its quality criteria were distributed
  across the main workflow and mining example.
- After: a reusable five-question reference standard and five-gate QA contract
  make mechanism credibility, responsive proof, buyer inspectability, and the
  production boundary explicit for any operational decision system.
- Mining-specific workflow and proof detail moved out of first load into the
  Mine-To-Margin reference; the normal path now states the domain-neutral rule.

## QA Ownership

One QA owner applies the complete checklist and returns one verdict. The five
gates are evidence categories, not five separately spawned tasks.

## Proof

- First-load behavior contains the checklist load condition.
- The detailed rubric and QA procedure live in owner-local files.
- Existing mining eval coverage remains applicable, so no new near-duplicate
  eval case was added.
- Independent review initially requested domain-neutral first-load wording and
  complete QA receipt fields; both were repaired. Re-review: `TAS-A`, pass,
  with no remaining findings.
- Canonical-source review also verified the generated registry row and installed
  `~/.codex` copy match this Farplane package: `TAS-A`, pass, no findings.
- Cross-skill review caught stale generated graph documentation; regeneration
  produced 119 skill docs and 835 edges. Re-review: `TAS-A`, pass.
