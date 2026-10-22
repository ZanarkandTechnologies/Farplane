---
name: prospect
description: "Use for \"prep me for this call\", \"find me leads\", \"look into this company\" or \"research this customer event\": qualify people and companies on a sourced trigger, return one OpportunityCase or a ranked lead list."
source: local
department: sales
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash, web_search
---

# Prospect

## Context

Use this when the operator names an industry, a company, or a person or call
and wants to know whom to approach, why them, why now, and how. It finds and
qualifies targets, grounds the people who pass, and matches the case to proof
the agency already has. One pass returns one `OpportunityCase`, or a ranked
lead list when the operator asks for leads in bulk ("find me 20 leads").

An `event` intake is one new dated event on a customer or prospect the
operator subscribes to (a hire, launch, funding round, post, or release), handed
over by the Feed Scout automation as its own thread. It researches what the
event changes for that account and returns the case for that one entity.

It does not write the message or offer (`approach`), price a proposal
(`proposal-pricing`), run a market-wide competitor study (`research` market),
watch feeds on a schedule (`feed-scout`), or change Wiki pages (`manage-wiki`).
Nothing is sent, enriched with paid data, or written to a CRM here.

## Skill Signature

```text
prospect(target: industry | company | person | call | event, filter?, geography?, depth?: quick | deep,
         output?: case | leads, count?, budget?)
  -> opportunity_case { relationship map + signal cards + proof class + rejection ledger + gaps + call_plan? }
     | lead_list { ranked rows + rejection ledger } ; next_owner
reads: .farplane/entities/*.md, earlier cases, supplied links and notes, public sources, an operator-authorized read-only session
does: binds the intake, scouts and qualifies on why-them/why-now, grounds shortlisted people, matches proof
writes: the caller's artifact, else .farplane/prospect/reports/YYYY-MM-DD-<slug>.md; inline for answer-only requests
returns: the OpportunityCase or lead list, decision approach | research_more | stop, and the next owner
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind the intake and read what is already known.**
  `target -> intake type + boundary + local state | archetypes-only | one narrow question`

  Rule: Classify the intake as `industry`, `company`, `person`, `call`, or
  `event`; an event binds its entity, the event, its source link and date, and
  skips discovery (N2) to qualify that one entity.
  Record the objective, value-chain boundary, geography, exclusions, and
  evidence budget. Read `.farplane/entities/*.md` and earlier cases first and
  reuse their IDs. With no geography and no safe default, map archetypes only
  and name geography as the next decision. When the boundary materially
  branches, show the options and recommend one before researching. An
  ambiguous person ("research Alex") gets one narrow identifying question.

  Example: `"AI for data-center construction", no geography -> owner, MEP
  contractor, and commissioning archetypes with relationship classes; no named
  companies yet`

  Assert:
  - No company or person claim is made outside a bound geography.
  - Supplied call facts stay separate from researched and inferred claims.
- [ ] **N2 — Write the signal ladder, then build the candidate pool.**
  `intake -> signal ladder + query ledger + candidate pool | thin-evidence branch`

  Rule: Before searching, write must-have fit signals, high-intent triggers,
  disqualifiers, weak proxies, and forbidden guesses, plus the hypothesis
  `why them`, `why now`, `why this source`, `why this channel`. Search
  separate discovery lanes (speaker lists, repo activity, job posts, launches,
  complaints, tool migrations, community asks). Prefer supplied and public
  sources; paid data calls follow [data recipes](references/data-recipes.md)
  within the operator's weekly spend cap, price quoted first. Label
  every observation `full_public`, `indexed_snippet`, `operator_supplied`,
  `operator_authorized_session`, `auth_walled`, or `not_inspected`. Dedupe by
  URL, domain, then name. Load [sources](references/sources.md) for platform
  limits and deep-mode sources.

  Assert:
  - A snippet discovers a candidate; it never proves a qualification field.
  - No unrestricted people search is claimed on a network that does not allow it.
- [ ] **N3 — Qualify each candidate and class the relationship.**
  `candidate pool -> shortlist + rejection ledger`

  Rule: Give each candidate one relationship class: `sell_to`,
  `partner_or_jv`, `channel`, `data_or_delivery`, `learn_from`, or
  `uncertain`. Never collapse them into one lead score. Rank by the stated
  filter only: trigger strength, fit, reachable proof, urgency, channel fit.
  Stage-exit check before any deep research: public or supplied evidence of
  fit plus one trigger (pain evidence, access path, timing, or an
  inbound/referral). A persona-only match with no timely trigger goes to the
  rejection ledger.

  With `output: leads`, stop after this node and return the ranked list:
  one row per shortlisted candidate with relationship class, why them, why now,
  the source link and date, and the filter field it ranked on, up to `count`
  (default 20), plus the rejection ledger. Ground people (N4) only for rows
  the operator then picks.

  Example: `founder fits the persona, no post, hire, launch, or referral in
  the last quarter -> rejected near-miss, "no trigger"`

  Assert:
  - Every rejected candidate keeps its failed or unknown field.
  - No wealth, personality, or sensitive-trait scoring.
- [ ] **N4 — Ground the shortlisted people with a Signal Card.**
  `shortlist -> one sourced paragraph + Signal Card per person`

  Rule: Open with one sourced paragraph of at most 150 words: role, one to
  three relevant achievements, why they matter now. The Signal Card holds at
  most three entries per section (goals and pressures, problem hypotheses,
  relationship surfaces, correction questions), each with evidence ref,
  access label, date, confidence, and a falsifier. In `deep` mode with a bound
  company, scan hiring and record coverage per [sources](references/sources.md).
  Hiring is committed investment or a capability need, never dysfunction. An
  operator-authorized session is read-only and bounded.

  Example: `active "trial operations analyst" listing -> "investing in
  readiness-reporting capacity", not "their reporting is broken"`

  Assert:
  - Problem hypotheses stay correctable; none is stated as private fact.
  - An auth-walled profile is recorded as `auth_walled`, never as read.
- [ ] **N5 — Add competitor context and match existing proof.**
  `shortlist + signal cards -> competitor view? + proof class`

  Rule: When vendors or peer approaches could change the case, run `research`
  (market) and name one established benchmark and one emerging specialist
  only from dated evidence against a stated buyer-job criterion; never call
  either "best". Search usecase roots and proof packages, then classify proof
  as `existing_skill`, `adapted_variant`, `new_usecase_experiment`,
  `report_or_analysis`, or `no_proof_yet`. Weak evidence returns a research
  gap, not a manufactured offer.

  Assert:
  - Existing proof is reused before new work is proposed.
  - A demo is not assumed; proof can be a report, run, or calculator.
- [ ] **N6 — Return the OpportunityCase and the next owner.**
  `case -> opportunity_case + decision + next_owner`

  Rule: For a `call` intake, add the call plan: warm openers tied to the
  Signal Card, two or three useful topics, risks to avoid, follow-up hooks,
  and the recommended first move. Render [the template](templates/opportunity-case.md) and decide
  `approach`, `research_more`, or `stop`. Hand `approach` one selected target,
  its relationship class, Signal Card, and proof class. Send durable sourced
  facts to `manage-wiki` with the operator's intent. Anything external (send,
  CRM write, paid enrichment, publish) stays approval-gated and is listed.

  Assert:
  - The case names gaps, correction questions, and one next owner.
  - No contact, CRM, enrichment, or Wiki change is claimed without a receipt.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- A list of logos or contacts is not an opportunity case; the reasons are the work.
- One post, interaction, or job ad is not proof of private pain; keep the
  alternative explanation beside it.
- Location or coordinates do not prove a commercial relationship.
- No private dossiers: family, health, personal life, private contact details,
  and sensitive traits stay out, even when the operator asks for them.
- Social pages (LinkedIn, X) open through the `agent-reach` CLI; logging in,
  exporting cookies, or social actions are never part of research.
- Researching every discovered person wastes the budget; shortlist first.

## Reference Map

- [sources](references/sources.md) - load in N2 and N4: discovery lanes,
  platform limits, deep-mode sources, the authorized-session rules, and the
  hiring scan.
- [data recipes](references/data-recipes.md) - load in N2 for a paid list,
  contact, signal, brief or creator pull: steps, gateway and published cost.
- [opportunity case template](templates/opportunity-case.md) - load in N6.
- [data-center construction example](examples/data-center-construction/example.md)
  - archetypes-only case when geography and entities are not yet sourced.
- [deep person example](examples/deep-person/example.md) - calibrates the
  150-word opening and a three-row Signal Card.

## Output

```yaml
intake: industry | company | person | call | event
output: case | leads
boundary: <objective, value chain, geography, exclusions>
relationship_map: <entity -> sell_to | partner_or_jv | channel | data_or_delivery | learn_from | uncertain, why them, why now, source>
signal_cards: <per shortlisted person: paragraph + <=3 rows per section with falsifiers>
rejection_ledger: <candidate -> failed or unknown field>
proof: existing_skill | adapted_variant | new_usecase_experiment | report_or_analysis | no_proof_yet
gaps: <research gaps, unsearched sources, correction questions>
call_plan: <call intake only: openers, topics, risks, follow-up hooks, first move>
lead_list: <leads output only: ranked rows with class, why them, why now, source and date>
decision: approach | research_more | stop
next_owner: approach | research | manage-wiki | none
```
