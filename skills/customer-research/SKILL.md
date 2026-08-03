---
name: customer-research
description: "Turn a person, profile link, or call target into a sourced customer research or deep ICP report and conversation plan before outreach or a call."
tier: 3
group: research
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

Use this when the operator has a call, intro, prospect, customer, partner, or
domain expert and needs enough grounded context to have a useful conversation.
The normal output is a Markdown report linked to canonical entities, not a CRM
pipeline record.

Use deep ICP mode when the operator asks for unusually deep person-level
research, buyer psychology, public professional signals, likely active problems,
or "what they care about" before outreach. Deep ICP mode may inspect public or
supplied professional evidence, plus professional material visible through an
explicitly operator-authorized browser session, such as LinkedIn activity,
company writing, podcasts, talks, newsletters, GitHub, X, YouTube, and local CRM
notes. It must not bypass access controls, expose session secrets, perform social
actions, scrape private data, or turn inferences into private-fact claims.
Deep ICP mode also inspects the target company's hiring footprint because open
roles and hiring posts reveal committed investment, capability gaps, and timing
signals that company positioning alone may hide.

Reports use minimal frontmatter for discovery and entity linking. Put judgment,
confidence, pain hypotheses, questions, and next actions in the report body.
`entity_refs` contains stable IDs compiled from `.farplane/entities/*.md`; one report
may reference a person, their organization, or several related entities. Do not
duplicate entity records or add pipeline fields to the report schema. When the
ledger is empty and CRM writes are not approved, use `entity_refs: []` and
include a proposed-but-not-applied CRM delta in the body.

Default storage:

- Project-specific target: `.farplane/customer-research/reports/YYYY-MM-DD-<person>.md`
- No project target: `~/.farplane/customer-research/reports/YYYY-MM-DD-<person>.md`
- Canonical entity source: `.farplane/entities/*.md` or `~/.farplane/entities/*.md`
- Compiled entity lookup index: `.farplane/entities/index.json` or
  `~/.farplane/entities/index.json`; use it for identity resolution, then read
  the matched `path` for full canonical Markdown
- Cross-skill discovery pattern: `.farplane/*/reports/**/*.md`

Keep the work ethical and source-labeled: use public or supplied business
context, label inference, and do not present private or guessed personal facts
as truth.

## Skill Signature

```text
customer_research(target, call_context?, project_context?, output_root?, mode?)
  -> customer_research_report | deep_person_icp_report + crm_entity_delta?
state: reads(public/supplied/operator-authorized professional sources,
       local project context, optional CRM entities);
       writes(skill-local report markdown, optional CRM entity create/update)
gates: target_bound; sources_labeled; inference_labeled; minimal_frontmatter;
       conversation_plan_present; no_private_dossiering; public_or_supplied_evidence_only;
       deep_icp_inferences_are_testable_hypotheses; source_access_labeled;
       person_signal_card_present; opening_summary_sourced;
       first_move_inside_signal_card;
       company_hiring_coverage_recorded_when_deep_icp_and_company_bound
routes: research:user-grounding | research:source-synthesis | solution-shaping |
        first-value-outreach
fails: bloated frontmatter; fake certainty; generic pitch; creepy personal dossier;
       uncited claims; biography_or_source_dump; CRM pipeline modeling
```

## Phase Boundary

Use `research:*` as the evidence method when the person, company, field, or
source set needs grounding. Use `solution-shaping` only for the "how I can help"
section after the problem hypotheses are labeled. Keep planning and report
authoring inline unless a separate research artifact is needed. When the next
goal is to earn a first conversation by contributing before a commercial ask,
hand the finished report and one traceable professional signal to
`first-value-outreach` rather than drafting generic free-help or offer copy.

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
  - [ ] For a supplied web profile, use the Codex in-app Browser when available
        to inspect the rendered page before declaring it
        inaccessible. Never log in, enter credentials, export cookies, or assume
        access to a private session. When the operator explicitly attaches and
        authorizes a browser session, inspect it read-only: do not message,
        connect, follow, react, publish, change settings, or expose auth state.
        If blocked, record `auth_walled` and continue with public company pages,
        indexed material, interviews, talks, and operator-supplied exports.
  - [ ] For deep ICP mode, collect public or supplied professional signal
        categories: repeated topics, posts, comments or reactions visible to
        the operator, talks, interviews, company writing, product launches,
        hiring signals, project history, and language they reuse.
  - [ ] When deep ICP has an identifiable company, run a bounded hiring scan:
        inspect the official careers/ATS surface, company LinkedIn jobs, company,
        founder, or recruiter hiring posts, and relevant job-board or indexed
        listings. Record coverage even when no current roles surface; otherwise
        record `not_applicable` with the missing company-binding reason.
  - [ ] Preserve each hiring signal's status and recency as `active`,
        `closed_or_stale`, or `status_unknown`; use `none_surfaced` only for an
        inspected source with no visible roles. Extract function, seniority,
        location, responsibilities, systems, metrics, and repeated capability
        themes. Treat hiring as revealed investment, not proof of dysfunction.
  - [ ] Refuse or narrow any request to bypass LinkedIn limits, access content
        the operator cannot ordinarily view, infer sensitive traits, perform
        social actions, run bulk extraction, or monitor a person over time.
  - [ ] Label each source `full_public`, `indexed_snippet`, `operator_supplied`,
        `operator_authorized_session`, `auth_walled`, or `not_inspected`. Do not
        give a claim high confidence when it depends only on an indexed snippet
        or one isolated interaction.
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
  - [ ] For deep ICP mode, use `templates/deep-person-icp.md`. Open with one
        sourced paragraph of no more than 150 words covering who they are,
        current role, one to three largest relevant achievements, and why they
        matter now. This is the first prose after the title/frontmatter—before
        any ask, bullets, or analysis. Do not narrate a full career history.
  - [ ] Promote only signals that change a likely next action. The default
        Person Signal Card contains at most three goals/pressures, three active
        problem hypotheses, three relationship surfaces, and three correction
        questions. Fold relevant hiring, interaction, language, project,
        trigger, objection, and timing evidence into those entries rather than
        adding mandatory standalone sections.
  - [ ] Preserve provenance, access, date, confidence, alternative explanation,
        and falsifier in a compact evidence block or linked appendix. Deep
        research may increase confidence without increasing the main brief
        linearly.
- [ ] 4. Shape the conversation.
  - [ ] Use [solution-shaping](../solution-shaping/SKILL.md) for the pain
        hypotheses and "how I can help" section when the call has an outreach,
        client, or MVP angle.
  - [ ] Include warm openers, useful topics, questions to ask, conversation
        risks, and follow-up hooks.
  - [ ] For deep ICP mode, convert the highest-information signals into no more
        than three correction-seeking questions, one recommended first move,
        one smallest credible help angle, and a concise avoid note.
  - [ ] Keep the first move, help, and avoid guidance inside the Signal Card.
        When the operator requests a timed call plan, add at most four short
        timing bullets; do not recreate standalone objection, language,
        follow-up, hiring, or conversation-plan sections.
  - [ ] The Person Signal Card is not complete until `Recommended First Move`
        and `Correction Questions` appear as its subsections before evidence.
        Do not place a standalone ask before the card or render first move,
        smallest help, or avoid as sibling top-level sections.
  - [ ] Prefer correction-seeking questions over leading pitch questions.
  - [ ] When the target is not yet ready for a commercial offer, hand one
        traceable professional signal, relationship goal, evidence gaps, and
        smallest credible help angle to
        [first-value-outreach](../first-value-outreach/SKILL.md) for a bounded
        useful contribution and correction-first unsent message.
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
  - [ ] Source access mode is explicit, snippet-only claims are not overstated,
        and the opening paragraph plus Person Signal Card surface the first
        decision without requiring the evidence appendix.
  - [ ] Default decision groups stay within three entries; additional findings
        are linked or included only when exhaustive coverage was requested.
  - [ ] Every promoted goal, pressure, problem, and relationship surface has an
        explicit confidence or uncertainty label plus a falsifier or boundary.
  - [ ] Deep ICP reports state which hiring surfaces were inspected, distinguish
        active roles from stale or unknown-status posts, and name what would
        falsify each capability-gap inference.
  - [ ] The report helps the operator lead a better call rather than pretending
        to know the person privately.
  - [ ] The conversation plan includes concrete questions and at least one
        useful non-obvious angle.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [templates/report.md](templates/report.md) - default customer research report
  template; use for every report unless a project supplies a stricter template.
- [templates/deep-person-icp.md](templates/deep-person-icp.md) - use when the
  operator asks for deep person-level ICP, buyer psychology, public signal
  mining, or outreach problem hypotheses.
- [examples/first-call/example.md](examples/first-call/example.md) - short
  example showing minimal frontmatter and report-body reasoning.
- [examples/deep-person-icp/example.md](examples/deep-person-icp/example.md) -
  synthetic example showing deep ICP signal mapping without private dossiering.

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
- Do not treat a search snippet, rendered public page, operator-supplied export,
  and auth-walled URL as equivalent evidence.
- Do not make "deep ICP" mean creepy surveillance. If the useful source would
  require login-only scraping, evading platform limits, private communities, or
  personal-life inference, ask for an operator-supplied export or omit it.
- Do not overfit to one post, like, comment, or public interaction. Prefer
  repeated professional patterns and label single-signal hypotheses as weak.
- An operator-authorized session expands visibility, not permission. Keep it
  read-only, bounded to the named target, and free of credential or cookie
  extraction; do not turn it into ongoing monitoring.
- A job post proves recruiting intent at a point in time, not an unsolved pain.
  Keep current status, role age, alternative explanations, and falsifiers visible.
- Do not put a new summary above the old category-complete report. Replace
  duplicated narrative, signal, hiring, trigger, objection, language, outreach,
  and conversation sections with the bounded Person Signal Card.

## Reference Map

- [../research/SKILL.md](../research/SKILL.md) - load when external source
  grounding is needed.
- [../solution-shaping/SKILL.md](../solution-shaping/SKILL.md) - load when the
  report needs pain hypotheses and a realistic MVP/help angle.
- Codex in-app Browser - use when a supplied profile or company page needs
  rendered browser inspection.
- [First Value Outreach](../first-value-outreach/SKILL.md) - load after the
  person and one professional signal are resolved when the next step is a
  contribution-first approach rather than a commercial offer.

## Output

Write a Markdown report with this frontmatter shape:

```yaml
---
skill: "customer-research"
entity_refs:
  - "person-name" # Or [] when CRM writes are not approved.
name: "Person Name"
links:
  - "https://example.com/profile"
industry: "Industry or field, when useful for search."
relevance: "Why this person is relevant to the call or project."
created_at: "YYYY-MM-DD"
---
```

Then include the research and conversation plan in the body. For deep ICP mode,
use the same minimal frontmatter and the compact Person Signal Card; link bulky
evidence instead of reproducing a source-by-source biography.
