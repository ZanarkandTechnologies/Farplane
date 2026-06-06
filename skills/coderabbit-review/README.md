# CodeRabbit Review

## Purpose

Run heavyweight external CodeRabbit CLI review at the right moment: usually
before push or on a PR-sized branch, not as a default Stop-hook behavior.

## Public API / Entrypoints

- [`SKILL.md`](/Users/kenjipcx/coding-harness/Farplane/skills/coderabbit-review/SKILL.md):
  main workflow contract
- `SKILL.md` Todo List:
  compact anti-forgetting checklist
- [`references/stage-matrix.md`](/Users/kenjipcx/coding-harness/Farplane/skills/coderabbit-review/references/stage-matrix.md):
  stage defaults and when to use each path
- [`references/hook-recipes.md`](/Users/kenjipcx/coding-harness/Farplane/skills/coderabbit-review/references/hook-recipes.md):
  opt-in git hook recipes
- [`scripts/run_review.py`](/Users/kenjipcx/coding-harness/Farplane/skills/coderabbit-review/scripts/run_review.py):
  repo-local helper for `pre-commit`, `pre-push`, and `pr`

## Minimal Example

1. Finish a focused branch or risky local slice.
2. Run `python3 skills/coderabbit-review/scripts/run_review.py --stage pre-push`.
3. Read the findings and fix must-fix issues.
4. Rerun if needed.
5. Push only after the heavy review pass is acceptable for the branch.

## How to Test

- `python3 skills/coderabbit-review/scripts/run_review.py --stage pre-commit --dry-run`
- `python3 skills/coderabbit-review/scripts/run_review.py --stage pre-push --dry-run`
- `python3 -m py_compile skills/coderabbit-review/scripts/run_review.py`
- Manually confirm `SKILL.md` says this workflow is explicit and not part of the
  Stop hook
