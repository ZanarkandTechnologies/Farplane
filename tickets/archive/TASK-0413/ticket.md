---
template_id: ticket-template
template_version: "0.2.5"
feature_refs:
  - FEAT-0008
  - FEAT-0022
  - FEAT-0029
ticket_id: TASK-0413
title: Make demo the default Goal recap workflow
status: done
created_at: 2026-07-26T17:00:00+08:00
updated_at: 2026-07-26T13:35:54.315409Z
---
# TASK-0413: Make demo the default Goal recap workflow

## Summary

Upgrade the outdated `demo` skill into the default evidence-grounded narrated
MP4 recap for material implementation Goals. Keep tickets free of demo
configuration: the demo skill owns the stable production recipe and the Goal
program owns the terminal invocation after QA.

## Scope

- In: demo skill template upgrade, lead-engineer recap method, QA/evals, Goal
  program and compiler wording, validation, audit, and independent review.
- Out: PPTX output, per-ticket demo configuration, generated visual assets,
  automatic external spend, and demos for direct non-Goal work.

## Delta

```text
overall_before:
  - Demo selected among screenshots, HTML, slides, clips, or video.
overall_after:
  - Demo produces one narrated lead-engineer recap MP4 from verified evidence.
  - Material implementation Goals call demo after QA and before completion review.
why_now:
  - Long-running changes need a fast context refresh, not another raw evidence folder.
first_principles_basis:
  objective: make completed Goal work legible and defensible to a lead engineer
  need: problem, decision, final behavior, proof, and residual risk in one artifact
  root_cause: demo packaging has no stable narrative or output contract
  constraints: no ticket schema growth; no unsupported claims or unauthorized spend
  first_viable_slice: deterministic Remotion recap from existing ticket evidence
  proof_or_falsification: skill validation, eval assertions, and TAS-A review
  tradeoff: material Goal completion gains a production step
  non_goals: presentations, marketing videos, or demos for tiny direct fixes
```

## Change Plan

```text
architecture_signatures:
  module_level:
    - demo(ticket, passed_qa, brand_kit?) -> narrated_mp4 + evidence_map + result_json
  main_flow:
    - material implementation Goal -> QA pass -> demo -> completion review -> close
  data_flow:
    - ticket/progress/QA/review evidence -> recap plan -> Remotion render -> reviewed MP4
  builder_freeform_boundary:
    - The demo skill owns recipe detail; Goal program owns only invocation order.
```

### Change 1: Replace generic demo packaging with the recap contract

```text
fixes:
  - ambiguous demo format and weak executive context
write:
  - path: skills/demo/
    change: upgrade template, add method reference, QA, evals, and package docs
routes:
  docs: update_docs
  qa: tests
  review: reviewer
```

### Change 2: Compile demo into material Goal completion

```text
fixes:
  - Goal completion does not reliably invoke the recap
write:
  - path: tickets/templates/goal-loop/program.md
    change: add QA -> demo -> completion review ordering
  - path: skills/goal-advisor/
    change: compile the same default without adding ticket fields
routes:
  docs: update_docs
  qa: tests
  review: reviewer
```

## Done

```text
done_when:
  - demo is on skill-template 0.3.9 with an executable narrated-MP4 default
  - stable recipe detail lives in one demo-owned reference
  - QA and evals reject unsupported evidence, failed QA, PPTX, and unauthorized spend
  - Goal program/compiler invoke demo only for material implementation Goals
  - skill registry validation and independent TAS-A review pass
```

## QA Strategy

```text
qa_strategy:
  proof_weight: review
  checks:
    - parse demo eval JSON and validate skill metadata/links/registry
    - inspect the Goal prompt ordering as QA -> demo -> review -> close
  delegated_lanes:
    - reviewer
  review:
    - rubric: skill + prompt + evidence
      required_tas: TAS-A
  evidence:
    - tickets/TASK-0413/artifacts/
  goal_advisor_inputs:
    proof_route: deterministic checks -> reviewer
    final_evidence: validation receipt and reviewer receipt
    final_checkpoint: TAS-A before completion
  residual_risk:
    - actual recap production remains dependent on available narration/render tooling
```

## Docs Strategy

```text
docs_strategy:
  outcome: update_docs
  doc_targets:
    - skills/demo/README.md
    - skills/demo/references/lead-engineer-recap.md
  validation:
    - python3 skills/skill-maintenance/scripts/check_skills.py --write
```

## Links

- Visual companion: `tickets/TASK-0413/diagrams.md`
- `program:` `none`
- `progress:` `none`
- `artifacts:` `tickets/TASK-0413/artifacts/`
- `review:` `tickets/TASK-0413/artifacts/review/completion-review.md`
- `refs:` `skills/demo/references/lead-engineer-recap.md`

## Notes

- Existing `result.json` verdict compatibility is preserved for runtime
  validators.
