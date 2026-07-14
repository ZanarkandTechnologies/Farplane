---
kind: skill-audit
skill: farplane-content-creation
created_at: 2026-07-14
status: implemented
owner: harness
---

# Create The Farplane Content Pipeline

## Decision

Replace the narrow `farplane-evidence-content` capability with one
project-local Tier 3 pipeline. Preserve evidence-to-content grounding, compose
`content-impl-plan` with the planning and execution phases of
`optimize-with-human`, and add approved-exemplar expansion into a controlled
ten-variant search batch.

## Placement

- Primary owner: `.agents/skills/farplane-content-creation/`.
- Not root `AGENTS.md`: this is a callable project workflow, not universal policy.
- Not `templates/global/AGENTS.md`: other projects should not inherit Farplane's creator strategy.
- Not `agents/*.toml`: the behavior is capability logic, not a reviewer or worker persona.
- Not hooks or `bin/*`: the pipeline needs judgment and visible artifacts, not hidden control flow.

## Preserved Mechanics

- one Best Bet by default and at most three proposals;
- human approve/revise/reject loops in planning and execution;
- approved plan reference and frozen execution skeleton;
- evidence/claim mapping and explicit authority gates;
- ticket-backed Goal state and persistent reply ownership for material loops.

## Added Mechanics

- one optimized exemplar before scaling;
- default ten-variant controlled search from declared variable axes;
- invariant checks, expected-learning rows, QA ranking, and a top-two-or-three handoff;
- explicit distinction between creative approval and publication authority.

## Acceptance Checks

- [x] Skill signature exposes inputs, outputs, state, gates, routes, and failures.
- [x] Main contract includes positive and negative examples.
- [x] QA checklist covers planning, execution, variation, review, and authority gates.
- [x] Behavior-sensitive evals cover gate ordering, phase reopening, variant expansion, and publication safety.
- [x] Standard skill and project-file validators pass.
- [x] All four behavior claims have current-source TAS-A evidence.
- [x] Independent reviewer returns TAS-A with no blocking findings.

## QA Application

| Skill Creator guardrail | Result | Evidence |
| --- | --- | --- |
| Stable reusable owner | pass | Project-local Tier 3 capability replaces the narrower content owner. |
| Executable first load | pass | Signature, pipeline state, receipts, gates, examples, and outputs are in `SKILL.md`. |
| Truthful metadata and routing | pass | Local index, market-learning route, and harness area binding use the new ID. |
| Conservative scaffolding | pass | No controller, hook, scheduler, alias, or compatibility shim was added. |
| Risk-matched proof | pass | Skill QA, four adversarial evals, project validators, and native reviewer receipt exist. |

## Validation Evidence

- `python3 skills/skill-maintenance/scripts/check_skills.py --write` — pass;
  registry, tier, surface-budget, capability, eval-query, doc-ref, and compile
  checks passed.
- `python3 bin/farplane.py project snapshot --project-root . --json` — refreshed
  ignored UI projection after the harness binding changed.
- `python3 bin/validators/check_farplane_project_files.py --root .` — pass.
- JSON and YAML parse checks — pass.

## Behavior Evidence

- Planning default and planning-reopen cases: TAS-A in
  `.farplane/evals/runs/20260714-083350-farplane-content-creation-v9-final/`.
- Controlled variation matrix and top-only handoff: TAS-A in
  `.farplane/evals/runs/20260714-083744-farplane-content-creation-v10-final/`.
- Authority and missing-input gate: TAS-A in
  `.farplane/evals/runs/20260714-084026-farplane-content-creation-v11-final/`.
- Initial failures were retained under `.farplane/evals/runs/` and used to
  harden required state receipts, recommendation judgment, named QA results,
  internal-proof ownership, and separate action authority.

## Independent Review

- Receipt: `audits/2026-07-14-independent-review.md`.
- Verdict: TAS-A / pass; no blocking findings.
