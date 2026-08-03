---
title: Anthropic skill-creator base adoption
skill: skill-creator
owner: skill-creator
status: active
kind: skill-audit
date: 2026-07-19
created_at: 2026-07-19
change_type: cross-skill-eval-lifecycle
review_route: inline-review
reasoning_basis: upstream comparison, local contract review, focused tests, production build
eval_required: yes
upstream_commit: fa0fa64bdc967915dc8399e803be67759e1e62b8
proof_artifacts:
  - skills/eval/tests/test_run_evals.py
  - skills/skill-creator/evals/evals.json
  - skills/skill-maintenance/evals/evals.json
  - skills/skill-maintenance/graph/farplane-lifecycle-graph.json
---

# Anthropic Skill-Creator Base Adoption

Upstream source: `anthropics/skills/skills/skill-creator` at commit
`fa0fa64bdc967915dc8399e803be67759e1e62b8`.

The exact upstream package and the pre-change Farplane packages are preserved
under ignored `.farplane/upstream/` and `.farplane/import-backups/` paths.

## Mapping

| Upstream surface | Decision | Farplane owner |
| --- | --- | --- |
| Creation and initial iteration flow | adapt | `skill-creator` |
| `evals/evals.json` convention | adopt | `eval` plus target skill |
| grader and evidence schema | adapt | `eval` runner artifacts |
| candidate/baseline comparison | adopt | `eval` |
| timing and benchmark aggregation | adapt | `eval` |
| analyzer and next-hypothesis loop | adapt | `self-improve` |
| description optimization | defer | future `self-improve` mode |
| bundled eval viewer | reject | Farplane UI already owns Eval OS |
| package and validation helpers | retain local | `skill-creator` and `skill-maintenance` |

## Prompt Boundary

The 485-line upstream `SKILL.md` is a reference implementation, not the active
Farplane prompt. Farplane keeps first-load creation, routing, gates, and proof
in `skill-creator/SKILL.md`; conditional eval mechanics live in `eval`, and
candidate search lives in `self-improve`.

## Structure Review

| Check | Verdict | Evidence |
| --- | --- | --- |
| first-load sufficiency | pass | Creation and maintenance contain explicit eval handoffs. |
| reference-load precision | pass | Artifact schema and self-improve detail live in conditional references. |
| missing-context risk | pass | Suite, baseline, candidate, and promotion obligations are named in first load. |
| noisy-context risk | pass | Upstream mechanics were split by owner instead of copied into the active prompt. |
| duplicated instructions | pass | Eval execution has one owner; the other skills only call it. |
| maintenance locality | pass | Suite beside target skill; experiment memory in self-improve; viewer in Eval OS. |
| composition clarity | pass | `skill-creator -> eval -> self-improve -> skill-maintenance` boundaries are explicit. |
| task success rate | unknown | Contract tests pass; no paid live-agent benchmark was run in this implementation pass. |

## Proof

- `python3 skills/eval/tests/test_run_evals.py` — 37 passing tests.
- `python3 skills/skill-maintenance/scripts/check_skills.py --write` — registry,
  graph, surface-budget, config, eval-query, and reference checks pass.
- Farplane UI Eval OS — 13 focused tests, root bridge typecheck, and production
  Vite build pass.
- Live install completed through `farplane install`; prior live state is backed
  up under `~/.codex/.install-backups/20260719-134824`.
