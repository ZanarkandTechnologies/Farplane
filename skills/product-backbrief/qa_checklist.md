---
title: Product Backbrief QA Checklist
owner: product-backbrief
status: active
kind: qa-checklist
applies_to:
  - product-alignment-backbriefs
---

# Product Backbrief QA Checklist

Read before producing a material product backbrief and apply again before
returning it for operator confirmation.

```text
product_backbrief_check(sources, backbrief) -> pass | revise | source_gap
```

## Checklist

- [ ] The product boundary and alignment question are explicit, and available
  product artifacts or task-recap evidence outrank transcript memory.
- [ ] Confirmed decisions, inferred assumptions, conflicts, and missing context
  remain visibly distinct; coherent prose does not manufacture agreement.
- [ ] The response tells one operated user story from trigger to value instead
  of returning a feature inventory, transcript chronology, or task-status card.
- [ ] When relationships matter, the ASCII view uses the same nouns as the
  story and makes object, state, ownership, or data-flow boundaries legible.
- [ ] The backbrief includes one realistic example, names boundaries or
  non-goals, asks two to five high-risk alignment questions, remains read-only,
  and is labeled proposed rather than approved.

## Reviewer Prompt

```text
Review the product backbrief against skills/product-backbrief/qa_checklist.md.
Return pass, revise, or source_gap for each failed check. Focus on whether the
story exposes rather than conceals possible misunderstanding. Do not rewrite
the product or approve downstream implementation.
```
