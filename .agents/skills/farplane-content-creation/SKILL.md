---
name: farplane-content-creation
description: "Turn Farplane evidence or content intent into a human-approved skeleton, an optimized exemplar, and controlled distribution variants."
tier: 3
source: local
group: capability
template_uses:
  skill-template: "0.3.2"
  skill-qa-checklist: "0.1.1"
  skill-surface-budget: "0.1.0"
qa_checklist: qa_checklist.md
eval: evals/evals.json
planner_contract:
  required_arguments: ["problem_ref", "system_ref", "feature_refs", "source_or_idea", "audience", "content_goal", "channels"]
---

# Farplane Content Creation

## Context

Use this project-local pipeline when Farplane should turn accepted evidence,
market learning, or a bounded content idea into something worth distributing.
It folds the useful taste-loop behavior into content production without
reviving a separate controller: propose a small number of strong bets, obtain
human planning feedback, freeze the chosen skeleton, optimize one exemplar,
then expand the proven pattern into controlled variants.

The pipeline produces local review artifacts. Publication, outreach, spend,
filming, external generation, and account mutation remain separately gated.

## Skill Signature

```text
farplane_content_creation(problem_ref, system_ref, feature_refs, source_or_idea, audience, content_goal, channels=all_configured, brand_kit?, tasty_pack_ref?, content_kind?, video_method?, ticket?, audience_context?, variation_count=10)
  -> best_bet_proposals + approved_skeleton + optimized_exemplar + format_transformations + variation_matrix + ranked_shortlist + distribution_handoff + proof_refs
state: reads(farplane/harness.yaml stable problems, docs/systems and docs/features registries, farplane/metrics.yaml, ticket audience_context first or configured Feed Scout World Memory as fallback, source/evidence refs, resolved Brand Kit, optional computed Tasty Pack, ticket Goal Packet); writes(ticket-local proposals, frozen creative-input bundle, skeleton, exemplar, variants, review evidence, and feedback state)
gates: strategic_ref_bound; source_ref_preserved; audience_problem_named; canonical_icp_bound; baseline_named; intended_belief_or_behavior_delta_named; audience_named; content_goal_named; claim_strength_matches_proof; planning_approval_before_execution; exemplar_approval_before_variations; publish_requires_separate_approval
routes: root skill `content-impl-plan` | root skill `optimize-with-human` | root skill `goal-advisor` | root skill `storyboard` | root skill `social-content` | root skill `video-production` | root skill `remotion` | root skill `qa` | root skill `review`
fails: unreferenced_random_feature; internal_name_as_hook; executes before skeleton approval; asks a human to judge an undifferentiated batch; generates random rewrites; varies the proof spine; publishes all variants; treats feedback as publication authority
```

## Pipeline Contract

```text
content_pipeline(input)
  -> best_bets(1..3)
  -> human_plan_loop(approve | revise | reject)
  -> frozen_skeleton
  -> exemplar_execution
  -> human_execution_loop(keep | approve | revise | reject)
  -> cross_format_transformations(configured channels)
  -> controlled_variants(default=10)
  -> qa_and_rank(top=2..3)
  -> gated_distribution_handoff
```

`optimize-with-human` supplies the feedback metric and pause/resume contract.
It does not replace `content-impl-plan`, the artifact-producing content skills,
or the ticket Goal Packet. Use one persistent task for a material loop so the
same worker can receive replies and continue from durable state.

## Required Turn Receipt

Make the pipeline state inspectable on every planning or feedback turn. Before
proposals or artifacts, emit or persist this compact receipt:

```yaml
content_pipeline_state:
  phase: planning | execution | variation | distribution_handoff
  route: content-impl-plan -> optimize-with-human
  problem_ref: configured stable problem
  system_ref: canonical system
  feature_refs: [canonical feature refs]
  audience: named audience
  content_goal: intended effect
  channel: format or undecided
  source_refs: evidence or explicitly unproven premise
  brand_kit_snapshot: resolved id, revision, prompt, and elements
  tasty_pack_ref: optional computed reference packet
  proof_limits: allowed and prohibited claims
  authority:
    local_drafting: allowed
    publication: gated
    outreach: gated
    spend: gated
    filming: gated
    external_generation: gated
    account_mutation: gated
  approved_plan_ref:
  active_gate: exact approval or proof still required
```

After human feedback, append or show a durable feedback receipt. A feedback
turn is invalid and must not return until it emits every field below, including
when feedback invalidates the skeleton and reopens planning:

```yaml
feedback_receipt:
  state_path: tickets/TASK-XXXX/progress.md
  artifact_ref: path-or-id-being-reviewed
  phase: planning | execution
  human_signal: exact verdict or bounded paraphrase
  learning: what the signal changes
  next_hypothesis: next local bet
  promotion_decision: keep_local | promote_candidate | reject
```

Naming the active route and receipt is required; a conversational “pick one”
or a revised skeleton without the receipt is not a completed pipeline turn.

Do not collapse authority into “posting requires approval.” Every handoff and
refusal must explicitly preserve the separate publication, outreach, spend,
filming, external-generation, and account-mutation gates so one approval cannot
silently broaden into another action class.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind one stable `problem_ref`, canonical `system_ref`, relevant `feature_refs`, audience, recognizable problem, content goal, channels, accepted source evidence, resolved Brand Kit, optional computed Tasty Pack, rights, proof limits, and authority. Freeze those inputs in one Creative Input Bundle and preserve them through every format. Lead with the audience's pain and visible result—not an internal Farplane feature name.
- [ ] 2. Use `content-impl-plan` to shape one Best Bet by default and no more than three genuinely distinct proposals for planning feedback; for video, bind content kind and method. Do not introduce a `style_profile` as a third composition source on the Brand Kit/Tasty path.
- [ ] 3. Run `optimize-with-human` in `phase: planning`; revise or reject locally until the human approves one proposal, then write its frozen skeleton and `approved_plan_ref`.
- [ ] 4. Route the skeleton to the smallest faithful artifact-producing skill and build one exemplar before any batch expansion. Dispatch video through the selected `video-production` method and pass the frozen Brand Kit/Tasty visual direction instead of forcing every video through explainer.
- [ ] 5. Run `optimize-with-human` in `phase: execution` until the exemplar reaches keep, approve, convergence, budget, or blocker; planning-invalidating feedback reopens step 2.
- [ ] 6. After exemplar approval, transform the frozen skeleton across every configured channel and useful format in the same ticket, then generate ten controlled variants by default from declared variable axes while preserving every skeleton invariant and proof boundary.
- [ ] 7. QA the batch, record the variation matrix and expected learning, then rank a two-to-three-item shortlist instead of sending or publishing the whole batch.
- [ ] 8. Obtain independent review for material readiness, persist feedback and proof receipts, and leave publication, outreach, spend, filming, external generation, and account actions approval-gated.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## 1. Bind The Creative Problem

The content brief must name:

- stable problem, canonical system, relevant features, and accepted evidence refs;
- audience or buyer and the problem they recognize;
- content goal and intended channel or format;
- source evidence, market learning, or explicitly unproven idea;
- taste references and the specific patterns worth borrowing;
- claim boundaries, prohibited claims, rights constraints, and approval gates;
- the smallest useful artifact that can test the premise.
- canonical ICP and selected world facts, the current baseline/default, and the
  precise belief or behavior delta the artifact is designed to cause.

Evidence-backed content must map material claims to proof. An unproven idea may
be explored, but it must remain labeled as a premise or hypothesis rather than
being laundered into a Farplane result.

The viewer-facing hook should answer how the audience can do something valuable
or avoid a recognized failure. Internal system and feature names remain proof
metadata unless the audience already uses those names.

## 2. Shape Best Bets

Call `content-impl-plan` before production. Produce one Best Bet by default;
use two or three only when the alternatives teach something materially
different. Each proposal must include:

- audience promise and core angle;
- taste insight and reference leverage;
- artifact shape and channel;
- narrative or teaching spine and execution beats;
- proof engine and claim boundary;
- why it could win, likely cringe risks, and rejected nearby formats;
- the one planning question and the next step if approved.

Output exactly one recommended Best Bet and ask `approve | revise | reject`.
Show two or three only when their materially different learning value is
explicitly justified. In that case label exactly one `recommended_default`,
label the rest `alternatives`, give a short comparative reason, and still ask
for approve/revise/reject on the default rather than asking the human to choose
among equally positioned options. The human may override the recommendation,
but the pipeline must contribute taste and judgment.

Do not make the human rank ten hooks, ten scripts, or ten rendered artifacts
before a direction exists.

The planning response must label `phase: planning`, name the
`content-impl-plan -> optimize-with-human` route, and fill the required turn
receipt before asking the short human question.

## 3. Optimize Planning And Freeze The Skeleton

Run `optimize-with-human` with `phase: planning`. Persist each hypothesis,
artifact reference, human question, signal, learning, and next hypothesis in
the ticket Goal Packet. Approval creates a frozen content skeleton:

```yaml
approved_skeleton:
  approved_plan_ref: path-or-id
  audience: named audience
  promise: one viewer-facing promise
  core_angle: one sentence
  narrative_or_teaching_spine: ordered beats
  proof_spine: evidence refs and allowed interpretations
  format_engine: repeatable structure or visual device
  video_method: selected method or not_applicable
  brand_kit_snapshot: resolved id, revision, prompt, and elements
  tasty_pack_ref: optional computed reference packet or not_supplied
  inspiration_pack: task evidence ref or not_supplied
  call_to_action: bounded next action
  invariants: elements every variant must preserve
  variable_axes: elements the later batch may vary
  prohibited_claims: unsupported or misleading claims
```

Approval means “use this skeleton for execution.” It does not authorize
publishing, paid generation, filming, outreach, or account mutation.

Feedback that changes audience, promise, core angle, proof spine, or format
engine invalidates the skeleton and returns to planning. Copy, pacing, layout,
shot, caption, or implementation feedback stays in execution unless it reveals
that the underlying premise is wrong.

## 4. Build And Optimize One Exemplar

Route to the smallest faithful production path: `storyboard`, `social-content`,
`video-production`, `remotion`, or another explicit artifact owner. Build one
exemplar against the approved skeleton. Then run `optimize-with-human` with
`phase: execution` and `approved_plan_ref` bound.

Keep iterating one inspectable artifact until the human chooses keep/approve,
the loop converges, the budget is exhausted, or a blocker is recorded. Do not
harden a reusable skill from one rejection; first perturb the local execution.

## 5. Expand The Proven Pattern

Only an approved exemplar unlocks transformation and the batch. First produce
the configured cross-format pack—such as primary video, short cuts, carousel,
X thread, and LinkedIn post—without changing the proof spine. Do not split one
approved skeleton into one ticket per format. Then generate ten variants by default
unless the ticket explicitly sets another count. A controlled variant changes
one or two declared axes, such as hook, opening visual, metaphor, proof order,
CTA wording, or channel adaptation, while preserving the skeleton invariants.

Record every row:

```yaml
variation:
  id: V01
  changed_axes: [hook]
  preserved_invariants: [audience, promise, proof_spine, format_engine]
  expected_learning: what this variant tests
  artifact_ref: path
  qa_checks:
    claim: pass | fail
    invariant: pass | fail
    format: pass | fail
    rights: pass | fail
    channel: pass | fail
  qa_verdict: pass | revise | reject
  rank: 1-10 or unranked when rejected
  rank_rationale: concise comparative reason
```

The batch is incomplete unless all ten rows record `changed_axes`,
`preserved_invariants`, `expected_learning`, `artifact_ref`, `qa_checks`,
`qa_verdict`, `rank`, and `rank_rationale`.
Do not replace per-variant learning hypotheses with one batch-level sentence,
and do not claim the variation step complete while any row lacks its receipt.
A generic `QA: pass` column is invalid. The rendered matrix must expose named
`claim`, `invariant`, `format`, `rights`, and `channel` pass/fail results for
every row, plus a separate ordinal rank and comparative rationale.

Ten variants are a local search batch, not ten publication instructions.
Reject variants that weaken the proof, collapse into generic AI content, or
break the approved story engine.

## 6. Rank And Hand Off

Run claim, continuity, format, rights, and channel checks appropriate to the
artifact. Rank every passing variant with a concise comparative rationale. Keep
the approved skeleton, exemplar, full variation matrix, named QA results, and
ranking rationales in `internal_proof`. Then create a distinct
`distribution_handoff`; its selected-artifact list contains only the top two
or three refs and points back to internal proof instead of copying other
variants or rationale prose.

Do not place the other seven or eight drafts in the distribution handoff. They
remain internal search evidence even though their matrix rows stay linked for
auditability.

Render the selection mechanically:

```yaml
distribution_handoff:
  selected_artifact_refs: [path/to/V01, path/to/V03, path/to/V02]
  approved_skeleton_ref: path/to/approved-skeleton.md
  approved_exemplar_ref: path/to/exemplar
  selection_rationale_ref: path/to/variation-matrix.md
  proposed_experiment: bounded distribution comparison
  expected_learning: what the selected set tests
  required_approvals: [publication, outreach, spend, filming, external_generation, account_mutation]
```

`selected_artifact_refs` must contain only the ranked top two or three. Names
and rationale live in the internal matrix; do not substitute prose for refs.

Use provider observations after approved distribution as later market
feedback. Never invent reach or treat draft count as outcome movement.

## Positive Example

Input: accepted activation evidence for serious agent builders, plus a taste
reference for crisp educational carousels. The pipeline proposes “Installed Is
Not Activated,” gets the teaching spine approved, freezes the activation
stages and evidence refs, and optimizes one carousel until the hierarchy and
copy are approved. It then creates ten variants across hook, metaphor, proof
order, and CTA while preserving the activation model and claim map. QA rejects
two, ranks the rest, and returns the best three for a separately approved
distribution test.

## Negative Example

The pipeline immediately writes ten unrelated “AI agents are the future”
posts, asks the human to pick one, mixes unsupported autonomy claims into the
batch, and schedules every post after a single “looks good” reply. This fails
because there is no approved skeleton, no optimized exemplar, no controlled
variation matrix, and no publication authority.

## Output

- One to three Best Bet proposals and planning feedback receipts.
- One frozen approved skeleton with invariant and variable-axis contracts.
- One optimized exemplar and execution feedback receipts.
- Ten controlled variants by default, a QA-backed ranking, and a top-two-or-three shortlist.
- Proof references, review evidence, expected learning, and explicit gated actions.
