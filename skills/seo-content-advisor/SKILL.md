---
name: seo-content-advisor
description: "Turn an audience, product, and search topic into a people-first SEO article brief, draft, and content QA verdict."
tier: 3
group: marketing
source: local
template_uses:
  skill-template: "0.3.7"
  skill-surface-budget: "0.1.0"
allowed-tools: Read, Glob, Grep, web_search
eval: evals/evals.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["copywriting-advisor", "research", "doc-advisor"]
---

# SEO Content Advisor

## Context

Use this skill when an audience, product, and topic need an SEO article brief,
outline, draft, refresh plan, title/meta options, FAQ ideas, or content-quality
QA. It owns people-first search content. It does not own final publication,
technical site implementation, paid promotion, social posting, or unsupported
performance claims.

Grounding from current SEO guidance: useful search content must satisfy the
reader first, show original value or expertise, match intent, and make
important claims verifiable. Keywords help describe the page; they do not
replace substance.

## Skill Signature

```text
seo_content_advisor(audience, product, topic, search_intent?,
                    keywords?, proof?, freshness_need?, draft_stage?)
  -> article_brief_or_draft + seo_qa_verdict | blocked_report
state:
  reads(user brief, supplied proof/source material, current search guidance,
        qa_checklist.md, copywriting-advisor output when voice/message matters)
  writes(article brief or draft only when caller owns an artifact path)
gates:
  search_intent_bound; reader_promise_named; original_value_present;
  serp_intent_fingerprint_named; article_format_fit_checked;
  who_how_why_named; proof_sources_named; copy_voice_checked;
  publication_human_gate_named
routes:
  copywriting-advisor | research | doc-advisor | social-content | review
fails:
  keyword_stuffing; generic_ai_article; ranking_page_rewrite;
  unsupported_expertise_claims; stale_fact_without_date; publishing_without_review
```

## Phase Boundary

Use current web grounding when search guidance, SERP expectations, freshness,
or peer article patterns materially affect the answer. Use `research` when the
topic needs source synthesis before writing. Use `copywriting-advisor` when the
message, audience emotion, or product voice is not yet sharp. Use `doc-advisor`
when the result is durable documentation rather than marketing content. Use
`review` before publishing, brand-sensitive claims, or expert-content claims.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the search and reader job.
  - [ ] Resolve audience, product, topic, search intent, keywords, proof,
        freshness need, target stage, and publication boundary.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
- [ ] 2. Ground the article before drafting.
  - [ ] Use current web or supplied-source grounding when search expectations,
        facts, freshness, or competitive norms affect the brief.
  - [ ] Identify the SERP intent fingerprint before outlining: content type,
        content format, dominant angle, SERP features, freshness need, real
        questions, and mixed-intent risks.
  - [ ] Name the reader promise, original angle, source/proof set, and what the
        article will not claim.
  - [ ] State the information gain: the example, experience, data, comparison,
        product proof, or decision rule this article adds beyond ranking-page
        paraphrase and generic AI output.
  - [ ] Check article format fit; block or reroute when the reader need is
        better served by a tool, calculator, comparison table, video, docs page,
        FAQ, or sales enablement asset.
  - [ ] Route to `copywriting-advisor` first when the audience, promise, or
        product language is fuzzy.
- [ ] 3. Produce the article packet.
  - [ ] Draft the search-intent note, working title options, meta description,
        outline, section jobs, proof requirements, internal-link ideas, FAQ
        candidates, and draft sections when requested.
  - [ ] Use keywords naturally as labels for the reader's problem; do not
        stuff them or let them drive a generic outline.
- [ ] 4. Make usefulness and originality visible.
  - [ ] Include the unique experience, example, data, comparison, workflow,
        opinion, or product insight that makes the article worth reading.
  - [ ] Mark facts that need dates, sources, expert review, screenshots, or
        product proof before publication.
- [ ] 5. Finish with SEO/content QA and handoff.
  - [ ] Apply `qa_checklist.md` to the finished packet.
  - [ ] Name the SEO QA verdict, weakest section, proof gaps, freshness risk,
        final publication/human gate, and next owner.
  - [ ] Route social derivatives to `social-content`, durable docs to
        `doc-advisor`, or high-stakes claims to `review`.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Article packet:

```text
Audience:
Product:
Topic:
Search intent:
SERP intent fingerprint:
  content type:
  content format:
  dominant angle:
  SERP features:
  freshness requirement:
Real questions:
Reader promise:
Original angle:
Information gain:
Buyer-question angle:
Article format fit:
Who / How / Why:
Proof/source set:
Title options:
Meta description:
Outline:
  H1:
  sections:
Section draft:
Internal links:
FAQ candidates:
Freshness notes:
Do-not-claim:
SEO QA verdict:
Next owner:
```

Short positive example:
[examples/article-brief/example.md](examples/article-brief/example.md) shows a
people-first article brief that reuses copywriting discipline without turning
SEO into keyword stuffing.

## Gotchas

- Do not rewrite the top ranking pages into a generic article. Add original
  experience, proof, examples, or a sharper point of view.
- Do not promise rankings, traffic, or conversion outcomes.
- Do not publish or mark expert/regulated claims ready without human review.
- Do not confuse an SEO article with product documentation; use `doc-advisor`
  when the reader job is durable product understanding.

## Reference Map

- [qa_checklist.md](qa_checklist.md) - read before drafting and apply before
  completion.
- [copywriting-advisor](../copywriting-advisor/SKILL.md) - use
  when audience emotion, message spine, or product voice needs sharpening
  before article drafting.
- [research](../research/SKILL.md) - use for source synthesis,
  parity, official docs, or user-grounding when the topic needs evidence first.
- [doc-advisor](../doc-advisor/SKILL.md) - use when the article is
  really durable documentation or knowledge-base content.
- [social-content](../social-content/SKILL.md) - use for social
  derivatives after the article packet exists.

## Output

- `article_brief_or_draft`: intent, reader promise, original angle, title/meta,
  outline, proof requirements, draft sections, links, FAQ candidates, and
  freshness notes.
- `seo_qa_verdict`: pass, revise, or blocked with people-first usefulness,
  intent fit, originality, proof, freshness, keyword use, and human gate.
- `blocked_report`: missing topic, audience, product, proof, source access,
  search-intent clarity, or approval boundary.
