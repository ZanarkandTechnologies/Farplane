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
| `approve.py request "<what>" --usd 2` or less | Opens at once for up to 60 minutes and sends Kenji one line (Kenji, 13 Nov 2026: "its fine if its below 2 usd"). A day's small requests stop at $10; after that they need a code. |
| `approve.py request "<what>" --usd 5 --minutes 60` | Sends a 6-digit code to Kenji's phone only. `approve.py grant <code>` opens the window. Three wrong codes or 30 minutes cancel it. |

Why small requests skip the code: 16 of the first 24 requests were $2 or
less, and 14 of the 24 never got an answer, so threads sat idle for cents.

The hook stays silent for read-only Modal commands (`modal app list`, `modal
volume ls`) and for commands that only read or name `deploy/release.sh`
(`cat`, `grep`). Every request and grant is appended to
`~/.farplane/approvals/log.md`.

## Test

```bash
.venv/bin/python -m unittest bin.tests.test_spend_approval_hook
```
