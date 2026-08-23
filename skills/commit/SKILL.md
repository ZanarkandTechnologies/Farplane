---
name: commit
version: 0.2.0
description: "Turn an already staged Git boundary into one verified local commit without staging or pushing."
tier: 2
source: local
capability:
  kind: shortcut
allowed-tools: Read, Glob, Grep, Bash
---

# Commit

## Context

Use this explicit shortcut when the operator wants to create a local commit.
It owns the already-staged boundary only: inspect it, choose a compact honest
subject, create one commit, and verify the receipt. It never runs `git add`,
modifies the index, or pushes.

## Skill Signature

```text
commit(staged_diff?, subject?) -> commit_receipt | no_staged_changes

state: reads(index, staged diff, recent history); writes(one local commit only)
owns: staged-boundary validation, subject selection, local commit receipt
gates: git_repository; staged_changes; subject_nonempty; head_advanced_once;
  unstaged_work_preserved
fails: auto_staging; auto_push; mixed-boundary commit; empty commit
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Inspect the staged boundary first with `git diff --cached`.
  - If it is empty, return `no_staged_changes` and do not mutate anything.
  - Do not inspect unstaged changes as candidates for this commit.
- [ ] 2. Inspect recent commit style and choose one compact, truthful subject.
  - Default to `type(scope): lower-case imperative summary`; name the main
    behavioral delta, not every touched file.
- [ ] 3. Create exactly one local commit using
  `scripts/commit_staged.py --message <subject>`.
  - The helper must be given the repository root when it is not the current
    directory. Do not add files or push.
- [ ] 4. Verify the receipt.
  - Confirm `HEAD` advanced by one commit, the staged boundary is now clean,
    and any pre-existing unstaged work remains untouched.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

```yaml
status: committed | no_staged_changes
subject: <commit subject when committed>
commit: <HEAD SHA when committed>
boundary: staged-only
unstaged_work: preserved
```

## Gotchas

- Do not treat a requested commit as permission to stage adjacent changes.
- Do not commit when the staged diff combines unrelated deltas; ask the
  operator to curate the boundary first.
- Do not push, amend, rebase, or rewrite history.

## References

- [references/style.md](references/style.md)
