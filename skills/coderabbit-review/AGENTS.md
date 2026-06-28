# CodeRabbit Review Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `SKILL.md` Todo List
- `references/stage-matrix.md`
- `references/hook-recipes.md`
- `scripts/run_review.py`
- `scripts/pre-commit.sample`
- `scripts/pre-push.sample`

## Boundaries

- Keep this skill about explicit local CodeRabbit CLI review.
- Keep the default recommendation at `pre-push` or PR time.
- Keep `pre-commit` available but clearly optional.
- Keep this off `hooks.json` and off the Stop hook by default. See `MEM-0039`.
- Do not imply GitHub PR-thread autofix unless a later ticket adds that flow.

## Conventions

- Prefer stage-aware defaults over long raw command explanations.
- Fail clearly when `coderabbit` is missing or unauthenticated.
- Keep the runner narrow: base detection, stage mapping, and clear errors.
- Keep the hook samples opt-in and easy to inspect.

## Checks

- Trigger conditions, workflow, branches, gotchas, and outcome contract exist.
- `SKILL.md` is executable without opening references.
- The runner supports `pre-commit`, `pre-push`, and `pr`.
- The docs consistently say this is not a Stop-hook default.

## Testing

- Re-read `SKILL.md` once and confirm the core path is executable without refs.
- Run `python3 skills/coderabbit-review/scripts/run_review.py --stage pre-commit --dry-run`.
- Run `python3 skills/coderabbit-review/scripts/run_review.py --stage pre-push --dry-run`.
- Confirm the sample hook files call the repo-local runner and do not
  auto-install anything.
