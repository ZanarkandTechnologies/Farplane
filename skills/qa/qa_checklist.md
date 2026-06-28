---
title: QA Skill Runtime Checklist
owner: qa
status: active
kind: qa-checklist
created_at: 2026-06-22
updated_at: 2026-06-27
applies_to:
  - qa
  - ticket-proof
---

# QA Skill Runtime Checklist

Use this for material QA reports and after changing the `qa` skill.

## Checks

1. `ticket-proof-read`
   - Question: Did QA read the selected ticket, `Done`, `QA Strategy`, proof weight,
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

4. `critical-path-reconciled`
   - Question: For material feature work, did QA reconcile evidence against the
     ticket's critical-path proof notes in `QA Strategy`, including smaller
     ordered sanity checks and any unrun full-path risk?
   - Violation: QA passes proxy checks while the claimed workflow, hook
     lifecycle, user path, or session path remains implicit or unexercised.

5. `visual-judgment-separated`
   - Question: For UI proof, did `visual-qa` judge captured screenshots?
   - Violation: Browser capture is treated as visual judgment.

6. `best-evidence-named`
   - Question: Does the QA result name `best_evidence`, preferably an image path
     for UI/user-visible tickets?
   - Violation: Final reporting cannot show the strongest proof.
