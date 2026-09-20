# Farplane hooks

Each active hook has one folder containing its Python entrypoint and usage guide.
[Root `hooks.json`](../hooks.json) is the only registration source; folder READMEs
explain behavior without maintaining duplicate registration snippets.

| Folder | Codex event | Responsibility |
| --- | --- | --- |
| [continuation](continuation/README.md) | Stop | Bounded Jev continuation advice |
| [response-length](response-length/README.md) | Stop | Deterministic final-answer prose limits |
| [lifecycle-telemetry](lifecycle-telemetry/README.md) | UserPromptSubmit, Stop, SubagentStart, SubagentStop | Classified lifecycle observations |
| [skill-length](skill-length/README.md) | PostToolUse | Repair feedback for oversized edited skills |
| [user-turn](user-turn/README.md) | UserPromptSubmit | User-intent capture and optional skill suggestion |

## Install and inspect

From the primary Farplane checkout:

```sh
farplane hooks install
farplane hooks list
farplane hooks doctor
```

Installation links each complete folder under `~/.codex/hooks/` and preserves
unrelated hooks. Temporary installed-only migration links keep old flat command
paths working for active Codex sessions with cached registrations. Source files
live only in the new folders; root `hooks.json` uses their new paths. Remove the
migration links only after old sessions have retired or reloaded. Review/trust changed
command paths in Codex `/hooks`; installation does not grant trust. The three Stop
handlers remain independently controlled. Shared Core/runtime code stays under
`bin/core/` and `bin/runtime/` rather than being copied into hook folders.

`shared_checkout_guard.py` is a retired no-op bridge for cached Codex commands,
not an active hook or a sixth package. It has no current registration.

See the [runtime guide](../docs/farplane-framework/hooks-and-runtime.md) for
cross-hook contracts, configuration precedence, and telemetry state boundaries.
