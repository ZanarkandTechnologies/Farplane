---
skill: research
date: 2026-08-20
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/external-patterns/SKILL.md@HEAD
after_ref: skills/research/SKILL.md@working-tree
reasoning_basis: eval
proof_artifacts:
  - .farplane/evals/runs/20260820T130634Z-task-0442-research-merge-fixtured-candidate/summary.json
eval_required: yes
---

# Research Code-Pattern Merge Audit

## Change

- Before: `external-patterns` duplicated the public code-pattern route while
  `research:code-patterns` held only a short workflow; Harness Scout and two
  specialist agents still named the wrapper.
- After: `research:code-patterns` is the sole public entrypoint. Conditional
  discovery/deep-dive behavior lives in `references/code-patterns.md`, assigned
  callers route to it, and the wrapper package is deleted without an alias.
- Why: retain the unique outcome and proof behavior while removing a duplicate
  same-tier skill.
- Tradeoff accepted: code-pattern users load one conditional reference after
  method selection instead of a separate top-level skill.

Harness Scout also replaced its retired `summarize` skill call with
`farplane run -- summarize "$source" --extract`, a missing-binary/fallback
gate, and explicit source-identity, untrusted-input, provenance, quote,
grounding, redaction, and retention rules. Its normal path was compacted from
314 to 139 lines; branch detail remains in precise references.

## First-Principles Reasoning

- Objective: one artifact-producing research owner for maintained-repository
  patterns, with no loss of discovery, provenance, failure-path, or local-fit
  evidence.
- Placement logic: method selection and hard route stay in `research/SKILL.md`;
  code-pattern-only search/deep-dive behavior stays in its conditional
  reference; repeatable behavior proof stays in research evals.
- Expected behavior delta: calls select `research:code-patterns`, not a wrapper;
  the Pattern Brief remains equally or more specific.
- Proof needed: line envelope, caller removal, deterministic link/JSON checks,
  focused candidate-versus-baseline behavior eval, and reviewer judgment.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Research selects every method and loads code-pattern detail conditionally; Harness Scout keeps its normal extraction-to-decision path visible. |
| `reference_load_precision` | pass | `references/code-patterns.md` loads only for `research:code-patterns`; Harness Scout branch references have named conditions. |
| `missing_context_rate` | pass | Literal queries, freshness, broad search, 1-3 deep dives, URLs/paths, architecture, tests/failures, comparison, and local adaptation are preserved. |
| `noisy_context_rate` | pass | Research is 156 lines (was 294); Harness Scout is 139 (was 314). |
| `duplicated_instruction_count` | pass | Wrapper removed; no alias or fallback parser added. |
| `prompt_size_tokens` | pass | Physical line envelopes pass at 156 and 139 lines. |
| `task_success_rate` | pass | Focused candidate eval passes 2/2; baseline passes 0/2. |
| `review_tas_rate` | pass | Independent reviewer returned TAS-A with no blockers. |
| `maintenance_locality` | pass | Code patterns have one owner and one conditional reference. |
| `composition_clarity` | pass | Callers and Librarian/Memory agents point to `research:code-patterns`; Harness Scout owns its CLI edge. |

## Proof Artifacts

- Skill-local evals: `skills/research/evals/evals.json` plus offline repository
  evidence fixtures.
- Behavior comparison:
  `.farplane/evals/runs/20260820T130634Z-task-0442-research-merge-fixtured-candidate/summary.json`
  (`candidate_gate_passed: true`, `2/2`; baseline `0/2`).
- Structure: `wc -l` reports Research 156 and Harness Scout 139.
- Validator: `check_skills.py` passes todo/tier checks and currently stops only
  because the concurrently generated `docs/skills/registry.jsonl` is stale;
  registry generation is owned by the parent migration lane.
- Reviewer receipt: TAS-A, no hard-gate failures; rerun not required for this
  representative audit. Parent completion still requires generated-registry
  refresh and full migration review.
- Evidence gaps: no live-network repository lookup was used by the eval; its
  deterministic fixtures test the skill's behavior and provenance contract,
  not the current truth of a named public repository.

## Before Behavior

Installed baseline selected `external-patterns` in both held-out cases and
failed both full Pattern Brief rubrics. Research first load was 294 lines and
Harness Scout first load was 314 lines.

## After Behavior

Candidate selected `research` in both cases and passed both full rubrics,
including literal query construction, maintained-source filtering, broad then
deep search, direct provenance, architecture/file maps, adjacent tests and
failure paths, comparison, and proportional local adaptation.

## Followups

- Parent registry lane regenerates canonical skill registry and removes the two
  curated-plugin allowlist literals in `sync_skill_plugins.py`.
- Parent completion review verifies no live wrapper callers remain across the
  full migration diff.
