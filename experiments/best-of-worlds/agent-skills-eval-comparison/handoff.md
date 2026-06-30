---
title: Agent Skills eval comparison handoff
created_at: 2026-06-30
target: Farplane skill system compared with Agent Skills eval and authoring practices
status: draft
recommended_owner: skills/eval plus skill-maintenance
---

# Handoff: Farplane skill system compared with Agent Skills eval and authoring practices

## Recommendation

Adapt Agent Skills' measurable loops into Farplane rather than copying its skill system. Farplane already has the stronger local harness shape: first-load contracts, tiered todo-linking, artifact-first proof, QA checklists, generated registry, skill signals, and opt-in surface budgets. The external system's strongest missing pieces are measurement loops:

1. output evals that compare `with_skill` against `without_skill` or a previous version;
2. trigger evals that measure whether descriptions select the right skill;
3. train/validation and fresh-query discipline for material description optimization;
4. trace-based simplification tied to maintenance decisions.

Best next implementation shape:

```text
skill_value_eval(skill, cases, baseline?)
  -> output_delta + trigger_rates + cost_delta + trace_findings + review_receipt
```

Do this as a small Farplane feature/ticket owned by `skills/eval` and `skill-maintenance`, with docs updates in `docs/skills/best-practices.md` and `docs/skills/system.md`. Keep live UI/reporting deferred until the data contract is used a few times.

## Adopt

- Skill-local assertions with concrete grading evidence.
- Trigger eval cases with `should_trigger` labels and near-miss negatives.
- Trace-based simplification as a first-class skill-maintenance evidence source.
- Real-expertise source priority: tickets, corrections, specs, reviews, history, and failure cases beat generic skill prose.
- Progressive disclosure and context discipline, treated as validation of Farplane's current direction.

## Adapt

- With/without-skill eval workspaces: keep the baseline comparison, but store outputs in Farplane skill or ticket artifact paths.
- Train/validation split: require for material/high-heat description changes, optional for tiny edits.
- Description style: borrow imperative/user-intent wording while preserving Farplane's 220-character generated-registry cap.
- Cost accounting: capture tokens/time when available, but do not block low-cost local evals when telemetry is missing.

## Reject

- Replacing Farplane's skill contract with Agent Skills' looser structure.
- Raising Farplane descriptions to the external 1024-character limit.
- Treating eval pass rate as a replacement for QA/review/TAS gates.
- Auto-mutating skills from eval results without a reviewed skill-maintenance pass.

## Defer

- Live HTML optimization report.
- Global mandatory eval coverage for all 99 skills.
- Standalone skill-quality scalar or scoreboard UI.
- Automatic fresh-query generation until trigger eval schema and runner behavior are stable.

## Next Skill

- Use `impl-plan` if turning this into a ticket.
- Use `skill-maintenance` for the first concrete rollout across one or two high-heat skills.
- Use `review` before promoting the decisions into canonical docs or feature specs.
