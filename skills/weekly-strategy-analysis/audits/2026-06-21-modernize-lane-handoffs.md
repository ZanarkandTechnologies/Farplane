---
skill: weekly-strategy-analysis
date: 2026-06-21
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/weekly-strategy-analysis/SKILL.md
after_ref: skills/weekly-strategy-analysis/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - /Users/kenjipcx/.codex/skills/skill-creator/SKILL.md
  - docs/skills/system.md
  - docs/skills/README.md
  - docs/skills/best-practices.md
  - skills/skill-maintenance/qa_checklist.md
  - skills/weekly-strategy-analysis/eval_task.json
  - skills/weekly-strategy-analysis/references/weekly-pm-plan-instance.md
  - skills/weekly-strategy-analysis/references/lane-plan-progress.md
  - skills/weekly-strategy-analysis/references/lane-meeting-people.md
  - skills/weekly-strategy-analysis/references/lane-codex-drift.md
  - skills/weekly-strategy-analysis/references/lane-opportunity-scan.md
eval_required: yes
---

# Skill Audit

## Change

- Before: the skill carried a long flat checklist. Lane execution said to split
  analysis into lanes, but did not make bundle-first file refs, lane output
  paths, or subagent/sequential fallback concrete enough.
- After: the skill follows the modern template with Context, Skill Signature,
  ordered Todo List, Source Normalization, Lane Contract, Hard Gates, and
  Reference Map. Lane details moved to focused reference files.
- Why: the live weekly automation needs a reliable ordered workflow before it
  can be folded into `weekly-pm-plan` phase hooks.
- Tradeoff accepted: lane details now require loading a focused reference before
  spawning each subagent, in exchange for a compact first-load skill.
- Skill Creator QA follow-up: removed future-migration prose, a duplicate
  `weekly_pm_plan(...)` first-load example, the duplicated `Output` section,
  and a stale `telegram-message` route.

## First-Principles Reasoning

- Objective: make Kenji weekly strategy automation executable and maintainable.
- Placement logic: source collection and lane handoff rules belong in this
  Kenji-specific wrapper until `weekly-pm-plan` hook support is implemented.
- Expected behavior delta: agents write a context bundle first, then give file
  refs to bounded lane workers, then synthesize from lane output files.
- Proof needed: skill registry validation, eval guardrails, and line-budget
  review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Normal path includes init, gathering, bundle, lanes, synthesis, writeback, gates, outputs. |
| `reference_load_precision` | pass | Context bundle, weekly-pm-plan instance, and each lane reference have explicit read conditions. |
| `missing_context_rate` | pass | Notion, Codex, meetings, opportunity, privacy, and report-order constraints remain in first load. |
| `noisy_context_rate` | pass | Flat 335-line checklist collapsed into ordered 207-line first-load contract; lane specs moved to references. |
| `duplicated_instruction_count` | pass | Lane prose is consolidated into lane references and the first-load todo names when to read them. |
| `prompt_size_tokens` | pass | Line count reduced from 335 to 207. |
| `task_success_rate` | unknown | No live weekly run has used the revised skill yet. |
| `review_tas_rate` | unknown | No reviewer lane was run. |
| `maintenance_locality` | pass | This wrapper owns Kenji-specific source collection; generic policy stays in `weekly-pm-plan`. |
| `composition_clarity` | pass | Signature and state reads/writes name inputs, outputs, and artifacts. |

## Proof Artifacts

- Skill-local evals: `weekly_strategy_context_bundle_before_lanes_01` and
  `weekly_strategy_lane_handoffs_01`.
- Validators:
  - `python3 -m json.tool skills/weekly-strategy-analysis/eval_task.json`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 skills/eval/tests/test_run_evals.py`
  - `git diff --check`
- Eval required: yes.
- Evidence gaps: live automation still points at installed skill copy until
  repo source is installed/synced.

## Before Behavior

- Agents could interpret "lane" vaguely and might run analysis from hidden chat
  context or refetch source data inside each lane.

## After Behavior

- Agents must write the context bundle first, then pass bundle path, lane output
  path, evidence rule, and lane question to each subagent or sequential lane.
  Task-progress and grand-plan priority are merged into `plan-progress`; the
  lane now tracks Plan Week conversion, goal coverage, task drag, plan realism,
  priority changes, due dates, and proof checks.
- Codex drift now lives in `references/lane-codex-drift.md`, prefers supplied
  Farplane-UI / Codex app-server session usage telemetry, and uses raw local
  Codex files only as a labeled fallback.
- Opportunity scan now lives in `references/lane-opportunity-scan.md`, routes
  to `feed-scout:run` when configured, otherwise uses a bounded manual search
  plan with query/result caps, dedupe, URLs, dates, fit, next actions,
  displacement judgment, and confidence.
- `references/weekly-pm-plan-instance.md` maps this wrapper into
  `weekly_pm_plan(project_root, context_refs, window, phase_hooks)` with
  `init_prompt`, `context_gathering_prompt`, `synthesis_prompt`, and
  `reporting_prompt`.
- Skill Creator cleanup removed first-load rationale and duplicated output
  prose while preserving the executable todo path.

## Skill Creator QA Pass

Skill Creator was applied after the initial structure pass. It required
`docs/skills/system.md`, `docs/skills/README.md`,
`docs/skills/best-practices.md`, and
`skills/skill-maintenance/qa_checklist.md`.

| Check | Verdict | Evidence |
| --- | --- | --- |
| `trigger_stable` | pass | Description is 145 characters and routes to one personal weekly strategy wrapper. |
| `template_structure_valid` | pass | `SKILL.md` has Context, Skill Signature, marker-delimited Todo List, Hard Gates, and Reference Map. |
| `first_load_sufficiency` | pass | Default run can initialize, gather, bundle, run lanes, synthesize, and finish from `SKILL.md`. |
| `reference_load_precision` | pass | Each lane reference is loaded only before spawning that lane; PM instance reference is loaded only for generic call compilation. |
| `noisy_context_rate` | pass | Removed migration note, inline generic call example, duplicate Output section, and stale route. |
| `duplicated_instruction_count` | pass | Lane metrics live in lane refs; output shape lives in signature and finish todo. |
| `prompt_size_tokens` | pass | First-load line count is 207, below the roughly 250-line review trigger. |
| `maintenance_locality` | pass | `SKILL.md` owns first-load run contract; lane refs own subagent detail; audit owns migration/history notes. |
| `composition_clarity` | pass | Signature names inputs, outputs, state reads/writes, gates, routes, and fails. |
| `actor_boundary` | pass | Skill defines lane handoff shape but does not own actor identity or tool policy. |
| `quality_example` | deferred | No representative weekly context bundle/report is committed yet; first live run should be saved as the transferable example instead of adding synthetic prose. |

## First-Load Review

```text
line_count_before: 335
line_count_after: 207
kept_in_skill: trigger, signature, ordered workflow, source normalization,
  lane contract, hard gates, reference map
moved_to_reference: weekly-pm-plan instance mapping, plan-progress lane,
  meeting-people lane, Codex drift lane, opportunity-scan lane
deleted_as_duplicate_or_rationale: flat checklist duplication, repeated
  explanatory prose, automation cadence preset that belongs in automations.md,
  future-migration note, duplicate inline weekly_pm_plan example, duplicate
  Output section, and stale telegram route
extra_sections_kept_with_reason: Source Normalization and Lane Contract remain
  first-load because every run needs row shape and handoff shape.
remaining_sections_over_budget: none
verdict: pass
```

## Followups

- Install/sync the updated source skill into `~/.codex/skills` before judging
  live automation behavior.
- Later, replace this wrapper with `weekly-pm-plan` phase hooks once the hook
  interface exists.
