---
title: SEO Article Method
owner: copywriting
status: active
kind: skill-reference
---

# SEO Article Method

Load after `SKILL.md` selects `seo`. Useful search content satisfies the
reader first, adds something the current results lack, matches intent, and
makes important claims verifiable. Keywords label the reader's problem; they
never replace substance.

```text
seo(audience, product, topic, search_intent?, keywords?, proof?,
    freshness_need?, draft_stage?: brief | outline | draft | refresh)
  -> article_packet + seo_qa_verdict | format_block | blocked_report
```

## 1. Bind the search and reader job

Resolve audience, product, topic, search intent, keywords, proof, freshness
need, target stage (brief, outline, draft, refresh, title/meta, FAQ), and the
publication boundary. When the audience, promise, or product language is
fuzzy, run `page` mode's message map first; the article reuses its reader
words.

## 1b. Pick the topic from search data when none is given

Adapted from treg's `seo-weekly` endpoints and Monid's SEO/GEO loop. Quote
each paid call first and stay inside the weekly spend cap; the gateway per job
is in the tool loadout note in `~/.farplane/memory/`.

1. **Striking distance:** read the site's own Search Console queries at
   positions 8-15 (`search-console.performance`, free on the operator's own
   property). These pages need a refresh, not a new article.
2. **Keyword gap:** pull competitors' ranked keywords
   (`google.domain.ranked_keywords`) and keep terms they rank for and the site
   does not; price them with keyword volume.
3. **AI-answer check:** for the top 10-12 buyer questions, record which
   domains AI answers cite (`ai-search.mentions` or Ahrefs AI responses). A
   cited host is a pitch or guest-post target, not only a competitor.
4. Queue topics by demand, gap and information gain; refresh beats new.

Tracking after publication (dated SERP position and AI-citation snapshots,
reviewed every two weeks) is a recurring job: set it up through
`automation-advisor`, never by hand each week. Published receipts: a full site
teardown about $0.63; daily SERP rows cost cents.

## 2. Check the SERP before outlining

Search the live query (web search, or a SERP tool through `treg` within the
spend cap) and record the intent fingerprint:

- content type: guide, list, template, comparison, tool, product page, video;
- content format: steps, table, templates, long explainer;
- dominant angle shared by the top results;
- SERP features: People Also Ask, snippets, video, local, shopping;
- freshness requirement: do the results carry recent dates;
- real questions readers ask, and mixed-intent risks.

State `Grounding:` with the source class. If no search is possible, mark the
fingerprint `unverified` and keep the brief a draft; never present an
unchecked fingerprint as observed.

## 3. Require information gain

Name what this article adds beyond paraphrasing the ranking pages and generic
AI output: first-hand experience, an original example, data, a comparison, a
product proof, a workflow, a decision rule, or a sharper point of view. Mine
it from source material the same way as page copy (see
[source mining](source-mining-and-swipe-workflow.md)). With no information
gain, return `revise` and the missing input; do not write a rewrite of the
top results.

## 4. Check format fit and block when an article is wrong

When a tool, calculator, comparison table, template download, video, docs
page, or FAQ serves the query better than prose, return `format_block`: say
plainly that an article is the wrong format, name the better format and why
the SERP or reader job points to it, and stop. Route a page-shaped answer to
[landing-page](../../landing-page/SKILL.md) and durable product docs to the
project's docs owner.

Example: "mortgage repayment calculator" shows calculators in every top
result -> block the article; recommend an embedded calculator with a short
explainer beneath it.

## 5. Produce the article packet

Draft the intent note, working title options, meta description, outline with
section jobs, proof requirements, internal-link ideas, FAQ candidates, and
draft sections when requested. Answer the query early. Use keywords naturally
as labels; do not stuff them or let them drive a generic outline. Mark every
fact that needs a date, source, expert review, screenshot, or product proof
before publication. Run the [final pass](final-pass.md) on drafted prose.

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

## 6. SEO QA

Verdict `pass | revise | blocked` covering people-first usefulness, intent
fit, information gain, proof, freshness risk, keyword use, weakest section,
and the human publication gate.

Fails to watch: keyword stuffing; a generic AI article; a rewrite of ranking
pages; unsupported expertise claims; a stale fact without a date; promised
rankings, traffic, or conversions; publishing or marking expert or regulated
claims ready without human review.

See [the article brief example](../examples/article-brief/example.md) for a
compact packet.
