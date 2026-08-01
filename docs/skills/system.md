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
- feature pages in `docs/features/` own skill-applicable harness feature docs
  with `category: "skills"`, and `docs/systems/skill-system.md` links the
  surviving feature refs.
- `docs/features/registry.jsonl` is generated feature output, not hand-authored
  truth.
- `docs/skills/registry.jsonl` is generated inventory, not hand-authored truth.
- `skills/<skill-name>/evals/evals.json` owns focused modular eval tasks for one
  skill's behavior when a runnable eval is the right proof surface.
- `skills/<skill-name>/qa_checklist.md` owns first-class skill-local QA checks
  for settled runtime guardrails when a Markdown checklist is the right
  real-time review surface.

Keep this file focused on stable system rules. Do not duplicate first-load
authoring detail here; link `docs/skills/best-practices.md` for checklist
shape, reference placement, repeatability, and finish gates.

## Skill-Local Configuration

A local Farplane skill may own an optional `config.toml` at its package root
when reusable non-secret defaults would otherwise drift across prompts or
prose. This is a package input, not a second runtime controller:

```text
load_skill_defaults(skill/config.toml, invocation)
  -> parsed_safe_defaults | blocked_report

precedence: invocation > skill-local config > explicit SKILL.md fallback
secrets: runtime environment / Doppler only
```

The skill must read its config before choosing a default method, profile, or
provider. Tracked config is safe to commit and limited to `schema_version`,
`skill`, and the `defaults`, `profiles`, and `providers` tables. Values are TOML
scalars or scalar arrays. API keys, tokens, passwords, private keys, auth
material, webhook secrets, and credential-bearing keys are forbidden at every
depth. Provider voice/reference IDs may be tracked only when intentionally
repo-shareable and rights-safe; personal or private IDs remain invocation or
private runtime context.

`skills/skill-maintenance/scripts/validate_skill_configs.py` enforces this
boundary across root and project-local skill packages. Adding `config.toml` to
one skill does not require migrating unrelated skills.

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

Numeric skill tiers are compound leverage classes. A lower numeric tier means
that improvements to the skill tend to propagate through more downstream
workflows, so those packages should be kept sharper and upgraded earlier. The
same tier metadata also informs first-load todo-link rules, but the link rules
are the loading contract; the tier itself is the skill's compounding upgrade
class.

```text
tier(skill) -> compound_leverage_class
todo_link_rules(skill) -> first_load_loading_boundary
upgrade_priority(skill, evidence) -> rollout_order
```

When a loop must rank skills as improvement targets, use the signal contract in
`docs/features/FEAT-0064-skill-signals.md`: direct heat, composition
heat, maintenance burden, and uniqueness. The output is a maintenance
recommendation such as `keep`, `harden`, `refine`, `merge`, `watch`, or
`retire_review`, not a skill tier, eval score, or skill quality grade.

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

Tier 1 skills are highest-compounding primitives. They are core moves or small
provider contracts that multiple higher-tier workflows need as base obligations.
Farplane's current core behavior primitives are:

- `advise`: choose among real options and name the recommendation.
- `consolidate`: compress artifacts into their minimal owner-correct form while
  preserving required behavior, proof, IDs, and actionability.
- `reference-grounding`: ground claims, plans, and recommendations in evidence.
- `prototyping`: prove a pattern at the smallest honest scale before expanding.

Create a new Tier 1 primitive only when multiple Tier 2 interfaces need that
move as a base dependency. Small provider primitives, such as notification
senders, may also be Tier 1 when they are intentionally reused by multiple
higher-tier workflows and have a narrow, stable contract.

Tier 2 skills are medium-compounding workflow interfaces. They turn primitive
obligations into reusable protocol surfaces such as:

- `brainstorm`
- `plan`
- `research:*`
- `harness-advisor`

Common reusable work that many Tier 3 skills need should usually start as a
Tier 2 interface or method, not a new Tier 1 primitive.

Tier 3 skills are application or domain skills. They have the narrowest normal
compounding radius and implement Tier 2 interfaces for a concrete workflow,
domain, package, or artifact type. Examples include coding pipeline skills,
frontend/media/document skills, and meta skills such as `skill-creator` and
`skill-maintenance`.

Meta skills are not Tier 0. They are skills whose domain is the harness or skill
system itself. Represent them with normal numeric `tier` plus `group: meta`,
`group: skills`, `group: harness`, or another explicit group. Use Tier 0 only
for universal lifecycle phases.

Do not create `tier: 4` to describe an end-to-end workflow. Numeric tiers are
compounding upgrade classes, not call-stack depth. Model e2e workflows as
composition artifacts owned by the orchestrating surface:

```text
workflow_chain(owner_skill, scenario)
  -> key_steps[] + source_refs[] + proof_surface
```

Use these surfaces to make a chain visible:

- observed skill heat from Farplane telemetry when deciding which skills should
  receive visual prominence in graph views. Invocation counts are behavior, not
  hand-maintained taxonomy.
- generated todo-chain edges from every skill's `## Todo List` when it contains
  first-seen explicit skill references in order: Markdown `SKILL.md` links,
  backticked `skill-name` refs, or `$skill-name` refs. Plain prose is ignored.
- `common_chains` in skill frontmatter for stable Tier 3 adjacency hints.
- `routes:` in `## Skill Signature` for normal downstream owners.
- workflow reference files under `skills/<owner>/references/` when one
  orchestrator owns a conditional multi-skill procedure.
- `evals/evals.json` rows when the composed behavior should be tested end to end.
- lifecycle graph curated edges only for framework-critical paths that need UI
  rendering.

An e2e eval should mark every required skill in the chain as a key workflow
step in its reference points. This tests composition without turning chained
skills into a new skill tier.

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

First-load todo links should follow the loading boundary derived from the tier
model. This preserves progressive disclosure and avoids making every domain
skill import every primitive directly:

- Tier 2 first-load todos may link Tier 1 primitives.
- Tier 3 first-load todos should usually link Tier 2 surfaces such as
  `research:*` and domain workflow interfaces when those are real invocable
  contracts.
- Tier 3 first-load todos may link peer Tier 3 skills when the domain flow has
  an intentional handoff.
- Tier 3 first-load todos should not direct-link Tier 1 primitives such as
  `advise`, `consolidate`, `reference-grounding`, or `prototyping` unless the
  skill owns that primitive step as part of its first-load contract.
- Tier 0 phase steps do not need skill links. Put the phase shape in the todo
  template or skill `## Phase Contract` instead of linking to `plan` or
  `execute`.
- `review` is a protocol exception: skills may link to the review wrapper when
  material evidence needs TAS judgment, regardless of normal one-level tier
  dependency direction.

Use `bin/validators/check_skill_todo_tiers.py --allow-peer-tier3` to audit the current
intentional first-load loading contract.

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
- `eval`: optional path to a skill-local eval task file, usually
  `evals/evals.json`.
- `qa_checklist`: optional path to a skill-local runtime checklist, usually
  `qa_checklist.md`.
- `skill_ui`: optional path or route for a skill-owned UI, viewer, dashboard,
  debug page, or UI binding.
- `group`: required for Tier 3 only.
- `methods`: optional method addresses owned by the skill.
- `common_chains`: optional one-way Tier 3 adjacency hints.
- `upstream_url`: optional for `source: external`.

Generated registry fields include `path`, `description`, `has_checklist`,
`version`, `allowed_tools`, `skill_links`, `todo_skill_refs`, and the manual
fields above.
Structural feature IDs belong to the versioned skill template metadata, not
per-skill frontmatter. Derive generated fields from source files instead of
duplicating them in frontmatter.

Skills that opt into capped surface enforcement declare the structural marker in
`template_uses`, not raw `feature_refs`:

```yaml
template_uses:
  skill-surface-budget: "0.1.0"
```

This marker is backed by `FEAT-0062` and checked by
`bin/validators/check_skill_surface_budget.py`. Subscribed skills must fit the
default `10 / 5 / 5` budget: 10 top-level `SKILL.md` todos, 5
`qa_checklist.md` items, and 5 skill-local eval tasks. Before adding item N+1,
run `skill-maintenance.refine_skill` with
`consolidate(target = edited_skill, structure = skill)` and keep, merge, move,
or delete units by value rather than appending by default.

## Source Ownership

- `source: local` means Farplane owns the skill package and may edit its body,
  references, scripts, templates, and direct todo list.
- `source: external` means the package is upstream-owned and should stay
  refreshable. Keep local Farplane wrapper policy in local caller skills.
- Do not patch installed skill bodies such as `~/.codex/skills/*` as the source
  of truth. Edit the Farplane source package, then reinstall selected skills.
- If a useful skill begins life in `~/.codex/skills`, pull it into repo source
  with `python3 skills/skill-maintenance/scripts/import_installed_skills.py --skills <name> --dry-run` first,
  then rerun without `--dry-run` after reviewing the package boundary. Existing
  repo packages require explicit `--overwrite` and are backed up under
  `.farplane/import-backups/`.
- Put skill-specific eval tasks beside the source skill as `evals/evals.json`.
  Keep broad working suites under `.farplane/evals` and reusable cross-skill
  examples under `skills/eval/examples`.
- Put skill-specific runtime QA guardrails beside the source skill as
  `qa_checklist.md` when the skill repeatedly needs the same preflight checks,
  final checks, reviewer prompts, or eval-derived guardrails. Keep the file
  Markdown until a runner or renderer needs stricter structure.
- Put skill-specific example fixtures beside the source skill as
  `examples/<slug>/example.md`, with optional local support files under
  `examples/<slug>/assets/`. Use this shape when a quality-dependent skill
  needs reference media, accepted outputs, comparison gates, or provenance that
  must travel with the package. Keep broad reusable eval examples under
  `skills/eval/examples`; do not add a skill frontmatter field just to list
  examples.

## Skill-Local QA Checklists

`qa_checklist.md` is an optional special file at the skill package root, not a
generic reference. Use it when a skill has reusable real-time checks that
should be read before execution as preflight guardrails, applied after material
changes, and applied again before claiming an output is ready.

For skills enrolled in `skill-surface-budget`, keep the checklist to the top 5
runtime guardrails. Merge overlapping preflight/final-review items and move
rare branch-specific detail to references with an explicit load condition.

```text
skill_qa_checklist(skill_package, changed_files, claim, budget?)
  -> checklist_verdicts + fixes_or_deferrals + evidence_note
```

Do not create a checklist just to mirror a todo list. The todo list says what
the invoking agent should do on first load; `qa_checklist.md` says what
failure modes to prevent while executing and how a finished or changed artifact
is checked. The eval file and QA checklist should converge over time:

```text
evals/evals.json discovers and pressures expected behavior
qa_checklist.md applies settled reusable guardrails before and after real work
```

When a skill has `qa_checklist.md`, the normal invocation pattern is:

```text
read SKILL.md
read qa_checklist.md as preflight guardrails
execute the selected workflow
apply qa_checklist.md again before completion
delegate final checklist review for material changes
```

When `evals/evals.json` changes, `skill-maintenance` should decide whether any
new `assertions` deserve promotion into `qa_checklist.md`, `SKILL.md`, a
reference, or a validator. Rare hard cases and benchmark-only examples can stay
in evals with an audit note.

## Template Versioning

`skill_template_version` tracks structural onboarding, not every migration ever
applied. A versioned skill promises that its `SKILL.md` follows the current
template spine and todo-list shape for that version.

Template source edits are release events. When
`docs/skills/templates/SKILL_TEMPLATE.md` changes, refresh the
generated release metadata and archive snapshots through the normal
skill-maintenance write path:

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

That command regenerates the skill registry and the template intelligence
artifact used by Skill OS. Do not hand-edit
`.farplane/generated/graphs/skill-template-intelligence.json`,
`.farplane/generated/graphs/skill-template-intelligence.js`, or generated
archive snapshots.

Use:

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --template-version 0.2.0
```

Add `--require-template-version` only when the rollout is intentionally ready to
fail missing or non-current skills.

Reusable method or subskill references are not skill packages and must not be
forced into the full `SKILL.md` template. When a reference under
`skills/*/references/*.md` is a reusable conditional workflow, declare:

```yaml
template_uses:
  skill-method-reference: "0.1.0"
```

Then follow `docs/skills/templates/METHOD_REFERENCE_TEMPLATE.md`. The standard
skill-maintenance check validates declared method references.

## Rollout Policy

Roll out skill-system standards from the most compound surfaces first. This is
the operational meaning of the numeric tiers:

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

Use `docs/features/FEAT-0039-behavior-correction-hardcase-metadata-and-narrow-eval-capture.md` for the full grammar and the
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

Skill-applicable features belong in first-class feature docs under
`docs/features/`, linked from `docs/systems/skill-system.md`:

```json
{"category": "skills"}
```

Use feature docs for supported optional capabilities such as eval support,
skill fixtures, template-owned metadata, or experiment support, then regenerate
`docs/features/registry.jsonl`.
Use versioned template metadata for structural `FEAT-####` adoption handles,
and use skill frontmatter only for local eval, QA checklist, and skill UI
surface paths. Use `skill_template_version` for structural template onboarding.

Do not store long applied-migration histories in skill frontmatter. If a
migration needs rollout tracking, let `skill-maintenance` compare the generated
skill inventory, template version report, local surface fields, template
metadata, and relevant feature docs.

## Installed Rendering

Source `SKILL.md` files own the first-load todo list. Installed skill packages
are rendered artifacts. After editing source skills, reinstall before judging
live Codex behavior:

```bash
bash install.sh --skills-only --skills <names> --target ~/.codex
```

Then inspect `~/.codex/skills/<name>/SKILL.md` when the user is checking the
installed experience.
