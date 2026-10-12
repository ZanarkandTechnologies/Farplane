# Project Knowledge Note

- `MEM-PATH-001` (2026-01-10): The canonical checkout is `/old/path`.
- `MEM-SECRETS-001` (2026-08-18): Never commit secrets to git.

Current evidence:

- The current repository root reported by project setup is `/new/path`.
- `AGENTS.md` already owns the rule that tracked artifacts must not contain
  secrets.

Do not silently replace a factual row. Classify it against the available
evidence and preserve or route it through the owning lifecycle.
