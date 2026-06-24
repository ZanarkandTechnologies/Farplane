---
skill: feed-scout
date: 2026-06-24
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/feed-scout/SKILL.md
after_ref: skills/feed-scout/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/feed-scout/SKILL.md
  - skills/feed-scout/references/workflow.md
  - skills/feed-scout/eval_task.json
eval_required: yes
---

# Skill Audit

## Change

- Before: `feed-scout` could discover and summarize videos/articles, then route
  eligible items into `harness-scout`, but it had no explicit route for feeds of
  book-summary content whose best output is a reusable skill workflow.
- After: `feed-scout` identifies book-summary videos, articles, blogs, public
  notes, app pages, and author interviews as summary-source items, extracts
  key-takeaway workflows with `summarize`, routes skill-worthy results to
  `skill-creator`'s book-summary branch, and is onboarded to
  `skill-template: "0.3.2"`.
- Why: The operator wants curated online book-summary sources to compound into
  better skills, not just content summaries or generic proposals.
- Tradeoff accepted: Keep the first-load rule compact in `SKILL.md` and put
  runbook detail in `references/workflow.md`; do not make `feed-scout` a new
  crawler, book summarizer, or skill writer.

## First-Principles Reasoning

- Objective: Turn repeated online summary-source feeds into workflow candidates
  and skill handoffs while preserving feed-scout's explicit-run, dedupe, and
  proposal boundaries.
- Placement logic: First-load needs the routing branch, callable signature,
  phase boundary, and output distinction; detailed step ordering belongs in the
  workflow reference.
- Expected behavior delta: A dry/live feed run over book-summary sources now
  dedupes, summarizes, extracts workflow-shaped takeaways, checks convergence,
  and routes reusable skill behavior to `skill-creator`.
- Proof needed: Registry validation plus future execution of
  `feed_scout_book_summary_workflow_route_01`.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` names the summary-source route, downstream skill, signature, phase boundary, and output contract. |
| `reference_load_precision` | pass | `references/workflow.md` owns runbook detail already linked from `SKILL.md`. |
| `missing_context_rate` | pass | Dedupe, summarize, routing, no-daemon, and Notion gates remain in first load. |
| `noisy_context_rate` | pass | Initial passes failed this check; mode prose, config JSON, schema list, workflow, branches, judgement questions, and dependency-list boilerplate were removed from first load or kept behind reference routes. |
| `duplicated_instruction_count` | pass | Initial file duplicated `references/workflow.md`, `references/data-model.md`, templates, and signature/todo routing; compacted `SKILL.md` keeps operational routing only. |
| `prompt_size_tokens` | pass | `SKILL.md` is now under the 250-line soft trigger, down from 263 before this change and 329 after the first template pass. |
| `task_success_rate` | unknown | Eval case added; runner execution is pending. |
| `review_tas_rate` | unknown | Self-check only; reviewer can be routed if this becomes a broader source-ingestion standard. |
| `maintenance_locality` | pass | Feed orchestration stays in `feed-scout`; skill-writing detail stays in `skill-creator`. |
| `composition_clarity` | pass | Routes distinguish `summarize`, `skill-creator`, `harness-scout`, and `best-of-worlds`. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/feed-scout/eval_task.json`
- Structure evals, when needed: `skills/skill-maintenance/qa_checklist.md`
  applied manually; first pass found bloat/duplication, second pass passed
  after compaction.
- Reviewer receipt: none
- Validator: `python3 scripts/check_skills.py --write` from
  `skills/skill-maintenance` passed on 2026-06-24.
- Eval required: yes; added case, runner execution pending
- Eval-to-QA sync: no `feed-scout/qa_checklist.md` exists; the new eval points
  are branch behavior guardrails covered in `SKILL.md` and
  `references/workflow.md`.
- Evidence gaps: future real feed run should produce a summary-source handoff
  or ledger row.

## First-Load Review

```text
line_count_before: 263
line_count_after_first_template_pass: 329
line_count_after_final: 146
kept_in_skill:
  - 0.3.2 template frontmatter via template_uses.skill-template
  - Context, Skill Signature, Phase Boundary, Todo List, Templates, Reference Map, and Output sections
  - summary-source routing before ordinary content-summary treatment
  - downstream route distinction for skill-creator, harness-scout, and best-of-worlds
  - outcome contract entry for skill-creator handoff
moved_to_reference:
  - detailed runbook steps for extracting workflow-shaped takeaway signals
  - user-facing modes and mode runbook detail to references/workflow.md
  - judgement questions to references/workflow.md
  - data model detail to references/data-model.md
  - config and DB examples to templates/*
deleted_as_duplicate_or_rationale:
  - duplicated Workflow section from SKILL.md
  - duplicated Decision Branches section from SKILL.md
  - duplicated Minimal Configuration JSON from SKILL.md
  - duplicated Data Model list from SKILL.md
  - dependency-list boilerplate from SKILL.md; signature routes and todos carry
    the real operational links
extra_sections_kept_with_reason:
  - none beyond current template sections; extra mode/schema/runbook sections
    now live in references or templates with explicit load conditions
```

## Before Behavior

- Book-summary feed items could become generic `summarize` outputs or ordinary
  `harness-scout` proposals without preserving the "key takeaway workflow to
  skill" intent.

## After Behavior

- Book-summary feed items have a route: dedupe, summarize, extract
  workflow-shaped takeaways, check convergence, then route skill behavior to
  `skill-creator` and broader harness patterns to `harness-scout`.

## Followups

- Run the new eval case in the next eval batch.
- If repeated real feed runs need a richer packet schema, add it to
  `references/data-model.md` after one concrete run proves the fields.
- Add a skill-maintenance hardening case for "template update must include
  checklist compaction before install" if this pattern recurs.
