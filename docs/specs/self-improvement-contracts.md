---
status: draft
owner: Farplane
created_at: 2026-06-10
ticket: TASK-0190
---

# Self-Improvement Contracts

## Purpose

Farplane self-improvement work should compose through explicit contracts, not
through overloaded skill names. A skill signature is the compact callable shape
that lets an operator or agent see how one skill's output feeds the next.

## Signature Grammar

Use a compact text block in `SKILL.md`:

```text
skill_action(required_text, optional_field?, state?) -> primary_output + evidence?
state: reads(...); writes(...); remembers(...)
gates: proof_condition; review_condition; blocker_condition
routes: next-skill | next-skill:method | direct-answer
fails: known bad behavior; overbroad behavior; misplaced ownership
```

Guidelines:

- Prefer plain text fields over verbose type systems unless a script or schema
  consumes the contract.
- `expected_behavior` can include a positive example, but the two are not
  identical. Use positive examples as calibration evidence.
- `state` means durable files, tickets, evals, run artifacts, memory, or
  surrounding context read or written by the skill.
- `gates` names what must be true before the output is trusted.
- `routes` names valid next owners, not every possible caller.
- `fails` names the anti-patterns the skill exists to prevent.

## Minimal Behavior-Fix SOP

```text
observe_wrong_behavior
  -> gap_analysis(target, expected_behavior?, evidence?)
  -> harness_place(gap_report)
  -> eval(task_intent, mode?)
  -> direct_change | self_improve_experiment(target, metric, search_space?, eval_suite?)
  -> review_change(change_or_evidence)
```

The stable high-level entrypoint is:

```text
optimize_harness(observed_behavior, expected_behavior?, metric?, evidence?)
  -> accepted_change | experiment_plan | blocked_report
```

## Core Skill Signatures

```text
gap_analysis(target, expected_behavior?, evidence?) -> gap_report + next_owner
state: reads(target_artifact, relevant_context, supplied_evidence); writes(gap_report?)
gates: current_state:grounded; expected_behavior:explicit_or_marked_unknown; owner_surface:named
routes: harness-advisor | eval | self-improve | skill-maintenance | impl-plan | functional-ui | research:gap | direct-fix
fails: jumps to a fix before naming the gap; confuses symptom with owner; invents expected behavior; creates duplicate skills
```

```text
harness_place(gap_or_request, evidence?) -> placement_decision
state: reads(harness doctrine, feature registry, skill registry, relevant surfaces); writes(ticket? handoff?)
gates: failure_named; owner_surface:named; rejected_surfaces:named; proof_path:named
routes: gap-analysis | eval | self-improve | skill-maintenance | impl-plan | spec-to-ticket | direct-answer
fails: defaults to AGENTS.md; creates new skill before checking registry; recommends hooks for judgment-heavy work
```

```text
eval(task_intent, harness?, target_root?, mode?) -> eval_case? + run_summary? + next_fix
state: reads(existing evals, fixtures, task context, expected behavior); writes(eval tasks, hardcase metadata, run artifacts)
gates: expected_behavior:testable; baseline_before_mutation; hardcase:sanitized_and_reusable
routes: optimize-harness | self-improve | skill-maintenance | agent-behavior-test | agent-qa-test | review
fails: wording-only eval; stores raw private transcript; delays obvious regression coverage; marks hardcase without benchmark value
```

```text
self_improve_experiment(target_skill_or_surface, metric, search_space?, eval_suite?) -> best_candidate + experiment_log + promotion_recommendation
state: reads(target package, evals, metric, prior runs, candidate constraints); writes(program.md?, evals?, results?, promoted_change?)
gates: metric_named; baseline_recorded; candidates_compared; promotion_rule_met
routes: eval | goal-advisor | autoresearch-plan | skill-maintenance | review
fails: optimizes by taste; mutates before baseline; promotes unmeasured changes; bloats the target skill
```

```text
optimize_harness(observed_behavior, expected_behavior?, metric?, evidence?) -> accepted_change | experiment_plan | blocked_report
state: reads(gap reports, harness doctrine, registries, evals, target surfaces); writes(ticket?, eval_case?, experiment_artifact?, applied_change?, review_receipt?)
gates: gap_named; owner_surface_named; proof_exists; review_passes_or_blocked
routes: gap-analysis | harness-advisor | eval | self-improve | skill-maintenance | impl | review
fails: changes without proof; optimizes vague taste; creates new skill before checking registry; hides blocked state
```

## Hardcase Rule

`hardcase` is an `eval` mode or metadata flag. It is not a separate skill,
lesson backlog, trouble backlog, or delayed drain process.

A hardcase should be:

- a runnable eval case
- sanitized for private context
- tagged with difficulty and benchmark value
- eligible for normal eval runs

Plain lessons and troubles remain direct docs actions when needed. They are not
part of the core self-improvement skill pipeline.

## Skill Self-Healing Contract

Skill self-healing is a meta pipeline over existing skills, not a scheduler or
new hidden runtime. It starts when an invoked skill fails its advertised
behavior, when a required tool/file/registry row is missing, when a wrapper
returns a gap where a working operation was expected, or when repeated user
correction shows a skill contract is failing.

Core flow:

```text
skill_failure
  -> gap_analysis(skill_operation, expected_behavior, evidence)
  -> skill_failure_packet
  -> safe_local_fix ? repair_ticket : escalation_recommendation
  -> spec-to-ticket | impl-plan | impl | review
```

Preferred failure packet:

```text
skill_failure_packet(skill, operation, expected, observed, failure_class, evidence_refs)
  -> repair_ticket | escalation_recommendation
state: reads(skill registry, capability fixtures, observed run evidence); writes(ticket? artifact?)
gates: failure_grounded; external_body_not_edited_without_operator_request; priority_named
routes: skill-maintenance | self-improve | runtime-debugging | spec-to-ticket | review
fails: silently patches installed external skills; creates hidden repair work; treats opportunity ideas as direct execution
```

Keep capability fixtures small and close to ownership:

- repo-owned skill sanity fixtures live under `skills/<skill>/tests/`
- installed or external skill mirrors live under `tests/<skill>/`
- deterministic fixture validation lives in `bin/check_skill_capabilities.py`
- repair execution still uses the normal ticket pipeline

Opportunity triggers, such as a high-value missing capability inferred from
current work, should create a proposal ticket unless the action is clearly
same-scope and safe. Repair triggers can create repair tickets directly when
the fix is local, non-destructive, and targets repo-owned wrappers, fixtures,
registry rows, or docs.
