# Convex Skill Maintenance Rules

## Scope

Applies to files in this directory:
- `SKILL.md`
- `references/*.md`
- `scripts/*`
- `assets/*`

## Boundaries

- Keep `SKILL.md` as the primary first-pass guide with always-needed defaults.
- Keep deep implementation details in `references/*.md`.
- Avoid duplicate references for the same topic; maintain one canonical file per topic.

## Conventions

- Prefer concise instructions and checklists over long prose in `SKILL.md`.
- Use stable names for canonical references (for example `multiplayer.md`, `workflows.md`).
- If splitting a canonical file, document why and update `SKILL.md` links in the same change.

## Required Checks After Edits

- All links in `SKILL.md` resolve to existing files.
- No stale references to removed files remain.
- New references are directly linked from `SKILL.md` (one level deep).

## Testing Expectations

- Validate link integrity with `rg`/file existence checks.
- Re-read `SKILL.md` to ensure always-load sections still match canonical references.
- Ensure workflow and multiplayer docs remain single-source unless a justified split is introduced.
