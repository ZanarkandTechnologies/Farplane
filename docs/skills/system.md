# Farplane Skill System

This is the canonical contract for Farplane skills. Use it before creating,
maintaining, or validating skills so the tier model, source ownership, registry
fields, and todo-link rules stay in one place.

## Ownership

- `docs/skills/system.md` owns the stable skill-system contract.
- `docs/skills/README.md` owns human skill selection and registry commands.
- `docs/skills/best-practices.md` owns skill authoring and maintenance quality,
  not runtime context for every skill invocation.
- `skills/skill-creator/` owns creating or updating one reusable skill package.
- `skills/skill-maintenance/` owns bulk upkeep, validation, generated registry
  sync, and rollout audits.
- `docs/features/registry.jsonl` owns harness-wide feature rows, including
  skill-applicable features with `category: "skills"`.
- `docs/skills/registry.jsonl` is generated inventory, not hand-authored truth.
- `skills/<skill-name>/eval_task.json` owns focused modular eval tasks for one
  skill's behavior when a runnable eval is the right proof surface.

Keep this file focused on stable system rules. Do not duplicate first-load
authoring detail here; link `docs/skills/best-practices.md` for checklist
shape, reference placement, repeatability, and finish gates.

## Tier Model

Tier 0 is the universal phase protocol, not a skill tier and not a frontmatter
value. It describes the lifecycle every material skill invocation should pass
through at the right level of ceremony:

```text
phase_protocol(task, skill_signature?, state?)
  -> grounded_inputs
   + plan_or_direct_action
   + plan_review_if_material
   + execution
   + guardrail_or_eval
   + evidence_review_if_material
   + writeback
```

Codex native planning and execution modes already own much of this runtime
behavior. Farplane uses Tier 0 to describe the expected phase shape in
`templates/global/AGENTS.md`, skill templates, tickets, and reviewer handoffs.
Do not create `tier: 0` skills for phases such as plan, execute, or review.
Phases are inherited by skills; they are not lower-level skill dependencies.

## Phase Ownership And Recursion

Every skill invocation may perform Tier 0 phases inline. A skill should call a
phase-like skill such as `plan`, `review`, or `eval` only when that phase needs
its own durable artifact, independent judgment, explicit budget, handoff, or
proof surface.

```text
inline_phase(skill, phase, task) -> local_decision
external_phase(skill, phase, task, budget) -> artifact + evidence
```

`plan` does not own review. It owns task decomposition, selected workflows,
proof target, handoff shape, and an optional review request for the plan
artifact. `review` does not own planning. It owns judgment of an artifact
against selected rubrics, and may plan its own review inline when the scope is
small enough.

Externalized phase calls must shrink or specialize the parent scope:

```text
externalize_phase(parent_task, phase, child_scope, budget)
  -> skill_call | inline_phase

valid_external_phase_call(parent_scope, child_scope)
  -> child_scope < parent_scope
```

Same-scope recursion is invalid. For example, `plan(epic)` may produce a
`review_request` for the epic plan, and `review(epic_plan)` may perform a small
inline review plan. But `review(epic_plan)` should not call `plan` for another
epic-sized review plan, and `plan(review_plan)` should not call `review` again
at the same scope.

Use phase skills when the expected value of a separate phase artifact exceeds
its coordination cost:

```text
use_phase_skill(phase, task, risk, ambiguity, proof_gap, coordination_cost)
  -> true when value(artifact_or_independent_judgment) > coordination_cost
```

When a skill's signature requires inputs that the user did not supply, the
agent should backpropagate the missing parameters: inspect local state, load the
right context, call a setup or planning workflow, or ask only if the missing
input is truly blocking. In function form:

```text
resolve_skill_params(skill_signature, user_request, state)
  -> bound_inputs | setup_workflow | blocking_question
```

Tier 1 skills are primitives. They are core thinking moves that multiple Tier 2
interfaces need as base obligations. Farplane's current Tier 1 primitives are:

- `advise`: choose among real options and name the recommendation.
- `reference-grounding`: ground claims, plans, and recommendations in evidence.
- `prototyping`: prove a pattern at the smallest honest scale before expanding.

Create a new Tier 1 primitive only when multiple Tier 2 interfaces need that
move as a base dependency.

Tier 2 skills are generic workflow interfaces. They turn primitive obligations
into reusable protocol surfaces such as:

- `brainstorm`
- `plan`
- `research:*`
- `harness-advisor`

Common reusable work that many Tier 3 skills need should usually start as a
Tier 2 interface or method, not a new Tier 1 primitive.

Tier 3 skills are application or domain skills. They implement Tier 2
interfaces for a concrete workflow, domain, package, or artifact type. Examples
include coding pipeline skills, frontend/media/document skills, and meta skills
such as `skill-creator` and `skill-maintenance`.

Meta skills are not Tier 0. They are skills whose domain is the harness or skill
system itself. Represent them with normal numeric `tier` plus `group: meta`,
`group: skills`, `group: harness`, or another explicit group. Use Tier 0 only
for universal lifecycle phases.

Reclassification candidates:

- `plan` is a Tier 2 planning prompt-template and todo-composition interface.
  It is not the Tier 0 planning phase itself; use it when planning can reduce
  wasted search, compose skill todos, or set proof and handoff before a costly
  phase.
- `execute` duplicates Codex native execution mode and should be treated as a
  transitional compatibility package unless a concrete Farplane workflow still
  calls it as an invocable contract.
- `review` is better understood as a review protocol and rubric/TAS contract.
  Keep the callable Tier 2 wrapper while it is useful; rubric bodies live in
  `docs/review/rubrics/*` and reviewer agents can read those docs directly.

## Todo-Link Rules

First-load todo links should follow the dependency hierarchy:

- Tier 2 first-load todos may link Tier 1 primitives.
- Tier 3 first-load todos should usually link Tier 2 surfaces such as
  `research:*` and domain workflow interfaces when those are real invocable
  contracts.
- Tier 3 first-load todos may link peer Tier 3 skills when the domain flow has
  an intentional handoff.
- Tier 3 first-load todos should not direct-link Tier 1 primitives such as
  `advise` or `reference-grounding` unless the skill owns that primitive step
  as part of its first-load contract.
- Tier 0 phase steps do not need skill links. Put the phase shape in the todo
  template or skill `## Phase Contract` instead of linking to `plan` or
  `execute`.
- `review` is a protocol exception: skills may link to the review wrapper when
  material evidence needs TAS judgment, regardless of normal one-level tier
  dependency direction.

Use `bin/validators/check_skill_todo_tiers.py --allow-peer-tier3` to audit the current
intentional hierarchy.

## Frontmatter Contract

Keep skill frontmatter small.

Manual fields:

- `tier`: required, numeric `1`, `2`, or `3`.
- `description`: required one-sentence functional routing definition of 220
  characters or less. Prefer
  `Verb input/context into output/artifact when call-condition`.
  Include the input and output when they are not obvious. Keep trigger
  catalogs, examples, model/provider maps, routing policy, and detailed caveats
  in the skill body or references.
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
- If a useful skill begins life in `~/.codex/skills`, pull it into repo source
  with `python3 bin/import_installed_skills.py --skills <name> --dry-run` first,
  then rerun without `--dry-run` after reviewing the package boundary. Existing
  repo packages require explicit `--overwrite` and are backed up under
  `.farplane/import-backups/`.
- Put skill-specific eval tasks beside the source skill as `eval_task.json`.
  Keep broad working suites under `.farplane/evals` and reusable cross-skill
  examples under `skills/eval/examples`.

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

Agents should treat skill signatures like callable contracts. When invoking a
skill, check the signature before execution:

1. Bind the known user request and current state to the signature inputs.
2. Resolve missing required inputs through context gathering, setup workflows,
   or a narrow blocking question.
3. Use the listed gates as the proof and review obligations.
4. Use the listed routes instead of inventing hidden downstream workflow.

## Skill Budgets

Budgets are optional parameters for skills where cost, depth, search breadth,
finish-gate depth, delegation, or external compute materially change the best
workflow. Do not add budget schema to every skill by default.

Use budgets when they help the coordinator choose the right effort level:

```text
skill_budget(task, risk, ambiguity, cost)
  -> grounding_depth + search_breadth + compute_mode + finish_gate_depth + stop_condition
```

Good budget-bearing skills expose a small set of parameters that alter behavior
in meaningful ways. For tiny, deterministic, or single-path skills, normal todo
binding is enough and a budget section is noise.

All skills inherit an implicit effort budget from the coordinator. Only
budget-sensitive skills should document explicit budget parameters. Phase
budgets should include a recursion cap when a phase skill may externalize
another phase:

```text
phase_budget = {
  effort?: "tiny" | "normal" | "deep",
  finish_gate?: "none" | "self-check" | "checklist" | "validator" | "eval" | "QA" | "review" | "external",
  max_phase_depth?: 0 | 1 | 2
}
```

`max_phase_depth: 0` means inline phases only. `max_phase_depth: 1` permits one
externalized phase. `max_phase_depth: 2` permits a phase of a phase only when
the child scope is smaller or more specialized than the parent scope.

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
