---
skill: runtime-debugging
date: 2026-08-26
change_type: behavior
owner: skill-maintenance
status: reviewed
review_route: reviewer
before_ref: skills/runtime-debugging/SKILL.md
after_ref: skills/runtime-debugging/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/runtime-debugging/SKILL.md
  - skills/runtime-debugging/references/runtime-repro.md
  - skills/runtime-debugging/README.md
eval_required: no
---

# Skill Audit

## Change

- Before: the reproducible-bug path asked for a codepath map and hypothesis set
  but did not force the nearest per-item control check before platform research.
- After: the first-load workflow requires the shortest local control path,
  cheapest discriminating check, same-repro rerun, and explicit escalation gate.
- Why: a skill-visibility incident spent roughly 17 minutes on a speculative
  platform-capacity theory after the local metadata would have explained the
  eight missing skills directly.
- Tradeoff accepted: some cases take one extra local inspection before broad
  research; that cost is lower than unfocused investigation.

## First-Principles Reasoning

- Objective: reach the first sufficient root cause with the least evidence work.
- Placement logic: the default order belongs in `SKILL.md`; the detailed
  configuration/package/discovery branch belongs in `runtime-repro.md`.
- Expected behavior delta: inspect effective config, package identity, and
  nearest metadata before binaries, release source, or broad searches.
- Proof needed: structural validation, focused behavior comparison, and review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Todo item 4 makes the required ordering explicit. |
| `reference_load_precision` | pass | `runtime-repro.md` owns only the detailed local-control branch. |
| `noisy_context_rate` | pass | Global research is gated behind failed local checks. |
| `task_success_rate` | unknown | No dedicated instruction-following evaluator exists for this skill. |
| `maintenance_locality` | pass | Changes stay in the runtime-debugging package. |

## Proof Artifacts

- Structure validation: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Behavior comparison: the recorded skill-visibility incident is the negative
  case; the new path reaches `agents/openai.yaml` before platform research.
- Reviewer receipt: pass (TAS-A); the primary strategy routes qualifying
  symptoms to the local-control path before broad codepath tracing.
- Eval required: no; static workflow change with an observed hardcase and no
  local behavior-eval harness.

## Before Behavior

```text
repro -> codepath map -> broad hypotheses -> platform-capacity research
```

## After Behavior

```text
repro -> effective config -> package identity -> item metadata -> patch -> rerun
```

## Followups

- Add an instruction-following eval when the project has a suitable local skill
  behavior harness.
