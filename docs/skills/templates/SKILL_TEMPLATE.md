---
template_id: skill-template
template_version: "0.4.4"
feature_refs:
  - FEAT-0022
  - FEAT-0054
  - FEAT-0057
  - FEAT-0062
consumer_scope: skill
applies_to:
  - skills/*/SKILL.md
surface_fields:
  eval: supported
  qa_checklist: supported
  skill_ui: supported
  workflow: optional
---

---
name: {skill_name}
description: "[TODO: Verb input/context into output/artifact when call-condition; <=220 chars.]"
tier: [TODO: 1 | 2 | 3]
source: local
template_uses:
  skill-template: "0.4.4"
# Add only after the skill fits 10 top-level todos, 5 QA checks, and 5 evals.
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

1. [Bind the real input, desired result, and any choice that would materially
   change the work. Infer ordinary context instead of asking for everything.]
2. [Inspect the input for the domain signals that determine the approach.]
   Example: [real input] -> [tempting wrong interpretation or result] -> [why
   it fails].
3. [Perform the domain transformation and name the facts, structure, behavior,
   or intent that must survive it.]
4. [Handle the one meaningful branch or quality decision, when one exists.]
   Assert: [add only when this stage has an ambiguous expected state, likely
   drift, costly failure, or a gate required by the next stage].
5. [Self-audit with two concrete questions: one about output quality and one
   about preservation or correctness. Fix failures, then return the exact output.]

[TODO: Replace every bracketed prompt with domain-specific language. Keep three
to five top-level actions by default. If a step could be pasted into an
unrelated skill, rewrite it. Omit the `Assert:` line when the result is obvious
or mechanically verified. Keep the embedded example, preservation rule, and
self-audit instead of replacing them with generic drafting steps.]
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

<!-- Optional modules:
- `## Templates`: keep when a reusable output shape is actually consumed.
- `## Reference Map`: keep when a conditional branch has detail to load.
- `qa_checklist.md`: add when repeatable runtime guardrails need preflight and
  finish use.
- `evals/evals.json`: add when variable behavior needs a focused judgeable case.
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
