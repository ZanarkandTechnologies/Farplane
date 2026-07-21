---
name: customer-research
description: "Turn a person, profile link, or call target into a sourced customer research report and conversation plan before a customer call."
tier: 3
group: research
source: local
template_uses:
  skill-template: "0.3.7"
eval: evals/evals.json
allowed-tools: Read, Glob, Grep, web_search
common_chains:
  after: ["research", "solution-shaping"]
---

# Customer Research

## Context

Use this when the operator has a call, intro, prospect, customer, partner, or
domain expert and needs enough grounded context to have a useful conversation.
The normal output is a Markdown report linked to canonical entities, not a CRM
pipeline record.

Reports use minimal frontmatter for discovery and entity linking. Put judgment,
confidence, pain hypotheses, questions, and next actions in the report body.
`entity_refs` contains stable IDs compiled from `.farplane/entities/*.md`; one report
may reference a person, their organization, or several related entities. Do not
duplicate entity records or add pipeline fields to the report schema.

Default storage:

- Project-specific target: `.farplane/customer-research/reports/YYYY-MM-DD-<person>.md`
- No project target: `~/.farplane/customer-research/reports/YYYY-MM-DD-<person>.md`
- Canonical entity source: `.farplane/entities/*.md` or `~/.farplane/entities/*.md`
- Compiled entity index: `.farplane/entities/index.json` or `~/.farplane/entities/index.json`
- Cross-skill discovery pattern: `.farplane/*/reports/**/*.md`

Keep the work ethical and source-labeled: use public or supplied business
context, label inference, and do not present private or guessed personal facts
as truth.

## Skill Signature

```text
customer_research(target, call_context?, project_context?, output_root?)
  -> customer_research_report + crm_entity_delta?
state: reads(public/supplied sources, local project context, optional CRM entities);
       writes(skill-local report markdown, optional CRM entity create/update)
gates: target_bound; sources_labeled; inference_labeled; minimal_frontmatter;
       conversation_plan_present; no_private_dossiering
routes: research:user-grounding | research:source-synthesis | solution-shaping
fails: bloated frontmatter; fake certainty; generic pitch; creepy personal dossier;
       uncited claims; CRM pipeline modeling
```

## Phase Boundary

Use `research:*` as the evidence method when the person, company, field, or
source set needs grounding. Use `solution-shaping` only for the "how I can help"
section after the problem hypotheses are labeled. Keep planning and report
authoring inline unless a separate research artifact is needed.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the call target and output location.
  - [ ] Resolve the person's name, supplied links, company or field, call reason,
        and whether the report belongs to a project
        `.farplane/customer-research/` directory or the global
        `~/.farplane/customer-research/` directory.
  - [ ] If the target cannot be identified from the request, ask one narrow
        blocking question instead of researching the wrong person.
- [ ] 2. Gather the smallest useful source set.
  - [ ] Start with supplied links, local project notes, LinkedIn or company pages
        when available, and current public web sources.
  - [ ] Use [research:user-grounding](../research/SKILL.md#researchuser-grounding)
        for role, job, context, friction, and success signals.
  - [ ] Use [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
        when several sources must be normalized before writing.
- [ ] 3. Draft the customer research report from `templates/report.md`.
  - [ ] Resolve stable entity IDs and keep report frontmatter minimal:
        `skill`, `entity_refs`, `name`, `links`, optional `industry`, `relevance`,
        and `created_at`. If the ledger is empty and writes are not approved,
        leave `entity_refs: []`, propose the entity delta in the body, and do
        not claim linkage or run the compile step.
  - [ ] Include who they are, their meaningful story, field overview, company or
        context, sourced facts, labeled inferences, unknowns, and source notes.
- [ ] 4. Shape the conversation.
  - [ ] Use [solution-shaping](../solution-shaping/SKILL.md) for the pain
        hypotheses and "how I can help" section when the call has an outreach,
        client, or MVP angle.
  - [ ] Include warm openers, useful topics, questions to ask, conversation
        risks, and follow-up hooks.
  - [ ] Prefer correction-seeking questions over leading pitch questions.
- [ ] 5. Write and link the artifact.
  - [ ] Save the report in the selected skill-local reports directory.
  - [ ] Ensure every `entity_refs` value resolves to the canonical entity index;
        update the entity Markdown only when the report produced new
        operator-approved relationship state, then run `farplane entities compile`.
- [ ] 6. Finish-check the report.
  - [ ] Frontmatter is minimal, discovery-oriented, and every entity reference
        resolves to the entity index.
  - [ ] Every important claim is sourced, supplied, or clearly labeled as an
        inference or unknown.
  - [ ] The report helps the operator lead a better call rather than pretending
        to know the person privately.
  - [ ] The conversation plan includes concrete questions and at least one
        useful non-obvious angle.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [templates/report.md](templates/report.md) - default customer research report
  template; use for every report unless a project supplies a stricter template.
- [examples/first-call/example.md](examples/first-call/example.md) - short
  example showing minimal frontmatter and report-body reasoning.

## Gotchas

- Do not turn the report into a lead-scoring CRM object. It is a dated,
  skill-owned research artifact linked to stable entity IDs.
- Do not put pain hypotheses, next actions, relationship stage, confidence, or
  project fields in frontmatter.
- Do not hand-maintain report paths on canonical entities. Discover backlinks by
  scanning skill-local report frontmatter for `entity_refs`.
- Do not invent an industry or a replacement project-controller field for
  indexing. Omit optional fields when the mapping is not clear.
- Do not write a generic pitch. Start from the person's likely world, then offer
  hypotheses they can correct.
- Do not imply hidden access to private data. Public/supplied/sourced/inferred
  labels matter here.

## Reference Map

- [../research/SKILL.md](../research/SKILL.md) - load when external source
  grounding is needed.
- [../solution-shaping/SKILL.md](../solution-shaping/SKILL.md) - load when the
  report needs pain hypotheses and a realistic MVP/help angle.

## Output

Write a Markdown report with this frontmatter shape:

```yaml
---
skill: "customer-research"
entity_refs:
  - "person-name"
name: "Person Name"
links:
  - "https://example.com/profile"
industry: "Industry or field, when useful for search."
relevance: "Why this person is relevant to the call or project."
created_at: "YYYY-MM-DD"
---
```

Then include the full research and conversation plan in the body.
