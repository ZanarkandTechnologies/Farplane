---
ticket_id: TASK-0356
title: Align the QA guide, tester contract, and learning loop
status: done
created_at: 2026-07-14T04:25:00+08:00
updated_at: 2026-07-14T04:43:00+08:00
---

# TASK-0356: Align the QA guide, tester contract, and learning loop

## Summary

Align the human QA guide, `qa` skill, `qa-tester`, cookbook, receipt validator,
and behavior cases around one current ticket-proof journey. Preserve the
existing July 13 single-owner QA edits while fixing stale ticket fields,
unconditional browser artifacts, ambiguous writeback, weak receipts, and lost
reusable learning.

## Scope

- In: `qa/`, `skills/qa/`, `agents/qa-tester.toml`, a skill-local receipt
  validator/test, QA eval rows, the known `core-hooks-runtime` lifecycle drift,
  and ticket-scoped audit/review evidence.
- Out: new skills, hooks, browser tools, global prompt policy, downstream app
  Playwright suites, or changes to visual/reviewer judgment semantics.

## Delta

```text
before: browser-first guide + current qa skill + stale oversized tester + weak learning writeback
after: one qa contract drives proof selection, capture, judgment, receipt, ticket writeback, and learning classification
why_now: operator review exposed execution drift behind a sound conceptual model
first_principles_basis:
  objective: make QA repeatable, inspectable, and progressively easier
  root_cause: duplicated contracts drifted while the ticket schema evolved
  constraint: preserve unrelated dirty-worktree and existing single-owner QA changes
  first_viable_slice: align existing owners and prove the contract with deterministic fixtures plus a real harness run
  tradeoff: synchronized multi-surface edit instead of another partial docs-only fix
  non_goals: universal QA keyboard mode or hidden orchestration
```

## Change Plan

```text
architecture_signatures:
  module_level:
    - skills/qa / qa(ticket, runtime_target?, proof_policy_override?) -> report + result + writeback + handoffs + learning
    - agents/qa-tester.toml / operate_qa(context_ref, effective_proof_policy, runtime_target?) -> captured_artifacts + receipt
    - qa/cookbook / qa_shortcut(entry, environment, prerequisites) -> deterministic_state + verification + cleanup
  main_flow:
    - finish_qa(run) -> canonical_result_json + ticket_links + optional_progress_entry + judgment_receipts + learning_decision
    - validate_qa_result(payload) -> errors[]
  data_flow:
    - Done + QA Strategy + optional Agent Contract + explicit override -> effective_proof_policy
    - captured artifacts + judgments -> result.json -> Links + conditional progress.md
    - findings -> ticket_only | cookbook_update | instrumentation_ticket
  builder_freeform_boundary:
    - Wording/helper structure is builder-owned; ticket fields, verdicts, receipt fields, artifact paths, role boundaries, and proof gates are fixed below.
```

### Change 1: Guide and cookbook

```text
fixes:
  - browser-first orientation, incorrect artifact path, weak shortcut contract, missing learning decision, and stale cookbook lifecycle metadata
read:
  - qa/README.md
  - qa/AGENTS.md
  - qa/cookbook/*
write:
  - qa/README.md
  - qa/AGENTS.md
  - qa/cookbook/README.md
  - qa/cookbook/TEMPLATE.md
  - qa/cookbook/core-hooks-runtime.md
operation:
  - document choose -> capture -> reconcile -> judge -> receipt -> learn
  - require shortcut trigger, environment guard, prerequisites, expected state, cleanup, verification, source ticket, and last verified receipt
  - classify learning without forcing a shared-doc edit after every run
qa:
  - doc refs, path scan, and cookbook contract inspection
```

### Change 2: Canonical skill and focused actor

```text
fixes:
  - retired ticket sections, undefined proof policy, wrong Evidence/State writeback, unconditional screenshots, runtime guessing, duplicated recipes, and adversarial boundary blur
read:
  - skills/qa/SKILL.md
  - skills/qa/qa_checklist.md
  - agents/qa-tester.toml
  - tickets/README.md
write:
  - skills/qa/SKILL.md
  - skills/qa/qa_checklist.md
  - agents/qa-tester.toml
operation:
  - preserve the single-owner five-gate journey
  - load qa as the canonical contract; keep tester role, context, retry/no-progress limits, operation, capture, and writeback
  - always link the receipt from ticket Links
  - append progress.md only when it already exists, the run is Goal-backed, or blocker/review state needs an append-only entry; never create it for every QA run
qa:
  - current-ticket, CLI, UI, runtime-gap, retry, routing, and learning behavior cases
```

### Change 3: Mechanically checkable receipt and behavior proof

```text
fixes:
  - result examples omit required fields and prose evals can drift without structural or real-harness proof
read:
  - skills/qa/evals/evals.json
  - skills/eval runner and nearby skill-local test patterns
write:
  - skills/qa/scripts/validate_qa_result.py
  - skills/qa/scripts/test_validate_qa_result.py
  - skills/qa/evals/evals.json
  - skills/qa/audits/2026-07-14-canonical-qa-journey.md
operation:
  - validate the frozen schema and conditional UI/runtime/pass/learning invariants
  - run changed QA rows through the actual Codex harness and record generated artifact paths
qa:
  - focused unittest, query-spoiler scan, check_skills, real-harness --skill qa run, and independent review
```

Canonical `result.json`:

```json
{
  "schema_version": "1",
  "ticket_id": "TASK-0000",
  "phase": "qa",
  "proof_type": "cli",
  "runtime_target": null,
  "proof_policy": "Done + QA Strategy",
  "verdict": "pass",
  "summary": "QA proved the required behavior.",
  "gate_results": {
    "contract": "pass",
    "mechanism": "pass",
    "journey": "pass",
    "adversarial": "pass",
    "receipt": "pass"
  },
  "best_evidence": "tickets/TASK-0000/artifacts/qa/run/logs/checks.txt",
  "artifacts": [
    "tickets/TASK-0000/artifacts/qa/run/report.md",
    "tickets/TASK-0000/artifacts/qa/run/logs/checks.txt"
  ],
  "blockers": [],
  "residual_risk": [],
  "judgment_receipts": [],
  "learning": {"outcome": "ticket_only", "ref": null}
}
```

Receipt invariants:

- Version `1`, phase `qa`; proof type is `cli`, `api`, `browser`, `ui`,
  `artifact`, or `agent`; verdict is `pass`, `revise`, `fail`, `blocked`, or
  `not_provable`.
- All five gate keys exist with `pass`, `fail`, or `blocked`.
- Artifacts are non-empty. Every pass has concrete `best_evidence` and that
  path appears in artifacts; an honest non-pass may use null when the blocker
  names the missing artifact.
- A pass has every gate passing and no blockers. A non-pass has at least one
  blocker and names missing evidence there.
- UI/browser passes require a runtime target and image best evidence. API proof
  requires a runtime target. CLI/artifact proof may use a log or generated file.
- Learning is `ticket_only`, `cookbook_update`, or `instrumentation_ticket`.
  The latter two require a ref; ticket-only uses null.
- Judgment receipt paths appear when the proof policy requires `visual-qa`,
  `agent-qa-test`, or reviewer judgment; the structural validator does not
  invent or assess those judgments.

```text
visual_companion:
  path: tickets/TASK-0356/diagrams.md
  generated_by: inline diagramming fallback
  blocks_approval: false
  canonical_contract: ticket.md
```

## Done

```text
done_when:
  - qa-tester reads the current ticket schema and canonical qa contract
  - UI/non-UI evidence, runtime, pass/non-pass, judgment, and learning invariants are synchronized and validated
  - proof always updates Links and conditionally updates progress.md
  - shortcuts and cookbook learning are deterministic and lifecycle-aware
  - existing single-owner QA changes remain intact
  - focused tests, real-harness QA evals, skill/docs/ticket validators, and independent review pass
```

## QA Strategy

```text
qa_strategy:
  proof_weight: tests + agent_qa + review
  checks:
    - python3 -m unittest skills/qa/scripts/test_validate_qa_result.py skills/qa/scripts/test_validate_eval_run.py
    - python3 -m json.tool skills/qa/evals/evals.json
    - python3 skills/eval/scripts/check_eval_queries.py --root .
    - python3 skills/skill-maintenance/scripts/check_skills.py --write
    - farplane validate ticket tickets/TASK-0356/ticket.md --phase planning
    - python3 bin/validators/check_doc_refs.py
    - farplane run -- python3 skills/eval/scripts/run_evals.py run --harness codex --skill qa --label task-0356-qa-final-reviewed
    - python3 skills/qa/scripts/validate_eval_run.py .farplane/evals/runs/20260713-203845-task-0356-qa-final-reviewed
  manual:
    - cross-surface scan for retired ticket fields, wrong artifact paths, unconditional UI evidence, and duplicated ownership
  delegated_lanes:
    - reviewer for plan and completion
    - real Codex eval harness for changed QA behavior rows
  review:
    - rubric: implementation-plan
      required_tas: TAS-A
    - rubric: skill-contract
      required_tas: TAS-A
    - rubric: integration-readiness
      required_tas: TAS-A
    - rubric: evidence-quality
      required_tas: TAS-A
    - rubric: eval-quality
      required_tas: TAS-A
  evidence:
    - tickets/TASK-0356/artifacts/qa/test-output.txt
    - tickets/TASK-0356/artifacts/qa/eval-summary.md
    - tickets/TASK-0356/artifacts/review/plan-review.md
    - tickets/TASK-0356/artifacts/review/completion-review.md
    - skills/qa/audits/2026-07-14-canonical-qa-journey.md
  goal_advisor_inputs:
    proof_route: approved direct implementation, focused tests, real-harness eval, then reviewer gate
    final_evidence: test output + eval summary + skill audit + reviewer receipt
    final_checkpoint: all focused checks and QA eval tasks pass, then required review families reach TAS-A
  residual_risk:
    - representative prompt cases do not replace downstream application browser QA
```

Grounding evidence: local-only; this aligns Farplane-owned contracts and
chooses no third-party API or ecosystem behavior.

## Docs Strategy

```text
docs_strategy:
  outcome: update_docs
  doc_targets:
    - qa/README.md
    - qa/AGENTS.md
    - qa/cookbook/README.md
    - qa/cookbook/TEMPLATE.md
    - qa/cookbook/core-hooks-runtime.md
  validation:
    - python3 bin/validators/check_doc_refs.py
```

## Run Hints

- Likely size: large
- Goal recommendation: none; operator approved direct implementation
- Compute hint: local_shared
- Expected beats: 5+
- Parallel: reviewer lanes only
- QA source: this ticket
- Human gates: none

## Links

- program: none
- progress: none; create only if Goal/blocker/review state later requires it
- visual companion: `tickets/TASK-0356/diagrams.md`
- artifacts: `tickets/TASK-0356/artifacts/`
- review: `tickets/TASK-0356/artifacts/review/`
- QA tests: `tickets/TASK-0356/artifacts/qa/test-output.txt`
- QA eval summary: `tickets/TASK-0356/artifacts/qa/eval-summary.md`
- strongest eval evidence: `.farplane/evals/runs/20260713-203845-task-0356-qa-final-reviewed/summary.json`
- current completion review: `tickets/TASK-0356/artifacts/review/completion-review.md`
- refs:
  - `docs/features/FEAT-0008-artifact-first-qa-and-completion-proof.md`
  - `docs/features/FEAT-0007-ticket-as-durable-task-memory.md`

## Notes

- Preserve all unrelated dirty-worktree changes and the July 13 single-owner
  QA journey edits already present in `skills/qa`.
- Minimal implementation: existing owners plus one skill-local validator and
  tests; no new skill, hook, registry, or global policy.
- Final evidence: 20 focused tests, full skill-system/doc/ticket preflight,
  one 5/5 TAS-A fixture-backed Codex run, generated-receipt validation, and an
  independent completion review at TAS-A across every required family.
- Handoff: archive-ready; no commit or push was performed because the shared
  worktree contains unrelated operator changes and publishing was not requested.
- Next action: none for TASK-0356. Use the new guide and receipt contract on
  the next application ticket; downstream browser proof remains ticket-specific.
