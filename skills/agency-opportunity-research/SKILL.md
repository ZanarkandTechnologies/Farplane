---
name: agency-opportunity-research
description: "Turn an industry, company, person, or call premise into a sourced agency opportunity case and solution-shaping handoff when deciding whom to approach and what to offer."
tier: 3
group: intelligence
source: local
template_uses:
  skill-template: "0.3.2"
  skill-qa-checklist: "0.1.0"
qa_checklist: qa_checklist.md
eval: evals/evals.json
---

# Agency Opportunity Research

## Context

Use this pipeline when an agency needs to turn an industry or
supply-chain premise, company, person, or call into a reviewable commercial
opportunity. The skill owns connected opportunity assembly: target companies,
people and roles, relationship strategy, problem hypotheses, evidence,
competitor context, proof needs, and the next research or solution-shaping
route.

This skill composes existing methods. Use `research` for external evidence,
`lead-scout` for candidate discovery, `customer-research` for a known person or
call target, `brainstorm` for first-principles option space, and
`solution-shaping` only after the target/problem frame is sufficiently
grounded. Do not reimplement those skills inside this pipeline.

## Skill Signature

```text
agency_opportunity_research(
  premise_or_target,
  scope?,
  evidence_budget?,
  context_refs?,
  usecase_roots?,
  owner_artifact?
) -> opportunity_case
   + evidence_refs
   + competitive_positioning_handoff?
   + solution_shaping_handoff?
   + research_gaps
   + next_owner

state: reads(project harness/PRD when present, supplied context, public sources,
             existing research, configured usecase roots, CRM entities,
             company/call artifacts);
       writes(owner_artifact when supplied, otherwise
              .farplane/agency-opportunity-research/reports/YYYY-MM-DD-<slug>.md;
              returns inline
              when the caller requested answer-only or prohibited edits)
gates: premise_bounded; sources_traceable; provenance_labeled;
       relationship_strategy_named; inferred_pains_not_presented_as_facts;
       solution_shaping_requires_problem_frame; competitor_labels_criteria_bounded;
       external_actions_approval_gated
routes: deep-interview | advise | research:* | lead-scout |
        customer-research | brainstorm | solution-shaping |
        usecase-experiment-loop | demo-realism | impl-plan | review
fails: generic company list; invented prospect facts; lead score without
       relationship strategy; solution pitch without evidence; duplicate
       child-skill logic; unsupported_best_claim; duplicate_buyer_choice_sidecar;
       CRM/outreach/publishing/account action without approval
```

## Phase Boundary

The normal result is an `OpportunityCase`, not a sent campaign, CRM record,
production schema, graph database, map UI, or finished demo. Route accepted
problem/offer work to `solution-shaping`; route proof experiments to
`usecase-experiment-loop`; route accepted proof that needs packaging through
the caller's selected demo-realism and implementation path.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read `qa_checklist.md` as preflight guardrails and bind the intake.
  - [ ] Classify it as `industry_premise`, `company`, `person`, or `call`.
  - [ ] Record objective, industry/value-chain boundary, geography, exclusions,
        evidence budget, context refs, and intended relationship outcomes.
  - [ ] If scope is materially branching, use `deep-interview` or `advise`
        before research rather than silently choosing a market boundary.
  - [ ] If geography is missing and no safe default follows from supplied
        context, keep company/person claims blocked, map archetypes only, and
        name geography as the next decision.
- [ ] 2. Inspect local state before external research.
  - [ ] Search existing research, opportunity artifacts, usecases, company
        profiles, calls, tickets, and source refs; reuse stable IDs and avoid
        duplicate records.
  - [ ] Read `.farplane/entities/*.md` when present. Treat frontmatter as
        structured identity/relationship state and the Markdown body as durable
        unstructured context; do not rely only on compiled JSON.
  - [ ] Name what the agency already knows, what is stale, and what remains unknown.
  - [ ] Write into the supplied owner artifact; if none exists, use
        `.farplane/agency-opportunity-research/reports/YYYY-MM-DD-<slug>.md` and
        create only the required parent directory. Return inline instead when
        the caller asked only for an answer or prohibited filesystem edits.
- [ ] 3. Build the market and relationship map.
  - [ ] For industry intake, use `research` plus `lead-scout` to identify
        supply-chain/value-chain segments, 10-20 candidate companies, relevant
        locations/projects, and public sources unless scope specifies otherwise.
  - [ ] For company intake, identify its segment, business model, adjacent
        companies, current public priorities, and plausible buyer/partner roles.
  - [ ] For person/call intake, use `customer-research` and connect the person,
        role, company, known statements, and relationship history.
  - [ ] Classify each relationship as `sell_to`, `partner_or_jv`, `channel`,
        `data_or_delivery_partner`, `learn_from`, or `uncertain`; do not collapse
        these into one lead score.
- [ ] 4. Ground people, jobs, and problem hypotheses.
  - [ ] For each shortlisted role, record job/decision, stakes, current-workflow
        evidence, likely friction, KPI or success signal, fit rationale, and a
        correction question.
  - [ ] Label claims `supplied`, `observed`, `researched`, `inferred`, or
        `unknown`; attach source, observation date, confidence, and freshness.
  - [ ] Route uncertain user jobs or pains to `research:user-grounding`; do not
        treat role stereotypes or private-company guesses as facts.
- [ ] 5. Add competitor and capability context.
  - [ ] Use `research:competitor`, `research:parity`, or source synthesis when
        current vendors, startups, internal approaches, open-source tools, or
        peer workflows could change the opportunity.
  - [ ] Select an `established_benchmark` and `emerging_specialist` only from
        dated evidence and an explicit buyer-job criterion. Do not call either
        “best” without defining and sourcing what best means; record a gap when
        no credible specialist exists.
  - [ ] Compare both with the agency/custom-execution path on the same fields:
        best suited for, strengths, limitations, proof/maturity, time to first
        useful result, customization/integration fit, choose-when guidance, and
        evidence that could invalidate the angle.
  - [ ] When an accepted demo needs the comparison, hand the concise sourced
        conclusion directly to its customer-facing landing surface as a
        semantic feature matrix with capabilities as rows and providers as
        columns, never vendor-summary rows or side-by-side cards. Use
        evidence-safe states such as documented, demonstrated here, and not
        shown in reviewed public material. Add one
        optional `reference/competitive-landscape.md` only when deeper evidence
        must be reused; never add a duplicate buyer-choice sidecar.
- [ ] 6. Explore and shape only when the evidence gate passes.
  - [ ] Use `brainstorm` for first-principles contrast and candidate directions.
  - [ ] Require an actor, job, stakes, constraints, source status, and problem
        boundary before routing to `solution-shaping`.
  - [ ] Preserve at least three viable offer shapes when three genuinely exist;
        select one only through the owning advice/solution-shaping judgment.
- [ ] 7. Match the opportunity to existing proof.
  - [ ] Search configured usecase roots and existing proof packages before
        proposing new work.
  - [ ] Classify the proof as `existing_skill`, `adapted_variant`,
        `new_usecase_experiment`, `report_or_analysis`, or `no_proof_yet`.
  - [ ] State the proof claim, required inputs, evidence limits, missing
        capability, and why a polished demo is or is not necessary.
  - [ ] With weak evidence, return a research gap and correction plan rather
        than manufacturing an offer; with accepted existing proof, reuse and
        route it instead of rebuilding it.
- [ ] 8. Assemble and review the OpportunityCase.
  - [ ] Use `templates/opportunity-case.md`; keep stable record IDs and explicit
        graph-shaped links without choosing a database or map implementation.
  - [ ] Name research gaps, confidence revisions, call questions, next action,
        next owner, and approval gates.
  - [ ] Propose CRM entity changes with stable fields/references in frontmatter
        and concise durable relationship context, cues, hypotheses, open
        questions, and follow-up rationale in Markdown bodies. Link full reports
        through `report_refs`, `source_refs`, or body links; reserve
        `entity_refs` for canonical entity IDs.
  - [ ] Apply CRM changes and run `farplane entities compile` only after explicit
        approval of that exact entity delta; report or offer approval alone is
        not CRM-write approval. Never hand-edit `index.json`; resolve the
        entity through its lookup row and follow `path` when full frontmatter
        or Markdown body context is needed.
  - [ ] Apply `qa_checklist.md` again and use `review` for material cases before
        presenting a target list, offer, or proof package as ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Use [Opportunity Case template](templates/opportunity-case.md) for the normal
artifact. It is an artifact schema, not a storage/database commitment.

Use [data-center construction example](examples/data-center-construction/example.md)
as a positive reference for archetype-first deferral when real entities are not
yet sourced.

## Gotchas

- A list of logos or contacts is not an opportunity case.
- Geographic coordinates do not prove a commercial relationship or problem.
- A role-based pain hypothesis stays inferred until sourced or corrected.
- Do not make every opportunity end in a polished demo page; proof can be a report,
  workflow run, analysis, calculator, dataset, or honest evidence gap.
- Do not let a project-specific demo runtime define this upstream contract.

## Reference Map

- [Opportunity Case template](templates/opportunity-case.md) — load when
  assembling or reviewing the final artifact.
- [Agency Opportunity Research QA checklist](qa_checklist.md) — read before execution
  and apply again before completion.
- [Behavior eval cases](evals/evals.json) — run when changing routing,
  provenance, or handoff behavior.
- [Data-center construction example](examples/data-center-construction/example.md)
  — use when checking artifact quality or unsourced-premise behavior.

## Output

Return or write one traceable `OpportunityCase` with evidence refs, research
gaps, relationship strategies, proof match, correction questions, approval
gates, and a concrete next owner. Never imply external action occurred unless
the operator explicitly approved it and evidence confirms it.
