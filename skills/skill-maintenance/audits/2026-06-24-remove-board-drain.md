---
skill: board-drain
date: 2026-06-24
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/board-drain/SKILL.md
after_ref: docs/skills/registry.jsonl
reasoning_basis: first_principles
proof_artifacts:
  - docs/skills/registry.jsonl
  - skills/skill-maintenance/graph/skill-graph.json
eval_required: no
---

# Skill Audit

## Change

- Before: `board-drain` existed as a public Tier 3 selector skill even though
  Goal Advisor now owns board-drain heartbeat policy.
- After: `skills/board-drain/` is removed and generated skill registries/graphs
  show 96 skills instead of 97.
- Why: The operator identified `board-drain` as legacy; keeping it as a public
  skill competes with the canonical Goal Advisor execution compiler.
- Tradeoff accepted: Historical docs still mention board-drain patterns where
  they describe Goal heartbeat policy or archived decisions; only the live
  skill package was removed.

## First-Principles Reasoning

- Objective: Remove a legacy public skill surface without deleting the useful
  board-drain heartbeat concept from Goal Advisor.
- Placement logic: Execution selection belongs under `goal-advisor`; stale
  standalone skill source should not remain discoverable.
- Expected behavior delta: Agents no longer see `board-drain` as an invokable
  skill; they route board-drain-like work through Goal Advisor heartbeat policy.
- Proof needed: registry row count drops, graph docs drop the node, and full
  skill-system validation passes.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `source_owner_preserved` | pass | Board-drain policy remains in Goal Advisor docs/references; live skill package removed. |
| `registry_synced` | pass | `check_skills.py --write` reports 96 skill rows. |
| `doc_refs` | pass | `check_doc_refs.py` passes via `check_skills.py --write`. |
| `graph_synced` | pass | `generate_skill_graph.py` reports 96 nodes and 96 skill docs. |
| `eval_required` | pass | No behavior eval needed for deletion of a legacy public surface. |

## Proof Artifacts

- Validator: pass, `python3 scripts/check_skills.py --write`.
- Graph sync: pass, `python3 skills/skill-maintenance/scripts/generate_skill_graph.py`.
- Harness graph sync: pass, `python3 skills/skill-maintenance/scripts/generate_harness_graph.py`.

## Followups

- Watch for any user habit or automation still invoking `board-drain`; migrate
  those calls to `goal-advisor` heartbeat wording.
