---
name: outreach-impl-plan
description: "Turn an outreach idea, strategy, and candidate evidence into an approval-ready campaign ticket with waves, advisor actions, CRM proposal, gates, and proof."
tier: 3
group: sales
source: local
template_uses:
  skill-template: "0.3.8"
  skill-qa-checklist: "0.1.0"
  skill-surface-budget: "0.1.0"
qa_checklist: qa_checklist.md
eval: evals/evals.json
allowed-tools: Read, Glob, Grep, Bash, web_search
---

# Outreach Impl Plan

## Context

Use this skill when an outreach idea, relationship strategy, candidate pool,
or proof direction must become an executable campaign ticket. This is the
outreach analogue to `content-impl-plan`: it owns the parent plan, campaign
lock, waves, advisor action list, CRM delta proposal, measurement route, and
approval boundaries. It does not perform prospect research, build
contributions, write offers, mutate CRM, send messages, publish, or replace its
child skills.

The campaign artifact owns operational wave state. CRM owns durable people,
companies, relationship context, and validated opportunities—not the campaign
queue. Plan approval admits local execution only when the accepted ticket says
so; every external send, publication, enrichment, spend, promise, and CRM write
still follows its exact gate.

## Skill Signature

```text
outreach_impl_plan(
  idea,
  strategy,
  candidate_pool_ref?,
  proof_refs?,
  constraints?,
  campaign_ref?,
  artifact_owner?
) -> outreach_campaign_ticket
   + advisor_action_list
   + campaign_program
   | blocked_report

state: reads(opportunity research, lead-scout packets, customer research,
             first-value and offer reports, proof assets, CRM entities,
             metrics contracts, qa_checklist.md);
       writes(artifact_owner or
              .farplane/outreach-impl-plan/reports/YYYY-MM-DD-<campaign>.md)
gates: objective_and_learning_named; evidence_boundary_visible;
       wave_logic_present; advisor_actions_executable;
       every_action_has_evidence_writeback;
       campaign_lock_passed; crm_delta_proposed_not_implied;
       metrics_and_review_point_named; external_actions_gated;
       external_send_action_and_receipt_present_when_contact_in_scope;
       metric_linkage_ids_bound
routes: agency-opportunity-research | lead-scout | customer-research |
        first-value-outreach | solution-shaping | demo-realism |
        personalized-offer | copywriting-advisor | metric-advisor |
        review | goal-advisor
fails: strategy_prose_without_program; bulk_message_as_campaign;
       parent_reimplements_children; wave_without_hypothesis;
       action_without_evidence_writeback;
       crm_as_campaign_runtime; inferred_opportunity_as_fact;
       plan_approval_implies_send; metrics_equal_activity_only;
       reviewed_message_without_send_action; unbound_metric_linkage
```

```text
AdvisorAction = {
  order, wave, target?, owner, input, output,
  acceptance_check, blocker, approval_gate, evidence_writeback
}

advisor_action_complete(row) -> pass only when every required field is a
non-empty cell. `target` may be a named cohort; `blocker` may be `none` only
with a reason; `approval_gate` may be `none` only for read-only local work; and
`evidence_writeback` must name a discoverable surface. A blocker described
elsewhere in the plan does not repair a missing action-row field.
```

## Phase Boundary

Plan inline and route only the child work needed to make the campaign ticket
executable. The normal result is `draft | awaiting_approval`; do not invoke
execution owners merely because they appear in the action list. After explicit
campaign approval, native ticket/Goal execution may materialize the approved
CRM delta and start local child work. Approval of the campaign never approves
an exact message, send, post, enrichment purchase, customer promise, or other
external action.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the campaign brief and read `qa_checklist.md` as preflight.
  - [ ] Resolve campaign idea, business objective, learning question,
        relationship strategy, audience, candidate evidence, proof assets,
        channels, budgets, review point, constraints, and artifact owner.
  - [ ] Route missing market/relationship strategy to
        `agency-opportunity-research`; route missing named candidates and
        access evidence to `lead-scout`. Stop with a blocked report when no
        sourced candidate pool or falsifiable campaign thesis can be formed.
- [ ] 2. Define campaign thesis, waves, and falsification logic.
  - [ ] State the objective, audience, relationship lanes, why-now evidence,
        value thesis, learning questions, campaign-level success evidence, and
        conditions that would revise or stop the campaign.
  - [ ] Group candidates into small waves by shared hypothesis and evidence
        maturity, not merely seniority; name entry, exit, promotion, and stop
        conditions plus the review point before expanding.
- [ ] 3. Compile the advisor action list without duplicating child workflows.
  - [ ] Route person evidence to `customer-research`, useful contribution
        design to `first-value-outreach`, accepted proof boundaries to
        `solution-shaping`, optional realism preparation to `demo-realism`,
        validated commercial or partnership offers to `personalized-offer`,
        and final message wording to `copywriting-advisor`.
  - [ ] Give every action an order, wave, target or cohort, owner skill, input,
        output, acceptance check, blocker, approval gate, and evidence
        writeback. Use a project-local demo or metrics owner when the project
        has one; otherwise name the generic implementation or `metric-advisor`
        route without inventing a missing skill.
  - [ ] Preserve the complete `AdvisorAction` columns in every action table.
        Block campaign lock when a row omits or leaves blank `blocker`,
        `approval_gate`, or `evidence_writeback`; plan-level prose is not a
        substitute for the per-action contract.
  - [ ] Do not use shorthand such as `same routes as Wave 1`, arrows, or a
        multi-skill chain as an action owner. Every admitted child action has
        one owner and its own complete row. If a later wave is not yet admitted,
        represent it only as one `outreach-impl-plan` re-planning action whose
        output is revised future rows; do not imply those child actions exist.
  - [ ] Treat an action row with a blank or generic evidence writeback as
        incomplete. Name the report, CRM entity proposal, campaign stage,
        event/observation, proof artifact, or review receipt that will make the
        result discoverable to the next action.
- [ ] 4. Compile CRM, state, metrics, and approval contracts.
  - [ ] Propose a diff-shaped CRM materialization set for sourced people and
        companies. Create opportunity deltas only for validated problems or
        collaboration directions; do not store campaign queue stages as CRM
        truth or edit generated CRM projections.
  - [ ] Keep candidate operational stages in the campaign artifact:
        `queued | researching | contribution_planned | contribution_ready |
        send_review | sent | replied | validated | stopped`.
  - [ ] Bind stable `campaign_id`, `person_id`, and opaque interaction
        `offer_id` values before any planned `outreach_sent` or
        `prospect_responded` event. For first-value outreach, `offer_id` is an
        attribution key for the contribution/message bundle, not proof that a
        commercial offer or CRM opportunity exists.
  - [ ] When contact is in scope, place an explicit send action after the
        per-person review and before metrics/review. Its input must be the exact
        approved person, artifact, message, and channel; its output must be a
        `send_receipt | stopped_receipt`; its blocker must include missing
        operator approval or unavailable provider route; and its writeback must
        name the receipt, campaign stage, and `outreach_sent` event surface.
  - [ ] Define campaign and per-wave observations, review cadence, evidence
        owner, and exact gates for CRM writes, private data, enrichment, spend,
        contribution production, sends, publishing, proposals, and promises.
- [ ] 5. Run the campaign lock and render the campaign ticket.
  - [ ] Require a sourced thesis, small first wave, personalized contribution
        route, ordered action list with non-empty evidence writebacks, CRM
        proposal, metrics beyond activity, review point, stop conditions, and
        separate local/external approvals.
  - [ ] Block campaign lock when contact is intended but no post-review send
        action exists, or when required metric linkage IDs are unbound.
  - [ ] Block generic mass outreach, one message for every person, demos with
        no proof need, unsupported opportunities, CRM-as-runtime, send approval
        hidden inside plan approval, shorthand/multi-owner action rows, or waves
        that cannot teach the next wave.
  - [ ] Render `templates/outreach-campaign-ticket.md`; use the supplied owner
        path or the default reports directory and leave state `draft` or
        `awaiting_approval` unless exact acceptance evidence already exists.
- [ ] 6. Finish-check and hand off execution.
  - [ ] Apply `qa_checklist.md` again and use `review` for material campaigns.
  - [ ] Return the plan verdict, campaign artifact, advisor action list,
        blocked actions, proposed CRM delta, explicit approval request, and the
        first execution action. Route an accepted long-running campaign to a
        ticket or `goal-advisor`; do not execute it inside this planning skill.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [Outreach Campaign Ticket](templates/outreach-campaign-ticket.md) — render
  for every durable campaign plan.
- [Industrial expert wave example](examples/industrial-expert-wave/example.md)
  — calibrates small-wave learning, advisor ownership, and CRM restraint.

## Gotchas

- A list of prospects and one reusable message is not a campaign program.
- Plan approval, CRM approval, contribution budget, and exact send approval are
  separate permissions even when the operator intends to move quickly.
- CRM may record durable relationship truth; it must not become the mutable
  queue for campaign execution.
- The parent plan names child inputs and acceptance checks. It does not copy the
  child skill's entire research, contribution, offer, or copy workflow.

## Reference Map

- [Outreach Impl Plan QA checklist](qa_checklist.md) — read before planning and
  apply again before returning a campaign.
- [Behavior eval cases](evals/evals.json) — run when changing campaign lock,
  advisor routing, CRM, metrics, or permission behavior.
- [Content Impl Plan](../content-impl-plan/SKILL.md) — use only as the parent
  plan/advisor-action structural reference, not as an outreach dependency.
- [First Value Outreach](../first-value-outreach/SKILL.md) — route one
  researched person's contribution design here.
- [Personalized Offer](../personalized-offer/SKILL.md) — route only after a
  use case, proof, or collaboration direction is accepted.

## Output

Write or return one `OutreachCampaignTicket`, ordered `AdvisorAction[]`, the
campaign lock verdict, proposed CRM delta, metrics and review contract,
approval inventory, blocked report when applicable, and the first downstream
execution action. Never imply that CRM mutation, research, artifact production,
contact, publishing, spend, or customer commitment occurred because it appears
in the plan.
