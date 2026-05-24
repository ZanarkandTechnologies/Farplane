# Safety and Rollback

Efficiency is useful only if outcomes are controlled and reversible.

## Preflight Checklist

- Confirm target path(s) exist.
- Confirm command scope is correct (file glob, regex, directory).
- Preview impacted files before mutation.
- Prefer dry-run flags when available.

## Mutation Rules

1. **Preview first** for delete/replace/move across many files.
2. **Narrow scope** to explicit paths/globs.
3. **Run once, verify once**, then continue.

## Verification Checklist

- Expected files changed?
- Unexpected files changed?
- Command exit code is success?
- Output content matches requested transformation?

## Rollback Guidance

For non-trivial operations, include one of:

- **Git rollback**: restore from clean commit if repo state allows.
- **Path rollback**: inverse `mv` commands for renames/moves.
- **Backup rollback**: restore from `.bak` or copied snapshot.

Example rollback block:

```text
Rollback:
1) mv new-name.txt old-name.txt
2) mv archive/*.log ./
3) Verify with ls -la and rg 'oldName' -n
```

## Stop-and-Ask Conditions

Stop and ask before proceeding if:

- Scope is ambiguous ("all configs", "everything in src")
- Command is destructive and preview does not match expectation
- Environment mismatch makes command semantics unclear
