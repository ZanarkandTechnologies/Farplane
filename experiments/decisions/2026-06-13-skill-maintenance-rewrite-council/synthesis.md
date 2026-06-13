---
title: "Skill Maintenance Rewrite Council Synthesis"
status: active
owner: deliberative-advice
created_at: 2026-06-13
updated_at: 2026-06-13
tags:
  - deliberative-advice
  - skill-maintenance
  - council
refs:
  - experiments/decisions/2026-06-13-skill-maintenance-rewrite-council/context.md
  - skills/skill-maintenance/SKILL.md
  - skills/skill-maintenance/eval_task.json
---

# Skill Maintenance Rewrite Council Synthesis

## Decision

Whether to rewrite `skills/skill-maintenance/SKILL.md` from the current verbose
two-signature checklist into a behavior-delta entrypoint with variables and
pseudocode branch routing.

## Council Method

All lanes received the same context packet:

```text
experiments/decisions/2026-06-13-skill-maintenance-rewrite-council/context.md
```

The packet included prior discussion summary, current and expected behavior,
three options, evidence refs, constraints, lane briefs, and proof expectations.
Each lane received only the packet path plus its perspective-specific brief.

## Perspective Results

| Lane | Recommendation | Confidence | Key Caveat |
| --- | --- | --- | --- |
| Operator value | Option B: conservative behavior-delta compression | High | Compress shape, not gates. |
| Engineering risk | Option B, with explicit hard gates and validator-compatible headings | High | Validators check shape, not semantic safety. |
| Evidence skeptic | Option B only as prototype-first path | Medium-high | Direct live replacement lacks evidence-quality and integration-readiness proof. |
| Systems fit | Option B, preserve owner boundaries | High | `skill-maintenance` must not absorb `optimize-harness` behavior-gap routing. |

## Option Ranking

1. **Option B: Conservative Behavior-Delta Compression**
   - Strongest fit. It improves entrypoint clarity while preserving safety.
2. **Option A: Keep Current Structure With Minor Wording**
   - Safest short term, but leaves the operator-value and scan-cost problem
     unsolved.
3. **Option C: Full Rewrite Plus Script-Assisted Detection**
   - Potentially useful later, but premature before the human-readable contract
     proves stable.

## Recommendation

Proceed with **Option B**, but treat the first implementation as a constrained
prototype that must pass eval, structure, validator, and reviewer proof before
live replacement is considered complete.

Target signature:

```text
skill_maintenance(expected_behavior, current_behavior, edited_skill, mode?, evidence?)
  -> updated_skill | audit_record | blocked_report
state: reads(edited_skill.SKILL.md, edited_skill.references?, edited_skill.eval_task?,
             edited_skill.qa_checklist?, registry, prior_audits?, run_artifacts?)
       writes(edited_skill.SKILL.md?, edited_skill.references?, edited_skill.eval_task?,
              edited_skill.qa_checklist?, audit?, registry)
modes: structure_update | metadata_update | eval_to_qa_sync | audit | bulk_rollout | registry_validation
gates: behavior_delta_named; owner_surface_clear; first_load_executable;
       source_owner_preserved; registry_synced; eval_guardrails_synced_or_skipped;
       audit_or_skip_recorded; reviewer_routed_when_material
fails: vague update; hidden installed-copy edit; eval changed without QA-sync check;
       bloated first-load contract; audit skipped for material change
```

## Required Implementation Constraints

- Use one primary behavior-delta signature; do not keep two equal top-level
  signatures.
- Preserve audit as a mode/output path, not as lost secondary behavior.
- Bind variables up front:
  `edited_skill`, `expected_behavior`, `current_behavior`, `mode`, `evidence`.
- Keep every-invocation hard gates inline:
  source ownership, sandbox/prototype-before-bulk, registry sync,
  template-version truth, validator command, audit-or-skip reason, reinstall
  when live behavior matters, and reviewer routing for material changes.
- Keep validator-compatible shape:
  `## Context`, `## Skill Signature`, marker-delimited `## Todo List`,
  `## Templates`, `## Gotchas`, `## Reference Map`, and `## Output`.
- Use pseudocode only for branch routing, not vague judgment prose.
- Add explicit branches for:
  `edited_skill.eval_task changed`, `installed copy differs`, `bulk rollout`,
  `template version changed`, and `registry/frontmatter changed`.
- Move long rationale, examples, rare recipes, and detailed structure rubric
  into references with precise load conditions.
- Do not introduce script-assisted detection until the rewritten human-readable
  contract proves stable.
- Do not let `skill-maintenance` duplicate `optimize-harness`; it maintains
  skill-system surfaces after the owner surface is known.

## Dissent

The evidence skeptic does not approve a direct live replacement yet. The
current skill is verbose because it carries real safety behavior, and a shorter
version could pass validators while silently weakening source ownership,
registry sync, audit records, broad-rollout prototyping, or eval-to-QA sync.

This dissent changes the rollout gate: implement as a constrained prototype and
prove no regression before considering the rewrite complete.

## Proof Required Before Completion

```text
python3 skills/skill-maintenance/scripts/check_skills.py --write
python3 skills/skill-maintenance/scripts/check_skills.py --template-version 0.2.0
python3 -m json.tool skills/skill-maintenance/eval_task.json
```

Additional proof:

- run or review all existing `skills/skill-maintenance/eval_task.json` cases
- perform a sandbox fixture repair against
  `skills/skill-maintenance/tests/fixtures/bad-skill-repo`
- run `skills/skill-maintenance/qa_checklist.md`
  against the draft
- obtain reviewer pass for `skill-contract`, `integration-readiness`, and
  `evidence-quality`

## Confidence

High on direction: Option B is the right target.

Medium-high on live replacement: proof is still required before the draft can be
called ready.
