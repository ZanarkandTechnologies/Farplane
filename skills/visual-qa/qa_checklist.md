---
title: Visual QA Runtime Checklist
owner: visual-qa
status: active
kind: qa-checklist
created_at: 2026-06-22
updated_at: 2026-06-22
applies_to:
  - visual-qa
  - screenshots
  - ui-proof
---

# Visual QA Runtime Checklist

Use this after changing `visual-qa` or before accepting a visual QA report.

## Checks

1. `expected-state-present`
   - Question: Did the report read `design.md` when present, or the ticket
     `Agent Contract` and declared screens/states when no design file exists?
   - Violation: The report invents the expected UI.

2. `screenshot-present`
   - Question: Does each judged screen/state cite a screenshot or image?
   - Violation: The verdict relies only on prose, logs, or route completion.

3. `geometry-assertions`
   - Question: Does each visual verdict include layout/geometry assertions or
     explicitly fail them as missing?
   - Violation: The report gives aesthetic comments without spatial proof.

4. `best-image`
   - Question: Does the report identify the best image evidence item for
     ticket writeback and final response rendering?
   - Violation: Downstream QA cannot surface visual proof to the operator.

5. `capture-boundary`
   - Question: Does `visual-qa` avoid browser orchestration and ticket
     writeback ownership?
   - Violation: It duplicates `qa` or `qa-tester`.
