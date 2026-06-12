# Git Hooks

These hooks are optional. `deep-init-project` scaffolds them so each repo has a
clear place for local quality gates, but nothing is enabled automatically.

## Recommended Default

Use `pre-push` for the heavier local gate:

- large-file scan: warn at `500` raw lines, block at `1000`
- project-owned local validators such as lint, typecheck, tests, and optional build
- advisory Codex SDK diff review after deterministic checks
- optional soft heavy checks such as `desloppify`

Use `pre-commit` only when you explicitly want a smaller fast gate before each
commit.

## Activate

To make this repo use `.githooks/`:

```bash
git config core.hooksPath .githooks
chmod +x .githooks/pre-push
```

If you also want the optional pre-commit hook:

```bash
chmod +x .githooks/pre-commit
```

## Notes

- The sample hooks call repo-local validation scripts first:
  - `scripts/pre_commit_check.sh`
  - `scripts/pre_push_check.sh`
- `scripts/pre_push_check.sh` is the main policy surface. Put project-specific
  commands and exclusions there rather than expanding the hook itself.
- The `pre-push` hook runs the local Codex SDK diff reviewer by default when
  configured. Use `FARPLANE_SKIP_AGENT_REVIEW=1` to skip it or
  `STRICT_AGENT_REVIEW=1` to make it blocking.
- The local diff reviewer should read the installed Farplane `code-review`
  skill from `~/.codex/skills/code-review/SKILL.md` when available. Run the
  Farplane install script to keep skills and review rubrics linked into
  `~/.codex`.
- CodeRabbit remains an optional heavier external review pass, not the default
  local reviewer.
- Utility-sharing warnings should stay advisory by default. Put the real shared
  utility placement convention in `PROJECT_RULES.md`.
- Remove or rename the hook files if the project should not use them.
