---
name: {skill_name}
description: [TODO: Clear trigger/use description. This metadata decides when the skill loads.]
tier: [TODO: 1 | 2 | 3]
source: local
skill_template_version: "0.2.0"
feature_refs:
  - FEAT-XXXX
group: [TODO: required for Tier 3]
allowed-tools: {tools}
---

# {skill_title}

## Context

[TODO: Only context needed every time this skill loads: tier/system placement,
source-of-truth docs, ownership constraints, and assumptions.]

[TODO: Do not add a generic `## Job`; put ordered work in `## Todo List` as
visible task labels like `- [ ] 1. ...`, and use a specific contract section
only when it adds non-duplicated durable shape.]

[TODO: Paths in this skill are relative to this skill package. Use
`scripts/foo.py` and `references/foo.md` for nearby files.]

## Skill Signature

[TODO: Keep this when it clarifies callable behavior, state, gates, routes, or
failure modes. Delete it only for tiny skills where the todo list already makes
composition obvious. See `docs/specs/self-improvement-contracts.md`.]

```text
{skill_function}(input_text, state?) -> primary_output + evidence?
state: reads(...); writes(...); remembers(...)
gates: proof_or_review_condition; blocker_condition
routes: next-skill | next-skill:method | direct-answer
fails: known bad behavior; overbroad behavior; misplaced ownership
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read required context and current artifacts.
- [ ] 2. Choose the branch.
   - [ ] 1. Default branch.
   - [ ] 2. Update/repair branch.
   - [ ] 3. Review branch.
- [ ] 3. Execute the workflow for the selected branch.
- [ ] 4. Produce or update the required artifact.
- [ ] 5. Verify with the named proof command or evidence surface.
- [ ] 6. Review against the gotchas before completion.
   - [ ] Repeatability from files alone.
   - [ ] No duplicated first-load logic.
   - [ ] Explicit proof command or blocker.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [TODO: Inline one short positive example, or link to `templates/*` /
  `prompts/*` when examples are too long.]
- [TODO: If this skill needs a focused behavioral eval, add
  `eval_task.json` at the skill package root using the eval task JSON-list
  schema.]

## Gotchas

- [TODO: Negative example or failure pattern.]
- [TODO: Negative example or failure pattern.]
- [TODO: Negative example or failure pattern.]

## Reference Map

- [TODO: `references/name.md` - read only when ...]

## Output

- [TODO: Expected artifact, type, path, or response shape.]
