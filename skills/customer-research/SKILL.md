---
name: customer-research
description: "Turn a person, profile link, or call target into a sourced customer research or deep ICP report and conversation plan before outreach or a call."
tier: 3
group: customer
source: local
template_uses:
  skill-template: "0.3.7"
eval: evals/evals.json
allowed-tools: Read, Glob, Grep, Bash, web_search
common_chains:
  after: ["research", "solution-shaping"]
---

# Customer Research

## Context

Use this for a call, intro, prospect, customer, partner, or domain expert who
needs enough grounded context for a useful conversation. The normal output is a
Markdown report linked to canonical Wiki entities, not a CRM pipeline record.

Use deep ICP mode for unusually deep person-level research, buyer psychology,
public professional signals, likely active problems, or “what they care about.”
It may inspect public/supplied professional evidence and a read-only browser
session explicitly authorized by the operator. It must not bypass access
controls, expose auth state, perform social actions, scrape private data, infer
sensitive traits, or present hypotheses as private facts. When a company is
bound, deep ICP also inspects its hiring footprint as evidence of committed
investment and capability needs, never as proof of dysfunction.

Reports use minimal frontmatter; judgment, confidence, pain hypotheses,
questions, and next actions belong in the body. `entity_refs` contains stable
IDs from `.farplane/entities/*.md`. Preview may reference already-existing
canonical IDs, but must omit staged new IDs until apply; use `entity_refs: []`
when no resolved canonical entity exists.

Default report roots are `.farplane/customer-research/reports/` for a project
and `~/.farplane/customer-research/reports/` otherwise. Canonical articles live
under the corresponding `.farplane/entities/`; generated indexes are lookup
projections, so read the matched article path for full context.

## Skill Signature

```text
customer_research(target, call_context?, project_context?, output_root?, mode?,
                  wiki_publication_intent = preview)
  -> customer_research_report | deep_person_icp_report + wiki_delta_proposal?
state: reads(public/supplied/operator-authorized professional sources,
             local project context, optional Wiki articles);
       writes(skill-local report Markdown, optional sourced Wiki delta handoff)
gates: target_bound; sources_labeled; inference_labeled; minimal_frontmatter;
       conversation_plan_present; no_private_dossiering;
       deep_icp_hypotheses_testable; person_signal_card_present;
       hiring_coverage_recorded_when_deep_icp_and_company_bound;
       wiki_publication_intent_bound
routes: research:user-grounding | research:source-synthesis | solution-shaping |
        first-value-outreach | manage-wiki
fails: bloated_frontmatter; fake_certainty; generic_pitch; private_dossier;
       uncited_claims; biography_dump; direct_wiki_or_projection_mutation
```

## Phase Boundary

Use `research:*` when the person, company, field, or source set needs grounding;
use `solution-shaping` only after problem hypotheses are labeled. When the next
goal is contribution before a commercial ask, hand the report and one traceable
professional signal to `first-value-outreach`.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the target, mode, and output location.
  - [ ] Resolve name, supplied links, company/field, call reason, and project or
        global report root. Ask one narrow question if the target is ambiguous.
  - [ ] Bind Wiki intent: save/add/update/write/publish to Wiki or apply these
        Wiki changes means `apply`; preview/no-write or no Wiki direction means
        `preview`; conflicting directions block publication.
- [ ] 2. Gather the smallest useful and ethical source set.
  - [ ] Start with supplied links, local notes, rendered public profiles,
        company pages, and current public sources. Label access as
        `full_public`, `indexed_snippet`, `operator_supplied`,
        `operator_authorized_session`, `auth_walled`, or `not_inspected`.
  - [ ] For deep ICP, load [deep ICP source protocol](references/deep-icp-sources.md)
        and collect repeated professional, interaction, project, language,
        trigger, and hiring signals without private surveillance.
  - [ ] Use [research:user-grounding](../research/SKILL.md#researchuser-grounding)
        for role, context, friction, and success signals; use
        [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
        when several sources need normalization.
- [ ] 3. Draft the report from the applicable template.
  - [ ] Resolve stable Wiki IDs and keep frontmatter to `skill`, `entity_refs`,
        `name`, `links`, optional `industry`, `relevance`, and `created_at`.
        Include only already-resolved canonical IDs. Omit staged new IDs from
        `entity_refs` until apply; stage the diff without claiming linkage.
  - [ ] Include who they are, meaningful story, context, sourced facts, labeled
        inferences, unknowns, and source notes. In deep ICP mode, open with one
        sourced paragraph of at most 150 words and use
        `templates/deep-person-icp.md`; do not narrate a full biography.
  - [ ] Promote only decision-changing signals. Keep the Person Signal Card to
        at most three goals/pressures, three problem hypotheses, three
        relationship surfaces, and three correction questions; attach
        provenance, date, access, confidence, alternative, and falsifier.
- [ ] 4. Shape a useful, correction-seeking conversation.
  - [ ] Use [solution-shaping](../solution-shaping/SKILL.md) for pain hypotheses
        and help angles when the call has an outreach, client, or MVP goal.
  - [ ] Include warm openers, useful topics, risks, follow-up hooks, no more
        than three correction questions, one recommended first move, one
        smallest credible help angle, and an avoid note. Keep these inside the
        Signal Card; add at most four timing bullets only for a timed call plan.
  - [ ] Route not-yet-commercial targets to
        [first-value-outreach](../first-value-outreach/SKILL.md) with one
        traceable signal, relationship goal, evidence gaps, and help angle.
- [ ] 5. Write the report and hand off Wiki changes.
  - [ ] Save the report in the selected report root and ensure each existing
        `entity_refs` value resolves to a canonical Wiki article.
  - [ ] When the report produces sourced durable entity or relationship state,
        pass the evidence and bound `preview | apply` intent to
        [manage-wiki](../manage-wiki/SKILL.md). Direct Wiki write intent is
        sufficient for apply; privacy, source, ambiguity, and validation still
        block. Manage Wiki chooses pages/entities. Never mutate Wiki state here.
- [ ] 6. Finish-check the decision surface.
  - [ ] Important claims are sourced, supplied, or labeled inference/unknown;
        source access is explicit and snippet-only evidence is not overstated.
  - [ ] The opening and Signal Card surface the first decision; promoted claims
        carry confidence plus a falsifier; deep ICP names inspected hiring
        surfaces and distinguishes active, stale, unknown, and none-surfaced.
  - [ ] The report supports a better conversation without pretending to know
        the person privately, and its Wiki handoff or no-write status is clear.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [default report](templates/report.md) — use unless the project is stricter.
- [deep person ICP](templates/deep-person-icp.md) — use for deep ICP mode.
- [first-call example](examples/first-call/example.md) — minimal report example.
- [deep ICP example](examples/deep-person-icp/example.md) — signal mapping
  without private dossiering.

## Gotchas

- This is a dated research artifact, not a lead-scoring CRM object; do not put
  pain, next action, relationship stage, confidence, or project in frontmatter.
- Search snippets, rendered public pages, supplied exports, and auth-walled URLs
  are different evidence classes. One interaction or job post is not proof of
  private pain; preserve status, alternatives, and falsifiers.
- An authorized session expands read visibility, not action permission or
  monitoring scope. Never extract credentials/cookies or perform social actions.
- Discover report backlinks from `entity_refs`; do not maintain report paths on
  canonical articles or bypass `manage-wiki` for article changes.

## Reference Map

- [deep ICP source protocol](references/deep-icp-sources.md) — load only for
  deep ICP evidence gathering, authorized-session inspection, or hiring scans.
- [Research](../research/SKILL.md) — load for external grounding.
- [Solution Shaping](../solution-shaping/SKILL.md) — load for help/solution fit.
- [Manage Wiki](../manage-wiki/SKILL.md) — load for a sourced durable Wiki
  preview or apply handoff.

## Output

Write one report with minimal frontmatter and a sourced conversation plan. Deep
ICP uses the compact Person Signal Card and linked evidence rather than a
source-by-source biography. Return the `manage-wiki` preview or apply receipt
separately and never imply mutation without an observed applied receipt. A
planned handoff is `not_executed`, not a fictional apply receipt.
