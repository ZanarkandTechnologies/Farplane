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

## Preflight

- [ ] One claim, decision, expectation, or comparison is in scope.
- [ ] Local baseline needs are identified when repo context matters.
- [ ] Source need is classified before searching: local-only, official/current,
  maintained implementation, peer/product, standards, or user-provided source.
- [ ] Primary sources and real implementations are preferred over commentary.
- [ ] The task has not silently expanded into a full research brief.

## Final Review

- [ ] The Grounding Note states source class used and sources actually checked.
- [ ] Claims do not rely on sources that were only searched but not opened or
  inspected.
- [ ] Local-only evidence is not used for current facts, best practice, latest
  behavior, law, pricing, external API behavior, or peer expectations.
- [ ] Evidence, confidence, and local impact are explicit.
- [ ] Any unresolved evidence gap is routed to the caller or to the right
  `research:*` method.
- [ ] The answer does not keep collecting sources after the active decision is
  sufficiently grounded.

## Reviewer Prompt

```text
Review the Grounding Note against skills/reference-grounding/qa_checklist.md.
Return pass, violation, or deferral for each failed check.
Focus on whether source class, actual inspection, confidence, and local impact
support the claim.
Do not perform a new research pass unless the note's evidence gap requires it.
```
