---
name: personalized-offer
description: "Turn one researched person, company context, and accepted use case into a source-bounded personalized offer report and unsent outreach package when an agency is ready to approach them."
tier: 3
group: deals
source: local
template_uses:
  skill-template: "0.3.2"
---

# Personalized Offer

## Context

Use this after an agency selects one person and an accepted use case, proof, or
bounded service offer. It creates a dated report explaining relevance, evidence,
proof, uncertainty, and a correction-seeking ask without inventing private pain.

This skill connects existing owners. `customer-research` owns the person's
public career and conversation context; `solution-shaping` owns the realistic
problem/solution boundary; `copywriting-advisor` owns the final message wording
and source-backed copy quality. This skill owns the person-to-use-case fit,
comparison of viable relationship-aware approaches, selected offer, proof
narrative, offer report, outreach packet, and proposed Wiki page delta.

## Skill Signature

```text
personalized_offer(person_ref, company_ref, customer_research_ref,
  accepted_usecase_ref, proof_refs?, usecase_roots?, relationship_context?,
  channel?, owner_artifact?, wiki_publication_intent = preview)
  -> personalized_offer_report + outreach_drafts + wiki_page_delta? + next_action

state: reads(customer research, canonical entity frontmatter and Markdown bodies,
             calls/notes, accepted usecase,
             sample data, proof traces, company/market evidence, public or
             supplied career sources);
       writes(owner_artifact or
              .farplane/personalized-offer/reports/YYYY-MM-DD-<person>-<usecase>.md;
              optional sourced Wiki delta handoff)
gates: person_resolved; accepted_usecase_resolved; career_claims_sourced;
       problem_fit_labeled; viable_approaches_compared; selected_approach_named;
       proof_matches_offer; correction_ask_present;
       wiki_publication_intent_bound; outreach_unsent_without_approval
routes: customer-research | research:* | solution-shaping |
        copywriting-advisor | manage-wiki | review | telegram-message
fails: creepy_personalization; invented_private_pain; generic_ai_pitch;
       fake_option_frontier; relationship_score_theater; usecase_feature_dump;
       proof_claim_mismatch; wiki_apply_without_explicit_intent;
       unobserved_wiki_applied_status; unapproved_outreach_or_publish
```
## Phase Boundary

The normal output is a report, unsent drafts, and a Wiki delta—not broad
discovery, use-case rebuilding, outreach, publishing, or account mutation.
Route missing market or qualification work to `agency-opportunity-research`.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read the first-load Todo List guardrails as preflight and bind the offer case.
  - [ ] Resolve stable person, company, relationship, opportunity, usecase, and
        proof refs plus channel, desired action, and owner artifact.
  - [ ] Require one selected person and one accepted usecase/proof direction;
        route missing qualification to `agency-opportunity-research`.
  - [ ] Bind Wiki intent: direct save/update/publish-to-Wiki language means
        `apply`; preview/no-write or no Wiki direction means `preview`; a
        conflict blocks Wiki publication.
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
- [ ] 8. Preview or apply the Wiki delta.
  - [ ] Link the report to stable entity IDs through `entity_refs` and
        propose relationship, qualification, opportunity, offer, proof, and
        next-action updates with evidence refs. Keep stable machine fields and
        references in frontmatter; put concise durable relationship context,
        personalization cues, open questions, and follow-up rationale in the
        entity Markdown body.
  - [ ] Put report/evidence paths in `report_refs`, `source_refs`, or Markdown
        body links; reserve `entity_refs` for canonical entity IDs.
  - [ ] Pass sourced durable facts and the bound `preview | apply` intent to
        [manage-wiki](../manage-wiki/SKILL.md), which selects pages/entities.
        Direct Wiki write intent is sufficient for apply; offer/copy approval
        alone is not. Source, privacy, ambiguity, and validation still block.
        Apply intent is not proof of application: without an observed Manage
        Wiki apply receipt, report `not_executed`, never `applied` or “saved.”
        Preserve fact-level source refs and name privacy/ambiguity blockers in
        that downstream receipt or intended handoff.
  - [ ] Do not store the full report, speculative pain, or outreach prose as
        CRM frontmatter. Keep full artifacts in report backlinks while allowing
        a sourced durable summary in the entity body.
  - [ ] Do not store approach options, ordinal judgments, selection rationale,
        or computed relationship value in entity Markdown/frontmatter. Never
        edit canonical articles or generated search/graph projections here.
- [ ] 9. Finish-check and review.
  - [ ] Render `templates/personalized-offer-report.md`, then apply
        the first-load Todo List guardrails again.
  - [ ] Confirm every personal claim is relevant and sourced/labeled, the offer
        fits the proof, the correction ask is credible, and drafts remain unsent.
  - [ ] Use `review` before marking material customer-facing copy or a Wiki delta
        ready; name the next owner and evidence that would change the offer.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->
## Templates

- [Personalized Offer Report](templates/personalized-offer-report.md) — use for
  every durable offer artifact.
- [Operations leader example](examples/operations-leader/example.md) — use as a
  quality reference for respectful, evidence-bounded personalization.
## Gotchas

- A personalized offer is not a mail merge; career history may explain
  relevance but does not prove current private pain.
- Do not force a sales ask for partnership, learning, or delivery relationships,
  and do not create decorative options.
- A thoughtful gesture must be relevant, supported, and free of quid-pro-quo framing.
- Do not let copy quality hide a weak solution or mismatched proof claim.
- Canonical articles hold concise durable context; full artifacts remain linked reports.
## Reference Map

- the first-load Todo List guardrails — read before execution and apply again before completion.
- [Behavior eval cases](evals/evals.json) — run when changing personalization, proof, Wiki, or outreach gates.
- [Agency Opportunity Research](../agency-opportunity-research/SKILL.md) — use when qualification or relationship strategy is missing.
- [Manage Wiki](../manage-wiki/SKILL.md) — use for sourced durable Wiki preview or apply intent.
## Output

Return one `PersonalizedOfferReport` with its compact approach frontier,
selected offer, requested unsent drafts, reviewed or proposed Wiki page delta,
source/proof gaps, approval gates, and next action. Never imply contact,
public publication, or Wiki apply occurred without an observed downstream receipt.
