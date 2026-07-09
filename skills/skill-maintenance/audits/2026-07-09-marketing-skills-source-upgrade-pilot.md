---
skill: skill-maintenance
date: 2026-07-09
change_type: source_upgrade_pilot
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/copywriting-advisor; skills/lead-scout; skills/ad-advisor; skills/seo-content-advisor
after_ref: skills/copywriting-advisor; skills/lead-scout; skills/ad-advisor; skills/seo-content-advisor
reasoning_basis: source_synthesis
proof_artifacts: []
eval_required: no
---

# Marketing Skills Source Upgrade Pilot

## Scope

Pilot `upgrade_skill_from_sources` across four recently created marketing
skills:

- `copywriting-advisor`
- `lead-scout`
- `ad-advisor`
- `seo-content-advisor`

Correction note: the first pilot pass was too shallow. After operator
correction, four source-upgrade subagents were spawned, one per skill, and this
artifact was rebuilt from their source packets and adopt/adapt/reject/defer
decisions.

Subagent lanes:

- `019f44e3-6e4e-7490-9748-10d542b51513`: `copywriting-advisor`
- `019f44e3-919a-7883-86d7-6ce522c90625`: `lead-scout`
- `019f44e3-b3a7-7d53-a0c6-a672bfaeaa0e`: `ad-advisor`
- `019f44e3-d1f3-79b3-ad9f-732bc19658f8`: `seo-content-advisor`

## Source Packet

| Skill | Sources | Source Confidence | Workflow Signal |
| --- | --- | --- | --- |
| `copywriting-advisor` | Copyhackers conversion-copy process; CXL voice-of-customer research; Wynter B2B message layers; `Breakthrough Advertising` public notes; `Great Leads` interview/notes; MECLABS heuristic | high for practitioner/framework sources, medium-high for book notes | high |
| `lead-scout` | Pipedrive B2B prospecting; Apollo prospecting workflow; Outreach prospecting guide; `Predictable Revenue` interview/official summary; `Fanatical Prospecting` public notes; `New Sales. Simplified` review/notes | high to medium | high |
| `ad-advisor` | Meta learning phase, A/B testing, conversion lift, Marketing API docs; Hunch creative-testing guide; Common Thread creative-testing framework; `Scientific Advertising`; `Breakthrough Advertising` notes; `How Brands Grow` / Ehrenberg-Bass summary | high for official Meta/docs, medium-high for practitioner/book sources | high |
| `seo-content-advisor` | Google people-first content docs; Ahrefs SEO content guide; Content Harmony SEO briefs; `They Ask, You Answer`; `Product-Led SEO` notes/framework; `Content Design` notes/interview | high for Google/practitioner sources, medium to medium-high for book notes | high |

## Best-Of-Worlds Decisions

### copywriting-advisor

- `adopt`: message-layer QA: clarity, relevance, value, differentiation,
  friction, and proof.
- `adopt`: copy-gap audit for rewrites: compare current copy against source
  atoms for missing needs, benefits, anxieties, proof, and reader language.
- `adopt`: dominant desire and market sophistication before choosing page
  angle or opening lead.
- `adapt`: treat formulas and lead types as diagnostic structures tied to
  reader stage, market sophistication, objection, proof, and CTA rather than as
  fill-in templates.
- `adapt`: MECLABS-style conversion diagnosis into a lightweight weakest-factor
  field: motivation, value, friction, anxiety, or incentive.
- `reject`: copying example ads, importing headline/power-word lists, or adding
  a long formula encyclopedia to first-load `SKILL.md`.
- `defer`: a full long-form direct-response or message-testing reference.

Delta:

- Updated `SKILL.md`, `qa_checklist.md`, and `eval_task.json` with
  dominant-desire, market-sophistication, lead-posture, message-layer, and
  conversion-diagnostic gates.

### lead-scout

- `adopt`: ICP-before-search, negative-fit criteria, stage-exit gates, and
  prospect tiering.
- `adapt`: add `scout_mode` and prospecting hypothesis: `why them`, `why now`,
  `why this source`, and `why this outreach channel`.
- `reject`: turning lead scout into outreach copywriting, CRM pipeline design,
  unbounded scraping, whole-vertical dumps, or raw volume scoring.
- `defer`: TAM/SAM/SOM sizing and prospecting-sequence/cadence design.

Delta:

- Updated `SKILL.md`, `qa_checklist.md`, and `eval_task.json` with scout mode,
  ICP/negative fit, prospect tiers, stage-exit, timely trigger, and channel-fit
  gates.

### ad-advisor

- `adopt`: hypothesis-first campaign gate, measurement-method gate, and keyed
  traceability for test evidence.
- `adapt`: platform learning/stability risk, one-variable learning discipline,
  market awareness/sophistication, category entry point, distinctive brand
  asset, and growth-targeting over-narrowing warning.
- `reject`: live spend or platform-specific tactical detail without current
  docs, account binding, and approval; reject ad-ranking-only proof and
  uninterpretable multi-variable changes.
- `defer`: a platform-specific Meta reference until the workflow needs actual
  CLI/API execution or lift-study math.

Delta:

- Updated `SKILL.md`, `qa_checklist.md`, and `eval_task.json` with primary
  hypothesis, isolated variable, matched setup, measurement method,
  interpretable testing, and platform-stability risk.

### seo-content-advisor

- `adopt`: Google-style Who/How/Why, SERP intent fingerprint, and buyer-question
  angle menu for commercial content.
- `adapt`: add `information gain`, product proof fit, and article-format fit as
  first-class packet fields and QA/eval requirements.
- `reject`: keyword stuffing, ranking-page paraphrase, and generic AI article
  outlines; reject matching top results exactly when it clones rather than
  satisfies intent.
- `defer`: full product-led SEO asset architecture and broader content strategy.

Delta:

- Updated `SKILL.md`, `qa_checklist.md`, and `eval_task.json` with SERP intent
  fingerprint, information gain, article-format fit, Who/How/Why, and
  commercial buyer-question gates.

## Proof Plan

- Run `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Confirm capped skills stay within 10 todos, 5 QA checks, and 5 eval rows.
- Review changed skill surfaces against `skill-contract`,
  `integration-readiness`, and `evidence-quality`.

## Residual Risk

- This repaired pilot used four subagent source packets and current web
  browsing, but still did not run local `summarize` transcript extraction for
  every book-summary video. The workflow reference now requires that for a full
  single-skill upgrade pass.
- Several book inputs are public notes, interviews, or secondary summaries;
  they are useful for transferable workflow extraction but should not be
  treated as primary book coverage.
- The target skills remain untracked packages in this worktree, so final PR
  review should inspect the whole packages once staged.
