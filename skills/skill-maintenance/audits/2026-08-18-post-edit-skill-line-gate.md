---
skill: skill-maintenance
date: 2026-08-18
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: HEAD
after_ref: working-tree
reasoning_basis: first_principles
proof_artifacts:
  - hooks/skill_file_line_gate.py
  - bin/tests/test_skill_file_line_gate.py
  - bin/validators/test_check_source_line_growth.py
eval_required: no
---

# Post-Edit Skill Line Gate Audit

## Change

- Before: skill size was advisory and an oversized edit received no immediate
  repair feedback; the current commit gate allowed oversized legacy skills to
  hold their line count.
- After: `PostToolUse` checks only `SKILL.md` paths named by an `apply_patch`
  command and returns repair feedback above 200 physical lines. A strict staged
  validator repeats the invariant before commit.
- Why: the useful repair moment is immediately after the edit, while the file
  and intent are still in context.
- Tradeoff accepted: the hook does not scan untouched skills or undo an edit;
  it asks the active agent to repair the applied change.

## First-Principles Reasoning

- Objective: make the 200-line skill envelope immediate, deterministic, and
  difficult to bypass accidentally.
- Placement logic: `PostToolUse` owns feedback, the existing source-line
  validator owns commit enforcement, and skill-maintenance owns safe repair.
- Expected behavior delta: an oversized skill edit causes the same agent turn
  to continue with exact file/count evidence and a source-preservation rule.
- Proof needed: 200/201 boundaries, touched-path scoping, staged-index strict
  behavior, install inventory, live hook doctor, skill-system checks, and review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | creator and maintenance contracts name the cap, feedback loop, backstop, and no-hiding rule |
| `reference_load_precision` | pass | conditional detail placement remains unchanged |
| `missing_context_rate` | pass | default-path preservation is included in hook feedback and both skills |
| `noisy_context_rate` | pass | policy delta adds only the deterministic invariant |
| `duplicated_instruction_count` | pass | hook, validator, and skills have separate runtime, enforcement, and repair jobs |
| `prompt_size_tokens` | pass | edited skill entrypoints are 169 and 184 lines |
| `task_success_rate` | pass | focused unit and integration tests pass |
| `review_tas_rate` | pass | independent reviewer returned TAS-A with no P1/P2 defects |
| `maintenance_locality` | pass | existing hook, validator, installer, and skill owners are reused |
| `composition_clarity` | pass | feedback → repair → staged backstop is explicit |

## Proof Artifacts

- Skill-local evals: skipped because the behavior is a deterministic file
  invariant with exact unit/integration tests; no model-judged workflow changed.
- Structure checks: `check_skills.py --write` passed for all 122 registry rows.
- Validator: the complete focused hook/install/validator suite passed 44 tests;
  harness invariants, doc refs, Python compilation, and diff hygiene passed.
- Live install: `farplane hooks doctor --json` reports the PostToolUse command
  linked, executable, and healthy with no issues.
- Reviewer receipt:
  `2026-08-18-post-edit-skill-line-gate-review.md` records TAS-A with no required fixes.
- Evidence gaps: Codex requires one-time operator trust when a hook-config hash
  changes; deterministic invocation is proven independently of that UI gate.

## Before Behavior

Editing an oversized `SKILL.md` completed silently, and commit-time source-line
enforcement did not provide a strict skill-specific backstop.

## After Behavior

An `apply_patch` touching an oversized `skills/**/SKILL.md` returns exact repair
feedback after the edit; the staged gate blocks the same file above 200 lines.

## Followups

- Review and trust the revised hook configuration once through Codex `/hooks`.
