# Specs

Canonical harness and product specs live here once ideas move past exploration.

Top-level companion docs:

- [`ARCHITECTURE.md`](/Users/kenjipcx/coding-harness/Codexter/ARCHITECTURE.md) - top-level system map and canonical surface guide
- [`README.md`](/Users/kenjipcx/coding-harness/Codexter/README.md) - product/setup story and public entrypoints

Current design docs:

- `doc-governance.md` - structural versus narrative doc-audit policy
- `context-and-handoff-policy.md`
- `harness-engineering-quickstart.md`
- `harness-techniques.md` - current-state feature and technique inventory
- `orchestrator-subagent-loop.md`
- `ralph-runtime-surface.md`
- `ralph-orchestration-blueprint.md`
- `review-gates.md`
- `spec-first-execution-loop.md`
- `ralph-v2-direction.md`
- `ralph-flow-examples.md` - start here for visual dry runs
- `ralph-run-state.schema.json`
- `ralph-judge-verdict.schema.json`

Use this folder for:

- execution model specs
- artifact and schema specs
- orchestration flow docs
- `skill` / `subagent` / `hook` stories tied to buildable system behavior

Keep exploratory source comparison notes and one-off research in `docs/research/`.

## Doc Gardening Loop

Run this loop when the public harness story changes:

1. Run `python3 tickets/scripts/check_ticket_metadata.py`.
2. Run `python3 bin/check_doc_parity.py`.
3. Re-read `ARCHITECTURE.md`, `README.md`, `docs/specs/README.md`, `docs/specs/harness-techniques.md`, and `tickets/README.md` against the active ticket plus `docs/MEMORY.md` / `docs/HISTORY.md`.
4. Use the `codex exec` narrative audit in `doc-governance.md` when the public story, implemented/proposed status, or canonical links changed.
5. Patch only the canonical surfaces that drifted; do not spread the same claim across more docs unless the new surface is truly canonical.
6. Re-run `python3 tickets/scripts/check_ticket_metadata.py` and `python3 bin/check_doc_parity.py`.
