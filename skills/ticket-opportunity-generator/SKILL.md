---
name: ticket-opportunity-generator
description: "Turn Farplane products, goals, interval reports, ops memory, board state, and recent evidence into concrete execution-ticket specs."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.3.7"
  skill-eval-task: "0.1.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash
---

# Ticket Opportunity Generator

## Context

Use this skill when Pulse has no proceedable tickets and needs to turn
`farplane/products.md`, goals, interval reports, ops memory, board state, and
recent evidence into concrete executable ticket specs. It is the manager-side
idea compiler for `pulse-update`: discover premises, score them, crystallize
hypotheses, reject vague or boring ideas, and return execution-ready ticket
specs.

A valid ticket is not automatically worth doing. This skill must reject
specific-but-mid work whose artifact would be a low-stakes internal note,
review receipt, or paperwork proof. Every selected worker ticket needs a big
claim, audience or operator tension, a reason the result could be surprising,
an honest baseline or contrast, an artifact level that matches the product
lane, and a dedupe decision against recent work. Good tickets are bets worth
proving, not chores with correct metadata.

This skill does not write tickets by default, spawn workers, run final
experiments, publish content, mutate accounts, deploy, spend, or replace
Daily/Weekly strategy. Pulse remains the manager and ticket writer. Worker
tickets remain execution only.

## Skill Signature

```text
generate_tickets(products, goals, daily_report, weekly_report,
                 ops_memory?, board_state?, recent_evidence?, policy?)
  -> lane_scan[]
   + trend_tensions[]?
   + leverage_bets[]?
   + opportunity_packets[]
   + dedupe_decisions[]
   + portfolio_selection
   + selected_hypotheses[]
   + executable_ticket_specs[]
   + scout_requests?
   + blocked_report?

state:
  reads(farplane/products.md, farplane/goals.yaml?,
        .farplane/reports/interval/daily_interval/*?,
        .farplane/reports/interval/weekly_interval/*?,
        farplane/ops-memory.md?, tickets/**/ticket.md?,
        .farplane/feed-scout/daily/*.json?,
        .farplane/reports/feed-scout/*?,
        .farplane/feed-scout/ledger.jsonl?,
        recent artifacts/rewards/metrics/reports?)
  writes(none by default; caller writes tickets or Pulse report)

gates:
  product_lanes_scanned; selected_and_skipped_lanes_reasoned;
  ai_planning_reward_frontmatter_named; product_backed_kpi_reward_named;
  maintenance_not_primary_throughput;
  product_lane_named; goal_or_interval_signal_named; evidence_refs_named;
  big_claim_named; audience_tension_named; surprise_factor_named;
  external_or_default_baseline_named_when_audience_facing;
  hypothesis_specific; baseline_or_variant_or_hook_named;
  measurement_method_named; expected_decision_or_content_job_named;
  artifact_level_sufficient; output_artifact_named; product_reward_named; reward_guard_named;
  dedupe_status_allowed;
  lifecycle_metadata_complete; dependencies_satisfied_or_named;
  human_gate_classified; executable_without_further_ideation

routes:
  pulse-update | feed-scout | leverage-advisor | harness-scout |
  metric-advisor | content-impl-plan | farplane-ablation-proof |
  farplane-experiment-report | review

fails:
  generic ablation/content/experiment ticket; planning-to-plan ticket;
  specific but boring ticket; low-stakes internal note presented as
  distribution work; review/capture/admin receipt presented as Pulse
  throughput; audience-facing claim without an external/default baseline;
  content ticket whose output level is only "note" or "outline" unless it is
  explicitly a small planning card;
  artifact without products.md contribution; hypothesis without evidence;
  ticket that asks the worker to find the idea; final-action ticket for post,
  publish, spend, deploy, account mutation, external contact, or destructive
  cleanup without a human gate; generator, Pulse, metadata, or maintenance
  cleanup ticket presented as primary product throughput without directly
  unblocking an existing product-backed ticket; converting the current
  parent-beat repair, regression check, or planner bug into the next worker
  ticket just because it can be framed as an experiment
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the frame.
  - [ ] Read `products.md` lanes, product outputs, rewards, and artifact
        workflows.
  - [ ] Read current goals, latest Daily/Weekly interval guidance, ops memory,
        board state, and recent completed tickets/artifacts/rewards.
  - [ ] Read the last 7 days of Feed Scout daily JSON and latest Feed Scout
        report when distribution, market-learning, demo, or public-proof
        content may be selected.
  - [ ] Read enough archived tickets, artifacts, Pulse reports, and Feed Scout
        ledgers to dedupe against claims and formats already tried.
  - [ ] Record human gates from bindings or caller policy.
- [ ] 2. Discover opportunity packets before ticket specs.
  - [ ] Scan every `products.md` lane or artifact workflow for current blocker,
        progress opportunity, safe autonomous work, and human-gate cost. Record
        why each lane is selected, skipped, or deferred.
  - [ ] For distribution and market-facing tickets, synthesize Feed Scout
        items into `trend_tensions[]`: what changed, why people may care now,
        which audience problem it exposes, and what Farplane can credibly prove
        or show against it.
  - [ ] For self-improvement, ablations, experiments, and productization, use
        `leverage-advisor` framing on existing Farplane capabilities:
        capability, loss term, compounding move, first proof step, and content
        upside.
  - [ ] Mine recent evidence, code/skill hotspots, source gaps, repeated
        blockers, completed tickets, content-worthy lessons, and competitor or
        default-workflow contrasts.
  - [ ] Use bounded scout requests only when discovery is too broad for the
        current beat; scout output is ranked premises, not final tickets.
- [ ] 3. Score packets.
  - [ ] Score product fit, goal fit, evidence strength, execution clarity,
        autonomy safety, expected reward, freshness, human-gate cost, audience
        tension, surprise, baseline strength, artifact ambition, dedupe
        novelty, and likely Kenji review value.
  - [ ] Prefer high-autonomy, low-gate work when Kenji is unavailable or review
        backlog is high.
  - [ ] Reject high-scoring metadata shape with weak ambition: if the result is
        true but boring, resize to a stronger baseline, better artifact level,
        or return a blocked/revise report.
  - [ ] Require product-backed KPI attribution. Each selected ticket spec must
        include frontmatter `rewards.kpi` and at least one body
        `Reward.kpi_rewards[].kpi_id` from `farplane/bindings.yaml` metrics
        whose metric product maps into `farplane/products.md`, plus
        `expected_reward` text and `guard`; the scope must produce that product
        output or artifact workflow. Do not use cross-product coordination KPIs
        as the only justification.
  - [ ] Treat generator, Pulse, metadata, or maintenance cleanup as repair work
        only when it directly unblocks an existing product-backed ticket. Do
        not select it as the primary next-wave product ticket.
  - [ ] Reject the current parent-beat repair or regression subject as a worker
        premise. A Pulse/classifier/metadata/generator fix that happened in
        the manager beat may be documented in the Pulse report, but it must not
        become the next product ticket unless a later Daily/Weekly strategy
        independently selects it with non-self-referential product evidence.
  - [ ] Select a portfolio wave sized by caller worker cap, useful lane
        diversity, and specificity. A one-ticket wave is valid only when the cap
        is one or only one premise survives the gates.
- [ ] 4. Crystallize selected hypotheses.
  - [ ] For ablations, name feature/behavior, baseline, variant, measurement,
        measurement method, expected decision, evidence refs, product reward,
        artifact path, and whether the baseline is external/default/normie
        enough for the claim. Audience-facing ablations should prefer vanilla
        Codex, no-template, competitor, or normal-human workflow baselines over
        Farplane-vs-Farplane comparisons.
  - [ ] For experiments, name target surface, proposed change, measurement,
        measurement method, baseline/current behavior, expected decision,
        expected reward, evidence refs, and artifact path. Preserve an
        experiment request as an experiment unless the caller explicitly asks
        for productization or existing accepted proof already makes the
        implementation ticket more appropriate.
  - [ ] For content, name harness-engineering insight, source evidence,
        audience, hook, format, content job, output artifact, product reward,
        final human gate, and artifact level: script, storyboard, visual,
        demo/video plan, rendered clip, carousel/slides, publish-ready thread,
        or explicit planning card. Generic notes and outlines are not enough
        for distribution throughput.
  - [ ] For market learning, name source/entity, question, decision informed,
        output artifact, and source limits.
- [ ] 5. Apply the specificity gate.
  - [ ] Reject vague titles such as "create first ablation proof", "write
        evidence content", or "find experiment candidates".
  - [ ] Reject tickets that require the worker to decide whether the idea is
        worth doing.
  - [ ] When rejecting a generic ablation/experiment/content request, name the
        missing fields explicitly, including the required output artifact path
        for any eventual executable ticket.
  - [ ] Reject artifacts that do not advance a named product, lane, reward, or
        artifact workflow from `products.md`.
  - [ ] Reject boring-but-valid tickets: if the big claim, audience tension,
        surprise factor, baseline contrast, artifact level, or likely review
        value is weak, do not render the ticket. Strengthen the premise or
        return a blocked/revise report.
  - [ ] Classify dedupe before acceptance:
        `same_claim_same_format` rejects; `same_claim_better_baseline` may pass;
        `same_topic_new_trend` may pass; `same_artifact_more_polish` passes
        only when the output level materially increases.
  - [ ] Reject self-referential planner artifacts that mainly prove Pulse,
        ticket generation, metadata repair, classifier logic, or the current
        automation beat. Product-backed experiments should study a user-facing
        or evidence-facing Farplane workflow, not the freshly patched planner
        machinery itself.
- [ ] 6. Render executable ticket specs.
  - [ ] Include validator-compatible lifecycle/admission metadata:
        `phase: planning`, `status: todo`, `ready: true`,
        `approval_required: false`, `blocked_by: []`, empty `claimed_by`,
        valid `human_gate`, frontmatter `rewards.kpi`, and dependency
        expectations (`depends_on` empty or only satisfied tickets; unresolved
        dependencies belong in `blocked_by`, not an admitted spec).
  - [ ] Include title, product lane, products.md contribution, big claim,
        audience tension, surprise factor, dedupe status, artifact level,
        review surface, hypothesis,
        baseline/current behavior when applicable, variant/proposed change when
        applicable, measurement method, expected decision or content job,
        inputs with exact evidence refs, output artifact, scope, stop
        condition, validations, reward block, and side-effect guards.
  - [ ] Return specs to Pulse; do not spawn or write tickets unless explicitly
        requested by the caller.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Workflow

```text
generate_tickets(...)
  -> extract_frame
  -> scan_product_lanes
  -> synthesize_trend_tensions
  -> generate_leverage_bets
  -> discover_opportunities_by_lane
  -> score_packets
  -> dedupe_against_recent_work
  -> select_portfolio_wave
  -> crystallize_hypotheses
  -> specificity_and_big_claim_gate
  -> render_executable_ticket_specs
```

### 1. Extract Frame

Capture the smallest decision frame:

```yaml
frame:
  active_focus:
  weekly_bets:
  daily_blockers:
  product_lanes:
  lane_weights:
  human_gates:
  recent_evidence:
  source_gaps:
  open_review_backlog:
  worker_cap:
  feed_scout_7d:
  attempted_claims:
  attempted_formats:
```

### 2. Discover Opportunities By Lane

Use `products.md` as the product portfolio, not as a generic category list.
Start with a scan row for every lane before choosing tickets:

```yaml
lane_scan:
  lane:
  weight:
  current_blocker:
  opportunity:
  safe_autonomous_work:
  human_gate_cost:
  decision: selected | skipped | deferred
  reason:
```

| Lane | Discovery question | Candidate output |
| --- | --- | --- |
| experiments | What measurable harness behavior could be tightened based on goals, code/skill hotspots, repeated interval complaints, or source gaps? | experiment hypothesis |
| ablations | What shipped feature or workflow do we believe matters but have not proven against a baseline? | baseline/variant proof hypothesis |
| productization | What accepted proof should become durable harness behavior? | implementation ticket spec |
| trust_distribution | What proven or surprising harness lesson would be useful to serious builders? | content/storyboard/demo draft spec |
| market_learning | What source/entity/question could sharpen positioning or product bets? | opportunity brief spec |
| maintenance | What local repair directly unblocks the active frontier? | repair/proof spec |

Trend-fed distribution branch:

```yaml
trend_tension:
  source_refs:
  what_changed:
  who_cares:
  pain_or_desire:
  current_world_reaction:
  farplane_angle:
  possible_big_claim:
  safe_local_artifacts:
    - script
    - storyboard
    - demo_brief
    - publish_ready_thread
```

Use Feed Scout as evidence of attention, not as permission to publish or scrape
beyond configured sources. A trend-fed ticket must still ground the Farplane
claim in local proof or a safe experiment.

Leverage-fed improvement branch:

```yaml
leverage_bet:
  feature_ref:
  loss_term:
  compounding_move:
  baseline_or_default:
  first_proof_step:
  content_upside:
  expected_reward:
```

Use `leverage-advisor` framing for existing Farplane capabilities such as
ticket-as-program, Goal Packets, closure gates, Feed Scout, or worker review
loops. The selected ticket should prove or exploit a compounding move, not
create another internal review chore.

### 3. Score Packets

Use compact ordinal scoring; do not fake precision.

```yaml
score:
  product_fit: 1-5
  goal_fit: 1-5
  evidence_strength: 1-5
  execution_clarity: 1-5
  autonomy_safety: 1-5
  expected_reward: 1-5
  freshness: 1-5
  human_gate_cost: 1-5
  audience_tension: 1-5
  surprise: 1-5
  baseline_strength: 1-5
  artifact_ambition: 1-5
  dedupe_novelty: 1-5
  kenji_review_value: 1-5
```

Prioritize high product fit, strong evidence, clear execution, safe autonomy,
low human-gate cost, strong audience/operator tension, real contrast, and an
artifact that would be worth reviewing. Preserve lane weights as a bias, not as
permission to create weak work.

Artifact levels:

| Product lane | Minimum worker artifact level |
| --- | --- |
| experiments | report with hypothesis, method, baseline/current behavior, result, conclusion, decision, limits |
| ablations | proof report with with/without comparison, baseline, variant, measurement, result, decision, limits |
| productization | shipped local skill/spec/eval/validator/docs delta plus productization receipt; reviewer receipt belongs to parent/reviewer lane |
| trust_distribution | script, storyboard, visual/carousel, demo/video brief, rendered clip, or publish-ready thread; note/outline only when explicitly labeled planning card |
| market_learning | source-grounded opportunity brief with decision informed, source limits, and next bet |
| maintenance | repair/proof only when it directly unblocks an existing product-backed ticket |

Dedupe statuses:

```yaml
dedupe:
  status: same_claim_same_format | same_claim_better_baseline |
    same_topic_new_trend | same_artifact_more_polish | novel
  decision: reject | allow | revise
  compared_against:
    - ops-memory
    - tickets/archive/TASK-XXXX/artifacts/example.md
    - .farplane/feed-scout/ledger.jsonl
```

Portfolio selection should be explicit:

```yaml
portfolio_selection:
  worker_cap:
  selected_lanes:
  skipped_lanes:
  reason:
  one_ticket_wave_exception:
```

### 4. Crystallize Hypotheses

Every selected opportunity becomes a concrete hypothesis before it can become a
ticket spec.

```yaml
hypothesis:
  id: HYP-YYYYMMDD-001
  product_lane: ablations
  title: Proof-ticket templates reduce stale completion ambiguity
  belief: Structured proof sections make ticket closeout less ambiguous.
  evidence_refs:
    - tickets/archive/TASK-0275/ticket.md
    - bin/validators/check_ticket_closure_gate.py
  baseline: Recent closeouts without strict proof/closure template.
  variant: Closeouts with proof template plus closure gate.
  measurement:
    - stale active ticket count
    - metadata failures
    - closure ambiguity notes
  measurement_method: Compare a fixed sample of archived closeouts and record
    ambiguity/stale-ticket observations in the artifact.
  big_claim: Farplane proof tickets make false completion harder than ordinary prompt-only work.
  audience_tension: serious AI builders lose trust when agents say "done" without inspectable proof.
  surprise_factor: baseline agents may produce plausible completion prose while leaving missing proof.
  external_or_default_baseline: prompt-only or no-template baseline, not only Farplane-vs-Farplane.
  artifact_level: ablation_proof_report
  dedupe_status: same_claim_better_baseline
  expected_decision: accept template/closure-gate proof, revise it, or reject
    the hypothesis as unsupported.
  output_artifact: tickets/TASK-XXXX/artifacts/proof-template-ablation.md
  products_md_contribution: Trust ablations output with reusable proof report.
  product_reward: accepted or rejected trust claim.
  expected_reward: Fewer stale tickets and cleaner Pulse admission.
  guard: Use existing local evidence only; no broad refactor.
```

### 5. Specificity Gate

Ask these before rendering any ticket:

```text
Does it name a products.md product lane or artifact workflow?
Does it name a concrete hypothesis or content angle?
Does it name a big claim, audience/operator tension, and surprise factor?
For audience-facing claims, does it compare against an external, default, normie, no-template, vanilla-agent, or competitor-like baseline when possible?
Does it name exact evidence, code, ticket, report, or artifact inputs?
For ablations, does it name baseline, variant, measurement method, and expected decision?
For experiments, does it name baseline/current behavior, proposed change, measurement method, and expected decision?
For content, does it name audience, hook, content job, format, artifact level, and human-gated final action?
Does it name the output artifact?
Is the output level strong enough for the lane, or is this just a note/review/capture/admin artifact?
Does dedupe say this is novel, a better baseline, a new trend on the same topic, or a real polish step?
Does it have a measurable or reviewable reward plus products.md contribution?
Does it include a product-backed KPI from bindings metrics, not only a generic
maintenance or cross-product coordination KPI?
Can a worker start immediately?
Can it finish without asking Kenji, unless only the final action is gated?
Is it product output rather than generator/Pulse/metadata cleanup, unless it
directly unblocks a named existing product-backed ticket?
Does it include validator-compatible lifecycle/admission metadata: phase planning,
status todo, ready true, approval_required false, blocked_by empty, claimed_by
empty, valid human_gate, and dependencies either satisfied or named as blockers?
```

If any answer is no, keep discovery in the parent beat, return a scout request,
or return `blocked_report`. Do not create a worker ticket.

### 6. Render Ticket Specs

Return ticket specs in this shape:

```yaml
executable_ticket_spec:
  lifecycle_metadata:
    phase: planning
    status: todo
    ready: true
    approval_required: false
    blocked_by: []
    claimed_by:
    depends_on: []
    human_gate: none | [post|publish|spend|deploy|external_contact|account_mutation|destructive_cleanup, "reason"]
  title:
  product_lane:
  products_md_contribution:
  big_claim:
  audience_tension:
  surprise_factor:
  dedupe_status:
  artifact_level:
  review_surface:
  hypothesis_id:
  hypothesis:
  baseline_or_current_behavior:
  variant_or_proposed_change:
  measurement_method:
  expected_decision_or_content_job:
  inputs:
  output_artifact:
  scope_in:
  scope_out:
  stop_condition:
  validations:
  dependency_expectations:
    - no unresolved dependency may appear in an admitted ready spec
    - if a required dependency is incomplete, set ready false in the eventual ticket and put the dependency in blocked_by instead of returning it as proceedable
  reward:
    kpi_rewards:
      - kpi_id:
        expected_reward:
    product_reward:
    guard:
  worker_prompt_notes:
    - do not decide whether this is worth doing
    - do not create more tickets
    - produce the named artifact and write proof
    - use worker-artifact-review-request when the artifact is ready, unless review_notify is explicitly none with a reason
    - bind feedback_channel=telegram, feedback_policy=ask_when_artifact_ready, and the worker-thread reply route
    - send the Telegram review request, write the review-cycle receipt, and satisfy the turn exit gate before stopping
    - record fallback only when telegram-message proves the route, credentials, or phone-readable review surface is unavailable
```

## Examples

Good:

```text
Ablate proof-ticket template against no-template closeouts
Compare Farplane ticket-as-program against vanilla Codex skill creation on the same task
Experiment with compact human_gate/frontmatter shape on archived tickets
Create storyboard for "most agents fake done because they lack proof contracts" using TASK-0275 and a no-template baseline
```

Bad:

```text
Create first ablation proof
Write evidence content
Find experiment candidates
Plan next productization wave
Research what we should do next
Prepare evidence-fidelity feedback capture note
Review the content packet as the next distribution worker ticket
```

## Ticket Spec Examples

Ablation ticket spec:

```yaml
title: Ablate proof-ticket template against no-template closeouts
lifecycle_metadata:
  phase: planning
  status: todo
  ready: true
  approval_required: false
  blocked_by: []
  claimed_by:
  depends_on: []
  human_gate: none
product_lane: ablations
products_md_contribution: Trust ablations output; reusable proof report for a harness trust claim.
hypothesis: Proof-ticket templates reduce stale completion ambiguity.
baseline_or_current_behavior: Archived closeouts before strict proof/closure template.
variant_or_proposed_change: Closeouts with proof template plus closure gate.
measurement_method: Compare a fixed local sample for stale active tickets, metadata failures, and closure ambiguity notes.
expected_decision_or_content_job: accept, revise, or reject the proof-template trust claim.
inputs:
  - tickets/archive/TASK-0275/ticket.md
  - bin/validators/check_ticket_closure_gate.py
output_artifact: tickets/TASK-XXXX/artifacts/proof-template-ablation.md
reward:
  product_reward: accepted or rejected trust claim
```

Experiment ticket spec:

```yaml
title: Experiment with compact human_gate/frontmatter shape on archived tickets
lifecycle_metadata:
  phase: planning
  status: todo
  ready: true
  approval_required: false
  blocked_by: []
  claimed_by:
  depends_on: []
  human_gate: none
product_lane: experiments
products_md_contribution: Experiment report with baseline, variant, measurement, and decision.
hypothesis: A compact `human_gate: [tag, reason]` shape reduces metadata friction without weakening final-action gates.
baseline_or_current_behavior: Current archived tickets with verbose or stale approval/human-gate metadata.
variant_or_proposed_change: Rewritten fixture examples using compact human_gate shape.
measurement_method: Apply both shapes to a fixed fixture sample and compare metadata validation clarity, stale-gate count, and reviewer ambiguity notes.
expected_decision_or_content_job: accept compact shape, revise field contract, or reject as not worth changing.
inputs:
  - farplane/bindings.yaml
  - tickets/templates/ticket.md
  - selected archived ticket fixtures
output_artifact: tickets/TASK-XXXX/artifacts/human-gate-frontmatter-experiment.md
reward:
  product_reward: validated improvement or rejected hypothesis
```

## Scout Boundary

Use a scout request only when premise discovery itself is too broad for the
current Pulse beat. Scout requests must ask for ranked opportunity packets with
evidence refs, not tickets. Pulse or this skill still performs final selection,
specificity gating, and ticket rendering.

```yaml
scout_request:
  question:
  sources:
  expected_output: ranked_opportunity_packets_with_feature_behavior,
    baseline_or_current_behavior, variant_or_proposed_change,
    measurement_method, expected_decision_or_content_job, evidence_refs,
    product_reward, and candidate_output_artifact
  hard_stop: no ticket specs, no external mutations, no final recommendations without evidence refs or candidate output artifact
```
