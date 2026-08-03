# Skill Maintenance Modes

Load this after selecting a `skill-maintenance` mode. Keep the default owner,
validation, audit, and review gates in `SKILL.md`.

## Hardening

```text
harden_skill(skill, lessons?, troubles?, progress?, usage?, cap?)
  -> eval_candidates + gotchas + guardrails + tickets + processed_state_delta?
```

Use fresh lessons, troubles, interval findings, proof failures, and repeated
planning misses. Dedupe them and add the smallest durable recurrence blocker.
Weekly Interval may call this as `skill_hardening`.

## Refinement

```text
refine_skill(skill, evals?, gotchas?, usage?)
  -> consolidated_evals + consolidated_gotchas + skill_delta + review_notes
```

Call `consolidate(target = edited_skill, structure = skill,
template = docs/skills/templates/SKILL_TEMPLATE.md,
constraints = {preserve_evidence: true, preserve_required_sections: true})`.
Apply only accepted owner-local edits. Split by branch or responsibility when
evidence shows mixed ownership or avoidable first-load cost.

## Source Upgrade

For `upgrade_skill_from_sources`, read
[source upgrade workflow](upgrade-skill-from-sources.md), the target package,
recent audits, book-to-skill extraction when applicable, and `best-of-worlds`.
Adopt or adapt only behavior that improves workflows, gates, examples, evals,
or QA without copying source prose.

## Other Modes

- `structure_update`: apply structure QA and first-load sufficiency.
- `metadata_update`: preserve source ownership, regenerate registries, and
  prove template claims.
- `qa_checklist_design`: compare target QA, eval assertions, gotchas, and
  recent audits; keep preflight and final-review prevention value.
- `eval_to_qa_sync`: promote only reusable runtime guardrails.
- `low_value_prose_scan`: classify candidates `keep | rewrite | move | delete`.
- `audit`: use binary evidence and name missing proof.
- `bulk_rollout`: prove one representative sample before scaling.
- `registry_validation`: regenerate generated rows and report ambiguous gaps.
- `installed_copy_import`: dry-run before overwrite; repo source remains owner.

## Automation Presets

```text
skill-maintenance.harden_skill @7d -> reports.skill_hardening
skill-maintenance.refine_skill @7d -> reports.skill_refinement
skill-maintenance.registry_drift @7d -> reports.registry_drift
```

The caller supplies cadence or review-window refs. Hardening owns dedupe,
immediate blockers, processed state, proof, and registry sync. Refinement owns
behavior-preserving consolidation. Registry drift owns generated sync and
follow-up gap reporting.

## Handoff Shapes

```text
edited_skill:
expected_behavior:
current_behavior:
mode:
behavior_delta:
owner_surface:
proof_required:
```

For hardening, add `source_rows`, `immediate_blockers`, and `processed_state`.
For refinement, add `inputs`, `consolidate_call`, and unit decisions for keep,
merge, move, and delete. For source upgrades, add source budget, source packet,
`best_of_worlds_decisions`, and the accepted skill delta.

Audit skip:

```text
audit_skipped:
  reason: tiny mechanical edit | no behavior delta | validation-only
  evidence:
  remaining_risk:
```

Review handoff:

```text
Review changed skill files for contract and integration readiness. Check source
ownership, first-load sufficiency, structure coherence, registry sync,
template truth, eval-to-QA sync, audit evidence, and reviewer routing. Return
TAS verdicts, blockers, and the smallest required fixes.
```
