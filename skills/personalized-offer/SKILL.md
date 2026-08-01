---
name: personalized-offer
description: "Turn one researched person, company context, and accepted use case into a source-bounded personalized offer report and unsent outreach package when an agency is ready to approach them."
tier: 3
group: marketing
source: local
template_uses:
  skill-template: "0.3.2"
  skill-qa-checklist: "0.1.0"
qa_checklist: qa_checklist.md
eval: evals/evals.json
---

# Personalized Offer

## Context

Use this skill after an agency has selected one person and one
accepted use case, proof package, or bounded service offer. It creates a dated
report that explains why the offer may matter to this person, which evidence
supports that view, what proof to show, what remains uncertain, and how to ask
for a correction or conversation without pretending to know private pain.

This skill connects existing owners. `customer-research` owns the person's
public career and conversation context; `solution-shaping` owns the realistic
problem/solution boundary; `copywriting-advisor` owns the final message wording
and source-backed copy quality. This skill owns the person-to-use-case fit,
comparison of viable relationship-aware approaches, selected offer, proof
narrative, offer report, outreach packet, and proposed CRM state delta.

## Skill Signature

```text
personalized_offer(
  person_ref,
  company_ref,
  customer_research_ref,
  accepted_usecase_ref,
  proof_refs?,
  usecase_roots?,
  relationship_context?,
  channel?,
  owner_artifact?
) -> personalized_offer_report
   + outreach_drafts
   + crm_entity_delta?
   + next_action

state: reads(customer research, canonical entity frontmatter and Markdown bodies,
             calls/notes, accepted usecase,
             sample data, proof traces, company/market evidence, public or
             supplied career sources);
       writes(owner_artifact or
              .farplane/personalized-offer/reports/YYYY-MM-DD-<person>-<usecase>.md;
              optional operator-approved CRM entity Markdown updates)
gates: person_resolved; accepted_usecase_resolved; career_claims_sourced;
       problem_fit_labeled; viable_approaches_compared; selected_approach_named;
       proof_matches_offer; correction_ask_present;
       crm_delta_review_status_named; outreach_unsent_without_approval
routes: customer-research | research:* | solution-shaping |
        copywriting-advisor | review | telegram-message
fails: creepy_personalization; invented_private_pain; generic_ai_pitch;
       fake_option_frontier; relationship_score_theater; usecase_feature_dump;
       proof_claim_mismatch; unapproved_crm_write;
       unapproved_outreach_or_publish
```

## Phase Boundary

The normal output is a report, unsent drafts, and a proposed CRM delta. The
skill does not discover broad markets, choose unqualified leads, rebuild the
use case, send outreach, publish a page, or mutate external CRM/account state.
Route missing market or qualification work to `agency-opportunity-research`.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read `qa_checklist.md` as preflight and bind the offer case.
  - [ ] Resolve stable person, company, relationship, opportunity, usecase, and
        proof refs plus channel, desired action, and owner artifact.
  - [ ] Require one selected person and one accepted usecase/proof direction;
        route missing qualification to `agency-opportunity-research`.
  - [ ] Use the supplied owner artifact or default to
        `.farplane/personalized-offer/reports/YYYY-MM-DD-<person>-<usecase>.md`;
        return inline only for answer-only requests.
- [ ] 2. Verify the person research and relationship state.
  - [ ] Load existing `customer-research` reports and canonical entities before new
        research; use `customer-research` when career history, role, company,
        current interests, or call context is missing or stale.
  - [ ] Read entity Markdown bodies for durable relationship history,
        personalization cues, open questions, relevant proof, and follow-up
        context. Body prose still needs linked evidence before it is treated as
        verified fact.
  - [ ] Separate `supplied`, `observed`, `researched`, `inferred`, and `unknown`
        claims; attach sources and dates to career or company facts.
  - [ ] Use only professionally relevant public/supplied context. Exclude
        sensitive personal traits, family, health, private contact data, and
        manipulative personal details.
- [ ] 3. Verify the accepted offer and proof.
  - [ ] Read the usecase package, solution brief, sample data, expected output,
        proof trace, review state, and known limits.
  - [ ] Use `solution-shaping` when the offer boundary, V1/V2 split, buyer job,
        decision rights, or proof model is not already accepted.
  - [ ] State what the proof actually demonstrates and what it does not; reject
        personalization that depends on unsupported production, compliance,
        ROI, safety, or company-specific claims.
- [ ] 4. Build the person-to-usecase fit map.
  - [ ] Connect sourced career/role evidence to the current job, likely
        decision or influence, problem hypothesis, usecase outcome, and proof.
  - [ ] For every personalization claim, record evidence, inference level,
        confidence, why it matters, and a correction question.
  - [ ] Distinguish `sell_to`, `partner_or_jv`, `channel`,
        `data_or_delivery_partner`, `learn_from`, and `uncertain`; adapt the ask
        to the relationship instead of forcing a sales CTA.
- [ ] 5. Compare viable approaches using existing resources.
  - [ ] Derive candidates only from the accepted use case, `proof_refs`,
        `usecase_roots`, customer research, canonical entity bodies, project
        context, and supplied `relationship_context`. Do not invent an
        introduction, favor, asset, shared interest, or private preference.
  - [ ] Include exactly three options only when three are genuinely viable;
        otherwise show the smaller honest frontier. A direct commercial ask,
        first-value contribution, warm relationship path, partnership, or
        thoughtful gesture is eligible only when evidence supports it.
  - [ ] Judge each option separately as `low | medium | high | unknown` for
        commercial movement, relationship value, ask burden, and relationship
        risk. Cite evidence and rationale; do not sum the judgments into a
        universal relationship-points score.
  - [ ] Render the compact comparison before the recommendation in both durable
        reports and answer-only requests. Do not collapse the four judgments
        into prose merely because the operator requested one short message.
  - [ ] Select one approach and state why each viable alternative lost. Prefer
        preserving trust when a higher-movement option spends unsupported
        relationship capital or imposes a disproportionate ask.
  - [ ] Keep option ranks and selection logic in the offer report. Only stable
        sourced facts, durable relationship history, cues, and open questions
        may enter a proposed entity Markdown delta.
- [ ] 6. Shape the personalized offer.
  - [ ] Produce one primary offer with target outcome, smallest useful
        engagement, deliverables, proof to show, reason-now hypothesis,
        assumptions, non-goals, and next step.
  - [ ] Explain why this person may care in their language without flattering,
        overclaiming, or narrating their biography back to them.
  - [ ] Include a correction ask that makes it easy to reject the inferred
        problem or redirect the agency to the right owner.
- [ ] 7. Draft channel-ready copy through the copy owner.
  - [ ] Use `copywriting-advisor` with only the selected approach and its
        source/proof pack; keep unsupported copy in explicit hypothesis mode.
  - [ ] Draft a short email/DM opener, a follow-up, a call opener, and a proof
        handoff note only for channels requested by the operator.
  - [ ] Omit unrequested channel sections or mark them `not_requested`; do not
        manufacture a full sequence when one message is enough.
  - [ ] Keep every message unsent and label the exact human approval required
        before contact, publishing, proposal movement, or account mutation.
- [ ] 8. Propose or apply the CRM delta.
  - [ ] Link the report to stable entity IDs through `entity_refs` and
        propose relationship, qualification, opportunity, offer, proof, and
        next-action updates with evidence refs. Keep stable machine fields and
        references in frontmatter; put concise durable relationship context,
        personalization cues, open questions, and follow-up rationale in the
        entity Markdown body.
  - [ ] Put report/evidence paths in `report_refs`, `source_refs`, or Markdown
        body links; reserve `entity_refs` for canonical entity IDs.
  - [ ] Write CRM entity Markdown and run `farplane entities compile` only when the
        operator has explicitly approved that exact entity delta. Approval of
        the offer report or outreach copy does not authorize CRM mutation;
        otherwise return a diff-shaped proposal.
  - [ ] Do not store the full report, speculative pain, or outreach prose as
        CRM frontmatter. Keep full artifacts in report backlinks while allowing
        a sourced durable summary in the entity body.
  - [ ] Do not store approach options, ordinal judgments, selection rationale,
        or computed relationship value in entity Markdown or CRM frontmatter.
  - [ ] Never hand-edit `entities.json`; after an approved Markdown entity
        change, run `farplane entities compile` and confirm compiled records retain
        both `frontmatter` and `body`.
- [ ] 9. Finish-check and review.
  - [ ] Render `templates/personalized-offer-report.md`, then apply
        `qa_checklist.md` again.
  - [ ] Confirm every personal claim is relevant and sourced/labeled, the offer
        fits the proof, the correction ask is credible, and drafts remain unsent.
  - [ ] Use `review` before marking material customer-facing copy or a CRM delta
        ready; name the next owner and evidence that would change the offer.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [Personalized Offer Report](templates/personalized-offer-report.md) — use for
  every durable offer artifact.
- [Operations leader example](examples/operations-leader/example.md) — use as a
  quality reference for respectful, evidence-bounded personalization.

## Gotchas

- A personalized offer is not a mail merge with a biography sentence.
- Career history may explain relevance; it does not prove current private pain.
- Do not force a sales ask when the relationship is partnership, learning, or
  delivery collaboration.
- Do not create three decorative options. The frontier exists to change the
  decision and may contain fewer than three viable approaches.
- A thoughtful gesture is optional and must be professionally appropriate,
  directly supported, and free of quid-pro-quo framing.
- Do not let copy quality hide a weak solution or mismatched proof claim.
- Canonical entity Markdown may hold concise durable relationship memory and
  unstructured context; full research and offer artifacts remain linked reports.

## Reference Map

- [Personalized Offer QA checklist](qa_checklist.md) — read before execution
  and apply again before completion.
- [Behavior eval cases](evals/evals.json) — run when changing personalization,
  proof, CRM, or outreach-gate behavior.
- [Agency Opportunity Research](../agency-opportunity-research/SKILL.md) — use
  when target qualification or relationship strategy is missing.

## Output

Return or write one `PersonalizedOfferReport` with its compact approach
frontier, selected offer, requested unsent drafts, a reviewed or proposed CRM
entity delta, source/proof gaps, approval gates, and a concrete next action.
Never imply contact, publication, or CRM mutation occurred without approval and
evidence.
