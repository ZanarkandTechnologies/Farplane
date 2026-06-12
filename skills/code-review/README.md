# Code Review

Lightweight local diff review for pre-push, pre-commit, or small branch checks.

This skill is the reusable prompt contract that Codex SDK reviewer scripts can
load. It deliberately does not replace Farplane's material TAS reviewer lane:

- local diff review: `skills/code-review/SKILL.md`
- material TAS review: `skills/review/SKILL.md` plus `agents/reviewer.toml`
- optional external heavyweight review: `skills/coderabbit-review/`

## Proof

After changing this package, run:

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
```
