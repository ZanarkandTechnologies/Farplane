---
name: optimize-harness
description: "Turn observed Farplane behavior gaps into placement decisions, proof or eval, accepted changes, and review."
tier: 3
group: operations
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# Optimize Harness

## Context

Use this when Farplane should behave differently, not merely be explained. It
owns the end-to-end behavior-gap loop: diagnose, place, prove, change or
experiment, then accept, hold, or roll back. Lower-level skills retain their
own artifacts: `gap-analysis`, `harness-advisor`, `metric-advisor`,
`proof-advisor`, `eval`, and implementation owners.

## Skill Signature

```text
optimize_harness(observed_behavior, expected_behavior?, metric?, evidence?)
  -> accepted_change | experiment_plan | blocked_report
reads: gap evidence, owner surfaces, metrics, registries, evals, tickets
writes: placement/proof decision and changed owner artifact when accepted
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind the loss-bearing behavior gap.**
  `observed + expected? + evidence -> bounded gap + loss term | clarification`

  Rule: Do not mutate on vague quality or ROI language; derive or request an
  observable expected behavior, evidence need, and loss term first.

  Assert: Current and expected behavior are separately stated, or the result is
  explicitly blocked for clarification.

- [ ] **N2 — Diagnose the gap.**
  `bounded gap + evidence -> gap report | known direct cause`

  Rule: Use [gap-analysis](../gap-analysis/SKILL.md) unless evidence already
  identifies the wrong or missing owner; never invent the target behavior.

  Assert: The report names the observed failure, expected result, and one
  evidence-backed cause or uncertainty.

- [ ] **N3 — Place one owner and its success signal.**
  `gap report + loss term -> primary owner + rejected surfaces + reward | metric branch`

  Rule: Use `metric-advisor` when the reward signal
  is missing, then [harness-advisor](../harness-advisor/SKILL.md) to select the
  primary owner. Return a smaller metric or leverage route when no full loop is
  needed.

  Assert: A generic agent's “edit the prompt” instinct is rejected when the
  loss and evidence place the guard in a ticket, skill, validator, or QA owner.

- [ ] **N4 — Choose proof before the change.**
  `owner + expected behavior -> proof route + runnable case | no durable proof`

  Rule: Use [proof-advisor](../proof-advisor/SKILL.md); use an eval only for a
  durable, testable behavior. Keep difficult reusable cases in the normal eval
  suite, with scenario in the fixture and expected behavior in assertions.

  Assert: Browser/UI proof stays with QA: qa-tester operates the Codex in-app
  Browser; Playwright is for requested regression coverage or settled scripts.

- [ ] **N5 — Select the smallest execution route.**
  `owner + proof route -> direct change | experiment | named handoff`

  Rule: Change directly only when owner and proof are clear. Use
  [self-improve](../self-improve/SKILL.md) only with metric, baseline, search
  space, and candidate comparison; route existing skills to
  [skill-maintenance](../skill-maintenance/SKILL.md), missing reusable owners to
  [skill-creator](../skill-creator/SKILL.md), code to
  [impl-plan](../impl-plan/SKILL.md), and a ready frontier to
  [goal-advisor](../goal-advisor/SKILL.md).

  Assert: The selected route preserves the proof owner and does not create a
  duplicate skill or hidden autonomous loop.

- [ ] **N6 — Decide from evidence and return the receipt.**
  `changed owner artifact + proof -> accept | hold | rollback + review route`

  Rule: Accept only when the named loss falls, proof supports the claim, and
  guards hold; hold when composition proof is missing; roll back on regression
  or incorrect placement.

  Assert: Material claims name the review/validation evidence; prose alone
  never proves behavior changed.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Do not optimize vague taste, raw agent hours, or an invented numeric score.
- Do not create a skill before checking the generated registry for an owner.
- Do not keep difficult regressions in a separate raw-transcript backlog.
- Do not bypass QA for operated browser evidence or treat a first viewport as
  full-page proof.
- Do not claim a harness improvement without the selected proof and review.

## Reference Map

- [harness doctrine](../../docs/fundamentals/harness-engineering-doctrine.md)
  for placement policy.
- [harness algebra](../../docs/fundamentals/harness-algebra.md) for loss and
  reward concepts.
- [eval feature contract](../../docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md)
  for runnable regression cases.
- [skill maintenance](../skill-maintenance/SKILL.md) for existing-skill repair
  and registry validation.

## Output

Return `Observed`, `Expected`, `Loss term`, `Gap report`, `Primary owner`,
`Proof`, `Execution route`, `Accept | hold | rollback`, `Evidence`, and `Next
concrete action`.
