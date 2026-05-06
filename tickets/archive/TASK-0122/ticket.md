---
ticket_id: TASK-0122
title: add external compute handoff recipes
phase: complete
status: done
owner: codex
claimed_by:
priority: medium
depends_on:
  - TASK-0121
blocked_by: []
ready: false
approval_required: false
requires_qa: false
requires_demo: false
created_at: 2026-05-06T17:18:41Z
updated_at: 2026-05-06T19:14:47Z
next_action: none; archived after V2 batch completion
last_verification: focused tests, validators, Codex Cloud help check, grep guardrail scan, and review passed on 2026-05-06
---

# TASK-0122: add external compute handoff recipes

## Summary
Create practical handoff recipes for sending one Codexter ticket to external
compute such as Codex Cloud or Symphony without making Codexter a compute
orchestrator. The recipes should tell an operator or future adapter how to pass
ticket context, invoke normal Codex with Codexter installed, and bring back a
diff plus ProofPacket for review.

## Batch Plan
This ticket is planned as the final recipe step in the capped V2 batch after
`TASK-0121` locks trigger vocabulary and `TASK-0123` locks adapter
conformance. The shared plan lives at
[2026-05-06-v2-batch-impl-plan.md](/Users/kenjipcx/coding-harness/Codexter/tickets/archive/TASK-0121/artifacts/plan/2026-05-06-v2-batch-impl-plan.md)
and the plan review passed at
[2026-05-06-v2-batch-plan-review.json](/Users/kenjipcx/coding-harness/Codexter/tickets/archive/TASK-0121/artifacts/review/2026-05-06-v2-batch-plan-review.json).

## V2 Importance
- `Why now:` this gives a practical answer for "run this ticket on the cloud"
  without building a cloud orchestrator. Codexter should package context and
  proof expectations; Codex Cloud or Symphony should own execution.
- `Why not later:` external compute is the most tempting place to overbuild.
  A recipe-first boundary now lets the operator use existing tools manually and
  keeps future automation from inventing new prompts.
- `Stop line:` document recipes and templates only. Do not submit cloud tasks,
  wrap `codex cloud`, launch Symphony, poll runs, auto-apply diffs, or merge
  remote output.

## Scope
- In:
  - Add a Codex Cloud handoff reference using `codex cloud exec`, `status`,
    `diff`, and `apply`.
  - Add or refine Symphony handoff reference language so Symphony launches
    normal Codex with a `CodexterRunEnvelope`.
  - Define the expected result contract: diff or changed files, linked ticket
    evidence, review output, and ProofPacket.
  - Provide copy-pasteable prompt/envelope templates for one ticket.
  - Keep `compute_target: codex_cloud` and `compute_target: symphony` blocked
    in local selector until a real adapter exists.
- Out:
  - No API wrapper for Codex Cloud.
  - No automatic cloud task creation from Ralph.
  - No Symphony daemon, Linear polling, or app-server client.
  - No automatic apply/merge.

## Plan
- `Change:` Add operator-facing and future-adapter-facing recipes for external
  compute handoff.
- `Why:` The CLI already exposes Codex Cloud tasks, and Symphony already owns
  background scheduling. Codexter should package context and proof expectations
  rather than duplicate those platforms.
- `Before -> After:`
  - Before: external compute targets exist as blocked enum values, but the
    operator does not have a clear recipe for using them safely.
  - After: an operator can intentionally send one ticket to Codex Cloud or a
    Symphony worker and know how to review/apply the result.
- `Touch:`
  - `skills/codexter-invocation/references/codex-cloud.md`
  - `skills/codexter-invocation/references/symphony.md`
  - `skills/codexter-invocation/templates/codex-cloud-task-prompt.md`
  - `skills/codexter-invocation/templates/symphony-run-envelope.json`
  - `skills/codexter-invocation/README.md`
  - `docs/specs/symphony-compatible-codexter-runner.md`
  - `docs/specs/board-compute-orchestration.md`
- `Inspect:`
  - `codex cloud --help`
  - `bin/codexter_invocation.py`
  - `bin/codexter_compute.py`
  - `skills/ralph/scripts/select_next_ticket.py`
  - `WORKFLOW.md`
- `Signature delta:`
  - `templates/codex-cloud-task-prompt.md / prompt(ticket, envelope): text`
  - `references/codex-cloud.md / Handoff Flow`
  - no new Python launcher seam unless tests need fixture validation.
- `Type Sketch:`
  - `ExternalComputeHandoff`:
    - `target`: `codex_cloud | symphony`
    - `input`: ticket id/path plus optional envelope file
    - `execution`: external platform command or worker launch
    - `return`: diff, evidence links, ProofPacket, review artifact
  - `ProofPacketExpectation`:
    - `verdict`, `commands`, `artifacts`, `nextAction`, `completedAt`
- `Typed flow example:`
  1. Operator decides `TASK-0124` can run in Codex Cloud.
  2. Operator prepares prompt from `codex-cloud-task-prompt.md`.
  3. `codex cloud exec` creates an external task.
  4. Operator checks `codex cloud status` and `codex cloud diff`.
  5. Operator applies locally only after inspecting the diff.
  6. Local Codexter review validates the ProofPacket and ticket evidence.
- `Execution steps:`
  1. Add Codex Cloud reference and template.
  2. Update Symphony reference to mirror the same input/output language.
  3. Document that `compute_target` remains an admission marker, not an
     automatic launcher.
  4. Add a fixture or markdown validation check if the repo has a suitable
     lightweight validator.
  5. Run doc parity, metadata, and relevant helper tests.
- `Recommendation:` Add recipes before adapters. This gives immediate operator
  value while preserving the boundary.
- `Options considered:`
  - Build a Codex Cloud wrapper now: more automation, but duplicates the CLI
    and introduces external side effects.
  - Add recipes/templates only: recommended; useful, safe, and easy to review.
  - Wait until Symphony/Cloud integration is urgent: lower effort now, but the
    future adapter contract stays fuzzy.
- `Blast radius:` invocation docs, future compute-target tickets, operator
  workflows for external work.
- `Risks:`
  - Recipes may go stale as `codex cloud` evolves. Containment: keep commands
    minimal and validate help text during implementation.
  - Operators may apply remote diffs too eagerly. Containment: recipe must put
    diff/review before apply/merge.

## Gap Analysis
- `Current state:` `codex_cloud` and `symphony` targets exist but block
  locally with setup hints rather than recipes.
- `Production expectation:` External compute handoff should define input,
  execution, output, review, and apply boundaries.
- `Missing gaps:` no Codex Cloud template, no apply/review flow, no shared
  return-proof expectations for external compute.
- `Comparable implementations:` Codex Cloud CLI, Symphony spec, Codexter
  ProofPacket helper.
- `Recommendation:` ship recipes now; defer adapters and automation.

## Acceptance Criteria
- [x] Codex Cloud handoff reference exists and uses current `codex cloud`
  command vocabulary.
- [x] Symphony reference and Codex Cloud reference share the same
  envelope/proof framing.
- [x] Recipes state that external compute is explicit and never triggered by
  ticket creation alone.
- [x] Local selectors still block unsupported external targets until real
  adapters exist.

## Verification
- `Tests:`
  - `python3 -m unittest bin/test_codexter_compute.py bin/test_codexter_invocation.py`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `python3 bin/check_doc_parity.py`
- `Manual checks:`
  - `codex cloud --help`
  - `python3 bin/codexter_invocation.py prepare --ticket TASK-0085 --phase building --proof .harness/results/task-0085.proof.json`
- `Evidence required:`
  - Review artifact verifying no wrapper or external side effect was added.

## Autonomy Readiness
- `Human inputs/assets:` approval of recipe-first external compute boundary.
- `Credentials / external access:` Codex Cloud may require user auth for real
  use; implementation should not submit tasks during tests.
- `Compute/runtime needs:` local docs/tests only.
- `Tooling gaps:` no external adapters yet.
- `QA risks:` docs could imply automation; review must check wording.
- `Human gates:` approval required before changing external-compute docs.
- `Agent decision boundaries:` may document and template handoffs; may not run
  paid/cloud tasks or apply remote diffs.

## Refs
- [Codexter invocation skill](/Users/kenjipcx/coding-harness/Codexter/skills/codexter-invocation/SKILL.md)
- [Compute selector](/Users/kenjipcx/coding-harness/Codexter/bin/codexter_compute.py)
- [Symphony-compatible runner spec](/Users/kenjipcx/coding-harness/Codexter/docs/specs/symphony-compatible-codexter-runner.md)
- [Codexter V2 milestone](/Users/kenjipcx/coding-harness/Codexter/docs/specs/codexter-v2-milestone.md)

## Evidence
- `Artifacts:`
  - [V2 batch impl-plan](/Users/kenjipcx/coding-harness/Codexter/tickets/archive/TASK-0121/artifacts/plan/2026-05-06-v2-batch-impl-plan.md)
  - [V2 batch plan review](/Users/kenjipcx/coding-harness/Codexter/tickets/archive/TASK-0121/artifacts/review/2026-05-06-v2-batch-plan-review.json)
  - [V2 batch evidence](/Users/kenjipcx/coding-harness/Codexter/tickets/archive/TASK-0121/artifacts/qa/2026-05-06-v2-batch-evidence.md)
  - [V2 batch implementation review](/Users/kenjipcx/coding-harness/Codexter/tickets/archive/TASK-0121/artifacts/review/2026-05-06-v2-batch-impl-review.json)
  - [next-batch plan review](/Users/kenjipcx/coding-harness/Codexter/tickets/archive/TASK-0120/artifacts/review/2026-05-06-next-batch-plan-review.json)
- `Commands:`
  - `python3 -m unittest bin/test_codexter_invocation.py bin/test_codexter_boards.py bin/test_codexter_compute.py`
  - `python3 -m py_compile bin/codexter_invocation.py bin/codexter_boards.py bin/codexter_compute.py`
  - `python3 -m json.tool tickets/archive/TASK-0121/artifacts/review/2026-05-06-v2-batch-plan-review.json`
  - `python3 -m json.tool tickets/archive/TASK-0121/artifacts/review/2026-05-06-v2-batch-impl-review.json`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `python3 bin/check_doc_parity.py`
  - `python3 bin/check_harness_invariants.py`
  - `codex cloud --help`
  - `codex cloud exec --help`
  - `codex cloud status --help`
  - `codex cloud diff --help`
  - `codex cloud apply --help`
  - `rg -n "auto.*run|watch|webhook|poll|daemon|listener|cloud exec|cloud apply" docs skills/codexter-invocation WORKFLOW.md`
  - `python3 skills/ralph/scripts/select_next_ticket.py --root . --json`
- `Result summary:`
  - External compute handoff recipes landed without adding cloud wrappers or auto-apply behavior.

## Blockers
- none
