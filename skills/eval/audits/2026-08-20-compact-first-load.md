---
title: Compact Eval first-load contract
owner: eval
status: accepted
kind: skill-maintenance-audit
created_at: 2026-08-20
ticket_id: TASK-0437
---

# Compact Eval first-load contract

## Bound change

- Target: `skills/eval/SKILL.md`
- Mode: `refine_skill`
- Constraint: preserve Eval triggers, executor selection, task ownership,
  anti-cheat gates, proof modes, artifact inspection, review, and output while
  meeting the 200-line envelope.
- Owning template: `docs/skills/templates/SKILL_TEMPLATE.md`
- Value function: execution + proof + routing + reuse + memory + user value,
  minus duplication, stale risk, fluff, and wrong-owner risk.

## Unit decisions

- Keep: frontmatter methods, concise context, callable signature, five-step
  normal path, artifact contract, hard gotchas, and exact output.
- Merge: mode descriptions, setup routing, authoring rules, proof selection,
  evidence inspection, and review gates into the numbered Todo List.
- Move: branch-specific setup, writing, placement, behavior-trace,
  consolidation, automation, and lifecycle detail behind existing references
  with explicit load conditions.
- Delete: the skill-local budget type, duplicated Tier 0 phase contract and
  boundary, repeated workflow prose, and the long output inventory.

## Loss check and proof

- Size: 342 lines before; 145 after.
- Preserved: Promptfoo skill comparison, project/trace runner, Agent Skills
  source format, hardcase, experiment preregistration, one-worker trace,
  consolidation, anti-spoiler QA, owner-local repair, Office artifacts, and
  independent review.
- Validation: skill registry/checklist/link/query/doc checks and focused
  Promptfoo adapter tests pass.
- Eval skip reason: this is behavior-preserving first-load compaction forced by
  a deterministic line-limit gate; no Eval runtime or task row changed. The
  replacement proof is owner-validator success, critical-contract loss check,
  and independent skill review.
- Remaining risk: phrasing is denser; future observed routing misses should
  become a focused Eval regression before adding prose back.
