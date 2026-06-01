# PR Splitting Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `SKILL.md` Important Checklist
- `references/decision-rules.md`
- `references/output-template.md`

## Boundaries

- Keep this skill about post-build PR decomposition, not pre-implementation
  planning.
- Keep it non-stacked by default.
- Keep feature-first as the default recommendation.
- Keep hunk-splitting discouraged except for rare mechanical cases.
- Keep the skill planning-first; do not imply automatic branch or GitHub
  mutation unless a later ticket explicitly adds that.

## Conventions

- Mergeability against base outranks size balancing.
- Reviewer story outranks neat folder symmetry.
- Exact file lists are required in the output.
- Shared-file blockers should be named explicitly, not hidden in misc buckets.

## Checks

- Trigger conditions, workflow, branches, guardrails, and output contract exist.
- The skill contains a refusal path for dishonest non-stacked splits.
- The references deepen the decision policy and output shape without duplicating
  the whole skill.

## Testing

- Re-read `SKILL.md` once and confirm it is executable without opening refs.
- Confirm the `SKILL.md` Important Checklist stays plain checklist text with Markdown links.
- Confirm the references reinforce feature-first with layer fallback rather than
  drifting toward stack planning or hunk surgery.
