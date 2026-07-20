---
template_id: ticket-template
template_version: "0.2.3"
feature_refs:
  - FEAT-0007
  - FEAT-0008
  - FEAT-0039
ticket_id: TASK-0396
title: Require lean convergence for coding implementation plans
status: awaiting_review
priority: high
created_at: 2026-07-20T18:57:08+08:00
updated_at: 2026-07-21T02:42:00+08:00
---

# TASK-0396: Require lean convergence for coding implementation plans

## Summary

Make leanness an evidenced approval condition for the one coding plan stored in
`ticket.md`. `impl-plan` must challenge additions subtractively, an adversarial
reviewer must reach TAS-A, and a final clean review pass must find no material
reduction before the plan may call itself lean or approval-ready.

For a material Farplane harness delta whose owner is unclear or whose proposal
adds or moves a durable harness surface, `impl-plan` first composes the existing
`harness-advisor` to choose the smallest owner and reject alternatives. Reuse
the existing implementation-plan rubric, reviewer lane, and Goal Advisor
optimization route. Do not create a planner ensemble, ten random rollouts, a
new score, a new plan artifact, or a Goal per metric.

## Scope

- `In:`
  - Strengthen the existing implementation-plan rubric so `bloatability` and
    `modularity` require subtractive evidence and a fixed-point receipt rather
    than a self-declared minimality sentence.
  - Make `impl-plan` compare the current plan against the status quo and an
    existing-owner reuse/merge/derive counterplan before accepting new fields,
    files, functions, modules, parameters, services, or routes.
  - Before drafting a material Farplane harness change, conditionally invoke
    the existing `harness-advisor` when ownership is unresolved or a new/moved
    policy, template, skill, agent, hook, ticket, doc, validator, or durable
    state surface is proposed. Reuse an already-reviewed placement receipt.
  - Keep the compact placement decision and rejected surfaces inside existing
    ticket `Notes` or its subtractive receipt; do not add a field or sidecar.
  - Require an adversarial native reviewer for material plan approval; repair
    valid findings until TAS-A and then require one clean no-material-delta
    pass.
  - When the same-artifact loop needs continuation, route to the existing Goal
    Advisor optimization shape with review as feedback and a bounded stop/block
    contract.
  - Add focused reducible and irreducible hardcases, including a sanitized
    version of the observed field/feature backtracking failure.
  - Keep `ticket.md` canonical; diagram, review, Goal, progress, and proof files
    remain linked evidence/control companions.
- `Out:`
  - No `content-impl-plan` change; its content-production artifact requires a
    separate ticket after this shared coding-plan contract proves useful.
  - No `harness-advisor` implementation change; `impl-plan` only composes its
    existing placement decision for the conditional Farplane harness case.
  - No `brainstorm` change; provisional recommendation claim discipline remains
    a separate artifact and exact pre-plan failure surface.
  - No `goal-advisor` implementation change; the existing optimization shape
    is composed, not extended.
  - No new feature doc, metric, rubric family, persistent plan schema, planner
    runtime, ten-way rollout, per-metric Goal, or indefinite convergence loop.
  - No mandatory Goal or subagent for tiny, local, reversible plans whose
    complete change is proven inline.

## Delta

```text
overall_before:
  - A material coding plan can pass minimality checks by asserting that it is the smallest required version and locally justifying each addition.
  - One reviewer pass can catch obvious bloat, but revise findings have no standard repair-until-fixed-point contract.
  - A Farplane harness plan can duplicate Harness Advisor's registry and placement reasoning inside impl-plan instead of binding the existing owner-selection result.
overall_after:
  - A material coding plan is approval-ready only after targeted subtraction, adversarial TAS-A review, and one subsequent no-material-delta pass over the same ticket.md.
  - A valid reduction that preserves objective, acceptance, safety, ownership, and proof forces revision; a rejected reduction names the invariant it would break.
  - Material Farplane harness changes with unresolved or new/moved ownership first receive one compact Harness Advisor placement decision, which the independent reviewer then tries to falsify.
why_now:
  - Session 019f7ec0-a37e-7c73-b3df-1b7942679e77 repeatedly proposed new durable surfaces and withdrew them only after operator challenge, proving that claim-only minimality is insufficient.
first_principles_basis:
  objective: preserve the required behavior and proof while minimizing new state, ownership surfaces, parameters, files, functions, modules, and coordination paths
  need: distinguish an irreducible coding plan from a persuasive first draft
  assumptions: leanness is constrained dominance rather than minimum line count; adversarial criticism has higher information value than many correlated random drafts
  root_cause: impl-plan asks whether a plan is minimal but does not require an observable subtractive search, convergence receipt, clean-pass stop condition, or conditional reuse of Farplane's existing harness-placement owner
  constraints: one ticket owns one canonical coding-plan artifact; qualitative judgment remains none mechanical; supporting files do not become parallel plans
  first_viable_slice: existing implementation-plan rubric + impl-plan contract with conditional Harness Advisor composition + paired hardcases + compact ticket-template wording
  proof_or_falsification: a triggered Farplane harness case must reuse Harness Advisor and an ordinary coding case must skip it; a reducible plan must be revised before operator challenge, while an irreducible modular plan must retain the surface whose removal breaks a protected invariant
  tradeoff: material planning consumes independent review and a clean pass; tiny same-surface plans keep the current direct path
  non_goals: arbitrary brevity, random search volume, self-approval, universal planner service, or content/exploration-policy changes
```

## Objective Contribution

```yaml
objective_contribution:
  ultimate_kpi_id: revenue_usd
  contribution_type: enabler
  kpi_or_guard_id: accepted_harness_improvements
  causal_mechanism: Coding plans that reject avoidable surfaces before implementation reduce wasted build and review work and make accepted harness changes easier to trust.
  expected_change: One shipped and independently accepted harness improvement proving that material coding plans cannot claim lean convergence without subtractive search and TAS-A review.
  forecast_basis:
    kind: configured_threshold
    ref: farplane/metrics.yaml#accepted_harness_improvements
  metric_provider: local_project_metrics
  signal_horizon: ticket completion
  check_in_at: unscheduled
```

## Reward

```yaml
kpi_rewards:
  - reward_id: accepted-harness-improvements-7d
    kpi_id: accepted_harness_improvements
    projection_type: enabler_result
    expected_reward: One shipped and independently accepted harness improvement proving that material coding plans cannot claim lean convergence without subtractive search and TAS-A review.
    check_in_at: unscheduled
    actual_result:
    decision:
    evaluated_at:
    evaluation_key:
    supersedes_evaluation_key:
    evidence_refs: []
guard: "count only after paired hardcases, QA evidence review, and adversarial TAS-A completion review pass"
```

## Change Plan

```text
architecture_signatures:
  module_level:
    - skills/harness-advisor / harness_place(gap_or_request, evidence?): placement_decision
    - skills/impl-plan / converge_plan(ticket, context, budget): canonical_ticket + convergence_receipt | blocked_report
    - skills/review / review_change(plan, rubric_families, required_tas): verdict + findings + evidence + repair_hints
  main_flow:
    - resolve_owner_if_needed(request, inspected_state) -> placement_decision | existing_reviewed_placement | not_needed
    - draft_plan(request, inspected_state, placement?) -> ticket.md
    - subtract(candidate_additions, protected_invariants) -> kept_with_reason[] + removed[] + unresolved[]
    - adversarial_review(ticket.md) -> pass | revise | block | invalid
    - repair_or_handoff(verdict, budget) -> revised ticket.md | Goal Advisor handoff | blocked report
  data_flow:
    - material Farplane harness gap + registries -> Harness Advisor primary/rejected surfaces -> ticket Notes or subtractive receipt
    - acceptance/proof/constraints -> protected invariants -> subtraction decisions
    - Change Plan write paths/signatures -> candidate additions -> remove/reuse/derive/merge/inline/localize/narrow
    - reviewer findings -> ticket repair -> review artifact -> final no-material-delta verdict
  builder_freeform_boundary:
    - Exact wording and fixture design are builder-owned, but one-artifact ownership, protected invariants, subtractive operators, reviewer independence, TAS-A, clean-pass stop, and budget-block behavior may not change without review.
```

### Change 1: Turn minimality into a fixed-point rubric gate

```text
fixes:
  - the implementation-plan rubric can reward a plausible minimality claim without proof that a valid smaller plan was sought
before:
  - bloatability and modularity judge whether the submitted plan appears lean and well-owned
  - a single TAS-A review can end the planning phase
after:
  - the existing dimensions require protected-invariant subtraction and reject a plan dominated by a cheaper valid candidate
  - approval requires adversarial TAS-A plus a subsequent clean pass after the latest material repair
  - the review remains a structured judgment event; no scalar leanness metric or new rubric family is added
read:
  - path: docs/review/rubrics/implementation-plan.md
    reason: canonical coding-plan readiness standard
  - path: docs/review/rubrics/reviewer-handoff.md
    reason: caller/reviewer independence and routing contract
write:
  - path: docs/review/rubrics/implementation-plan.md
    change: strengthen bloatability, modularity, hard gates, and TAS-A evidence with subtraction and fixed-point semantics
  - path: skills/review/evals/evals.json
    change: add paired reducible and irreducible implementation-plan judgments
operation:
  - protect objective, acceptance, safety, current ownership, and proof before optimizing
  - test status quo, existing-owner reuse/merge/derive, and the proposed path
  - return revise whenever a cheaper valid plan dominates the submission
  - reserve approval for TAS-A followed by a clean no-material-delta pass
signature_or_type_impact:
  - docs/review/rubrics/implementation-plan.md / classify_lean_convergence(plan, protected_invariants, prior_receipt?): pass | revise | block | invalid
  - skills/review / review_change(...): judgment event retains verdict, TAS, evidence, and repair_hints
routes:
  docs: doc-advisor
  qa: agent-qa-test
  review: reviewer
qa:
  - unnecessary config-field/helper/companion additions receive revise
  - removing required proof or a real owner boundary cannot improve readiness merely by shortening the plan
failure_modes:
  - optimizing file or line count instead of total system complexity
  - accepting self-reported subtraction without reviewer evidence
  - letting the planning lane self-certify adversarial review
```

### Change 2: Make impl-plan repair until fixed point or block

```text
fixes:
  - impl-plan can finish after one draft and one review without a standard subtractive repair loop
before:
  - the planner declares the smallest implementation and justifies additions locally
  - valid reviewer reductions depend on ad hoc follow-up
after:
  - a material Farplane harness delta with unclear ownership or a proposed new/moved harness surface conditionally calls existing Harness Advisor before the draft; ordinary and tiny plans do not
  - its compact placement and rejected surfaces live inside ticket Notes or the existing subtractive receipt, and an already-reviewed receipt is reused
  - impl-plan derives candidate additions from existing Change Plan write paths and signatures and applies remove, reuse, derive, merge, inline, localize, and narrow operators
  - material plans repair adversarial findings until TAS-A and one clean pass
  - if useful repair cannot finish inline, the caller hands the same ticket to existing Goal Advisor optimization; budget exhaustion with an open valid reduction blocks
read:
  - path: skills/harness-advisor/SKILL.md
    reason: existing Farplane harness placement contract composed conditionally, not modified
  - path: skills/impl-plan/SKILL.md
    reason: public coding-plan workflow
  - path: skills/impl-plan/qa_checklist.md
    reason: preflight and repair guardrail
  - path: skills/impl-plan/prompts/plan.md
    reason: unified planning prompt
write:
  - path: skills/impl-plan/SKILL.md
    change: add the conditional existing Harness Advisor placement route, bounded subtraction, adversarial review convergence, one-artifact ownership, and existing Goal Advisor handoff
  - path: skills/impl-plan/qa_checklist.md
    change: replace claim-only minimality with conditional placement reuse, observable subtraction, and fixed-point checks
  - path: skills/impl-plan/prompts/plan.md
    change: synchronize the conditional placement predicate, loop, claim boundary, and stop/block contract
  - path: skills/impl-plan/evals/evals.json
    change: add triggered/skipped placement cases, sanitized backtracking hardcase, clean-pass sequence, and irreducible modular control
operation:
  - classify whether the request is a material Farplane harness delta with unresolved ownership or a proposed new/moved durable harness surface
  - when true and no reviewed placement exists, call Harness Advisor once; place its primary owner and rejected surfaces in existing ticket Notes or the subtractive receipt
  - when false, or when a reviewed placement already exists, skip the call and continue without new ceremony
  - draft one ticket from inspected code and explicit constraints
  - enumerate additions from the plan itself rather than adding a parallel inventory schema
  - challenge each addition with the ordered subtractive operators
  - request adversarial implementation-plan, architecture, and evidence-quality review; for the conditional harness case, require the reviewer to attempt a better placement rather than trust the advisor receipt
  - repair valid findings; rerun after every material change; stop only on TAS-A plus one clean pass
  - call existing goal-advisor only when the same-artifact loop needs continuation; never spawn one Goal per finding or dimension
signature_or_type_impact:
  - skills/impl-plan / resolve_owner_if_needed(request, context): placement_decision | existing_reviewed_placement | not_needed
  - skills/harness-advisor / harness_place(gap_or_request, evidence?): primary_owner + rejected_surfaces + proof_path
  - skills/impl-plan / converge_plan(ticket, context, budget): canonical_ticket + convergence_receipt | blocked_report
  - skills/impl-plan / subtract(candidate_additions, protected_invariants): kept_with_reason[] + removed[] + unresolved[]
  - ticket QA Strategy or Notes / lean convergence receipt: reviewer artifact ref + final fixed-point verdict, not a new top-level field
routes:
  docs: doc-advisor
  qa: agent-qa-test
  review: reviewer
qa:
  - material Farplane harness case with ambiguous or new/moved ownership calls Harness Advisor exactly once and embeds its compact decision without a new field or artifact
  - ordinary coding, tiny fixes, and tickets with an already-reviewed placement skip the advisor call
  - adversarial reviewer can overturn a weak placement and force both placement note and plan repair
  - sanitized reducible case rejects the speculative field/feature before operator challenge
  - irreducible control retains a modular helper when inlining duplicates policy or breaks ownership
  - tiny local fix remains inline without forced Goal or reviewer lane
failure_modes:
  - invoking Harness Advisor for every coding plan and duplicating generic owner scans
  - treating Harness Advisor as the planner or final reviewer
  - accepting the placement receipt without an independent counter-placement attempt
  - generating ten shallow variants instead of testing causal alternatives
  - deleting a modular boundary solely to reduce file count
  - creating a reviewer-owned rewrite or second canonical plan
  - treating the last materially changed review as the clean pass
```

### Change 3: Keep the ticket artifact and proof wording aligned

```text
fixes:
  - the canonical ticket template does not state the convergence receipt or explicitly distinguish the target artifact from required companions
before:
  - ticket.md is canonical, while diagrams and review evidence are required but their support role is implicit
after:
  - existing QA Strategy/Notes guidance records the final reviewer reference and fixed-point verdict without new top-level fields
  - when conditional Harness Advisor placement applies, existing Notes/subtractive-receipt guidance carries primary and rejected surfaces without a new field
  - ticket.md remains the only coding-plan target; diagrams, reviews, Goal Packet, progress, and proof remain linked companions
read:
  - path: tickets/templates/ticket.md
    reason: canonical ticket artifact contract
write:
  - path: tickets/templates/ticket.md
    change: add compact one-target-artifact, conditional placement-receipt, and lean-convergence guidance inside existing sections
operation:
  - update the existing template only; do not create a feature doc, sidecar schema, metric, or new plan document
signature_or_type_impact:
  - ticket contract / ticket.md = canonical coding plan; diagrams.md + artifacts/* + program.md + progress.md = companion evidence/control state
routes:
  docs: doc-advisor
  qa: tests
  review: reviewer
qa:
  - a generated plan can link required companions without turning them into independent target artifacts
  - a triggered placement result fits existing Notes or subtractive receipt without a new schema key
  - template and impl-plan language agree without duplicating the full rubric
failure_modes:
  - adding top-level ticket fields for evidence already represented in QA Strategy, Notes, and artifacts
  - calling diagrams non-blocking to validation; they are non-canonical but still required before planning validation passes
```

```text
visual_companion:
  path: tickets/TASK-0396/diagrams.md
  generated_by: delegated diagramming lane after adversarial plan reconciliation
  blocks_approval: false; its content is non-authoritative, while planning validation still requires the linked file to exist
  canonical_contract: ticket.md
```

## Done

```text
done_when:
  - material Farplane harness plans with unclear ownership or proposed new/moved durable surfaces conditionally reuse existing Harness Advisor before drafting, while ordinary/tiny/reviewed-placement plans skip it
  - the compact placement decision stays inside existing ticket Notes or subtractive receipt and creates no new field, sidecar, or canonical artifact
  - the adversarial reviewer independently attempts a better owner and can force placement plus plan revision
  - material impl-plan outputs cannot claim lean/minimal/approval-ready without targeted subtraction, adversarial TAS-A, and one clean no-material-delta pass
  - the search protects objective, acceptance, safety, ownership, and proof and rejects shorter plans that violate those invariants
  - status quo, existing-owner reuse/merge/derive, and the proposed path are tested; ten random rollouts are not required
  - one ticket owns one canonical coding-plan artifact and required companions remain linked evidence/control state
  - an unconverged plan uses at most one bounded Goal over the ticket with review as feedback; no per-metric Goals or scalar leanness score exist
  - tiny same-surface plans retain a direct inline path
  - paired hardcases reject speculative additions and preserve a necessary modular boundary
  - affected skill, rubric, template, and focused evals validate
  - independent QA evidence review and adversarial completion review pass at TAS-A with no unresolved hard gate
```

## QA Strategy

```text
qa_strategy:
  proof_weight: agent_qa
  checks:
    - python3 skills/skill-maintenance/scripts/check_skills.py --write
    - python3 bin/validators/check_doc_refs.py
    - python3 skills/eval/scripts/run_evals.py status --harness codex --target-root .
    - run focused isolated behavior traces for impl-plan and review from the installed .farplane eval runner
    - farplane validate ticket tickets/TASK-0396/ticket.md --phase complete
  manual:
    - inspect one triggered and one skipped Harness Advisor route and confirm the predicate is narrow and the receipt is embedded in the ticket
    - inspect the paired reducible/irreducible traces and every retained new surface reason
    - inspect the final ticket and companions to confirm ticket.md is the only canonical plan
  delegated_lanes:
    - qa-tester runs behavior traces and writes ticket-scoped evidence
    - reviewer critiques QA evidence before completion
    - adversarial reviewer performs final completion review independently of the implementer
  review:
    - rubric: spec-contract + implementation-plan + architecture + skill-contract + integration-readiness + prompt-quality + evidence-quality
      required_tas: TAS-A
    - hard_gate: no approval-ready claim without independent reviewer receipt, an independent counter-placement attempt when Harness Advisor was used, and a clean no-material-delta pass
  evidence:
    - tickets/TASK-0396/artifacts/qa/behavior-traces/
    - tickets/TASK-0396/artifacts/qa/evidence-review.md
    - tickets/TASK-0396/artifacts/review/plan-review.md
    - tickets/TASK-0396/artifacts/review/completion-review.md
  goal_advisor_inputs:
    proof_route: static checks -> paired behavior traces -> evidence review -> adversarial completion review
    final_evidence: behavior traces, evidence-review receipt, completion-review receipt
    final_checkpoint: reviewer TAS-A plus clean no-material-delta pass, then farplane ticket close TASK-0396
  residual_risk:
    - qualitative reviewer judgment can vary; paired controls and protected invariants constrain but do not make leanness mathematically unique
    - an over-broad trigger would add placement ceremony to ordinary coding plans; the skipped-route trace is a completion gate
```

### Sanitized hardcase

```text
input:
  - Existing tickets already own durable work state and current plan/review surfaces already carry the relevant intent.
  - The request is a material Farplane harness change proposing a new durable planning field and feature handles.
failed_output:
  - Add planning.operator_focus, then propose several new feature handles as the lean recommendation.
operator_challenge:
  - Tickets already solve the state problem. Is this actually as lean as possible?
expected_before_challenge:
  - Invoke existing Harness Advisor once because the material Farplane harness proposal adds durable surfaces; record its existing-owner placement and rejected alternatives inside the ticket rather than a new artifact.
  - Map each proposed field, file, feature, helper, and route to an existing owner.
  - Reject planning.operator_focus and duplicate feature handles when ticket scope, Delta, Change Plan, and review already satisfy the requirement.
  - Retain a new surface only when removal or reuse breaks a named acceptance, ownership, safety, or proof invariant.
  - Do not claim lean convergence until an adversarial TAS-A review and subsequent clean pass exist.
```

## Docs Strategy

```text
docs_strategy:
  outcome: update_docs
  doc_targets:
    - docs/review/rubrics/implementation-plan.md
    - tickets/templates/ticket.md
  no_docs_reason:
  validation:
    - python3 bin/validators/check_doc_refs.py
    - python3 skills/skill-maintenance/scripts/check_skills.py --write
```

## Run Hints

- `Likely size:` normal
- `Goal recommendation:` required after plan approval
- `Budget hint:` one implementation Goal; reserve budget for paired behavior
  traces, evidence review, and adversarial completion review
- `Compute hint:` local_shared
- `Planning hint:` impl_plan
- `Expected beats:` 2-4
- `Parallel:` no for overlapping contract edits; QA traces may fan out later
- `QA source:` QA Strategy
- `Batchability:` single-ticket
- `Batch reason:` one coding-plan behavior artifact and its existing rubric/template support
- `Human inputs/assets:` none
- `Credentials / external access:` none for static checks
- `Compute/runtime needs:` local validators and isolated Codex behavior traces
- `Tooling gaps:` none known
- `QA risks:` correlated judgments; mitigate with adversarial reviewer and paired controls
- `Human gates:` approve this plan before Goal-backed implementation
- `Agent decision boundaries:` no new metric, rubric family, planner service,
  plan artifact, or per-metric Goal without ticket revision

## Links

- `program:` `none` until plan approval
- `progress:` `none` until plan approval
- Visual companion: [diagrams.md](diagrams.md)
- `artifacts:` `tickets/TASK-0396/artifacts/`
- `review:` `tickets/TASK-0396/artifacts/review/plan-review.md`
- `refs:` `skills/impl-plan/SKILL.md`,
  `skills/harness-advisor/SKILL.md`,
  `docs/review/rubrics/implementation-plan.md`, `tickets/templates/ticket.md`

## Notes

### Subtractive receipt

| Candidate | Decision | Invariant / reason |
|---|---|---|
| Rubric + impl-plan + paired evals | keep | Smallest end-to-end owner path: rubric classifies, planner repairs, evals falsify. |
| Conditional existing Harness Advisor call | keep | Avoids duplicating Farplane-specific registry/placement logic when a material harness plan has unresolved or new/moved ownership; adds no change to Harness Advisor and no artifact. |
| Ticket-template wording | keep | Encodes the operator's one-ticket/one-canonical-artifact rule where every plan is materialized; no new field is added. |
| Goal Advisor code/docs/evals | remove | Existing optimization route accepts one artifact, review feedback, budget, and stop conditions; caller composition is sufficient. |
| Content implementation planning | remove | Different production-plan artifact and different subtractive units; requires its own ticket. |
| Harness Advisor implementation changes | remove | Its current signature already returns primary/rejected surfaces and proof; caller composition is sufficient. |
| Brainstorm claim guard | remove | Exact provisional-recommendation surface is distinct from the coding-plan artifact; requires its own ticket. |
| Feature/system docs | remove | Existing rubric, skill, and ticket template are sufficient owners for the first viable slice. |
| New leanness metric/rubric/schema/runtime | reject | Adds state without improving qualitative judgment or proof. |
| Ten-plan rollout / per-metric Goals | reject | High correlated cost; targeted causal counterplans plus adversarial repair provide better information per budget. |

- `Minimality claim:` After the subtractive receipt above, this ticket retains
  only the existing conditional placement call, coding-plan rubric, planner,
  paired falsification, and canonical ticket wording required to make the
  behavior executable and durable.
- `Rollback:` Revert the rubric, skill, eval, and template changes together;
  no migration or external state is involved.
- `Follow-up boundary:` Create separate tickets for content-plan convergence
  and provisional recommendation claim discipline only after this core contract
  passes its paired hardcases.
- `Plan QA:` PASS — the revised companion and planning validation pass;
  adversarial pass 3 reached TAS-A with no material delta. The trigger is
  limited to material Farplane harness changes with unresolved or proposed
  new/moved ownership, while ordinary, tiny, and reviewed-placement plans skip
  it. Highest implementation risk is widening this conditional route into
  mandatory ceremony for generic plans.
- `Grounding:` local-only—current Farplane skill, rubric, ticket, Goal, eval,
  and sanitized session evidence.
