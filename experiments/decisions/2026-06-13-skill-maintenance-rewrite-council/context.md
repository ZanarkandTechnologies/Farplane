---
title: "Skill Maintenance Rewrite Council Context"
status: active
owner: deliberative-advice
created_at: 2026-06-13
updated_at: 2026-06-13
tags:
  - deliberative-advice
  - skill-maintenance
  - council
  - skill-design
refs:
  - skills/skill-maintenance/SKILL.md
  - skills/optimize-harness/SKILL.md
  - docs/specs/self-improvement-contracts.md
  - docs/skills/best-practices.md
  - skills/skill-maintenance/qa_checklist.md
---

# Skill Maintenance Rewrite Council Context

## Decision

Should Farplane rewrite `skills/skill-maintenance/SKILL.md` into a tighter
behavior-delta entrypoint with variable/pseudocode todos, similar in spirit to
`optimize-harness`, or should it keep the current verbose checklist structure?

## Why This Matters

`skill-maintenance` is the entrypoint the operator uses whenever they want to
update a skill. It needs to be fast and clear enough for frequent use, but it
also owns high-risk safeguards: source ownership, registry sync, template
version correctness, audit records, and review routing. A bad rewrite could
make the skill easier to scan but less reliable.

The operator specifically disliked weak confidence in prior advice. The goal of
this council is to produce a stronger, better-grounded recommendation about the
rewrite shape and implementation constraints.

## Prior Discussion Summary

The thread produced these observations:

- The current `skill-maintenance/SKILL.md` is broad and verbose.
- It currently has two signatures:
  - `maintain_skills(...)`
  - `audit_skill_structure(...)`
- The operator sees `skill-maintenance` as the wide entrypoint for all skill
  updates, so two equal signatures may feel split-brained.
- The operator proposed a PPO-like behavior-delta signature:

  ```text
  skill_maintenance(good_expected_behaviour, current_behaviour, skill_N)
    -> updated skill_N
  ```

- The operator also proposed variable-style todos and pseudocode branches, such
  as:

  ```text
  if edited_skill.eval_task changed:
    compare edited_skill.eval.reference_points against edited_skill.qa_checklist
    promote reusable runtime guardrails
  ```

- Earlier assistant advice recommended a conservative compression:
  one behavior-delta signature, mode-based todos, hard gates inline, verbose
  policy moved to references.
- A first council pass agreed mostly with conservative compression but was
  weakened by thin subagent prompts. This packet tests the improved council
  handoff pattern.

## Current Behavior

`skills/skill-maintenance/SKILL.md` currently:

- describes `skill-maintenance` as the owner for bulk Farplane skill upkeep
- includes two signature blocks
- has a 10-step todo list:
  - load baseline
  - classify maintenance operation
  - route non-mechanical choices
  - record edit boundary
  - prototype broad rewrites
  - edit target `SKILL.md`
  - verify template structure
  - run `check_skills.py --write`
  - reinstall when live behavior matters
  - review readiness
- keeps many first-load rules in `Core Rules`
- is near the 250-line threshold referenced by the skill-structure checklist

## Expected Behavior

The ideal `skill-maintenance` should:

- feel like the direct entrypoint for updating any skill
- bind variables such as `edited_skill`, `expected_behavior`,
  `current_behavior`, `change_scope`, and `evidence`
- make branch logic explicit through readable pseudocode
- keep every-invocation hard gates inline
- move conditional or verbose details into references
- preserve audit/proof safety
- make eval-to-QA sync explicit when `edited_skill.eval_task` changes
- pass existing skill-system validators and skill-structure review

## Options Under Consideration

### Option A: Keep Current Structure With Minor Wording Edits

Do not substantially rewrite `skill-maintenance/SKILL.md`. Add only targeted
lines such as eval-to-QA sync and maybe rename the signatures.

Strength:

- lowest regression risk
- preserves all visible safeguards

Risk:

- keeps high cognitive load
- does not solve the split-entrypoint feeling
- misses the chance to make skill updates feel like a clean transformation

### Option B: Conservative Behavior-Delta Compression

Rewrite `skill-maintenance/SKILL.md` around one primary behavior-delta
signature and mode-based pseudocode todo list. Keep hard gates inline; move
long rationale, examples, audit rubric detail, and rare recipes to references.

Candidate signature:

```text
skill_maintenance(expected_behavior, current_behavior, edited_skill, mode?, evidence?)
  -> updated_skill | audit_record | blocked_report
state: reads(edited_skill.SKILL.md, edited_skill.references?, edited_skill.eval_task?,
             edited_skill.qa_checklist?, registry, prior_audits?, run_artifacts?)
       writes(edited_skill.SKILL.md?, edited_skill.references?, edited_skill.eval_task?,
              edited_skill.qa_checklist?, audit?, registry)
modes: structure_update | metadata_update | eval_to_qa_sync | audit | bulk_rollout | registry_validation
gates: behavior_delta_named; owner_surface_clear; first_load_executable;
       eval_guardrails_synced_or_skipped; check_skills_passed;
       audit_or_skip_recorded; reviewer_routed_when_material
fails: vague update; hidden installed-copy edit; eval changed without QA-sync check;
       bloated first-load contract; audit skipped for material change
```

Candidate todo shape:

```text
1. Bind edited_skill, expected_behavior, current_behavior, mode, evidence.
2. Read edited_skill.SKILL.md plus only branch-required files.
3. Compute behavior_delta := expected_behavior - current_behavior.
4. Choose owner surface:
   if first-load behavior changes: edit edited_skill.SKILL.md
   else if branch detail/template/example changes: edit edited_skill.references
   else if repeatable behavior proof changes: edit edited_skill.eval_task
   else if runtime guardrail changes: edit edited_skill.qa_checklist or validator candidate
5. If edited_skill.eval_task changed:
   compare changed reference_points against edited_skill.qa_checklist
   promote reusable runtime guardrails
   record skipped rare/hardcase/judgment points in audit
6. Validate with check_skills.py --write and focused checks.
7. Write audit or skip reason; route reviewer when material.
```

Strength:

- directly addresses operator workflow
- lowers scan cost
- makes state variables and branch behavior explicit
- keeps proof gates

Risk:

- could over-abstract and hide required safety rules if not careful
- needs proof against existing `skill-maintenance` eval cases

### Option C: Full Rewrite Plus Script-Assisted Detection

Rewrite the skill aggressively and introduce helper scripts such as:

```text
inspect_skill_change(edited_skill) -> changed_surfaces
compare_eval_to_checklist(edited_skill) -> candidate_guardrails + missing_checks
```

Strength:

- strongest mechanical support
- can reduce manual checklist burden

Risk:

- larger implementation blast radius
- the judgment-heavy parts cannot be fully scripted
- risks introducing a brittle half-automation before the contract is stable

## Known Evidence

Relevant files:

- `skills/skill-maintenance/SKILL.md`
- `skills/skill-maintenance/eval_task.json`
- `skills/skill-maintenance/qa_checklist.md`
- `skills/optimize-harness/SKILL.md`
- `docs/specs/self-improvement-contracts.md`
- `docs/skills/best-practices.md`
- `skills/skill-maintenance/scripts/check_skills.py`

Current grounding:

- `self-improvement-contracts.md` supports compact signatures with explicit
  `state`, `gates`, `routes`, and `fails`.
- `best-practices.md` says first-load sufficiency beats modular neatness but
  also treats oversized first-load context as a reliability risk.
- `optimize-harness` is compact because it is a router, while
  `skill-maintenance` owns concrete skill-system mechanics.
- `skill-maintenance/eval_task.json` tests sandboxing, registry sync, source
  ownership, and honest blocker/proof behavior.

## Relevant Files

Each lane should read at least:

- `skills/skill-maintenance/SKILL.md`
- `skills/optimize-harness/SKILL.md`
- `docs/specs/self-improvement-contracts.md`
- `docs/skills/best-practices.md`

Lanes focused on evidence or safety should also read:

- `skills/skill-maintenance/eval_task.json`
- `skills/skill-maintenance/qa_checklist.md`
- `skills/skill-maintenance/scripts/check_skills.py`

## Constraints And Non-Goals

- Do not edit files in this council pass.
- Do not decide by majority vote; rank argument quality and local fit.
- Do not remove hard gates such as source ownership, prototype-before-bulk,
  `check_skills.py --write`, audit-or-skip reason, reinstall checks when live
  behavior matters, and reviewer routing for material changes.
- Do not require an implementation ticket for this advice-only council pass.
- Do not optimize only for brevity; optimize for repeatable correct skill
  maintenance from files alone.

## Lane Briefs

### Operator Value

Focus on the operator's day-to-day workflow: speed, cognitive load, expressive
fit, confidence, and how often this skill is invoked.

### Engineering Risk

Focus on implementation safety: validators, template compatibility, lost gates,
scriptability, proof, and migration blast radius.

### Evidence Skeptic

Focus on what is actually proven by repo evidence, where the theory is
unsupported, and which tests or prototypes should be required.

### Systems Fit

Focus on owner surfaces: what belongs in `SKILL.md`, references, scripts, evals,
docs, agent prompts, or tickets.

## Output Shape

Each lane must return:

- recommendation
- strongest opposing point
- evidence that would change their mind
- concrete implementation constraints
- confidence

## Critique And Ranking Plan

After first-pass lane outputs are captured, the chair should compare three final
options:

1. keep current structure with minor edits
2. conservative behavior-delta compression
3. full rewrite plus script-assisted detection

The chair should recommend one option, preserve dissent, and name the next
owner and proof surface.

## Proof Or Next Owner

If the recommendation is to change the skill, next owner is `skill-maintenance`.

Proof should include:

```text
python3 skills/skill-maintenance/scripts/check_skills.py --write
python3 -m json.tool skills/skill-maintenance/eval_task.json
structure checklist pass/fail audit
reviewer pass for skill-contract + integration-readiness + evidence-quality
```

If the recommendation is to prototype first, use a fixture or branch-local
variant before applying the rewrite to the live skill.
