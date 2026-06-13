# Skill Best Practices

Use this as the shared standard for creating, reviewing, and maintaining
Farplane skills. This is an authoring and maintenance standard, not runtime
context for every skill invocation. Apply it to `skill-creator` and
`skill-maintenance` first; roll it out to other skills only after a
representative pass proves the shape.

Keep this file focused on skill authoring and review quality. Do not redefine
tier, source, template-version, or feature-tracking policy here; link
`docs/skills/system.md` for stable skill-system rules.

## Load Policy

Do not require normal skill users to load this whole file. A skill should be
usable from its own `SKILL.md` first-load contract unless the active task is
creating, maintaining, auditing, or reviewing skill structure.

```text
load_skill_authoring_context(task, target_skill, change_type)
  -> no_load | SKILL.md_inline_rule | anchored_section | full_doc
```

Use this file directly when:

- creating a new skill;
- changing a skill's first-load shape, references, template version, eval
  coverage, or audit record;
- reviewing skill-system work;
- changing a shared skill-system standard.

Do not load this file for ordinary use of an unrelated skill. Instead, distill
any rule needed for that skill's normal execution into that skill's `SKILL.md`.
If the rule is short and prevents common wrong behavior, duplicate the short
rule in first load and link the shared source only for deeper rationale.

Use anchored sections instead of the full file when the task is narrow:

- `#first-load-shape` for first-load contract and todo-list shape.
- `#placement-boundaries` for `SKILL.md` versus references versus docs.
- `#structure-optimization` for metric tradeoffs.
- `#advice-and-proof-routing` for advice tier, research, eval, review, QA, and
  proof routing.
- `#finish-gates-and-checklists` for choosing review, QA, eval, validator, or
  skill-local checklist gates.
- `#skill-audit-records` for audit artifacts.

If this file grows past roughly 500 lines, or any one section grows past roughly
100 lines, split the long section into a topic file under `docs/skills/` or a
skill-owned reference and keep this file as the index plus first-load authoring
standard. Shared policy stays in docs; one-skill conditional detail belongs in
that skill's references; always-needed runtime behavior belongs in the owning
`SKILL.md`.

## First-Load Shape

First-load sufficiency has priority over modular neatness. A skill can have
beautiful references and still fail if the agent cannot execute the normal path
from `SKILL.md` alone.

```text
first_load_contract(skill) -> trigger + context + signature? + todo_path + gates + proof + output
```

Put these in `SKILL.md` for every non-trivial skill:

- Trigger boundary: when to use the skill and when not to.
- Minimal context: owner docs, source-of-truth constraints, fixture assumptions,
  and surrounding system shape needed every time.
- Skill signature when composition would otherwise be implicit: inputs, outputs,
  state reads/writes, gates, routes, and failure modes.
- Phase contract when the skill owns material work whose grounding, planning,
  execution, guardrail, evidence review, or writeback phases would otherwise be
  implicit.
- Ordered todo path: default branch, important branches, proof, and final
  finish gate.
- Hard gates and stop conditions: safety, evidence, review, or setup checks that
  cannot be optional.
- Output contract: artifacts, response shape, proof paths, or handoff shape.
- Reference routing: exactly which reference to load for conditional detail.
- At least one short positive example when output quality depends on style,
  taste, persuasion, explanation, generated media, creative direction, or
  other non-deterministic judgment.

Only move material out of `SKILL.md` when the remaining first-load contract is
still executable without hidden chat context.

Frontmatter `description` is the exception to first-load richness: keep it as a
one-sentence functional routing definition capped at 220 characters. It should
help the main model decide whether to load the skill before the skill body is
visible.

Use this shape:

```text
Verb input/context into output/artifact when call-condition.
```

Good descriptions name:

- the input or starting context, such as a URL, ticket, decision, bug, prompt,
  PR, design goal, media file, or existing codebase
- the output or artifact, such as a recommendation, plan, evidence bundle,
  generated asset, rendered video, ticket, proof packet, review verdict, or
  implementation handoff
- the ownership condition that separates this skill from neighboring skills

Do not use description text for trigger phrase catalogs, examples,
model/provider maps, orchestration policy, tool instructions, long caveats,
method lists, or downstream routing chains. Put that detail in `SKILL.md` or a
reference so it is loaded only after selection.

- Put a short `## Context` section near the top of `SKILL.md` before the todo
  list when the skill depends on tier, ownership, source, or surrounding
  system shape.
- Put a compact `## Skill Signature` after `## Context` when the skill needs
  callable behavior, state reads/writes, gates, routes, failure modes, or
  composition boundaries. Follow
  [`docs/specs/self-improvement-contracts.md`](../specs/self-improvement-contracts.md)
  and do not add a verbose schema when a compact signature is enough.
- Treat the signature as a parameter contract. If the user invokes a skill
  without required inputs, the agent should resolve those inputs from files,
  state, setup workflows, or one narrow blocking question before execution.
- Include a compact budget type only when effort, search breadth,
  finish-gate depth, delegation, or external compute materially change the
  workflow. Do not add a budget schema to tiny, deterministic, or single-path
  skills.
- Put a compact `## Phase Contract` after `## Skill Signature` when the skill's
  material work needs explicit lifecycle shape:

  ```text
  phase_contract(task, bound_inputs, state)
    -> grounded_context
     + plan_or_direct_action
     + plan_review_if_material
     + execution
     + guardrail_or_eval
     + evidence_review_if_material
     + writeback
  ```

  Tier 0 phases are not skill links and not frontmatter tiers. Use Codex native
  planning/execution phases unless a named skill package owns a specific
  artifact or workflow.
- Add a compact `## Phase Boundary` when a skill may call phase-like skills
  such as `plan`, `review`, `eval`, or `research`. The boundary should say
  whether the phase stays inline or becomes an external skill call.

  ```text
  externalize_phase(parent_task, phase, child_scope, budget)
    -> skill_call | inline_phase
  ```

  External phase calls must shrink or specialize the current scope. Do not
  recurse through `plan` and `review` at the same task size.
- `## Todo List` is the first-load todo list, not a generic checklist section.
- Use visible sequential task-list items such as `- [ ] 1.`, `- [ ] 2.`, and
  `- [ ] 3.` for ordered work. Put the number after the checkbox marker so
  rich Markdown task-list views keep the sequence visible.
- Make every top-level todo an executable action with an observable result.
  Move policy, tips, and warnings to `## Gotchas`, `## Core Rules`, or nested
  verification checks.
- Use nested visible numbered task-list items for branch choices that should
  stay ordered and easy to reference.
- Use plain markdown todos such as `- [ ]` only for embedded verification or
  detail checks under a numbered todo.
- Do not use unordered prose bullets inside `## Todo List`; branch choices
  should be numbered task items, and embedded checks should be checkbox items.
- Do not put literal `FARPLANE_IMPORTANT_CHECKLIST` marker comments inside
  fenced examples; link the source template instead.
- Fold the default workflow into the numbered todo list instead of repeating it
  in a second workflow section.
- Do not add a generic `## Job` section when `## Context` plus `## Todo List`
  already state the work. Use a specific section name such as `## Contract` only
  when it adds a durable contract that is not just a repeat of the todo list.
- Put the final finish gate as the last numbered todo. The gate may be review,
  QA, eval, validator, doc-quality checklist, demo proof, human feedback, or a
  small self-check. Embedded plain todo checks are allowed under that final
  todo; avoid deep checkbox trees elsewhere.
- Move onboarding, examples, rubric detail, and long rationale to references.
- A good first-load todo list should tell the next agent what to do now, not
  teach the whole domain.

## Placement Boundaries

Use progressive disclosure, access frequency, and ownership before line count.
Length is a pressure signal, not the source of truth.

```text
place_skill_content(content, needed_now, needed_later, owner_scope, depth, line_count)
  -> SKILL.md | skill_reference | shared_doc | template | eval
```

Put content directly in `SKILL.md` when the agent needs it on first load to act
correctly now. That includes content needed for most invocations:

- Trigger and non-trigger boundaries.
- Required context that changes the first action.
- The default todo path and branch routing.
- Hard gates, stop conditions, proof requirements, and final review checks.
- Output contract and handoff shape.
- Short examples or negative examples that prevent common wrong behavior.
- Exact reference-routing hints for conditional detail.

Put content in a skill-local `references/*.md` file when it is owned by one
skill but only needed later through an explicit branch, deeper rationale,
optional detail, or rare mode:

- Onboarding walkthroughs, long examples, deep rubrics, QA checklists,
  doc-quality checklists, model maps, provider maps, command recipes, or rare
  branches.
- Detail that is loaded by one explicit todo branch.
- Material that would make `SKILL.md` harder to scan while not changing the
  default action.

Put content in `docs/*` when it is a shared standard, stable system contract, or
cross-skill policy:

- Rules used by multiple skills, templates, reviewers, validators, or agents.
- Concepts that need one canonical owner, such as tiering, file lifecycle,
  finish gates, skill structure, or harness algebra.
- Decisions that should not drift across multiple skill-local references.

Use these thresholds as review triggers:

- If a `SKILL.md` section grows past roughly 100 lines, ask whether part of it is
  branch-specific detail that belongs in a reference.
- If `SKILL.md` grows past roughly 250 lines, run a structure review; keep it
  long only when most lines are truly first-load contract.
- If one reference grows past roughly 200 lines, split by branch, provider,
  method, or artifact type.
- If the same rule appears in two or more skills, consider a shared doc or
  template owner. Keep a one-line pointer in each `SKILL.md` when the rule is
  required for first-load behavior.

Prefer duplication of a short first-load rule over hiding required behavior in a
deep reference. Prefer a shared doc over duplicated long policy. Prefer a
skill-local reference over a shared doc when only one skill owns the detail.

## Example Standard

Examples are mandatory for quality-dependent skills. A skill is
quality-dependent when the main output is judged by taste, persuasion,
explanatory clarity, brand fit, narrative structure, visual composition,
creative direction, or human preference rather than a deterministic command.

```text
example_required(skill) -> true when quality_depends_on_style_or_judgment
good_example(input, output, why_it_works?) -> repeatable_pattern
```

For those skills, include at least one positive example before trying to
optimize the checklist. The example can be:

- inline in `SKILL.md` when it is short enough to improve first-load behavior;
- a linked `references/examples.md` when the example is longer than a few
  paragraphs, includes artifacts, or has several variants;
- a `templates/*` or `prompts/*` example when the reusable asset is a prompt,
  output packet, or generated artifact shape.

A good example should show:

- the input brief or starting context;
- the final output or artifact shape;
- the style, quality bar, or "why this works" note that makes the example
  transferable;
- any boundary the agent must preserve, such as publish limits, source
  provenance, or human review.

When maintaining a quality-dependent skill with no good example, prioritize a
representative example before broad structural rewrites. Structure improves
reliability, but examples often provide the fastest lift from "valid workflow"
to "usable output."

## Structure Optimization

Use first principles before moving content between `SKILL.md`, references,
templates, evals, or review checks:

```text
maximize task_success + reliability + reusable_behavior + auditability
minimize token_cost + turn_count + duplicated_instruction + missing_context
subject to prompt_size <= limit and no quality regression
```

Key metrics:

| Metric | Direction | How to Estimate |
| --- | --- | --- |
| `first_load_sufficiency` | maximize | A new agent can execute the default path from `SKILL.md` without chat context. |
| `reference_load_precision` | maximize | References are loaded only when the current branch needs them. |
| `missing_context_rate` | minimize | The agent has to ask or rediscover info that should have been in first-load scope. |
| `noisy_context_rate` | minimize | First-load content includes optional detail irrelevant to the current branch. |
| `duplicated_instruction_count` | minimize | Same rule appears in `SKILL.md`, references, templates, docs, and examples without distinct jobs. |
| `prompt_size_tokens` | constrain/minimize | `SKILL.md` stays below the size where agents skip or flatten it. |
| `task_success_rate` | maximize | Skill eval tasks pass without weakening workflow evals. |
| `review_tas_rate` | maximize | Skill-contract and eval-quality reviews reach required TAS-A. |
| `maintenance_locality` | maximize | Future edits have one obvious owner surface. |
| `composition_clarity` | maximize | Inputs, outputs, state reads/writes, evidence, and routes are explicit. |

Placement rule:

```text
place_instruction(rule, frequency, failure_cost, token_cost)
  -> SKILL.md | reference | template | eval | review_check
```

Put a rule in `SKILL.md` when all are true:

- It is needed in most invocations.
- Missing it causes wrong behavior or extra turns.
- It is short enough to state without tutorial bloat.
- It affects routing, output shape, proof, or safety.

Put a rule in a reference when any are true:

- It is branch-specific, rare, long, or example-heavy.
- It teaches the domain rather than directing the current action.
- It is useful for authoring or review but not for every run.

Use a deliberative-advice loop only for structural changes that are expensive,
high-blast-radius, or likely to set precedent across many skills. The default
path for ordinary skill edits is still:

```text
skill_change -> review(skill-contract + eval-quality) -> TAS verdict
```

Escalate only for standard-setting changes:

```text
skill_system_standard_change
  -> deliberative-advice perspectives
  -> review(skill-contract + eval-quality + integration-readiness)
  -> eval or validator proof
```

Review routing:

```text
route_skill_structure_review(skill_change, template_age, drift, blast_radius)
  -> self_check | advise | deliberative_advice | reviewer
```

## Advice And Proof Routing

```text
route_skill_decision(decision, stakes, uncertainty, evidence_need, blast_radius)
  -> first_principles | advise | deliberative_advice | research | eval | reviewer
```

Use first-principles reasoning directly when the choice is obvious, reversible,
local to one skill, and does not set precedent. Record the reasoning in the
audit for material edits.

Use `advise` when there are real options but the decision is still local,
reversible, and cheap to correct. Good examples: one-skill reference placement,
whether to add a short example, or choosing between two equivalent output
shapes.

Use `deliberative-advice` before editing when the decision changes a shared
standard, affects Tier 1 primitives, meta skills, `skill-creator`,
`skill-maintenance`, `eval`, reviewer rubrics, templates, cross-skill policy,
or any rule likely to compound across many downstream workflows.

Use `research` before advice when the recommendation depends on external facts,
official behavior, peer patterns, source comparisons, or current local baselines
that are not already in context.

Use `eval` when the claim is behavioral, disputed, regression-prone, or cannot
be judged by file inspection. Do not use evals just to bless an obvious
structure placement.

Use the native `reviewer` lane before calling material skill-system work ready.
The reviewer judges the final artifact and evidence; it does not replace
`deliberative-advice` for important pre-edit decisions.

## Finish Gates And Checklists

Do not make `review` the default name for every finish step. A skill's last
todo should name the finish gate that matches the claim being made.

```text
finish_gate(skill, output, claim, risk)
  -> self_check | checklist | validator | eval | QA | review | demo | human_feedback
```

Use this routing:

| Claim | Finish Gate | Where Detail Belongs |
| --- | --- | --- |
| Human judgment, sufficiency, taste, readiness, or evidence quality. | `review` / reviewer lane | Review rubric or reviewer handoff. |
| User-visible workflow, browser operation, UI state, generated media playback, or demo realism. | QA checklist or `qa` / `visual-qa` / `agent-qa-test` | Skill-local `references/*-qa-checklist.md` or QA artifact contract. |
| Repeatable agent, prompt, or skill behavior. | `eval` | `eval_task.json` or eval suite artifact. |
| Deterministic file, schema, registry, link, generated state, or syntax invariant. | validator or command | Script, validator, or proof command in `SKILL.md`. |
| Documentation quality, terminology, stale sections, examples, or reader fit. | doc-quality checklist | Skill-local reference such as `references/doc-quality-checklist.md`. |
| Skill structure, first-load size, progressive disclosure, reference routing, or compaction risk. | structure checklist | `skills/skill-maintenance/references/skill-structure-checklist.md`, plus a skill-local audit for material changes. |
| Generated asset or public deliverable presentation. | demo or QA proof | Demo checklist, render artifact, screenshot, or playback proof. |
| Operator taste, ranking, or approval. | human feedback | Feedback artifact, Telegram request, or explicit approval record. |
| Tiny deterministic edit. | self-check | One inline final todo or command. |

First-load `SKILL.md` should usually say which gate to run and when to load the
detail. Keep the detailed checklist in a reference when it is only needed after
the draft, implementation, render, or evidence bundle exists.

```text
place_finish_checklist(checklist, needed_before_execution, owner_scope)
  -> SKILL.md when needed_before_execution
  -> references/*-checklist.md when owned_by_one_skill
  -> docs/* when shared_across_many_skills
```

Add a skill-local QA checklist when the skill repeatedly produces or verifies a
user-visible artifact and the checks are domain-specific. Examples:

- frontend and UI skills: layout, console errors, responsive behavior,
  accessibility, primary workflow, screenshots, and visual regressions.
- media skills: duration, resolution, playback, audio sync, captions, artifact
  paths, and platform constraints.
- content/social skills: platform fit, required variants, links, rendered
  previews, and copy/asset consistency.
- agent-testing skills: case coverage, tester evidence, evidence-review
  critique, rerun policy, and final proof bundle.

For skill creation or material skill restructuring, load and run
`skills/skill-maintenance/references/skill-structure-checklist.md`. Its key
threshold is:

```text
place_skill_detail(detail)
  -> SKILL.md when defer_loading_risk > context_rot_risk + compaction_loss_risk
  -> reference when defer_loading_risk <= context_rot_risk + compaction_loss_risk
```

This treats oversized first-load context as a reliability risk, not just a style
issue. If loading everything early increases context rot or forces compaction
before the task state stabilizes, keep a precise first-load pointer and defer
the branch detail to a reference.

Treat each checklist item as a violation scan over the actual changed files,
not as a passive reminder. Record any violation in the skill-local audit or
final proof notes, then fix or explicitly defer it. Use the checklist's
subagent prompt when independent structure review is useful.

Do not put long QA checklists directly in `## Todo List` unless those checks
are needed before execution. Prefer a compact final todo:

```text
- [ ] Finalize with the skill-local QA checklist when the artifact exists.
```

Then link the reference from `## Reference Map`.

Always review skill creation and maintenance against the structure metrics. Vary
the review depth:

- Use a direct self-check for tiny mechanical edits that do not change trigger,
  routing, proof, references, or first-load behavior.
- Use `advise` for recent skills that already match the current template and
  need a normal placement decision.
- Default to `deliberative-advice` for structural changes to Tier 1 primitives,
  meta skills, `skill-creator`, `skill-maintenance`, `eval`, cross-skill
  standards, or any skill whose behavior compounds across many downstream
  workflows.
- Also use `deliberative-advice` when the skill is old, far from the current
  template, high-traffic, cross-skill, precedent-setting, or likely to move
  important rules between `SKILL.md`, references, templates, evals, and review
  checks.
- Use the native `reviewer` lane for material skill-system changes before
  calling them ready. The reviewer should explicitly judge
  `first_load_sufficiency`, `reference_load_precision`, `missing_context_rate`,
  `noisy_context_rate`, `duplicated_instruction_count`, `prompt_size_tokens`,
  `task_success_rate`, `review_tas_rate`, `maintenance_locality`, and
  `composition_clarity`.
- Do not assert `task_success_rate` or `review_tas_rate` from file inspection
  alone. Those need eval run artifacts, reviewer receipts, or explicit evidence
  gaps.

## Skill Audit Records

Use binary rubric outcomes instead of health scores. Numeric scores hide the
reason for disagreement and are too easy to overfit. A skill audit should say
which checks passed, which failed, what evidence exists, and what changed before
and after the edit.

```text
audit_skill_structure(skill, change, reasoning, evidence?) -> audit_record + pass_fail_rubric + followups
```

For material skill creation or maintenance, write an audit record under the
skill package:

```text
skills/<skill-name>/audits/YYYY-MM-DD-<short-change>.md
```

Material means the change affects trigger behavior, first-load content,
reference placement, routing, proof gates, templates, eval tasks, reviewer
rubrics, Tier 1/meta behavior, or any cross-skill standard. Tiny metadata,
typo, link, or formatting edits can skip the audit record when they do not
change behavior.

Each audit record should include YAML front matter and a binary checklist:

- `skill`, `date`, `change_type`, `owner`, and `status`.
- `before_ref` and `after_ref` when there are commits, branches, or artifact
  paths to compare.
- `review_route`: `self_check`, `advise`, `deliberative_advice`, or `reviewer`.
- `reasoning_basis`: first-principles review, `advise`, `deliberative_advice`,
  reviewer receipt, eval run, or a combination.
- `proof_artifacts`: commands, eval artifact paths, reviewer receipts, or
  explicit evidence gaps.
- `eval_required`: `yes` or `no`, with a short reason.
- `rubric`: pass/fail/unknown rows for the structure metrics.
- `before_behavior`, `after_behavior`, and `followups`.

Do not put `health_score` in `SKILL.md` front matter. Do not add `last_edited`
when git history already carries that fact. If a freshness signal is needed,
derive it from git history and the newest audit record rather than duplicating
state in every skill.

Use `unknown` rather than guessing for evidence-backed checks such as
`task_success_rate` and `review_tas_rate` when no eval run or reviewer receipt
exists.

First-principles reasoning is the default review engine for skill structure.
Use it to inspect where instructions belong, whether the first-load path is
executable, whether references are precise, and whether the change compounds
cleanly through other skills.

```text
improve_skill_structure(skill_change)
  -> first_principles_review
  -> advise_or_deliberative_advice_when_high_leverage
  -> targeted_eval_or_reviewer_receipt_when_needed
  -> audit_record
```

Run evals, variant tournaments, or reviewer receipts when reasoning alone cannot
settle the choice, when reviewers disagree, when the change is a regression
guard, or when the final claim depends on measured behavior. Do not require
benchmarks for every skill edit, and do not claim measured improvement without
proof.

## Main File Versus References

- `SKILL.md` owns trigger conditions, job, branch routing, hard gates, and proof
  obligations.
- `SKILL.md` owns a short skill signature when the skill's callable behavior,
  state, artifact variables, eval boundaries, or downstream composition would
  otherwise stay implicit.
- Paths inside a skill are relative to that skill package by default. Use
  `scripts/foo.py` for nearby helper scripts, `references/foo.md` for nearby
  references, and sibling paths such as `../skill-maintenance/scripts/foo.py`
  when calling another skill package. Use repo-root paths only when the command
  truly must be run from the repository root.
- References own conditional detail: onboarding, examples, templates, long
  rubrics, model maps, and rare-path recipes.
- Skill-local evals own focused behavioral regression tasks for that skill.
  Use `eval_task.json` at the skill package root when the task proves the
  skill's own contract; use cross-skill examples or `.farplane/evals` when the
  behavior belongs to the broader harness.
- If a reference must be read on every invocation, promote the needed rule into
  `SKILL.md`.
- Do not copy the same instruction into `SKILL.md`, references, templates, and
  README-style docs unless each surface has a distinct job.

## Actor Prompts Versus Skill Contracts

- Actor prompts such as `agents/*.toml` own identity, responsibility,
  delegation boundaries, tool use, durable task loading, artifact writeback,
  and anti-recursion rules.
- Material actor prompts should expect a durable `context_ref` such as a
  ticket, spec, decision packet, evidence artifact, or handoff file when prior
  discussion, options, constraints, or proof targets matter.
- Skills own reusable domain contracts: trigger boundaries, rubric or workflow
  shape, templates, hard gates, and proof expectations.
- Do not put subagent spawning, caller routing, or actor identity inside a
  reusable skill unless that skill's primary job is orchestration.
- When a skill is equipped to an agent, the skill should remain usable as a
  lower-level contract without causing the agent to delegate itself.

## Repeatability

Repeatability is the core quality bar for skills.

A skill is repeatable when another agent can use it from repo files alone
without hidden chat context, rediscovering prior decisions, or depending on the
author's memory.

Check repeatability by asking:

- Can another agent identify when to use the skill from its description?
- Can it execute the first-load todo list without reading every reference?
- Are scripts, commands, paths, artifacts, and validation steps explicit?
- Are setup/onboarding paths separated from the normal run path?
- Are the skill's inputs, outputs, write-set artifacts, evidence, and
  downstream handoffs explicit enough to compose with other skills?
- Does the skill avoid verbose duplication that would drift later?

## On-Contact Upgrade Check

When touching a skill that has not been onboarded to the current standard, do
the smallest useful upgrade in the same pass:

- Check whether the first-load `## Todo List` is ordered, executable, and
  marker-delimited.
- Add or tighten `## Skill Signature` when it would clarify real process
  inputs, outputs, state, files, evidence, gates, routes, or composition.
- Move optional detail, rare branches, examples, long rubrics, and model maps
  into references.
- Remove duplicate workflow prose when the todo list already carries the
  default path.
- Confirm proof commands, output artifacts, or explicit blockers are named.
- Set or keep `skill_template_version` only after the actual `SKILL.md`
  structure has been verified against the template.
- Reinstall and inspect the live installed skill when visible Codex behavior is
  part of the claim.

## Finish Gate

Before calling skill work complete, run the finish gate that matches the
artifact and claim. For ordinary skill-system work, the default gate is still a
review pass that checks:

- concise first-load todo list
- branch-aware workflow shape
- references used only for conditional detail
- no duplicated instructions across surfaces
- explicit proof commands and artifacts
- repeatability from files alone

For nontrivial skill-system work, delegate review to the native `reviewer` subagent
when one is available. The calling skill owns rubric routing: pass a reviewer
handoff with the active ticket or task artifact, changed skill files, evidence
artifacts, review focus, rubric families, required TAS gates, hard gates, and
expected output path. Use
`docs/review/rubrics/reviewer-handoff.md` for the template.

For skill-system review, the usual caller-declared families are `skill-contract`,
`integration-readiness`, and `evidence-quality`. Add task-specific hard gates
for repeatability, duplicated first-load logic, actor-prompt versus
skill-contract boundaries, and explicit proof commands. Self-review is
acceptable for tiny mechanical edits, but it is weaker at catching duplicated
instructions, hidden assumptions, and vague "sounds good" skill contracts.

For large skill-system rollouts, prove the pattern on a representative sample
before editing the whole registry.
