---
title: Reference Grounding QA / Review Checklist
owner: reference-grounding
status: active
kind: qa-checklist
applies_to:
  - grounding-notes
  - evidence-backed-claims
---

# Reference Grounding QA / Review Checklist

Use this checklist before gathering evidence and again before returning a
Grounding Note. For durable, high-stakes, or externally dependent claims, ask an
independent reviewer/subagent to apply it to the evidence note.

```text
grounding_check(claim, source_need, sources_checked, local_impact)
  -> pass | violation | deferral
```

## Checklist

- [ ] One claim, decision, expectation, or comparison is in scope, with local
  baseline needs identified when repo context matters.
- [ ] Source need is classified before searching: local-only, official/current,
  maintained implementation, peer/product, standards, or user-provided source.
- [ ] Primary sources and real implementations are preferred, and claims rely
  only on sources that were opened or inspected.
- [ ] Local-only evidence is not used for current facts, best practice, latest
  behavior, law, pricing, external API behavior, or peer expectations.
- [ ] The Grounding Note states source class, sources checked, evidence,
  confidence, local impact, and any routed evidence gap without expanding into
  a full research brief.

## Reviewer Prompt

```text
Review the Grounding Note against skills/reference-grounding/qa_checklist.md.
Return pass, violation, or deferral for each failed check.
Focus on whether source class, actual inspection, confidence, and local impact
support the claim.
Do not perform a new research pass unless the note's evidence gap requires it.
```
