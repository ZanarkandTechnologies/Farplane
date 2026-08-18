---
title: Newsletter Writer QA Checklist
owner: newsletter-writer
status: active
kind: qa-checklist
applies_to:
  - newsletter-blueprints
  - newsletter-issues
---

# Newsletter Writer QA Checklist

Read before drafting and apply again before calling an issue ready for human
review.

```text
newsletter_check(issue, source_material, voice_examples?)
  -> pass | revise | blocked
```

## Checklist

- [ ] The audience, list expectation, issue goal, verified raw material or
  editorial-hypothesis boundary, and `voice_mode` are explicit; missing
  optional metadata does not stall a truthful draft, and missing voice evidence
  does not become an invented story, feeling, quotation, or personal claim.
- [ ] The issue uses one format and one reader promise. Editorial formats carry
  one central idea; release digests group only high-impact changes into two to
  four themes rather than forcing a personal story or dumping every activity.
- [ ] Three subjects are each at most 45 characters, preview text is at most 90
  characters and additive, and the opening is concrete without boilerplate or
  clickbait the body cannot cash.
- [ ] The body is scannable. Editorial paragraphs stay at three sentences or
  fewer and normally target 300–800 words; release digests use a one- or
  two-sentence factual opener followed by indented `Changed`, `Impact`, and
  `Evidence` units. Editorial formats use one CTA; release digests use at most
  one. Any promotion is confined to the P.S. and makes only verified claims
  unless the operator explicitly requests a promotional issue.
- [ ] Every factual claim is attributable, unsupported anecdotes are cut,
  internal proof paths stay out of reader copy, source gaps are visible in send
  notes, and human fact/privacy/voice/link/media/publication approval remains
  required.

## Reviewer Prompt

```text
Review the issue against skills/newsletter-writer/qa_checklist.md and its bound
source material. Return pass, revise, or blocked. Focus on format fit, impact
hierarchy, specificity, voice fidelity, truthful sourcing, mobile scanning,
and the human publication gate.
```
