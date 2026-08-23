---
template_id: skill-template
template_version: "0.6.1"
feature_refs:
  - FEAT-0022
  - FEAT-0054
  - FEAT-0057
  - FEAT-0062
consumer_scope: skill
applies_to:
  - skills/*/SKILL.md
surface_fields:
  skill_ui: supported
---

---
name: {skill_name}
description: "[TODO: Verb input/context into output/artifact when call-condition; <=220 chars.]"
tier: [TODO: 1 | 2 | 3]
source: local
# Optional static projection. Choose exactly one kind; variants remain normal
# invocation inputs rather than their own skills or capabilities.
# capability:
#   kind: artifact # artifact | integration | shortcut
#   consumes: ["input-artifact-id"]
#   produces: ["output-artifact-id"] # artifact only; exactly one
# capability:
#   kind: integration
#   consumes: ["input-artifact-id"]
template_uses:
  skill-template: "0.6.0"
# Add only after the skill fits 10 top-level todos and 5 evals.
# skill-surface-budget: "0.1.0"
# Tier 3 only: back-office | sales | deals | marketing | operations |
# intelligence | customer. See rules/skill-departments.toml.
group: [TODO: canonical department required for Tier 3]
allowed-tools: {tools}
---

# {skill_title}

## Context

[TODO: In two to four plain sentences say when to use this skill, what it does,
and what it preserves or does not own. Keep only normal-path context here. Put
branch-only detail in `references/*`.]

[TODO: Do not add a generic `## Job`. Paths inside the package are relative,
such as `scripts/foo.py` and `references/foo.md`.]

## Skill Signature

```text
{skill_function}(required_input, option?) -> output
reads: {files or data required}
does: {one plain sentence describing the work}
writes: {files changed, or none}
returns: {files, artifacts, result, or verdict}
```

[TODO: Treat this as type linting, not a state-machine specification. Name only
the required inputs or files, caller-controlled parameters, work performed, and
files, artifacts, or result returned. Put workflow rules in Todo List and
failure examples in Gotchas.]

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — {domain verb + concrete outcome}.**
  `{input_state} -> {output_state} | {named_branch}`

  Rule: {non-obvious domain decision that changes the result.}

  Example: `{representative input} -> {decisive signal} -> {accepted output}`

  Assert:
  - {observable output condition}
  - {critical invariant, rejection, or branch condition}

[TODO: Repeat the Golden Workflow Node block for three to seven real workflow
moves. Each top-level node must be executable as one bounded operation, emit
inspectable state for the next node, and contain domain language that would not
fit an unrelated skill. Keep Rule and Assert. Keep Example when judgment,
hidden edge, or a tempting ambiguity changes the route; otherwise omit it.
Do not add generic bind, inspect, transform, preserve, self-audit, or next
fields—the signature and assertions carry those obligations.]
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

<!-- Optional modules:
- `## Templates`: keep when a reusable output shape is actually consumed.
- `## Reference Map`: keep when a conditional branch has detail to load.
- `evals/evals.json`: add when variable behavior needs a focused judgeable case;
  the registry discovers it by path, so do not repeat that fact in frontmatter.
- `ensemble.yaml`: add only when the skill owns optional independent-perspective
  coverage. Direct remains the default; `auto` selects three relevant personas
  and `max` selects all without changing the skill's output contract.
- `examples/golden/*`: add when a useful example is too large to sit beside its
  rule. Keep short examples inline.
Follow docs/skills/best-practices.md and skill-maintenance for their exact
contracts instead of copying setup instructions into every new skill.
-->

## Gotchas

- [TODO: Show one to three tempting mistakes concretely. Name the bad action
  and consequence; generic warnings such as "be accurate" are not enough.]

## Output

- [TODO: Name the exact files, artifacts, result, or verdict returned and its
  default response format. Do not repeat the signature or todo path.]
