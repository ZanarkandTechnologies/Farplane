---
name: codexter-invocation
description: Interpret a CodexterRunEnvelope inside normal Codex, validate repo policy and one filesystem ticket, select local compute, route to existing Codexter skills, and write a ProofPacket.
---

# Codexter Invocation

Use this when Codex receives a `CodexterRunEnvelope` from the operator, a local
file, or a future external caller such as Symphony.

Codexter is not a separate CLI. Codexter is normal Codex after this repository's
skills, templates, hooks, and rules have been installed.

A ticket existing in `tickets/`, a ticket becoming `ready: true`, or a board
card moving state is context only. It is not a run trigger. Start this skill
only after an explicit invocation, such as a local operator asking Codex to run
one ticket, an operator-invoked `$ralph` pass, a recognized ticket comment that
an external runner has converted into an envelope, or a Symphony/Codex Cloud
payload.

## Trigger Vocabulary

Use these trigger kinds when explaining or templating a run:

| Kind | Example | Envelope mode |
| --- | --- | --- |
| `local_chat` | `run TASK-0123 locally` | `local_codex` |
| `local_ralph` | operator invokes `$ralph` | `local_ralph` |
| `ticket_comment` | `@codexter implement` after a caller recognizes it | `external_runner` |
| `codex_cloud_task` | Codex Cloud task prompt includes the envelope | `external_runner` |
| `symphony_worker` | Symphony writes the envelope in a worker workspace | `symphony_worker` |

Never infer a trigger from ticket creation, `ready`, status movement, or
`compute_target`. For shared boards, a comment/action is only a convention until
an external caller converts it into a `CodexterRunEnvelope`.

## Workflow

1. Read `WORKFLOW.md`.
2. Read or construct one `CodexterRunEnvelope`.
3. Load the selected board item through the configured BoardAdapter. V1 only
   supports `board.adapter: filesystem`, implemented by
   `bin/codexter_boards.py`, and normalizes one ticket into `WorkItem`.
4. Run the diagnostic helper to prepare the invocation:

   ```bash
   python3 bin/codexter_invocation.py prepare --envelope <json-or-file>
   ```

   For conversational local use, pass `--ticket`, `--phase`, `--compute`, and
   `--proof` instead of `--envelope`.
5. Inspect the returned JSON:
   - `status: ready` means follow `route.skill_name`.
   - `status: blocked` means stop and report `compute.blockers` or missing
     route information.
   - `compute.requiredSetup` is an operator/agent setup hint, not permission for
     this helper to launch worktrees, Symphony, or cloud tasks.
6. Invoke the existing phase skill named by `route.skill_name`.
7. Keep the ticket evidence updated.
8. Write or validate a `ProofPacket` at the requested `proofPacketPath`.

## Boundaries

- `planning` routes to `impl-plan`.
- `building` routes to `impl`.
- `qa` routes to `qa`.
- `review` routes to `review`.
- `documenting` routes to `close-ticket`.

The helper validates and writes artifacts. It does not launch Codex, poll a
board, claim tickets, retry failed work, or manage remote workspaces. Symphony or
another external runner may own those orchestration concerns later.

Readiness gates and `compute_target` are admission inputs, not execution
authority. If no explicit invocation exists, do not infer one from ticket
metadata.

`FileTicketAdapter` is read-first in v1. It rejects ticket paths outside the
configured board source and returns a manual writeback result for evidence
instead of silently mutating ticket files.

`codexter_compute.py` is also read-first/admission-only. It can select
`local_shared`, defer `local_worktree` until `.harness/state/tickets/*.runtime.json`
exists, and block `symphony` or `codex_cloud` until external adapters exist.

For Symphony-shaped requests, read
`skills/codexter-invocation/references/symphony.md` and use
`skills/codexter-invocation/templates/symphony-run-envelope.json` as the
request-file fixture. The fixture intentionally uses `mode: "symphony_worker"`
with `computeTarget: "local_shared"` because Symphony has already chosen the
workspace; `computeTarget: "symphony"` remains a future adapter target and
blocks in local Codexter.

For Codex Cloud-shaped requests, read
`skills/codexter-invocation/references/codex-cloud.md` and use
`skills/codexter-invocation/templates/codex-cloud-task-prompt.md` as the prompt
template. The template is for manual or future-adapter submission through
`codex cloud exec`; this skill must not submit the task, poll it, apply its
diff, or hide review from the local ticket evidence.

For future board adapters, read
`docs/specs/board-adapter-conformance.md` before adding adapter code. The
filesystem adapter is the only live adapter today.

## Local Example

```bash
python3 bin/codexter_invocation.py prepare \
  --ticket TASK-0107 \
  --phase planning \
  --proof .harness/results/task-0107-plan.proof.json
```

If the result routes to `impl-plan`, use the `impl-plan` skill against the
selected ticket and keep the ticket in `review` until approval exists.

## Proof Example

```bash
python3 bin/codexter_invocation.py write-proof \
  --ticket TASK-0107 \
  --phase planning \
  --proof .harness/results/task-0107-plan.proof.json \
  --verdict pass \
  --next-action "ready for build"
```

Link proof artifacts from the ticket `Evidence` section. Keep detailed result
state in JSON, not in transcript memory.

## AI Misread Checks

Before acting on an envelope, verify:

- there is exactly one selected work item;
- the trigger was explicit and did not come from board state alone;
- unsupported external targets are reported as blockers, not silently run
  locally;
- comments are caller-side conventions unless an adapter has already produced
  an envelope;
- this helper is validating and writing artifacts only, not launching Codex or
  cloud tasks.
