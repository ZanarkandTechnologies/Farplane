---
skill: pulse-update
date: 2026-07-13
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/pulse-update/SKILL.md
after_ref: skills/pulse-update/SKILL.md
reasoning_basis: reviewer
proof_artifacts:
  - /Users/kenjipcx/.codex/sessions/2026/07/13/rollout-2026-07-13T18-59-58-019f5b22-3ee1-7d11-abca-03029b76a751.jsonl
  - /Users/kenjipcx/.codex/archived_sessions/rollout-2026-07-13T20-52-23-019f5b89-296a-7990-85ee-98f5f84b3f3b.jsonl
  - skills/pulse-update/evals/evals.json
  - .farplane/evals/runs/20260713-125422-20260713-clean-worker-thread/summary.json
  - .farplane/evals/runs/20260713-125901-20260713-clean-worker-thread-regression/summary.json
  - .farplane/evals/runs/20260713-130021-20260713-clean-worker-thread-regression-final/summary.json
eval_required: yes
---

# Clean Worker Thread Creation Audit

## Change

- Before: Pulse required one persistent task per ticket but did not distinguish
  clean creation from a context-inheriting fork.
- After: new ticket workers use `create_thread` with the delegation as the
  initial prompt, reject inherited manager lineage/history before claim or
  ledger registration, and reserve forks for tasks that require source history.
- Why: TASK-0347 was created with `fork_thread`, copying the complete Work Pulse
  heartbeat transcript into a bounded worker task.
- Tradeoff accepted: clean workers must receive complete context refs in their
  delegation packet instead of relying on hidden manager history.

## First-Principles Reasoning

- Objective: isolate ticket execution context while preserving visible,
  persistent worker tasks.
- Placement logic: `pulse-update` owns worker admission and creation behavior;
  the automation prompt owns cadence and root policy does not need expansion.
- Expected behavior delta: a new worker's first task turn is its delegation,
  with no `forked_from_id` or pre-delegation heartbeat turns.
- Proof needed: regression eval wording, skill-system validation, installed-copy
  sync, clean-create runtime probe, and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Clean-create and lineage gates are in the dispatch todo and signature gates/fails. |
| `reference_load_precision` | pass | No new reference dependency. |
| `missing_context_rate` | pass | Worker handoff remains complete and now explicitly replaces inherited context. |
| `noisy_context_rate` | pass | The change removes copied manager history from future workers. |
| `duplicated_instruction_count` | pass | Todo owns execution; contract/outcome text states the data shape and invariant. |
| `prompt_size_tokens` | pass | Added only the hard runtime boundary required before dispatch. |
| `task_success_rate` | unknown | Requires future production worker evidence. |
| `review_tas_rate` | pass | Independent review found the behavior and placement correct; the requested audit repair is applied here. |
| `maintenance_locality` | pass | Worker creation remains owned by `skills/pulse-update/SKILL.md`. |
| `composition_clarity` | pass | Creation mode, verification gate, and failure behavior are explicit. |

## First-Load Review

```yaml
first_load_review:
  line_count_before: 355
  line_count_after: 389
  kept_in_skill: [clean-create dispatch gate, lineage verification, failure handling]
  moved_to_reference: []
  deleted_as_duplicate_or_rationale: []
  extra_sections_kept_with_reason: [Worker Handoff Contract is an existing runtime schema]
  remaining_sections_over_budget: [existing skill remains above the approximate 250-line advisory threshold]
  proof_surface_fit: eval plus live clean-create probe
  task_case_quality: dedicated worker-context case covers the observed fork regression
  anti_cheat_case_design: prompt describes the context boundary without prescribing the expected primitive
  qa_preflight_loaded: inline Todo List is the target runtime guardrail
  qa_finish_independence: reviewer required
  qa_gotcha_deduplication: no new standalone gotcha
  project_specific_context_isolation: generic across Farplane projects
  low_value_prose_scan: new text changes runtime selection, verification, or failure behavior
```

## Proof Artifacts

- Skill-local evals: `skills/pulse-update/evals/evals.json`; the initial generic
  case exposed a proof-design mismatch, so a dedicated natural worker-context
  regression now tests clean creation, no fork, pre-claim lineage verification,
  and post-verification canonical titling. Its first run met all four core
  regression points; two unrelated lifecycle assertions were removed from this
  case while remaining mandatory in the skill contract.
- Final dedicated regression: TAS-A with all four defect-specific reference
  points met at
  `.farplane/evals/runs/20260713-130021-20260713-clean-worker-thread-regression-final/summary.json`.
- Structure evals: `skills/skill-maintenance/scripts/check_skills.py --write`
- Reviewer receipt: final TAS-A with no blockers after audit repair; behavior,
  smallest-owner placement, runtime proof, and defect-specific eval all passed.
- Validator: `check_skills.py --write` passed; installed `pulse-update` skill
  and eval copies matched repo source after `farplane install`.
- Eval required: yes
- Runtime probe: clean task `019f5b89-296a-7990-85ee-98f5f84b3f3b` had no
  `forked_from_id`, exactly one initial delegation turn, returned
  `CLEAN_WORKER_PROBE_OK`, and was archived after inspection.
- Evidence gaps: next real production Pulse-dispatched worker observation.

## Before Behavior

- Pulse called `fork_thread` for TASK-0347, then renamed the fork and sent a
  delegation, leaving the worker with the manager's historical heartbeats.

## After Behavior

- Pulse calls clean thread creation with the full handoff as the initial prompt
  and rejects inherited lineage before ticket claim or worker registration.

## Followups

- Observe the next real Pulse-dispatched ticket worker and attach its clean
  lineage receipt if the runtime probe passes.
