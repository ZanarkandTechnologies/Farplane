---
name: first-value-outreach
description: "Turn one researched person and traceable professional signal into a bounded useful contribution and correction-first unsent outreach packet when earning the first conversation."
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

# First Value Outreach

## Context

Use this skill after `lead-scout` has qualified a candidate and
`customer-research` has resolved one person, their professional role, and at
least one traceable public or supplied work signal. It earns the right to a
first conversation by creating something independently useful before asking
for a sale, partnership, data, or substantial time.

This skill owns contribution selection, bounded creation or builder routing,
the correction-first unsent message, learning objective, and stop conditions.
It does not discover prospects, infer private pain, create a commercial
proposal, or send anything. Route a validated problem and accepted use case to
`personalized-offer`; route a contribution that requires a realistic product
proof through `solution-shaping` before any demo build.

## Skill Signature

```text
first_value_outreach(
  person_ref,
  customer_research_ref,
  professional_signal_ref,
  relationship_goal,
  contribution_budget?,
  proof_refs?,
  channel?,
  owner_artifact?
) -> first_value_contribution_packet
   + contribution_artifact_or_builder_handoff
   + correction_first_unsent_message
   + learning_handoff

state: reads(customer research, professional signal, relationship history,
             available proof and builder artifacts);
       writes(owner_artifact or
              .farplane/first-value-outreach/reports/YYYY-MM-DD-<person>-<signal>.md)
gates: person_researched; professional_signal_traceable;
       value_stands_alone; contribution_bounded; recipient_effort_low;
       private_pain_not_asserted; correction_ask_present;
       demo_route_complete_when_demo_selected;
       external_actions_unapproved
routes: customer-research | research:* | solution-shaping | demo-realism |
        diagramming | infographic | functional-ui |
        impl-plan | copywriting-advisor | personalized-offer | review
fails: generic_free_help; biography_personalization; invented_private_pain;
       manipulative_irresistibility; speculative_large_build;
       pre_research_outreach_template; demo_realism_named_as_builder;
       contribution_without_learning_goal; unauthorized_public_amplification;
       unapproved_outreach_or_crm_write
```

```text
ContributionBudget = {
  effort: "micro" | "small" | "proof-sized",
  recipient_time_cap_minutes: 2 | 5 | 10,
  external_spend: 0,
  finish_gate: "checklist" | "review"
}
```

## Phase Boundary

Keep contribution framing and packaging in this skill. Call a builder only
after the contribution type and effort cap are fixed, and give it a narrower
artifact brief. A demo is optional, not the default: `solution-shaping` must
accept the proof boundary first; `demo-realism` may prepare believable workflow
and data, but does not build the demo; route implementation to the project's
actual demo owner or `impl-plan` when
the build needs a ticket-shaped handoff. Keep commercial offer shaping
downstream until the recipient confirms, corrects, or otherwise validates a
problem or collaboration direction.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read `qa_checklist.md` as preflight and bind the contribution case.
  - [ ] Resolve one person, one `customer-research` report, one traceable
        professional signal, relationship goal, channel, effort cap, and owner
        artifact; route missing person context to `customer-research`.
  - [ ] If the request contains neither a completed person research artifact
        nor one traceable signal, stop at a named `customer-research` handoff
        with the missing inputs. Do not draft even a placeholder outreach
        template; that hides the unresolved relevance problem.
  - [ ] Default to `effort: micro`, five recipient minutes, zero external
        spend, and `.farplane/first-value-outreach/reports/` when no safe budget
        or owner path is supplied.
- [ ] 2. Build the signal-to-value hypothesis without claiming private pain.
  - [ ] Record what the person actually said, published, built, hired for, or
        is professionally responsible for; label supplied, observed,
        researched, inferred, and unknown claims.
  - [ ] Express one falsifiable hypothesis about a job, decision, risk, or
        opportunity the signal makes relevant, plus the correction that would
        invalidate it.
- [ ] 3. Select the smallest contribution that passes the standalone-value gate.
  - [ ] Choose one contribution type: annotated workflow map, teardown,
        benchmark, field note, checklist, calculator, transformed explanation,
        or proof-sized demo.
  - [ ] Reject generic advice, vague offers of free help, disguised discovery
        homework, and artifacts whose value depends on booking a call.
  - [ ] Prefer an inspectable artifact the recipient can use, correct, or
        forward in the stated time cap; do not force a demo when a one-page
        artifact answers the same uncertainty.
- [ ] 4. Define the contribution brief and learning contract.
  - [ ] Name recipient benefit, input evidence, artifact, effort cap, honest
        claim, known limits, recipient action, learning objective, falsifier,
        and stop condition.
  - [ ] Ensure the contribution remains worthwhile if the recipient never
        replies and does not expose confidential, sensitive, or unauthorized
        information.
- [ ] 5. Create the contribution or route one bounded builder handoff.
  - [ ] Create simple text/analysis artifacts directly; use `solution-shaping`
        before product proof. Use `demo-realism` only to shape believable
        workflow/data when needed, then route the accepted brief to the actual
        project demo owner or a ticket through `impl-plan`;
        use `diagramming` or `infographic` when a static artifact is sufficient.
  - [ ] Permit a proof-sized demo only when the packet explains why a static
        artifact cannot test the uncertainty, bounds one workflow and one
        decision, names the build owner and inspection surface, and preserves
        the same zero-spend and external-action gates.
  - [ ] For every selected demo, include an explicit route receipt:
        `solution boundary: accepted | blocked`; `realism preparation:
        required with demo-realism | not_required`; `implementation owner:
        <project demo owner | ticket via impl-plan>`; and
        `inspection surface: <path or expected artifact>`. A generic “builder
        handoff” does not pass.
  - [ ] Do not exceed the contribution budget, publish about the person, use
        their likeness or endorsement, spend money, or request private data.
- [ ] 6. Package one correction-first message.
  - [ ] Use `copywriting-advisor` when final wording quality matters, grounded
        in the contribution packet rather than biography theater.
  - [ ] Lead with the useful artifact and its relevant signal, state the limit,
        ask one easy correction or redirect question, and make the no-response
        path comfortable; do not ask them to invent a task for the agency.
  - [ ] Keep the message and any follow-up unsent; name the exact human
        approval required before contact or public amplification.
- [ ] 7. Finish-check, review, and hand off the learning.
  - [ ] Render `templates/first-value-contribution.md`, apply
        `qa_checklist.md` again, and use `review` for material customer-facing
        packages.
  - [ ] Return `send | revise | stop` readiness, the unsent message, artifact
        or builder handoff, evidence gaps, approval gate, and the observation
        that would route the case to `personalized-offer`.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [First value contribution packet](templates/first-value-contribution.md) —
  render for each durable contribution case.
- [Construction operator example](examples/construction-operator/example.md) —
  use to calibrate standalone value, restraint, and correction-first wording.

## Gotchas

- “Let me know if you need free AI help” transfers all problem definition work
  to the recipient and is not first value.
- Hard-to-ignore means relevant, useful, inspectable, and low effort—not
  coercive, guaranteed, artificially scarce, or impossible to refuse.
- Turning a person's public idea into public content requires separate
  permission; private delivery of a credited draft does not authorize posting.
- A polished demo can still fail when it guesses the workflow, demands setup,
  or costs more than the learning it can produce.

## Reference Map

- [First Value Outreach QA checklist](qa_checklist.md) — read before execution
  and apply again before completion.
- [Behavior eval cases](evals/evals.json) — run when changing contribution,
  restraint, routing, or external-action behavior.
- [Customer Research](../customer-research/SKILL.md) — use when the person,
  professional signal, or conversation context is unresolved.
- [Personalized Offer](../personalized-offer/SKILL.md) — use only after a
  problem, use case, or collaboration direction is accepted enough to package
  a commercial or partnership offer.

## Output

Write or return one `FirstValueContributionPacket`, one contribution artifact
or bounded builder handoff, one correction-first unsent message, a learning
handoff, readiness verdict, and explicit approval gates. Never imply that
contact, publication, CRM mutation, enrichment, or spend occurred without
approval and evidence.
