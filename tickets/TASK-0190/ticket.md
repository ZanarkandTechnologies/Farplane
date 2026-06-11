---
ticket_id: TASK-0190
title: define compact contracts for self-improvement skills
phase: planning
status: review
owner: codex
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: true
requires_qa: false
requires_demo: false
created_at: 2026-06-10T00:00:00+08:00
updated_at: 2026-06-10T22:07:31+08:00
next_action: review the systems-architecture council recommendation, then approve the compact self-improvement contract taxonomy before setting status: building
last_verification: skill system check, graph generation, eval example JSON parse, ticket metadata check, and self-review all passed on 2026-06-10
---

# TASK-0190: define compact contracts for self-improvement skills

## Summary

Define a compact contract notation for Farplane's meta and self-improvement
skills so they compose like ticket-sized functions without pretending every
English field needs a rigid TypeScript interface. This fixes the confusion
where skill tiers, workflow order, proof ownership, and recovery/capture naming
became overloaded during planning.

The decisive path is to keep Tier 1/2/3 as reuse and maintenance priority, then
add a separate contract block that names each skill's inputs, outputs, state
effects, gates, routes, failure modes, and optional examples.

## Systems Architecture Council Recommendation

Recommendation: keep the self-improvement system as a small routed pipeline,
not a new skill taxonomy. The stable breakdown should be:

```text
optimize_harness(observed_behavior, expected_behavior?, metric?, evidence?) -> AcceptedChange | ExperimentPlan | BlockedReport
gap_analysis(target, expected_behavior?, evidence?) -> GapReport + NextOwner
harness_place(gap_or_request, evidence?) -> PlacementDecision
eval(task_intent, harness?, target_root?, mode?) -> EvalCase? + RunSummary? + NextFix
self_improve_experiment(target_skill_or_surface, metric, search_space?, eval_suite?) -> BestCandidate + ExperimentLog + PromotionRecommendation
maintain_skills(accepted_change, targets?, rollout_scope?) -> AppliedChange + RegistryChecks
review_change(change_or_evidence, rubric_requirements?) -> ReviewReceipt
```

Target system:

- `optimize-harness` is the public entry point for "fix this harness behavior"
  when the operator wants the end-to-end loop handled.
- `gap-analysis` is the standalone diagnosis workflow for current-versus-
  expected behavior across skills, harness workflows, UI/product surfaces,
  docs, and code.
- `harness-advisor` remains the placement decision skill for "where should this
  improvement live?"
- `eval` designs and runs durable proof surfaces.
- `agent-behavior-test` and `agent-qa-test` are proof strategies, not parallel
  source-of-truth registries.
- `self-improve` runs metric-driven experiments across a target skill, prompt,
  or harness surface. It searches candidate changes and compares them against a
  baseline; it does not simply apply a requested implementation plan.
- `skill-maintenance` promotes accepted skill changes, template rollouts,
  registry refreshes, and source/installed-skill hygiene.
- `review` validates proof quality and completion claims.
- Known corrected behavior should become an eval immediately when the expected
  behavior is clear.
- `hardcase` is an `eval` mode or metadata flag for unusually difficult,
  reusable, or potentially saleable benchmark samples. The ideal destination of
  a hardcase is still a runnable eval, not a separate capture backlog.
- `LESSONS.md` and `TROUBLES.md` remain direct docs destinations for explicit
  "log this" requests; they are not part of the core self-improvement skill
  taxonomy.

Naming guidance:

- Use `optimize-harness` when the operator wants the full diagnose, place,
  prove, change, and review loop.
- Keep `harness-advisor` as the public placement decision skill.
- Use `gap-analysis` when current behavior, expected behavior, owner surface,
  or proof route is fuzzy.
- Keep `eval` as the repeatable proof definition and runner for clean-room
  behavioral tasks.
- Keep `review` as the judgment gate for proof quality, integration readiness,
  and completion claims.
- Keep `self-improve` as the measured improvement workspace for a target skill,
  prompt, or harness surface after proof exists or the proof gap is explicit.
- Keep `skill-maintenance` as the promotion/writeback path for accepted skill
  source changes, registry refreshes, and skill-system checks.
- Remove `repent` from the active skill taxonomy. Corrected behavior routes to
  `eval`; rich hard episodes route to `eval` with hardcase metadata; plain
  lessons/troubles route to docs only when explicitly requested.

Routes:

```text
operator correction
  -> direct same-scope fix when safe
  -> eval when expected behavior is clear
  -> eval hardcase mode when the sample is unusually hard, rich, reusable, or saleable
  -> direct LESSONS.md/TROUBLES.md logging only when explicitly requested

harness improvement request
  -> optimize-harness when full loop ownership is desired
  -> gap-analysis when the gap is fuzzy
  -> harness-advisor for placement
  -> eval / agent-behavior-test / agent-qa-test for proof
  -> self-improve or direct implementation
  -> skill-maintenance for accepted skill writeback
  -> review for material pass/hold
```

Agent testing fit:

- `agent-behavior-test(claim, prompt, harness?) -> BehaviorTrace` is the cheap
  isolated child-agent probe. Use it when the proof question is narrow, such as
  "does a named skill get read before use?"
- `agent-qa-test(target_behavior, acceptance_criteria) -> QAReport` is the
  adversarial readiness lane. Use it when evidence quality itself needs attack,
  multiple cases, reruns, or tester/evidence-review separation.
- `eval` remains the canonical durable suite. Agent-test artifacts can seed or
  validate eval rows; they should not become a parallel proof registry.

Tradeoff accepted: this removes a neat-sounding capture skill from the core
loop. The system becomes less ceremonious: clear expected behavior becomes eval
coverage now; ambiguous pain becomes a gap report or explicit docs log; rich
benchmark material becomes eval hardcase metadata.

New-skill promotion rule:

Do not create a public skill for a lifecycle state until it has:

- three or more real examples where it was useful independently of its parent
  workflow
- a distinct input contract and output artifact
- a proof path such as eval, validator, or review rubric
- evidence that keeping it as a method/todo caused repeated misses or
  coordination cost

Until then:

- fold `normalize_gap` into `harness-advisor`
- fold `hardcase` into `eval` as mode/metadata
- keep `LESSONS.md` and `TROUBLES.md` as direct docs logging destinations, not
  skill taxonomy nodes
- fold skill-template rollout mechanics into `skill-maintenance`
- fold external-proposal classification into `harness-advisor`, then route to
  `harness-scout`, `best-of-worlds`, `eval`, `self-improve`, or a ticket only
  when the proposal needs that owner

## Scope

- In:
  - one canonical spec for compact skill/function contracts
  - a self-improvement role map that separates tier from call graph
  - preview contract blocks for the key meta/self-improvement skills
  - guidance for when `eval`, `review`, `skill-maintenance`, `harness-advisor`,
    existing `gap-analysis`, eval hardcase mode, and future diagnosis
    workflows are called
  - a small rollout plan for adding the notation to source skills without a
    broad migration
- Out:
  - no new Tier 4 taxonomy
  - no TypeScript-like schema for every string field
  - no automatic parser or validator in the first slice
  - no new correction-capture, hardcase-capture, or repent replacement skill in this slice
  - no bulk rewrite of every skill package

## Plan

- `Change:` add a canonical compact contract notation and apply it first to the
  self-improvement skill cluster as a preview before changing skill bodies.
- `Why:` the current mental model overloads Tier 1/2/3 as both maintenance
  priority and call graph. The result is confusion over whether
  `harness-advisor`, `eval`, `self-improve`, `skill-maintenance`,
  `agent-qa-test`, and `review` own diagnosis, placement, proof,
  experimentation, promotion, or validation.
- `First-principles basis:`
  - `Objective:` make self-improvement workflows composable and reviewable.
  - `User/system need:` when the operator spots bad behavior, Farplane should
    convert that into diagnosis, placement, proof, change, and review without
    fuzzy skill ownership.
  - `Root cause:` skill tiers explain reuse and maintenance priority, but not
    workflow function, artifact flow, state mutation, or proof gates.
  - `Assumptions:` most skill inputs remain natural language, so strict
    string-heavy schemas create fake precision; artifact flow and gates are the
    useful typed boundary.
  - `First viable slice:` one doc plus preview contracts for the core
    self-improvement skills, then update a small set of source `SKILL.md`
    files only after review.
  - `Proof/falsification:` if the preview contracts make a representative
    "bad behavior -> fix" path unambiguous without adding verbose ceremony, the
    notation is useful. If it creates decorative fields that are not used by
    routing, testing, review, or maintenance, cut it back.
  - `Tradeoff accepted:` preserve lightweight human-readable contracts before
    attempting parser-enforced schemas.
  - `Non-goals:` no recursive optimizer, no hidden background repair loop, no
    global prompt bloat, and no broad automated migration.
- `Before -> After:`
  - Before: self-improvement skills are described mostly by prose checklists;
    tiers are mistakenly read as an execution stack; correction capture,
    hardcase capture, eval seeds, and docs logging are mixed together as if
    they are one workflow.
  - After: each meta skill has a compact function contract with declared
    inputs, outputs, state effects, gates, routes, and known failure modes.
    Tiers remain maintenance priority; contracts express composition; hardcase
    samples live under eval semantics.
- `Touch:`
  - `docs/specs/self-improvement-contracts.md`
  - `docs/skills/system.md`
  - `skills/harness-advisor/SKILL.md`
  - `skills/eval/SKILL.md`
  - `skills/self-improve/SKILL.md`
  - `skills/skill-maintenance/SKILL.md`
  - `skills/review/SKILL.md`
  - optional: `skills/agent-qa-test/SKILL.md`,
    `skills/agent-behavior-test/SKILL.md`, `skills/goal-advisor/SKILL.md`
- `Inspect:`
  - `docs/skills/system.md`
  - `docs/skills/best-practices.md`
  - `docs/specs/harness-engineering-doctrine.md`
  - `docs/specs/self-improvement-contracts.md`
  - `skills/harness-advisor/SKILL.md`
  - `skills/eval/references/eval-best-practices.md`
  - `skills/self-improve/references/skill-evals.md`
  - `tickets/README.md`
- `Signature delta:`
  - `self_improvement_contract / name(inputs...) -> outputs`
  - `self_improvement_contract / state: reads(...); writes(...); remembers(...)`
  - `self_improvement_contract / gates: proof/check/review requirements`
  - `self_improvement_contract / routes: allowed next skills or artifacts`
  - `self_improvement_contract / fails: known bad behavior`
  - `self_improvement_contract / examples: optional calibration cases`
- `Type Sketch:`
  - `ContractBlock`: compact Markdown block with `signature`, `state`,
    `gates`, `routes`, `fails`, and optional `examples`.
  - `Incident`: observed bad behavior, correction, or expected behavior request
    expressed in normal text.
  - `Gap`: named delta between current/observed behavior and expected behavior.
  - `PlacementDecision`: owning surface, rejected surfaces, proof surface,
    implementation owner, and next action.
  - `ProofPlan`: eval, validator, review, agent behavior test, agent QA test,
    or manual evidence plan.
  - `ChangeSet`: skill/doc/hook/ticket/prompt changes accepted for writeback.
  - `ReviewReceipt`: pass/hold/revise judgment against proof gates.
  - `EvalCase`: runnable regression or benchmark sample, optionally marked as a
    hardcase.
- `Typed flow example:`
  1. Operator says: "Harness advisor, fix this: when I name a skill, Codex
     answers without reading it."
  2. `normalize_gap(incident, expected?) -> gap` normalizes the issue inside
     `harness-advisor`, or `skill_gap_analysis(skill, intended_behavior) ->
     GapReport + next_owner` when a specific skill contract is under question.
  3. `harness_place(gap_or_request) -> placement_decision` chooses owner and
     proof.
  4. `design_proof(placement_decision) -> proof_plan` creates the eval or
     validator path.
  5. If the change path is exploratory, `self_improve_experiment(target, metric,
     search_space?) -> best_candidate + experiment_log + promotion_recommendation`
     benchmarks candidate changes against the proof plan.
  6. If the change path is direct and obvious, the implementation owner drafts
     the bounded change through `skill-maintenance`, `impl`, or the owning
     ticket workflow.
  7. `maintain_skills(accepted_change) -> applied_change + checks` promotes
     accepted skill changes and updates generated skill surfaces.
  8. `review_change(applied_change, evidence) -> review_receipt` accepts,
     holds, or revises.
  9. Optional: `capture_eval_case(behavior_case, hardcase?) -> eval_case`
     preserves the contrast as runnable proof when recurrence matters.
- `Execution steps:`
  1. Write `docs/specs/self-improvement-contracts.md` with the compact contract
     grammar and role map.
  2. Add the preview contracts below to the spec.
  3. Update `docs/skills/system.md` to state that tiers are not the workflow
     call graph.
  4. Update the smallest relevant source skills with contract blocks after the
     spec is reviewed.
  5. Run `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
  6. Add or update at least one eval/check that catches contract drift for a
     high-leverage self-improvement skill.
  7. Send the final skill-system change through `review`.
- `Recommendation:` do not add Tier 4. Add `role`/contract notation and keep
  call graphs explicit through `routes`.
- `Options considered:`
  - Add Tier 4 for meta workflows: rejected because it makes taxonomy fight the
    call graph and will likely create new "Tier 3 vs Tier 4" arguments.
  - Replace tiers with function composition only: rejected because tiers still
    help prioritize which skills must remain sharp and current.
  - Keep tiers and add compact contracts: recommended because it preserves
    maintenance priority while making composition explicit.
- `Blast radius:` skill-system docs, meta-skill checklists, generated skill
  registry expectations, future self-improvement tickets, and review rubrics
  for skill changes.
- `Risks:`
  - contract blocks become decorative and drift from actual skill behavior
  - the notation grows into a second programming language
  - hardcase metadata becomes a dumping ground for vague examples instead of
    runnable evals
  - eval routing remains ambiguous if `proof` ownership is not named in each
    contract

## Preview Contract Blocks

```md
normalize_gap(signal, expected?, evidence?) -> gap
state: reads(evidence?, ticket?, skill?, transcript_excerpt?); writes(none)
gates: evidence:linked; ambiguity:explicit
routes: harness-advisor | gap-analysis | eval | direct-fix | ask
fails: invents expected behavior without evidence; turns ambiguity into architecture; hides missing evidence
examples:
- "it ignored the named skill; it should read SKILL.md first" -> gap: skill invocation miss
```

```md
gap_analysis(target, expected_behavior?, evidence?) -> GapReport + next_owner
state: reads(target_artifact, relevant_context, supplied_evidence); writes(gap_report?)
gates: current_state:grounded; expected_behavior:explicit_or_marked_unknown; owner_surface:named
routes: harness-advisor | eval | self-improve | skill-maintenance | impl-plan | functional-ui | research:gap | direct-fix
fails: jumps to a fix before naming the gap; confuses symptom with owner; invents expected behavior; creates duplicate skills
examples:
- capture workflow is overloaded -> gap report routes clear behavior to eval and explicit docs logs to LESSONS/TROUBLES
```

```md
harness_place(gap_or_request) -> placement_decision
state: reads(harness_doctrine, feature_registry, skill_registry, relevant_surfaces); writes(ticket? handoff?)
gates: review for material placement; evidence:grounded
routes: gap-analysis | eval | self-improve | skill-maintenance | impl-plan | spec-to-ticket | direct-answer
fails: defaults to AGENTS.md; creates new skill before checking registry; recommends hooks for judgment-heavy work
examples:
- skill invocation miss -> proof: eval or agent-behavior-test; owner: skill contract or global skill-loading rule
```

```md
design_proof(expected_behavior_or_placement) -> proof_plan
state: reads(eval_best_practices, existing_evals, fixtures?); writes(eval_case? validator? proof_artifact?)
gates: baseline before mutation when improving behavior; proof matches failure mode
routes: self-improve | skill-maintenance | agent-behavior-test | agent-qa-test | review
fails: adds wording-only eval; tests implementation detail instead of behavior; skips baseline for skill change
examples:
- expected skill invocation behavior -> eval case that fails when named SKILL.md is not read
- rich corrected episode with reusable benchmark value -> eval case marked `hardcase`
```

```md
self_improve_experiment(target_skill_or_surface, metric, search_space?, eval_suite?) -> best_candidate + experiment_log + promotion_recommendation
state: reads(target, references, scripts, self-improve context, evals, prior results, failure analysis, candidates); writes(experiments, candidate_variants, scores, lessons?)
gates: baseline:recorded; metric:honest; candidate:beats_baseline; promotion:reviewed
routes: skill-maintenance | review | goal-advisor | no-change
fails: directly edits source without experiment loop; optimizes vague taste; promotes candidate without benchmark; treats one lucky run as durable improvement
examples:
- improve `advise` for direct recommendation -> compare candidate checklist/prompts against eval suite and recommend promotion only if the metric improves
```

```md
maintain_skills(change_set) -> applied_change + registry_checks
state: reads(skill_system_docs, target_skills, registry); writes(SKILL.md, references?, docs/skills/registry.jsonl)
gates: check_skills:pass; source_ownership:preserved; eval_or_exemption:present
routes: review | install-skills | close-ticket
fails: patches installed skill as source of truth; bulk-edits without prototype; updates registry by hand
examples:
- accepted Tier 1 contract update -> source SKILL.md edit + regenerated registry + skill check
```

```md
review_change(change, evidence) -> review_receipt
state: reads(ticket, changed_files, proof_artifacts, rubrics); writes(review_artifact?)
gates: required_tas met; hard_gates pass; evidence fresh
routes: revise | accept | block | close-ticket
fails: self-approves material change; treats stale evidence as pass; ignores caller-declared rubrics
examples:
- skill contract change -> review checks evidence-quality, skill-contract, integration-readiness
```

```md
capture_eval_case(behavior_case, hardcase?) -> eval_case
state: reads(expected_behavior, current_or_negative_example?, evidence, privacy_constraints); writes(eval_suite)
gates: expected_behavior:clear; privacy:redacted; runnable_or_marked_fixture_gap
routes: eval | self-improve | review
fails: delays obvious regression coverage; stores raw private transcript; marks hardcase without benchmark value
examples:
- "this should never happen again" after fixed miss -> runnable eval case
- rare multi-step failure with resale/benchmark value -> eval case with `hardcase: true`
```

```md
advise_goal_use(intent, proof_requirements?) -> native_goal_contract
state: reads(ticket?, proof_contract?, target_skill?, self-improve context?); writes(goal_prompt)
gates: evidence:not_proxy_only; blocked_stop:explicit; boundaries:clear
routes: native-goal | work | self-improve | agent-qa-test | review
fails: emits "improve X" without verification; creates a separate loop runner; asks broad questions already answered by ticket
examples:
- skill improvement request -> /goal that reads target skill, evals, latest results, and uses skill-maintenance for writeback
```

```md
agent_behavior_probe(claim, prompt, harness?) -> behavior_trace
state: reads(prompt, skill?, fixture?); writes(run_log, final_output, evidence_bundle)
gates: isolated_child_run:captured; claim:bounded
routes: eval | harness-advisor | review
fails: tests broad vibes; omits logs; lets child infer hidden context
examples:
- named skill invocation claim -> child run showing whether SKILL.md was loaded
```

```md
agent_qa_challenge(target_behavior, acceptance_criteria) -> qa_report
state: reads(ticket, target_artifact, acceptance_criteria); writes(qa_report, evidence)
gates: adversarial_cases:covered; evidence:linked; rerun_policy:clear
routes: revise | review | close-ticket
fails: repeats implementer proof; lacks adversarial cases; treats subjective impression as evidence
examples:
- human-like QA for Farplane UI -> report with realistic user paths and failure evidence
```

## Acceptance Criteria

- [x] A canonical `docs/specs/self-improvement-contracts.md` exists and defines
  the compact contract notation.
- [x] The spec includes contract blocks for the stable core workflow:
  `optimize_harness`, `gap_analysis`, `harness_place`, `eval`,
  `self_improve_experiment`, `maintain_skills`, and `review_change`.
- [x] The spec states that hardcase is an eval mode/metadata flag, not a
  separate skill or capture backlog.
- [x] The spec states that explicit lesson/trouble logging is a direct docs
  action unless a future repeated workflow proves it needs a skill.
- [x] The spec states that `self-improve` is metric-driven experimentation over
  candidate changes, not direct promotion/writeback.
- [x] The ticket includes the new-skill promotion rule so lifecycle states stay as
  methods/todo items until repeated independent use justifies a public skill.
- [x] `docs/skills/system.md` links or summarizes the skill signature
  distinction.
- [x] The `repent` skill package is removed from the active source tree.
- [x] `gap-analysis` and `optimize-harness` source skill packages exist.
- [x] At least one source skill in the self-improvement cluster is updated with
  the approved contract block pattern.
- [x] Skill-system validation passes after the change.
- [x] A review pass judges whether the notation reduces ambiguity without
  adding decorative fields.

## Verification

- `Tests:` `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  with `--template-version 0.2.0`,
  `python3 skills/skill-maintenance/scripts/generate_skill_graph.py`, and
  `python3 tickets/scripts/check_ticket_metadata.py`
- `Manual checks:` inspect the self-improvement spec and updated skill bodies
  for concise contracts, non-decorative fields, and clear routes.
- `Evidence required:` command output for skill checks and ticket metadata,
  plus a review artifact covering `skill-contract`, `evidence-quality`, and
  `integration-readiness`.

## Proof Contract

- `Metrics:`
  - `Primary metric:` pass/fail
  - `Direction:` pass/fail
  - `Verify:` `python3 skills/skill-maintenance/scripts/check_skills.py --write`
    and `python3 tickets/scripts/check_ticket_metadata.py`
  - `Guard:` review confirms contract blocks are used by routing, testing,
    review, or maintenance rather than decorative prose
  - `Min acceptable result:` both commands pass and review is TAS-A for
    `skill-contract` plus TAS-A for `evidence-quality`
  - `Autoresearch warranted:` no
  - `Autoresearch session:` none
- `Review Rubrics:`
  - `skill-contract: TAS-A`
  - `evidence-quality: TAS-A`
  - `integration-readiness: TAS-A`
  - hard gate: no new Tier 4 taxonomy unless separately approved
  - hard gate: no TypeScript-like field schema for every string value
- `Reviewer Handoff:`
  - `task_path:` `tickets/TASK-0190/ticket.md`
  - `review_focus:` skill-change, prompt-change, docs, evidence
  - `changed_files:` expected docs and selected source skill files listed in
    `Plan / Touch`
  - `evidence:` skill check output, ticket metadata output, and contract spec
  - `rubric_families:` skill-contract, evidence-quality,
    integration-readiness
  - `required_tas:` skill-contract TAS-A; evidence-quality TAS-A;
    integration-readiness TAS-A
  - `hard_gates:` no decorative fields; no broad migration; no hidden loop
    runner; no root-prompt bloat
  - `expected_output:` `tickets/TASK-0190/artifacts/review/2026-06-10-self-improvement-signature-review.md`
- `Required Evidence:`
  - `tickets/TASK-0190/artifacts/check-skills.txt`
  - `tickets/TASK-0190/artifacts/generate-skill-graph.txt`
  - `tickets/TASK-0190/artifacts/check-ticket-metadata.txt`
  - `tickets/TASK-0190/artifacts/review/2026-06-10-self-improvement-signature-review.md`

## Autonomy Readiness

- `Human inputs/assets:` operator approved compact notation, `repent` removal,
  `gap-analysis`, `optimize-harness`, signatures, and hardcase-as-eval mode.
- `Credentials / external access:` none.
- `Compute/runtime needs:` local repo checks only.
- `Tooling gaps:` no parser/validator for contract blocks in this first slice.
- `QA risks:` risk is mostly conceptual drift; use review rather than browser
  QA.
- `Human gates:` satisfied for this slice.
- `Agent decision boundaries:` agent may draft docs and source-skill signature
  blocks after approval; agent should not migrate all skills without separate
  explicit scope.

## Execution Profile Hints

- `Likely size:` normal
- `Goal recommendation:` recommend
- `Compute hint:` local_shared
- `Planning hint:` impl_plan
- `Proof weight:` review
- `Batchability:` single-ticket
- `Batch reason:` central taxonomy/spec change should land coherently before
  skill-specific rollout tickets.

## Refs

- `docs/skills/system.md`
- `docs/specs/harness-engineering-doctrine.md`
- `docs/specs/self-improvement-contracts.md`
- `skills/harness-advisor/SKILL.md`
- `skills/eval/SKILL.md`
- `skills/self-improve/SKILL.md`
- `skills/skill-maintenance/SKILL.md`
- `skills/review/SKILL.md`
- `tickets/README.md`

## Evidence

- Ticket creation evidence: this file.

## Blockers

- `repent` removal approved by operator in this pass; surviving eval-related
  behavior folds into `eval` hardcase mode and high-priority regression capture.
