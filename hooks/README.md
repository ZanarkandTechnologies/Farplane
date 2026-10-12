# Farplane hooks

Each active hook has one folder containing its Python entrypoint and usage guide.
[`hooks/hooks.json`](hooks.json) is the only registration source; folder READMEs
explain behavior without maintaining duplicate registration snippets.

| Folder | Codex event | Responsibility |
| --- | --- | --- |
| [stop-gate](stop-gate/README.md) | Stop | The one blocking Stop gate: length, then continuation, then response format |
| [continuation](continuation/README.md) | Stop (via stop-gate) | Bounded Jev continuation advice |
| [response-length](response-length/README.md) | Stop (via stop-gate) | Deterministic final-answer prose limits |
| [lifecycle-telemetry](lifecycle-telemetry/README.md) | UserPromptSubmit, Stop, SubagentStart, SubagentStop | Classified lifecycle observations |
| [skill-length](skill-length/README.md) | PostToolUse | Repair feedback for oversized edited skills |
| [skill-invocation](skill-invocation/README.md) | PostToolUse | Records real skill invocations for skill heat |
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
live only in the new folders; `hooks/hooks.json` uses their new paths. Remove the
migration links only after old sessions have retired or reloaded. Review/trust changed
command paths in Codex `/hooks`; installation does not grant trust. One Stop gate
blocks; `FARPLANE_STOP_CHECKS` selects its checks. The continuation and
response-length entrypoints stay installed for sessions with cached commands. Hook code lives in its hook's folder;
code two hooks share lives once in [`shared/`](shared/README.md), and code the CLI
also uses lives in `bin/core/`.

See the [runtime guide](../docs/farplane-framework/hooks-and-runtime.md) for
cross-hook contracts, configuration precedence, and telemetry state boundaries.
