---
title: SEO Content Advisor QA Checklist
owner: seo-content-advisor
status: active
kind: qa-checklist
applies_to:
  - seo-content-advisor
---

# SEO Content Advisor QA Checklist

Use this checklist before drafting and again before claiming article quality,
SEO fit, or publication readiness.

```text
seo_content_check(article_packet, target_stage?)
  -> pass | revise | blocked
```

## Preflight

- [ ] Audience, product, topic, search intent, target stage, proof/source set,
  freshness need, reader promise, and final-publication human gate are bound or
  explicitly marked as assumptions.

## Article Checks

- [ ] The article satisfies a real search intent and answers the main question
  early instead of hiding value after a long generic intro; SERP intent
  fingerprint, real questions, and article-format fit are visible.
- [ ] The outline includes original value: experience, example, data, product
  insight, comparison, workflow, or point of view.
- [ ] The content strategy would not transfer unchanged to a generic writing
  skill: it names the intent angle, reader promise, original proof asset,
  information gain, Who/How/Why proof, buyer-question angle when commercial,
  freshness risk, do-not-claim boundary, and section jobs.
- [ ] Claims, titles, meta, headings, FAQ candidates, internal links, weakest
  section, proof gaps, freshness risks, do-not-claim list, next owner, and
  blockers are visible and reader-serving; keywords are used naturally as
  labels for the problem, not stuffed into headings or repeated without value.

## Reviewer Prompt

```text
Review the article packet against skills/seo-content-advisor/qa_checklist.md.
Return pass, revise, or blocked. Focus on people-first usefulness, search
intent, originality, proof, freshness, keyword restraint, and publication
approval safety.
```
