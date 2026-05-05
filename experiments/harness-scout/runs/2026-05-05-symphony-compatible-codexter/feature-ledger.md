# Feature Ledger: Symphony-Compatible Codexter

Date: 2026-05-05

## Candidate Features

| Candidate | Symphony source idea | Local Codexter baseline | Local match |
| --- | --- | --- | --- |
| `WORKFLOW.md` control tower | Repo-owned workflow prompt/config with front matter | Many strong skills/specs, but no single board-run front door | Partial |
| `WorkItem` normalized model | Normalized `Issue` entity | Filesystem ticket frontmatter/body, no adapter-independent model | Partial |
| `BoardAdapter` contract | Linear tracker client operations | Filesystem selector in `skills/ralph/scripts/select_next_ticket.py` | Partial |
| Codexter invocation envelope | App-server launches one issue prompt in workspace | `$impl` and skills exist, but no stable external `CodexterRunEnvelope` contract | Missing |
| Workspace/compute target policy | Per-issue workspace root and hooks | `pr-runtime`/ticket runtime partial; local invocation not abstracted | Partial |
| Run events | Agent update events and session metadata | Stop hook and ticket evidence exist, but no normalized runner event vocabulary | Partial |
| Claim/lease registry | `claimed`, `running`, retry entries | `claimed_by` human alias and runtime claim state | Partial |
| Proof packet | Not first-class in Symphony, but needed for Codexter integration | Ticket evidence and review receipts exist; no portable result schema | Partial |
| Conformance test matrix | Symphony test sections 17/18 | Ticket metadata, doc parity, harness invariant tests | Partial |

## Dedupe Notes

- `Serial Ralph board draining` already exists as `FEAT-0009`, but it is
  filesystem-specific and serial.
- `Artifact-first QA and completion proof` already exists as `FEAT-0008`.
- `Stop-hook continuation and completion judgment` already exists as
  `FEAT-0010`.
- The missing layer is not another skill. It is an invocation and adapter
  contract so Symphony, Linear, or future runners can run Codexter reliably.
