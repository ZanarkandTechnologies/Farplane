---
title: QA Skill Runtime Checklist
owner: qa
status: active
kind: qa-checklist
created_at: 2026-06-22
updated_at: 2026-06-22
applies_to:
  - qa
  - ticket-proof
---

# QA Skill Runtime Checklist

Use this for material QA reports and after changing the `qa` skill.

## Checks

1. `ticket-proof-read`
   - Question: Did QA read the selected ticket, `Done / Proof`, proof weight,
     and any design baseline before collecting evidence?
   - Violation: QA improvises a flow from chat or route intuition.

2. `delegated-capture`
   - Question: For browser/user-visible proof, did `qa-tester` or an equivalent
     delegated lane own operation and capture when available?
   - Violation: The coordinator self-certifies operated evidence.

3. `artifact-set-complete`
   - Question: Are `report.md`, `result.json`, and required supporting
     screenshots/logs/snapshots present or explicitly blocked?
   - Violation: QA passes with only prose or terminal output.

4. `visual-judgment-separated`
   - Question: For UI proof, did `visual-qa` judge captured screenshots?
   - Violation: Browser capture is treated as visual judgment.

5. `best-evidence-named`
   - Question: Does the QA result name `best_evidence`, preferably an image path
     for UI/user-visible tickets?
   - Violation: Final reporting cannot show the strongest proof.
