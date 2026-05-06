# V2 Batch Evidence

Date: 2026-05-06T19:10:35Z
Tickets: `TASK-0121`, `TASK-0123`, `TASK-0122`

## Implemented Surface

- Added explicit invocation trigger vocabulary across the invocation specs and
  `codexter-invocation` skill docs.
- Added `docs/specs/board-adapter-conformance.md` and filesystem adapter
  conformance coverage.
- Added Codex Cloud handoff recipe and prompt template.
- Strengthened Symphony handoff docs with a diff/evidence/review/`ProofPacket`
  return contract.
- Added envelope `mode` validation so future agents cannot invent values such
  as `polling_daemon`.

## Commands

```bash
python3 -m unittest bin/test_codexter_invocation.py
python3 -m unittest bin/test_codexter_boards.py
python3 -m unittest bin/test_codexter_compute.py
python3 -m unittest bin/test_codexter_invocation.py bin/test_codexter_boards.py bin/test_codexter_compute.py
python3 -m py_compile bin/codexter_invocation.py bin/codexter_boards.py bin/codexter_compute.py
python3 tickets/scripts/check_ticket_metadata.py
python3 bin/check_doc_parity.py
python3 bin/check_harness_invariants.py
python3 bin/codexter_invocation.py prepare --ticket TASK-0085 --phase building --proof .harness/results/task-0085.proof.json
codex cloud --help
codex cloud exec --help
codex cloud status --help
codex cloud diff --help
codex cloud apply --help
rg -n "auto.*run|watch|webhook|poll|daemon|listener|cloud exec|cloud apply" docs skills/codexter-invocation WORKFLOW.md
```

## Results

- `bin/test_codexter_invocation.py`: 10 tests passed.
- `bin/test_codexter_boards.py`: 8 tests passed.
- `bin/test_codexter_compute.py`: 7 tests passed.
- Combined focused unittest run: 25 tests passed.
- `py_compile`: passed.
- Ticket metadata: OK, 10 ticket files checked.
- Structural doc parity: OK, 6 files checked, 29 rules.
- Harness invariants: OK, 5 files checked, 15 agents, 13 rules.
- `codexter_invocation.py prepare` for `TASK-0085` returned `status: ready`.
- `codex cloud --help` was available locally and listed `exec`, `status`,
  `list`, `diff`, and `apply`.
- The grep scan found daemon/poll/cloud terms in guardrail, reference, research,
  or explicit manual-recipe contexts; no new Codexter-owned watcher, daemon,
  cloud wrapper, or external adapter code was added.

## AI Misunderstanding Risks Checked

- `ready: true` and status movement are still described as context, not run
  triggers.
- Ticket comments are described as caller-side conventions until an external
  runner converts them into an envelope.
- `codexter_invocation.py` remains diagnostic and artifact-oriented; it does
  not launch Codex, cloud tasks, or board polling.
- `codex_cloud` and `symphony` remain unsupported local compute targets.
- Codex Cloud docs require `diff` and review before `apply`.
- Future board adapters must satisfy conformance before becoming live sources.
