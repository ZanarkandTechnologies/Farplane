# Spend approval

- **Event:** `PreToolUse`, matched to `Bash`.
- **Entrypoint:** `spend_approval.sh` (five-second timeout; plain `sh`, so a
  Bash call without `modal` or `release.sh` spawns nothing).
- **Purpose:** A Modal run, deploy, serve or shell, or a run of
  `deploy/release.sh`, needs Kenji's approval first. In the week of 10 Nov
  2026, $171 of unapproved Modal research and $69 of failed image builds were
  spent.

## Behavior

The hook denies the call unless `~/.farplane/approvals/grant` holds an open
window. `approve.py` opens one:

| Request | What happens |
| --- | --- |
| `approve.py request "<what>" --usd 1` or less | Opens at once for up to 60 minutes and sends Kenji one line (Kenji, 14 Nov 2026: "lets make the rule $1 or less"). A day's small requests stop at $10; after that they need a code. |
| `approve.py request "<what>" --usd 5 --minutes 60` | Sends a 6-digit code to Kenji's phone only. `approve.py grant <code>` opens the window. Three wrong codes or 30 minutes cancel it. |

Why small requests skip the code: 15 of the first 27 requests were $1 or
less, and 15 of the 27 never got an answer, so threads sat idle for cents.
Both messages tell the thread to ask for the leanest run that answers the
question, never a large budget.

The hook stays silent for read-only Modal commands (`modal app list`, `modal
volume ls`) and for commands that only read or name `deploy/release.sh`
(`cat`, `grep`). Every request and grant is appended to
`~/.farplane/approvals/log.md`.

## Test

```bash
.venv/bin/python -m unittest bin.tests.test_spend_approval_hook
```
