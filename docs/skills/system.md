# Farplane Skill System

This is the canonical contract for Farplane skills. Use it before creating,
maintaining, or validating skills so the tier model, source ownership, registry
fields, and todo-link rules stay in one place.

## Ownership

- `docs/skills/system.md` owns the stable skill-system contract.
- `docs/skills/README.md` owns human skill selection and registry commands.
- `docs/skills/best-practices.md` owns first-load authoring quality.
- `skills/skill-creator/` owns creating or updating one reusable skill package.
- `skills/skill-maintenance/` owns bulk upkeep, validation, generated registry
  sync, and rollout audits.
- `docs/features/registry.jsonl` owns harness-wide feature rows, including
  skill-applicable features with `category: "skills"`.
- `docs/skills/registry.jsonl` is generated inventory, not hand-authored truth.

Keep this file focused on stable system rules. Do not duplicate first-load
authoring detail here; link `docs/skills/best-practices.md` for checklist
shape, reference placement, repeatability, and review gates.

## Tier Model

Tier 1 skills are primitives. They are core thinking moves that multiple Tier 2
interfaces need as base obligations. Farplane's current Tier 1 primitives are:

- `advise`: choose among real options and name the recommendation.
- `reference-grounding`: ground claims, plans, and recommendations in evidence.
- `prototyping`: prove a pattern at the smallest honest scale before expanding.
- `review`: challenge completion claims against evidence and rubric gates.

Create a new Tier 1 primitive only when multiple Tier 2 interfaces need that
move as a base dependency.

Tier 2 skills are generic workflow interfaces. They turn primitive obligations
into reusable protocol surfaces such as:

- `brainstorm`
- `research:*`
- `plan`
- `execute`
- `harness-advisor`

Common reusable work that many Tier 3 skills need should usually start as a
Tier 2 interface or method, not a new Tier 1 primitive.

Tier 3 skills are application or domain skills. They implement Tier 2
interfaces for a concrete workflow, domain, package, or artifact type. Examples
include coding pipeline skills, frontend/media/document skills, and meta skills
such as `skill-creator` and `skill-maintenance`.

## Todo-Link Rules

First-load todo links should follow the dependency hierarchy:

- Tier 2 first-load todos may link Tier 1 primitives.
- Tier 3 first-load todos should usually link Tier 2 surfaces such as
  `research:*`, `plan`, and `execute`.
- Tier 3 first-load todos may link peer Tier 3 skills when the domain flow has
  an intentional handoff.
- Tier 3 first-load todos should not direct-link Tier 1 primitives such as
  `advise`, `reference-grounding`, or `review`; the Tier 2 surface carries
  those obligations.

Use `bin/check_skill_todo_tiers.py --allow-peer-tier3` to audit the current
intentional hierarchy.

## Frontmatter Contract

Keep skill frontmatter small.

Manual fields:

- `tier`: required, numeric `1`, `2`, or `3`.
- `source`: required, `local` or `external`.
- `skill_template_version`: optional structural baseline for skills onboarded
  to a known Farplane skill template version; absence means not onboarded yet.
- `feature_refs`: optional compact list of `FEAT-####` records this skill
  package implements, depends on, or deliberately adopts. The feature registry
  owns the feature details, evidence, limits, and metrics.
- `group`: required for Tier 3 only.
- `methods`: optional method addresses owned by the skill.
- `common_chains`: optional one-way Tier 3 adjacency hints.
- `upstream_url`: optional for `source: external`.

Generated registry fields include `path`, `description`, `has_checklist`,
`has_todos`, `version`, `allowed_tools`, `skill_links`, and the manual fields
above. `feature_refs` values are validated against
`docs/features/registry.jsonl`. Derive generated fields from source files
instead of duplicating them in frontmatter.

## Source Ownership

- `source: local` means Farplane owns the skill package and may edit its body,
  references, scripts, templates, and direct todo list.
- `source: external` means the package is upstream-owned and should stay
  refreshable. Keep local Farplane wrapper policy in local caller skills.
- Do not patch installed skill bodies such as `~/.codex/skills/*` as the source
  of truth. Edit the Farplane source package, then reinstall selected skills.

## Template Versioning

`skill_template_version` tracks structural onboarding, not every migration ever
applied. A versioned skill promises that its `SKILL.md` follows the current
template spine and todo-list shape for that version.

Use:

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --template-version 0.2.0
```

Add `--require-template-version` only when the rollout is intentionally ready to
fail missing or non-current skills.

## Rollout Policy

Roll out skill-system standards from the most compound surfaces first:

1. Meta skills and Tier 1 primitives stay current by default.
2. Core Tier 2 interfaces are updated when standards change.
3. Tier 3 skills are updated on contact, by cluster, or when repeated failure
   evidence shows the old shape is hurting execution.
4. Broad migration requires a representative sample before a full batch.
5. Missing `skill_template_version` means not onboarded yet, not invalid.

Use `skill-maintenance` for rollout audits and `docs/skills/best-practices.md`
for the concrete on-contact upgrade checklist.

## Skill Signatures

Template `0.2.0` adds a compact `## Skill Signature` section for skills whose
composition would otherwise stay implicit. The signature is a human-readable
contract, not a heavy schema:

```text
skill_action(input_text, state?) -> primary_output + evidence?
state: reads(...); writes(...)
gates: proof_condition; review_condition
routes: next-skill | next-skill:method | direct-answer
fails: known bad behavior
```

Use `docs/specs/self-improvement-contracts.md` for the full grammar and the
self-improvement workflow contracts.

## Feature Tracking

Skill-applicable capabilities belong in the harness-wide feature registry:

```json
{"category": "skills"}
```

Use feature rows for supported optional capabilities such as eval support,
skill capability fixtures, or autoresearchability. Use `feature_refs` in skill
frontmatter only to record compact `FEAT-####` adoption handles for the skill
package. Use `skill_template_version` for structural template onboarding.

Do not store long applied-migration histories in skill frontmatter. If a
migration needs rollout tracking, let `skill-maintenance` compare the generated
skill inventory, template version report, `feature_refs`, and relevant feature
rows.

## Installed Rendering

Source `SKILL.md` files own the first-load todo list. Installed skill packages
are rendered artifacts. After editing source skills, reinstall before judging
live Codex behavior:

```bash
bash install.sh --skills-only --skills <names> --target ~/.codex
```

Then inspect `~/.codex/skills/<name>/SKILL.md` when the user is checking the
installed experience.
