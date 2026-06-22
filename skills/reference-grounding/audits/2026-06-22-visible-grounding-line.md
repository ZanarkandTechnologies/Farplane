---
skill: reference-grounding
date: 2026-06-22
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/reference-grounding/SKILL.md
after_ref: skills/reference-grounding/SKILL.md
reasoning_basis: advise
proof_artifacts:
  - .farplane/evals/runs/20260622-100058-reference-grounding-smoke-all/summary.json
eval_required: yes
---

# Skill Audit

## Change

- Before: `reference-grounding` asked for compact evidence, but direct answers
  could satisfy the rule invisibly or skip it without a visible reason.
- After: direct answers that depend on real-world practice, current docs, peer
  norms, or implementation examples must include a compact `Grounding:` line
  naming the source class used or why grounding was intentionally skipped.
- Why: The operator observed that global "ground yourself" guidance was not
  showing up in behavior; the missing lever was an observable proof signal.
- Tradeoff accepted: Slightly more first-load skill text in exchange for a
  visible compliance check.

## First-Principles Reasoning

- Objective: Make compact grounding observable without turning every answer
  into a research brief.
- Placement logic: The global template owns the cross-repo trigger; this skill
  owns the reusable grounding output contract.
- Expected behavior delta: Agents surface `Grounding:` for real-world or
  current-practice answers and state a skip reason for tiny local-only work.
- Proof needed: A skill-local eval loads the skill context and checks for the
  visible evidence line behavior.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` Todo List and Output now name `Grounding:`. |
| `reference_load_precision` | pass | No new reference file required; behavior is first-load. |
| `missing_context_rate` | unknown | Requires real harness eval runs over multiple prompts. |
| `noisy_context_rate` | pass | Added 20 lines to a Tier 1 skill and 5 global-template lines. |
| `duplicated_instruction_count` | pass | Global template triggers visible grounding; skill owns output detail. |
| `prompt_size_tokens` | unknown | Token count not measured. |
| `task_success_rate` | pass | Custom eval smoke passed: `20260622-100058-reference-grounding-smoke-all` with two A verdicts. |
| `review_tas_rate` | unknown | No reviewer lane was run for this small direct fix. |
| `maintenance_locality` | pass | Change stays in global template plus owning skill package. |
| `composition_clarity` | pass | `research:*` remains the escalation path for broader synthesis. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/reference-grounding/eval_task.json`
- Structure evals, when needed: not needed
- Reviewer receipt: not run
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py`
- Eval required: yes
- Evidence gaps: Full Codex harness eval with live browsing/tool behavior was
  not run; the smoke proves task loading and expected output contract shape.

## Before Behavior

- Grounding could happen in private reasoning or be omitted from the answer.
- Skip reasons for local-only tasks were not an explicit output obligation.

## After Behavior

- Real-world/current-practice answers expose the evidence class with
  `Grounding:`.
- Tiny local-only work can skip external grounding only with a visible reason.

## Followups

- Run a real Codex harness eval after the next install/template sync if the
  operator wants live-agent proof rather than a custom-runner smoke.
