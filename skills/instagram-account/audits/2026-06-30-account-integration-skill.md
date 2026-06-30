---
kind: skill-audit
skill: instagram-account
status: pass
created_at: 2026-06-30
---

# Instagram Account Skill Audit

## Change

Created a platform account-integration skill for Instagram publishing
boundaries, profile/media insights, metrics normalization, and gated API
actions.

## Grounding

- Existing `social-content` owns creative drafting and campaign artifacts.
- `farplane/bindings.md` owns non-secret account aliases and policy.
- Private credentials follow the existing `~/.codex/private/` convention.
- Instagram Platform/Graph API docs are linked in `references/api.md`; broad
  scraping routes to `apify` or `feed-scout`.

## Checklist Verdicts

- `ownership_explicit:` pass - account integration is separate from drafting.
- `first_load_sufficiency:` pass - default path, gates, outputs, and blockers
  are visible in `SKILL.md`.
- `reference_load_precision:` pass - API and metrics references have explicit
  load conditions.
- `secret_boundary:` pass - tracked files name only env prefixes and aliases.
- `proof_surface_fit:` pass - skill system validators are the current proof;
  live API behavior is blocked until credentials and approval exist.

## Proof

- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- `python3 bin/validators/check_farplane_project_files.py`
